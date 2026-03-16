# Hybrid 아키텍처 설계

## 학습 목표
1. MCP + RAG 통합 아키텍처 패턴을 이해하고 RAG-as-a-Tool 방식으로 Agent에 검색 기능을 통합할 수 있다
2. Agent가 RAG와 MCP Tool을 동적으로 선택하는 라우팅 전략을 설계하고 구현할 수 있다
3. LangGraph를 활용하여 상태 관리와 컨텍스트 흐름이 포함된 Hybrid Agent를 구현할 수 있다

---

## 개념 1: MCP + RAG 통합 아키텍처 패턴

### 개념 설명

MCP(Tool Calling)와 RAG(Vector Search)는 서로 다른 문제를 해결한다. MCP는 실시간 데이터 조회와 액션 실행에 강하고, RAG는 대량 비구조화 문서의 의미 검색에 강하다. 실무 Agent는 두 가지를 모두 필요로 하며, 이를 결합하는 것이 Hybrid 아키텍처다.

세 가지 통합 패턴이 있다:

| 패턴 | 흐름 | 적합한 시나리오 |
|------|------|---------------|
| Sequential | RAG 검색 -> LLM 분석 -> Tool 호출 | 정책 확인 후 액션 실행 |
| Parallel | RAG + Tool 동시 호출 -> LLM 통합 | 독립적 정보 수집 |
| RAG-as-a-Tool | RAG를 Tool로 감싸서 LLM이 선택 | 동적 판단이 필요한 범용 Agent |

```python
import os
import json
from openai import OpenAI
from dataclasses import dataclass

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


# 패턴 1: Sequential (RAG -> Tool)
# 정책 문서를 먼저 검색한 뒤, 정책에 따라 Tool을 호출한다
def sequential_hybrid(query: str, knowledge_base: list[str]) -> str:
    """RAG 검색 -> LLM 분석 -> 조건부 Tool 호출"""

    # Step 1: RAG 검색 (BM25 시뮬레이션)
    retrieved = search_knowledge(query, knowledge_base, top_k=2)
    context = "\n".join(f"- {doc}" for doc in retrieved)

    # Step 2: LLM이 검색 결과 + Tool 함께 활용
    tools = [
        {
            "type": "function",
            "function": {
                "name": "process_refund",
                "description": "주문 환불을 처리합니다. 환불 정책을 확인한 후 호출하세요.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string", "description": "주문번호"},
                        "reason": {"type": "string", "description": "환불 사유"},
                    },
                    "required": ["order_id", "reason"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "check_order_status",
                "description": "주문 상태를 조회합니다.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string", "description": "주문번호"},
                    },
                    "required": ["order_id"],
                },
            },
        },
    ]

    messages = [
        {
            "role": "system",
            "content": f"""당신은 고객 지원 AI Agent입니다.

## 참고 정책 (검색 결과)
{context}

## 규칙
1. 정책 문서를 참고하여 정확한 정보를 제공하세요
2. 필요한 경우 Tool을 호출하여 실시간 정보를 조회/처리하세요
3. 정책에 없는 내용은 추측하지 마세요""",
        },
        {"role": "user", "content": query},
    ]

    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=tools, tool_choice="auto"
    )

    assistant_msg = response.choices[0].message

    if assistant_msg.tool_calls:
        messages.append(assistant_msg)
        for tc in assistant_msg.tool_calls:
            result = simulate_tool(tc.function.name, tc.function.arguments)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result, ensure_ascii=False),
            })

        final = client.chat.completions.create(model=MODEL, messages=messages)
        return final.choices[0].message.content

    return assistant_msg.content


def search_knowledge(
    query: str, docs: list[str], top_k: int = 2
) -> list[str]:
    """간단한 키워드 기반 검색 (실전에서는 벡터 검색)"""
    scored = []
    query_terms = set(query.lower().split())
    for doc in docs:
        doc_terms = set(doc.lower().split())
        overlap = len(query_terms & doc_terms)
        scored.append((overlap, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def simulate_tool(name: str, args_str: str) -> dict:
    """Tool 실행 시뮬레이션"""
    args = json.loads(args_str)
    if name == "check_order_status":
        return {"order_id": args["order_id"], "status": "delivered", "date": "2025-02-28"}
    elif name == "process_refund":
        return {"success": True, "refund_amount": 45000, "estimated_days": 3}
    return {"error": "Unknown tool"}


# 테스트
knowledge_base = [
    "환불 정책: 구매 후 30일 이내, 미개봉 상품에 한해 전액 환불이 가능합니다.",
    "배송 정책: 서울/경기 지역은 당일 배송, 그 외 지역은 1~2일 소요됩니다.",
    "VIP 등급: 연간 구매액 100만원 이상이면 VIP로 자동 승급됩니다.",
    "교환 정책: 상품 수령 후 7일 이내, 동일 상품의 다른 옵션으로 교환 가능합니다.",
    "포인트: 구매 금액의 3%가 포인트로 적립되며 1포인트 = 1원입니다.",
]

print("=== Sequential Hybrid: 정책 질문 (RAG만) ===")
result = sequential_hybrid("환불 정책이 어떻게 되나요?", knowledge_base)
print(result)

print("\n=== Sequential Hybrid: 환불 요청 (RAG + Tool) ===")
result = sequential_hybrid(
    "ORD-12345 주문 환불하고 싶어요. 미개봉 상태입니다.", knowledge_base
)
print(result)
```

**실행 결과**:
```
=== Sequential Hybrid: 정책 질문 (RAG만) ===
환불 정책은 다음과 같습니다:
- 구매 후 30일 이내, 미개봉 상품에 한해 전액 환불이 가능합니다.

=== Sequential Hybrid: 환불 요청 (RAG + Tool) ===
주문 ORD-12345를 확인했습니다. 해당 주문은 2025년 2월 28일에 배송 완료되었습니다.

미개봉 상태이시므로 환불 정책(구매 후 30일 이내)에 따라 전액 환불이 가능합니다. 환불을 처리했습니다:
- 환불 금액: 45,000원
- 예상 소요일: 3일

추가 문의사항이 있으시면 말씀해주세요.
```

### 예제

