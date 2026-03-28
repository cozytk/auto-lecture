"""분석기 테스트 스위트

에이전트가 생성한 테스트와 달리, 이 테스트는 실제 비즈니스 요구사항을 검증한다.
각 테스트는 독립적으로 실행되며, assert 메시지로 실패 원인을 명확히 표시한다.
"""

import os
import json
import tempfile
import sys

# solution 디렉토리를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analyzer.reader import read_csv, extract_numeric_column
from analyzer.statistics import compute_stats, group_by_category
from analyzer.outlier import detect_outliers
from analyzer.reporter import classify_grades, find_high_performers
from main import run


# ── 헬퍼 ────────────────────────────────────────────────────────────────────

def make_temp_csv(content: str) -> str:
    """임시 CSV 파일을 생성하고 경로를 반환한다."""
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8')
    f.write(content)
    f.close()
    return f.name


def cleanup(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)


# ── reader 테스트 ────────────────────────────────────────────────────────────

def test_read_csv_정상파일_읽기():
    """정상적인 CSV 파일을 올바르게 읽어야 한다."""
    csv_path = make_temp_csv("id,name,score\n1,홍길동,85.0\n2,김철수,90.0\n")
    try:
        rows = read_csv(csv_path)
        assert len(rows) == 2, f"행 수가 2여야 하지만 {len(rows)}임"
        assert rows[0]['name'] == '홍길동', "첫 번째 행의 name이 '홍길동'이어야 함"
        assert rows[1]['score'] == '90.0', "두 번째 행의 score가 '90.0'이어야 함"
    finally:
        cleanup(csv_path)


def test_read_csv_헤더만있는파일_빈리스트반환():
    """헤더만 있고 데이터 행이 없는 파일은 빈 리스트를 반환해야 한다."""
    csv_path = make_temp_csv("id,name,score\n")
    try:
        rows = read_csv(csv_path)
        assert rows == [], f"빈 리스트여야 하지만 {rows}임"
    finally:
        cleanup(csv_path)


def test_read_csv_존재하지않는파일_예외발생():
    """존재하지 않는 파일 경로는 FileNotFoundError를 발생시켜야 한다."""
    try:
        read_csv("/존재하지않는/경로/file.csv")
        assert False, "FileNotFoundError가 발생해야 함"
    except FileNotFoundError:
        pass


def test_extract_numeric_column_결측값_건너뜀():
    """결측값이나 빈 문자열은 변환하지 않고 건너뛰어야 한다."""
    rows = [
        {'score': '85.0'},
        {'score': ''},       # 빈 값
        {'score': 'N/A'},    # 변환 불가
        {'score': '92.5'},
    ]
    values = extract_numeric_column(rows, 'score')
    assert len(values) == 2, f"유효한 값이 2개여야 하지만 {len(values)}개임"
    assert values == [85.0, 92.5], f"값이 [85.0, 92.5]여야 하지만 {values}임"


# ── statistics 테스트 ────────────────────────────────────────────────────────

def test_compute_stats_기본통계_정확성():
    """평균, 중앙값, 표준편차가 수학적으로 정확해야 한다."""
    values = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    stats = compute_stats(values)
    assert stats['mean'] == 5.0, f"평균이 5.0이어야 하지만 {stats['mean']}임"
    assert stats['median'] == 4.5, f"중앙값이 4.5여야 하지만 {stats['median']}임"
    assert stats['std_dev'] == 2.0, f"표준편차가 2.0이어야 하지만 {stats['std_dev']}임"


def test_compute_stats_단일값_표준편차_0():
    """값이 하나면 표준편차는 0이어야 한다."""
    stats = compute_stats([42.0])
    assert stats['std_dev'] == 0.0, f"표준편차가 0.0이어야 하지만 {stats['std_dev']}임"
    assert stats['mean'] == 42.0
    assert stats['median'] == 42.0


def test_compute_stats_빈리스트_예외발생():
    """빈 리스트 입력 시 ValueError를 발생시켜야 한다."""
    try:
        compute_stats([])
        assert False, "ValueError가 발생해야 함"
    except ValueError:
        pass


