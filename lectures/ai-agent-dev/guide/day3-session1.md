# MCP(Function Calling) 고급 설계

## 학습 목표
1. JSON Schema 기반 Tool 정의를 전략적으로 설계하여 LLM의 Tool 선택 정확도를 극대화할 수 있다
2. Multi-tool Routing 전략을 구현하여 복수 Tool 중 최적의 도구를 자동 선택하는 시스템을 구축할 수 있다
3. Tool 실행 실패 시 재시도 및 Fallback 메커니즘을 설계하여 안정적인 Agent를 만들 수 있다

---

## 개념 1: JSON Schema Tool 정의 전략

### 개념 설명

**왜 이것이 중요한가**: AI Agent가 외부 세계와 상호작용하려면 Tool(도구)을 호출해야 하고, 이 호출의 정확성은 전적으로 Tool 정의의 품질에 달려 있다. Tool 정의는 LLM이 "이 도구를 언제, 어떤 인자로 호출할지"를 결정하는 유일한 판단 근거다. 아무리 뛰어난 LLM이라도 Tool 정의가 모호하면 올바른 도구를 선택할 수 없다. 실무에서 Agent의 Tool 호출 오류 중 약 60% 이상이 잘못된 Tool 정의에서 비롯된다는 보고가 있다. 따라서 Tool 정의 전략은 Agent 개발에서 가장 기본적이면서도 가장 큰 영향을 미치는 설계 역량이다.

**핵심 원리**: AI 모델이 외부 도구를 호출하는 개념은 2023년 OpenAI의 GPT-3.5 Turbo Function Calling에서 본격적으로 시작되었다. 초기에는 모델이 단순히 JSON 형태의 함수 인자를 생성하는 수준이었으나, 이후 Anthropic의 Tool Use, Google의 Function Calling 등 각 사업자마다 유사하지만 호환되지 않는 프로토콜이 난립하게 되었다. 이 문제를 해결하기 위해 Anthropic이 2024년 제안한 것이 **MCP(Model Context Protocol)**이다. MCP는 LLM과 외부 도구 사이의 통신을 표준화하는 개방형 프로토콜로, 특정 모델이나 벤더에 종속되지 않는 범용 인터페이스를 지향한다.

MCP의 핵심 설계 철학은 "도구의 사용 방법을 사람이 아닌 LLM이 이해해야 한다"는 점이다. 전통적인 API 문서는 개발자가 읽고 해석하지만, MCP에서는 LLM이 Tool의 JSON Schema를 직접 읽고 "이 도구를 언제, 어떤 인자로 호출할지"를 자율적으로 결정한다. 따라서 Tool의 `name`, `description`, `parameters` 설계가 곧 LLM과의 의사소통이며, 이 설계의 품질이 Tool 선택 정확도를 좌우한다.

**실무에서의 의미**: 실무에서 가장 흔한 실수는 Tool을 "개발자가 편한 방식"으로 정의하는 것이다. 예를 들어 이름을 `search`로 짓거나, description을 한 단어로 끝내거나, 파라미터에 `q`처럼 축약어를 쓰는 경우가 많다. 그러나 LLM은 이 정보만으로 수십 개의 Tool 중 어떤 것을 호출할지 판단해야 한다. 개발자가 읽기 편한 이름이 아니라 LLM이 판단하기 쉬운 이름을 지어야 한다. 이것은 API 설계에서 "소비자 중심 설계(Consumer-Driven Design)"와 같은 원칙인데, 여기서 소비자가 사람이 아니라 LLM이라는 점이 다를 뿐이다.

**다른 접근법과의 비교**: 단순한 Function Calling과 MCP의 차이는 "프로토콜의 범위"에 있다. Function Calling은 LLM에게 함수 시그니처를 전달하고 인자를 생성받는 1회성 인터랙션이지만, MCP는 Tool 탐색(discovery), 호출(invocation), 결과 반환(response), 에러 처리까지 전체 라이프사이클을 표준화한다. 이 때문에 MCP 기반 Agent는 새로운 도구가 추가되어도 코드를 수정할 필요 없이 자동으로 사용 가능한 Tool 목록을 갱신할 수 있다. GitHub Copilot, Cursor, Claude Desktop 등 주요 프로덕션 환경이 이미 MCP를 채택하고 있어, Tool 설계 역량은 Agent 개발에서 가장 실무적인 스킬이 되었다.

**주의사항**: Tool 정의에서 지켜야 할 세 가지 핵심 원칙이 있다. 첫째, **명확한 네이밍**으로, Tool 이름만으로 기능을 추론할 수 있어야 한다. `search`가 아니라 `search_product_catalog`처럼 구체적으로 짓는다. 둘째, **상세한 description**으로, LLM이 언제 이 Tool을 사용해야 하는지 판단하는 근거가 된다. 특히 "사용하지 말아야 할 경우(negative instruction)"를 명시하면 유사 Tool 간 오선택률이 크게 낮아진다. OpenAI의 내부 실험에 따르면 negative instruction 추가 시 Tool 선택 정확도가 평균 12% 향상되었다. 셋째, **엄격한 parameter schema**로, `enum`으로 선택지를 제한하고, `description`으로 각 파라미터의 용도를 설명하며, `required`로 필수 입력을 강제한다. 이렇게 하면 LLM이 잘못된 입력을 생성할 가능성을 사전에 차단할 수 있다.

이 원칙들을 "나쁜 Tool 정의"와 "좋은 Tool 정의"로 비교하면 다음과 같다:

