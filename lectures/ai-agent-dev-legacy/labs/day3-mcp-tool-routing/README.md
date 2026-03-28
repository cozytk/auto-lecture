# 실습: MCP Tool Routing 정확도 비교

**세션**: Day 3 Session 1 — MCP(Function Calling) 고급 설계
**소요 시간**: 75분 (I DO 15분 · WE DO 30분 · YOU DO 30분)
**목표**: JSON Schema 설계 품질이 Tool 선택 정확도에 미치는 영향을 측정하고, Multi-tool Routing 패턴을 구현한다.

---

## 사전 준비

```bash
# 의존성 설치
just setup

# 환경변수 설정
export ANTHROPIC_API_KEY=your_key_here

# 실행 확인
just check
```

---

## I DO — 강사 시연 (15분)

강사가 다음 두 가지를 직접 시연합니다.

### 시연 1: 모호한 Tool 정의의 실패

`src/bad_tools.py`를 실행하면 모호한 description으로 인해
모델이 엉뚱한 Tool을 선택하는 장면을 확인한다.

```bash
just demo-bad
```

**확인 포인트**:
- "서울 날씨 알려줘" → `search_web` 대신 `get_current_weather`를 선택해야 하는데?
- "내일 날씨 예보" → `get_weather_forecast`를 선택해야 하는데 `get_current_weather`를 선택?

### 시연 2: 개선된 Tool 정의

```bash
just demo-good
```

**확인 포인트**:
- 동일 쿼리에서 올바른 Tool 선택
- Sequential → Parallel 전환 시 응답 시간 변화
- Tool 실패 시 Fallback 동작

---

## WE DO — 함께 구현 (30분)

`src/agent.py`를 열고 단계별로 함께 구현합니다.

### Step 1: Tool 정의 작성

```python
# src/agent.py 의 TOOLS 리스트를 완성하세요
TOOLS = [
    {
        "name": "get_current_weather",
        "description": "???",  # TODO: 조건 + 유사 Tool 차이 명시
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "???",  # TODO: 예시 포함
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "default": "celsius"
                }
            },
            "required": ["city"]
        }
    },
    # TODO: get_news, calculate Tool 추가
]
```

### Step 2: Agent 루프 구현

```python
def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4096,
            tools=TOOLS,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            # TODO: 텍스트 응답 반환
            pass

        # TODO: Tool 호출 처리
        # TODO: 메시지 히스토리 업데이트
```

### Step 3: 병렬 호출 결과 매핑

```python
# tool_use_id를 사용해 결과를 올바르게 매핑하는 코드 작성
tool_results = []
for block in response.content:
    if block.type == "tool_use":
        result = execute_tool(block.name, block.input)
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,  # 반드시 id 매핑
            "content": json.dumps(result, ensure_ascii=False)
        })
```

### Step 4: Fallback 체인 구현

```python
async def get_data_with_fallback(query: str) -> dict:
    # 1차: 실시간 API
    # 2차: 캐시
    # 3차: 기본값
    pass  # TODO: 구현
```

실행:

```bash
just run
```

---

## YOU DO — 독립 실습 (30분)

### 과제

다음 세 가지를 독립적으로 구현하세요.

**과제 1: 새로운 Tool 2개 추가**

아래 두 Tool을 완전한 스키마로 정의하고 실제 동작을 구현하세요.

```
- get_stock_price: 주식 가격 조회 (심볼, 거래소 파라미터)
- translate_text: 텍스트 번역 (원문, 대상 언어 파라미터)
```

**과제 2: Tool 선택 정확도 측정**

`tests/test_accuracy.py`에 10개 테스트 케이스를 작성하고
각 케이스에서 올바른 Tool이 선택되는지 확인하세요.

```python
TEST_CASES = [
    {"query": "서울 지금 날씨는?", "expected_tool": "get_current_weather"},
    {"query": "삼성전자 주가 알려줘", "expected_tool": "get_stock_price"},
    # TODO: 8개 더 추가
]
```

**과제 3: Fallback 시나리오 3가지 테스트**

```
시나리오 1: get_current_weather API Timeout → 캐시로 Fallback
시나리오 2: get_stock_price 404 Not Found → 기본값 Fallback
시나리오 3: get_news Rate Limit → 대기 후 재시도
```

완료 후 다음을 실행하여 확인:

```bash
just test
```

정답 코드: `solution/` 폴더를 참조하세요.

---

## 체크리스트

실습 완료 전 확인:

```
□ Tool description에 호출 조건 명시
□ 유사 Tool과의 차이 description에 포함
□ parameters에 description + examples 포함
□ Agent 루프가 stop_reason == "end_turn"에서 종료
□ tool_use_id로 결과 매핑
□ Fallback 체인 3단계 구현
□ 정확도 테스트 10케이스 통과
```

---

## 참고: 올바른 Tool description 패턴

```
나쁜 예: "Gets weather information"

좋은 예: "사용자가 특정 도시의 현재 날씨(온도, 습도, 상태)를 요청할 때 호출.
         날씨 예보(내일, 주간)가 필요하면 get_weather_forecast를 사용할 것.
         현재 시점 날씨만 이 Tool로 조회 가능."
```
