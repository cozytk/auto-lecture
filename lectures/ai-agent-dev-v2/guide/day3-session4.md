# Day 3 Session 4 — Hybrid 아키텍처 설계

> **목표**: MCP 중심 vs RAG 중심 구조 기준, Retrieval 이후 Tool 호출 패턴, Trade-off 분석
> **시간**: 2시간 | **대상**: AI 개발자, 데이터 엔지니어, 기술 리더

---

## 1. 왜 중요한가

MCP(Tool Calling)만으로는 대규모 지식을 실시간 처리할 수 없다.
RAG만으로는 동적 행동(API 호출, 계산)을 수행할 수 없다.
→ **둘을 조합한 Hybrid 아키텍처가 실무 표준이 되고 있다**

어떤 구조를 선택하느냐는 비용, 정확도, 확장성에 직접 영향을 준다.
이 세션에서는 판단 기준과 구체적인 패턴을 다룬다.

---

## 2. 핵심 원리

### 2.1 MCP 중심 vs RAG 중심 구조 기준

**MCP(Tool Calling) 중심의 특성**

```
강점:
- 실시간 데이터 접근 (현재 날씨, 주가, DB 쿼리)
- 부작용 있는 작업 수행 (파일 저장, 이메일 발송)
- 계산·변환 수행 (코드 실행, 수식 계산)
- 외부 시스템과 상호작용

약점:
- API 호출 지연 (100ms~수초)
- 호출 비용 (API 요금, Rate Limit)
- 복잡한 오류 처리 필요
- 대규모 지식 처리 어려움
```

**RAG 중심의 특성**

```
강점:
- 대용량 지식 베이스 검색 (수백만 문서)
- 정적 지식 기반 QA
- 빠른 컨텍스트 주입 (벡터 검색 ~10ms)
- 추가 API 비용 없음

약점:
- 실시간 데이터 불가 (인덱싱 시점 기준)
- 행동(Action) 수행 불가
- Chunking·임베딩 품질에 의존
- 문서 업데이트 시 재인덱싱 필요
```

**구조 선택 기준표**

| 요구사항 | MCP 중심 | RAG 중심 | Hybrid |
|----------|----------|----------|--------|
| 실시간 데이터 | ✅ | ❌ | ✅ |
| 대용량 지식 QA | ❌ | ✅ | ✅ |
| 부작용 있는 작업 | ✅ | ❌ | ✅ |
| 낮은 지연 시간 | 중간 | ✅ | 중간 |
| 낮은 비용 | ❌ | ✅ | 중간 |
| 복잡한 추론 | 중간 | 중간 | ✅ |

**결론**

> 단순 정보 조회 → RAG 중심
> 동적 행동 필요 → MCP 중심
> 지식 기반 + 행동 = **Hybrid** (대부분의 프로덕션 시스템)

---

### 2.2 Retrieval 이후 Tool 호출 패턴

**패턴 1: RAG-then-Tool (검색 후 행동)**

```
사용자: "삼성 주식을 살까요? 현재 가격과 최근 뉴스를 참고해서 알려줘"

1단계: RAG → 삼성 투자 분석 문서 검색
2단계: Tool → 현재 주가 조회 (get_stock_price)
3단계: Tool → 최근 뉴스 조회 (get_news)
4단계: LLM → 문서 + 실시간 데이터 종합 분석
```

```python
async def rag_then_tool_pipeline(query: str) -> str:
    # 1. RAG: 관련 지식 검색
    retrieved_docs = rag_store.search(query, k=5)
    knowledge_context = format_docs(retrieved_docs)

    # 2. LLM에게 Tool 사용 여부 판단 위임
    response = await client.messages.create(
        model="claude-opus-4-5",
        tools=available_tools,
        system=f"다음 지식을 참조하세요:\n{knowledge_context}",
        messages=[{"role": "user", "content": query}]
    )

    # 3. Tool 호출 처리
    while response.stop_reason == "tool_use":
        tool_results = await execute_tools(response)
        response = await continue_with_results(response, tool_results)

    return response.content[0].text
```

