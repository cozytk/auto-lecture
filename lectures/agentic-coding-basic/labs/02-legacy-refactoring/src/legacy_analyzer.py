import csv
import json
import sys
import math

# 전역변수들
data = []
results = {}
fileName = ""
outputFile = "result.json"

# 오래된 주석: 2019년 인턴이 작성한 분석 스크립트
# TODO: 나중에 정리하기 (3년째 미완)

def analyze_data(file_path):
    global data, results, fileName, outputFile

    fileName = file_path

    # 파일 읽기
    f = open(file_path, 'r', encoding='utf-8')
    reader = csv.DictReader(f)

    rows = []
    for row in reader:
        rows.append(row)

    f.close()

    # score 데이터 추출 (점수 분석)
    scoreList = []
    for i in range(len(rows)):
        r = rows[i]
        scoreList.append(float(r['score']))

    # 평균 계산
    total = 0
    for i in range(len(scoreList)):
        total = total + scoreList[i]
    avg = total / len(scoreList)

    # 중앙값 계산
    sorted_scores = sorted(scoreList)
    n = len(sorted_scores)
    if n % 2 == 0:
        median_val = (sorted_scores[n//2 - 1] + sorted_scores[n//2]) / 2
    else:
        median_val = sorted_scores[n//2]

    # 표준편차 계산
    variance_sum = 0
    for i in range(len(scoreList)):
        variance_sum = variance_sum + (scoreList[i] - avg) ** 2
    variance = variance_sum / len(scoreList)
    std_dev = math.sqrt(variance)

    # 이상치 탐지 (IQR 방식)
    q1_idx = int(n * 0.25)
    q3_idx = int(n * 0.75)
    Q1 = sorted_scores[q1_idx]
    Q3 = sorted_scores[q3_idx]
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers_score = []
    for i in range(len(scoreList)):
        if scoreList[i] < lower_bound or scoreList[i] > upper_bound:
            outliers_score.append({'index': i, 'value': scoreList[i], 'name': rows[i]['name']})

    # salary 데이터 추출 (급여 분석)
    salaryList = []
    for i in range(len(rows)):
        r = rows[i]
        salaryList.append(float(r['salary']))

    # 평균 계산 (급여)
    total2 = 0
    for i in range(len(salaryList)):
        total2 = total2 + salaryList[i]
    avg2 = total2 / len(salaryList)

    # 중앙값 계산 (급여)
    sorted_salary = sorted(salaryList)
    n2 = len(sorted_salary)
    if n2 % 2 == 0:
        median_salary = (sorted_salary[n2//2 - 1] + sorted_salary[n2//2]) / 2
    else:
        median_salary = sorted_salary[n2//2]

    # 표준편차 계산 (급여)
    variance_sum2 = 0
    for i in range(len(salaryList)):
        variance_sum2 = variance_sum2 + (salaryList[i] - avg2) ** 2
    variance2 = variance_sum2 / len(salaryList)
    std_dev2 = math.sqrt(variance2)

    # 이상치 탐지 급여 (IQR)
    q1_idx2 = int(n2 * 0.25)
    q3_idx2 = int(n2 * 0.75)
    Q1_s = sorted_salary[q1_idx2]
    Q3_s = sorted_salary[q3_idx2]
    IQR_s = Q3_s - Q1_s
    lower_s = Q1_s - 1.5 * IQR_s
    upper_s = Q3_s + 1.5 * IQR_s

    outliers_salary = []
    for i in range(len(salaryList)):
        if salaryList[i] < lower_s or salaryList[i] > upper_s:
            outliers_salary.append({'index': i, 'value': salaryList[i], 'name': rows[i]['name']})

    # age 분석
    ageList = []
    for i in range(len(rows)):
        r = rows[i]
        ageList.append(float(r['age']))

    # 평균 계산 (나이)
    total3 = 0
    for i in range(len(ageList)):
        total3 = total3 + ageList[i]
    avg3 = total3 / len(ageList)

    # 중앙값 계산 (나이)
    sorted_age = sorted(ageList)
    n3 = len(sorted_age)
    if n3 % 2 == 0:
        median_age = (sorted_age[n3//2 - 1] + sorted_age[n3//2]) / 2
    else:
        median_age = sorted_age[n3//2]

    # 표준편차 (나이)
    variance_sum3 = 0
    for i in range(len(ageList)):
        variance_sum3 = variance_sum3 + (ageList[i] - avg3) ** 2
    variance3 = variance_sum3 / len(ageList)
    std_dev3 = math.sqrt(variance3)

    # 부서별 평균 점수
    dept_scores = {}
    for i in range(len(rows)):
        dept = rows[i]['department']
        sc = float(rows[i]['score'])
        if dept not in dept_scores:
            dept_scores[dept] = []
        dept_scores[dept].append(sc)

    dept_avg = {}
    for dept in dept_scores:
        s = 0
        for x in dept_scores[dept]:
            s += x
        dept_avg[dept] = s / len(dept_scores[dept])

    # 성과 등급 분류 (매직 넘버)
    grade_A = []
    grade_B = []
    grade_C = []
    grade_D = []

    for i in range(len(rows)):
        sc = float(rows[i]['score'])
        name = rows[i]['name']
        if sc >= 90:
            grade_A.append(name)
        elif sc >= 80:
            grade_B.append(name)
        elif sc >= 70:
            grade_C.append(name)
        else:
            grade_D.append(name)

    # 고성과자 정의: 점수 85 이상 AND 재직연수 환산 나이 30 이상 (임의 기준)
    high_performers = []
    for i in range(len(rows)):
        sc = float(rows[i]['score'])
        age_val = float(rows[i]['age'])
        if sc >= 85 and age_val >= 30:
            high_performers.append(rows[i]['name'])

    # 결과 출력
    print("=" * 50)
    print(f"파일: {fileName}")
    print(f"총 레코드 수: {len(rows)}")
    print("=" * 50)

    print("\n[점수 통계]")
    print(f"  평균:     {avg:.2f}")
    print(f"  중앙값:   {median_val:.2f}")
    print(f"  표준편차: {std_dev:.2f}")
    print(f"  최솟값:   {min(scoreList):.2f}")
    print(f"  최댓값:   {max(scoreList):.2f}")

    print("\n[점수 이상치]")
    if len(outliers_score) == 0:
        print("  없음")
    else:
        for o in outliers_score:
            print(f"  {o['name']}: {o['value']}")

    print("\n[급여 통계]")
    print(f"  평균:     {avg2:,.0f}원")
    print(f"  중앙값:   {median_salary:,.0f}원")
    print(f"  표준편차: {std_dev2:,.0f}원")
    print(f"  최솟값:   {min(salaryList):,.0f}원")
    print(f"  최댓값:   {max(salaryList):,.0f}원")

    print("\n[급여 이상치]")
    if len(outliers_salary) == 0:
        print("  없음")
    else:
        for o in outliers_salary:
            print(f"  {o['name']}: {o['value']:,.0f}원")

    print("\n[나이 통계]")
    print(f"  평균:     {avg3:.1f}세")
    print(f"  중앙값:   {median_age:.1f}세")
    print(f"  표준편차: {std_dev3:.1f}세")

    print("\n[부서별 평균 점수]")
    for dept in dept_avg:
        print(f"  {dept}: {dept_avg[dept]:.2f}")

    print("\n[성과 등급]")
    print(f"  A등급 (90+): {len(grade_A)}명 - {', '.join(grade_A)}")
    print(f"  B등급 (80+): {len(grade_B)}명 - {', '.join(grade_B)}")
    print(f"  C등급 (70+): {len(grade_C)}명 - {', '.join(grade_C)}")
    print(f"  D등급 (70미만): {len(grade_D)}명 - {', '.join(grade_D)}")

    print("\n[고성과자 (점수 85+ & 나이 30+)]")
    print(f"  {', '.join(high_performers) if high_performers else '없음'}")

    # 결과를 딕셔너리에 저장
    results['file'] = fileName
    results['total_records'] = len(rows)
    results['score'] = {
        'mean': round(avg, 2),
        'median': round(median_val, 2),
        'std_dev': round(std_dev, 2),
        'min': min(scoreList),
        'max': max(scoreList),
        'outliers': outliers_score
    }
    results['salary'] = {
        'mean': round(avg2, 2),
        'median': round(median_salary, 2),
        'std_dev': round(std_dev2, 2),
        'min': min(salaryList),
        'max': max(salaryList),
        'outliers': outliers_salary
    }
    results['age'] = {
        'mean': round(avg3, 2),
        'median': round(median_age, 2),
        'std_dev': round(std_dev3, 2)
    }
    results['department_avg_score'] = dept_avg
    results['grades'] = {
        'A': grade_A,
        'B': grade_B,
        'C': grade_C,
        'D': grade_D
    }
    results['high_performers'] = high_performers

    # JSON으로 저장
    out = open(outputFile, 'w', encoding='utf-8')
    json.dump(results, out, ensure_ascii=False, indent=2)
    out.close()

    print(f"\n결과 저장: {outputFile}")
    print("=" * 50)


# 메인 실행
if len(sys.argv) < 2:
    print("사용법: python3 legacy_analyzer.py <csv파일경로>")
    sys.exit(1)

analyze_data(sys.argv[1])
