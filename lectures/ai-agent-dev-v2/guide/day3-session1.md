# Day 3 Session 1 — MCP(Function Calling) 고급 설계

> **목표**: JSON Schema Tool 정의 전략부터 Multi-tool Routing, 실패 복구 패턴까지
> **시간**: 2시간 | **대상**: AI 개발자, 데이터 엔지니어, 기술 리더

---

## 1. 왜 중요한가

LLM이 Tool을 잘못 선택하면 결과는 예측 불가능하다.
Tool 정의가 모호하면 모델은 잘못된 인수를 생성한다.
→ **Tool 설계 품질 = Agent 신뢰도**

2026년 기준, Agent 시스템의 생산 장애 원인 1위는
잘못 설계된 Tool 스키마다(Anthropic 내부 데이터).
Tool을 정확하게 정의하는 것은 프롬프트 설계만큼 중요하다.

---

## 2. 핵심 원리

### 2.1 JSON Schema Tool 정의 전략

**기본 구조 3요소**

| 요소 | 역할 | 설계 원칙 |
|------|------|-----------|
| `name` | Tool 식별자 | 동사_명사 패턴, 명확한 의미 |
| `description` | 언제 쓸지 설명 | 50자 이내, 조건 명시 |
| `parameters` | 입력 스키마 | 필수/선택 구분, 예시 포함 |

**description 설계 원칙**

```
나쁜 예: "Gets weather data"
좋은 예: "사용자가 특정 도시의 현재 날씨를 물어볼 때 호출.
         과거/예보 데이터는 get_weather_forecast 사용."
```

→ 경쟁 Tool과 구분되는 조건을 명시해야 한다.

**parameters 설계 원칙**

```json
{
  "type": "object",
  "properties": {
    "city": {
      "type": "string",
      "description": "도시명 (영문 또는 한글). 예: Seoul, 서울",
      "examples": ["Seoul", "New York", "도쿄"]
    },
    "unit": {
      "type": "string",
      "enum": ["celsius", "fahrenheit"],
      "default": "celsius",
      "description": "온도 단위. 기본값: celsius"
    }
  },
  "required": ["city"]
}
```

→ `enum`으로 허용값 제한, `examples`로 포맷 가이드, `required`로 필수값 명시.

---

### 2.2 Tool 선택 정확도 향상 Prompt 설계

**System Prompt에서 Tool 사용 지침 명시**

```
도구 선택 원칙:
1. 날씨 정보 → get_current_weather
2. 예보 정보 → get_weather_forecast
3. 두 정보 모두 필요 → 순차 호출
4. 불확실한 경우 → 사용자에게 되물어볼 것
```

**Tool간 우선순위 체계**

```
우선순위 1: 정확한 데이터 조회 Tool
우선순위 2: 추론·계산 Tool
우선순위 3: 외부 API 호출 Tool
```

→ 모델이 비용이 낮은 Tool을 먼저 시도하도록 유도한다.

**Few-shot Tool Calling 예시 삽입**

System Prompt에 올바른 Tool 호출 예시를 2~3개 포함한다.
"언제 이 Tool을 쓰고, 언제 쓰지 않는지"를 함께 보여준다.
이것만으로 Tool 선택 정확도가 15~30% 향상된다.

---

### 2.3 Multi-tool Routing 전략

**Routing 패턴 3가지**

```
패턴 1: Sequential (순차)
  → Tool A 결과를 Tool B 입력으로 사용
  → 의존성 있는 작업에 적합

패턴 2: Parallel (병렬)
  → 독립적인 Tool을 동시 호출
  → 지연시간 단축, 비용 주의

패턴 3: Conditional (조건부)
  → 첫 Tool 결과에 따라 다음 Tool 선택
  → 동적 분기 처리에 적합
```

**Sequential 패턴 예시**

```python
# 1단계: 사용자 정보 조회
user_info = get_user_profile(user_id="U123")

# 2단계: 조회 결과 기반 추천
recommendations = get_recommendations(
    user_segment=user_info["segment"],
    history=user_info["purchase_history"]
)
```

**Parallel 패턴 예시 (Claude API)**

