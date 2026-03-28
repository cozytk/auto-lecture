"""
WE DO + YOU DO: RAG 파이프라인 스캐폴드

강사와 함께 빈 칸을 채워나갑니다.
TODO 주석을 찾아 구현하세요.
"""

import os
import re
import json
import argparse
import numpy as np
from typing import Optional

def _get_client():
    """anthropic 클라이언트를 지연 초기화 (테스트 환경에서 임포트 오류 방지)"""
    import anthropic  # noqa: PLC0415
    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

# ── 샘플 문서 로드 ─────────────────────────────────────────
def load_document(path: str = "./src/sample_doc.md") -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


# ── Chunking 함수들 ────────────────────────────────────────

def fixed_size_chunk(text: str, size: int = 300, overlap: int = 50) -> list[str]:
    """
    고정 크기 Chunking

    TODO:
    1. start=0 에서 시작
    2. end = start + size 로 슬라이싱
    3. text[start:end] 를 chunks에 추가
    4. start = end - overlap 으로 이동 (오버랩 적용)
    5. 마지막 남은 텍스트도 포함
    """
    chunks = []
    # TODO: 구현하세요
    return chunks


def semantic_chunk(text: str, max_size: int = 400) -> list[str]:
    """
    의미 단위 Chunking (단락 → 줄 → 문장 순서로 분할)

    TODO:
    1. "\n\n" 로 먼저 분할
    2. max_size보다 큰 단락은 "\n", 그래도 크면 "." 로 재분할
    3. 작은 단락들은 합쳐서 max_size에 가깝게 묶기
    """
    chunks = []
    # TODO: 구현하세요
    return chunks


def header_based_chunk(markdown: str) -> list[dict]:
    """
    헤더 기반 Chunking (## 헤더 단위로 분할)

    반환 형식: [{"header": "헤더명", "content": "헤더 + 내용 전체"}, ...]

    TODO:
    1. re.split 또는 re.findall로 헤더(#, ##, ###) 위치 찾기
    2. 각 헤더와 그 다음 헤더 사이의 내용을 content로 저장
    3. {"header": 헤더명, "content": 섹션 전체} 형태로 반환
    """
    sections = []
    # TODO: 구현하세요
    return sections


# ── 임베딩 ─────────────────────────────────────────────────

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    텍스트 목록을 임베딩 벡터로 변환

    실제 API 키가 없을 경우 Mock 벡터 반환
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        # Mock: 랜덤 벡터 (테스트용)
        return [list(np.random.randn(256).astype(float)) for _ in texts]

    # TODO: client.beta.messages 대신 임베딩 API 호출
    # voyage-3 모델 사용 (Anthropic 권장)
    # 실제 구현 시 참고: solution/rag_solution.py
    return [list(np.random.randn(256).astype(float)) for _ in texts]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """코사인 유사도 계산"""
    # TODO: numpy를 사용해 구현하세요
    # 힌트: np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return 0.0


# ── 벡터 스토어 ────────────────────────────────────────────

class SimpleVectorStore:
    """인메모리 벡터 스토어"""

    def __init__(self, name: str = "default"):
        self.name = name
        self.docs: list[dict] = []
        self.vectors: list[list[float]] = []

    def add(self, chunks: list[str], metadata: Optional[dict] = None):
        """Chunk 목록을 임베딩하여 저장"""
        # TODO: 구현하세요
        # 1. embed_texts(chunks) 호출
        # 2. 각 Chunk를 {"content": chunk, "metadata": metadata or {}} 형태로 저장
        pass

    def add_dicts(self, chunk_dicts: list[dict]):
        """딕셔너리 형태 Chunk 저장 (header_based_chunk 결과용)"""
        texts = [d.get("content", "") for d in chunk_dicts]
        vectors = embed_texts(texts)
        for d, v in zip(chunk_dicts, vectors):
            self.docs.append(d)
            self.vectors.append(v)

    def search(
        self,
        query: str,
        k: int = 5,
        threshold: float = 0.0
    ) -> list[dict]:
        """쿼리와 유사한 상위 k개 Chunk 반환"""
        if not self.docs:
            return []

        query_vec = embed_texts([query])[0]
        scores = [cosine_similarity(query_vec, v) for v in self.vectors]

        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in ranked[:k]:
            if score >= threshold:
                results.append({**self.docs[idx], "score": score})

        return results

    def stats(self) -> dict:
        """스토어 통계"""
        if not self.docs:
            return {"count": 0, "avg_len": 0, "min_len": 0, "max_len": 0}
        lengths = [len(d.get("content", "")) for d in self.docs]
        return {
            "name": self.name,
            "count": len(self.docs),
            "avg_len": int(np.mean(lengths)),
            "min_len": min(lengths),
            "max_len": max(lengths),
        }


# ── RAG 파이프라인 ─────────────────────────────────────────

SYSTEM_PROMPT = """
당신은 제공된 문서 기반으로만 답변하는 전문가입니다.

규칙:
1. [참조 문서]에 있는 내용만 사용하여 답변하세요.
2. 문서에 없는 내용은 "제공된 문서에서 확인할 수 없습니다"라고 명시하세요.
3. 추측하지 마세요.
4. 답변 근거 문서는 [출처: n] 형식으로 표시하세요.
"""


