"""
YOU DO: RAG 파이프라인 구현 - 독립 과제

본인의 도메인에 맞는 문서 5개 이상을 준비하고
Retrieval → Augmentation → Generation 전체 파이프라인을 구현하세요.
"""

import os
import numpy as np
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")
EMBED_MODEL = "openai/text-embedding-3-small"

# TODO: 본인 도메인에 맞는 문서를 5개 이상 준비하세요
# 예시: 사내 FAQ, 제품 매뉴얼, 정책 문서 등
# 각 문서는 하나의 주제를 명확히 다루는 1~3문장으로 작성하세요
documents = [
    # TODO: 문서 5개 이상 추가
    # "문서 1: ...",
    # "문서 2: ...",
    # "문서 3: ...",
    # "문서 4: ...",
    # "문서 5: ...",
]


def embed(texts: list[str]) -> list[list[float]]:
    """텍스트 목록을 벡터로 변환합니다."""
    # TODO: OpenRouter Embedding API를 호출하여 벡터를 반환하세요
    # 힌트: client.embeddings.create(model=EMBED_MODEL, input=texts)
    return []


# TODO: 문서 벡터화
# doc_vectors = embed(documents)


def retrieve(query: str, top_k: int = 3) -> list[tuple[str, float]]:
    """질문과 가장 유사한 문서 top_k개를 반환합니다.

    반환 형식: [(문서내용, 유사도점수), ...]
    """
    # TODO: 구현하세요
    # 1. query를 벡터로 변환
    # 2. 각 문서 벡터와 코사인 유사도 계산
    #    cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    # 3. 유사도 내림차순 정렬
    # 4. 상위 top_k개 반환
    return []


def rag_answer(query: str, top_k: int = 3) -> str:
    """RAG 파이프라인 전체를 실행합니다.

    단계:
    1. Retrieval: retrieve() 호출로 관련 문서 검색
    2. Augmentation: 검색된 문서를 프롬프트에 포함
    3. Generation: LLM으로 최종 답변 생성
    """
    # TODO: 구현하세요

    # 1. Retrieval
    # retrieved = retrieve(query, top_k=top_k)

    # 2. Augmentation
    # context = "\n".join(f"[문서{i}] {doc}" for i, (doc, _) in enumerate(retrieved, 1))
    # augmented_prompt = (
    #     f"참고 문서:\n{context}\n\n"
    #     "위 문서만 참고하여 답변하세요. "
    #     "문서에 없는 내용은 '문서에서 확인할 수 없습니다'라고 답변하세요.\n\n"
    #     f"질문: {query}"
    # )

    # 3. Generation
    # response = client.chat.completions.create(
    #     model=MODEL,
    #     messages=[{"role": "user", "content": augmented_prompt}],
    #     temperature=0.1,
    # )
    # return response.choices[0].message.content

    return "TODO: RAG 파이프라인 구현 필요"


# 검증용 테스트 입력 (본인 도메인에 맞게 수정하세요)
test_queries = [
    # TODO: 문서 내용에 맞는 질문 3개를 추가하세요
    # "질문 1: 문서에서 답을 찾을 수 있는 질문",
    # "질문 2: 다른 문서에서 답을 찾을 수 있는 질문",
    # "질문 3: 문서에 없는 정보를 묻는 질문 (확인 불가 테스트)",
]

if __name__ == "__main__":
    print("=== YOU DO: RAG 파이프라인 테스트 ===\n")

    if not documents:
        print("ERROR: documents 목록을 먼저 채워주세요!")
    elif not test_queries:
        print("ERROR: test_queries 목록을 먼저 채워주세요!")
    else:
        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"질문: {query}")
            answer = rag_answer(query)
            print(f"답변: {answer}")
