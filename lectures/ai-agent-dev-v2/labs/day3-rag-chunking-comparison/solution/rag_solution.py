"""
정답 코드: RAG 파이프라인 완성본

YOU DO 과제를 마친 후 참고하세요.
"""

import os
import re
import json
import time
import numpy as np
import anthropic
from typing import Optional

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))


# ── Chunking ───────────────────────────────────────────────

def fixed_size_chunk(text: str, size: int = 300, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap
    return chunks


def semantic_chunk(text: str, max_size: int = 400) -> list[str]:
    # 1단계: 단락으로 분할
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks = []
    current = ""

    for para in paragraphs:
        # 단락이 max_size보다 크면 문장 단위로 재분할
        if len(para) > max_size:
            sentences = re.split(r"(?<=[.!?])\s+", para)
            for sent in sentences:
                if len(current) + len(sent) + 1 <= max_size:
                    current = (current + " " + sent).strip()
                else:
                    if current:
                        chunks.append(current)
                    current = sent
        else:
            if len(current) + len(para) + 2 <= max_size:
                current = (current + "\n\n" + para).strip()
            else:
                if current:
                    chunks.append(current)
                current = para

    if current:
        chunks.append(current)

    return [c for c in chunks if c.strip()]


def header_based_chunk(markdown: str) -> list[dict]:
    # 헤더 패턴으로 분할
    header_pattern = re.compile(r"^(#{1,3})\s+(.+)$", re.MULTILINE)
    matches = list(header_pattern.finditer(markdown))

    if not matches:
        return [{"header": "전체 문서", "content": markdown.strip()}]

    sections = []
    for i, match in enumerate(matches):
        header_text = match.group(2).strip()
        content_start = match.end()
        content_end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown)
        content = markdown[content_start:content_end].strip()

        sections.append({
            "header": header_text,
            "content": f"# {header_text}\n\n{content}",
            "level": len(match.group(1))
        })

    return sections


# ── 임베딩 ─────────────────────────────────────────────────

def embed_texts(texts: list[str]) -> list[list[float]]:
    """실제 임베딩 API 호출 (API 키 없으면 Mock)"""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        np.random.seed(hash(texts[0]) % (2**32) if texts else 0)
        return [list(np.random.randn(256).astype(float)) for _ in texts]

    try:
        # voyage-3는 별도 API 엔드포인트 사용
        # 실제 운영에서는 voyageai 패키지 또는 Anthropic 클라이언트 사용
        import voyageai  # type: ignore
        vo = voyageai.Client()
        result = vo.embed(texts, model="voyage-3")
        return result.embeddings
    except Exception:
        # Fallback: Mock 벡터
        return [list(np.random.randn(256).astype(float)) for _ in texts]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a_arr, b_arr = np.array(a), np.array(b)
    denom = np.linalg.norm(a_arr) * np.linalg.norm(b_arr)
    if denom == 0:
        return 0.0
    return float(np.dot(a_arr, b_arr) / denom)


# ── 벡터 스토어 ────────────────────────────────────────────

class SimpleVectorStore:
    def __init__(self, name: str = "default"):
        self.name = name
        self.docs: list[dict] = []
        self.vectors: list[list[float]] = []

    def add(self, chunks: list[str], metadata: Optional[dict] = None):
        vectors = embed_texts(chunks)
        for chunk, vec in zip(chunks, vectors):
            self.docs.append({"content": chunk, "metadata": metadata or {}})
            self.vectors.append(vec)

    def add_dicts(self, chunk_dicts: list[dict]):
        texts = [d.get("content", "") for d in chunk_dicts]
        vectors = embed_texts(texts)
        for d, v in zip(chunk_dicts, vectors):
            self.docs.append(d)
            self.vectors.append(v)

    def search(self, query: str, k: int = 5, threshold: float = 0.0) -> list[dict]:
        if not self.docs:
            return []
        query_vec = embed_texts([query])[0]
        scores = [cosine_similarity(query_vec, v) for v in self.vectors]
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in ranked[:k * 2]:  # 여유 있게 가져온 후 threshold 필터
            if score >= threshold and len(results) < k:
                results.append({**self.docs[idx], "score": score})
        return results

    def stats(self) -> dict:
        if not self.docs:
            return {"name": self.name, "count": 0, "avg_len": 0, "min_len": 0, "max_len": 0}
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
    retrieved = store.search(query, k=k, threshold=threshold)

    if not retrieved:
        return {
            "answer": "관련 문서를 찾을 수 없습니다.",
            "confidence": "none",
            "sources": [],
            "top_score": 0.0,
            "chunks_used": 0
        }

    context = "\n\n".join([
        f"[문서 {i+1}] (관련도: {r['score']:.2f})\n{r['content']}"
        for i, r in enumerate(retrieved)
    ])

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"[참조 문서]\n{context}\n\n[질문]\n{query}"
        }]
    )

    max_score = max(r["score"] for r in retrieved)
    return {
        "answer": response.content[0].text,
        "confidence": "high" if max_score > 0.8 else "medium" if max_score > 0.65 else "low",
        "sources": [r.get("header", r.get("metadata", {}).get("source", "unknown")) for r in retrieved],
        "top_score": max_score,
        "chunks_used": len(retrieved)
    }