**패턴 2: Tool-then-RAG (행동 후 검색)**

```
사용자: "방금 발생한 오류 코드 E2024를 분석해줘"

1단계: Tool → 현재 시스템 로그 조회 (get_system_logs)
2단계: RAG → 오류 코드 매뉴얼 검색
3단계: LLM → 실시간 로그 + 매뉴얼 종합
```

```python
async def tool_then_rag_pipeline(query: str) -> str:
    # 1. Tool로 실시간 데이터 수집
    log_data = await get_system_logs(hours=1)
    error_codes = extract_error_codes(log_data)

    # 2. 오류 코드 기반 RAG 검색
    all_docs = []
    for code in error_codes:
        docs = rag_store.search(f"오류 코드 {code}", k=3)
        all_docs.extend(docs)

    # 3. 종합 분석
    context = format_docs(all_docs)
    analysis = await llm_analyze(query, log_data, context)
    return analysis
```

**패턴 3: Parallel Hybrid (병렬 처리)**

```
사용자: "서울 날씨, 회사 정책, 오늘 일정을 종합해서 알려줘"

동시 실행:
  - Tool: 현재 날씨 API 호출
  - RAG: 회사 정책 문서 검색
  - Tool: 캘린더 API 호출

→ 모든 결과를 LLM에 전달하여 종합
```

```python
async def parallel_hybrid(query: str) -> str:
    # 병렬 실행: Tool + RAG 동시
    weather_task = get_current_weather("Seoul")
    policy_task = asyncio.create_task(
        asyncio.to_thread(rag_store.search, "회사 정책", 3)
    )
    calendar_task = get_calendar_events()

    weather, policy_docs, calendar = await asyncio.gather(
        weather_task, policy_task, calendar_task,
        return_exceptions=True
    )

    # 모든 컨텍스트 종합
    context = build_combined_context(weather, policy_docs, calendar)
    return await llm_synthesize(query, context)
```

---

### 2.3 정확도 · 비용 · 확장성 Trade-off

**정확도 관점**

```
낮음 ←────────────────────────────→ 높음

LLM Only → RAG Only → MCP Only → Hybrid
                                    ↑
                               최고 정확도
                          (실시간 + 지식 기반)
```

**비용 관점**

```
낮음 ←────────────────────────────→ 높음

RAG Only → LLM Only → MCP Only → Hybrid
   ↑                                 ↑
 최저 비용                        최고 비용
(벡터 검색만)              (API 호출 + 임베딩 + LLM)
```

**확장성 관점**

| 구조 | 문서 1M개 | 동시 사용자 | 실시간 갱신 |
|------|-----------|------------|------------|
| RAG Only | ✅ 가능 | ✅ 가능 | ❌ 재인덱싱 |
| MCP Only | N/A | 중간 (API 한도) | ✅ 가능 |
| Hybrid | ✅ 가능 | 중간 | 부분 가능 |

**의사결정 프레임워크**

```python
def choose_architecture(requirements: dict) -> str:
    needs_realtime = requirements.get("realtime_data", False)
    needs_action = requirements.get("side_effects", False)
    large_knowledge = requirements.get("doc_count", 0) > 10000
    budget_sensitive = requirements.get("low_cost", False)

    if needs_realtime and large_knowledge:
        return "Hybrid"
    elif needs_action and not large_knowledge:
        return "MCP-centric"
    elif large_knowledge and not needs_realtime:
        return "RAG-centric"
    elif budget_sensitive:
        return "RAG-centric"
    else:
        return "Hybrid"  # 기본값: Hybrid
```

---

## 3. 실무 의미

**아키텍처 선택 체크리스트**

