# Day 3 Session 3 — RAG 성능을 결정하는 4가지 요소

> **목표**: Chunking 전략, Embedding 선택, Retrieval 튜닝, Hallucination 방지를 체계적으로 이해
> **시간**: 2시간 | **대상**: AI 개발자, 데이터 엔지니어, 기술 리더

---

## 1. 왜 중요한가

RAG(Retrieval-Augmented Generation)는 LLM의 환각을 줄이는
가장 실용적인 방법이다.
그러나 잘못 설계된 RAG는 오히려 노이즈를 증폭시킨다.

"RAG를 쓴다"는 것만으로 성능이 보장되지 않는다.
Chunking 방식 하나가 Retrieval 정확도를 30% 바꾼다.
→ **설계 디테일이 RAG의 품질을 결정한다**

---

## 2. 핵심 원리

### 2.1 Chunking 전략 비교

**Chunking이란**

대용량 문서를 검색 가능한 단위(Chunk)로 분할하는 과정이다.
Chunk가 너무 크면 관련 없는 내용이 포함된다.
Chunk가 너무 작으면 맥락이 끊겨 이해하기 어렵다.

**전략 1: Fixed-size Chunking (고정 크기)**

```python
def fixed_size_chunk(text: str, size: int = 512, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap  # 오버랩으로 맥락 연속성 확보
    return chunks
```

| 항목 | 내용 |
|------|------|
| 장점 | 구현 단순, 일관된 크기 |
| 단점 | 문장 중간에서 분할 가능 |
| 적합 | 비구조화 텍스트, 빠른 프로토타입 |

**전략 2: Semantic Chunking (의미 단위)**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", "!", "?", ",", " "]
    # 우선순위: 단락 > 줄 > 문장 > 단어
)
chunks = splitter.split_text(document)
```

| 항목 | 내용 |
|------|------|
| 장점 | 자연스러운 경계에서 분할 |
| 단점 | Chunk 크기 불일치 |
| 적합 | 일반 문서, 기사, 보고서 |

**전략 3: Document-aware Chunking (구조 인식)**

```python
# Markdown 문서: 헤더 단위로 분할
import re

def header_based_chunk(markdown: str) -> list[dict]:
    sections = re.split(r"^#{1,3}\s+", markdown, flags=re.MULTILINE)
    headers = re.findall(r"^#{1,3}\s+(.+)$", markdown, flags=re.MULTILINE)

    return [
        {"header": h, "content": s.strip()}
        for h, s in zip(headers, sections[1:])
        if s.strip()
    ]
```

| 항목 | 내용 |
|------|------|
| 장점 | 문서 구조 보존, 맥락 완전 |
| 단점 | 문서 포맷 의존적 |
| 적합 | Markdown, HTML, PDF(구조화) |

**전략 4: Hierarchical Chunking (계층형)**

```
문서
├── 대단원 (2000 tokens) → 개요 검색용
│   ├── 소단원 (500 tokens) → 세부 검색용
│   │   └── 문장 (50 tokens) → 정밀 검색용
```

→ 쿼리 유형에 따라 적절한 레벨의 Chunk를 선택한다.
→ 구현 복잡도는 높지만 정확도가 가장 높다.

---

### 2.2 Embedding 모델 선택

**Embedding이란**

텍스트를 고차원 벡터로 변환하는 과정이다.
유사한 의미의 텍스트는 벡터 공간에서 가까운 위치에 있다.
Embedding 품질 = 검색 품질의 상한선이다.

**주요 모델 비교 (2026년 기준)**

| 모델 | 차원 | 한국어 | 속도 | 비용 | 추천 상황 |
|------|------|--------|------|------|-----------|
| `text-embedding-3-large` | 3072 | 우수 | 중간 | 유료 | 프로덕션 (영어 중심) |
| `text-embedding-3-small` | 1536 | 양호 | 빠름 | 저렴 | 비용 민감한 서비스 |
| `multilingual-e5-large` | 1024 | 최우수 | 중간 | 무료 | 한국어 전용 서비스 |
| `bge-m3` | 1024 | 우수 | 빠름 | 무료 | 온프레미스 배포 |
| `voyage-3` | 1024 | 양호 | 빠름 | 유료 | Claude와 최적화 |

**임베딩 생성 예시**

```python
import anthropic
import numpy as np

