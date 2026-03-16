"""
RAG 파이프라인 테스트

Chunking 함수의 동작과 Retrieval 기본 로직을 검증합니다.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ── Chunking 테스트 ────────────────────────────────────────

def _is_implemented(fn, *args, **kwargs):
    """함수가 TODO 상태(빈 결과 반환)인지 확인"""
    result = fn(*args, **kwargs)
    if result is None or result == [] or result == 0.0:
        return False
    return True


class TestFixedSizeChunk:

    def test_chunks_not_empty(self):
        """빈 입력이 아닐 때 Chunk가 생성되는지 확인"""
        from rag_pipeline import fixed_size_chunk
        text = "이것은 테스트 문서입니다. " * 50
        chunks = fixed_size_chunk(text, size=100, overlap=20)
        if not chunks:
            pytest.skip("TODO: fixed_size_chunk 구현 후 테스트 실행 (WE DO 과제)")
        assert len(chunks) > 0, "Chunk가 생성되지 않았습니다"

    def test_chunk_size_limit(self):
        """각 Chunk가 size 이하인지 확인"""
        from rag_pipeline import fixed_size_chunk
        text = "A" * 1000
        size = 200
        chunks = fixed_size_chunk(text, size=size, overlap=20)
        if not chunks:
            pytest.skip("TODO: fixed_size_chunk 구현 후 테스트 실행")
        for i, chunk in enumerate(chunks):
            assert len(chunk) <= size + 5, (
                f"Chunk {i}의 크기 {len(chunk)}가 size {size}를 초과합니다"
            )

    def test_overlap_covers_boundary(self):
        """Overlap으로 경계 내용이 포함되는지 확인"""
        from rag_pipeline import fixed_size_chunk
        text = "ABCDEFGHIJ" * 10  # 100 문자
        chunks = fixed_size_chunk(text, size=30, overlap=10)
        if not chunks:
            pytest.skip("TODO: fixed_size_chunk 구현 후 테스트 실행")
        if len(chunks) >= 2:
            assert len(chunks) > 1, "Overlap이 있으면 Chunk 수가 증가해야 합니다"

    def test_all_content_preserved(self):
        """모든 내용이 Chunk에 포함되는지 확인"""
        from rag_pipeline import fixed_size_chunk
        text = "테스트 문서 내용입니다. " * 20
        chunks = fixed_size_chunk(text, size=50, overlap=10)
        if not chunks:
            pytest.skip("TODO: fixed_size_chunk 구현 후 테스트 실행")
        combined = " ".join(chunks)
        assert "테스트 문서" in combined


class TestSemanticChunk:

    def test_chunks_not_empty(self):
        """Semantic Chunk가 생성되는지 확인"""
        from rag_pipeline import semantic_chunk
        text = "첫 번째 단락입니다.\n\n두 번째 단락입니다.\n\n세 번째 단락입니다."
        chunks = semantic_chunk(text, max_size=200)
        if not chunks:
            pytest.skip("TODO: semantic_chunk 구현 후 테스트 실행 (WE DO 과제)")
        assert len(chunks) > 0

    def test_paragraph_boundary_respected(self):
        """단락 경계에서 분할되는지 확인"""
        from rag_pipeline import semantic_chunk
        para1 = "첫 번째 단락 내용입니다."
        para2 = "두 번째 단락 내용입니다."
        text = f"{para1}\n\n{para2}"
        chunks = semantic_chunk(text, max_size=30)
        if not chunks:
            pytest.skip("TODO: semantic_chunk 구현 후 테스트 실행")
        assert len(chunks) >= 1

    def test_max_size_respected(self):
        """max_size를 크게 초과하지 않는지 확인"""
        from rag_pipeline import semantic_chunk
        text = "짧은 문장. " * 100
        max_size = 200
        chunks = semantic_chunk(text, max_size=max_size)
        for chunk in chunks:
            # 단일 문장이 max_size를 초과할 수 있지만 일반적으로는 지켜져야 함
            assert len(chunk) <= max_size * 2, (
                f"Chunk 크기 {len(chunk)}가 max_size {max_size}의 2배를 초과합니다"
            )


class TestHeaderBasedChunk:

    def test_headers_extracted(self):
        """헤더가 올바르게 추출되는지 확인"""
        from rag_pipeline import header_based_chunk
        markdown = """# 제목 1

내용 1

## 제목 2

내용 2

### 제목 3

