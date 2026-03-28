"""기초 통계 계산 모듈"""

import math
from typing import List, Dict


def compute_stats(values: List[float]) -> Dict[str, float]:
    """숫자 리스트에 대한 기초 통계를 계산한다.

    Args:
        values: 분석할 숫자 리스트

    Returns:
        mean, median, std_dev, min, max 키를 포함한 딕셔너리

    Raises:
        ValueError: 리스트가 비어 있을 때
    """
    if not values:
        raise ValueError("통계 계산에 필요한 데이터가 없습니다.")

    n = len(values)
    mean = sum(values) / n
    median = _compute_median(values)
    std_dev = _compute_std_dev(values, mean)

    return {
        'mean': round(mean, 2),
        'median': round(median, 2),
        'std_dev': round(std_dev, 2),
        'min': min(values),
        'max': max(values),
    }


def _compute_median(values: List[float]) -> float:
    """중앙값을 계산한다."""
    sorted_values = sorted(values)
    n = len(sorted_values)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_values[mid - 1] + sorted_values[mid]) / 2
    return sorted_values[mid]


def _compute_std_dev(values: List[float], mean: float) -> float:
    """모표준편차를 계산한다."""
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(variance)


def group_by_category(rows: list, category_col: str, value_col: str) -> Dict[str, List[float]]:
    """카테고리 컬럼 기준으로 숫자 값을 그룹화한다.

    Args:
        rows: CSV 행 리스트
        category_col: 그룹 기준 컬럼명
        value_col: 집계할 숫자 컬럼명

    Returns:
        카테고리 -> 값 리스트 딕셔너리
    """
    groups: Dict[str, List[float]] = {}
    for row in rows:
        category = row.get(category_col, '').strip()
        raw = row.get(value_col, '').strip()
        if not category or not raw:
            continue
        try:
            value = float(raw)
        except ValueError:
            continue
        groups.setdefault(category, []).append(value)
    return groups
