# Session 4: MCP·RAG·Hybrid 구조 판단 (2h)

## 학습 목표

1. MCP(Function Calling)의 역사적 배경과 동작 원리를 이해하고, Tool 기반 아키텍처를 설계할 수 있다
2. RAG의 Retrieval-Augmentation-Generation 파이프라인을 이해하고, 각 단계의 설계 기준을 수립할 수 있다
3. MCP와 RAG의 구조적 한계를 인식하고, 의사결정 트리를 활용하여 최적의 구조를 선택할 수 있다

---

## 개념 1: MCP(Function Calling) 아키텍처

### 왜 이것이 중요한가

LLM은 본질적으로 **텍스트 입력 → 텍스트 출력** 모델이다.
아무리 뛰어난 추론 능력을 갖추더라도, LLM 단독으로는:
- 현재 날씨를 확인할 수 없다
- 데이터베이스에서 고객 정보를 조회할 수 없다
- 외부 서비스에 요청을 보낼 수 없다

> 이 근본적 한계를 해결하기 위해 등장한 것이 **Function Calling(Tool Use)**이다.

---

### 핵심 원리: Function Calling의 역사와 동작 방식

**진화 과정:**

| 연도 | 사건 | 의미 |
|------|------|------|
| 2023년 초 | OpenAI ChatGPT Plugins 출시 | "LLM이 외부 세계와 상호작용 가능" 첫 실험 |
| 2023년 6월 | OpenAI GPT API Function Calling 공식 도입 | Agent 아키텍처의 사실상 표준화 |
| 2024년 | Anthropic MCP(Model Context Protocol) 발표 | 벤더 중립적 표준 프로토콜 지향 |

**핵심 메커니즘:**

**LLM이 직접 수행하는 것:**
→ 사용자 메시지 분석 및 의도 파악
→ 적합한 Tool 선택 및 파라미터 JSON 생성
→ Tool 결과를 바탕으로 자연어 응답 생성

**개발자 코드가 수행하는 것:**
→ 외부 API 실제 호출 및 데이터 수신
→ Tool 호출 결과의 유효성 검증

> **핵심**: LLM은 "무엇을 호출할지 결정"하고, 애플리케이션은 "실제로 호출하고 결과를 검증"한다.

---

### 실무에서의 의미

**전체 흐름 5단계:**

① 사용자가 메시지를 보낸다
② LLM이 분석하고 `tool_calls` 응답을 반환한다
③ 애플리케이션이 지정된 Tool을 실제로 실행한다
④ Tool 실행 결과를 대화 이력에 추가한다
⑤ LLM이 Tool 결과를 참고하여 최종 응답을 생성한다

→ 하나의 사용자 요청에 이 사이클이 여러 번 반복될 수 있다.

**적합한 사용 사례:**

| 사례 | 설명 |
|------|------|
| 외부 시스템 조회/조작 | DB 쿼리, REST API 호출, 파일 시스템 접근 |
| 실시간 데이터 접근 | 현재 날씨, 주가, 재고 상태 |
| 정확한 계산/변환 | 복잡한 수학 계산, 단위 변환 |

---

### 다른 접근법과의 비교

| 구분 | Function Calling | MCP |
|------|-----------------|-----|
| 범위 | 함수 호출 메커니즘 | Tool + Resource + Prompt + Sampling 표준화 |
| 벤더 종속 | 각 벤더별 구현 | 벤더 중립적 표준 프로토콜 |
| 현재 상태 | 사실상 표준 | 업계 통합 진행 중 |

---

### 주의사항

> **Tool 폭발(Tool Explosion) 문제**
> Tool이 10개 이상이면 LLM의 Tool 선택 정확도가 급격히 떨어진다.
> Tool 정의가 프롬프트의 일부로 매 호출마다 전송 → 토큰 비용 비례 증가
> 유사 기능의 Tool이 많으면 LLM이 혼동한다 (`search_orders` vs `find_orders`)

Tool 수가 20개를 넘으면:
→ 카테고리별 그룹화 후 2단계 선택 패턴을 사용한다

> **할루시네이션에 의한 잘못된 호출**
> Tool description에 "언제 이 Tool을 사용해야 하는지"를 명확히 기술한다.
> 반환된 JSON의 유효성을 반드시 검증한다.

---

### 코드 예제

이를 코드로 표현하면:

```python
import os
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

# Tool 정의: JSON Schema로 함수 시그니처를 기술
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_orders",
            "description": (
                "고객 ID로 주문 이력을 조회합니다. "
                "최근 주문부터 반환합니다. "
                "환불/교환 처리 전 주문 상태 확인에 사용하세요."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "고객 고유 식별자 (예: CUST-12345)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "반환할 최대 주문 수. 기본값: 10",
                    },
                },
                "required": ["customer_id"],
            },
        },
    },
]

def execute_tool(name: str, args: dict) -> dict:
    """Tool 실행 (실제 환경에서는 DB/API 호출)"""
    if name == "search_orders":
        return {"success": True, "orders": [
            {"order_id": "ORD-789", "status": "delivered",
             "items": ["노트북"], "amount": 1500000}]}
    return {"success": False, "error": f"Unknown tool: {name}"}

def run_agent(user_message: str):
    messages = [
        {"role": "system", "content": "당신은 고객 지원 Agent입니다."},
        {"role": "user", "content": user_message},
    ]
    # 1차 호출: LLM이 Tool 호출 여부를 판단
    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=tools, tool_choice="auto",
    )
    assistant_msg = response.choices[0].message

    if assistant_msg.tool_calls:
        messages.append(assistant_msg)
        for tc in assistant_msg.tool_calls:
            fn_args = json.loads(tc.function.arguments)
            result = execute_tool(tc.function.name, fn_args)
            messages.append({
                "role": "tool", "tool_call_id": tc.id,
                "content": json.dumps(result, ensure_ascii=False),
            })
        # 2차 호출: Tool 결과 기반 최종 응답 생성
        final = client.chat.completions.create(model=MODEL, messages=messages)
        return final.choices[0].message.content
    return assistant_msg.content

print(run_agent("CUST-123 고객의 최근 주문 상태를 확인해주세요"))
```

