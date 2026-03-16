"""
강사 시연용: Threshold 없을 때 Hallucination 발생 예시

실제 LLM 호출 없이 패턴을 보여줍니다.
"""

import os


# 관련 없는 Chunk 예시 (노이즈)
NOISY_CHUNKS = [
    {
        "content": "오늘 점심 메뉴는 김치찌개입니다. 직원 식당은 12시부터 1시까지 운영합니다.",
        "score": 0.42,
        "reason": "완전히 무관한 내용"
    },
    {
        "content": "주차장 이용 안내: 방문객은 B2층을 이용해 주세요. 2시간 무료 제공.",
        "score": 0.38,
        "reason": "완전히 무관한 내용"
    },
    {
        "content": "RAG는 Retrieval-Augmented Generation의 약자입니다.",
        "score": 0.85,
        "reason": "관련 있는 내용"
    },
    {
        "content": "Chunking은 대용량 문서를 검색 단위로 분할하는 과정입니다.",
        "score": 0.78,
        "reason": "관련 있는 내용"
    },
]


def show_without_threshold():
    print("=" * 60)
    print("시나리오 1: Threshold 없음 (모든 결과 사용)")
    print("=" * 60)
    print("\n검색 결과 (threshold=0.0):")
    for i, chunk in enumerate(NOISY_CHUNKS):
        print(f"  {i+1}. [score={chunk['score']:.2f}] {chunk['content'][:60]}...")
        print(f"     → {chunk['reason']}")

    print("\n[LLM 프롬프트에 포함되는 내용]")
    print("  문서 1: 오늘 점심 메뉴는 김치찌개...")
    print("  문서 2: 주차장 이용 안내...")
    print("  문서 3: RAG는 Retrieval-Augmented...")
    print("  문서 4: Chunking은 대용량 문서를...")

    print("\n[Hallucination 위험]")
    print("  → 노이즈 문서가 LLM 답변에 영향을 줄 수 있음")
    print("  → '점심 메뉴'나 '주차장' 내용이 답변에 혼입될 가능성")
    print("  → 컨텍스트가 길어져 핵심 내용이 희석됨")


def show_with_threshold():
    print("\n" + "=" * 60)
    print("시나리오 2: Threshold=0.65 적용")
    print("=" * 60)
    threshold = 0.65
    filtered = [c for c in NOISY_CHUNKS if c["score"] >= threshold]

    print(f"\n검색 결과 (threshold={threshold}):")
    for i, chunk in enumerate(filtered):
        print(f"  {i+1}. [score={chunk['score']:.2f}] {chunk['content'][:60]}...")
        print(f"     → {chunk['reason']}")

    removed = [c for c in NOISY_CHUNKS if c["score"] < threshold]
    print(f"\n제거된 Chunk ({len(removed)}개):")
    for chunk in removed:
        print(f"  ✗ [score={chunk['score']:.2f}] {chunk['content'][:60]}...")

    print("\n[효과]")
    print("  → 노이즈 문서 제거")
    print("  → 관련 내용만 LLM에 전달")
    print("  → Hallucination 위험 감소")


def show_confidence_based_rejection():
    print("\n" + "=" * 60)
    print("시나리오 3: 신뢰도 기반 답변 거부")
    print("=" * 60)

    print("\n쿼리: '회사 주식 배당 정책은?'")
    print("→ 이 주제는 샘플 문서에 없는 내용입니다.")
    print("\n검색 결과:")
    print("  1. [score=0.32] RAG는 Retrieval-Augmented Generation...")
    print("  2. [score=0.28] Chunking은 대용량 문서를...")
    print("  3. [score=0.25] 오늘 점심 메뉴는 김치찌개...")

    print("\n[신뢰도 0.6 미만 → 답변 거부]")
    print("  → 답변: '죄송합니다. 해당 질문에 대한 신뢰할 수 있는 정보를 찾을 수 없습니다.'")
    print("  → Hallucination 방지: 잘못된 답변 대신 명확한 거부 응답")

    print("\n[Threshold 없으면?]")
    print("  → 낮은 관련도의 문서로 답변 생성 시도")
    print("  → '배당 정책은 3월에 발표되며 점심 식당에서 공지됩니다' 같은 엉터리 답변 위험")


def main():
    print("시연: Threshold 없을 때 Hallucination 발생 패턴")
    show_without_threshold()
    show_with_threshold()
    show_confidence_based_rejection()

    print("\n" + "=" * 60)
    print("핵심 교훈")
    print("=" * 60)
    print("1. Threshold 없으면 → 노이즈 문서가 LLM에 전달됨")
    print("2. Threshold 0.65~0.75 → 관련 문서만 필터링")
    print("3. 최대 점수 < 0.6 → 답변 거부가 잘못된 답변보다 낫다")
    print("4. 프롬프트에 '모르면 모른다고 하라' 지침 필수")


if __name__ == "__main__":
    main()