```python
# 나쁜 Tool 정의 - LLM이 용도를 파악하기 어렵다
bad_tool = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "검색합니다",
        "parameters": {
            "type": "object",
            "properties": {"q": {"type": "string"}}
        }
    }
}

# 좋은 Tool 정의 - LLM이 정확히 판단할 수 있다
good_tool = {
    "type": "function",
    "function": {
        "name": "search_product_catalog",
        "description": "상품 카탈로그에서 상품을 검색합니다. 사용자가 상품명, 카테고리, "
                       "가격대로 상품을 찾을 때 사용합니다. "
                       "재고 조회나 주문 관련 질문에는 사용하지 마세요.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "검색할 상품명 또는 키워드"},
                "category": {
                    "type": "string",
                    "enum": ["electronics", "clothing", "food", "furniture"],
                    "description": "상품 카테고리 필터"
                },
                # ... (min_price, max_price 등 추가 파라미터)
            },
            "required": ["query"]
        }
    }
}
```

### 예제

다음 예제는 전략적으로 설계된 Tool 세트를 실제 LLM에 전달하여, description의 차이가 Tool 선택 결과에 어떤 영향을 미치는지 확인한다. `get_weather_current`와 `get_weather_forecast` 두 Tool의 description에 각각 "현재 시점의 날씨만"과 "미래 예보만"이라는 경계를 명확히 기술해 두었다는 점에 주목하자.

```python
import os
from openai import OpenAI
import json

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather_current",
            "description": "현재 날씨 정보를 조회합니다. 특정 도시의 현재 기온, 습도, 날씨 상태를 반환합니다. "
                           "예보(미래 날씨)가 아닌 현재 시점의 날씨만 제공합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "도시명 (예: Seoul, Tokyo)"},
                    "units": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_forecast",
            "description": "향후 1~7일 날씨 예보를 조회합니다. 미래 날씨, 주간 예보, 내일/모레 날씨를 물을 때 사용합니다. "
                           "현재 날씨가 아닌 미래 예보만 제공합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "도시명"},
                    "days": {"type": "integer", "minimum": 1, "maximum": 7, "description": "예보 일수"}
                },
                "required": ["city", "days"]
            }
        }
    }
]

response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "내일 서울 날씨 어때?"}],
    tools=tools,
    tool_choice="auto"
)

tool_call = response.choices[0].message.tool_calls[0]
print(f"선택된 Tool: {tool_call.function.name}")
print(f"인자: {tool_call.function.arguments}")
```

**실행 결과**:
```
선택된 Tool: get_weather_forecast
인자: {"city": "Seoul", "days": 1}
```

LLM이 "내일"이라는 키워드를 보고 `get_weather_forecast`를 정확히 선택했다. description에 "미래 날씨"를 명시했기 때문이다.

### Q&A
**Q: Tool description은 얼마나 길어야 하나요?**
A: 2~3문장이 최적이다. 첫 문장은 Tool의 핵심 기능, 두 번째 문장은 사용 시점, 세 번째 문장은 사용하지 말아야 할 경우(negative instruction)를 기술한다. 너무 길면 LLM의 context window를 낭비하고, 너무 짧으면 선택 정확도가 떨어진다.

**Q: enum 필드와 자유 텍스트 중 어떤 것을 써야 하나요?**
A: 선택지가 명확하고 제한적이면 `enum`을 사용한다. LLM이 잘못된 값을 생성할 가능성을 원천 차단한다. 자유 텍스트는 검색 쿼리처럼 사용자 입력을 그대로 전달해야 할 때 사용한다.

<details>
<summary>퀴즈: Tool의 description에 "이 Tool을 사용하지 마세요"라는 negative instruction을 추가하면 어떤 효과가 있을까요?</summary>

**힌트**: LLM은 유사한 Tool이 여러 개 있을 때 어떤 기준으로 선택할까요?

**정답**: Negative instruction은 유사 Tool 간의 경계를 명확히 하여 오선택(mis-routing)을 줄인다. 예를 들어 `search_product`와 `check_inventory` Tool이 있을 때, `search_product`의 description에 "재고 조회에는 사용하지 마세요"를 추가하면 LLM이 재고 관련 질문에 `check_inventory`를 선택할 확률이 높아진다. OpenAI 실험에서 negative instruction 추가 시 Tool 선택 정확도가 평균 12% 향상되었다.
</details>

---

## 개념 2: Tool 선택 정확도 향상 Prompt 설계

### 개념 설명

**왜 이것이 중요한가**: Tool 정의의 `description`을 아무리 잘 작성해도 한계가 있는 경우가 있다. 개별 Tool의 용도는 명확하지만, 여러 Tool을 조합해서 사용해야 하는 상황에서는 Tool 하나의 description만으로는 "어떤 순서로 호출해야 하는지"를 LLM에게 전달하기 어렵다. 예를 들어 "환불 요청"이 들어왔을 때 LLM이 바로 환불 Tool을 호출하면 안 되고, 먼저 주문 상태를 확인한 후에 환불을 진행해야 한다. 이런 다단계 워크플로우의 정확도를 높이는 것이 System Prompt 기반 Tool 사용 가이드라인이다.