실행 결과:

```
CUST-123 고객님의 최근 주문을 확인했습니다.
- 주문번호: ORD-789, 상태: 배송 완료, 상품: 노트북, 금액: 1,500,000원
```

---

### Q&A

**Q: Function Calling과 MCP는 같은 것인가요?**
A: 엄밀히 말하면 다르다.
Function Calling: LLM이 함수 호출을 결정하는 메커니즘 (각 벤더별 구현).
MCP: Anthropic이 주도하는 개방형 표준 프로토콜 (Function Calling을 포함한 상위 개념).
실무에서는 "Function Calling"과 "Tool Use"를 거의 동의어로 사용한다.

**Q: Tool 호출 비용은 어떻게 계산하나요?**
A: Tool 호출 자체에는 별도 비용이 없다.
다만 Tool 정의(JSON Schema)가 시스템 프롬프트에 포함되어 매 호출마다 입력 토큰으로 소비된다.
Tool 3개를 정의하면 약 500~1000 토큰이 추가된다.
공식: `Tool 정의 토큰 + 2회 이상의 LLM 호출 비용 + 외부 API 비용`

<details>
<summary>퀴즈: Function Calling 흐름에서 LLM이 직접 수행하는 것과 수행하지 않는 것을 구분해보자</summary>

**보기:**
1. 사용자 메시지 분석 및 의도 파악
2. 적합한 Tool 선택 및 파라미터 JSON 생성
3. 외부 API 실제 호출 및 데이터 수신
4. Tool 실행 결과를 바탕으로 자연어 응답 생성
5. Tool 호출 결과의 유효성 검증

**힌트**: LLM은 "텍스트 입력 → 텍스트 출력" 모델이라는 본질을 기억하자.

**정답**: LLM이 직접 수행하는 것은 **1, 2, 4번**이다.
**3번**(실제 API 호출)과 **5번**(결과 검증)은 개발자의 애플리케이션 코드가 수행한다.
LLM은 "무엇을 호출할지 결정"하고, 애플리케이션은 "실제로 호출하고 검증"한다.
</details>

---

## 개념 2: RAG 아키텍처

### 왜 이것이 중요한가

LLM은 학습 데이터에 포함된 정보만 "알고 있다."
학습 데이터에는 시간적 한계(cutoff date)가 있다.
기업 내부 문서, 비공개 데이터, 최신 정보는 포함되지 않는다.

"우리 회사의 2025년 1분기 환불 정책이 뭐야?"라고 물으면:
→ LLM이 할 수 있는 것은 두 가지뿐이다.
→ "모르겠습니다" 또는 **그럴듯하게 지어내는 것(할루시네이션)**

> **RAG(Retrieval-Augmented Generation)**: "LLM에게 질문을 보내기 전에, 먼저 관련된 문서를 찾아서 함께 전달하자"

---

### 핵심 원리: RAG 파이프라인 3단계

**① Retrieval(검색)**
→ 사용자의 질문과 관련성이 높은 문서 조각(chunk)을 검색
→ 사전 준비: 문서를 적절한 크기로 분할(chunking) + 벡터(embedding)로 변환 + Vector DB 저장
→ 질문도 벡터화 → 코사인 유사도로 가장 유사한 문서 조각 반환

> **"검색이 잘못되면 아무리 뛰어난 LLM도 정확한 답변을 생성할 수 없다"**
> 이것이 RAG의 가장 중요한 원칙이다.

**② Augmentation(증강)**
→ 검색된 문서 조각을 사용자의 질문과 함께 LLM 프롬프트로 구성
→ "다음 문서를 참고하여 답변하세요. 문서에 없는 내용은 답변하지 마세요."
→ top_k 권장값: **3~5** (너무 작으면 정보 누락, 너무 크면 관련 없는 정보 혼입)

**③ Generation(생성)**
→ LLM이 증강된 프롬프트를 입력받아 최종 답변을 생성
→ 자신의 내재 지식이 아닌 **제공된 문서를 주요 근거**로 사용
→ 사실 기반 답변: temperature 0에 가깝게 설정

---

### 실무에서의 의미

**RAG가 적합한 사용 사례:**

| 사례 | 설명 |
|------|------|
| 문서 기반 Q&A | 사내 위키, 매뉴얼, FAQ |
| 지식 검색 | 기술 문서, 법률 조항, 의료 가이드라인 |
| 정책/규정 확인 | 환불 정책, 인사 규정, 컴플라이언스 |

