"""
I DO: RAG 파이프라인 구현 - 시연 코드

강사가 실행하며 시연합니다. 학생은 관찰하며 이해하세요.

핵심 관찰 포인트:
- RAG = Retrieval + Augmentation + Generation 3단계
- Embedding으로 의미 기반 검색 (키워드 아닌 의미 유사도)
- top_k 문서를 프롬프트에 포함하여 LLM이 참고
- "문서에 없는 내용은 답변하지 마세요" 지시가 할루시네이션 방지의 핵심
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

# 1단계: 문서 준비 (실제 환경에서는 PDF/DB에서 로드)
documents = [
    "환불 정책: 상품 수령 후 7일 이내 환불 가능합니다. 신선식품은 24시간, 전자제품은 14일 이내입니다.",
    "배송 안내: 일반 배송은 2~3 영업일 소요됩니다. 당일 배송은 오후 2시 이전 주문 시 적용됩니다.",
    "포인트 정책: 구매 금액의 1%가 적립됩니다. 1,000P 이상 사용 가능하며 유효기간은 12개월입니다.",
    "회원 등급: Silver(연 50만원) → Gold(연 100만원) → Platinum(연 200만원) 순으로 승급됩니다.",
    "교환 정책: 상품 불량이나 오배송의 경우 30일 이내 무료 교환 가능합니다. 단순 변심은 7일 이내입니다.",
]


def embed(texts: list[str]) -> list[list[float]]:
    """텍스트 목록을 벡터로 변환 (Embedding 단계)"""
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=texts,
    )
    return [item.embedding for item in response.data]


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """코사인 유사도 계산"""
    a = np.array(v1)
    b = np.array(v2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# 사전 처리: 문서 벡터화 (실제 환경에서는 Vector DB에 저장)
print("문서 임베딩 중...")
doc_vectors = embed(documents)
print(f"임베딩 완료: {len(documents)}개 문서\n")


def retrieve(query: str, top_k: int = 2) -> list[tuple[str, float]]:
    """질문과 가장 유사한 문서 top_k개 검색 (Retrieval 단계)"""
    query_vector = embed([query])[0]

    scored = []
    for doc, doc_vec in zip(documents, doc_vectors):
        sim = cosine_similarity(query_vector, doc_vec)
        scored.append((doc, sim))

    # 유사도 내림차순 정렬
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


def rag_answer(query: str, top_k: int = 2) -> str:
    """RAG 3단계: Retrieval → Augmentation → Generation"""

    # Retrieval: 관련 문서 검색
    retrieved = retrieve(query, top_k=top_k)

    print(f"[Retrieval] '{query}'에 대한 상위 {top_k}개 문서:")
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

    # Generation: LLM이 증강된 프롬프트로 답변 생성
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": augmented_prompt}],
        temperature=0.1,  # 사실 기반 답변을 위해 낮은 temperature
    )

    return response.choices[0].message.content


# 테스트: 다양한 질문과 top_k 비교
test_queries = [
    "전자제품은 몇 일 이내에 환불할 수 있나요?",
    "Gold 등급이 되려면 얼마나 구매해야 하나요?",
    "오늘 주문하면 내일 받을 수 있나요?",
    "재고가 얼마나 남아있나요?",  # 문서에 없는 정보
]

if __name__ == "__main__":
    print("=== RAG 파이프라인 시연 ===\n")

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"질문: {query}")
        answer = rag_answer(query, top_k=2)
        print(f"답변: {answer}")

    # top_k 비교 실험
    print(f"\n{'='*60}")
    print("\n[top_k 비교 실험]")
    query = "환불 정책에 대해 알려주세요"
    for k in [1, 2, 3]:
        print(f"\n--- top_k={k} ---")
        answer = rag_answer(query, top_k=k)
        print(f"답변: {answer}")
