"""
RAG 파이프라인 (ChromaDB)

문서를 로드하고, Chunk로 분할하고, ChromaDB에 색인한 뒤,
유사도 검색을 수행하는 RAG 파이프라인이다.

TODO: 프로젝트에 맞게 아래 항목을 수정하세요.
  1. load_documents()에 실제 문서 로드 로직 추가
  2. Chunk 크기/오버랩 조정 (config.py에서 설정)
  3. 검색 파라미터 튜닝 (top_k, 유사도 임계값)
  4. (선택) metadata 필터 추가
"""

import os
from typing import Optional

import chromadb
from chromadb.utils import embedding_functions

from config import (
    CHROMA_COLLECTION_NAME,
    CHROMA_PERSIST_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    RETRIEVAL_TOP_K,
    OPENAI_API_KEY,
)


# ============================================================
# 1. 문서 로드
# ============================================================
def load_documents(source_path: str = "./data/documents") -> list[dict]:
    """문서를 로드한다.

    TODO: 프로젝트에 맞는 문서 로드 로직을 구현하세요.

    Returns:
        list[dict]: [{"content": "...", "metadata": {"source": "파일명", ...}}, ...]
    """
    documents = []

    if not os.path.exists(source_path):
        print(f"문서 경로가 존재하지 않습니다: {source_path}")
        print("data/documents/ 디렉토리를 생성하고 문서를 추가하세요.")
        return documents

    for filename in os.listdir(source_path):
        filepath = os.path.join(source_path, filename)

        if not os.path.isfile(filepath):
            continue

        # 텍스트 파일 로드
        if filename.endswith((".txt", ".md")):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            documents.append({
                "content": content,
                "metadata": {"source": filename, "type": "text"},
            })

    print(f"총 {len(documents)}개 문서 로드 완료")
    return documents


# ============================================================
# 2. 문서 Chunking
# ============================================================
def chunk_documents(
    documents: list[dict],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[dict]:
    """문서를 Chunk 단위로 분할한다.

    Args:
        documents: 원본 문서 목록
        chunk_size: Chunk 크기 (문자 수)
        chunk_overlap: Chunk 간 오버랩 (문자 수)

    Returns:
        list[dict]: Chunk 목록 [{"content": "...", "metadata": {...}}, ...]
    """
    chunks = []

    for doc in documents:
        text = doc["content"]
        metadata = doc["metadata"]

        # 간단한 문자 기반 Chunking
        start = 0
        chunk_index = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunks.append({
                "content": chunk_text,
                "metadata": {
                    **metadata,
                    "chunk_index": chunk_index,
                    "start_char": start,
                    "end_char": min(end, len(text)),
                },
            })

            start += chunk_size - chunk_overlap
            chunk_index += 1

    print(f"총 {len(chunks)}개 Chunk 생성 완료 (크기: {chunk_size}, 오버랩: {chunk_overlap})")
    return chunks


# ============================================================
# 3. ChromaDB 색인
# ============================================================
def get_collection(
    collection_name: str = CHROMA_COLLECTION_NAME,
    persist_dir: str = CHROMA_PERSIST_DIR,
):
    """ChromaDB 컬렉션을 가져온다 (없으면 생성)."""
    # 임베딩 함수 설정
    if OPENAI_API_KEY:
        ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=OPENAI_API_KEY,
            model_name="text-embedding-3-small",
        )
    else:
        # API 키가 없으면 기본 임베딩 사용
        ef = embedding_functions.DefaultEmbeddingFunction()

    # ChromaDB 클라이언트 생성
    client = chromadb.PersistentClient(path=persist_dir)

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=ef,
    )

    return collection


def index_documents(chunks: list[dict], collection_name: str = CHROMA_COLLECTION_NAME):
    """Chunk를 ChromaDB에 색인한다."""
    collection = get_collection(collection_name)

    # 기존 데이터 확인
    existing_count = collection.count()
    if existing_count > 0:
        print(f"기존 색인 {existing_count}건이 있습니다. 건너뜁니다.")
        print("재색인하려면 data/chroma_db 디렉토리를 삭제하세요.")
        return

    # 색인 실행
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    documents = [chunk["content"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    # ChromaDB는 한 번에 최대 5461개까지 추가 가능
    batch_size = 5000
    for i in range(0, len(ids), batch_size):
        collection.add(
            ids=ids[i:i + batch_size],
            documents=documents[i:i + batch_size],
            metadatas=metadatas[i:i + batch_size],
        )

    print(f"총 {len(chunks)}건 색인 완료")


# ============================================================
# 4. 유사도 검색
# ============================================================
def search_documents(
    query: str,
    top_k: int = RETRIEVAL_TOP_K,
    collection_name: str = CHROMA_COLLECTION_NAME,
    where_filter: Optional[dict] = None,
) -> list[dict]:
    """쿼리와 유사한 문서를 검색한다.

    Args:
        query: 검색 쿼리 (자연어)
        top_k: 반환할 최대 결과 수
        collection_name: ChromaDB 컬렉션 이름
        where_filter: metadata 필터 (예: {"source": "api-docs.md"})

    Returns:
        list[dict]: 검색 결과 [{"content": "...", "metadata": {...}, "distance": 0.x}, ...]
    """
    collection = get_collection(collection_name)

    if collection.count() == 0:
        print("색인된 문서가 없습니다. index_documents()를 먼저 실행하세요.")
        return []

    # 검색 실행
    query_params = {
        "query_texts": [query],
        "n_results": top_k,
    }
    if where_filter:
        query_params["where"] = where_filter

    results = collection.query(**query_params)

    # 결과 정리
    search_results = []
    for i in range(len(results["ids"][0])):
        search_results.append({
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i] if results.get("distances") else None,
        })

    return search_results


# ============================================================
# 5. 전체 파이프라인 실행
# ============================================================
def build_rag_pipeline(source_path: str = "./data/documents"):
    """RAG 파이프라인을 구축한다 (로드 → Chunk → 색인)."""
    print("=== RAG 파이프라인 구축 시작 ===")

    # 문서 로드
    documents = load_documents(source_path)
    if not documents:
        print("로드할 문서가 없습니다.")
        return

    # Chunking
    chunks = chunk_documents(documents)

    # 색인
    index_documents(chunks)

    print("=== RAG 파이프라인 구축 완료 ===")


if __name__ == "__main__":
    # RAG 파이프라인 테스트
    print("1. RAG 파이프라인 구축")
    build_rag_pipeline()

    print("\n2. 검색 테스트")
    results = search_documents("테스트 검색 쿼리")
    if results:
        for i, r in enumerate(results):
            print(f"  [{i+1}] (거리: {r['distance']:.4f}) {r['content'][:100]}...")
    else:
        print("  검색 결과가 없습니다.")