공통점: "대량의 문서에서 관련 정보를 찾아 답변을 생성하는" **읽기 전용 패턴**

---

### 다른 접근법과의 비교

| 구분 | 키워드 검색(BM25) | 벡터 검색(RAG) |
|------|----------------|--------------|
| 매칭 방식 | 정확히 같은 단어 | 의미적 유사성 |
| "환불 기한" 검색 시 | "환불 기한" 포함 문서만 | "7일 이내 환불 가능" 문서도 매칭 |
| 오타/동의어 | 약함 | 강함 |
| 속도 | 빠름 | 상대적으로 느림 |

---

### 주의사항

> **"garbage in, garbage out"**
> 검색 품질이 낮으면 관련 없는 문서가 검색되고, LLM은 잘못된 답변을 생성한다.

> **RAG는 읽기 전용 시스템이다.**
> "환불 정책이 뭐야?" → 답할 수 있다.
> "환불 처리해줘" → 수행할 수 없다.

> **데이터 신선도의 한계**
> RAG의 데이터는 인덱싱 시점 기준이다.
> 인덱싱 이후 변경된 정보는 반영되지 않는다.

---

### 코드 예제

이를 코드로 표현하면:

```python
import os
import numpy as np
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

# --- 문서 준비 및 Chunking ---
documents = [
    "환불 정책: 상품 수령 후 7일 이내 환불 가능. 신선식품 24시간, 전자제품 14일 이내.",
    "배송 안내: 일반 배송 2-3 영업일. 당일 배송은 오후 2시 이전 주문 시 적용.",
    "포인트: 구매 금액 1% 적립. 1,000P 이상 사용 가능, 유효기간 12개월.",
]

# --- Embedding + 유사도 검색 ---
def embed(texts):
    r = client.embeddings.create(
        model="openai/text-embedding-3-small", input=texts,
    )
    return [i.embedding for i in r.data]

doc_vecs = embed(documents)

def retrieve(query: str, top_k: int = 2) -> list[str]:
    qv = embed([query])[0]
    scored = []
    for doc, vec in zip(documents, doc_vecs):
        sim = np.dot(qv, vec) / (np.linalg.norm(qv) * np.linalg.norm(vec))
        scored.append((doc, float(sim)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in scored[:top_k]]

# --- Augmentation + Generation ---
def rag_answer(query: str) -> str:
    docs = retrieve(query)
    context = "\n".join(f"[문서{i+1}] {d}" for i, d in enumerate(docs))
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": (
            f"참고 문서:\n{context}\n\n"
            f"위 문서만 참고하여 답변하세요. "
            f"문서에 없으면 '확인 불가'로 표시.\n\n"
            f"질문: {query}"
        )}],
    )
    return resp.choices[0].message.content

print(rag_answer("전자제품 환불 기한이 어떻게 되나요?"))
```

실행 결과:

```
전자제품의 환불 기한은 14일 이내입니다. [문서1 참고]
```

---

### Q&A

**Q: RAG를 사용하면 할루시네이션이 완전히 사라지나요?**
A: 아니다. RAG는 할루시네이션을 크게 **줄이지만** 완전히 제거하지는 못한다.
두 가지 경우에 여전히 발생한다:
① 검색된 문서에 답이 없는 경우 → LLM이 자체 지식으로 "지어낼" 수 있다.
② 검색된 문서를 LLM이 잘못 해석하는 경우.
프롬프트에 "문서에 없는 내용은 답변하지 마세요"를 반드시 포함해야 한다.

**Q: Chunking 크기는 어떻게 정해야 하나요?**
A: 경험적 가이드라인이 있다.
- 너무 작으면(100토큰 이하): 문맥이 부족
- 너무 크면(2000토큰 이상): 관련 없는 내용이 섞임
- 권장 범위: **300~800토큰**, overlap은 chunk_size의 10~20%
실제 질문 세트로 테스트하여 최적값을 찾아야 한다.

<details>
<summary>퀴즈: RAG 파이프라인에서 가장 큰 성능 병목이 되는 단계는?</summary>

**보기:**
1. Chunking (문서 분할)
2. Embedding (벡터 변환)
3. Retrieval (유사도 검색)
4. Generation (LLM 답변 생성)

**힌트**: "전체 시스템의 품질을 좌우하는 단계"와 "실행 시간이 가장 긴 단계"를 구분하자.

**정답**:
- **품질 병목**: 3번 Retrieval. 검색 결과가 잘못되면 LLM도 정확한 답변을 생성할 수 없다.
- **시간 병목**: 4번 Generation. LLM 호출은 보통 1~5초가 소요된다.
품질 최적화 관점에서는 **Retrieval 단계**에 가장 많은 노력을 투자해야 한다.
</details>

---

## 개념 3: Hybrid 아키텍처

### 왜 이것이 중요한가

MCP: LLM에게 **행동 능력(Tool)**을 부여한다.
RAG: LLM에게 **지식(문서)**을 주입한다.

실무에서 가치 있는 Agent의 대부분: **행동과 지식을 동시에 필요로 한다.**

