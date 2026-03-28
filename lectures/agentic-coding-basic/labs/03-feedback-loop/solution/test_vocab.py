#!/usr/bin/env python3
"""
단어장 앱 테스트 - solution 디렉토리용
solution/ 코드를 사용하므로 모든 테스트가 통과해야 합니다.
"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestScoreCalculation(unittest.TestCase):
    """stats.py의 calculate_score 테스트"""

    def test_score_calculation_with_string_values(self):
        """correct 값이 문자열로 저장되어도 올바르게 점수를 계산해야 합니다."""
        from stats import calculate_score

        self.assertAlmostEqual(calculate_score(5, 10), 50.0)

        try:
            result = calculate_score("5", 10)
            self.assertAlmostEqual(result, 50.0)
        except TypeError:
            self.fail("calculate_score('5', 10)에서 TypeError 발생.")

    def test_score_zero_attempts(self):
        from stats import calculate_score
        self.assertEqual(calculate_score(0, 0), 0.0)

    def test_score_perfect(self):
        from stats import calculate_score
        self.assertAlmostEqual(calculate_score(10, 10), 100.0)


class TestCaseInsensitiveAnswer(unittest.TestCase):
    """quiz.py의 check_answer 테스트"""

    def test_case_insensitive_answer(self):
        """정답 판정은 대소문자를 구분하지 않아야 합니다."""
        from quiz import check_answer

        self.assertTrue(check_answer("apple", "apple"))
        self.assertTrue(check_answer("Apple", "apple"))
        self.assertTrue(check_answer("APPLE", "apple"))
        self.assertFalse(check_answer("banana", "apple"))

    def test_case_insensitive_with_spaces(self):
        from quiz import check_answer
        self.assertTrue(check_answer("  Apple  ", "apple"))


class TestDeleteCleanStats(unittest.TestCase):
    """vocab.py의 delete_word 데이터 무결성 테스트"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _create_vocab_file(self, data: dict):
        with open("vocab_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    def _create_stats_file(self, data: dict):
        with open("stats_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    def _load_stats_file(self) -> dict:
        if not os.path.exists("stats_data.json"):
            return {}
        with open("stats_data.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def test_delete_cleans_stats(self):
        """단어를 삭제하면 해당 단어의 학습 통계도 함께 삭제되어야 합니다."""
        from vocab import delete_word

        self._create_vocab_file({
            "apple": {"korean": "사과", "added_at": "2024-01-01T00:00:00"},
            "banana": {"korean": "바나나", "added_at": "2024-01-01T00:00:00"},
        })
        self._create_stats_file({
            "apple": {"attempts": 5, "correct": 3, "last_attempt": "2024-01-02T00:00:00"},
            "banana": {"attempts": 3, "correct": 2, "last_attempt": "2024-01-02T00:00:00"},
        })

        result = delete_word("apple")
        self.assertTrue(result)

        stats = self._load_stats_file()
        self.assertNotIn("apple", stats)
        self.assertIn("banana", stats)

    def test_word_count_after_delete(self):
        from vocab import delete_word, get_word_count

        self._create_vocab_file({
            "apple": {"korean": "사과", "added_at": "2024-01-01T00:00:00"},
            "banana": {"korean": "바나나", "added_at": "2024-01-01T00:00:00"},
        })

        self.assertEqual(get_word_count(), 2)
        delete_word("apple")
        self.assertEqual(get_word_count(), 1)


class TestVocabBasicFunctions(unittest.TestCase):
    """단어장 기본 기능 테스트"""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_add_word(self):
        from vocab import add_word, load_vocab
        result = add_word("apple", "사과")
        self.assertTrue(result)
        vocab = load_vocab()
        self.assertIn("apple", vocab)
        self.assertEqual(vocab["apple"]["korean"], "사과")

    def test_add_duplicate_word(self):
        from vocab import add_word
        add_word("apple", "사과")
        result = add_word("apple", "애플")
        self.assertFalse(result)

    def test_list_words_empty(self):
        from vocab import list_words
        result = list_words()
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