client = anthropic.Anthropic()

def embed_texts(texts: list[str], model: str = "voyage-3") -> list[list[float]]:
    # Voyage AI (Anthropic 권장)
    response = client.embeddings.create(
        model=model,
        input=texts
    )
    return [e.embedding for e in response.data]

def cosine_similarity(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

**차원 선택 기준**

```
고차원 (3072): 정확도 최우선, 저장 비용 감수
중간 (1024~1536): 정확도와 비용의 균형
저차원 (256~512): 속도 최우선, 정확도 일부 포기
```

→ Matryoshka Representation Learning(MRL) 지원 모델은
차원을 동적으로 줄일 수 있다 (`text-embedding-3` 시리즈).

---

### 2.3 Retrieval 튜닝 (Top-k, Threshold, Re-ranking)

**기본 Retrieval 파이프라인**

```
쿼리
 → 쿼리 임베딩 생성
 → 벡터 DB에서 Top-k 검색
 → Threshold 필터링
 → Re-ranking
 → 최종 컨텍스트 선택
 → LLM 생성
```

**Top-k 설정**

```python
# Top-k: 검색할 Chunk 수
# 작을수록: 관련성 높지만 커버리지 낮음
# 클수록: 커버리지 높지만 노이즈 증가

def retrieve(query: str, k: int = 5) -> list[dict]:
    query_embedding = embed_texts([query])[0]

    results = vector_db.search(
        vector=query_embedding,
        top_k=k,
        include_metadata=True
    )
    return results
```

| Top-k | 장점 | 단점 | 추천 상황 |
|-------|------|------|-----------|
| 3 | 노이즈 적음 | 누락 가능 | 정확한 사실 조회 |
| 5~10 | 균형 | - | 일반 QA |
| 20+ | 커버리지 높음 | 토큰 비용 증가 | 포괄적 요약 |

**Similarity Threshold 필터링**

```python
def retrieve_with_threshold(
    query: str,
    k: int = 10,
    threshold: float = 0.7
) -> list[dict]:
    results = retrieve(query, k=k)

    # 유사도가 threshold 미만인 결과 제거
    filtered = [r for r in results if r["score"] >= threshold]

    if not filtered:
        # 임계값 내 결과 없으면 최상위 1개만 반환 (Fallback)
        return results[:1]

    return filtered
```

→ Threshold를 너무 높게 설정하면 관련 문서를 놓친다.
→ 0.65~0.75가 일반적인 권장 범위다.
→ 도메인별로 실험적으로 조정해야 한다.

**Re-ranking (Cross-encoder)**

```python
from sentence_transformers import CrossEncoder

# Cross-encoder: 쿼리-문서 쌍을 함께 평가 (더 정확하지만 느림)
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, candidates: list[dict], top_n: int = 3) -> list[dict]:
    if not candidates:
        return []

    # (쿼리, 문서) 쌍 생성
    pairs = [(query, c["content"]) for c in candidates]

    # Re-ranking 점수 계산
    scores = reranker.predict(pairs)

    # 점수 기준 정렬 후 상위 N개 반환
    ranked = sorted(
        zip(candidates, scores),
        key=lambda x: x[1],
        reverse=True
    )
    return [doc for doc, _ in ranked[:top_n]]
```

**Re-ranking이 중요한 이유**

```
벡터 검색 (Bi-encoder): 쿼리와 문서를 각각 임베딩 후 코사인 유사도
→ 빠르지만 쿼리-문서 상호작용을 포착하지 못함

Re-ranking (Cross-encoder): 쿼리+문서를 함께 입력
→ 느리지만 관련성 정확도가 20~40% 향상
→ 처음 100개 검색 후 Top 5로 줄이는 패턴이 일반적
```

---

### 2.4 Hallucination 최소화 전략

**Hallucination 발생 원인**

| 원인 | 설명 | 해결책 |
|------|------|--------|
| 관련 문서 없음 | 검색 실패 → LLM이 추측 | Threshold 강화 |
| 노이즈 문서 포함 | 무관한 내용이 컨텍스트에 포함 | Re-ranking, Threshold |
| 컨텍스트 초과 | 너무 많은 Chunk → 핵심 희석 | Top-k 줄이기 |
| 프롬프트 설계 부재 | "모른다"고 말하도록 유도 안 함 | 명시적 지침 |

**Prompt 수준 Hallucination 방지**

```python
SYSTEM_PROMPT = """
당신은 주어진 문서 기반으로만 답변하는 전문가입니다.

규칙:
1. 아래 [참조 문서]에 있는 내용만 사용하여 답변하세요.
2. 문서에 없는 내용은 "제공된 문서에서 확인할 수 없습니다"라고 명시하세요.
3. 추측이나 일반 지식으로 답변하지 마세요.
4. 답변 근거가 된 문서 번호를 [출처: n]으로 표시하세요.
"""

def build_rag_prompt(query: str, retrieved_docs: list[dict]) -> str:
    context = "\n\n".join([
        f"[문서 {i+1}]\n{doc['content']}"
        for i, doc in enumerate(retrieved_docs)
    ])

    return f"""
[참조 문서]
{context}

[질문]
{query}

위 참조 문서에 기반하여 답변해주세요.
"""
```

**신뢰도 점수 기반 필터링**

```python
def rag_with_confidence(query: str) -> dict:
    # 1. Retrieval
    candidates = retrieve(query, k=10)
    reranked = rerank(query, candidates, top_n=5)

    # 2. 신뢰도 확인
    max_score = max(r["score"] for r in reranked) if reranked else 0

    if max_score < 0.6:
        return {
            "answer": "죄송합니다. 해당 질문에 대한 신뢰할 수 있는 정보를 찾을 수 없습니다.",
            "confidence": "low",
            "sources": []
        }

    # 3. LLM 생성
    prompt = build_rag_prompt(query, reranked)
    answer = llm_generate(prompt)

    return {
        "answer": answer,
        "confidence": "high" if max_score > 0.8 else "medium",
        "sources": [r["metadata"]["source"] for r in reranked]
    }
```

**자기 검증 (Self-verification) 패턴**

```python
VERIFICATION_PROMPT = """
다음 답변이 제공된 문서에 근거하는지 검토하세요.

[문서]
{context}

[답변]
{answer}

검토 결과:
- 문서 기반: (예/아니오)
- 추측 포함: (예/아니오)
- 수정 필요 사항: (없으면 "없음")
"""

def verify_answer(answer: str, context: str) -> dict:
    verification = llm_generate(VERIFICATION_PROMPT.format(
        context=context,
        answer=answer
    ))
    return parse_verification(verification)
```

---

## 3. 실무 의미

**RAG 파이프라인 설계 체크리스트**

```
□ Chunking: 문서 유형에 맞는 전략 선택
□ Overlap: 경계 맥락 보존을 위한 50~100 토큰 오버랩
□ Embedding: 언어·도메인에 맞는 모델 선택
□ Top-k: 쿼리 유형에 따라 3~10 사이 조정
□ Threshold: 0.65~0.75 기준, 도메인별 실험
□ Re-ranking: 정확도 중요 시 Cross-encoder 적용
□ Prompt: "모른다" 답변 허용, 출처 표시 요구
□ 신뢰도: 낮은 점수 시 답변 거부 또는 경고
```

**성능 측정 지표**

| 지표 | 설명 | 목표 |
|------|------|------|
| Recall@k | 관련 문서 포함 비율 | ≥ 0.85 |
| Precision@k | 검색 결과 중 관련 비율 | ≥ 0.70 |
| MRR | 첫 번째 관련 문서 순위 | ≥ 0.80 |
| Faithfulness | 답변이 문서 기반인지 | ≥ 0.90 |
| Answer Relevancy | 질문에 답변이 관련 있는지 | ≥ 0.85 |

---

## 4. 비교

### Chunking 전략 비교

| 전략 | 구현 난이도 | 정확도 | 적합 문서 |
|------|------------|--------|-----------|
| Fixed-size | 낮음 | 중간 | 비구조화 텍스트 |
| Semantic | 중간 | 높음 | 일반 문서 |
| Document-aware | 중간 | 높음 | Markdown, HTML |
| Hierarchical | 높음 | 최고 | 복잡한 기술 문서 |

### Retrieval 방법 비교

| 방법 | 속도 | 정확도 | 비용 |
|------|------|--------|------|
| Dense (Vector) | 빠름 | 중간 | 낮음 |
| Sparse (BM25) | 빠름 | 중간 | 낮음 |
| Hybrid (Dense+Sparse) | 중간 | 높음 | 중간 |
| + Re-ranking | 느림 | 최고 | 높음 |

---

## 5. 주의사항

**Embedding 모델 변경 시 재인덱싱 필요**

> Embedding 모델을 바꾸면 기존 벡터와 호환되지 않는다.
> 전체 문서를 새 모델로 다시 임베딩해야 한다.
> 프로덕션에서 모델 변경은 계획적으로 진행해야 한다.

**Chunk 크기와 LLM Context Window**

> Top-k × Chunk 크기 ≤ LLM Context Window.
> Claude 3.5의 경우 200K 토큰이지만,
> 컨텍스트가 길수록 "중간 내용 무시" 현상이 발생할 수 있다.
> 실용적으로는 10~20K 토큰 이내 컨텍스트를 권장한다.

**Re-ranking 지연 시간**

> Cross-encoder 기반 Re-ranking은 Bi-encoder보다 5~10배 느리다.
> 100개 후보를 Re-ranking하면 수백 ms가 소요된다.
> 지연 시간이 중요하면 가벼운 Re-ranker 모델을 선택한다.

**Threshold 0으로 설정하면**

> 모든 검색 결과를 사용하게 되어 노이즈가 급증한다.
> Hallucination 발생 확률이 높아진다.
> 반드시 실험을 통해 적절한 Threshold를 설정해야 한다.

---

## 6. 코드 예제

### 완성된 RAG 파이프라인

```python
import anthropic
import numpy as np
from typing import Optional

client = anthropic.Anthropic()


# ── 임베딩 ────────────────────────────────────────
def embed(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model="voyage-3",
        input=texts
    )
    return [e.embedding for e in response.data]


def cosine_sim(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# ── 간단한 인메모리 벡터 스토어 ────────────────────
class SimpleVectorStore:
    def __init__(self):
        self.docs: list[dict] = []
        self.vectors: list[list[float]] = []

    def add(self, docs: list[dict]):
        texts = [d["content"] for d in docs]
        vectors = embed(texts)
        self.docs.extend(docs)
        self.vectors.extend(vectors)

    def search(self, query: str, k: int = 10, threshold: float = 0.65) -> list[dict]:
        query_vec = embed([query])[0]
        scores = [cosine_sim(query_vec, v) for v in self.vectors]

        # (점수, 인덱스) 정렬
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in ranked[:k]:
            if score >= threshold:
                results.append({**self.docs[idx], "score": score})

        return results


# ── Chunking ──────────────────────────────────────
def chunk_document(text: str, size: int = 512, overlap: int = 50) -> list[str]:
    chunks, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


# ── RAG 파이프라인 ─────────────────────────────────
store = SimpleVectorStore()

SYSTEM_PROMPT = """
당신은 제공된 문서 기반으로만 답변하는 전문가입니다.
문서에 없는 내용은 "제공된 문서에서 확인할 수 없습니다"라고 명시하세요.
답변 근거 문서는 [출처: n] 형식으로 표시하세요.
"""

def rag_answer(query: str, top_k: int = 5) -> dict:
    # 1. Retrieval
    retrieved = store.search(query, k=top_k, threshold=0.65)

    if not retrieved:
        return {
            "answer": "관련 문서를 찾을 수 없습니다.",
            "confidence": "none",
            "sources": []
        }

    # 2. Context 구성
    context = "\n\n".join([
        f"[문서 {i+1}] (관련도: {r['score']:.2f})\n{r['content']}"
        for i, r in enumerate(retrieved)
    ])

    # 3. LLM 생성
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"[참조 문서]\n{context}\n\n[질문]\n{query}"
        }]
    )

    max_score = max(r["score"] for r in retrieved)
    return {
        "answer": response.content[0].text,
        "confidence": "high" if max_score > 0.8 else "medium",
        "sources": [r.get("source", "unknown") for r in retrieved],
        "top_score": max_score
    }


# ── 사용 예시 ──────────────────────────────────────
def main():
    # 문서 인덱싱
    documents = [
        {"content": "RAG는 Retrieval-Augmented Generation의 약자입니다.", "source": "doc1"},
        {"content": "Chunking은 문서를 검색 단위로 분할하는 과정입니다.", "source": "doc2"},
    ]
    store.add(documents)

    # 질의
    result = rag_answer("RAG가 무엇인가요?")
    print(f"답변: {result['answer']}")
    print(f"신뢰도: {result['confidence']}")
    print(f"출처: {result['sources']}")
```

---

## Q&A

**Q1. 한국어 문서에는 어떤 Embedding 모델이 가장 좋나요?**

> `multilingual-e5-large`나 `bge-m3`가 한국어 성능이 우수하다.
> 오픈소스라 비용 없이 사용 가능하다.
> 프로덕션 영어 중심이라면 `text-embedding-3-large`가 더 나을 수 있다.
> 실제 데이터로 벤치마크를 돌려보고 결정하는 것을 권장한다.

**Q2. RAG와 Fine-tuning을 어떻게 선택하나요?**

> 업데이트가 잦은 데이터 → RAG (실시간 갱신 가능)
> 도메인 스타일/어투 변경 → Fine-tuning
> 특정 사실 주입 → RAG (Fine-tuning으로 사실 주입은 신뢰성 낮음)
> 비용 민감 → RAG (Fine-tuning은 학습 비용 발생)

**Q3. 벡터 DB는 어떤 것을 선택해야 하나요?**

> 소규모 프로토타입: ChromaDB (로컬, 무료)
> 중규모 프로덕션: Weaviate, Qdrant (오픈소스)
> 대규모 클라우드: Pinecone, AWS OpenSearch
> 기존 PostgreSQL 사용 중: pgvector 확장

---

## 퀴즈

**Q1. Chunk 크기를 너무 작게 설정했을 때 발생하는 주요 문제는?**

> a) 저장 비용이 증가한다
> b) 맥락이 끊겨 LLM이 충분한 정보를 받지 못한다
> c) 임베딩 모델이 처리할 수 없다
> d) 검색 속도가 느려진다