# ── Faithfulness 측정 ──────────────────────────────────────

FAITHFULNESS_PROMPT = """
다음 답변이 제공된 문서에 근거하는지 검토하세요.

[문서]
{context}

[답변]
{answer}

각 문장을 검토하고 다음 JSON으로 응답하세요:
{{
  "faithful_sentences": <문서 근거 문장 수>,
  "total_sentences": <전체 문장 수>,
  "unsupported_claims": [<근거 없는 주장 목록>]
}}
"""


def measure_faithfulness(answer: str, source_docs: list[str]) -> float:
    context = "\n\n".join(source_docs[:3])  # 상위 3개 문서만 사용
    prompt = FAITHFULNESS_PROMPT.format(context=context, answer=answer)

    try:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.content[0].text
        # JSON 파싱 시도
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            total = data.get("total_sentences", 1)
            faithful = data.get("faithful_sentences", 0)
            return faithful / total if total > 0 else 0.0
    except Exception:
        pass
    return 0.5  # 파싱 실패 시 중간값 반환


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


# ── 메인 ───────────────────────────────────────────────────

def main():
    doc_path = "./src/sample_doc.md"
    try:
        with open(doc_path, encoding="utf-8") as f:
            doc = f.read()
    except FileNotFoundError:
        print(f"문서 없음: {doc_path}")
        return

    print("=" * 60)
    print("RAG 파이프라인 정답 코드 실행")
    print("=" * 60)
    print(f"문서 길이: {len(doc)} 문자")

    # Chunking
    chunks_fixed = fixed_size_chunk(doc, size=300, overlap=50)
    chunks_semantic = semantic_chunk(doc, max_size=400)
    chunks_header = header_based_chunk(doc)

    print(f"\nChunking 결과:")
    print(f"  Fixed-size  : {len(chunks_fixed)}개")
    print(f"  Semantic    : {len(chunks_semantic)}개")
    print(f"  Header-based: {len(chunks_header)}개")

    # 인덱싱
    print("\n인덱싱 중...")
    store_fixed = SimpleVectorStore("fixed")
    store_semantic = SimpleVectorStore("semantic")
    store_header = SimpleVectorStore("header")

    store_fixed.add(chunks_fixed)
    store_semantic.add(chunks_semantic)
    store_header.add_dicts(chunks_header)

    for s in [store_fixed, store_semantic, store_header]:
        st = s.stats()
        print(f"  [{st['name']:8s}] {st['count']}개, 평균 {st['avg_len']}자")

    # Recall@3 평가
    print("\nRecall@3 측정:")
    for store in [store_fixed, store_semantic, store_header]:
        r = evaluate_store(store, k=3)
        print(f"  [{r['store']:8s}] {r['hits']}/{r['total']} ({r['recall_at_k']*100:.0f}%)")

    # Threshold 비교
    test_query = "Chunking이란 무엇인가?"
    print(f"\nThreshold 비교 ('{test_query}'):")
    for thr in [0.5, 0.7, 0.85]:
        results = store_semantic.search(test_query, k=10, threshold=thr)
        print(f"  threshold={thr}: {len(results)}개 결과")

    # RAG 답변 샘플
    print("\nRAG 답변 샘플:")
    result = rag_answer("RAG의 핵심 구성 요소를 설명해줘", store_semantic, k=5, threshold=0.65)
    print(f"  신뢰도: {result['confidence']} ({result['top_score']:.2f})")
    print(f"  Chunk 수: {result['chunks_used']}")
    print(f"  답변:\n{result['answer'][:300]}...")

    # Faithfulness 측정
    if result["chunks_used"] > 0:
        top_docs = [r["content"] for r in store_semantic.search(
            "RAG의 핵심 구성 요소", k=3, threshold=0.0)]
        faith = measure_faithfulness(result["answer"], top_docs)
        print(f"\nFaithfulness 점수: {faith:.2f}")


if __name__ == "__main__":
    main()