> 고객이 "환불해주세요"라고 요청하면:
> → 주문 상태를 실시간 조회 (Tool)
> → 환불 정책을 검색 (RAG)
> → 두 정보를 종합 판단
> → 환불을 실행 (Tool)

---

### 핵심 원리: MCP만, RAG만으로 부족한 경우

**MCP만으로 부족한 경우:**
→ 고객 "환불 가능한가요?" → 주문 상태 조회(Tool)는 가능하다.
→ 그런데 "환불이 가능한지" 판단하려면 **회사 환불 정책**을 알아야 한다.
→ 수십 페이지 정책 문서를 Tool 코드에 하드코딩하면 유지보수의 악몽이다.
→ **RAG가 필요하다.**

**RAG만으로 부족한 경우:**
→ 트러블슈팅 문서에서 "서비스를 재시작하면 해결됩니다"라는 답을 얻었다.
→ 그런데 현재 서버 메모리 사용량이 얼마인지는 RAG가 알 수 없다.
→ "서비스를 재시작한다"는 행동 자체를 RAG는 수행할 수 없다.
→ **Tool이 필요하다.**

---

### Hybrid 아키텍처의 3가지 패턴

**패턴 1: RAG as Tool**
→ RAG 검색 기능을 하나의 Tool로 래핑하여 Agent Tool 목록에 등록
→ `search_policy(query: str)` → LLM이 정책 관련 질문에 자동으로 호출
→ 적합: **요청 유형이 다양하고 예측하기 어려운 범용 Agent**

**패턴 2: RAG-then-Act**
→ 모든 요청에 대해 먼저 RAG로 지식 수집 → 그 지식을 바탕으로 Tool 호출 판단
→ 보험 상담처럼 "먼저 약관 확인 → 고객 정보 조회 → 보장 내용 안내" 순차 흐름
→ 적합: **지식 확인이 항상 선행되어야 하는 규정/정책 기반 업무**

**패턴 3: Router 기반**
→ 경량 모델이 먼저 요청을 분류 → "RAG 필요", "Tool 필요", "둘 다 필요"로 라우팅
→ 불필요한 RAG 검색이나 Tool 호출을 사전에 차단하여 비용 최적화
→ 적합: **요청 유형이 명확히 구분되고 비용 최적화가 중요한 대규모 서비스**

---

### 실무에서의 의미

**패턴 선택 기준:**

| 패턴 | 적합 상황 | 단점 |
|------|---------|------|
| RAG as Tool | 범용 Agent, 유연한 조합 | LLM이 Tool 선택 놓칠 수 있음 |
| RAG-then-Act | 규정 기반 업무, 순차 흐름 | 단순 질문에서도 RAG 비용 발생 |
| Router | 대규모 서비스, 비용 최적화 | Router 분류 오류 시 정보 누락 |

> **디버깅 용이성도 고려하라.**
> RAG-then-Act: 항상 같은 순서로 실행 → 로그 추적 쉬움.
> RAG as Tool: LLM의 자율적 판단에 의존 → 왜 이 Tool을 선택했는지 추적 어려움.
> **초기에는 디버깅이 쉬운 패턴으로 시작하고, 안정화 후 전환한다.**

---

### 다른 접근법과의 비교

| 구분 | MCP 단독 | RAG 단독 | Hybrid |
|------|---------|---------|--------|
| 쓰기 작업 | ✅ 가능 | ❌ 불가 | ✅ 가능 |
| 문서 기반 판단 | ❌ 어려움 | ✅ 가능 | ✅ 가능 |
| 복잡도 | 중간 | 낮음 | 높음 |
| 비용 | 중간 | 낮음 | 높음 |

---

### 주의사항

> **RAG와 Tool의 정보가 모순되면?**
> 명시적 우선순위 규칙을 시스템 프롬프트에 설정해야 한다.
> 사실적 데이터(재고, 주문 상태): Tool의 실시간 결과를 우선한다.
> 규범적 정보(정책, 법규): RAG 검색 결과를 우선한다.

> **처음부터 Hybrid를 구축하려 하지 말 것.**
> MVP: 단일 아키텍처(RAG 또는 Tool)로 시작한다.
> 사용자 피드백에서 요구가 나올 때 Hybrid로 확장한다.

---

### 코드 예제

이를 코드로 표현하면:

