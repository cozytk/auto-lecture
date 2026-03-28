"""IQR 기반 이상치 탐지 모듈"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List, Dict, Any
import config


def detect_outliers(
    rows: List[Dict[str, str]],
    column: str,
    values: List[float],
    name_col: str = config.NAME_COLUMN,
) -> List[Dict[str, Any]]:
    """IQR 방식으로 이상치를 탐지한다.

    Args:
        rows: 원본 CSV 행 리스트 (이름 참조용)
        column: 분석 컬럼명
        values: 해당 컬럼의 숫자 값 리스트 (rows와 동일 순서)
        name_col: 이상치 레코드 식별에 사용할 이름 컬럼

    Returns:
        이상치 레코드 리스트. 각 항목은 index, name, value 키를 포함.
    """
    if len(values) < 4:
        return []

    q1, q3 = _compute_iqr_bounds(values)
    iqr = q3 - q1
    lower = q1 - config.IQR_MULTIPLIER * iqr
    upper = q3 + config.IQR_MULTIPLIER * iqr

    outliers = []
    valid_idx = 0
    for i, row in enumerate(rows):
        raw = row.get(column, '').strip()
        if not raw:
            continue
        try:
            value = float(raw)
        except ValueError:
            continue

        if value < lower or value > upper:
            outliers.append({
                'index': i,
                'name': row.get(name_col, ''),
                'value': value,
            })
        valid_idx += 1

    return outliers


def _compute_iqr_bounds(values: List[float]):
    """Q1, Q3 값을 반환한다."""
    sorted_values = sorted(values)
    n = len(sorted_values)
    q1 = sorted_values[int(n * config.Q1_PERCENTILE)]
    q3 = sorted_values[int(n * config.Q3_PERCENTILE)]
    return q1, q3