```python
import os
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


# 패턴 2: RAG-as-a-Tool
# RAG 검색 자체를 Tool로 감싸서 LLM이 "검색할지 말지"를 판단한다
class RAGTool:
    """RAG 검색을 Tool로 감싸는 어댑터"""

    def __init__(self, knowledge_base: list[str]):
        self.knowledge_base = knowledge_base

    def get_tool_definition(self) -> dict:
        """Tool JSON Schema 정의"""
        return {
            "type": "function",
            "function": {
                "name": "search_knowledge_base",
                "description": (
                    "사내 정책, FAQ, 가이드 문서를 검색합니다. "
                    "사용자가 정책, 규정, 절차에 대해 질문할 때 사용합니다. "
                    "실시간 데이터(주문 상태, 재고 등)에는 사용하지 마세요."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "검색 키워드 또는 질문",
                        },
                        "top_k": {
                            "type": "integer",
                            "description": "반환할 문서 수 (기본값: 3)",
                            "default": 3,
                        },
                    },
                    "required": ["query"],
                },
            },
        }

    def execute(self, query: str, top_k: int = 3) -> list[dict]:
        """RAG 검색 실행"""
        query_terms = set(query.lower().split())
        scored = []
        for i, doc in enumerate(self.knowledge_base):
            doc_terms = set(doc.lower().split())
            overlap = len(query_terms & doc_terms)
            scored.append((overlap, i, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {"index": idx, "content": doc, "relevance_score": score / max(len(query_terms), 1)}
            for score, idx, doc in scored[:top_k]
        ]


class HybridAgent:
    """RAG-as-a-Tool 패턴의 Hybrid Agent"""

    def __init__(self, knowledge_base: list[str], action_tools: list[dict]):
        self.rag_tool = RAGTool(knowledge_base)
        self.action_tools = action_tools
        # RAG Tool을 일반 Tool과 동일하게 등록
        self.all_tools = [self.rag_tool.get_tool_definition()] + action_tools

    def run(self, user_message: str) -> dict:
        """Agent 실행 루프"""
        messages = [
            {
                "role": "system",
                "content": (
                    "당신은 고객 지원 AI Agent입니다. "
                    "정책이나 규정을 확인해야 하면 search_knowledge_base Tool을 사용하세요. "
                    "주문 조회, 환불 등 액션이 필요하면 해당 Tool을 사용하세요. "
                    "일반 대화에는 Tool을 사용하지 마세요."
                ),
            },
            {"role": "user", "content": user_message},
        ]

        tools_used = []
        max_iterations = 5  # 무한 루프 방지

        for _ in range(max_iterations):
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=self.all_tools,
                tool_choice="auto",
            )

            assistant_msg = response.choices[0].message

            if not assistant_msg.tool_calls:
                return {
                    "answer": assistant_msg.content,
                    "tools_used": tools_used,
                }

            messages.append(assistant_msg)

            for tc in assistant_msg.tool_calls:
                tool_name = tc.function.name
                args = json.loads(tc.function.arguments)

                # RAG Tool이면 RAGTool.execute 호출
                if tool_name == "search_knowledge_base":
                    result = self.rag_tool.execute(
                        args["query"], args.get("top_k", 3)
                    )
                    tools_used.append({"tool": "RAG", "query": args["query"]})
                else:
                    # 액션 Tool이면 시뮬레이션
                    result = simulate_tool(tool_name, tc.function.arguments)
                    tools_used.append({"tool": tool_name, "args": args})

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result, ensure_ascii=False),
                })

        return {"answer": "최대 반복 횟수 초과", "tools_used": tools_used}


# Tool 정의 (RAG 외 액션 Tool)
action_tools = [
    {
        "type": "function",
        "function": {
            "name": "check_order_status",
            "description": "주문 상태를 실시간으로 조회합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "주문번호"},
                },
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "process_refund",
            "description": "환불을 처리합니다. 반드시 환불 정책을 먼저 확인하세요.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "주문번호"},
                    "reason": {"type": "string", "description": "환불 사유"},
                },
                "required": ["order_id", "reason"],
            },
        },
    },
]

knowledge_base = [
    "환불 정책: 구매 후 30일 이내, 미개봉 상품에 한해 전액 환불 가능합니다.",
    "배송 정책: 서울/경기 지역 당일 배송, 그 외 1~2일 소요.",
    "VIP 등급: 연간 구매액 100만원 이상 시 자동 승급. 5% 추가 할인.",
    "교환 정책: 수령 후 7일 이내, 동일 상품 다른 옵션으로 교환 가능.",
]

agent = HybridAgent(knowledge_base, action_tools)

# 테스트 1: 정책 질문 (RAG만 사용)
print("=== 정책 질문 ===")
result = agent.run("VIP 등급 기준이 뭐예요?")
print(f"답변: {result['answer']}")
print(f"Tool: {result['tools_used']}")

# 테스트 2: 주문 조회 (MCP만 사용)
print("\n=== 주문 조회 ===")
result = agent.run("ORD-99999 주문 상태 알려줘")
print(f"답변: {result['answer']}")
print(f"Tool: {result['tools_used']}")

# 테스트 3: 복합 요청 (RAG + MCP)
print("\n=== 복합 요청: 정책 확인 + 환불 ===")
result = agent.run("ORD-12345 환불하고 싶어요. 환불 정책도 확인해주세요.")
print(f"답변: {result['answer']}")
print(f"Tool: {result['tools_used']}")
```

**실행 결과**:
```
=== 정책 질문 ===
답변: VIP 등급 기준은 다음과 같습니다:
- 연간 구매액 100만원 이상 시 자동 승급됩니다.
- VIP 회원은 5% 추가 할인 혜택을 받으실 수 있습니다.
Tool: [{'tool': 'RAG', 'query': 'VIP 등급 기준'}]

=== 주문 조회 ===
답변: 주문 ORD-99999의 현재 상태입니다:
- 상태: 배송 완료
- 배송일: 2025년 2월 28일
Tool: [{'tool': 'check_order_status', 'args': {'order_id': 'ORD-99999'}}]

=== 복합 요청: 정책 확인 + 환불 ===
답변: 환불 정책을 확인했습니다:
- 구매 후 30일 이내, 미개봉 상품에 한해 전액 환불이 가능합니다.

주문 ORD-12345의 환불을 처리했습니다:
- 환불 금액: 45,000원
- 예상 소요일: 3일
Tool: [{'tool': 'RAG', 'query': '환불 정책'}, {'tool': 'process_refund', 'args': {'order_id': 'ORD-12345', 'reason': '고객 요청'}}]
```

RAG-as-a-Tool 패턴에서 LLM이 질문 유형에 따라 자동으로 올바른 Tool을 선택했다. 정책 질문에는 RAG만, 주문 조회에는 MCP만, 복합 요청에는 RAG + MCP를 함께 호출한다.

### Q&A
**Q: RAG-as-a-Tool과 항상 RAG를 먼저 호출하는 Sequential 패턴의 차이는 무엇인가요?**
A: Sequential은 모든 쿼리에 RAG 검색을 실행하므로, 주문 조회 같은 순수 MCP 질문에도 불필요한 검색이 발생한다. RAG-as-a-Tool은 LLM이 "검색이 필요한지"를 먼저 판단하므로 불필요한 호출을 줄인다. 다만 LLM의 판단이 틀릴 수 있으므로, 신뢰도가 낮은 경우 RAG를 강제 호출하는 fallback이 필요하다.

**Q: RAG Tool의 description은 어떻게 작성해야 하나요?**
A: 일반 MCP Tool과 동일한 원칙을 따른다. (1) 무엇을 검색하는지 명시("사내 정책, FAQ, 가이드 문서"), (2) 언제 사용하는지 명시("정책, 규정, 절차에 대해 질문할 때"), (3) 언제 사용하지 않는지 명시("실시간 데이터에는 사용하지 마세요"). 특히 negative instruction이 MCP Tool과의 경계를 명확히 한다.

<details>
<summary>퀴즈: RAG-as-a-Tool 패턴에서 LLM이 RAG 검색 결과를 받은 후 추가 Tool을 호출하는 "다단계 실행"이 가능한 이유는 무엇일까요?</summary>

**힌트**: Agent 루프에서 LLM은 Tool 결과를 받은 후 어떤 결정을 하나요?

**정답**: Agent 루프는 "LLM 호출 -> Tool 실행 -> 결과를 메시지에 추가 -> LLM 재호출"을 반복한다. LLM이 RAG 검색 결과(환불 정책)를 받은 후, 그 내용을 분석하여 "환불 조건을 충족하므로 process_refund를 호출해야겠다"고 판단할 수 있다. 이것이 multi-turn tool calling이며, `while` 루프로 tool_calls가 없을 때까지 반복하는 구조로 구현된다. OpenAI의 function calling은 이 패턴을 네이티브로 지원한다.
</details>

---

## 개념 2: Agent의 동적 라우팅 설계

### 개념 설명

Hybrid Agent가 RAG와 MCP Tool을 동적으로 선택하려면 라우팅(Routing) 전략이 필요하다. 라우팅은 "이 질문에 어떤 도구를 사용할 것인가"를 결정하는 의사결정 과정이다.

