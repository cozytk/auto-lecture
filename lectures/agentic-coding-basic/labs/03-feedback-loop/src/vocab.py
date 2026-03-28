#!/usr/bin/env python3
"""
단어장 앱 - 메인 CLI
영어 단어를 추가, 조회, 삭제하고 학습 기록을 관리합니다.
"""

import json
import os
from datetime import datetime

VOCAB_FILE = "vocab_data.json"
STATS_FILE = "stats_data.json"


def load_vocab() -> dict:
    """단어장 데이터를 파일에서 불러옵니다."""
    if os.path.exists(VOCAB_FILE):
        with open(VOCAB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_vocab(vocab: dict) -> None:
    """단어장 데이터를 파일에 저장합니다."""
    with open(VOCAB_FILE, "w", encoding="utf-8") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)


def load_stats() -> dict:
    """학습 통계 데이터를 파일에서 불러옵니다."""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_stats(stats: dict) -> None:
    """학습 통계 데이터를 파일에 저장합니다."""
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


def add_word(english: str, korean: str) -> bool:
    """단어를 단어장에 추가합니다."""
    vocab = load_vocab()
    if english in vocab:
        print(f"'{english}'는 이미 단어장에 있습니다.")
        return False
    vocab[english] = {
        "korean": korean,
        "added_at": datetime.now().isoformat(),
    }
    save_vocab(vocab)
    print(f"'{english} - {korean}' 추가 완료!")
    return True


def list_words() -> list:
    """단어장의 모든 단어를 반환합니다."""
    vocab = load_vocab()
    if not vocab:
        print("단어장이 비어 있습니다.")
        return []
    print(f"\n=== 단어장 ({len(vocab)}개) ===")
    words = []
    for english, data in vocab.items():
        korean = data["korean"]
        print(f"  {english} - {korean}")
        words.append((english, korean))
    return words


def delete_word(english: str) -> bool:
    """단어를 단어장에서 삭제합니다.

    버그: 단어를 삭제할 때 해당 단어의 학습 통계를 삭제하지 않아
    통계가 유령 데이터를 포함하게 됩니다.
    """
    vocab = load_vocab()
    if english not in vocab:
        print(f"'{english}'를 찾을 수 없습니다.")
        return False

    del vocab[english]
    save_vocab(vocab)

    # 버그: stats에서 해당 단어 기록을 삭제하지 않음
    # 올바른 코드:
    # stats = load_stats()
    # if english in stats:
    #     del stats[english]
    #     save_stats(stats)

    print(f"'{english}' 삭제 완료!")
    return True


def get_word_count() -> int:
    """현재 단어장의 단어 수를 반환합니다."""
    return len(load_vocab())


def main():
    """메인 CLI 진입점"""
    import sys

    if len(sys.argv) < 2:
        print("사용법:")
        print("  python vocab.py add <영어> <한국어>")
        print("  python vocab.py list")
        print("  python vocab.py delete <영어>")
        print("  python vocab.py quiz")
        print("  python vocab.py stats")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 4:
            print("사용법: python vocab.py add <영어> <한국어>")
            return
        add_word(sys.argv[2], sys.argv[3])

    elif command == "list":
        list_words()

    elif command == "delete":
        if len(sys.argv) < 3:
            print("사용법: python vocab.py delete <영어>")
            return
        delete_word(sys.argv[2])

    elif command == "quiz":
        from quiz import run_quiz
        run_quiz()

    elif command == "stats":
        from stats import show_stats
        show_stats()

    else:
        print(f"알 수 없는 명령어: {command}")


if __name__ == "__main__":
    main()
