"""결과 출력 및 저장 모듈"""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import Dict, Any, List
import config


def classify_grades(rows: List[Dict[str, str]], score_col: str = 'score') -> Dict[str, List[str]]:
    """점수 기준으로 성과 등급을 분류한다."""
    grades: Dict[str, List[str]] = {'A': [], 'B': [], 'C': [], 'D': []}
    for row in rows:
        raw = row.get(score_col, '').strip()
        if not raw:
            continue
        try:
            score = float(raw)
        except ValueError:
            continue
        name = row.get(config.NAME_COLUMN, '')
        if score >= config.GRADE_A_THRESHOLD:
            grades['A'].append(name)
        elif score >= config.GRADE_B_THRESHOLD:
            grades['B'].append(name)
        elif score >= config.GRADE_C_THRESHOLD:
            grades['C'].append(name)
        else:
            grades['D'].append(name)
    return grades


def find_high_performers(rows: List[Dict[str, str]]) -> List[str]:
    """고성과자 기준(점수 85+, 나이 30+)에 해당하는 이름 목록을 반환한다."""
    result = []
    for row in rows:
        try:
            score = float(row.get('score', '') or 0)
            age = float(row.get('age', '') or 0)
        except ValueError:
            continue
        if score >= config.HIGH_PERFORMER_SCORE and age >= config.HIGH_PERFORMER_AGE:
            result.append(row.get(config.NAME_COLUMN, ''))
    return result


def print_report(
    file_path: str,
    total: int,
    score_stats: Dict[str, Any],
    salary_stats: Dict[str, Any],
    age_stats: Dict[str, Any],
    score_outliers: list,
    salary_outliers: list,
    dept_avg: Dict[str, float],
    grades: Dict[str, List[str]],
    high_performers: List[str],
) -> None:
    """분석 결과를 콘솔에 출력한다."""
    print("=" * 50)
    print(f"파일: {file_path}")
    print(f"총 레코드 수: {total}")
    print("=" * 50)

    _print_stats_section("점수 통계", score_stats, "점", score_outliers)
    _print_stats_section("급여 통계", salary_stats, "원", salary_outliers, currency=True)

    print("\n[나이 통계]")
    print(f"  평균:     {age_stats['mean']:.1f}세")
    print(f"  중앙값:   {age_stats['median']:.1f}세")
    print(f"  표준편차: {age_stats['std_dev']:.1f}세")

    print("\n[부서별 평균 점수]")
    for dept, avg in dept_avg.items():
        print(f"  {dept}: {avg:.2f}")

    print("\n[성과 등급]")
    for grade, names in grades.items():
        threshold = {
            'A': '90+', 'B': '80+', 'C': '70+', 'D': '70미만'
        }[grade]
        print(f"  {grade}등급 ({threshold}): {len(names)}명 - {', '.join(names)}")

    print("\n[고성과자 (점수 85+ & 나이 30+)]")
    print(f"  {', '.join(high_performers) if high_performers else '없음'}")


def _print_stats_section(
    title: str,
    stats: Dict[str, Any],
    unit: str,
    outliers: list,
    currency: bool = False,
) -> None:
    fmt = "{:,.0f}" if currency else "{:.2f}"
    print(f"\n[{title}]")
    print(f"  평균:     {fmt.format(stats['mean'])}{unit}")
    print(f"  중앙값:   {fmt.format(stats['median'])}{unit}")
    print(f"  표준편차: {fmt.format(stats['std_dev'])}{unit}")
    print(f"  최솟값:   {fmt.format(stats['min'])}{unit}")
    print(f"  최댓값:   {fmt.format(stats['max'])}{unit}")

    label = f"[{title.split()[0]} 이상치]"
    print(f"\n{label}")
    if not outliers:
        print("  없음")
    else:
        for o in outliers:
            print(f"  {o['name']}: {fmt.format(o['value'])}{unit}")


def save_report(report: Dict[str, Any], output_path: str) -> None:
    """분석 결과를 JSON 파일로 저장한다."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n결과 저장: {output_path}")
    print("=" * 50)