```
질문 1: 실시간 데이터가 필요한가?
  → 예: MCP 또는 Hybrid
  → 아니오: RAG 또는 Hybrid

질문 2: 부작용 있는 작업(저장, 발송)이 필요한가?
  → 예: MCP 또는 Hybrid

질문 3: 10,000개 이상의 문서를 참조해야 하는가?
  → 예: RAG 또는 Hybrid

질문 4: 응답 지연이 3초 이내여야 하는가?
  → 예: RAG 중심 (벡터 검색이 빠름)
  → 아니오: Hybrid 가능

질문 5: API 호출 비용을 최소화해야 하는가?
  → 예: RAG 중심
```

**Hybrid 시스템 설계 원칙**

```
원칙 1: RAG를 먼저 시도한다 (빠르고 저렴)
원칙 2: RAG 신뢰도가 낮을 때 Tool 호출
원칙 3: 실시간 데이터는 항상 Tool 사용
원칙 4: 병렬 처리로 지연 최소화
원칙 5: 결과 캐싱으로 중복 호출 방지
```

---

## 4. 비교

### 아키텍처 종합 비교

| 항목 | MCP 중심 | RAG 중심 | Hybrid |
|------|----------|----------|--------|
| 구현 복잡도 | 중간 | 중간 | 높음 |
| 응답 지연 | 중간 (API 의존) | 낮음 | 중간~높음 |
| 비용 | 높음 | 낮음 | 중간 |
| 정확도 | 높음 (실시간) | 높음 (지식) | 최고 |
| 확장성 | API 한도 의존 | 높음 | 높음 |
| 유지보수 | 중간 | 중간 | 복잡 |

### Hybrid 패턴 비교

| 패턴 | 지연 | 적합한 상황 |
|------|------|-------------|
| RAG-then-Tool | 중간 | 지식 기반 후 행동 |
| Tool-then-RAG | 중간 | 실시간 데이터 후 분석 |
| Parallel Hybrid | 낮음 | 독립적인 다중 소스 |
| Conditional | 가변 | 결과에 따른 분기 |

---

## 5. 주의사항

**Hybrid 복잡도 관리**

> Hybrid 시스템은 RAG와 MCP 각각의 실패 모드를 모두 처리해야 한다.
> 초기 구현은 단순하게 시작하고, 필요에 따라 복잡도를 높여야 한다.
> "Hybrid = 복잡하지만 강력하다"는 의미이지, 항상 최선이 아니다.

**비용 계산 미스**

> Hybrid 시스템은 임베딩 + 벡터 DB + LLM + API 비용이 모두 발생한다.
> 운영 전에 쿼리 수 × 각 비용을 계산하여 예산을 수립해야 한다.
> 캐싱으로 반복 호출 비용을 줄이는 것이 필수다.

**Retrieval 결과 없을 때 Tool 자동 전환**

> RAG 결과가 없거나 신뢰도가 낮을 때 자동으로 Tool을 호출하는 로직이 필요하다.
> 이 전환 로직이 없으면 답변 품질이 불안정해진다.

**비동기 처리 일관성**

> Parallel Hybrid에서 Tool과 RAG 결과가 서로 다른 시점의 데이터를 반환할 수 있다.
> 특히 실시간 데이터와 캐시된 RAG 결과 간의 시점 불일치를 명시적으로 처리해야 한다.

---

## 6. 코드 예제

### 완성된 Hybrid Agent

