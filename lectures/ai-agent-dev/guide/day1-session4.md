# Day 1 - Session 4: MCP · RAG · Hybrid 구조 판단

**시간**: 2시간 | **대상**: AI 개발자, 데이터 엔지니어, 기술 리더

---

## 1. 왜 중요한가

### 구조 선택이 시스템 한계를 결정한다

MCP, RAG, Hybrid — 세 구조는 각기 다른 문제를 해결한다.
잘못된 구조를 선택하면 기능을 추가할수록 복잡도만 높아진다.
**초기 설계 단계에서 올바른 구조를 선택해야 한다.**

> 나중에 RAG에서 Agent로, Agent에서 Hybrid로 마이그레이션하는 것은
> 처음부터 올바르게 설계하는 것보다 5-10배 더 비싸다.

**이 세션에서 배우는 것**:
- MCP(Function Calling) Tool 설계 기준
- RAG 구조 (Chunking / Embedding / Retrieval)
- Tool 중심 vs RAG 중심 구조 비교
- Hybrid 설계 시 정확도·비용·확장성 고려

---

## 2. 핵심 원리

### 2-1. MCP(Function Calling) Tool 설계

#### MCP란?

MCP(Model Context Protocol)는 LLM이 외부 기능(Tool)을 호출하는 표준 방식이다.
LLM이 직접 코드를 실행하는 것이 아니라, **"이 Tool을 이 인자로 호출하라"는 명령을 생성**하고 실제 실행은 시스템이 담당한다.

```
[사용자 요청] → [LLM] → [Tool 호출 명령 생성]
                                    ↓
                              [실제 Tool 실행]
                                    ↓
                              [결과를 LLM에 전달]
                                    ↓
                           [최종 응답 생성]
```

#### 좋은 Tool 설계 기준

**① 단일 책임**: 하나의 Tool은 하나의 명확한 기능만 수행

```python
# 나쁜 예시 - 너무 많은 책임
def manage_data(action: str, data: dict) -> dict:
    """데이터 관리: 생성/조회/수정/삭제"""
    ...

# 좋은 예시 - 명확한 단일 기능
def get_user_by_id(user_id: str) -> dict:
    """사용자 ID로 정보 조회"""
    ...

def update_user_email(user_id: str, new_email: str) -> dict:
    """사용자 이메일 변경"""
    ...
```

**② 명확한 Description**: LLM이 언제 이 Tool을 사용해야 할지 이해할 수 있어야 한다

```python
tools = [{
    "name": "search_jira_issues",
    "description": """Jira에서 이슈를 검색한다.
특정 프로젝트, 상태, 담당자 조건으로 필터링 가능하다.
이슈 목록이나 특정 이슈 상태를 확인할 때 사용한다.
날짜 범위로 특정 기간의 이슈만 조회할 수 있다.""",
    "input_schema": {
        "type": "object",
        "properties": {
            "project": {
                "type": "string",
                "description": "Jira 프로젝트 키 (예: PROJ, DEV)"
            },
            "status": {
                "type": "string",
                "enum": ["open", "in_progress", "done", "all"],
                "description": "이슈 상태 필터"
            },
            "assignee": {
                "type": "string",
                "description": "담당자 사용자명 (선택사항)"
            },
            "days_back": {
                "type": "integer",
                "description": "최근 N일 이내 이슈만 조회 (기본값: 7)"
            }
        },
        "required": ["project"]
    }
}]
```

**③ 적절한 에러 응답**: Tool이 실패했을 때 LLM이 이해할 수 있는 에러 메시지

```python
def search_jira_issues(project: str, status: str = "all", ...) -> dict:
    try:
        issues = jira_client.search(project=project, status=status)
        return {"success": True, "issues": issues, "count": len(issues)}
    except JiraConnectionError:
        return {"success": False, "error": "Jira 서버에 연결할 수 없습니다. 잠시 후 다시 시도하세요."}
    except ProjectNotFoundError:
        return {"success": False, "error": f"프로젝트 '{project}'를 찾을 수 없습니다. 프로젝트 키를 확인하세요."}
```

