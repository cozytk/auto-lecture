import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent
LEGACY_PATH = ROOT / "src" / "legacy_analyzer.py"
SAMPLE_CSV = ROOT / "src" / "data" / "sample_data.csv"
EDGE_CASE_CSV = ROOT / "src" / "data" / "edge_case.csv"
EMPTY_CSV = ROOT / "src" / "data" / "empty.csv"


def load_legacy_module(monkeypatch, tmp_path, bootstrap_csv=SAMPLE_CSV):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", [str(LEGACY_PATH), str(bootstrap_csv)])

    spec = importlib.util.spec_from_file_location(
        "legacy_analyzer_under_test", LEGACY_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_sample_data_results_match_expected_statistics(monkeypatch, tmp_path):
    module = load_legacy_module(monkeypatch, tmp_path)
    result = module.results

    assert result["file"] == str(SAMPLE_CSV)
    assert result["total_records"] == 25

    assert result["score"] == {
        "mean": 83.3,
        "median": 85.5,
        "std_dev": 8.49,
        "min": 65.2,
        "max": 96.1,
        "outliers": [],
    }
    assert result["salary"] == {
        "mean": 3788000.0,
        "median": 3500000.0,
        "std_dev": 850562.17,
        "min": 2600000.0,
        "max": 5600000.0,
        "outliers": [],
    }
    assert result["age"] == {
        "mean": 32.2,
        "median": 30.0,
        "std_dev": 5.98,
    }
    assert result["department_avg_score"] == {
        "engineering": 87.35454545454546,
        "marketing": 79.375,
        "hr": 81.10000000000001,
    }
    assert result["grades"] == {
        "A": ["이영희", "한지현", "강동원", "전지현", "송혜교", "아이유"],
        "B": [
            "김철수",
            "최수진",
            "윤미래",
            "신민아",
            "손예진",
            "현빈",
            "김태희",
            "이민호",
            "박보검",
            "BTS진",
        ],
        "C": ["박민준", "오승환", "임서연", "류준열", "이병헌", "원빈", "수지"],
        "D": ["정대호", "공유"],
    }
    assert result["high_performers"] == [
        "이영희",
        "최수진",
        "전지현",
        "김태희",
        "아이유",
    ]


def test_writes_json_report_to_configured_output_file(monkeypatch, tmp_path):
    module = load_legacy_module(monkeypatch, tmp_path)
    output_path = tmp_path / "custom-report.json"

    module.results = {}
    module.outputFile = str(output_path)
    module.analyze_data(str(SAMPLE_CSV))

    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved == module.results
    assert saved["score"]["mean"] == 83.3
    assert saved["salary"]["median"] == 3500000.0


def test_invalid_numeric_rows_raise_value_error(monkeypatch, tmp_path):
    module = load_legacy_module(monkeypatch, tmp_path)

    module.results = {}
    with pytest.raises(ValueError):
        module.analyze_data(str(EDGE_CASE_CSV))


def test_empty_csv_raises_zero_division_error(monkeypatch, tmp_path):
    module = load_legacy_module(monkeypatch, tmp_path)

    module.results = {}
    with pytest.raises(ZeroDivisionError):
        module.analyze_data(str(EMPTY_CSV))
