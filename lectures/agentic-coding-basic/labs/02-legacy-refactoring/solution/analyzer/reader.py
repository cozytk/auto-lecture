"""CSV 파일 읽기 모듈"""

import csv
from typing import List, Dict


def read_csv(file_path: str) -> List[Dict[str, str]]:
    """CSV 파일을 읽어 딕셔너리 리스트로 반환한다.

    Args:
        file_path: 읽을 CSV 파일 경로

    Returns:
        각 행을 딕셔너리로 표현한 리스트

    Raises:
        FileNotFoundError: 파일이 존재하지 않을 때
        ValueError: 파일 형식이 올바르지 않을 때 (헤더 없음 등)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV 파일에 헤더가 없습니다: {file_path}")
        rows = [row for row in reader]
    return rows


def extract_numeric_column(rows: List[Dict[str, str]], column: str) -> List[float]:
    """행 리스트에서 특정 컬럼의 숫자 값을 추출한다. 변환 실패한 값은 건너뛴다.

    Args:
        rows: CSV 행 리스트
        column: 추출할 컬럼명

    Returns:
        유효한 숫자 값 리스트
    """
    values = []
    for row in rows:
        raw = row.get(column, '').strip()
        if raw:
            try:
                values.append(float(raw))
            except ValueError:
                pass
    return values