<details>
<summary>힌트 및 정답</summary>

**힌트**: "서울의 인구는 약 950만 명이다. 이 도시는 한반도 북위 37도에 위치한다." 이 두 문장을 따로 자르면 어떤 문제가 생길까?

**정답**: b) 맥락이 끊겨 LLM이 충분한 정보를 받지 못한다

Chunk가 너무 작으면 하나의 개념을 설명하는 문장들이 분리되어 검색 결과에 단편적인 정보만 포함된다. LLM은 불완전한 맥락으로 답변을 생성하게 된다.

</details>

---

**Q2. Bi-encoder와 Cross-encoder의 주요 차이점은?**

> a) Bi-encoder는 유료, Cross-encoder는 무료
> b) Bi-encoder는 쿼리와 문서를 각각 임베딩, Cross-encoder는 함께 입력
> c) Cross-encoder는 벡터를 사용하지 않는다
> d) Bi-encoder는 한국어를 지원하지 않는다

<details>
<summary>힌트 및 정답</summary>

**힌트**: 왜 Cross-encoder가 더 정확하지만 느릴까?

**정답**: b) Bi-encoder는 쿼리와 문서를 각각 임베딩, Cross-encoder는 함께 입력

Bi-encoder는 각각 임베딩 후 코사인 유사도를 계산하므로 빠르다. Cross-encoder는 (쿼리, 문서) 쌍을 함께 처리해 상호작용을 포착하므로 더 정확하지만 느리다.