```python
# Claude는 한 번의 응답에서 여러 Tool을 동시 호출 가능
response = client.messages.create(
    model="claude-opus-4-5",
    tools=[weather_tool, news_tool, stock_tool],
    messages=[{"role": "user", "content": "서울 날씨, 오늘 뉴스, 삼성 주가 알려줘"}]
)

# tool_use 블록이 여러 개 반환됨
for block in response.content:
    if block.type == "tool_use":
        results[block.name] = call_tool(block.name, block.input)
```

---

### 2.4 Tool 실패 재시도·Fallback 전략

**실패 유형 분류**

| 유형 | 원인 | 처리 방법 |
|------|------|-----------|
| Timeout | 외부 API 지연 | 재시도 (지수 백오프) |
| Invalid Input | 잘못된 인수 | 오류 메시지 → 모델 재생성 |
| Auth Error | 인증 만료 | 즉시 중단 + 알림 |
| Rate Limit | 호출 한도 초과 | 대기 후 재시도 |
| Not Found | 데이터 없음 | Fallback Tool 호출 |

**재시도 패턴 (지수 백오프)**

```python
import asyncio

async def call_with_retry(tool_fn, args, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await tool_fn(**args)
        except TimeoutError:
            if attempt == max_retries - 1:
                raise
            wait = 2 ** attempt  # 1s, 2s, 4s
            await asyncio.sleep(wait)
```

**Fallback 체인 패턴**

```python
async def get_product_info(product_id: str):
    # 1차: 실시간 DB 조회
    try:
        return await realtime_db.get(product_id)
    except Exception:
        pass

    # 2차: 캐시 조회
    try:
        return await cache.get(product_id)
    except Exception:
        pass

    # 3차: 기본값 반환
    return {"product_id": product_id, "status": "unavailable"}
```

**Tool 결과를 모델에 전달하는 오류 형식**

```python
# 오류 발생 시 tool_result에 오류 정보 전달
{
    "type": "tool_result",
    "tool_use_id": "tool_123",
    "is_error": True,
    "content": "날씨 API 응답 시간 초과. 잠시 후 재시도하거나 다른 방법으로 확인해 주세요."
}
```

→ 모델이 오류 내용을 이해하고 대안을 생성할 수 있다.

---

## 3. 실무 의미

**Tool 설계 체크리스트**

```
□ name: 동사_명사 패턴, 20자 이내
□ description: 호출 조건 + 유사 Tool과의 차이 명시
□ parameters: 모든 필드에 description + 예시
□ required: 실제 필수 필드만 포함
□ enum: 허용값이 정해진 파라미터에 적용
□ 실패 시나리오: 오류 유형별 처리 방법 구현
```

**프로덕션 운영 지표**

| 지표 | 목표값 | 측정 방법 |
|------|--------|-----------|
| Tool 선택 정확도 | ≥ 95% | 샘플 테스트 평가 |
| 평균 Tool 호출 횟수 | ≤ 3회/쿼리 | API 로그 |
| Tool 실패율 | ≤ 2% | 오류 로그 |
| Fallback 성공율 | ≥ 80% | 복구 성공 카운트 |

---

## 4. 비교

### Tool 정의 방식 비교

| 항목 | 최소 정의 | 완전 정의 |
|------|-----------|-----------|
| description | "Gets data" | 조건·제한·예시 포함 |
| parameters | type만 | description + examples + enum |
| 선택 정확도 | ~70% | ~95% |
| 유지보수 | 어려움 | 명확한 의도 |

### Routing 패턴 비교

| 패턴 | 장점 | 단점 | 적합한 상황 |
|------|------|------|-------------|
| Sequential | 결과 활용 용이 | 느림 | 의존성 있는 작업 |
| Parallel | 빠름 | 비용 증가 | 독립적인 다중 조회 |
| Conditional | 유연함 | 복잡한 설계 | 동적 분기 필요 시 |

---

## 5. 주의사항

**Tool 수 제한**

> Claude API는 최대 64개 Tool을 지원하지만
> Tool이 많을수록 선택 정확도가 떨어진다.
> 실무에서는 10개 이하를 권장한다.

**Parallel 호출의 함정**

