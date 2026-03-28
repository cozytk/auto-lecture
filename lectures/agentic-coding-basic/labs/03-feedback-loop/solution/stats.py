#!/usr/bin/env python3
"""
학습 통계 - 단어별 학습 현황을 분석하고 표시합니다. (버그 수정 버전)
"""


def calculate_score(correct: int, attempts: int) -> float:
    """정답률을 0~100 사이의 점수로 계산합니다.

    수정: correct와 attempts를 int()로 명시적 변환하여
    문자열 값도 올바르게 처리합니다.
    """
    if int(attempts) == 0:
        return 0.0
    # 버그 수정: int()로 변환하여 문자열도 처리
    return (int(correct) / int(attempts)) * 100


def get_weak_words(stats: dict, threshold: float = 60.0) -> list:
    """취약 단어 목록을 반환합니다 (정답률이 threshold 미만인 단어)."""
    weak_words = []
    for english, data in stats.items():
        attempts = data.get("attempts", 0)
        correct = data.get("correct", 0)
        score = calculate_score(correct, attempts)
        if score < threshold:
            weak_words.append((english, score))
    return sorted(weak_words, key=lambda x: x[1])


def get_stats_summary(stats: dict) -> dict:
    """전체 학습 통계 요약을 반환합니다."""
    if not stats:
        return {
            "total_words": 0,
            "total_attempts": 0,
            "total_correct": 0,
            "average_score": 0.0,
        }

    total_attempts = sum(d.get("attempts", 0) for d in stats.values())
    total_correct = sum(d.get("correct", 0) for d in stats.values())

    return {
        "total_words": len(stats),
        "total_attempts": total_attempts,
        "total_correct": total_correct,
        "average_score": calculate_score(total_correct, total_attempts),
    }


def show_stats() -> None:
    """학습 통계를 화면에 출력합니다."""
    from vocab import load_vocab, load_stats

    vocab = load_vocab()
    stats = load_stats()

    if not stats:
        print("아직 학습 기록이 없습니다. 퀴즈를 먼저 풀어보세요.")
        return

    summary = get_stats_summary(stats)
    print(f"\n=== 학습 통계 ===")
    print(f"학습한 단어 수: {summary['total_words']}개")
    print(f"총 시도 횟수: {summary['total_attempts']}회")
    print(f"총 정답 수: {summary['total_correct']}개")
    print(f"평균 정답률: {summary['average_score']:.1f}%")

    weak_words = get_weak_words(stats)
    if weak_words:
        print(f"\n취약 단어 (정답률 60% 미만):")
        for english, score in weak_words:
            korean = vocab.get(english, {}).get("korean", "???")
            print(f"  {english} ({korean}): {score:.1f}%")
