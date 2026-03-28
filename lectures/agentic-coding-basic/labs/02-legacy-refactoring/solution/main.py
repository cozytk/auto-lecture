"""리팩토링된 데이터 분석기 진입점"""

import sys
from analyzer.reader import read_csv, extract_numeric_column
from analyzer.statistics import compute_stats, group_by_category
from analyzer.outlier import detect_outliers
from analyzer.reporter import (
    classify_grades,
    find_high_performers,
    print_report,
    save_report,
)
from config import DEFAULT_OUTPUT_FILE, CATEGORY_COLUMN


def run(file_path: str, output_path: str = DEFAULT_OUTPUT_FILE) -> dict:
    """CSV 파일을 분석하고 결과를 반환한다.

    Args:
        file_path: 입력 CSV 파일 경로
        output_path: 결과 JSON 저장 경로

    Returns:
        분석 결과 딕셔너리
    """
    rows = read_csv(file_path)
    if not rows:
        raise ValueError(f"데이터가 없습니다: {file_path}")

    score_values = extract_numeric_column(rows, 'score')
    salary_values = extract_numeric_column(rows, 'salary')
    age_values = extract_numeric_column(rows, 'age')

    score_stats = compute_stats(score_values)
    salary_stats = compute_stats(salary_values)
    age_stats = compute_stats(age_values)

    score_outliers = detect_outliers(rows, 'score', score_values)
    salary_outliers = detect_outliers(rows, 'salary', salary_values)

    dept_groups = group_by_category(rows, CATEGORY_COLUMN, 'score')
    dept_avg = {dept: round(sum(v) / len(v), 2) for dept, v in dept_groups.items()}

    grades = classify_grades(rows)
    high_performers = find_high_performers(rows)

    print_report(
        file_path=file_path,
        total=len(rows),
        score_stats=score_stats,
        salary_stats=salary_stats,
        age_stats=age_stats,
        score_outliers=score_outliers,
        salary_outliers=salary_outliers,
        dept_avg=dept_avg,
        grades=grades,
        high_performers=high_performers,
    )

    report = {
        'file': file_path,
        'total_records': len(rows),
        'score': {**score_stats, 'outliers': score_outliers},
        'salary': {**salary_stats, 'outliers': salary_outliers},
        'age': age_stats,
        'department_avg_score': dept_avg,
        'grades': grades,
        'high_performers': high_performers,
    }

    save_report(report, output_path)
    return report


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("사용법: python3 main.py <csv파일경로> [출력파일경로]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_FILE
    run(input_file, output_file)