def test_compute_stats_짝수개_중앙값():
    """짝수 개 데이터의 중앙값은 중간 두 값의 평균이어야 한다."""
    stats = compute_stats([1.0, 2.0, 3.0, 4.0])
    assert stats['median'] == 2.5, f"중앙값이 2.5여야 하지만 {stats['median']}임"


def test_group_by_category_부서별_그룹화():
    """부서별로 점수가 올바르게 그룹화되어야 한다."""
    rows = [
        {'department': 'engineering', 'score': '85.0'},
        {'department': 'marketing', 'score': '70.0'},
        {'department': 'engineering', 'score': '90.0'},
    ]
    groups = group_by_category(rows, 'department', 'score')
    assert 'engineering' in groups, "engineering 그룹이 있어야 함"
    assert sorted(groups['engineering']) == [85.0, 90.0], \
        f"engineering 점수가 [85.0, 90.0]이어야 하지만 {groups['engineering']}임"
    assert groups['marketing'] == [70.0]


# ── outlier 테스트 ────────────────────────────────────────────────────────────

def test_detect_outliers_명확한이상치_탐지():
    """분포에서 크게 벗어난 값은 이상치로 탐지되어야 한다."""
    # 85~95 범위의 정상 데이터 + 명확한 이상치 150
    rows = [{'score': str(v), 'name': f'사람{i}'} for i, v in
            enumerate([85, 87, 88, 90, 91, 92, 93, 94, 95, 150])]
    values = [float(r['score']) for r in rows]
    outliers = detect_outliers(rows, 'score', values)
    assert len(outliers) == 1, f"이상치가 1개여야 하지만 {len(outliers)}개임"
    assert outliers[0]['value'] == 150.0, f"이상치 값이 150이어야 하지만 {outliers[0]['value']}임"


def test_detect_outliers_정상분포_이상치없음():
    """균일한 분포에서는 이상치가 없어야 한다."""
    rows = [{'score': str(v), 'name': f'사람{i}'} for i, v in
            enumerate([80, 82, 84, 86, 88, 90, 92, 94])]
    values = [float(r['score']) for r in rows]
    outliers = detect_outliers(rows, 'score', values)
    assert len(outliers) == 0, f"이상치가 없어야 하지만 {outliers}임"


def test_detect_outliers_데이터부족_빈리스트():
    """데이터가 4개 미만이면 이상치 탐지를 건너뛰고 빈 리스트를 반환해야 한다."""
    rows = [{'score': '85', 'name': '사람1'}, {'score': '90', 'name': '사람2'}]
    values = [85.0, 90.0]
    outliers = detect_outliers(rows, 'score', values)
    assert outliers == [], f"빈 리스트여야 하지만 {outliers}임"


# ── reporter 테스트 ────────────────────────────────────────────────────────────

def test_classify_grades_등급_분류():
    """90+ A, 80+ B, 70+ C, 70미만 D로 정확히 분류해야 한다."""
    rows = [
        {'name': '최고', 'score': '95'},
        {'name': '우수', 'score': '85'},
        {'name': '보통', 'score': '75'},
        {'name': '미흡', 'score': '65'},
        {'name': '경계선', 'score': '90'},  # A 경계
    ]
    grades = classify_grades(rows)
    assert '최고' in grades['A'] and '경계선' in grades['A'], "90점은 A등급이어야 함"
    assert '우수' in grades['B'], "85점은 B등급이어야 함"
    assert '보통' in grades['C'], "75점은 C등급이어야 함"
    assert '미흡' in grades['D'], "65점은 D등급이어야 함"


def test_classify_grades_결측값_무시():
    """score가 없거나 변환 불가한 행은 등급 분류에서 무시되어야 한다."""
    rows = [
        {'name': '정상', 'score': '85'},
        {'name': '빈값', 'score': ''},
        {'name': '문자', 'score': 'abc'},
    ]
    grades = classify_grades(rows)
    total = sum(len(v) for v in grades.values())
    assert total == 1, f"유효한 등급이 1개여야 하지만 {total}개임"