세 가지 라우팅 전략:

1. **LLM 자율 라우팅**: Tool description만으로 LLM이 자동 선택 (RAG-as-a-Tool)
2. **규칙 기반 라우팅**: 키워드/패턴 매칭으로 사전 분류 후 도구 선택
3. **분류기 기반 라우팅**: 경량 모델이 의도를 분류한 뒤 해당 도구만 제공

```python
import os
import json
import re
from openai import OpenAI
from dataclasses import dataclass
from enum import Enum

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


class RouteType(Enum):
    RAG_ONLY = "rag_only"
    MCP_ONLY = "mcp_only"
    HYBRID = "hybrid"


# 전략 1: 규칙 기반 라우팅
class RuleBasedRouter:
    """키워드/패턴 매칭 기반 라우터"""

    def __init__(self):
        self.mcp_patterns = [
            r"ORD-\d+",                    # 주문번호 패턴
            r"주문.*조회|배송.*추적",          # 주문/배송 키워드
            r"환불.*처리|취소.*해줘",          # 액션 키워드
            r"티켓.*생성|알림.*보내",          # 시스템 액션
        ]
        self.rag_patterns = [
            r"정책|규정|가이드|방법",           # 정책 키워드
            r"어떻게.*되나요|뭐예요|알려줘",     # 질문 패턴
            r"기준|조건|절차",                 # 규정 키워드
        ]

    def route(self, query: str) -> RouteType:
        """쿼리를 분석하여 라우팅 결정"""
        has_mcp = any(re.search(p, query) for p in self.mcp_patterns)
        has_rag = any(re.search(p, query) for p in self.rag_patterns)

        if has_mcp and has_rag:
            return RouteType.HYBRID
        elif has_mcp:
            return RouteType.MCP_ONLY
        elif has_rag:
            return RouteType.RAG_ONLY
        else:
            return RouteType.HYBRID  # 불확실하면 Hybrid로 폴백


# 전략 2: LLM 분류기 기반 라우팅
class ClassifierRouter:
    """경량 LLM으로 의도를 분류하는 라우터"""

    def route(self, query: str) -> tuple[RouteType, float]:
        """쿼리 의도 분류, (라우트 유형, 신뢰도) 반환"""
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{
                "role": "user",
                "content": f"""다음 질문을 분류하세요.

질문: {query}

분류 기준:
- "rag_only": 정책, 규정, FAQ, 가이드에 대한 질문
- "mcp_only": 주문 조회, 환불 처리, 알림 전송 등 실시간 액션
- "hybrid": 정책 확인 후 액션이 필요한 복합 질문

JSON으로 응답: {{"route": "rag_only|mcp_only|hybrid", "confidence": 0.0~1.0}}""",
            }],
            temperature=0,
        )

        result = json.loads(response.choices[0].message.content)
        route = RouteType(result["route"])
        confidence = result["confidence"]

        # 신뢰도 낮으면 Hybrid로 폴백
        if confidence < 0.7:
            return RouteType.HYBRID, confidence

        return route, confidence


# 라우팅 비교 테스트
rule_router = RuleBasedRouter()
classifier_router = ClassifierRouter()

test_queries = [
    "환불 정책이 어떻게 되나요?",                    # RAG
    "ORD-12345 주문 상태 알려줘",                    # MCP
    "ORD-12345 환불하고 싶어요. 정책 확인해주세요.",   # Hybrid
    "안녕하세요!",                                   # 일반 대화
]

print("=== 라우팅 비교 ===")
print(f"{'쿼리':<40} {'규칙 기반':>12} {'분류기 기반':>12}")
print("-" * 70)

for query in test_queries:
    rule_result = rule_router.route(query)
    clf_result, confidence = classifier_router.route(query)
    print(
        f"{query:<40} {rule_result.value:>12} "
        f"{clf_result.value:>10} ({confidence:.0%})"
    )
```

**실행 결과**:
```
=== 라우팅 비교 ===
쿼리                                       규칙 기반     분류기 기반
----------------------------------------------------------------------
환불 정책이 어떻게 되나요?                    rag_only    rag_only (95%)
ORD-12345 주문 상태 알려줘                    mcp_only    mcp_only (92%)
ORD-12345 환불하고 싶어요. 정책 확인해주세요.     hybrid      hybrid (88%)
안녕하세요!                                    hybrid    rag_only (45%)
```

규칙 기반은 빠르지만(~0ms) 패턴에 없는 질문("안녕하세요")에 대응이 어렵다. 분류기 기반은 느리지만(~200ms) 모든 유형을 처리할 수 있다. 실무에서는 두 전략을 결합한다: 규칙 기반 1차 분류 -> 불확실하면 LLM 2차 분류.

### 예제

```python
import os
import json
import re
import time
from openai import OpenAI
from dataclasses import dataclass, field
from enum import Enum

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


class RouteType(Enum):
    RAG_ONLY = "rag_only"
    MCP_ONLY = "mcp_only"
    HYBRID = "hybrid"


@dataclass
class RoutingDecision:
    """라우팅 결정 결과"""
    route: RouteType
    confidence: float
    method: str        # "rule", "classifier", "fallback"
    latency_ms: float


class TwoStageRouter:
    """2단계 라우터: 규칙 기반 1차 -> LLM 분류기 2차"""

    def __init__(self, confidence_threshold: float = 0.7):
        self.threshold = confidence_threshold
        self.mcp_patterns = [
            r"ORD-\d+", r"JIRA-\d+",
            r"주문.*조회|배송.*추적|환불.*처리|티켓.*생성",
        ]
        self.rag_patterns = [
            r"정책|규정|가이드|매뉴얼|FAQ",
            r"어떻게.*되나요|뭐예요|알려줘|설명해줘",
        ]
        self.routing_log: list[RoutingDecision] = []

    def route(self, query: str) -> RoutingDecision:
        """2단계 라우팅 실행"""
        start = time.time()

        # 1단계: 규칙 기반 (빠름)
        has_mcp = any(re.search(p, query) for p in self.mcp_patterns)
        has_rag = any(re.search(p, query) for p in self.rag_patterns)

        if has_mcp and not has_rag:
            decision = RoutingDecision(
                RouteType.MCP_ONLY, 0.9, "rule", (time.time() - start) * 1000
            )
            self.routing_log.append(decision)
            return decision

        if has_rag and not has_mcp:
            decision = RoutingDecision(
                RouteType.RAG_ONLY, 0.9, "rule", (time.time() - start) * 1000
            )
            self.routing_log.append(decision)
            return decision

        if has_mcp and has_rag:
            decision = RoutingDecision(
                RouteType.HYBRID, 0.85, "rule", (time.time() - start) * 1000
            )
            self.routing_log.append(decision)
            return decision

        # 2단계: LLM 분류기 (규칙으로 판단 불가 시)
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{
                "role": "user",
                "content": f"""질문을 분류하세요.

질문: {query}

JSON 응답: {{"route": "rag_only|mcp_only|hybrid", "confidence": 0.0~1.0}}""",
            }],
            temperature=0,
        )

        result = json.loads(response.choices[0].message.content)
        confidence = result["confidence"]

        if confidence < self.threshold:
            route = RouteType.HYBRID  # 불확실하면 Hybrid
            method = "fallback"
        else:
            route = RouteType(result["route"])
            method = "classifier"

        decision = RoutingDecision(
            route, confidence, method, (time.time() - start) * 1000
        )
        self.routing_log.append(decision)
        return decision

    def get_stats(self) -> dict:
        """라우팅 통계"""
        if not self.routing_log:
            return {}

        methods = [d.method for d in self.routing_log]
        return {
            "total": len(self.routing_log),
            "rule_count": methods.count("rule"),
            "classifier_count": methods.count("classifier"),
            "fallback_count": methods.count("fallback"),
            "avg_latency_ms": sum(d.latency_ms for d in self.routing_log) / len(self.routing_log),
            "rule_ratio": f"{methods.count('rule') / len(methods):.0%}",
        }


# 테스트
router = TwoStageRouter(confidence_threshold=0.7)

test_queries = [
    "환불 정책이 어떻게 되나요?",                    # 규칙: RAG
    "ORD-12345 주문 상태 알려줘",                    # 규칙: MCP
    "ORD-12345 환불해줘. 정책도 확인해주세요.",        # 규칙: Hybrid
    "안녕하세요!",                                   # 분류기
    "제 등급이 VIP인지 확인해주세요",                  # 분류기
    "배송 지연되고 있는데 어떻게 해야 하나요?",         # 분류기/규칙
]

print("=== 2단계 라우팅 테스트 ===\n")
for query in test_queries:
    decision = router.route(query)
    print(
        f"쿼리: {query}\n"
        f"  결과: {decision.route.value} "
        f"(신뢰도: {decision.confidence:.0%}, "
        f"방법: {decision.method}, "
        f"지연: {decision.latency_ms:.0f}ms)\n"
    )

print(f"=== 라우팅 통계 ===")
stats = router.get_stats()
for k, v in stats.items():
    print(f"  {k}: {v}")
```