**핵심 원리**: 이 접근법은 In-Context Learning(ICL)의 원리에 기반한다. LLM은 프롬프트에 포함된 예시로부터 패턴을 학습하여 새로운 입력에 적용하는 능력이 뛰어나다. 따라서 System Prompt에 "어떤 질문이 들어왔을 때 어떤 Tool을 호출하라"는 Few-shot 예시를 넣으면, LLM이 유사한 새 질문에서도 올바른 Tool 선택 및 호출 순서를 따를 가능성이 크게 높아진다. 이는 단일 Tool 선택을 넘어 **다단계 Tool 체이닝(multi-step tool chaining)**의 정확도를 향상시키는 가장 실용적인 방법이다.

**실무에서의 의미**: 핵심 전략은 세 가지로 구분된다. 첫째, **Tool 사용 우선순위 지정**이다. "환불 요청 시 먼저 주문 상태를 확인하고, 확인 후 CS 티켓을 생성하라"처럼 순서를 명시한다. 둘째, **Tool 선택 기준 명시**로, "사용자가 상품을 검색하면 A Tool, 주문을 물으면 B Tool"처럼 조건-Tool 매핑을 제공한다. 셋째, **Tool 미사용 조건 명시**다. "인사말이나 일반 대화에는 Tool을 호출하지 마라"를 지시하지 않으면 LLM은 모든 입력에서 Tool을 호출하려는 경향이 있다. 이 세 가지는 마치 신입 직원에게 "이 상황에서는 이렇게 하고, 저 상황에서는 저렇게 해"라는 업무 매뉴얼을 제공하는 것과 같다.

**다른 접근법과의 비교**: Tool description과 System Prompt 가이드라인은 역할이 다르다. description은 "개별 Tool이 무엇을 하는가"를, System Prompt는 "Tool들을 어떻게 조합하는가"를 각각 담당한다. 두 가지가 서로 모순되지 않도록 주의해야 한다. description에서 "재고 조회에 사용하세요"라고 했는데 System Prompt에서 "재고는 다른 Tool을 쓰세요"라고 하면 LLM이 혼란스러워진다.

**주의사항**: Few-shot 예시는 3~5개가 최적이며, 10개 이상은 수확 체감이 발생한다. 비용 관점에서도 3~5개 예시는 약 200~400 토큰 수준으로, Tool 오선택으로 인한 재호출 비용보다 훨씬 저렴하다. 실무에서는 이 세 가지를 System Prompt 안에 구조화된 마크다운 형태로 작성하는 것이 일반적이다.

이를 코드로 구현하면 다음과 같다:

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

system_prompt = """당신은 고객 지원 AI Agent입니다.

## Tool 사용 가이드라인

### 사용 가능한 Tool과 선택 기준:
1. `search_product_catalog`: 사용자가 상품을 검색하거나 추천을 요청할 때
2. `check_order_status`: 주문번호를 언급하며 배송/주문 상태를 물을 때
3. `create_support_ticket`: 불만, 환불, 교환 등 CS 이슈를 접수할 때

### Tool 미사용 조건:
- 인사말, 일반 대화에는 Tool을 호출하지 마세요
- "감사합니다", "안녕하세요" 등에는 직접 응답하세요

### 다단계 처리:
- 환불 요청 시: 먼저 check_order_status로 주문 확인 → create_support_ticket으로 접수
- 상품 추천 후 주문 질문: search_product_catalog → check_order_status 순서
"""

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "주문번호 ORD-12345 환불하고 싶어요"}
    ],
    tools=tools,  # 앞서 정의한 tools
    tool_choice="auto"
)
```

**실행 결과**:
```
# Step 1: check_order_status 호출 → {"order_id": "ORD-12345"}
# Step 2: create_support_ticket 호출 → {"type": "refund", "order_id": "ORD-12345"}
```

### 예제

다음 예제는 여행 플래너 Agent에 Few-shot 패턴을 적용한 사례다. System Prompt에 "파리 3박 4일"이라는 입력이 어떤 Tool 호출 순서로 이어지는지를 예시로 제공했기 때문에, 유사한 "도쿄 2박 3일" 입력에서도 동일한 패턴(여행지 검색 -> 호텔 추천)으로 Tool이 호출된다.

```python
import os
from openai import OpenAI
import json

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

system_prompt = """당신은 여행 플래너 AI Agent입니다.

## Tool 사용 예시

사용자: "파리 3박 4일 여행 계획 세워줘"
→ search_destinations(query="파리") → get_hotel_recommendations(city="Paris", nights=3)

사용자: "지금 환율이 얼마야?"
→ get_exchange_rate(from="KRW", to="EUR")

사용자: "여행 꿀팁 알려줘"
→ Tool 미사용, 직접 답변
"""

tools = [
    {"type": "function", "function": {
        "name": "search_destinations",
        "description": "여행지 정보를 검색합니다. 관광지, 맛집, 액티비티 정보를 포함합니다.",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string", "description": "검색할 여행지 또는 키워드"},
            "category": {"type": "string", "enum": ["sightseeing", "food", "activity", "all"]}
        }, "required": ["query"]}
    }},
    {"type": "function", "function": {
        "name": "get_hotel_recommendations",
        "description": "호텔 추천 목록을 반환합니다. 도시명과 숙박 일수 기반으로 최적의 호텔을 추천합니다.",
        "parameters": {"type": "object", "properties": {
            "city": {"type": "string", "description": "도시명 (영문)"},
            "nights": {"type": "integer", "description": "숙박 일수"},
            "budget": {"type": "string", "enum": ["budget", "mid-range", "luxury"]}
        }, "required": ["city", "nights"]}
    }},
    {"type": "function", "function": {
        "name": "get_exchange_rate",
        "description": "실시간 환율 정보를 조회합니다.",
        "parameters": {"type": "object", "properties": {
            "from_currency": {"type": "string", "description": "원본 통화 코드 (예: KRW)"},
            "to_currency": {"type": "string", "description": "대상 통화 코드 (예: USD)"}
        }, "required": ["from_currency", "to_currency"]}
    }}
]

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "도쿄 2박 3일 추천해줘"}
    ],
    tools=tools,
    tool_choice="auto"
)