---

### 2-2. RAG 구조 (Chunking / Embedding / Retrieval)

#### RAG의 전체 흐름

```
[문서 수집]
    ↓
[청킹 (Chunking)] ── 문서를 적절한 크기로 분할
    ↓
[임베딩 (Embedding)] ── 텍스트 → 벡터 변환
    ↓
[벡터 DB 저장]

─── 사용 시 ───

[사용자 질문]
    ↓
[질문 임베딩]
    ↓
[유사도 검색 (Retrieval)] ── 관련 청크 N개 추출
    ↓
[Context 구성] ── 질문 + 검색된 청크
    ↓
[LLM 답변 생성]
```

#### 청킹 전략

| 전략 | 방법 | 적합 문서 유형 | 장단점 |
|------|------|----------------|--------|
| 고정 크기 | N 토큰마다 분할 | 균일한 텍스트 | 단순하지만 문장 끊길 수 있음 |
| 문장 단위 | 문장 경계로 분할 | 일반 문서 | 의미 보존, 크기 불균일 |
| 단락 단위 | 빈 줄 기준 분할 | 구조화된 문서 | 의미 단위 보존 |
| 계층적 | 섹션 > 단락 > 문장 | 긴 기술 문서 | 정확하지만 복잡 |
| 의미 기반 | 의미 변화점 기준 | 모든 문서 | 가장 정확, 비용 높음 |

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 실무에서 많이 사용하는 재귀적 분할
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # 목표 청크 크기 (토큰)
    chunk_overlap=50,      # 청크 간 겹치는 토큰 수 (문맥 연결)
    separators=["\n\n", "\n", ".", " "],  # 분할 우선순위
)

chunks = splitter.split_text(document_text)
print(f"총 {len(chunks)}개 청크 생성")
```

#### 임베딩과 검색

```python
import anthropic
import numpy as np

client = anthropic.Anthropic()

def embed_text(text: str) -> list[float]:
    """텍스트를 임베딩 벡터로 변환"""
    # 실무에서는 Voyage AI, OpenAI Embeddings 등 사용
    # 여기서는 개념 설명용 의사코드
    response = embedding_client.embed(text)
    return response.embedding

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """두 벡터의 코사인 유사도 계산"""
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query: str, chunks: list[str], top_k: int = 3) -> list[str]:
    """질문과 가장 관련 있는 청크 top_k개 반환"""
    query_embedding = embed_text(query)
    chunk_embeddings = [embed_text(chunk) for chunk in chunks]

    similarities = [
        cosine_similarity(query_embedding, chunk_emb)
        for chunk_emb in chunk_embeddings
    ]

    # 유사도 높은 순서로 정렬하여 top_k 반환
    ranked = sorted(
        zip(chunks, similarities),
        key=lambda x: x[1],
        reverse=True
    )
    return [chunk for chunk, _ in ranked[:top_k]]

def rag_answer(query: str, chunks: list[str]) -> str:
    """RAG 기반 답변 생성"""
    relevant_chunks = retrieve(query, chunks, top_k=3)
    context = "\n\n---\n\n".join(relevant_chunks)

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        system=f"""다음 문서 내용을 바탕으로 질문에 답변하라.
문서에 없는 내용은 "제공된 문서에 해당 정보가 없습니다"라고 답하라.

문서:
{context}""",
        messages=[{"role": "user", "content": query}]
    )
    return response.content[0].text
```

---

### 2-3. Tool 중심 vs RAG 중심 구조 비교

#### Tool 중심 (MCP Agent)

```
[사용자 요청]
    ↓
[LLM: 어떤 Tool을 써야 하나 판단]
    ↓
[Tool 실행 (API, DB, 계산 등)]
    ↓
[결과를 LLM에 전달]
    ↓