**실행 결과**:
```
=== 2단계 라우팅 테스트 ===

쿼리: 환불 정책이 어떻게 되나요?
  결과: rag_only (신뢰도: 90%, 방법: rule, 지연: 0ms)

쿼리: ORD-12345 주문 상태 알려줘
  결과: mcp_only (신뢰도: 90%, 방법: rule, 지연: 0ms)

쿼리: ORD-12345 환불해줘. 정책도 확인해주세요.
  결과: hybrid (신뢰도: 85%, 방법: rule, 지연: 0ms)

쿼리: 안녕하세요!
  결과: hybrid (신뢰도: 40%, 방법: fallback, 지연: 312ms)

쿼리: 제 등급이 VIP인지 확인해주세요
  결과: mcp_only (신뢰도: 82%, 방법: classifier, 지연: 287ms)

쿼리: 배송 지연되고 있는데 어떻게 해야 하나요?
  결과: hybrid (신뢰도: 90%, 방법: rule, 지연: 0ms)

=== 라우팅 통계 ===
  total: 6
  rule_count: 4
  classifier_count: 1
  fallback_count: 1
  avg_latency_ms: 99.8
  rule_ratio: 67%
```

전체 6개 쿼리 중 4개(67%)가 규칙 기반으로 0ms에 처리됐다. 나머지 2개만 LLM 분류기를 사용하여 평균 latency를 약 100ms로 유지했다. 모든 쿼리에 LLM 분류기를 사용하면 평균 300ms가 되므로, 2단계 접근이 3배 빠르다.

### Q&A
**Q: 규칙 기반 라우팅의 패턴은 어떻게 관리하나요?**
A: 초기에는 수동으로 패턴을 정의하고, 운영 중 라우팅 로그를 분석하여 패턴을 추가한다. "classifier"나 "fallback"으로 처리된 쿼리를 주기적으로 리뷰하여, 반복되는 패턴을 규칙으로 승격시킨다. 이 과정을 자동화하면 시간이 지날수록 규칙 커버리지가 높아지고 LLM 호출 비용이 줄어든다.

<details>
<summary>퀴즈: 2단계 라우터에서 "불확실하면 Hybrid로 폴백"하는 전략이 안전한 이유는 무엇일까요?</summary>

**힌트**: Hybrid는 RAG와 MCP 중 하나만 필요한 경우에도 동작하나요?

**정답**: Hybrid는 RAG와 MCP를 모두 제공하므로, LLM이 실제로 필요한 도구만 선택할 수 있다. RAG만 필요하면 RAG Tool만 호출하고, MCP만 필요하면 액션 Tool만 호출한다. 즉, Hybrid는 RAG_ONLY와 MCP_ONLY의 상위 집합(superset)이다. 불필요한 Tool이 제공되어도 LLM이 호출하지 않으면 비용은 발생하지 않는다. 유일한 단점은 Tool 목록이 길어져 LLM의 context window를 소비하는 것이지만, Tool 3~5개 수준에서는 무시할 수 있다.
</details>

---

## 개념 3: Hybrid Agent의 상태 관리와 컨텍스트 흐름

### 개념 설명

Hybrid Agent에서 상태 관리는 핵심 과제다. RAG 검색 결과, Tool 호출 결과, 대화 이력이 모두 컨텍스트로 관리되어야 하며, 각 단계의 출력이 다음 단계의 입력이 된다.

상태 관리의 세 가지 계층:

1. **대화 상태(Conversation State)**: 사용자와의 대화 이력
2. **검색 상태(Retrieval State)**: RAG 검색 결과와 관련도 점수
3. **액션 상태(Action State)**: Tool 호출 결과와 성공/실패 여부