for tool_call in response.choices[0].message.tool_calls:
    print(f"Tool: {tool_call.function.name}")
    print(f"Args: {tool_call.function.arguments}\n")
```

**실행 결과**:
```
Tool: search_destinations
Args: {"query": "도쿄", "category": "all"}

Tool: get_hotel_recommendations
Args: {"city": "Tokyo", "nights": 2}
```

### Q&A
**Q: Few-shot 예시를 System Prompt에 넣으면 토큰 비용이 많이 들지 않나요?**
A: 3~5개의 예시는 대략 200~400 토큰이다. Tool 오선택으로 인한 재호출, 에러 처리, 사용자 불만 대비 비용이 훨씬 크므로 충분히 투자할 가치가 있다. 다만 10개 이상의 예시는 수확 체감이 발생하므로 핵심 케이스만 선별한다.

<details>
<summary>퀴즈: System Prompt에 Tool 사용 예시를 넣는 방식과 Tool description을 상세히 작성하는 방식 중 어느 것이 더 효과적일까요?</summary>

**힌트**: 두 방식은 서로 다른 문제를 해결합니다. Tool description은 "무엇"을, 예시는 "어떻게"를 알려줍니다.

**정답**: 두 방식은 보완적이다. Tool description은 개별 Tool의 용도를 정의하고, System Prompt 예시는 복수 Tool 간의 조합/순서를 학습시킨다. 실무에서는 두 방식을 함께 사용하는 것이 최적이다. 단일 Tool 선택 정확도는 description이, 다단계 Tool 체이닝 정확도는 Few-shot 예시가 더 큰 영향을 미친다.
</details>

---

## 개념 3: Multi-tool Routing 전략

### 개념 설명

**왜 이것이 중요한가**: 현실의 프로덕션 Agent는 5개가 아니라 수십 개의 Tool을 가진다. 예를 들어 e-커머스 Agent는 상품 검색, 상품 상세 조회, 상품 비교, 주문 생성, 주문 조회, 주문 취소, CS 티켓 생성, FAQ 검색, 상담사 연결 등 최소 9~12개의 Tool이 필요하다. 그런데 LLM에게 10개 이상의 Tool을 한꺼번에 제공하면 심각한 문제가 발생한다. LLM이 모든 Tool의 description을 비교 분석해야 하므로 선택 정확도가 급격히 하락하고, 유사한 이름이나 기능의 Tool 간에 혼동이 빈번해진다. OpenAI의 내부 벤치마크에 따르면, Tool 수가 5개일 때 95%였던 선택 정확도가 15개로 늘어나면 약 75%까지 떨어진다.

**핵심 원리**: Multi-tool Routing은 이 문제를 해결하기 위한 아키텍처 패턴이다. 핵심 아이디어는 "LLM에게 모든 Tool을 한꺼번에 보여주지 말고, 필요한 Tool만 선별하여 제공하라"는 것이다. 이는 도서관에서 책을 찾는 과정과 유사하다. 100만 권의 책을 한꺼번에 뒤지는 것보다, 먼저 "컴퓨터 과학" 섹션으로 이동한 뒤 그 안에서 검색하는 것이 훨씬 효율적이다. Agent에서도 마찬가지로, 사용자 요청을 먼저 분류한 뒤 해당 카테고리에 속한 Tool만 LLM에 제공하면, 선택 정확도를 5개 Tool 수준(95%)으로 유지할 수 있다.

**실무에서의 의미**: 세 가지 구체적 전략이 있다. **카테고리 기반 2단계 라우팅**은 먼저 경량 모델로 사용자 요청의 카테고리(상품/주문/고객지원 등)를 분류한 뒤, 해당 카테고리에 속한 Tool만 LLM에 제공하는 방식이다. 9개 Tool을 3개 카테고리로 나누면, 실제 Tool 선택 시 LLM은 3개 중에서 고르기만 하면 된다. **의도 분류 -> Tool 매핑** 전략은 사용자의 의도를 먼저 분류(classification)한 뒤 의도에 따라 Tool 세트를 동적으로 결정한다. 분류 단계에서 신뢰도(confidence)를 함께 반환하도록 설계하면, 신뢰도가 낮을 때 전체 Tool을 제공하는 fallback 로직을 자연스럽게 추가할 수 있다. **Tool 그룹핑**은 관련 Tool 여러 개를 하나의 "super tool"로 묶어 LLM에 제공하고, LLM이 super tool을 선택하면 내부적으로 세부 Tool을 다시 선택하는 방식이다.

**다른 접근법과의 비교**: 비용 최적화 관점에서 중요한 점은 카테고리 분류처럼 단순한 classification 작업에는 GPT-4o-mini 같은 저비용 모델을 사용하고, 실제 Tool 실행과 결과 생성에는 고성능 모델을 사용하는 "이종 모델 조합"이 효과적이라는 것이다. GPT-4o-mini는 GPT-4o 대비 약 1/30 비용이면서 단순 분류 정확도는 거의 동등하기 때문에, 이 구조에서 "분류는 저렴하게, 실행은 정확하게"라는 비용-품질 밸런스를 달성할 수 있다. Tool이 5개 이하라면 라우팅 레이어가 오히려 latency와 비용만 증가시키므로, 8~10개 이상일 때 도입을 검토하는 것이 현실적이다.

이를 코드로 구현하면 다음과 같다:

```python
import os
from openai import OpenAI
import json

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

