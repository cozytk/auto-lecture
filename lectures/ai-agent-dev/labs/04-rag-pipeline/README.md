# 실습 04: RAG 파이프라인 구현

## 실습 목적

Retrieval-Augmented Generation의 전체 파이프라인을 직접 구현하고,
Embedding 기반 의미 검색이 키워드 검색과 어떻게 다른지 체험한다.

- **연관 세션**: Session 4 - MCP·RAG·Hybrid 구조 판단
- **난이도**: 중급
- **예상 소요 시간**: 30분 (I DO 8분 / WE DO 10분 / YOU DO 12분)

## 사전 준비

```bash
export OPENROUTER_API_KEY="your-api-key"
export MODEL="moonshotai/kimi-k2"
just setup
```

---

## I DO: 시연 관찰 (약 8분)

강사가 시연하는 코드를 관찰하세요. 직접 코드를 작성하지 않아도 됩니다.

### 시연 내용

- 5개 FAQ 문서를 Embedding으로 벡터화
- 질문과의 코사인 유사도로 관련 문서 검색 (Retrieval)
- 검색된 문서를 프롬프트에 포함 (Augmentation)
- LLM이 문서 기반으로 답변 생성 (Generation)

### 시연 코드 실행

```bash
just run-i-do
```

### 관찰 포인트

- `"재고가 얼마나 남아있나요?"`처럼 문서에 없는 질문에는 "확인할 수 없습니다"라고 답변한다
- top_k=1과 top_k=3의 답변 품질 차이를 비교한다
- 코사인 유사도 점수로 어떤 문서가 검색되는지 확인한다

---

## WE DO: 함께 실습 (약 10분)

강사와 함께 `src/we-do/rag_pipeline.py`의 `retrieve` 함수를 완성합니다.

### 1단계: retrieve 함수 완성

```python
def retrieve(query: str, top_k: int = 2) -> list[tuple[str, float]]:
    # 1. query를 벡터로 변환
    query_vector = embed([query])[0]

    scored = []
    for doc, doc_vec in zip(documents, doc_vectors):
        # 2. 코사인 유사도 계산
        a, b = np.array(query_vector), np.array(doc_vec)
        sim = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        scored.append((doc, sim))

    # 3. 내림차순 정렬 후 top_k 반환
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]
```

### 2단계: top_k 비교 실험

```bash
just run-we-do
```

`top_k=1, 2, 3`으로 바꾸어가며 답변 품질 차이를 확인하세요.

---

## YOU DO: 독립 과제 (약 12분)

`src/you-do/rag_pipeline.py`를 완성하세요.

### 과제 설명

본인의 도메인에 맞는 RAG 파이프라인을 구현하세요:

1. `documents`에 본인 도메인 문서 **5개 이상** 작성
   - 각 문서는 하나의 주제를 명확히 다루는 1~3문장
2. `embed` 함수 구현 (OpenRouter Embedding API 호출)
3. `retrieve` 함수 구현 (코사인 유사도 기반 검색)
4. `rag_answer` 함수 구현 (Retrieval → Augmentation → Generation)

### 시작 방법

```bash
just run
```

### 검증 기준

- 문서가 5개 이상인가
- 3가지 질문에서 올바른 문서가 검색되는가
- 문서에 없는 질문에 "확인할 수 없습니다"라고 답하는가

### 힌트

<details>
<summary>힌트 1: embed 함수</summary>

```python
def embed(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model="openai/text-embedding-3-small",
        input=texts,
    )
    return [item.embedding for item in response.data]
```
</details>

<details>
<summary>힌트 2: 코사인 유사도 계산</summary>

```python
import numpy as np

a = np.array(vector1)
b = np.array(vector2)
cosine_sim = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
```
</details>

<details>
<summary>힌트 3: Augmentation 프롬프트 구조</summary>

```python
context = "\n".join(
    f"[문서{i}] {doc}" for i, (doc, _) in enumerate(retrieved, 1)
)
augmented_prompt = (
    f"참고 문서:\n{context}\n\n"
    "위 문서만 참고하여 답변하세요. "
    "문서에 없는 내용은 '문서에서 확인할 수 없습니다'라고 답변하세요.\n\n"
    f"질문: {query}"
)
```
</details>

### 정답 확인

```bash
just run-solution
```

---

## 검증 방법

```bash
just test
```

## 트러블슈팅

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| 관련 없는 문서가 검색됨 | 문서가 너무 짧거나 주제가 모호함 | 각 문서를 1~3문장, 단일 주제로 작성 |
| 문서에 있는 내용도 "확인 불가" | top_k가 너무 작아 관련 문서 누락 | top_k를 2~3으로 늘리기 |
| 할루시네이션 발생 | 프롬프트에 "문서에 없으면..." 지시 누락 | Augmentation 프롬프트 확인 |
| `numpy` 없음 | 패키지 미설치 | `pip install numpy` |
