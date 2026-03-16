"""
YOU DO 정답: RAG 파이프라인 구현

학생이 과제 완료 후 참고하는 정답 코드입니다.
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

# 도메인: 쇼핑몰 고객 FAQ (5개 문서)
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


# 문서 사전 벡터화
print("문서 임베딩 중...")
doc_vectors = embed(documents)
print(f"임베딩 완료: {len(documents)}개 문서\n")


def retrieve(query: str, top_k: int = 3) -> list[tuple[str, float]]:
    """질문과 가장 유사한 문서 top_k개를 반환합니다."""
    query_vector = embed([query])[0]

    scored = []
    for doc, doc_vec in zip(documents, doc_vectors):
        a = np.array(query_vector)
        b = np.array(doc_vec)
        sim = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        scored.append((doc, sim))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


def rag_answer(query: str, top_k: int = 3) -> str:
    """RAG 파이프라인 전체 실행: Retrieval → Augmentation → Generation"""

    # 1. Retrieval
    retrieved = retrieve(query, top_k=top_k)

    print(f"[Retrieval] '{query}'에 대한 상위 {top_k}개 문서:")
    for i, (doc, score) in enumerate(retrieved, 1):
        print(f"  {i}. (유사도: {score:.3f}) {doc[:50]}...")

    # 2. Augmentation
    context = "\n".join(
        f"[문서{i}] {doc}" for i, (doc, _) in enumerate(retrieved, 1)
    )
    augmented_prompt = (
        f"참고 문서:\n{context}\n\n"
        "위 문서만 참고하여 답변하세요. "
        "문서에 없는 내용은 '문서에서 확인할 수 없습니다'라고 답변하세요.\n\n"
        f"질문: {query}"
    )

    # 3. Generation
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": augmented_prompt}],
        temperature=0.1,
    )
    return response.choices[0].message.content


# 검증용 테스트
test_queries = [
    "전자제품은 몇 일 이내에 환불할 수 있나요?",
    "Gold 등급이 되려면 얼마나 구매해야 하나요?",
    "재고가 얼마나 남아있나요?",  # 문서에 없는 정보
]

if __name__ == "__main__":
    print("=== RAG 파이프라인 정답 코드 ===\n")

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"질문: {query}")
        answer = rag_answer(query, top_k=2)
        print(f"답변: {answer}")

    # top_k 비교 실험
    print(f"\n{'='*60}")
    print("\n[top_k 비교 실험]")
    query = "환불 및 교환 정책을 알려주세요"
    for k in [1, 2, 3]:
        print(f"\n--- top_k={k} ---")
        answer = rag_answer(query, top_k=k)
        print(f"답변: {answer}")