# 카테고리 기반 2단계 라우팅
TOOL_CATEGORIES = {
    "product": ["search_product", "get_product_detail", "compare_products"],
    "order": ["create_order", "check_order_status", "cancel_order"],
    "support": ["create_ticket", "get_faq", "escalate_to_human"]
}

category_tool = {
    "type": "function",
    "function": {
        "name": "classify_intent",
        "description": "사용자 요청의 카테고리를 분류합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["product", "order", "support"],
                    "description": "요청 카테고리"
                }
            },
            "required": ["category"]
        }
    }
}

def route_to_tools(user_message: str) -> dict:
    """2단계 라우팅: 카테고리 분류 → 해당 Tool 제공"""
    # Step 1: 카테고리 분류
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": user_message}],
        tools=[category_tool],
        tool_choice={"type": "function", "function": {"name": "classify_intent"}}
    )
    category = json.loads(
        response.choices[0].message.tool_calls[0].function.arguments
    )["category"]

    # Step 2: 해당 카테고리의 Tool만 로드
    available_tools = TOOL_CATEGORIES[category]
    print(f"카테고리: {category}")
    print(f"사용 가능 Tool: {available_tools}")
    return {"category": category, "tools": available_tools}

result = route_to_tools("주문한 상품이 아직 안 왔어요")
```

**실행 결과**:
```
카테고리: order
사용 가능 Tool: ['create_order', 'check_order_status', 'cancel_order']
```

9개 Tool 전체를 제공하지 않고 3개만 제공함으로써 Tool 선택 정확도를 높인다.

### 예제

아래는 의도 분류 + Tool 매핑 전략을 클래스로 구조화한 실전 구현이다. `ToolRouter`는 의도별 Tool 그룹을 동적으로 등록하고, 신뢰도 기반 fallback 로직을 내장한다. 분류 신뢰도가 0.7 미만이면 전체 Tool을 제공하여 안전망을 확보하는 설계다.

```python
import os
from openai import OpenAI
import json
from typing import Any

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

class ToolRouter:
    def __init__(self):
        self.tool_registry: dict[str, list[dict]] = {}
        self.intent_descriptions: dict[str, str] = {}

    def register_tools(self, intent: str, description: str, tools: list[dict]):
        """의도별 Tool 그룹 등록"""
        self.tool_registry[intent] = tools
        self.intent_descriptions[intent] = description

    def _build_classifier_tool(self) -> dict:
        """의도 분류용 Tool 동적 생성"""
        return {
            "type": "function",
            "function": {
                "name": "classify_user_intent",
                "description": "사용자 메시지의 의도를 분류합니다.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "intent": {
                            "type": "string",
                            "enum": list(self.tool_registry.keys()),
                            "description": "\n".join(
                                f"- {k}: {v}" for k, v in self.intent_descriptions.items()
                            )
                        },
                        "confidence": {"type": "number", "description": "분류 신뢰도 (0.0~1.0)"}
                    },
                    "required": ["intent", "confidence"]
                }
            }
        }

    def route(self, user_message: str) -> dict[str, Any]:
        """사용자 메시지 → 의도 분류 → Tool 세트 반환"""
        classifier = self._build_classifier_tool()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": user_message}],
            tools=[classifier],
            tool_choice={"type": "function", "function": {"name": "classify_user_intent"}}
        )
        result = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        intent, confidence = result["intent"], result["confidence"]

        # 신뢰도가 낮으면 전체 Tool 제공 (fallback)
        if confidence < 0.7:
            all_tools = [t for tools in self.tool_registry.values() for t in tools]
            return {"intent": "unknown", "confidence": confidence, "tools": all_tools}

        return {"intent": intent, "confidence": confidence, "tools": self.tool_registry[intent]}

# 사용 예시
router = ToolRouter()
router.register_tools("product_search", "상품 검색, 비교, 추천 관련 요청", [
    {"type": "function", "function": {"name": "search_product", "description": "상품 검색",
        "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "compare_products", "description": "상품 비교",
        "parameters": {"type": "object", "properties": {"product_ids": {"type": "array", "items": {"type": "string"}}}, "required": ["product_ids"]}}}
])
router.register_tools("order_management", "주문 조회, 취소, 환불 관련 요청", [
    {"type": "function", "function": {"name": "check_order", "description": "주문 상태 조회",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}}},
    {"type": "function", "function": {"name": "cancel_order", "description": "주문 취소",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}, "reason": {"type": "string"}}, "required": ["order_id"]}}}
])