> 병렬 호출 시 각 Tool의 결과가 순서 없이 반환된다.
> tool_use_id로 결과를 매핑해야 한다.
> 하나의 Tool 실패가 전체 흐름을 깨면 안 된다.

**오류 메시지 품질**

> is_error: True만으로는 충분하지 않다.
> 오류 원인과 대안을 구체적으로 명시해야
> 모델이 적절한 복구 행동을 취할 수 있다.

**Schema 변경 시 주의**

> Tool 스키마를 변경하면 기존 대화 맥락이 깨질 수 있다.
> 프로덕션에서는 버전 관리를 권장한다.
> 예: `get_weather_v2` 방식으로 신규 Tool 추가 후 점진적 마이그레이션.

---

## 6. 코드 예제

### 완성된 Multi-tool Agent 구현

```python
import anthropic
import json
from typing import Any

client = anthropic.Anthropic()

# Tool 정의 (완전한 스키마)
tools = [
    {
        "name": "get_current_weather",
        "description": (
            "사용자가 특정 도시의 현재 날씨를 요청할 때 호출. "
            "날씨 예보가 필요하면 get_weather_forecast를 사용."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "도시명 (영문 또는 한글). 예: Seoul, 서울, Tokyo"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "default": "celsius",
                    "description": "온도 단위"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "search_web",
        "description": (
            "최신 정보나 사실 확인이 필요할 때 호출. "
            "날씨, 주가 등 전용 Tool이 있는 경우는 해당 Tool 우선 사용."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "검색 쿼리. 구체적일수록 좋음"
                },
                "max_results": {
                    "type": "integer",
                    "default": 5,
                    "description": "반환할 최대 결과 수 (1~10)"
                }
            },
            "required": ["query"]
        }
    }
]


# Tool 실행 함수 (재시도 포함)
async def execute_tool(name: str, input_data: dict) -> Any:
    tool_functions = {
        "get_current_weather": fetch_weather,
        "search_web": search_web_api
    }

    fn = tool_functions.get(name)
    if not fn:
        return {"error": f"알 수 없는 Tool: {name}"}

    # 재시도 로직
    for attempt in range(3):
        try:
            return await fn(**input_data)
        except TimeoutError:
            if attempt == 2:
                return {"error": "API 응답 시간 초과. 잠시 후 재시도해 주세요."}
        except Exception as e:
            return {"error": str(e)}


# Agent 루프
def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        # Tool 호출이 없으면 종료
        if response.stop_reason == "end_turn":
            return response.content[0].text

        # Tool 호출 처리
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })

        # 메시지 히스토리 업데이트
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
```

---

## Q&A

**Q1. Tool description을 길게 쓰면 토큰 비용이 늘지 않나요?**

> 맞다. Tool 정의는 매 API 호출마다 포함된다.
> description은 핵심만 담되, 선택 조건은 명확히 쓴다.
> 일반적으로 description 당 30~80자가 최적이다.

**Q2. 모델이 존재하지 않는 Tool을 호출하면 어떻게 되나요?**

> Claude API는 정의된 Tool 목록에서만 선택한다.
> 존재하지 않는 Tool은 호출할 수 없다.
> 단, Tool 이름과 유사한 것을 잘못 선택할 수 있어 name 설계가 중요하다.

**Q3. Tool 호출을 강제로 막을 수 있나요?**

> `tool_choice: {"type": "none"}`으로 Tool 사용을 비활성화할 수 있다.
> 특정 Tool만 강제하려면 `{"type": "tool", "name": "tool_name"}`을 사용한다.
> 기본값은 `auto`로 모델이 판단한다.

---

## 퀴즈

**Q1. Tool의 `description`에 반드시 포함해야 하는 핵심 정보는?**

> a) Tool의 내부 구현 방식
> b) 언제 이 Tool을 호출해야 하는지 조건
> c) 개발자 이름과 버전
> d) 처리 속도

<details>
<summary>힌트 및 정답</summary>

**힌트**: 모델은 description을 읽고 Tool을 선택한다. 무엇을 알아야 올바른 선택을 할까?

**정답**: b) 언제 이 Tool을 호출해야 하는지 조건

description의 핵심 역할은 "이 Tool을 언제 쓰고 언제 쓰지 말아야 하는지"를 모델에게 알려주는 것이다.