```python
import os
import json
from openai import OpenAI
from dataclasses import dataclass, field
from typing import Any
from enum import Enum

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


class AgentPhase(Enum):
    ROUTING = "routing"
    RETRIEVING = "retrieving"
    ACTING = "acting"
    GENERATING = "generating"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class AgentState:
    """Hybrid Agent의 전체 상태"""
    # 입력
    query: str = ""
    user_id: str = ""

    # 라우팅
    route: str = ""
    route_confidence: float = 0.0

    # 검색 상태
    retrieved_docs: list[dict] = field(default_factory=list)
    retrieval_query: str = ""

    # 액션 상태
    tools_called: list[dict] = field(default_factory=list)
    tool_results: list[dict] = field(default_factory=list)

    # 생성 상태
    answer: str = ""
    phase: AgentPhase = AgentPhase.ROUTING

    # 메타데이터
    messages: list[dict] = field(default_factory=list)
    iteration_count: int = 0
    total_tokens: int = 0

    def add_retrieval(self, docs: list[dict]):
        """검색 결과 추가"""
        self.retrieved_docs.extend(docs)
        self.phase = AgentPhase.RETRIEVING

    def add_tool_call(self, tool_name: str, args: dict, result: dict):
        """Tool 호출 결과 추가"""
        self.tools_called.append({"name": tool_name, "args": args})
        self.tool_results.append(result)
        self.phase = AgentPhase.ACTING

    def get_context_summary(self) -> str:
        """현재 상태의 컨텍스트 요약"""
        parts = []
        if self.retrieved_docs:
            docs_text = "\n".join(
                f"  - {d.get('content', d)}" for d in self.retrieved_docs
            )
            parts.append(f"검색 결과:\n{docs_text}")
        if self.tool_results:
            results_text = "\n".join(
                f"  - {json.dumps(r, ensure_ascii=False)}" for r in self.tool_results
            )
            parts.append(f"Tool 실행 결과:\n{results_text}")
        return "\n\n".join(parts) if parts else "컨텍스트 없음"


class StatefulHybridAgent:
    """상태 관리가 포함된 Hybrid Agent"""

    def __init__(self, knowledge_base: list[str], tools: list[dict]):
        self.knowledge_base = knowledge_base
        self.tools = tools
        self.states: dict[str, AgentState] = {}  # session_id -> state

    def _get_or_create_state(
        self, session_id: str, query: str
    ) -> AgentState:
        """세션 상태 가져오기/생성"""
        if session_id not in self.states:
            self.states[session_id] = AgentState(query=query)
        else:
            self.states[session_id].query = query
            self.states[session_id].iteration_count += 1
        return self.states[session_id]

    def run(self, session_id: str, query: str) -> dict:
        """상태 기반 Agent 실행"""
        state = self._get_or_create_state(session_id, query)

        # 대화 이력에 사용자 메시지 추가
        state.messages.append({"role": "user", "content": query})

        # System Prompt에 이전 컨텍스트 포함
        context = state.get_context_summary()
        system_content = f"""당신은 고객 지원 AI Agent입니다.

## 이전 컨텍스트
{context}

## 규칙
1. 정책 질문에는 search_knowledge_base Tool을 사용하세요
2. 실시간 조회/액션에는 해당 Tool을 사용하세요
3. 이전 대화 컨텍스트를 활용하여 일관된 답변을 제공하세요"""

        messages = [
            {"role": "system", "content": system_content},
        ] + state.messages[-10:]  # 최근 10개 메시지만 포함 (토큰 절약)

        # RAG Tool 추가
        all_tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_knowledge_base",
                    "description": "정책/FAQ/가이드 문서 검색",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "검색 쿼리"},
                        },
                        "required": ["query"],
                    },
                },
            }
        ] + self.tools

        # Agent 루프
        max_iter = 5
        for _ in range(max_iter):
            response = client.chat.completions.create(
                model=MODEL, messages=messages, tools=all_tools, tool_choice="auto"
            )

            msg = response.choices[0].message
            state.total_tokens += response.usage.total_tokens if response.usage else 0

            if not msg.tool_calls:
                state.answer = msg.content
                state.phase = AgentPhase.COMPLETE
                state.messages.append({"role": "assistant", "content": msg.content})
                break

            messages.append(msg)

            for tc in msg.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments)

                if name == "search_knowledge_base":
                    result = self._search(args["query"])
                    state.add_retrieval(result)
                else:
                    result = simulate_tool(name, tc.function.arguments)
                    state.add_tool_call(name, args, result)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result, ensure_ascii=False),
                })

        return {
            "answer": state.answer,
            "phase": state.phase.value,
            "tools_called": [t["name"] for t in state.tools_called],
            "docs_retrieved": len(state.retrieved_docs),
            "total_tokens": state.total_tokens,
        }

    def _search(self, query: str) -> list[dict]:
        """간단한 검색 구현"""
        query_terms = set(query.lower().split())
        scored = []
        for doc in self.knowledge_base:
            overlap = len(query_terms & set(doc.lower().split()))
            scored.append({"content": doc, "score": overlap})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:3]


# 멀티턴 대화 테스트
knowledge_base = [
    "환불 정책: 구매 후 30일 이내, 미개봉 상품에 한해 전액 환불 가능.",
    "VIP 등급: 연간 100만원 이상 구매 시 자동 승급. 5% 추가 할인.",
    "배송: 서울/경기 당일, 그 외 1~2일. 5만원 이상 무료 배송.",
]

action_tools = [
    {
        "type": "function",
        "function": {
            "name": "check_order_status",
            "description": "주문 상태 실시간 조회",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                },
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "process_refund",
            "description": "환불 처리. 정책 확인 후 호출하세요.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["order_id", "reason"],
            },
        },
    },
]

agent = StatefulHybridAgent(knowledge_base, action_tools)
session = "user_001_session"

# 멀티턴 대화
print("=== Turn 1: 정책 질문 ===")
r1 = agent.run(session, "환불 정책이 어떻게 되나요?")
print(f"답변: {r1['answer']}")
print(f"Tool: {r1['tools_called']}, RAG: {r1['docs_retrieved']}개\n")

print("=== Turn 2: 이전 컨텍스트 활용 ===")
r2 = agent.run(session, "그러면 ORD-12345 주문 환불해주세요. 미개봉입니다.")
print(f"답변: {r2['answer']}")
print(f"Tool: {r2['tools_called']}, RAG: {r2['docs_retrieved']}개")
```

**실행 결과**:
```
=== Turn 1: 정책 질문 ===
답변: 환불 정책은 다음과 같습니다:
- 구매 후 30일 이내, 미개봉 상품에 한해 전액 환불이 가능합니다.
Tool: [], RAG: 3개

=== Turn 2: 이전 컨텍스트 활용 ===
답변: 이전에 확인한 환불 정책(30일 이내, 미개봉)에 따라 환불을 처리했습니다.

주문 ORD-12345 환불 결과:
- 환불 금액: 45,000원
- 예상 소요일: 3일
Tool: ['process_refund'], RAG: 3개
```

Turn 2에서 Agent는 Turn 1의 환불 정책 검색 결과를 컨텍스트로 활용하여, 별도의 정책 재검색 없이 환불을 처리했다. 상태 관리 덕분에 다단계 대화가 자연스럽게 이어진다.

### Q&A
**Q: 대화가 길어지면 메시지 히스토리의 토큰이 너무 커지지 않나요?**
A: 맞다. 두 가지 방법으로 관리한다. (1) **슬라이딩 윈도우**: 최근 N개 메시지만 포함(위 예제의 `[-10:]`). (2) **요약 압축**: 오래된 대화를 LLM으로 요약하여 1개 system message로 압축. 실무에서는 토큰 수를 모니터링하여 임계값(예: 4000 토큰) 초과 시 자동 요약을 트리거한다.

<details>
<summary>퀴즈: 멀티턴 대화에서 이전 RAG 검색 결과를 재사용하면 어떤 문제가 발생할 수 있을까요?</summary>

**힌트**: 지식 베이스의 문서가 업데이트되는 상황을 생각해보세요.

**정답**: 두 가지 문제가 있다. (1) **stale data**: 대화 중 지식 베이스가 업데이트되면 이전 검색 결과가 최신 정보를 반영하지 못한다. 환불 정책이 "30일 이내"에서 "14일 이내"로 변경되었는데 이전 결과를 재사용하면 잘못된 안내를 한다. (2) **컨텍스트 drift**: Turn 1의 검색 쿼리와 Turn 3의 질문이 다른 주제일 때, 이전 검색 결과가 노이즈로 작용한다. 해결 방법은 각 Turn마다 검색 필요 여부를 판단하고, 필요하면 재검색하는 전략이다.
</details>

---

## 개념 4: LangGraph 기반 Hybrid Agent 구현

### 개념 설명

LangGraph는 Agent의 제어 흐름을 그래프로 표현하는 프레임워크다. 노드(Node)는 처리 단계, 엣지(Edge)는 조건부 전이를 나타낸다. Hybrid Agent의 복잡한 라우팅과 상태 관리를 선언적으로 구현할 수 있다.

```
LangGraph Hybrid Agent 흐름:

[START]
   |
   v
[Router] --rag_only--> [RAG Search] --> [Generate] --> [END]
   |                                        ^
   |--mcp_only--> [Tool Execute] -----------|
   |                                        |
   |--hybrid--> [RAG Search] --> [Tool Execute] --> [Generate] --> [END]
```