</details>

---

**Q3. Hallucination을 줄이기 위한 Prompt 설계에서 가장 중요한 요소는?**

> a) 프롬프트를 최대한 짧게 작성한다
> b) "모른다"고 답변하는 것을 명시적으로 허용한다
> c) 항상 답변을 생성하도록 강제한다
> d) 영어로 프롬프트를 작성한다

<details>
<summary>힌트 및 정답</summary>

**힌트**: LLM이 답을 모를 때 어떻게 행동하도록 유도해야 할까?

**정답**: b) "모른다"고 답변하는 것을 명시적으로 허용한다

LLM은 기본적으로 답변을 생성하려 한다. "문서에 없는 내용은 모른다고 하라"고 명시해야 추측 기반 답변을 방지할 수 있다.

</details>

---

**Q4. Similarity Threshold를 0.9로 높게 설정하면 어떤 문제가 생기나요?**

> a) 검색 속도가 느려진다
> b) 관련 문서를 놓쳐 빈 결과가 반환될 수 있다
> c) 임베딩 벡터 크기가 증가한다
> d) API 비용이 증가한다

<details>
<summary>힌트 및 정답</summary>

**힌트**: 기준이 너무 높으면 통과하는 것이 줄어든다.

**정답**: b) 관련 문서를 놓쳐 빈 결과가 반환될 수 있다