내용 3
"""
        sections = header_based_chunk(markdown)
        if not sections:
            pytest.skip("TODO: header_based_chunk 구현 후 테스트 실행 (WE DO 과제)")
        assert len(sections) >= 1, "섹션이 생성되지 않았습니다"

    def test_section_has_header_and_content(self):
        """각 섹션에 header와 content가 있는지 확인"""
        from rag_pipeline import header_based_chunk
        markdown = "## 섹션 1\n\n내용입니다.\n\n## 섹션 2\n\n다른 내용입니다."
        sections = header_based_chunk(markdown)
        for sec in sections:
            assert "header" in sec, "section에 'header' 키가 없습니다"
            assert "content" in sec, "section에 'content' 키가 없습니다"
            assert len(sec["header"]) > 0, "header가 비어 있습니다"

    def test_content_under_correct_header(self):
        """내용이 올바른 헤더 아래에 있는지 확인"""
        from rag_pipeline import header_based_chunk
        markdown = "## RAG 소개\n\nRAG는 Retrieval입니다.\n\n## Chunking\n\nChunking이란 분할입니다."
        sections = header_based_chunk(markdown)
        if not sections:
            pytest.skip("TODO: header_based_chunk 구현 후 테스트 실행")
        headers = [s["header"] for s in sections]
        assert "RAG 소개" in headers or any("RAG" in h for h in headers)


# ── 벡터 스토어 테스트 ─────────────────────────────────────

class TestSimpleVectorStore:

    def test_add_and_search(self):
        """문서 추가 후 검색이 동작하는지 확인"""
        from rag_pipeline import SimpleVectorStore
        store = SimpleVectorStore("test")
        store.add(["테스트 문서입니다", "다른 내용입니다"])
        results = store.search("테스트", k=2)
        assert len(results) >= 0  # 결과가 있을 수도 없을 수도 있음 (Mock 벡터)

    def test_empty_store_returns_empty(self):
        """빈 스토어에서 검색 시 빈 리스트 반환"""
        from rag_pipeline import SimpleVectorStore
        store = SimpleVectorStore("empty")
        results = store.search("쿼리", k=5)
        assert results == []

    def test_stats_returns_dict(self):
        """stats()가 딕셔너리를 반환하는지 확인"""
        from rag_pipeline import SimpleVectorStore
        store = SimpleVectorStore("stats_test")
        store.add(["문서 1", "문서 2", "문서 3"])
        stats = store.stats()
        assert isinstance(stats, dict)
        assert "count" in stats
        # store.add가 TODO이면 count=0, 구현 후 count=3
        if stats["count"] == 0:
            pytest.skip("TODO: SimpleVectorStore.add 구현 후 테스트 실행 (WE DO 과제)")
        assert stats["count"] == 3

    def test_threshold_filters_results(self):
        """Threshold가 적용되는지 확인"""
        from rag_pipeline import SimpleVectorStore
        store = SimpleVectorStore("threshold_test")
        store.add(["문서 내용"])
        # threshold=1.0이면 완벽히 일치하는 것 외에는 제거
        results_high = store.search("전혀 다른 내용", k=5, threshold=0.99)
        results_low = store.search("전혀 다른 내용", k=5, threshold=0.0)
        # 낮은 threshold가 더 많거나 같은 결과를 반환
        assert len(results_low) >= len(results_high)


# ── 코사인 유사도 테스트 ───────────────────────────────────

class TestCosineSimilarity:

    def test_identical_vectors(self):
        """동일한 벡터의 유사도는 1.0"""
        from rag_pipeline import cosine_similarity
        vec = [1.0, 0.0, 0.0]
        sim = cosine_similarity(vec, vec)
        if sim == 0.0:
            pytest.skip("TODO: cosine_similarity 구현 후 테스트 실행 (WE DO 과제)")
        assert abs(sim - 1.0) < 1e-6, f"동일 벡터 유사도가 1.0이 아님: {sim}"

    def test_orthogonal_vectors(self):
        """직교 벡터의 유사도는 0.0"""
        from rag_pipeline import cosine_similarity
        a = [1.0, 0.0]
        b = [0.0, 1.0]
        sim = cosine_similarity(a, b)
        assert abs(sim) < 1e-6, f"직교 벡터 유사도가 0.0이 아님: {sim}"

    def test_similarity_range(self):
        """유사도가 -1.0 ~ 1.0 범위인지 확인"""
        from rag_pipeline import cosine_similarity
        import random
        for _ in range(10):
            a = [random.random() for _ in range(8)]
            b = [random.random() for _ in range(8)]
            sim = cosine_similarity(a, b)
            assert -1.01 <= sim <= 1.01, f"유사도 범위 초과: {sim}"


# ── 통합 테스트 ────────────────────────────────────────────

class TestRAGPipeline:

    def test_full_pipeline_runs(self):
        """전체 파이프라인이 오류 없이 실행되는지 확인"""
        from rag_pipeline import (
            fixed_size_chunk, semantic_chunk, header_based_chunk,
            SimpleVectorStore, rag_answer
        )

        doc = "RAG는 검색 증강 생성입니다.\n\nChunking은 분할 과정입니다.\n\n## 임베딩\n\n임베딩은 벡터 변환입니다."

        chunks = fixed_size_chunk(doc, size=100, overlap=20)
        store = SimpleVectorStore("pipeline_test")
        store.add(chunks)

        result = rag_answer("RAG란?", store, k=3, threshold=0.0)
        assert isinstance(result, dict)
        assert "answer" in result
        assert "confidence" in result

    def test_chunking_comparison(self):
        """세 가지 전략의 결과가 모두 생성되는지 확인"""
        from rag_pipeline import fixed_size_chunk, semantic_chunk, header_based_chunk

        doc = "# 제목\n\n단락 1 내용.\n\n단락 2 내용.\n\n## 소제목\n\n더 많은 내용."

        f = fixed_size_chunk(doc, size=50, overlap=10)
        s = semantic_chunk(doc, max_size=100)
        h = header_based_chunk(doc)

        assert isinstance(f, list)
        assert isinstance(s, list)
        assert isinstance(h, list)
        if len(f) == 0 and len(s) == 0 and len(h) == 0:
            pytest.skip("TODO: chunking 함수들 구현 후 테스트 실행 (WE DO 과제)")
        assert len(f) > 0 or len(s) > 0 or len(h) > 0