```python
import os
import json
import numpy as np
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

# --- RAG 컴포넌트 ---
policy_docs = [
    "환불 기한: 일반 7일, 전자제품 14일, 신선식품 24시간",
    "환불 불가: 개봉 사용 상품, 고객 과실 파손, 주문제작",
    "환불 금액: 10만원 미만 자동처리, 이상은 관리자 승인",
]

def embed(texts):
    r = client.embeddings.create(
        model="openai/text-embedding-3-small", input=texts)
    return [i.embedding for i in r.data]

pvecs = embed(policy_docs)

def search_policy(query: str) -> dict:
    qv = embed([query])[0]
    scored = [(d, float(np.dot(qv, v)/(np.linalg.norm(qv)*np.linalg.norm(v))))
              for d, v in zip(policy_docs, pvecs)]
    scored.sort(key=lambda x: x[1], reverse=True)
    return {"results": [{"content": d, "score": round(s, 3)}
                        for d, s in scored[:2]]}

# --- Tool 정의: RAG + API 혼합 ---
tools = [
    {"type": "function", "function": {
        "name": "search_policy",
        "description": "회사 정책/규정 검색. 환불, 배송 등 정책 질문에 사용.",
        "parameters": {"type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]},
    }},
    {"type": "function", "function": {
        "name": "get_order",
        "description": "주문 ID로 실시간 주문 상태 조회.",
        "parameters": {"type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"]},
    }},
]

def execute(name, args):
    if name == "search_policy": return search_policy(args["query"])
    if name == "get_order":
        return {"order_id": args["order_id"], "amount": 85000,
                "status": "delivered", "delivered_at": "2025-03-01"}
    return {"error": "Unknown tool"}

def hybrid_agent(user_msg: str):
    msgs = [
        {"role": "system", "content":
         "고객 지원 Agent. 정책은 search_policy, 주문은 get_order 사용."},
        {"role": "user", "content": user_msg},
    ]
    while True:
        r = client.chat.completions.create(
            model=MODEL, messages=msgs, tools=tools, tool_choice="auto")
        m = r.choices[0].message
        if not m.tool_calls:
            return m.content
        msgs.append(m)
        for tc in m.tool_calls:
            res = execute(tc.function.name, json.loads(tc.function.arguments))
            msgs.append({"role": "tool", "tool_call_id": tc.id,
                         "content": json.dumps(res, ensure_ascii=False)})

print(hybrid_agent("ORD-456 주문 환불 가능한가요?"))
```

실행 결과:

```
ORD-456 주문(85,000원, 배송완료)을 확인했습니다.
정책상 일반 상품은 수령 후 7일 이내 환불 가능하며,
금액이 10만원 미만이므로 자동 처리됩니다.
```

---

### Q&A

**Q: Hybrid 아키텍처에서 RAG와 Tool의 정보가 모순되면 어떻게 하나요?**
A: 명시적 우선순위 규칙을 시스템 프롬프트에 설정해야 한다.
사실적 데이터(재고, 주문 상태, 잔액) → Tool의 실시간 결과를 우선한다.
규범적 정보(정책, 법규, 규정) → RAG 검색 결과를 우선한다.
두 소스 모두 불확실한 경우 → 사용자에게 양쪽 정보를 모두 제시하고 판단을 요청한다.

**Q: 처음부터 Hybrid로 구축해야 하나요?**
A: 단일 아키텍처로 시작하고 점진적으로 확장하는 것이 권장된다.
RAG 먼저 구축 후 "직접 처리해줬으면"이라는 요구가 나올 때 Tool을 추가한다.
RAG를 Tool로 래핑(RAG as Tool)이 가장 자연스러운 Hybrid 진입점이다.

<details>
<summary>퀴즈: 다음 시나리오에 가장 적합한 Hybrid 패턴은?</summary>

**시나리오**: "개발자가 에러 로그를 붙여넣으면, 사내 트러블슈팅 위키에서 관련 해결책을 찾아 안내하고, 필요하면 Jira 티켓을 자동으로 생성한다."

**보기:**
1. RAG as Tool
2. RAG-then-Act
3. Router

**힌트**: (1) 위키 검색은 어떤 구조? (2) Jira 티켓 생성은 어떤 구조? (3) 이 두 작업의 실행 순서는?

**정답**: **2번 RAG-then-Act**.
먼저 에러 로그를 분석하여 사내 위키에서 트러블슈팅 문서를 검색해야 한다 (RAG).
검색된 해결책을 확인한 후, 해결책이 없거나 수동 조치가 필요한 경우에만 Jira 티켓을 생성한다 (Tool).
"지식 수집 → 판단 → 조건부 행동"의 순차적 흐름이므로 RAG-then-Act가 자연스럽다.
</details>

---

## 개념 4: 아키텍처 선택 의사결정 트리

### 왜 이것이 중요한가

실무에서 가장 어려운 순간: **"우리 문제에는 어떤 아키텍처가 맞는가?"**

잘못된 선택은 두 가지 형태로 비용을 발생시킨다.
→ **과잉 설계(오버엔지니어링)**: 불필요한 복잡도로 개발 속도·유지보수성 저하
→ **과소 설계(언더엔지니어링)**: 기능 부족으로 사용자 가치를 전달하지 못함

---

### 핵심 원리: 의사결정의 3축

**① 데이터 소스**
→ 정적 문서(매뉴얼, 정책, FAQ) → **RAG 적합**
→ 실시간 API(DB, SaaS API, 모니터링) → **Tool(MCP) 적합**
→ 양쪽 모두 → **Hybrid 검토**

**② 상호작용 패턴 (읽기 vs 쓰기)**

> **핵심 구분: 외부 시스템에 변경(side effect)을 가해야 하는가?**

→ 읽기만 필요 → RAG 또는 Tool
→ **쓰기가 하나라도 있으면 Tool은 필수다** (RAG는 읽기 전용)

**③ 실시간성**
→ 분 단위로 변하는 데이터(재고, 주문 상태, 서버 메트릭) → **Tool 필수**
→ 변경 빈도 낮은 데이터(정책, 매뉴얼, 주 1회 변경) → **RAG로 충분**

---

### 의사결정 플로우차트