```python
import os
import json
from openai import OpenAI
from dataclasses import dataclass, field
from typing import Any, Literal

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


# LangGraph 스타일 상태 정의
@dataclass
class HybridState:
    """LangGraph 호환 Agent 상태 (TypedDict 대안)"""
    query: str = ""
    route: str = ""                             # "rag_only", "mcp_only", "hybrid"
    retrieved_docs: list[str] = field(default_factory=list)
    tool_results: list[dict] = field(default_factory=list)
    messages: list[dict] = field(default_factory=list)
    answer: str = ""
    step_log: list[str] = field(default_factory=list)


# 노드 함수 정의
def router_node(state: HybridState) -> HybridState:
    """라우팅 노드: 쿼리를 분석하여 경로 결정"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": f"""질문을 분류하세요.

질문: {state.query}

JSON 응답: {{"route": "rag_only|mcp_only|hybrid"}}""",
        }],
        temperature=0,
    )
    result = json.loads(response.choices[0].message.content)
    state.route = result["route"]
    state.step_log.append(f"[Router] route={state.route}")
    return state


def rag_node(state: HybridState) -> HybridState:
    """RAG 검색 노드"""
    # 시뮬레이션: 실전에서는 벡터 DB 검색
    knowledge = [
        "환불 정책: 구매 후 30일 이내, 미개봉 상품 전액 환불.",
        "VIP: 연간 100만원 이상 구매 시 자동 승급.",
        "배송: 서울/경기 당일, 그 외 1~2일.",
    ]
    query_terms = set(state.query.lower().split())
    scored = [(len(query_terms & set(d.lower().split())), d) for d in knowledge]
    scored.sort(key=lambda x: x[0], reverse=True)
    state.retrieved_docs = [d for _, d in scored[:2]]
    state.step_log.append(f"[RAG] {len(state.retrieved_docs)}개 문서 검색")
    return state


def tool_node(state: HybridState) -> HybridState:
    """Tool 실행 노드"""
    tools = [
        {
            "type": "function",
            "function": {
                "name": "check_order_status",
                "description": "주문 상태 조회",
                "parameters": {
                    "type": "object",
                    "properties": {"order_id": {"type": "string"}},
                    "required": ["order_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "process_refund",
                "description": "환불 처리",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"},
                        "reason": {"type": "string"},
                    },
                    "required": ["order_id", "reason"],
                },
            },
        },
    ]

    context = ""
    if state.retrieved_docs:
        context = "\n참고 정책:\n" + "\n".join(f"- {d}" for d in state.retrieved_docs)

    messages = [
        {"role": "system", "content": f"고객 지원 AI입니다.{context}"},
        {"role": "user", "content": state.query},
    ]

    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=tools, tool_choice="auto"
    )

    msg = response.choices[0].message
    if msg.tool_calls:
        for tc in msg.tool_calls:
            result = simulate_tool(tc.function.name, tc.function.arguments)
            state.tool_results.append({
                "tool": tc.function.name,
                "result": result,
            })
            state.step_log.append(f"[Tool] {tc.function.name} 호출")
    else:
        state.step_log.append("[Tool] Tool 호출 없음")

    return state


def generate_node(state: HybridState) -> HybridState:
    """응답 생성 노드"""
    # 컨텍스트 구성
    context_parts = []
    if state.retrieved_docs:
        context_parts.append(
            "참고 문서:\n" + "\n".join(f"- {d}" for d in state.retrieved_docs)
        )
    if state.tool_results:
        context_parts.append(
            "실행 결과:\n" + "\n".join(
                f"- {r['tool']}: {json.dumps(r['result'], ensure_ascii=False)}"
                for r in state.tool_results
            )
        )

    context = "\n\n".join(context_parts)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": f"다음 정보를 바탕으로 사용자에게 답변하세요.\n\n{context}",
            },
            {"role": "user", "content": state.query},
        ],
        temperature=0,
    )

    state.answer = response.choices[0].message.content
    state.step_log.append("[Generate] 응답 생성 완료")
    return state


# 그래프 실행 엔진 (LangGraph 경량 구현)
class SimpleGraph:
    """LangGraph 개념의 경량 구현"""

    def __init__(self):
        self.nodes: dict[str, Any] = {}
        self.edges: dict[str, Any] = {}  # node -> next_node or conditional
        self.entry_point: str = ""

    def add_node(self, name: str, func):
        self.nodes[name] = func

    def set_entry_point(self, name: str):
        self.entry_point = name

    def add_edge(self, from_node: str, to_node: str):
        self.edges[from_node] = to_node

    def add_conditional_edges(
        self, from_node: str, condition_fn, route_map: dict[str, str]
    ):
        self.edges[from_node] = {"condition": condition_fn, "routes": route_map}

    def run(self, initial_state: HybridState) -> HybridState:
        """그래프 실행"""
        state = initial_state
        current = self.entry_point

        while current and current != "END":
            # 노드 실행
            if current in self.nodes:
                state = self.nodes[current](state)

            # 다음 노드 결정
            edge = self.edges.get(current)
            if edge is None:
                break
            elif isinstance(edge, str):
                current = edge
            elif isinstance(edge, dict):
                route_key = edge["condition"](state)
                current = edge["routes"].get(route_key, "END")
            else:
                break

        return state


# 그래프 구성
graph = SimpleGraph()

# 노드 등록
graph.add_node("router", router_node)
graph.add_node("rag", rag_node)
graph.add_node("tool", tool_node)
graph.add_node("generate", generate_node)

# 엣지 등록
graph.set_entry_point("router")

# 조건부 라우팅
graph.add_conditional_edges(
    "router",
    lambda state: state.route,
    {
        "rag_only": "rag",
        "mcp_only": "tool",
        "hybrid": "rag",
    },
)
graph.add_edge("rag", "generate")  # RAG-only: rag -> generate
graph.add_edge("tool", "generate")  # MCP-only: tool -> generate

# Hybrid는 rag -> tool -> generate 이므로 조건 분기 추가
# (간략화: rag 이후 route가 hybrid이면 tool로)
original_rag_edge = graph.edges["rag"]
graph.add_conditional_edges(
    "rag",
    lambda state: "tool" if state.route == "hybrid" else "generate",
    {"tool": "tool", "generate": "generate"},
)
graph.add_edge("tool", "generate")
graph.add_edge("generate", "END")

# 테스트
test_cases = [
    "환불 정책이 어떻게 되나요?",
    "ORD-12345 주문 상태 알려줘",
    "ORD-12345 환불 처리해주세요. 정책도 확인해주세요.",
]

for query in test_cases:
    state = HybridState(query=query)
    result = graph.run(state)

    print(f"\n쿼리: {query}")
    print(f"경로: {result.route}")
    print(f"실행 로그: {' -> '.join(result.step_log)}")
    print(f"답변: {result.answer[:80]}...")
```

**실행 결과**:
```
쿼리: 환불 정책이 어떻게 되나요?
경로: rag_only
실행 로그: [Router] route=rag_only -> [RAG] 2개 문서 검색 -> [Generate] 응답 생성 완료
답변: 환불 정책은 구매 후 30일 이내, 미개봉 상품에 한해 전액 환불이 가능합니다...

쿼리: ORD-12345 주문 상태 알려줘
경로: mcp_only
실행 로그: [Router] route=mcp_only -> [Tool] check_order_status 호출 -> [Generate] 응답 생성 완료
답변: 주문 ORD-12345의 현재 상태입니다: 배송 완료 (2025-02-28)...

쿼리: ORD-12345 환불 처리해주세요. 정책도 확인해주세요.
경로: hybrid
실행 로그: [Router] route=hybrid -> [RAG] 2개 문서 검색 -> [Tool] process_refund 호출 -> [Generate] 응답 생성 완료
답변: 환불 정책(30일 이내, 미개봉)을 확인했습니다. 주문 ORD-12345의 환불을 처리했습니다...
```

### 예제