def test_find_high_performers_기준충족():
    """점수 85 이상이고 나이 30 이상인 사람만 고성과자로 분류되어야 한다."""
    rows = [
        {'name': '고성과자', 'score': '90', 'age': '35'},   # 통과
        {'name': '점수낮음', 'score': '80', 'age': '35'},   # score 미달
        {'name': '나이젊음', 'score': '90', 'age': '25'},   # age 미달
        {'name': '경계선', 'score': '85', 'age': '30'},     # 정확히 기준값 통과
    ]
    result = find_high_performers(rows)
    assert '고성과자' in result, "고성과자는 결과에 있어야 함"
    assert '점수낮음' not in result, "점수 미달은 고성과자가 아니어야 함"
    assert '나이젊음' not in result, "나이 미달은 고성과자가 아니어야 함"
    assert '경계선' in result, "경계값 85/30은 고성과자 기준 충족이어야 함"


# ── 통합 테스트 ────────────────────────────────────────────────────────────────

def test_run_정상파일_완전분석():
    """정상 CSV로 run() 실행 시 모든 분석 결과가 포함된 딕셔너리를 반환해야 한다."""
    csv_content = (
        "id,name,age,score,salary,department\n"
        "1,홍길동,30,85.0,3500000,engineering\n"
        "2,김철수,25,70.0,2800000,marketing\n"
        "3,이영희,35,92.0,4500000,hr\n"
        "4,박민준,28,78.0,3200000,engineering\n"
        "5,최수진,40,88.0,5000000,hr\n"
    )
    csv_path = make_temp_csv(csv_content)
    out_path = csv_path + '_result.json'
    try:
        result = run(csv_path, out_path)
        assert result['total_records'] == 5, "레코드 수가 5여야 함"
        assert 'score' in result, "score 통계가 있어야 함"
        assert 'salary' in result, "salary 통계가 있어야 함"
        assert 'age' in result, "age 통계가 있어야 함"
        assert 'grades' in result, "등급 분류가 있어야 함"
        assert 'high_performers' in result, "고성과자 목록이 있어야 함"
        assert os.path.exists(out_path), "결과 JSON 파일이 생성되어야 함"
        with open(out_path, encoding='utf-8') as f:
            saved = json.load(f)
        assert saved['total_records'] == 5, "저장된 JSON의 레코드 수가 5여야 함"
    finally:
        cleanup(csv_path)
        cleanup(out_path)


def test_run_빈파일_예외발생():
    """데이터 행이 없는 파일로 run() 호출 시 ValueError가 발생해야 한다."""
    csv_path = make_temp_csv("id,name,age,score,salary,department\n")
    out_path = csv_path + '_result.json'
    try:
        run(csv_path, out_path)
        assert False, "ValueError가 발생해야 함"
    except ValueError:
        pass
    finally:
        cleanup(csv_path)
        cleanup(out_path)


# ── 테스트 실행 ────────────────────────────────────────────────────────────────

def run_all_tests():
    tests = [
        test_read_csv_정상파일_읽기,
        test_read_csv_헤더만있는파일_빈리스트반환,
        test_read_csv_존재하지않는파일_예외발생,
        test_extract_numeric_column_결측값_건너뜀,
        test_compute_stats_기본통계_정확성,
        test_compute_stats_단일값_표준편차_0,
        test_compute_stats_빈리스트_예외발생,
        test_compute_stats_짝수개_중앙값,
        test_group_by_category_부서별_그룹화,
        test_detect_outliers_명확한이상치_탐지,
        test_detect_outliers_정상분포_이상치없음,
        test_detect_outliers_데이터부족_빈리스트,
        test_classify_grades_등급_분류,
        test_classify_grades_결측값_무시,
        test_find_high_performers_기준충족,
        test_run_정상파일_완전분석,
        test_run_빈파일_예외발생,
    ]

    passed = 0
    failed = 0
    print("\n테스트 실행 중...\n")
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {test.__name__}")
            print(f"        {e}")
            failed += 1

    print(f"\n결과: {passed}개 통과 / {failed}개 실패 (총 {len(tests)}개)")
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