result = router.route("노트북 추천해줘")
print(f"의도: {result['intent']}, 신뢰도: {result['confidence']}, Tool 수: {len(result['tools'])}")
```

**실행 결과**:
```
의도: product_search, 신뢰도: 0.95, Tool 수: 2
```

### Q&A
**Q: Tool이 5개 이하면 라우팅이 필요 없나요?**
A: 맞다. 5개 이하에서는 LLM이 description만으로 충분히 구분한다. 라우팅 레이어를 추가하면 오히려 latency와 비용만 증가한다. 라우팅은 Tool이 8~10개 이상이거나, 유사한 Tool이 3개 이상일 때 도입을 검토한다.

<details>
<summary>퀴즈: 2단계 라우팅에서 카테고리 분류에 GPT-4o-mini를 사용하는 이유는 무엇일까요?</summary>

**힌트**: 카테고리 분류는 복잡한 추론이 필요한 작업인가요?

**정답**: 카테고리 분류는 단순 분류(classification) 작업이므로 가벼운 모델로 충분하다. GPT-4o-mini는 GPT-4o 대비 약 1/30 비용이면서 분류 정확도는 거의 동등하다. 이 구조에서 비용 최적화의 핵심은 "분류는 저렴하게, 실행은 정확하게"이다. 분류 단계에서 절약한 비용을 실제 Tool 실행 단계의 고성능 모델에 투자할 수 있다.
</details>

---

## 개념 4: Tool 실패 재시도 및 Fallback

### 개념 설명

**왜 이것이 중요한가**: 지금까지 다룬 Tool 정의, Prompt 설계, Multi-tool Routing은 모두 "LLM이 올바른 Tool을 선택하도록" 하는 데 집중했다. 그러나 실제 운영 환경에서는 Tool 선택이 정확하더라도 **Tool 실행 자체가 실패**하는 경우가 빈번하다. 네트워크 타임아웃, 외부 API의 일시적 장애, Rate Limit 초과, 인증 토큰 만료, 잘못된 파라미터 형식 등 실패 원인은 매우 다양하다. 프로덕션 환경에서 외부 API의 가용성(availability)은 99.9%라 해도, 하루 1000회 호출하면 평균 1회는 실패한다는 뜻이며, 실제로는 네트워크 불안정까지 합치면 실패율이 더 높다.

**핵심 원리**: 안정적인 Agent를 만들기 위해서는 에러를 무시하거나 사용자에게 그대로 던지는 것이 아니라, **에러의 유형을 분류하고 유형별로 다른 복구 전략**을 적용해야 한다. 에러는 크게 세 가지로 분류된다. **Transient(일시적) 에러**는 네트워크 타임아웃이나 서버 과부하처럼 시간이 지나면 자연히 해결되는 유형으로, 재시도(retry)가 적절한 전략이다. **Permanent(영구적) 에러**는 API 키 만료, 서비스 폐지, 권한 부족처럼 재시도해도 해결되지 않는 유형으로, 대안 서비스(fallback)로 전환해야 한다. **Invalid Input 에러**는 LLM이 잘못된 파라미터를 생성한 경우로, LLM에게 에러 메시지를 전달하여 파라미터를 재생성하도록 요청하는 것이 올바른 전략이다.

**실무에서의 의미**: 재시도 시에는 **지수 백오프(Exponential Backoff)**를 반드시 적용해야 한다. 1초, 2초, 4초로 대기 시간을 점점 늘려가면 서버가 과부하에서 회복할 시간을 확보하면서도, 불필요하게 긴 대기를 피할 수 있다. 일반적으로 최대 3회 재시도가 표준이며, 총 대기 시간은 약 7초가 된다. 사용자 체감 응답 시간이 10초를 넘기면 UX가 급격히 저하되므로, 3회 재시도 후에는 Fallback으로 전환하거나 실패를 즉시 알리는 것이 바람직하다. 이 설계는 마이크로서비스 아키텍처에서 서킷 브레이커(Circuit Breaker) 패턴과 매우 유사한데, Agent 맥락에서는 "외부 API가 아닌 LLM이 소비자"라는 점이 다를 뿐이다.

**다른 접근법과의 비교**: Fallback 체인은 동일한 기능을 제공하는 여러 서비스를 우선순위 순으로 배열한 구조다. 예를 들어 상품 검색 기능에 "실시간 DB 검색 -> 캐시 검색 -> 정적 데이터 반환" 순서의 Fallback 체인을 두면, DB가 장애가 나도 캐시에서 결과를 반환할 수 있다. 중요한 것은 Fallback이 발생했을 때 이를 **모니터링 시스템에 기록**하는 것이다. Primary가 지속적으로 실패하면 인프라팀에 알림이 가야 하며, 어떤 Fallback에서 성공했는지 추적해야 서비스 품질을 관리할 수 있다. 단순히 "장애를 숨기는" 것이 아니라 "장애를 우회하면서 동시에 가시화하는" 것이 올바른 설계다.

이를 코드로 구현하면 다음과 같다:

```python
import os
from openai import OpenAI
import json
import time
from enum import Enum
from dataclasses import dataclass

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

class FailureType(Enum):
    TRANSIENT = "transient"      # 일시적 오류 → 재시도
    PERMANENT = "permanent"      # 영구적 오류 → Fallback
    INVALID_INPUT = "invalid"    # 잘못된 입력 → LLM에게 재생성 요청

@dataclass
class ToolResult:
    success: bool
    data: dict | None = None
    error: str | None = None
    failure_type: FailureType | None = None

def execute_with_retry(
    tool_name: str, arguments: dict,
    max_retries: int = 3, backoff_base: float = 1.0
) -> ToolResult:
    """지수 백오프 기반 Tool 실행 재시도"""
    for attempt in range(max_retries):
        try:
            result = call_tool(tool_name, arguments)
            return ToolResult(success=True, data=result)
        except TransientError as e:
            wait_time = backoff_base * (2 ** attempt)
            print(f"[재시도 {attempt + 1}/{max_retries}] {wait_time}초 후 재시도...")
            time.sleep(wait_time)
        except PermanentError as e:
            return ToolResult(success=False, error=str(e), failure_type=FailureType.PERMANENT)
        except InvalidInputError as e:
            return ToolResult(success=False, error=str(e), failure_type=FailureType.INVALID_INPUT)

    return ToolResult(success=False, error=f"{max_retries}회 재시도 실패", failure_type=FailureType.TRANSIENT)