def rag_answer(
    query: str,
    store: SimpleVectorStore,
    k: int = 5,
    threshold: float = 0.65,
) -> dict:
    """
    RAG 파이프라인 실행

    TODO:
    1. store.search(query, k, threshold)로 관련 Chunk 검색
    2. 검색 결과가 없으면 "관련 문서 없음" 반환
    3. 검색 결과로 컨텍스트 구성
    4. LLM에 전달하여 답변 생성
    5. 신뢰도(max score) 계산하여 반환
    """
    # TODO: 구현하세요
    return {
        "answer": "TODO: 구현 필요",
        "confidence": "none",
        "sources": [],
        "top_score": 0.0,
        "chunks_used": 0
    }


# ── 평가 ───────────────────────────────────────────────────

EVAL_QUERIES = [
    {"query": "RAG의 핵심 구성 요소는?", "keyword": "Retrieval"},
    {"query": "Chunking이란 무엇인가?", "keyword": "Chunk"},
    {"query": "Semantic Chunking의 분할 우선순위는?", "keyword": "단락"},
    {"query": "Top-k 값이 작으면 어떤 문제가 있나?", "keyword": "커버리지"},
    {"query": "Re-ranking에서 Cross-encoder의 역할은?", "keyword": "Cross-encoder"},
    {"query": "한국어 임베딩 모델 추천은?", "keyword": "multilingual"},
    {"query": "Similarity Threshold 권장 범위는?", "keyword": "0.65"},
    {"query": "Hallucination을 줄이는 프롬프트 전략은?", "keyword": "확인할 수 없다"},
    {"query": "Fixed-size Chunking의 Overlap이란?", "keyword": "Overlap"},
    {"query": "Document-aware Chunking의 장점은?", "keyword": "헤더"},
]


def evaluate_store(store: SimpleVectorStore, k: int = 3) -> dict:
    """
    각 쿼리에 대한 Recall@k 측정
    keyword가 Top-k 결과에 포함되면 Hit으로 간주
    """
    hits = 0
    for case in EVAL_QUERIES:
        results = store.search(case["query"], k=k, threshold=0.0)
        found = any(
            case["keyword"].lower() in r.get("content", "").lower()
            for r in results
        )
        if found:
            hits += 1
    recall = hits / len(EVAL_QUERIES)
    return {
        "store": store.name,
        "recall_at_k": recall,
        "k": k,
        "hits": hits,
        "total": len(EVAL_QUERIES)
    }


def measure_faithfulness(answer: str, source_docs: list[str]) -> float:
    """
    TODO (YOU DO 과제):
    답변의 각 문장이 출처 문서에 근거하는지 확인
    반환값: 0.0 ~ 1.0 (1.0이 완전 충실)

    힌트: LLM에게 "이 답변이 아래 문서에 근거하는가?" 를 물어보는
         Self-verification 패턴을 사용하세요.
    """
    # TODO: 구현하세요
    return 0.0


# ── 메인 ───────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", default="./src/sample_doc.md")
    parser.add_argument("--threshold", type=float, default=0.65)
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()

    print("=" * 60)
    print("RAG Chunking 전략 비교")
    print("=" * 60)

    # 문서 로드
    try:
        doc = load_document(args.doc)
    except FileNotFoundError:
        print(f"문서를 찾을 수 없습니다: {args.doc}")
        return

    print(f"\n문서 길이: {len(doc)} 문자")

    # ── Chunking ───────────────────────────────────────────
    chunks_fixed = fixed_size_chunk(doc, size=300, overlap=50)
    chunks_semantic = semantic_chunk(doc, max_size=400)
    chunks_header = header_based_chunk(doc)

    print(f"\nChunking 결과:")
    print(f"  Fixed-size  : {len(chunks_fixed)}개 Chunk")
    print(f"  Semantic    : {len(chunks_semantic)}개 Chunk")
    print(f"  Header-based: {len(chunks_header)}개 섹션")

    # ── 인덱싱 ─────────────────────────────────────────────
    print("\n인덱싱 중...")
    store_fixed = SimpleVectorStore("fixed")
    store_semantic = SimpleVectorStore("semantic")
    store_header = SimpleVectorStore("header")

    store_fixed.add(chunks_fixed)
    store_semantic.add(chunks_semantic)
    store_header.add_dicts(chunks_header)

    for s in [store_fixed, store_semantic, store_header]:
        stats = s.stats()
        print(f"  [{stats['name']}] {stats['count']}개, "
              f"평균 {stats['avg_len']}자, "
              f"최소 {stats['min_len']}자, 최대 {stats['max_len']}자")

    # ── 평가 ───────────────────────────────────────────────
    print(f"\nRecall@{args.k} 측정 (keyword 포함 여부):")
    for store in [store_fixed, store_semantic, store_header]:
        result = evaluate_store(store, k=args.k)
        print(f"  [{result['store']:8s}] Recall@{args.k}: "
              f"{result['hits']}/{result['total']} "
              f"({result['recall_at_k']*100:.0f}%)")

    # ── Threshold 비교 ─────────────────────────────────────
    test_query = "Chunking이란 무엇인가?"
    print(f"\nThreshold 비교 (쿼리: '{test_query}'):")
    for threshold in [0.5, 0.7, 0.85]:
        results = store_semantic.search(test_query, k=10, threshold=threshold)
        print(f"  threshold={threshold}: {len(results)}개 결과")

    # ── RAG 답변 (샘플) ────────────────────────────────────
    print(f"\n샘플 RAG 답변:")
    result = rag_answer(
        "RAG의 핵심 구성 요소를 설명해줘",
        store_semantic,
        k=args.k,
        threshold=args.threshold
    )
    print(f"  신뢰도: {result['confidence']} (top_score: {result['top_score']:.2f})")
    print(f"  사용된 Chunk 수: {result['chunks_used']}")
    print(f"  답변 (앞 200자): {result['answer'][:200]}...")


if __name__ == "__main__":
    main()
