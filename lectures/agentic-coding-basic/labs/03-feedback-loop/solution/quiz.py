#!/usr/bin/env python3
"""
퀴즈 기능 - 단어장을 기반으로 퀴즈를 진행합니다. (버그 수정 버전)
"""

import random
from datetime import datetime


def check_answer(user_answer: str, correct_answer: str) -> bool:
    """사용자의 답변과 정답을 비교합니다.

    수정: 대소문자를 무시하고 비교합니다.
    """
    # 버그 수정: .lower()로 변환 후 비교
    return user_answer.strip().lower() == correct_answer.strip().lower()


def run_quiz(word_list: list = None) -> dict:
    """퀴즈를 실행합니다."""
    from vocab import load_vocab

    if word_list is None:
        vocab = load_vocab()
        if not vocab:
            print("단어장이 비어 있습니다. 먼저 단어를 추가해주세요.")
            return {"correct": 0, "total": 0, "results": []}
        word_list = [(eng, data["korean"]) for eng, data in vocab.items()]

    if not word_list:
        return {"correct": 0, "total": 0, "results": []}

    random.shuffle(word_list)
    correct_count = 0
    results = []

    print(f"\n=== 퀴즈 시작 ({len(word_list)}문제) ===")
    print("한국어를 보고 영어 단어를 입력하세요.\n")

    for english, korean in word_list:
        print(f"문제: {korean}")
        user_input = input("답변: ").strip()

        is_correct = check_answer(user_input, english)
        if is_correct:
            print("정답!")
            correct_count += 1
        else:
            print(f"오답! 정답: {english}")

        results.append({
            "english": english,
            "korean": korean,
            "user_answer": user_input,
            "correct": is_correct,
        })

        _update_quiz_stats(english, is_correct)

    print(f"\n=== 퀴즈 완료 ===")
    print(f"결과: {correct_count}/{len(word_list)} 정답")

    return {
        "correct": correct_count,
        "total": len(word_list),
        "results": results,
    }


def _update_quiz_stats(english: str, is_correct: bool) -> None:
    """퀴즈 결과를 통계에 업데이트합니다."""
    from vocab import load_stats, save_stats

    stats = load_stats()
    if english not in stats:
        stats[english] = {
            "attempts": 0,
            "correct": 0,
            "last_attempt": None,
        }

    stats[english]["attempts"] += 1
    if is_correct:
        stats[english]["correct"] += 1
    stats[english]["last_attempt"] = datetime.now().isoformat()

    save_stats(stats)