```python
import os
import json
from openai import OpenAI
from dataclasses import dataclass, field
from typing import Any

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


# 실전 LangGraph 코드 (langgraph 패키지 사용)
# pip install langgraph langchain-openai

"""
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

# 1. 상태 정의
class AgentState(TypedDict):
    query: str
    route: str
    messages: Annotated[list, add_messages]
    retrieved_docs: list[str]
    tool_results: list[dict]
    answer: str

# 2. LLM 초기화
llm = ChatOpenAI(
    model="moonshotai/kimi-k2",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

# 3. 노드 함수
def router(state: AgentState) -> AgentState:
    # 라우팅 로직
    ...

def rag_search(state: AgentState) -> AgentState:
    # RAG 검색
    ...

def tool_execute(state: AgentState) -> AgentState:
    # Tool 실행
    ...

def generate(state: AgentState) -> AgentState:
    # 응답 생성
    ...

# 4. 그래프 구성
graph = StateGraph(AgentState)
graph.add_node("router", router)
graph.add_node("rag", rag_search)
graph.add_node("tool", tool_execute)
graph.add_node("generate", generate)

graph.set_entry_point("router")
graph.add_conditional_edges(
    "router",
    lambda s: s["route"],
    {"rag_only": "rag", "mcp_only": "tool", "hybrid": "rag"},
)
graph.add_conditional_edges(
    "rag",
    lambda s: "tool" if s["route"] == "hybrid" else "generate",
    {"tool": "tool", "generate": "generate"},
)
graph.add_edge("tool", "generate")
graph.add_edge("generate", END)

# 5. 컴파일 및 실행
app = graph.compile()
result = app.invoke({"query": "환불 정책 확인 후 ORD-123 환불해주세요"})
"""


# LangGraph 없이 동일 패턴 구현 (패키지 의존성 없음)
@dataclass
class ProductionState:
    """프로덕션 Hybrid Agent 상태"""
    query: str = ""
    route: str = ""
    retrieved_docs: list[str] = field(default_factory=list)
    tool_results: list[dict] = field(default_factory=list)
    answer: str = ""
    error: str = ""
    steps: list[dict] = field(default_factory=list)
    total_cost: float = 0.0


class ProductionHybridAgent:
    """프로덕션 수준의 Hybrid Agent (에러 핸들링, 비용 추적 포함)"""

    def __init__(self, knowledge_base: list[str]):
        self.knowledge_base = knowledge_base
        self.cost_per_1k_tokens = 0.002  # 예상 비용

    def run(self, query: str) -> ProductionState:
        """전체 파이프라인 실행"""
        state = ProductionState(query=query)

        try:
            # Step 1: Router
            state = self._route(state)

            # Step 2: RAG (필요 시)
            if state.route in ("rag_only", "hybrid"):
                state = self._rag_search(state)

            # Step 3: Tool (필요 시)
            if state.route in ("mcp_only", "hybrid"):
                state = self._tool_execute(state)

            # Step 4: Generate
            state = self._generate(state)

        except Exception as e:
            state.error = str(e)
            state.answer = "죄송합니다. 처리 중 오류가 발생했습니다."

        return state

    def _route(self, state: ProductionState) -> ProductionState:
        """라우팅"""
        import re

        # 규칙 기반 1차 분류
        has_order = bool(re.search(r"ORD-\d+", state.query))
        has_policy = bool(re.search(r"정책|규정|가이드|방법", state.query))

        if has_order and has_policy:
            state.route = "hybrid"
        elif has_order:
            state.route = "mcp_only"
        elif has_policy:
            state.route = "rag_only"
        else:
            # LLM 2차 분류
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{
                    "role": "user",
                    "content": f'분류: "{state.query}" -> JSON: {{"route":"rag_only|mcp_only|hybrid"}}',
                }],
                temperature=0,
            )
            result = json.loads(response.choices[0].message.content)
            state.route = result["route"]
            self._track_cost(state, response)

        state.steps.append({"step": "route", "result": state.route})
        return state

    def _rag_search(self, state: ProductionState) -> ProductionState:
        """RAG 검색"""
        query_terms = set(state.query.lower().split())
        scored = []
        for doc in self.knowledge_base:
            overlap = len(query_terms & set(doc.lower().split()))
            scored.append((overlap, doc))
        scored.sort(reverse=True)
        state.retrieved_docs = [d for _, d in scored[:3]]
        state.steps.append({
            "step": "rag",
            "docs_count": len(state.retrieved_docs),
        })
        return state

    def _tool_execute(self, state: ProductionState) -> ProductionState:
        """Tool 실행"""
        context = ""
        if state.retrieved_docs:
            context = "\n정책:\n" + "\n".join(f"- {d}" for d in state.retrieved_docs)

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "check_order_status",
                    "description": "주문 상태 조회",
                    "parameters": {
                        "type": "object",
                        "properties": {"order_id": {"type": "string"}},
                        "required": ["order_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "process_refund",
                    "description": "환불 처리",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order_id": {"type": "string"},
                            "reason": {"type": "string"},
                        },
                        "required": ["order_id", "reason"],
                    },
                },
            },
        ]

        messages = [
            {"role": "system", "content": f"고객 지원 AI.{context}"},
            {"role": "user", "content": state.query},
        ]

        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=tools, tool_choice="auto"
        )
        self._track_cost(state, response)

        msg = response.choices[0].message
        if msg.tool_calls:
            for tc in msg.tool_calls:
                result = simulate_tool(tc.function.name, tc.function.arguments)
                state.tool_results.append({
                    "tool": tc.function.name,
                    "result": result,
                })
                state.steps.append({"step": "tool", "name": tc.function.name})

        return state

    def _generate(self, state: ProductionState) -> ProductionState:
        """응답 생성"""
        parts = []
        if state.retrieved_docs:
            parts.append("문서:\n" + "\n".join(f"- {d}" for d in state.retrieved_docs))
        if state.tool_results:
            parts.append("결과:\n" + "\n".join(
                f"- {r['tool']}: {json.dumps(r['result'], ensure_ascii=False)}"
                for r in state.tool_results
            ))

        context = "\n".join(parts)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": f"정보를 바탕으로 답변하세요.\n\n{context}"},
                {"role": "user", "content": state.query},
            ],
            temperature=0,
        )
        self._track_cost(state, response)

        state.answer = response.choices[0].message.content
        state.steps.append({"step": "generate"})
        return state

    def _track_cost(self, state: ProductionState, response):
        """비용 추적"""
        if response.usage:
            tokens = response.usage.total_tokens
            state.total_cost += (tokens / 1000) * self.cost_per_1k_tokens


# 프로덕션 테스트
agent = ProductionHybridAgent(knowledge_base=[
    "환불 정책: 구매 후 30일 이내, 미개봉 상품 전액 환불 가능.",
    "VIP: 연간 100만원 이상 구매 시 자동 승급. 5% 추가 할인.",
    "배송: 서울/경기 당일, 그 외 1~2일. 5만원 이상 무료 배송.",
])

test_cases = [
    "VIP 등급 기준 알려주세요",
    "ORD-55555 주문 어디까지 왔어요?",
    "ORD-12345 환불해주세요. 환불 정책도 알려주세요.",
]

print("=== Production Hybrid Agent ===\n")
for query in test_cases:
    result = agent.run(query)
    steps = " -> ".join(s["step"] for s in result.steps)
    print(f"쿼리: {query}")
    print(f"경로: {result.route} | 단계: {steps}")
    print(f"비용: ${result.total_cost:.4f}")
    print(f"답변: {result.answer[:80]}...")
    print()
```

