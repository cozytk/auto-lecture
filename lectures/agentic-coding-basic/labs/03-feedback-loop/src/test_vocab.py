#!/usr/bin/env python3
"""
단어장 앱 테스트 - 3개의 버그에 대응하는 테스트
테스트 자체는 올바르며, 버그는 모두 src/ 코드에 있습니다.
"""

import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# 현재 디렉토리를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestScoreCalculation(unittest.TestCase):
    """버그 1: stats.py의 타입 에러 - calculate_score에서 문자열 correct 처리"""

    def test_score_calculation_with_string_values(self):
        """correct 값이 문자열로 저장되어도 올바르게 점수를 계산해야 합니다.

        실제 JSON 역직렬화 과정에서 숫자가 문자열로 오는 경우를 처리해야 합니다.
        예: {"correct": "5", "attempts": 10} -> 50.0점
        """
        from stats import calculate_score

        # 정수로 저장된 경우 (정상 케이스)
        self.assertAlmostEqual(calculate_score(5, 10), 50.0)

        # 문자열로 저장된 경우 (버그가 있으면 TypeError 발생)
        try:
            result = calculate_score("5", 10)
            self.assertAlmostEqual(result, 50.0,
                msg="문자열 correct 값도 올바르게 처리해야 합니다.")
        except TypeError:
            self.fail(
                "calculate_score('5', 10)에서 TypeError 발생. "
                "int()로 변환하여 처리해야 합니다."
            )

    def test_score_zero_attempts(self):
        """시도 횟수가 0이면 0.0을 반환해야 합니다."""
        from stats import calculate_score
        self.assertEqual(calculate_score(0, 0), 0.0)

    def test_score_perfect(self):
        """모두 정답이면 100.0을 반환해야 합니다."""
        from stats import calculate_score
        self.assertAlmostEqual(calculate_score(10, 10), 100.0)


class TestCaseInsensitiveAnswer(unittest.TestCase):
    """버그 2: quiz.py의 대소문자 구분 로직 버그"""

    def test_case_insensitive_answer(self):
        """정답 판정은 대소문자를 구분하지 않아야 합니다.

        학생이 "Apple"을 입력했을 때 정답이 "apple"이어도 맞는 것으로 처리해야 합니다.
        """
        from quiz import check_answer

        # 동일한 값 - 반드시 정답
        self.assertTrue(check_answer("apple", "apple"))

        # 대문자 입력 - 정답으로 처리해야 함 (버그가 있으면 False 반환)
        self.assertTrue(check_answer("Apple", "apple"),
            msg="'Apple' 입력은 'apple'과 동일하게 처리해야 합니다.")

        # 모두 대문자 - 정답으로 처리해야 함
        self.assertTrue(check_answer("APPLE", "apple"),
            msg="'APPLE' 입력은 'apple'과 동일하게 처리해야 합니다.")

        # 명백히 틀린 답 - 오답
        self.assertFalse(check_answer("banana", "apple"))

    def test_whitespace_trimming(self):
        """앞뒤 공백은 제거하고 비교해야 합니다 (대소문자 무관)."""
        from quiz import check_answer

        # 공백 제거는 이미 .strip()으로 처리됨 - 소문자 기준으로 확인
        self.assertTrue(check_answer("  apple  ", "apple"),
            msg="앞뒤 공백을 제거하고 비교해야 합니다.")


class TestDeleteCleanStats(unittest.TestCase):
    """버그 3: vocab.py의 데이터 무결성 버그 - 단어 삭제 시 통계 미삭제"""

    def setUp(self):
        """테스트용 임시 디렉토리를 설정합니다."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """테스트 후 원래 디렉토리로 복귀하고 임시 파일을 정리합니다."""
        os.chdir(self.original_dir)
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _create_vocab_file(self, data: dict):
        """테스트용 단어장 파일을 생성합니다."""
        with open("vocab_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    def _create_stats_file(self, data: dict):
        """테스트용 통계 파일을 생성합니다."""
        with open("stats_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    def _load_stats_file(self) -> dict:
        """통계 파일을 읽습니다."""
        if not os.path.exists("stats_data.json"):
            return {}
        with open("stats_data.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def test_delete_cleans_stats(self):
        """단어를 삭제하면 해당 단어의 학습 통계도 함께 삭제되어야 합니다.

        단어장에서 'apple'을 삭제할 때, stats_data.json에서도
        'apple' 항목이 제거되어야 합니다.
        """
        from vocab import delete_word

        # 테스트 데이터 설정
        self._create_vocab_file({
            "apple": {"korean": "사과", "added_at": "2024-01-01T00:00:00"},
            "banana": {"korean": "바나나", "added_at": "2024-01-01T00:00:00"},
        })
        self._create_stats_file({
            "apple": {"attempts": 5, "correct": 3, "last_attempt": "2024-01-02T00:00:00"},
            "banana": {"attempts": 3, "correct": 2, "last_attempt": "2024-01-02T00:00:00"},
        })

        # apple 삭제
        result = delete_word("apple")
        self.assertTrue(result, "삭제 성공 시 True를 반환해야 합니다.")

        # 통계에서도 apple이 삭제되었는지 확인
        stats = self._load_stats_file()
        self.assertNotIn("apple", stats,
            msg="단어 삭제 시 해당 단어의 통계도 함께 삭제되어야 합니다. "
                "vocab.py의 delete_word()에서 stats도 업데이트하세요.")

        # banana 통계는 그대로 남아있어야 함
        self.assertIn("banana", stats,
            msg="삭제하지 않은 banana의 통계는 남아있어야 합니다.")

    def test_word_count_after_delete(self):
        """단어 삭제 후 단어 수가 올바르게 감소해야 합니다."""
        from vocab import delete_word, get_word_count

        self._create_vocab_file({
            "apple": {"korean": "사과", "added_at": "2024-01-01T00:00:00"},
            "banana": {"korean": "바나나", "added_at": "2024-01-01T00:00:00"},
        })

        self.assertEqual(get_word_count(), 2)
        delete_word("apple")
        self.assertEqual(get_word_count(), 1)


class TestVocabBasicFunctions(unittest.TestCase):
    """단어장 기본 기능 테스트 (버그 없음, 통과해야 함)"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_add_word(self):
        """단어 추가가 정상적으로 동작해야 합니다."""
        from vocab import add_word, load_vocab

        result = add_word("apple", "사과")
        self.assertTrue(result)

        vocab = load_vocab()
        self.assertIn("apple", vocab)
        self.assertEqual(vocab["apple"]["korean"], "사과")

    def test_add_duplicate_word(self):
        """중복 단어 추가는 실패해야 합니다."""
        from vocab import add_word

        add_word("apple", "사과")
        result = add_word("apple", "애플")
        self.assertFalse(result)

    def test_list_words_empty(self):
        """빈 단어장에서 list_words는 빈 리스트를 반환해야 합니다."""
        from vocab import list_words
        result = list_words()
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