```
시작: Agent가 해결하는 문제는 무엇인가?
  │
  ├─ Q1: 외부 시스템에 쓰기(생성/수정/삭제) 작업이 필요한가?
  │   ├─ YES → Q2: 대량 문서에서 지식 검색도 필요한가?
  │   │          ├─ YES → Hybrid (MCP + RAG)
  │   │          └─ NO  → MCP (Tool) 단독
  │   └─ NO  → Q3: 실시간 데이터 조회가 필요한가?
  │              ├─ YES → Q4: 정적 문서 검색도 필요한가?
  │              │          ├─ YES → Hybrid (MCP + RAG)
  │              │          └─ NO  → MCP (Tool) 단독
  │              └─ NO  → Q5: 대량 문서 기반 Q&A인가?
  │                         ├─ YES → RAG 단독
  │                         └─ NO  → Simple LLM Call
```

---

### 실무에서의 의미

**실제 사례에 적용:**

| 사례 | Q1(쓰기?) | Q2(문서?) | 결론 |
|------|---------|---------|------|
| 사내 HR 규정 Q&A | No | Yes (수백 페이지) | **RAG 단독** |
| 고객 주문 환불 처리 | Yes | Yes (환불 정책) | **Hybrid** |
| 서버 모니터링/자동복구 | Yes | No | **MCP 단독** |
| 마케팅 카피 생성 | No | No | **Simple LLM** |

**경계 사례 처리:**

문서량이 A4 3~4장 이하라면:
→ RAG를 구축하는 것보다 **시스템 프롬프트에 직접 포함**하는 것이 더 간단하고 정확하다.
→ 일반 기준: 문서량 10페이지 이하 → 시스템 프롬프트, 초과 → RAG 도입

---

### 다른 접근법과의 비교

**아키텍처별 비용-정확도-지연 프로파일:**

| 아키텍처 | LLM호출 | 지연 | 비용 | 정확도 |
|---------|---------|------|------|--------|
| Simple LLM | 1.0회 | 1.5초 | 1.0x | 60~75% |
| RAG 단독 | 1.5회 | 2.5초 | 1.8x | 75~85% |
| MCP 단독 | 2.5회 | 4.0초 | 3.0x | 70~85% |
| Hybrid(RAG+MCP) | 3.5회 | 6.0초 | 4.5x | 85~95% |
| Hybrid(Router) | 2.5회 | 4.5초 | 3.2x | 82~92% |

**핵심 인사이트:**
→ Simple LLM → RAG: 비용 1.8배, 정확도 10~15%p 향상
→ MCP의 가치: 정확도가 아닌 **"행동 능력"(쓰기 작업)**에 있다
→ Hybrid(Router): Hybrid 대비 비용 30% 절감, 정확도 하락 3%p 이내

---

### 주의사항

> **의사결정 트리가 Hybrid를 추천해도 팀 역량이 부족하다면?**
> **점진적 구축 전략**을 따른다.
> ① MVP: 단일 아키텍처로 핵심 가치를 빠르게 검증
> ② 팀이 익숙해지면 두 번째 아키텍처를 추가
> ③ RAG 먼저 → RAG를 Tool로 래핑(RAG as Tool)이 가장 자연스러운 진입점

> **아키텍처 선택을 나중에 바꿀 수 있는가?**
> 가능하지만, 초기 설계에서 **인터페이스 분리**를 해두어야 전환 비용이 최소화된다.
> `get_refund_policy()` 함수를 추상화해두면 내부 구현이 바뀌어도 Agent 로직은 수정하지 않아도 된다.

---

### 코드 예제

이를 코드로 표현하면:

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

def decide_architecture(req: dict) -> dict:
    """아키텍처 의사결정 트리"""
    w = req.get("needs_write", False)
    r = req.get("needs_realtime", False)
    d = req.get("needs_doc_search", False)

    if w:
        if d:
            return {"arch": "Hybrid (MCP+RAG)", "pattern": "RAG as Tool"}
        return {"arch": "MCP 단독", "pattern": "Function Calling Agent"}
    if r:
        if d:
            return {"arch": "Hybrid (MCP+RAG)", "pattern": "Router"}
        return {"arch": "MCP 단독", "pattern": "Function Calling Agent"}
    if d:
        return {"arch": "RAG 단독", "pattern": "기본 RAG 파이프라인"}
    return {"arch": "Simple LLM", "pattern": "단일 API 호출"}

scenarios = [
    {"name": "사내 HR 규정 Q&A",
     "needs_write": False, "needs_realtime": False, "needs_doc_search": True},
    {"name": "고객 주문 환불 처리",
     "needs_write": True,  "needs_realtime": True,  "needs_doc_search": True},
    {"name": "서버 모니터링/자동복구",
     "needs_write": True,  "needs_realtime": True,  "needs_doc_search": False},
    {"name": "마케팅 카피 생성",
     "needs_write": False, "needs_realtime": False, "needs_doc_search": False},
    {"name": "기술문서 기반 장애진단",
     "needs_write": False, "needs_realtime": True,  "needs_doc_search": True},
]

print(f"{'시나리오':<22} {'아키텍처':<18} {'패턴'}")
print("-" * 65)
for s in scenarios:
    n = s.pop("name")
    r = decide_architecture(s)
    print(f"{n:<22} {r['arch']:<18} {r['pattern']}")