```python
import asyncio
import anthropic
from dataclasses import dataclass
from typing import Optional

client = anthropic.Anthropic()


@dataclass
class HybridContext:
    rag_docs: list[dict]
    tool_results: dict[str, any]
    confidence: float


# ── Tool 정의 ──────────────────────────────────────
tools = [
    {
        "name": "get_realtime_data",
        "description": (
            "실시간 데이터가 필요할 때 호출. 날씨, 주가, 최신 뉴스 등. "
            "정적 지식(회사 정책, 제품 매뉴얼 등)은 RAG를 사용."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "data_type": {
                    "type": "string",
                    "enum": ["weather", "stock", "news"],
                    "description": "조회할 데이터 유형"
                },
                "query": {
                    "type": "string",
                    "description": "구체적인 조회 내용"
                }
            },
            "required": ["data_type", "query"]
        }
    },
    {
        "name": "execute_action",
        "description": "이메일 발송, 파일 저장, DB 업데이트 등 부작용 있는 작업 수행.",
        "input_schema": {
            "type": "object",
            "properties": {
                "action_type": {
                    "type": "string",
                    "enum": ["send_email", "save_file", "update_db"]
                },
                "params": {
                    "type": "object",
                    "description": "액션 파라미터"
                }
            },
            "required": ["action_type", "params"]
        }
    }
]


# ── RAG 컴포넌트 ───────────────────────────────────
class RAGComponent:
    def __init__(self, vector_store):
        self.store = vector_store

    async def retrieve(self, query: str, threshold: float = 0.65) -> tuple[list[dict], float]:
        docs = self.store.search(query, k=5, threshold=threshold)
        max_score = max((d["score"] for d in docs), default=0.0)
        return docs, max_score

    def format_context(self, docs: list[dict]) -> str:
        if not docs:
            return ""
        return "\n\n".join([
            f"[지식 {i+1}] (관련도: {d['score']:.2f})\n{d['content']}"
            for i, d in enumerate(docs)
        ])


# ── Hybrid Agent ───────────────────────────────────
class HybridAgent:
    def __init__(self, rag: RAGComponent, rag_threshold: float = 0.70):
        self.rag = rag
        self.rag_threshold = rag_threshold

    async def run(self, query: str) -> dict:
        # 1. RAG 검색 (빠르고 저렴한 경로 먼저)
        rag_docs, rag_score = await self.rag.retrieve(query)
        rag_context = self.rag.format_context(rag_docs)

        # 2. RAG 신뢰도에 따른 System Prompt 조정
        if rag_score >= self.rag_threshold:
            system = (
                f"다음 지식을 기반으로 답변하세요. "
                f"실시간 데이터가 추가로 필요하면 Tool을 사용하세요.\n\n"
                f"[지식 베이스]\n{rag_context}"
            )
        else:
            system = (
                "지식 베이스에서 관련 정보를 찾지 못했습니다. "
                "실시간 데이터나 일반 지식으로 답변하세요."
            )

        # 3. LLM + Tool 루프
        messages = [{"role": "user", "content": query}]
        tool_results = {}

        while True:
            response = await asyncio.to_thread(
                client.messages.create,
                model="claude-opus-4-5",
                max_tokens=4096,
                system=system,
                tools=tools,
                messages=messages
            )

            if response.stop_reason == "end_turn":
                break

            # Tool 호출 처리
            tool_calls = [b for b in response.content if b.type == "tool_use"]
            if not tool_calls:
                break

            tool_result_blocks = []
            for tool_call in tool_calls:
                result = await self._execute_tool(tool_call.name, tool_call.input)
                tool_results[tool_call.name] = result
                tool_result_blocks.append({
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": str(result)
                })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_result_blocks})

        return {
            "answer": response.content[-1].text if response.content else "",
            "rag_score": rag_score,
            "rag_docs_used": len(rag_docs),
            "tools_called": list(tool_results.keys()),
            "architecture": self._determine_architecture(rag_score, tool_results)
        }

    def _determine_architecture(self, rag_score: float, tool_results: dict) -> str:
        used_rag = rag_score >= self.rag_threshold
        used_tools = bool(tool_results)

        if used_rag and used_tools:
            return "Hybrid"
        elif used_rag:
            return "RAG-only"
        elif used_tools:
            return "Tool-only"
        else:
            return "LLM-only"

    async def _execute_tool(self, name: str, params: dict) -> dict:
        # 실제 구현에서는 외부 API 호출
        if name == "get_realtime_data":
            return {"status": "success", "data": f"Mock {params['data_type']} data"}
        elif name == "execute_action":
            return {"status": "success", "message": f"Action {params['action_type']} executed"}
        return {"error": f"Unknown tool: {name}"}


# ── 사용 예시 ──────────────────────────────────────
async def main():
    # 실제 구현에서는 vector_store를 초기화
    vector_store = None  # SimpleVectorStore()
    rag = RAGComponent(vector_store)
    agent = HybridAgent(rag, rag_threshold=0.70)

    queries = [
        "서울 현재 날씨는?",                    # Tool 중심
        "회사 출장 정책이 어떻게 되나요?",        # RAG 중심
        "삼성 주가와 투자 전략을 알려줘",          # Hybrid
    ]

    for query in queries:
        print(f"\n질문: {query}")
        result = await agent.run(query)
        print(f"아키텍처: {result['architecture']}")
        print(f"RAG 신뢰도: {result['rag_score']:.2f}")
        print(f"사용된 Tool: {result['tools_called']}")
        print(f"답변: {result['answer'][:100]}...")
```