[LLM: 최종 답변 생성]
```

**적합 상황**:
- 실시간 데이터 필요 (주가, 날씨, DB 현황)
- 외부 시스템 조작 필요 (이슈 생성, 이메일 발송)
- 계산·변환 작업 필요
- 데이터가 자주 변경됨

**한계**:
- Tool 수가 많아지면 LLM이 올바른 Tool 선택 어려움
- 비정형 지식 검색에 불리
- API 의존성이 높아 외부 서비스 장애에 취약

---

#### RAG 중심

```
[사용자 질문]
    ↓
[질문 임베딩]
    ↓
[벡터 DB 유사도 검색]
    ↓
[관련 문서 청크 추출]
    ↓
[LLM: 문서 기반 답변 생성]
```

**적합 상황**:
- 사내 문서, 매뉴얼, 기술 문서 기반 Q&A
- 지식 베이스가 크고 정적임 (잘 변하지 않음)
- 근거 있는 답변이 중요
- 외부 시스템 조작 불필요

**한계**:
- 실시간 데이터 미지원
- 검색 품질에 전적으로 의존
- 복잡한 다단계 추론 어려움

---

### 2-4. Hybrid 설계

#### Hybrid 구조란?

RAG와 Tool을 **함께 사용**하는 구조다.
Agent가 Tool의 일부로 RAG를 사용하거나, RAG가 Tool로 검색을 보강한다.

```
[사용자 요청]
    ↓
[LLM: 전략 판단]
    ↙           ↘
[RAG 검색]    [외부 Tool 호출]
    ↘           ↙
[결과 통합]
    ↓
[LLM: 최종 답변]
```

#### Hybrid 설계 결정 기준

| 기준 | RAG 비중 높임 | Tool 비중 높임 |
|------|---------------|----------------|
| 데이터 변경 빈도 | 낮음 (문서 중심) | 높음 (실시간) |
| 정확도 요구 | 근거 문서 필요 | 최신 데이터 필요 |
| 비용 | 임베딩 비용 | API 호출 비용 |
| 응답 속도 | 상대적으로 빠름 | API 지연 있음 |

#### Hybrid 구현 예시

```python
import anthropic
import json

client = anthropic.Anthropic()

# Tool 정의: RAG 검색도 Tool로 정의
tools = [
    {
        "name": "search_docs",
        "description": "사내 기술 문서에서 관련 내용을 검색한다. 정책, 가이드라인, 과거 사례 조회에 사용한다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "검색할 내용"},
                "top_k": {"type": "integer", "description": "반환할 결과 수 (기본: 3)"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_realtime_metrics",
        "description": "실시간 시스템 지표를 조회한다. 현재 서버 상태, 트래픽, 에러율 조회에 사용한다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "metric_type": {
                    "type": "string",
                    "enum": ["cpu", "memory", "error_rate", "traffic"]
                },
                "duration_minutes": {"type": "integer"}
            },
            "required": ["metric_type"]
        }
    }
]

