# 분석 설정값 (매직 넘버를 상수로 추출)

# IQR 이상치 탐지 배수
IQR_MULTIPLIER = 1.5

# IQR 사분위수 위치
Q1_PERCENTILE = 0.25
Q3_PERCENTILE = 0.75

# 성과 등급 임계값
GRADE_A_THRESHOLD = 90.0
GRADE_B_THRESHOLD = 80.0
GRADE_C_THRESHOLD = 70.0

# 고성과자 기준
HIGH_PERFORMER_SCORE = 85.0
HIGH_PERFORMER_AGE = 30

# 분석 대상 컬럼
NUMERIC_COLUMNS = ['score', 'salary', 'age']
CATEGORY_COLUMN = 'department'
NAME_COLUMN = 'name'

# 기본 출력 파일명
DEFAULT_OUTPUT_FILE = 'result.json'
