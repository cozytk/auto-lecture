"""
WE DO: RAG 파이프라인 구현 - 함께 실습

강사와 함께 top_k 실험과 retrieve 함수를 완성합니다.
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

documents = [
    "환불 정책: 상품 수령 후 7일 이내 환불 가능합니다. 신선식품은 24시간, 전자제품은 14일 이내입니다.",
    "배송 안내: 일반 배송은 2~3 영업일 소요됩니다. 당일 배송은 오후 2시 이전 주문 시 적용됩니다.",
    "포인트 정책: 구매 금액의 1%가 적립됩니다. 1,000P 이상 사용 가능하며 유효기간은 12개월입니다.",
    "회원 등급: Silver(연 50만원) → Gold(연 100만원) → Platinum(연 200만원) 순으로 승급됩니다.",
    "교환 정책: 상품 불량이나 오배송의 경우 30일 이내 무료 교환 가능합니다. 단순 변심은 7일 이내입니다.",
]


def embed(texts: list[str]) -> list[list[float]]:
    """텍스트 목록을 벡터로 변환"""
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=texts,
    )
    return [item.embedding for item in response.data]


print("문서 임베딩 중...")
doc_vectors = embed(documents)
print(f"임베딩 완료: {len(documents)}개 문서\n")


def retrieve(query: str, top_k: int = 2) -> list[tuple[str, float]]:
    """질문과 가장 유사한 문서를 검색합니다.

    TODO: 아래 단계를 완성하세요
    1. query를 벡터로 변환 (embed 함수 사용)
    2. 각 문서 벡터와 코사인 유사도 계산
    3. 유사도 내림차순 정렬 후 top_k개 반환
    """
    # TODO 1: 질문을 벡터로 변환하세요
    query_vector = None  # embed([query])[0]

    scored = []
    for doc, doc_vec in zip(documents, doc_vectors):
        # TODO 2: 코사인 유사도를 계산하세요
        # 힌트: np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        sim = 0.0  # TODO: 계산 식으로 교체
        scored.append((doc, sim))

    # TODO 3: 유사도 내림차순 정렬 후 top_k 반환
    # scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


def rag_answer(query: str, top_k: int = 2) -> str:
    """RAG 파이프라인: Retrieval → Augmentation → Generation"""

    # Retrieval
    retrieved = retrieve(query, top_k=top_k)

    print(f"[Retrieval] 상위 {top_k}개 문서:")
    for i, (doc, score) in enumerate(retrieved, 1):
        print(f"  {i}. (유사도: {score:.3f}) {doc[:50]}...")

    # Augmentation: 검색된 문서를 프롬프트에 포함
    context = "\n".join(
        f"[문서{i}] {doc}" for i, (doc, _) in enumerate(retrieved, 1)
    )

    augmented_prompt = (
        f"참고 문서:\n{context}\n\n"
        f"위 문서만 참고하여 답변하세요. "
        f"문서에 없는 내용은 '문서에서 확인할 수 없습니다'라고 답변하세요.\n\n"
        f"질문: {query}"
    )

    # Generation
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": augmented_prompt}],
        temperature=0.1,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print("=== WE DO: top_k 비교 실험 ===\n")

    query = "전자제품 환불 기한이 어떻게 되나요?"

    # TODO: top_k를 1, 2, 3으로 바꾸어가며 답변 품질 비교
    for k in [1, 2, 3]:
        print(f"\n--- top_k={k} ---")
        print(f"질문: {query}")
        answer = rag_answer(query, top_k=k)
        print(f"답변: {answer}")
        print()

    # TODO: retrieve가 완성되면 아래 질문도 테스트해보세요
    # print("\n=== 추가 테스트 ===")
    # print(rag_answer("Gold 회원이 되려면?"))
    # print(rag_answer("재고 현황은?"))  # 문서에 없는 정보 테스트