```

실행 결과:

```
시나리오                 아키텍처             패턴
-----------------------------------------------------------------
사내 HR 규정 Q&A         RAG 단독             기본 RAG 파이프라인
고객 주문 환불 처리       Hybrid (MCP+RAG)     RAG as Tool
서버 모니터링/자동복구    MCP 단독             Function Calling Agent
마케팅 카피 생성          Simple LLM           단일 API 호출
기술문서 기반 장애진단    Hybrid (MCP+RAG)     Router
```

---

### Q&A

**Q: 의사결정 트리가 Hybrid를 추천하는데, 팀 역량이 부족하면 어떻게 하나요?**
A: 점진적 구축 전략을 따른다.
① MVP는 단일 아키텍처로 핵심 가치를 빠르게 검증한다.
② 팀이 첫 번째 아키텍처에 익숙해지면 두 번째를 추가한다.
③ RAG를 먼저 구축했다면, RAG as Tool 방식으로 Hybrid로 확장한다.

**Q: 아키텍처 선택을 나중에 바꿀 수 있나요?**
A: 가능하지만, 초기 설계에서 인터페이스 분리를 해두어야 전환 비용이 최소화된다.
`get_refund_policy()` 함수를 추상화해두면 내부 구현을 바꾸어도 Agent 로직은 수정할 필요가 없다.
이 원칙은 "의존성 역전(Dependency Inversion)"이라 불리며, 테스트 용이성에도 도움이 된다.

<details>
<summary>퀴즈: 다음 요구사항에 의사결정 트리를 적용하면 어떤 아키텍처가 선택되는가?</summary>

**요구사항**: "법률 사무소에서, 의뢰인이 자신의 사건과 유사한 판례를 찾아달라고 요청하면, 판례 데이터베이스에서 유사 판례를 검색하여 요약본을 제공한다. 필요하면 해당 판례의 원문 PDF를 이메일로 발송한다."

**의사결정 과정:**
- Q1(쓰기 필요?): 이메일 발송은 쓰기 작업인가?
- Q2(문서 검색?): 수천~수만 건의 판례 검색은?

**정답**: **Hybrid (MCP + RAG)**
Q1: Yes → 이메일 발송은 외부 시스템에 대한 쓰기 작업이다.
Q2: Yes → 수천~수만 건의 판례 검색은 전형적인 RAG 사용 사례다.
패턴: **RAG-then-Act** → 먼저 유사 판례를 검색(RAG) → 이메일 발송 여부 판단 → 발송(Tool).
</details>

---

## 실습

### 실습 1: MCP Tool 기반 Agent 구현

- **연관 학습 목표**: 학습 목표 1
- **실습 목적**: Function Calling 기반 Agent의 전체 흐름을 직접 구현하고 동작을 확인한다
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 30분 (I DO 8분 / WE DO 10분 / YOU DO 12분)
- **선행 조건**: Session 3 실습 완료, OpenRouter API 키 준비
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**I DO**: 강사가 `search_orders` Tool 1개를 정의하고, Agent 루프의 전체 흐름을 시연한다.
Tool description의 중요성("언제 사용해야 하는지"를 명시)을 강조한다.

**WE DO**: `cancel_order` Tool을 함께 추가한다.
description을 풍부하게 쓰는 방법, required 파라미터 설정을 함께 작성한다.

**YOU DO**: Session 3에서 설계한 Agent의 Sub-task 중 Tool로 구현할 항목을 선정하여 3개 이상의 Tool을 정의하고 Agent 루프를 구현한다.

```python
import os
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

# TODO: 본인의 Agent에 맞는 Tool을 3개 이상 정의하세요
tools = [
    {
        "type": "function",
        "function": {
            "name": "...",
            "description": "...",  # 언제/왜 사용하는지 상세히 (30자 이상)
            "parameters": {
                "type": "object",
                "properties": {
                    # TODO: 파라미터 정의
                },
                "required": [...],
            },
        },
    },
]
```

3가지 테스트 입력으로 동작을 확인한다:

```python
test_inputs = [
    "Tool 호출이 필요한 질문 1",
    "Tool 호출이 필요 없는 질문",
    "여러 Tool을 순차 호출해야 하는 질문",
]
```

**검증 기준:**
- Tool이 3개 이상 정의되었는가
- Tool description이 30자 이상으로 상세한가
- LLM이 적절한 Tool을 선택하여 호출하는가
- Tool 호출이 불필요한 질문에는 직접 답변하는가

---

### 실습 2: RAG 파이프라인 구현

- **연관 학습 목표**: 학습 목표 2
- **실습 목적**: Chunking, Embedding, Retrieval, Generation의 전체 RAG 파이프라인을 직접 구현한다
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 30분 (I DO 8분 / WE DO 10분 / YOU DO 12분)
- **선행 조건**: 실습 1 완료, openai 패키지 설치
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**I DO**: 강사가 3개 문서로 RAG를 구현하고 "전자제품 환불 기한"을 질문하는 과정을 시연한다.
Chunking, Embedding, Retrieval, Generation 각 단계를 설명한다.

**WE DO**: top_k 값을 1, 2, 5로 바꾸어 가며 답변 품질의 차이를 함께 확인한다.
"왜 top_k가 중요한가?"를 토론한다.

**YOU DO**: 본인의 도메인에 맞는 문서 5개 이상을 준비하고 RAG를 구현한다.
3가지 질문으로 테스트하고 top_k 최적값을 찾는다.

**정답 예시:**

```python
import os
import numpy as np
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

