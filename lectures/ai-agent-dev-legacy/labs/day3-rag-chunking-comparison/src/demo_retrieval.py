"""
강사 시연용: 동일 쿼리에 대한 Chunking 전략별 Retrieval 결과 비교
"""

import os
import re
import numpy as np


def fixed_size_chunk(text: str, size: int = 300, overlap: int = 50) -> list[str]:
    chunks, start = [], 0
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
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, current = [], ""
    for para in paragraphs:
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
    pattern = re.compile(r"^(#{1,3})\s+(.+)$", re.MULTILINE)
    matches = list(pattern.finditer(markdown))
    if not matches:
        return [{"header": "전체 문서", "content": markdown.strip()}]
    sections = []
    for i, match in enumerate(matches):
        header_text = match.group(2).strip()
        content_start = match.end()
        content_end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown)
        content = markdown[content_start:content_end].strip()
        sections.append({"header": header_text, "content": f"# {header_text}\n\n{content}"})
    return sections


def mock_embed(text: str) -> np.ndarray:
    """키워드 기반 Mock 임베딩 (API 없이 시연용)"""
    keywords = [
        "RAG", "Retrieval", "Chunking", "Embedding", "벡터",
        "검색", "문서", "LLM", "임베딩", "Top-k", "Threshold",
        "Re-ranking", "Hallucination", "Fixed", "Semantic", "Header"
    ]
    vec = np.zeros(len(keywords))
    text_lower = text.lower()
    for i, kw in enumerate(keywords):
        if kw.lower() in text_lower:
            count = text_lower.count(kw.lower())
            vec[i] = min(count / 3.0, 1.0)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec + 1e-8


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / denom) if denom > 0 else 0.0


def simple_search(query: str, chunks: list, k: int = 3, threshold: float = 0.0) -> list[dict]:
    q_vec = mock_embed(query)
    results = []
    for chunk in chunks:
        content = chunk if isinstance(chunk, str) else chunk.get("content", "")
        score = cosine_sim(q_vec, mock_embed(content))
        if score >= threshold:
            results.append({"content": content[:120] + "...", "score": score})
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:k]


def main():
    doc_path = os.path.join(os.path.dirname(__file__), "sample_doc.md")
    with open(doc_path, encoding="utf-8") as f:
        doc = f.read()

    chunks_fixed = fixed_size_chunk(doc, size=300, overlap=50)
    chunks_semantic = semantic_chunk(doc, max_size=400)
    chunks_header = header_based_chunk(doc)

    test_queries = [
        "RAG의 핵심 구성 요소는?",
        "Chunking 전략의 종류를 알려줘",
        "Hallucination을 줄이는 방법은?",
    ]

    for query in test_queries:
        print("\n" + "=" * 60)
        print(f"쿼리: {query}")
        print("=" * 60)

        for name, chunks in [
            ("Fixed-size", chunks_fixed),
            ("Semantic", chunks_semantic),
            ("Header", chunks_header),
        ]:
            results = simple_search(query, chunks, k=2)
            print(f"\n  [{name}] Top-2 결과:")
            for i, r in enumerate(results):
                print(f"    {i+1}. (score={r['score']:.2f}) {r['content'][:80]}...")

    # Threshold 비교
    print("\n" + "=" * 60)
    print("Threshold 비교 (쿼리: 'Chunking 전략의 종류를 알려줘')")
    print("=" * 60)
    query = "Chunking 전략의 종류를 알려줘"
    for thr in [0.0, 0.3, 0.5]:
        results = simple_search(query, chunks_semantic, k=10, threshold=thr)
        print(f"  threshold={thr}: {len(results)}개 결과")


if __name__ == "__main__":
    main()