Threshold가 너무 높으면 실제로 관련 있는 문서도 필터링되어 검색 결과가 없게 된다. 이 경우 RAG 없이 LLM만 사용하는 것과 같아져 Hallucination이 증가한다.

</details>

---

**Q5. 프로덕션 RAG에서 권장하는 Retrieval 순서는?**

> a) 쿼리 임베딩 → 벡터 검색 → LLM 생성
> b) 쿼리 임베딩 → 벡터 검색 → Re-ranking → Threshold 필터 → LLM 생성
> c) LLM 생성 → 결과 검증 → 벡터 검색
> d) 벡터 검색 → 쿼리 임베딩 → Re-ranking

<details>
<summary>힌트 및 정답</summary>

**힌트**: 정확도를 높이려면 검색 후 어떤 단계를 추가해야 할까?

**정답**: b) 쿼리 임베딩 → 벡터 검색 → Re-ranking → Threshold 필터 → LLM 생성

이 순서가 정확도와 효율의 균형을 잡는 표준 파이프라인이다. 넓게 검색(Top-k 크게) 후 Re-ranking으로 좁히고, Threshold로 최종 필터링한다.

</details>

---

## 실습 명세

### 실습 제목: Chunk 전략별 Retrieval 비교

**I DO (시연, 15분)**

강사가 직접 시연한다:
1. 동일 문서를 Fixed-size vs Semantic 방식으로 Chunking
2. 각 전략의 Chunk 수, 크기 분포 시각화
3. 동일 쿼리에 대한 각 전략의 Retrieval 결과 비교
4. Threshold 0 vs 0.7 설정 시 결과 차이 확인

**WE DO (함께, 30분)**

학생과 함께 단계별 구현:
1. 3가지 Chunking 함수 구현 (Fixed, Semantic, Header-based)
2. SimpleVectorStore에 각 전략의 결과 인덱싱
3. 동일 10개 쿼리로 각 전략 검색 정확도 측정
4. Re-ranking 적용 전후 결과 비교

**YOU DO (독립, 30분)**

- 자신만의 문서(PDF 또는 텍스트)로 RAG 파이프라인 구축
- Chunking 전략 2가지 이상 비교 실험
- Threshold 값 3가지 (0.5, 0.7, 0.85) 비교
- Faithfulness 점수 측정 스크립트 작성
- `solution/` 폴더에 정답 코드 제공