# 1. 문서 준비
my_documents = [
    # 본인 도메인의 문서 5개 이상
]

# 2. Embedding
def embed(texts):
    r = client.embeddings.create(model="openai/text-embedding-3-small", input=texts)
    return [i.embedding for i in r.data]

doc_vecs = embed(my_documents)

# 3. Retrieval
def retrieve(query: str, top_k: int = 3) -> list[str]:
    qv = embed([query])[0]
    scored = [(d, float(np.dot(qv, v)/(np.linalg.norm(qv)*np.linalg.norm(v))))
              for d, v in zip(my_documents, doc_vecs)]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in scored[:top_k]]

# 4. Generation
def rag_answer(query: str) -> str:
    docs = retrieve(query)
    context = "\n".join(f"[문서{i+1}] {d}" for i, d in enumerate(docs))
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": (
            f"참고 문서:\n{context}\n\n위 문서만 참고하여 답변하세요. "
            f"문서에 없으면 '확인 불가'로 표시.\n\n질문: {query}"
        )}],
    )
    return resp.choices[0].message.content
```

**검증 기준:**
- 문서 5개 이상이 준비되었는가
- 3가지 질문 모두 관련 문서를 정확히 검색하는가
- top_k 비교 실험 결과가 기록되었는가

---

### 실습 3: 아키텍처 선택 의사결정 실습

- **연관 학습 목표**: 학습 목표 3
- **실습 목적**: Session 1에서 도출한 Agent 후보 2개에 의사결정 트리를 적용하여 최적 구조를 선택한다
- **실습 유형**: 분석 + 설계
- **난이도**: 중급
- **예상 소요 시간**: 25분 (I DO 5분 / WE DO 8분 / YOU DO 12분)
- **선행 조건**: 실습 1, 2 완료, Session 1 Agent 후보 도출 결과
- **실행 환경**: 로컬 (문서 작성 + Python 코드 실행)

**I DO**: 강사가 "코드 리뷰 자동화" 시나리오를 의사결정 트리로 분석하고 Hybrid(RAG as Tool)를 선택하는 과정을 시연한다.

**WE DO**: "DevOps 장애 대응 자동화"를 함께 분석한다. Q1~Q5를 단계별로 함께 풀어간다.

**YOU DO**: Session 1에서 도출한 Agent 후보 2개 각각에 대해 의사결정 트리를 적용한다.

```python
architecture_decision = {
    "candidate_name": "후보 이름",
    "requirements": {
        "needs_write": True,        # 외부 시스템 쓰기 필요?
        "needs_realtime": True,     # 실시간 데이터 필요?
        "needs_doc_search": False,  # 대량 문서 검색 필요?
    },
    "decision": "Agent / RAG / Hybrid",
    "pattern": "RAG as Tool / RAG-then-Act / Router",
    "reasoning": [
        "이유 1: ...",
        "이유 2: ...",
    ],
    "alternative_considered": "대안 아키텍처와 배제 이유",
}
```

**정답 예시** (주간 보고서 자동화):

```python
architecture_decision = {
    "candidate_name": "주간 보고서 자동화",
    "requirements": {
        "needs_write": True,        # Jira, Slack, Git API 쓰기
        "needs_realtime": True,     # 이번 주 데이터 실시간 조회
        "needs_doc_search": False,  # 정적 문서 검색 불필요
    },
    "decision": "MCP 단독",
    "pattern": "Function Calling Agent",
    "reasoning": [
        "이유 1: 외부 시스템(Jira, Git, Slack, Confluence) 쓰기 작업 필요",
        "이유 2: 4개 Task가 순차적으로 연결되는 멀티스텝 작업",
        "이유 3: 고정된 문서 지식 검색이 아닌 실시간 API 데이터 수집",
    ],
    "alternative_considered": "RAG 배제 - 이번 주 데이터를 실시간 API로 수집해야 하므로 정적 문서 검색인 RAG는 부적합",
}
```

**검증 기준:**
- 3가지 축(쓰기, 실시간, 문서)이 모두 분석되었는가
- 아키텍처 선택이 Session 3 기획서의 목적/범위와 논리적으로 일치하는가
- 대안 아키텍처를 고려하고 배제 이유를 설명했는가

---

## 핵심 정리

- **MCP(Function Calling)**: LLM에게 행동 능력(Tool)을 부여한다. LLM은 "무엇을 호출할지 결정"하고, 애플리케이션이 "실제로 호출하고 검증"한다
- **RAG**: LLM에게 지식(문서)을 주입한다. Retrieval 단계가 전체 품질을 좌우한다. 본질적으로 읽기 전용 시스템이다
- **Hybrid**: 행동(MCP)과 지식(RAG)을 결합한다. 3가지 패턴(RAG as Tool, RAG-then-Act, Router) 중 상황에 맞게 선택한다
- **의사결정 3축**: 쓰기 필요 여부 → 실시간성 → 문서 검색 필요 여부로 아키텍처를 결정한다
- **점진적 접근**: 단일 아키텍처에서 시작하여 필요에 따라 Hybrid로 확장한다
