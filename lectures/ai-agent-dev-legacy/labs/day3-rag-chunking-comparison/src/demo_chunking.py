"""
강사 시연용: Chunking 전략별 Chunk 수·크기 분포 비교
"""

import re
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))


def load_doc() -> str:
    path = os.path.join(os.path.dirname(__file__), "sample_doc.md")
    with open(path, encoding="utf-8") as f:
        return f.read()


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
        sections.append({
            "header": header_text,
            "content": f"# {header_text}\n\n{content}",
            "level": len(match.group(1))
        })
    return sections


def print_stats(name: str, chunks: list) -> None:
    if not chunks:
        print(f"  [{name}] 결과 없음")
        return
    lengths = [len(c if isinstance(c, str) else c.get("content", "")) for c in chunks]
    import statistics
    print(f"\n[{name}]")
    print(f"  Chunk 수    : {len(chunks)}개")
    print(f"  평균 길이   : {statistics.mean(lengths):.0f} 문자")
    print(f"  최소 길이   : {min(lengths)} 문자")
    print(f"  최대 길이   : {max(lengths)} 문자")
    print(f"  중앙값 길이 : {statistics.median(lengths):.0f} 문자")


def main():
    doc = load_doc()
    print("=" * 60)
    print("시연: Chunking 전략별 Chunk 수·크기 분포")
    print("=" * 60)
    print(f"원본 문서: {len(doc)} 문자")

    chunks_fixed = fixed_size_chunk(doc, size=300, overlap=50)
    chunks_semantic = semantic_chunk(doc, max_size=400)
    chunks_header = header_based_chunk(doc)

    print_stats("Fixed-size (size=300, overlap=50)", chunks_fixed)
    print_stats("Semantic   (max_size=400)", chunks_semantic)
    print_stats("Header-based", chunks_header)

    # 문장 분리 예시 시연
    print("\n" + "=" * 60)
    print("Fixed-size: 문장 중간 분리 예시")
    print("=" * 60)
    if len(chunks_fixed) >= 2:
        print(f"Chunk 1 끝:\n...{chunks_fixed[0][-80:]}")
        print(f"\nChunk 2 시작:\n{chunks_fixed[1][:80]}...")

    print("\n" + "=" * 60)
    print("Header-based: 섹션 목록")
    print("=" * 60)
    for sec in chunks_header:
        print(f"  {'  ' * (sec.get('level', 1) - 1)}[H{sec.get('level', 1)}] {sec['header']}")


if __name__ == "__main__":
    main()