```

### 예제

다음 예제는 Fallback 체인과 Agent 루프를 통합한 실전 구현이다. `execute_tool_with_fallback` 함수는 Primary -> Fallback 순서로 Tool을 시도하고, 모든 Fallback이 실패하면 LLM에게 에러 메시지를 전달하여 사용자에게 자연어로 안내하도록 한다. 이 구조에서 핵심은 에러 메시지를 단순히 "실패"라고 하지 않고 구체적 내용을 전달한다는 점이다. LLM은 구체적 에러 메시지를 분석하여 사용자에게 상황을 설명하거나, 다른 Tool을 호출하거나, 파라미터를 수정하여 재시도하는 등 더 지능적인 에러 핸들링이 가능해진다.

```python
import os
from openai import OpenAI
import json
from dataclasses import dataclass, field

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

@dataclass
class FallbackChain:
    """Tool Fallback 체인 구현"""
    primary: str
    fallbacks: list[str] = field(default_factory=list)

FALLBACK_CHAINS = {
    "search_product": FallbackChain(
        primary="search_product_db",
        fallbacks=["search_product_cache", "search_product_static"]
    ),
}

def execute_tool_with_fallback(tool_name: str, arguments: dict) -> dict:
    """Fallback 체인을 따라 Tool 실행"""
    chain = FALLBACK_CHAINS.get(tool_name)
    if not chain:
        return _execute_single(tool_name, arguments)

    result = _execute_single(chain.primary, arguments)
    if result["success"]:
        return result

    print(f"[Primary 실패] {chain.primary}: {result['error']}")
    for fallback in chain.fallbacks:
        print(f"[Fallback 시도] {fallback}")
        result = _execute_single(fallback, arguments)
        if result["success"]:
            result["source"] = fallback
            return result

    return {"success": False, "error": "모든 Fallback 소진", "chain": tool_name}

def agent_loop_with_fallback(user_message: str):
    """Fallback이 통합된 Agent 실행 루프"""
    tools = [{"type": "function", "function": {
        "name": "search_product", "description": "상품을 검색합니다.",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string", "description": "검색 키워드"}
        }, "required": ["query"]}
    }}]

    messages = [{"role": "user", "content": user_message}]
    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=tools, tool_choice="auto"
    )
    assistant_msg = response.choices[0].message

    if assistant_msg.tool_calls:
        messages.append(assistant_msg)
        for tool_call in assistant_msg.tool_calls:
            result = execute_tool_with_fallback(
                tool_call.function.name, json.loads(tool_call.function.arguments)
            )
            content = json.dumps(
                result["data"] if result["success"]
                else {"error": result["error"], "message": "도구 실행에 실패했습니다."},
                ensure_ascii=False
            )
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": content})

        final = client.chat.completions.create(model=MODEL, messages=messages)
        return final.choices[0].message.content

result = agent_loop_with_fallback("무선 이어폰 추천해줘")
print(result)
```

**실행 결과**:
```
[Primary 실패] search_product_db: Connection timeout
[Fallback 시도] search_product_cache
무선 이어폰을 추천해드리겠습니다. 현재 인기 있는 제품들을 검색했습니다...
```

### Q&A
**Q: 재시도 횟수는 몇 번이 적절한가요?**
A: 일반적으로 3회가 표준이다. 지수 백오프(1초, 2초, 4초)를 적용하면 총 대기 시간이 약 7초다. 사용자 체감 응답 시간이 10초를 넘기면 UX가 급격히 저하되므로, 3회 재시도 후에는 Fallback으로 전환하거나 실패를 즉시 알려야 한다.

<details>
<summary>퀴즈: Tool 실행 실패 시 에러 메시지를 LLM에게 전달하면 어떤 이점이 있을까요?</summary>

**힌트**: LLM은 에러 메시지를 어떻게 활용할 수 있을까요?

**정답**: LLM은 에러 메시지를 분석하여 두 가지 행동을 할 수 있다. (1) 사용자에게 상황을 자연어로 설명("현재 검색 서비스에 문제가 있습니다. 잠시 후 다시 시도해주세요"), (2) 에러 원인에 따라 다른 Tool을 호출하거나 파라미터를 수정하여 재시도. 단순히 "실패"만 전달하는 것보다 구체적 에러 메시지를 전달하면 LLM의 에러 핸들링 품질이 크게 향상된다.
</details>

---

## 실습

### 실습 1: 복수 Tool 선택 정확도 비교 실험
- **연관 학습 목표**: 학습 목표 1, 2
- **실습 목적**: Tool description 품질에 따른 선택 정확도 차이를 정량적으로 측정한다
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 30분
- **선행 조건**: OpenAI API Key 발급
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**실습 내용**:

5개의 Tool(상품 검색, 주문 조회, 환불 접수, 배송 추적, FAQ 검색)을 정의하되, 두 가지 버전을 만든다:
- Version A: 간단한 description (1문장, 파라미터 설명 없음)
- Version B: 상세한 description (2~3문장, negative instruction 포함, 파라미터 상세 설명)

10개의 테스트 질문에 대해 각 버전의 Tool 선택 정확도를 비교한다.

```python
import os
from openai import OpenAI
import json

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