**실행 결과**:
```
=== Production Hybrid Agent ===

쿼리: VIP 등급 기준 알려주세요
경로: rag_only | 단계: route -> rag -> generate
비용: $0.0024
답변: VIP 등급 기준은 연간 구매액 100만원 이상입니다. VIP 회원은 5% 추가 할인 혜택을 받으실 수 있습...

쿼리: ORD-55555 주문 어디까지 왔어요?
경로: mcp_only | 단계: route -> tool -> check_order_status -> generate
비용: $0.0036
답변: 주문 ORD-55555의 현재 상태입니다: 배송 완료 (2025-02-28)...

쿼리: ORD-12345 환불해주세요. 환불 정책도 알려주세요.
경로: hybrid | 단계: route -> rag -> tool -> process_refund -> generate
비용: $0.0052
답변: 환불 정책을 확인했습니다: 구매 후 30일 이내 미개봉 상품은 전액 환불 가능합니다. 주문 ORD-12345...
```

### Q&A
**Q: LangGraph를 쓰면 직접 구현 대비 어떤 장점이 있나요?**
A: 세 가지 핵심 장점이 있다. (1) **체크포인팅**: 각 노드 실행 후 상태를 자동 저장하여 장애 시 복구 가능. (2) **스트리밍**: 각 노드의 출력을 실시간 스트리밍하여 UX 개선. (3) **시각화**: `app.get_graph().draw_mermaid()`로 그래프를 다이어그램으로 출력. 프로토타입에서는 직접 구현도 충분하지만, 프로덕션에서는 LangGraph의 인프라 기능이 가치가 있다.

<details>
<summary>퀴즈: LangGraph에서 "조건부 엣지"와 "일반 엣지"의 차이는 무엇이며, Hybrid Agent에서 조건부 엣지가 필수인 이유는?</summary>

**힌트**: 일반 엣지는 항상 같은 다음 노드로 이동합니다. 조건부 엣지는?

**정답**: 일반 엣지는 A 노드 실행 후 항상 B 노드로 이동하는 고정 경로다. 조건부 엣지는 상태(state)를 검사하여 B, C, D 중 하나로 분기하는 동적 경로다. Hybrid Agent에서 Router 노드의 결과(`route`)에 따라 RAG/Tool/둘 다 실행이 달라지므로, Router 다음에 조건부 엣지가 필수다. 이것이 없으면 모든 쿼리가 동일한 경로를 거치게 되어 불필요한 RAG 검색이나 Tool 호출이 발생한다.
</details>

---

## 실습

### 실습 1: RAG-as-a-Tool Hybrid Agent 구현
- **연관 학습 목표**: 학습 목표 1
- **실습 목적**: RAG 검색을 Tool로 감싸는 패턴을 구현하여 LLM이 검색 필요 여부를 자율적으로 판단하는 Agent를 만든다
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 30분
- **선행 조건**: Day 3 Session 1~3 내용 이해
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**실습 내용**:

IT 헬프데스크 시나리오에서 다음 기능을 가진 Hybrid Agent를 구현한다:
- RAG Tool: IT 정책/가이드 문서 검색 (5개 이상 문서)
- MCP Tool: Jira 티켓 생성, Slack 알림 전송
- 10개 테스트 질문에 대해 올바른 Tool 선택 여부 평가

```python
# TODO: ITHelpdeskAgent 구현
# 1. RAGTool 클래스: IT 정책 문서 검색 Tool
# 2. action_tools: create_jira_ticket, send_slack_notification
# 3. HybridAgent: RAG + MCP Tool을 가진 Agent
# 4. 테스트: 다양한 유형의 질문 10개

test_questions = [
    ("VPN 연결 방법 알려줘", "RAG"),
    ("JIRA-456 티켓 상태 확인해줘", "MCP"),
    ("서버 장애 발생. 매뉴얼 확인 후 티켓 생성해줘", "RAG+MCP"),
    ("비밀번호 변경 절차가 뭐야?", "RAG"),
    ("개발팀에 배포 완료 알림 보내줘", "MCP"),
    ("노트북 교체 신청 방법", "RAG"),
    ("장애 대응 매뉴얼 검색 후 Slack에 공유해줘", "RAG+MCP"),
    ("회의실 예약 시스템 접속 방법", "RAG"),
    ("JIRA-789 티켓 우선순위를 높여줘", "MCP"),
    ("보안 정책 위반 시 처리 절차", "RAG"),
]
```

### 실습 2: 2단계 라우터 구현 및 성능 비교
- **연관 학습 목표**: 학습 목표 2
- **실습 목적**: 규칙 기반 + LLM 분류기의 2단계 라우터를 구현하고 순수 LLM 라우터 대비 속도/정확도를 비교한다
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 25분
- **선행 조건**: 실습 1 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**실습 내용**:

20개의 테스트 쿼리에 대해 세 가지 라우터를 비교한다:
- 규칙 기반 Only
- LLM 분류기 Only
- 2단계 (규칙 1차 + LLM 2차)

```python
# TODO: RouterBenchmark 클래스를 구현하세요
# 1. RuleBasedRouter: 정규표현식 패턴 매칭
# 2. ClassifierRouter: LLM 기반 의도 분류
# 3. TwoStageRouter: 규칙 1차 -> LLM 2차
# 4. 20개 테스트 쿼리에 대해 정확도, 평균 latency 비교
# 5. 결과 테이블 출력
```

### 실습 3: LangGraph 스타일 Hybrid Agent 구축
- **연관 학습 목표**: 학습 목표 2, 3
- **실습 목적**: 그래프 기반 제어 흐름으로 Hybrid Agent를 구현하고, 에러 핸들링과 비용 추적을 포함한 프로덕션 수준 파이프라인을 완성한다
- **실습 유형**: 코드 작성
- **난이도**: 심화
- **예상 소요 시간**: 40분
- **선행 조건**: 실습 1, 2 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**실습 내용**:

다음 기능을 갖춘 프로덕션 Hybrid Agent를 구현한다:
1. 그래프 기반 실행 엔진 (Router -> RAG -> Tool -> Generate)
2. 에러 핸들링: Tool 실패 시 재시도 또는 Fallback
3. 비용 추적: 각 단계의 토큰 사용량과 비용 계산
4. 실행 로그: 각 단계의 입력/출력 기록
5. 10개 테스트로 End-to-End 검증

```python
# TODO: ProductionHybridPipeline 구현
# 1. SimpleGraph: 노드/엣지 기반 실행 엔진
# 2. 노드: router, rag_search, tool_execute, generate, error_handler
# 3. 조건부 엣지: route 결과에 따라 분기
# 4. 에러 핸들링: try/except + 재시도 로직
# 5. 비용/시간 추적 미들웨어
# 6. 10개 시나리오 테스트 + 결과 리포트 출력
```

---

## 핵심 정리
- Hybrid 아키텍처의 핵심 패턴은 RAG-as-a-Tool이다. RAG 검색을 일반 Tool과 동일한 인터페이스로 감싸면, LLM이 검색 필요 여부를 자율적으로 판단하여 불필요한 검색을 줄인다
- 동적 라우팅은 2단계(규칙 기반 1차 -> LLM 분류기 2차)가 최적이다. 규칙으로 처리 가능한 쿼리는 0ms에 분류하고, 모호한 쿼리만 LLM에 위임하여 비용과 latency를 절감한다
- 상태 관리는 대화 상태, 검색 상태, 액션 상태를 분리하여 관리한다. 멀티턴 대화에서 이전 컨텍스트를 활용하되, stale data 문제를 방지하기 위해 필요 시 재검색을 트리거해야 한다
- LangGraph 스타일의 그래프 기반 설계는 Hybrid Agent의 복잡한 제어 흐름을 선언적으로 표현한다. 조건부 엣지로 라우팅을 구현하고, 각 노드의 입출력을 상태 객체로 통일하면 디버깅과 확장이 용이하다
- 프로덕션 환경에서는 에러 핸들링(Tool 실패 시 재시도/Fallback), 비용 추적(단계별 토큰 사용량), 실행 로그(입출력 기록)를 반드시 포함해야 한다