---

## Q&A

**Q1. Hybrid 시스템의 가장 큰 도전 과제는 무엇인가요?**

> 복잡도 관리와 비용 예측이다.
> RAG, MCP, LLM 각각의 실패 모드를 모두 처리해야 한다.
> 비용은 세 구성요소의 합이므로 사전에 철저히 계산해야 한다.
> 단순하게 시작해서 필요한 복잡도만 추가하는 것을 권장한다.

**Q2. RAG 신뢰도 임계값(Threshold)을 어떻게 결정하나요?**

> 도메인별로 다르지만 일반적으로 0.65~0.75가 시작점이다.
> A/B 테스트로 임계값별 사용자 만족도를 측정한다.
> 임계값이 낮으면 → Tool 호출 감소 (비용 절감) but 부정확한 RAG 결과 위험
> 임계값이 높으면 → Tool 호출 증가 (비용 상승) but RAG 결과 신뢰도 높음

**Q3. Hybrid 시스템을 모니터링할 때 어떤 지표가 중요한가요?**

> 1) 아키텍처 사용 비율: RAG-only / Tool-only / Hybrid 각각의 비율
> 2) RAG 신뢰도 분포: 낮은 신뢰도 쿼리의 비중
> 3) Tool 호출 성공률: 실패율이 높으면 Tool 재설계 필요
> 4) 전체 응답 지연: P50, P95, P99
> 5) 쿼리당 비용: RAG + Tool + LLM 비용 합계

---

## 퀴즈

**Q1. "회사 5년치 계약서에서 특정 조항을 찾아줘"에 가장 적합한 아키텍처는?**

> a) MCP 중심 (Tool Calling)
> b) RAG 중심 (벡터 검색)
> c) LLM Only (프롬프트에 전체 삽입)
> d) Hybrid (RAG + Tool)

<details>
<summary>힌트 및 정답</summary>

**힌트**: 5년치 계약서는 몇 MB나 될까? LLM Context Window에 들어갈까?

**정답**: b) RAG 중심 (벡터 검색)

대용량 정적 문서 검색은 RAG가 최적이다. 실시간 데이터나 행동이 필요 없으므로 MCP는 불필요하다. LLM Context에 전체 삽입은 불가능하다.

</details>

---

**Q2. "현재 서버 상태를 확인하고 이상 시 알림 이메일을 발송해줘"에 필요한 아키텍처는?**

> a) RAG 중심
> b) LLM Only
> c) MCP 중심 (Tool Calling)
> d) RAG + LLM

<details>
<summary>힌트 및 정답</summary>

**힌트**: "현재 서버 상태"와 "이메일 발송"은 어떤 특성이 있나?

**정답**: c) MCP 중심 (Tool Calling)

실시간 데이터 조회(서버 상태)와 부작용 있는 행동(이메일 발송) 모두 Tool이 필요하다. 정적 지식 검색이 필요 없으므로 RAG는 불필요하다.

</details>

---

**Q3. Parallel Hybrid 패턴의 핵심 장점은?**

> a) 코드가 가장 단순하다
> b) Tool과 RAG를 동시에 실행하여 지연 시간을 줄인다
> c) API 비용이 가장 저렴하다
> d) 실패 처리가 가장 쉽다

<details>
<summary>힌트 및 정답</summary>

**힌트**: 3개의 API를 순차 실행하면 3초, 동시 실행하면?