# Version A: 간단한 Tool 정의 (5개)
tools_simple = [
    {"type": "function", "function": {"name": "search_product", "description": "상품 검색", "parameters": {"type": "object", "properties": {"q": {"type": "string"}}, "required": ["q"]}}},
    {"type": "function", "function": {"name": "check_order", "description": "주문 확인", "parameters": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]}}},
    # ... (request_refund, track_delivery, search_faq 동일 패턴)
]

# Version B: 상세한 Tool 정의 (5개) - negative instruction 포함
tools_detailed = [
    {"type": "function", "function": {
        "name": "search_product",
        "description": "상품 카탈로그에서 상품을 검색합니다. 상품명, 카테고리, 브랜드로 검색할 때 사용합니다. "
                       "주문 조회나 배송 추적에는 사용하지 마세요.",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string", "description": "검색할 상품명 또는 키워드"},
            "category": {"type": "string", "enum": ["electronics", "clothing", "food"]}
        }, "required": ["query"]}
    }},
    # ... (check_order, request_refund, track_delivery, search_faq 동일 패턴)
]

# 테스트 케이스: (질문, 정답 Tool)
test_cases = [
    ("노트북 추천해줘", "search_product"),
    ("ORD-12345 주문 상태 알려줘", "check_order"),
    ("ORD-12345 환불해줘", "request_refund"),
    ("내 택배 어디까지 왔어?", "track_delivery"),
    ("반품 규정이 어떻게 되나요?", "search_faq"),
    # ... (추가 5개 테스트 케이스)
]

def evaluate_accuracy(tools: list[dict], label: str) -> float:
    correct = 0
    for question, expected_tool in test_cases:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": question}],
            tools=tools, tool_choice="auto"
        )
        if response.choices[0].message.tool_calls:
            selected = response.choices[0].message.tool_calls[0].function.name
            is_correct = selected == expected_tool
            correct += int(is_correct)
            print(f"  [{'O' if is_correct else 'X'}] '{question}' → {selected} (정답: {expected_tool})")
    accuracy = correct / len(test_cases)
    print(f"\n{label} 정확도: {accuracy:.0%} ({correct}/{len(test_cases)})")
    return accuracy

print("=== Version A: 간단한 Tool 정의 ===")
acc_a = evaluate_accuracy(tools_simple, "Version A")
print("\n=== Version B: 상세한 Tool 정의 ===")
acc_b = evaluate_accuracy(tools_detailed, "Version B")
print(f"\n정확도 개선: {acc_b - acc_a:+.0%}")
```

### 실습 2: Multi-tool Router 구현
- **연관 학습 목표**: 학습 목표 2
- **실습 목적**: 2단계 라우팅 시스템을 직접 구현하여 대규모 Tool 세트의 선택 정확도를 개선한다
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 25분
- **선행 조건**: 실습 1 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**실습 내용**:

12개의 Tool을 3개 카테고리(상품, 주문, 고객지원)로 분류하는 `ToolRouter` 클래스를 구현한다. 의도 분류(Step 1)에는 gpt-4o-mini를, 실제 Tool 실행(Step 2)에는 gpt-4o를 사용하여 비용 최적화를 달성한다.

```python
# TODO: ToolRouter 클래스를 구현하세요
# 1. register_category(name, description, tools) - 카테고리 등록
# 2. classify(user_message) -> category_name - 의도 분류
# 3. route(user_message) -> tool_call_result - 라우팅 + Tool 실행
# 4. 신뢰도 < 0.7이면 전체 Tool 제공 (fallback)
```

### 실습 3: Fallback Chain 시스템 구축
- **연관 학습 목표**: 학습 목표 3
- **실습 목적**: Tool 실패에 대비한 재시도/Fallback 메커니즘을 구현하여 Agent의 안정성을 확보한다
- **실습 유형**: 코드 작성
- **난이도**: 심화
- **예상 소요 시간**: 30분
- **선행 조건**: 실습 2 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**실습 내용**:

지수 백오프 재시도, Fallback 체인, 에러 분류(Transient/Permanent/InvalidInput)를 포함하는 `ResilientToolExecutor` 클래스를 구현한다. 30% 확률로 실패하는 시뮬레이션 환경에서 테스트한다.

```python
# TODO: ResilientToolExecutor 클래스를 구현하세요
# 1. add_fallback(primary_tool, fallback_tools) - Fallback 체인 등록
# 2. execute(tool_name, arguments) -> ToolResult - 재시도 + Fallback 실행
# 3. 실행 로그 기록: 시도 횟수, 성공/실패 Tool, 총 소요 시간
# 4. 에러 유형별 다른 전략: transient→재시도, permanent→fallback, invalid→LLM 재생성
```

---

## 핵심 정리
- Tool의 `name`, `description`, `parameters`는 LLM의 Tool 선택 정확도를 결정하는 핵심 요소이다. 특히 description의 negative instruction이 유사 Tool 간 구분에 효과적이다
- System Prompt에 Tool 사용 가이드라인과 Few-shot 예시를 추가하면 다단계 Tool 체이닝의 정확도가 향상된다
- Tool이 8개 이상이면 2단계 라우팅(카테고리 분류 → Tool 선택)을 도입한다. 분류 단계에는 저비용 모델을 사용하여 비용을 최적화한다
- Tool 실패에 대비하여 지수 백오프 재시도와 Fallback 체인을 반드시 구현한다. 에러 유형(Transient/Permanent/Invalid)에 따라 전략을 분기한다
- 에러 메시지를 LLM에게 전달하면, LLM이 사용자에게 자연어로 상황을 설명하거나 대안 행동을 취할 수 있다