def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Tool 실행 디스패처"""
    if tool_name == "search_docs":
        # RAG 검색 실행
        results = rag_search(tool_input["query"], tool_input.get("top_k", 3))
        return json.dumps({"results": results}, ensure_ascii=False)
    elif tool_name == "get_realtime_metrics":
        # 실시간 API 호출
        metrics = metrics_api.get(
            tool_input["metric_type"],
            tool_input.get("duration_minutes", 10)
        )
        return json.dumps({"metrics": metrics}, ensure_ascii=False)
    return json.dumps({"error": f"Unknown tool: {tool_name}"})

def hybrid_agent(user_query: str) -> str:
    """Hybrid Agent: RAG + Tool Use"""
    messages = [{"role": "user", "content": user_query}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            # 최종 텍스트 응답 반환
            return response.content[0].text

        if response.stop_reason == "tool_use":
            # Tool 호출 처리
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            # 대화 이력에 추가
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
```

---

## 3. 실무 의미

### 구조 선택이 팀 역량과 맞아야 한다

**Tool 중심 (MCP Agent)** 선택 시:
- 통합할 API 목록 미리 파악
- API 인증, 권한 관리 설계 필요
- API 실패에 대한 fallback 전략 필수

**RAG 중심** 선택 시:
- 문서 수집·정제 파이프라인 구축 필요
- 청킹 전략과 임베딩 모델 선택이 품질 결정
- 문서 업데이트 주기와 재임베딩 전략 설계

**Hybrid** 선택 시:
- 두 구조의 복잡도 합산
- 언제 RAG를, 언제 Tool을 쓸지 명확한 기준 필요
- 비용이 가장 높음 → 충분한 이유가 있어야 함

---

## 4. 비교

### 세 구조 종합 비교

| 항목 | MCP (Tool 중심) | RAG 중심 | Hybrid |
|------|-----------------|----------|--------|
| 실시간 데이터 | 지원 | 미지원 | 지원 |
| 지식 기반 Q&A | 제한적 | 강함 | 강함 |
| 외부 시스템 조작 | 강함 | 미지원 | 강함 |
| 구현 복잡도 | 중간 | 중간 | 높음 |
| 운영 비용 | API 비용 | 임베딩 비용 | 높음 |
| 확장성 | Tool 추가로 확장 | 문서 추가로 확장 | 복합 |
| 정확도 | Tool 정확도 의존 | 검색 품질 의존 | 높은 편 |

---

## 5. 주의사항

### 구조 선택 실수

**① Hybrid를 기본 선택으로 삼는 것**
- Hybrid는 복잡하고 비싸다
- RAG나 Tool 단독으로 해결되는지 먼저 확인하라

**② Tool 수를 과도하게 늘리는 것**
- Tool이 많을수록 LLM의 선택 정확도 저하
- 15개 이상의 Tool은 성능 문제를 일으킨다
- 관련 Tool을 그룹화하거나 서브 에이전트로 분리하라

**③ 청킹 크기를 기본값으로 방치하는 것**
- 문서 유형에 따라 최적 청킹 크기가 다르다
- 너무 크면: 검색 정밀도 저하
- 너무 작으면: 문맥 손실
- 실험을 통해 최적값을 찾아라

**④ 임베딩 모델 미스매치**
- 색인 시와 검색 시 반드시 같은 임베딩 모델을 사용해야 한다
- 모델을 변경하면 전체 재임베딩이 필요하다

---

## 6. 코드 예제

### 구조 판단 프레임워크

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class ArchitectureDecision:
    """구조 판단 결과"""
    recommendation: Literal["MCP", "RAG", "Hybrid"]
    rationale: list[str]
    concerns: list[str]

def decide_architecture(
    needs_realtime: bool,
    needs_external_actions: bool,
    has_knowledge_base: bool,
    knowledge_changes_frequently: bool,
    team_api_experience: bool,
    budget_sensitive: bool,
) -> ArchitectureDecision:
    """
    요구사항 기반으로 구조를 추천한다.
    실무에서는 이 함수를 팀 논의의 출발점으로 사용한다.
    """
    rationale = []
    concerns = []

    # 판단 로직
    if needs_external_actions and not has_knowledge_base:
        rec = "MCP"
        rationale.append("외부 시스템 조작이 필요하고 문서 검색은 불필요")
    elif has_knowledge_base and not needs_realtime and not needs_external_actions:
        rec = "RAG"
        rationale.append("정적 지식 기반 Q&A에 최적화")
        if knowledge_changes_frequently:
            concerns.append("문서 변경 시 재임베딩 파이프라인 구축 필요")
    else:
        rec = "Hybrid"
        rationale.append("실시간 데이터와 지식 검색 모두 필요")
        concerns.append("구현 복잡도와 운영 비용이 높음")
        if budget_sensitive:
            concerns.append("비용 초과 위험: RAG와 API 비용 모두 발생")

    if not team_api_experience and rec in ["MCP", "Hybrid"]:
        concerns.append("팀의 API 통합 경험 부족 → 학습 비용 고려")

    return ArchitectureDecision(
        recommendation=rec,
        rationale=rationale,
        concerns=concerns
    )

# 사용 예시
decision = decide_architecture(
    needs_realtime=True,           # 실시간 데이터 필요
    needs_external_actions=True,   # 외부 시스템 조작 필요
    has_knowledge_base=True,       # 사내 문서 있음
    knowledge_changes_frequently=False,
    team_api_experience=True,
    budget_sensitive=False,
)

print(f"권장 구조: {decision.recommendation}")
print(f"이유: {', '.join(decision.rationale)}")
if decision.concerns:
    print(f"주의사항: {', '.join(decision.concerns)}")
```

---

## Q&A

**Q. RAG와 Fine-tuning 중 무엇을 선택해야 하는가?**

> Fine-tuning은 모델의 "행동 방식"을 바꾸는 데 적합하다.
> RAG는 모델에게 "최신 지식"을 제공하는 데 적합하다.
> 사내 문서 검색에는 RAG가, 특정 스타일이나 형식 준수에는 Fine-tuning이 적합하다.
> 대부분의 실무 케이스는 RAG로 충분하다.

**Q. Tool 수가 많아지면 어떻게 처리해야 하는가?**

> 라우팅 레이어를 추가한다.
> 첫 번째 LLM이 "어떤 Tool 그룹이 필요한가"를 판단하고,
> 두 번째 LLM이 해당 그룹 내에서 구체적인 Tool을 선택한다.
> 또는 도메인별로 Sub-agent를 분리하여 각각이 관련 Tool만 관리한다.

**Q. 벡터 DB는 어떤 것을 써야 하는가?**

> 2026년 기준 주요 선택지: Pinecone(관리형), Weaviate(오픈소스), pgvector(Postgres 확장).
> 소규모(문서 100만 개 이하): pgvector로 시작하면 충분하다.
> 대규모·고성능: Pinecone이나 Weaviate 고려.
> 가장 중요한 것은 임베딩 모델 선택이며, 벡터 DB는 나중에 교체 가능하다.

---

## 퀴즈

### Q1. Tool 설계 원칙

다음 Tool 설계 중 가장 문제가 있는 것은?

```python
# Tool A
def manage_everything(action: str, target: str, data: dict) -> dict:
    """모든 데이터 관리 작업 처리"""
    ...

# Tool B
def get_user_profile(user_id: str) -> dict:
    """사용자 프로필 조회"""
    ...

# Tool C
def send_notification(channel: str, message: str, priority: str) -> dict:
    """알림 발송"""
    ...
```

<details>
<summary>힌트</summary>
LLM이 어떤 Tool을 언제 써야 하는지 이해할 수 있어야 한다.
</details>

<details>
<summary>정답 및 해설</summary>

**정답: Tool A**

Tool A는 단일 책임 원칙을 위반한다:
- `action` 파라미터로 동작이 완전히 달라진다
- LLM이 "manage_everything"이 언제 필요한지 이해하기 어렵다
- 실패 시 어떤 동작이 실패했는지 파악 어렵다

B, C는 명확한 단일 책임을 가진다.

</details>

---

### Q2. RAG 청킹 전략

기술 매뉴얼(섹션 > 단락 > 문장 구조)을 RAG에 사용할 때 가장 적합한 청킹 전략은?

- A) 고정 크기 (200 토큰마다 분할)
- B) 계층적 청킹 (섹션 → 단락 단위)
- C) 단일 문장 단위 분할
- D) 문서 전체를 하나의 청크로

<details>
<summary>힌트</summary>
구조화된 문서는 구조를 유지하는 청킹이 유리하다.
</details>

<details>
<summary>정답 및 해설</summary>

**정답: B**

기술 매뉴얼은 섹션 > 단락의 계층 구조를 가진다.
계층적 청킹을 사용하면:
- 의미 단위가 분리되지 않음
- 검색 시 적절한 문맥 제공
- 섹션 제목이 청크에 포함되어 검색 정확도 향상

A: 문장 중간에서 잘릴 수 있음
C: 단일 문장은 문맥이 너무 적음
D: 너무 크면 검색 정밀도 저하

</details>

---

### Q3. 구조 선택

다음 시나리오에 가장 적합한 구조는?

> "고객 서비스 Agent: 고객이 질문하면 제품 매뉴얼(PDF 500페이지)에서 답변을 찾고, 필요 시 주문 시스템에서 고객의 주문 현황을 조회한다."

- A) MCP만 사용 (Tool 중심)
- B) RAG만 사용
- C) Hybrid (RAG + MCP)
- D) 단순 LLM 호출

<details>
<summary>힌트</summary>
두 가지 다른 유형의 정보 소스가 필요하다.
</details>

<details>
<summary>정답 및 해설</summary>

**정답: C (Hybrid)**

두 가지 요구사항이 다른 구조를 필요로 한다:
- 매뉴얼 검색 → RAG (정적 문서 기반)
- 주문 현황 조회 → MCP Tool (실시간 DB 조회)

이 경우 Hybrid가 불가피하다.
RAG 결과와 Tool 결과를 LLM이 통합하여 최종 답변을 생성한다.

</details>

---

### Q4. RAG 한계

다음 중 RAG가 잘 처리하지 못하는 경우는?

- A) "환불 정책이 어떻게 되나요?" (정책 문서 기반)
- B) "제 주문 #12345의 현재 배송 위치는?" (실시간 배송 추적)
- C) "제품 설치 방법을 알려주세요" (매뉴얼 기반)
- D) "이전 고객 문의 사례에서 비슷한 케이스를 찾아주세요" (과거 데이터)

<details>
<summary>힌트</summary>
RAG는 문서에 없는 실시간 정보를 가져올 수 없다.
</details>

<details>
<summary>정답 및 해설</summary>

**정답: B**

실시간 배송 위치는 배송 API를 통해 실시간으로 조회해야 한다.
RAG는 이미 임베딩된 문서만 검색할 수 있으므로 실시간 데이터 조회 불가.

A, C, D는 모두 문서/데이터베이스 기반으로 RAG가 처리 가능하다.

</details>

---

### Q5. Hybrid 구조 주의사항

Hybrid 구조를 도입할 때 가장 먼저 확인해야 할 것은?

- A) 어떤 벡터 DB를 사용할지
- B) RAG와 Tool 각각으로 해결할 수 없는지 먼저 검토
- C) 몇 개의 Tool을 만들지
- D) 임베딩 모델 선택

<details>
<summary>힌트</summary>
Hybrid는 복잡도가 높다. 단순한 구조로 해결되는지 먼저 확인해야 한다.
</details>

<details>
<summary>정답 및 해설</summary>

**정답: B**

Hybrid는 구현 복잡도와 운영 비용이 높다.
반드시 "RAG만으로 안 되는가?" "Tool만으로 안 되는가?"를 먼저 검토해야 한다.
두 구조가 모두 필요한 이유가 명확할 때만 Hybrid를 선택한다.

A, C, D는 Hybrid 선택 후 결정할 사항이다.

</details>

---

## 실습 안내

> 실습 상세는 `labs/day1/s4-architecture-decision/README.md` 참고

### 강의 (25분)

MCP와 RAG의 개념, 동작 원리, 적용 기준을 설명한다.

### 시연 (25분)

강사가 PydanticAI로 MCP 방식과 RAG 방식을 각각 구현하여 같은 질문에 대한 차이를 시연한다.

- `src/01_demo_mcp.ipynb` — PydanticAI Agent + Tool 호출 방식
- `src/02_demo_rag.ipynb` — 문서 임베딩 + 유사도 검색 방식

### 과제 (40분)

MCP와 RAG를 직접 구현하고 비교한 뒤, 의사결정 매트릭스로 자신의 Agent에 최적 구조를 선택한다.

- `src/03_compare_lab.ipynb` — TODO 채워서 MCP vs RAG 비교
- `artifacts/decision-matrix-template.md` — 구조 설계 의사결정 문서
- 정답: `solution/01_comparison.ipynb`

### 같이 보기 (15분)

"신입 사원 온보딩 도우미 Agent" 시나리오에 대해 전체가 함께 구조를 결정한다.
