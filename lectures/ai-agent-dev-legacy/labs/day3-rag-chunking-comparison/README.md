# 실습: RAG Chunking 전략별 Retrieval 비교

**세션**: Day 3 Session 3 — RAG 성능을 결정하는 4가지 요소
**소요 시간**: 75분 (I DO 15분 · WE DO 30분 · YOU DO 30분)
**목표**: Fixed-size, Semantic, Document-aware 세 가지 Chunking 전략을 구현하고, 동일 쿼리에 대한 Retrieval 정확도와 Hallucination 발생률을 비교한다.

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

### 시연 1: Chunking 전략별 Chunk 수·크기 분포

```bash
just demo-chunk
```

**확인 포인트**:
- 동일 문서를 세 가지 방식으로 자르면 Chunk 수가 얼마나 다른가?
- Fixed-size에서 문장이 중간에 잘리는 경우를 확인

### 시연 2: 동일 쿼리의 Retrieval 결과 비교

```bash
just demo-retrieval
```

**확인 포인트**:
- "RAG의 핵심 구성 요소는?" 쿼리에 대해 각 전략이 어떤 Chunk를 반환하는가?
- Threshold 0 vs 0.7 설정 시 결과 개수 차이

### 시연 3: Hallucination 발생 예시

```bash
just demo-hallucination
```

**확인 포인트**:
- Threshold 없이 모든 결과를 LLM에 전달했을 때 답변 품질
- 낮은 관련도 Chunk가 LLM 답변에 어떤 영향을 주는가

---

## WE DO — 함께 구현 (30분)

`src/rag_pipeline.py`를 열고 단계별로 함께 구현합니다.

### Step 1: 세 가지 Chunking 함수 구현

```python
# src/rag_pipeline.py의 chunking 함수들을 완성하세요

def fixed_size_chunk(text: str, size: int = 512, overlap: int = 50) -> list[str]:
    # TODO: 고정 크기로 텍스트를 분할, overlap 적용
    pass

def semantic_chunk(text: str, max_size: int = 512) -> list[str]:
    # TODO: 문장·단락 경계에서 분할
    # 힌트: "\n\n", "\n", ".", "!", "?" 순서로 분할 시도
    pass

def header_based_chunk(markdown: str) -> list[dict]:
    # TODO: ## 헤더 단위로 분할
    # 반환 형식: [{"header": "헤더명", "content": "내용"}, ...]
    pass
```

### Step 2: 벡터 스토어 인덱싱

```python
store_fixed = SimpleVectorStore()
store_semantic = SimpleVectorStore()
store_header = SimpleVectorStore()

# TODO: 각 전략으로 Chunk 생성 후 인덱싱
chunks_fixed = fixed_size_chunk(SAMPLE_DOC)
# ...
```

### Step 3: 동일 쿼리로 정확도 측정

```python
EVAL_QUERIES = [
    {"query": "RAG의 핵심 구성 요소는?", "relevant_keyword": "Retrieval"},
    {"query": "Chunking이란 무엇인가?", "relevant_keyword": "Chunk"},
    # 8개 더 추가...
]
```

### Step 4: Re-ranking 적용 전후 비교

```bash
just run
```

---

## YOU DO — 독립 실습 (30분)

### 과제

**과제 1: 자체 문서로 RAG 파이프라인 구축**

아래 샘플 문서 대신 자신의 문서(텍스트 파일 또는 마크다운)를 사용하여
RAG 파이프라인을 구축하세요.

```bash
# 자신의 문서 경로 설정
export RAG_DOC_PATH=./my_document.md
just run-custom
```

**과제 2: Chunking 전략 비교 실험**

두 가지 이상의 Chunking 전략을 비교하고 결과를 기록하세요.

비교 항목:
- Chunk 수
- 평균 Chunk 크기 (토큰)
- Top-1 Recall (관련 Chunk가 1위에 오는 비율)
- Top-3 Recall (관련 Chunk가 3위 이내에 오는 비율)

**과제 3: Threshold 3가지 비교**

동일 쿼리에 대해 Threshold 0.5, 0.7, 0.85를 설정하고
각 설정의 결과 수와 답변 품질을 비교하세요.

| Threshold | 결과 수 | 답변 품질 | 특이사항 |
|-----------|---------|---------|---------|
| 0.5 | ? | ? | |
| 0.7 | ? | ? | |
| 0.85 | ? | ? | |

**과제 4: Faithfulness 측정**

생성된 답변이 문서 내용에 얼마나 충실한지 측정하는 스크립트를 작성하세요.

```python
def measure_faithfulness(answer: str, source_docs: list[str]) -> float:
    """
    답변의 각 문장이 출처 문서에 근거하는지 확인
    반환값: 0.0 ~ 1.0 (1.0이 완전 충실)
    """
    # TODO: 구현
    pass
```

```bash
just test
```

정답 코드: `solution/` 폴더를 참조하세요.

---

## 체크리스트

실습 완료 전 확인:

```
□ fixed_size_chunk: overlap 적용 확인
□ semantic_chunk: 문장 경계에서 분할 확인
□ header_based_chunk: 헤더별 딕셔너리 반환 확인
□ 세 전략의 Chunk 수·크기 비교 결과 기록
□ Threshold 0.5 / 0.7 / 0.85 결과 비교
□ Faithfulness 측정 함수 구현
□ 과제 결과 표 작성 완료
```

---

## 참고: Chunking 전략 선택 가이드

```
문서 유형별 권장 전략:

비구조화 텍스트 (소설, 뉴스 기사)
  → Fixed-size (overlap 50~100 토큰)

일반 문서 (보고서, 논문 초록)
  → Semantic (단락·문장 경계 기준)

구조화 문서 (Markdown, HTML, API 문서)
  → Document-aware (헤더·섹션 단위)

복잡한 기술 문서 (수백 페이지 매뉴얼)
  → Hierarchical (대단원 → 소단원 → 문장)
```

---

## 성능 측정 지표 참고

| 지표 | 설명 | 측정 방법 |
|------|------|----------|
| Recall@k | Top-k 안에 관련 Chunk 포함 비율 | 수동 레이블 비교 |
| Precision@k | Top-k 중 실제 관련 비율 | 수동 레이블 비교 |
| Faithfulness | 답변이 문서에 근거하는 비율 | LLM 자기 검증 |
| Answer Relevancy | 답변이 질문에 관련 있는 비율 | 임베딩 유사도 |
