#!/usr/bin/env python3
"""
학습 통계 - 단어별 학습 현황을 분석하고 표시합니다.
"""


def calculate_score(correct: int, attempts: int) -> float:
    """정답률을 0~100 사이의 점수로 계산합니다.

    버그: correct가 문자열로 저장된 경우를 처리하지 않아
    타입 에러 또는 잘못된 비교가 발생합니다.
    문자열 "5"와 정수 0을 비교하면 파이썬에서는 에러가 발생하지 않지만
    산술 연산에서 TypeError가 발생합니다.
    """
    if attempts == 0:
        return 0.0
    # 버그: correct가 문자열일 때 나눗셈에서 TypeError 발생
    return (correct / attempts) * 100
    # 올바른 코드:
    # return (int(correct) / int(attempts)) * 100


def get_weak_words(stats: dict, threshold: float = 60.0) -> list:
    """취약 단어 목록을 반환합니다 (정답률이 threshold 미만인 단어).

    Args:
        stats: 단어별 통계 딕셔너리
        threshold: 취약 단어 기준 정답률 (기본값 60%)

    Returns:
        [(영어, 정답률), ...] 형태의 취약 단어 목록
    """
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

    # 단어장에 없는 유령 통계 표시
    ghost_words = [w for w in stats if w not in vocab]
    if ghost_words:
        print(f"\n[주의] 삭제된 단어의 기록이 남아있음: {', '.join(ghost_words)}")