</details>

---

**Q2. 다음 중 Parallel Tool Calling이 가장 적합한 상황은?**

> a) Tool A의 결과를 Tool B의 입력으로 사용해야 할 때
> b) 날씨, 뉴스, 주가를 각각 독립적으로 조회할 때
> c) 첫 번째 Tool이 실패하면 두 번째 Tool을 쓸 때
> d) 하나의 Tool을 3번 반복 호출할 때

<details>
<summary>힌트 및 정답</summary>

**힌트**: Parallel은 "동시에" 실행한다. 어떤 조건이 필요할까?

**정답**: b) 날씨, 뉴스, 주가를 각각 독립적으로 조회할 때

서로 의존성이 없는 Tool들을 병렬로 호출하면 전체 응답 시간이 단축된다. a는 Sequential, c는 Fallback, d는 반복 호출 패턴이다.

</details>

---

**Q3. Tool 실패 시 `is_error: True`와 함께 전달해야 하는 가장 중요한 정보는?**

> a) HTTP 상태 코드
> b) 스택 트레이스 전체
> c) 오류 원인과 사용자가 취할 수 있는 대안
> d) 실패한 Tool의 소스 코드

<details>
<summary>힌트 및 정답</summary>

**힌트**: 이 정보를 받는 것은 모델이다. 모델이 다음에 무엇을 해야 할지 알 수 있어야 한다.

**정답**: c) 오류 원인과 사용자가 취할 수 있는 대안

모델이 오류 내용을 이해하고 적절한 복구 행동(재시도, 대안 Tool 호출, 사용자 안내)을 취할 수 있어야 한다.

</details>

---

**Q4. Tool 선택 정확도를 높이기 위해 System Prompt에 추가하면 가장 효과적인 것은?**

> a) "항상 도구를 사용하세요"
> b) 각 Tool의 GitHub 링크
> c) 올바른 Tool 호출 Few-shot 예시
> d) 모델의 온도(temperature) 설정

<details>
<summary>힌트 및 정답</summary>

**힌트**: 모델은 예시에서 패턴을 학습한다. 무엇이 올바른 행동 패턴을 가르쳐줄까?

**정답**: c) 올바른 Tool 호출 Few-shot 예시

"언제 이 Tool을 쓰는지, 언제 쓰지 않는지"를 예시로 보여주면 Tool 선택 정확도가 15~30% 향상된다.

</details>

---

**Q5. 프로덕션 환경에서 권장하는 Tool 최대 개수는?**

> a) 64개 (API 최대값)
> b) 30개
> c) 10개 이하
> d) 제한 없음

<details>
<summary>힌트 및 정답</summary>

**힌트**: Tool이 많을수록 어떤 문제가 생길까?

**정답**: c) 10개 이하

Tool 수가 늘어날수록 모델의 선택 정확도가 떨어지고 토큰 비용이 증가한다. API 최대값(64개)은 기술적 한계이지, 권장값이 아니다.

</details>

---

## 실습 명세

### 실습 제목: Multi-tool Routing 정확도 비교

**I DO (시연, 15분)**

강사가 직접 시연한다:
1. 모호한 Tool 정의로 Agent 실행 → 잘못된 Tool 선택 확인
2. 개선된 Tool 정의로 동일 쿼리 실행 → 올바른 Tool 선택 확인
3. Sequential → Parallel 전환 시 응답 시간 변화 측정
4. Tool 실패 시 Fallback 동작 확인

**WE DO (함께, 30분)**

학생과 함께 단계별 구현:
1. `get_current_weather`, `get_news`, `calculate` Tool 정의
2. Multi-tool Agent 루프 구현
3. 병렬 호출 → 결과 매핑 구현
4. 오류 주입 → Fallback 동작 확인

**YOU DO (독립, 30분)**

- 새로운 Tool 2개 이상 추가 (예: `get_stock_price`, `translate_text`)
- Tool 선택 정확도 측정 스크립트 작성 (10개 테스트 케이스)
- Fallback 체인 구현 및 실패 시나리오 3가지 테스트
- `solution/` 폴더에 정답 코드 제공