**정답**: b) Tool과 RAG를 동시에 실행하여 지연 시간을 줄인다

독립적인 Tool 호출과 RAG 검색을 병렬로 실행하면 전체 지연이 가장 느린 단일 작업 시간으로 줄어든다. 예: 각각 1초씩 걸리면 순차 3초 → 병렬 1초.

</details>

---

**Q4. Hybrid 시스템에서 RAG 신뢰도가 낮을 때 취해야 할 행동은?**

> a) 즉시 오류 반환
> b) RAG 결과를 그대로 사용
> c) Tool 호출로 전환하거나 LLM 일반 지식으로 폴백
> d) 사용자에게 질문을 다시 입력하도록 요청

<details>
<summary>힌트 및 정답</summary>

**힌트**: 신뢰도가 낮다는 것은 "관련 문서를 찾지 못했다"는 의미다.

**정답**: c) Tool 호출로 전환하거나 LLM 일반 지식으로 폴백

RAG가 실패했을 때 시스템이 자동으로 다른 경로를 시도해야 한다. 오류를 바로 반환하거나 신뢰도 낮은 RAG 결과를 그대로 사용하면 품질이 떨어진다.

</details>

---

**Q5. Hybrid 시스템의 비용을 가장 효과적으로 줄이는 방법은?**

> a) LLM 모델을 더 비싼 것으로 교체
> b) Tool 수를 늘린다
> c) RAG 결과와 Tool 결과를 적극적으로 캐싱
> d) 벡터 DB를 비활성화

<details>
<summary>힌트 및 정답</summary>

**힌트**: 동일한 질문이 하루에 100번 반복된다면, 매번 API를 호출할 필요가 있을까?

**정답**: c) RAG 결과와 Tool 결과를 적극적으로 캐싱

반복 쿼리에 대해 캐싱을 적용하면 임베딩 + 벡터 검색 + API 호출 비용을 모두 절감할 수 있다. 특히 날씨처럼 짧은 간격으로 동일 데이터를 요청하는 경우 효과가 크다.

</details>

---

## 실습 명세

### 실습 제목: Hybrid 구조 아키텍처 설계 및 구현

**I DO (시연, 20분)**

강사가 직접 시연한다:
1. 동일 쿼리를 RAG-only / MCP-only / Hybrid로 각각 처리
2. 각 방식의 응답 시간, 비용, 정확도 비교
3. RAG 신뢰도에 따른 자동 Tool 전환 동작 확인
4. Parallel Hybrid로 지연 시간 단축 시연

**WE DO (함께, 40분)**

학생과 함께 단계별 구현:
1. HybridAgent 클래스 기본 구조 구현
2. RAG 신뢰도 임계값 설정 및 분기 로직 구현
3. Tool + RAG 병렬 실행 구현
4. 아키텍처 사용 비율 로깅 추가

**YOU DO (독립, 45분)**

- 3가지 유형의 쿼리 세트 설계 (RAG 중심 / Tool 중심 / Hybrid)
- HybridAgent 구현 및 각 쿼리 유형별 실행
- 응답 시간, 비용, 정확도를 기록하는 벤치마크 스크립트 작성
- 아키텍처 선택 기준표 작성 (직접 경험한 Trade-off 기반)
- `solution/` 폴더에 정답 코드 및 벤치마크 결과 예시 제공

---

## Day 3 마무리

### 오늘 배운 핵심 내용

```
Session 1: MCP Tool 설계 품질이 Agent 신뢰도를 결정한다
Session 2: API 연동은 비동기 + 검증 + 보안이 기본이다
Session 3: RAG는 Chunking → Embedding → Retrieval → Guardrail 4단계다
Session 4: 대부분의 프로덕션 시스템은 Hybrid 아키텍처가 최적이다
```

### 내일(Day 4) 예고

- Agent 평가 프레임워크 설계
- 프로덕션 모니터링 및 관찰 가능성
- Agent 성능 최적화 전략
- 비용 최적화 실전 기법
