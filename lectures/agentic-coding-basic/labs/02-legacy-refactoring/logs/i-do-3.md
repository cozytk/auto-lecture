# legacy_analyzer.py 단위 테스트 작성

**Session ID:** ses_2ffa2f3f9ffeM0cKdpp1684KMc
**Created:** 3/18/2026, 6:53:11 PM
**Updated:** 3/18/2026, 6:55:32 PM

---

## User

@src/legacy_analyzer.py 파일에 대한 단위 테스트를 작성해줘.
파일명은 test_legacy.py로 저장해줘.

---

## Assistant (Build · gpt-5.4 · 6.8s)

_Thinking:_

**Planning unit tests**

I need to write unit tests for `test_legacy.py` based on the user's request, so I'll start by inspecting the repository to figure out the testing framework in use. It looks like the code has top-level execution and calls `sys.exit` if certain conditions aren't met, which complicates things a bit. I might have to adjust `sys.argv` during testing. I'll explore the file structure and consider creating tests that focus on the script's behavior. Using subprocesses could also help eliminate import side effects. Let's get to work on this!

**Tool: glob**

**Input:**
```json
{
  "pattern": "**/*",
  "path": "/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring"
}
```

**Output:**
```
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/README.md
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/src/result.json
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/__pycache__/main.cpython-314.pyc
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/analyzer/__pycache__/reporter.cpython-314.pyc
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/__pycache__/config.cpython-314.pyc
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/analyzer/__pycache__/outlier.cpython-314.pyc
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/analyzer/__pycache__/statistics.cpython-314.pyc
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/analyzer/__pycache__/reader.cpython-314.pyc
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/analyzer/__pycache__/__init__.cpython-314.pyc
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/__pycache__/test_analyzer.cpython-314.pyc
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/analyzer/reporter.py
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/analyzer/outlier.py
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/artifacts/quality-checklist.md
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/Justfile
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/test_analyzer.py
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/main.py
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/analyzer/statistics.py
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/analyzer/reader.py
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/analyzer/__init__.py
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/config.py
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/src/legacy_analyzer.py
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/src/data/empty.csv
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/src/data/edge_case.csv
/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/src/data/sample_data.csv
```

**Tool: grep**

**Input:**
```json
{
  "pattern": "pytest|unittest",
  "path": "/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring",
  "include": "*.*"
}
```

**Output:**
```
No files found
```

---

## Assistant (Build · gpt-5.4 · 4.8s)

_Thinking:_



**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/test_analyzer.py"
}
```

**Output:**
```
<path>/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/solution/test_analyzer.py</path>
<type>file</type>
<content>1: """분석기 테스트 스위트
2: 
3: 에이전트가 생성한 테스트와 달리, 이 테스트는 실제 비즈니스 요구사항을 검증한다.
4: 각 테스트는 독립적으로 실행되며, assert 메시지로 실패 원인을 명확히 표시한다.
5: """
6: 
7: import os
8: import json
9: import tempfile
10: import sys
11: 
12: # solution 디렉토리를 경로에 추가
13: sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
14: 
15: from analyzer.reader import read_csv, extract_numeric_column
16: from analyzer.statistics import compute_stats, group_by_category
17: from analyzer.outlier import detect_outliers
18: from analyzer.reporter import classify_grades, find_high_performers
19: from main import run
20: 
21: 
22: # ── 헬퍼 ────────────────────────────────────────────────────────────────────
23: 
24: def make_temp_csv(content: str) -> str:
25:     """임시 CSV 파일을 생성하고 경로를 반환한다."""
26:     f = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8')
27:     f.write(content)
28:     f.close()
29:     return f.name
30: 
31: 
32: def cleanup(path: str) -> None:
33:     if os.path.exists(path):
34:         os.remove(path)
35: 
36: 
37: # ── reader 테스트 ────────────────────────────────────────────────────────────
38: 
39: def test_read_csv_정상파일_읽기():
40:     """정상적인 CSV 파일을 올바르게 읽어야 한다."""
41:     csv_path = make_temp_csv("id,name,score\n1,홍길동,85.0\n2,김철수,90.0\n")
42:     try:
43:         rows = read_csv(csv_path)
44:         assert len(rows) == 2, f"행 수가 2여야 하지만 {len(rows)}임"
45:         assert rows[0]['name'] == '홍길동', "첫 번째 행의 name이 '홍길동'이어야 함"
46:         assert rows[1]['score'] == '90.0', "두 번째 행의 score가 '90.0'이어야 함"
47:     finally:
48:         cleanup(csv_path)
49: 
50: 
51: def test_read_csv_헤더만있는파일_빈리스트반환():
52:     """헤더만 있고 데이터 행이 없는 파일은 빈 리스트를 반환해야 한다."""
53:     csv_path = make_temp_csv("id,name,score\n")
54:     try:
55:         rows = read_csv(csv_path)
56:         assert rows == [], f"빈 리스트여야 하지만 {rows}임"
57:     finally:
58:         cleanup(csv_path)
59: 
60: 
61: def test_read_csv_존재하지않는파일_예외발생():
62:     """존재하지 않는 파일 경로는 FileNotFoundError를 발생시켜야 한다."""
63:     try:
64:         read_csv("/존재하지않는/경로/file.csv")
65:         assert False, "FileNotFoundError가 발생해야 함"
66:     except FileNotFoundError:
67:         pass
68: 
69: 
70: def test_extract_numeric_column_결측값_건너뜀():
71:     """결측값이나 빈 문자열은 변환하지 않고 건너뛰어야 한다."""
72:     rows = [
73:         {'score': '85.0'},
74:         {'score': ''},       # 빈 값
75:         {'score': 'N/A'},    # 변환 불가
76:         {'score': '92.5'},
77:     ]
78:     values = extract_numeric_column(rows, 'score')
79:     assert len(values) == 2, f"유효한 값이 2개여야 하지만 {len(values)}개임"
80:     assert values == [85.0, 92.5], f"값이 [85.0, 92.5]여야 하지만 {values}임"
81: 
82: 
83: # ── statistics 테스트 ────────────────────────────────────────────────────────
84: 
85: def test_compute_stats_기본통계_정확성():
86:     """평균, 중앙값, 표준편차가 수학적으로 정확해야 한다."""
87:     values = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
88:     stats = compute_stats(values)
89:     assert stats['mean'] == 5.0, f"평균이 5.0이어야 하지만 {stats['mean']}임"
90:     assert stats['median'] == 4.5, f"중앙값이 4.5여야 하지만 {stats['median']}임"
91:     assert stats['std_dev'] == 2.0, f"표준편차가 2.0이어야 하지만 {stats['std_dev']}임"
92: 
93: 
94: def test_compute_stats_단일값_표준편차_0():
95:     """값이 하나면 표준편차는 0이어야 한다."""
96:     stats = compute_stats([42.0])
97:     assert stats['std_dev'] == 0.0, f"표준편차가 0.0이어야 하지만 {stats['std_dev']}임"
98:     assert stats['mean'] == 42.0
99:     assert stats['median'] == 42.0
100: 
101: 
102: def test_compute_stats_빈리스트_예외발생():
103:     """빈 리스트 입력 시 ValueError를 발생시켜야 한다."""
104:     try:
105:         compute_stats([])
106:         assert False, "ValueError가 발생해야 함"
107:     except ValueError:
108:         pass
109: 
110: 
111: def test_compute_stats_짝수개_중앙값():
112:     """짝수 개 데이터의 중앙값은 중간 두 값의 평균이어야 한다."""
113:     stats = compute_stats([1.0, 2.0, 3.0, 4.0])
114:     assert stats['median'] == 2.5, f"중앙값이 2.5여야 하지만 {stats['median']}임"
115: 
116: 
117: def test_group_by_category_부서별_그룹화():
118:     """부서별로 점수가 올바르게 그룹화되어야 한다."""
119:     rows = [
120:         {'department': 'engineering', 'score': '85.0'},
121:         {'department': 'marketing', 'score': '70.0'},
122:         {'department': 'engineering', 'score': '90.0'},
123:     ]
124:     groups = group_by_category(rows, 'department', 'score')
125:     assert 'engineering' in groups, "engineering 그룹이 있어야 함"
126:     assert sorted(groups['engineering']) == [85.0, 90.0], \
127:         f"engineering 점수가 [85.0, 90.0]이어야 하지만 {groups['engineering']}임"
128:     assert groups['marketing'] == [70.0]
129: 
130: 
131: # ── outlier 테스트 ────────────────────────────────────────────────────────────
132: 
133: def test_detect_outliers_명확한이상치_탐지():
134:     """분포에서 크게 벗어난 값은 이상치로 탐지되어야 한다."""
135:     # 85~95 범위의 정상 데이터 + 명확한 이상치 150
136:     rows = [{'score': str(v), 'name': f'사람{i}'} for i, v in
137:             enumerate([85, 87, 88, 90, 91, 92, 93, 94, 95, 150])]
138:     values = [float(r['score']) for r in rows]
139:     outliers = detect_outliers(rows, 'score', values)
140:     assert len(outliers) == 1, f"이상치가 1개여야 하지만 {len(outliers)}개임"
141:     assert outliers[0]['value'] == 150.0, f"이상치 값이 150이어야 하지만 {outliers[0]['value']}임"
142: 
143: 
144: def test_detect_outliers_정상분포_이상치없음():
145:     """균일한 분포에서는 이상치가 없어야 한다."""
146:     rows = [{'score': str(v), 'name': f'사람{i}'} for i, v in
147:             enumerate([80, 82, 84, 86, 88, 90, 92, 94])]
148:     values = [float(r['score']) for r in rows]
149:     outliers = detect_outliers(rows, 'score', values)
150:     assert len(outliers) == 0, f"이상치가 없어야 하지만 {outliers}임"
151: 
152: 
153: def test_detect_outliers_데이터부족_빈리스트():
154:     """데이터가 4개 미만이면 이상치 탐지를 건너뛰고 빈 리스트를 반환해야 한다."""
155:     rows = [{'score': '85', 'name': '사람1'}, {'score': '90', 'name': '사람2'}]
156:     values = [85.0, 90.0]
157:     outliers = detect_outliers(rows, 'score', values)
158:     assert outliers == [], f"빈 리스트여야 하지만 {outliers}임"
159: 
160: 
161: # ── reporter 테스트 ────────────────────────────────────────────────────────────
162: 
163: def test_classify_grades_등급_분류():
164:     """90+ A, 80+ B, 70+ C, 70미만 D로 정확히 분류해야 한다."""
165:     rows = [
166:         {'name': '최고', 'score': '95'},
167:         {'name': '우수', 'score': '85'},
168:         {'name': '보통', 'score': '75'},
169:         {'name': '미흡', 'score': '65'},
170:         {'name': '경계선', 'score': '90'},  # A 경계
171:     ]
172:     grades = classify_grades(rows)
173:     assert '최고' in grades['A'] and '경계선' in grades['A'], "90점은 A등급이어야 함"
174:     assert '우수' in grades['B'], "85점은 B등급이어야 함"
175:     assert '보통' in grades['C'], "75점은 C등급이어야 함"
176:     assert '미흡' in grades['D'], "65점은 D등급이어야 함"
177: 
178: 
179: def test_classify_grades_결측값_무시():
180:     """score가 없거나 변환 불가한 행은 등급 분류에서 무시되어야 한다."""
181:     rows = [
182:         {'name': '정상', 'score': '85'},
183:         {'name': '빈값', 'score': ''},
184:         {'name': '문자', 'score': 'abc'},
185:     ]
186:     grades = classify_grades(rows)
187:     total = sum(len(v) for v in grades.values())
188:     assert total == 1, f"유효한 등급이 1개여야 하지만 {total}개임"
189: 
190: 
191: def test_find_high_performers_기준충족():
192:     """점수 85 이상이고 나이 30 이상인 사람만 고성과자로 분류되어야 한다."""
193:     rows = [
194:         {'name': '고성과자', 'score': '90', 'age': '35'},   # 통과
195:         {'name': '점수낮음', 'score': '80', 'age': '35'},   # score 미달
196:         {'name': '나이젊음', 'score': '90', 'age': '25'},   # age 미달
197:         {'name': '경계선', 'score': '85', 'age': '30'},     # 정확히 기준값 통과
198:     ]
199:     result = find_high_performers(rows)
200:     assert '고성과자' in result, "고성과자는 결과에 있어야 함"
201:     assert '점수낮음' not in result, "점수 미달은 고성과자가 아니어야 함"
202:     assert '나이젊음' not in result, "나이 미달은 고성과자가 아니어야 함"
203:     assert '경계선' in result, "경계값 85/30은 고성과자 기준 충족이어야 함"
204: 
205: 
206: # ── 통합 테스트 ────────────────────────────────────────────────────────────────
207: 
208: def test_run_정상파일_완전분석():
209:     """정상 CSV로 run() 실행 시 모든 분석 결과가 포함된 딕셔너리를 반환해야 한다."""
210:     csv_content = (
211:         "id,name,age,score,salary,department\n"
212:         "1,홍길동,30,85.0,3500000,engineering\n"
213:         "2,김철수,25,70.0,2800000,marketing\n"
214:         "3,이영희,35,92.0,4500000,hr\n"
215:         "4,박민준,28,78.0,3200000,engineering\n"
216:         "5,최수진,40,88.0,5000000,hr\n"
217:     )
218:     csv_path = make_temp_csv(csv_content)
219:     out_path = csv_path + '_result.json'
220:     try:
221:         result = run(csv_path, out_path)
222:         assert result['total_records'] == 5, "레코드 수가 5여야 함"
223:         assert 'score' in result, "score 통계가 있어야 함"
224:         assert 'salary' in result, "salary 통계가 있어야 함"
225:         assert 'age' in result, "age 통계가 있어야 함"
226:         assert 'grades' in result, "등급 분류가 있어야 함"
227:         assert 'high_performers' in result, "고성과자 목록이 있어야 함"
228:         assert os.path.exists(out_path), "결과 JSON 파일이 생성되어야 함"
229:         with open(out_path, encoding='utf-8') as f:
230:             saved = json.load(f)
231:         assert saved['total_records'] == 5, "저장된 JSON의 레코드 수가 5여야 함"
232:     finally:
233:         cleanup(csv_path)
234:         cleanup(out_path)
235: 
236: 
237: def test_run_빈파일_예외발생():
238:     """데이터 행이 없는 파일로 run() 호출 시 ValueError가 발생해야 한다."""
239:     csv_path = make_temp_csv("id,name,age,score,salary,department\n")
240:     out_path = csv_path + '_result.json'
241:     try:
242:         run(csv_path, out_path)
243:         assert False, "ValueError가 발생해야 함"
244:     except ValueError:
245:         pass
246:     finally:
247:         cleanup(csv_path)
248:         cleanup(out_path)
249: 
250: 
251: # ── 테스트 실행 ────────────────────────────────────────────────────────────────
252: 
253: def run_all_tests():
254:     tests = [
255:         test_read_csv_정상파일_읽기,
256:         test_read_csv_헤더만있는파일_빈리스트반환,
257:         test_read_csv_존재하지않는파일_예외발생,
258:         test_extract_numeric_column_결측값_건너뜀,
259:         test_compute_stats_기본통계_정확성,
260:         test_compute_stats_단일값_표준편차_0,
261:         test_compute_stats_빈리스트_예외발생,
262:         test_compute_stats_짝수개_중앙값,
263:         test_group_by_category_부서별_그룹화,
264:         test_detect_outliers_명확한이상치_탐지,
265:         test_detect_outliers_정상분포_이상치없음,
266:         test_detect_outliers_데이터부족_빈리스트,
267:         test_classify_grades_등급_분류,
268:         test_classify_grades_결측값_무시,
269:         test_find_high_performers_기준충족,
270:         test_run_정상파일_완전분석,
271:         test_run_빈파일_예외발생,
272:     ]
273: 
274:     passed = 0
275:     failed = 0
276:     print("\n테스트 실행 중...\n")
277:     for test in tests:
278:         try:
279:             test()
280:             print(f"  PASS  {test.__name__}")
281:             passed += 1
282:         except Exception as e:
283:             print(f"  FAIL  {test.__name__}")
284:             print(f"        {e}")
285:             failed += 1
286: 
287:     print(f"\n결과: {passed}개 통과 / {failed}개 실패 (총 {len(tests)}개)")
288:     return failed == 0
289: 
290: 
291: if __name__ == '__main__':
292:     success = run_all_tests()
293:     sys.exit(0 if success else 1)

(End of file - total 293 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/README.md"
}
```

**Output:**
```
<path>/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/README.md</path>
<type>file</type>
<content>1: # Lab 02: 레거시 코드 리팩토링 + 테스트 생성
2: 
3: **세션**: Session 3 | **소요 시간**: 40분 | **난이도**: 중급
4: 
5: ## 학습 목표
6: 
7: - 에이전트를 활용해 지저분한 레거시 코드를 빠르게 리팩토링한다
8: - 에이전트가 생성한 테스트의 **품질 문제(동어반복 테스트)**를 직접 식별한다
9: - AGENTS.md에 리팩토링 규칙을 추가해 에이전트 동작을 제어하는 법을 익힌다
10: - 에이전트의 강점(빠른 구조 개선)과 한계(테스트 의미 검증 부재)를 체험한다
11: 
12: ## 실습 구조
13: 
14: ```
15: 02-legacy-refactoring/
16: ├── README.md               # 이 파일
17: ├── Justfile                # 실습 명령어 모음
18: ├── src/
19: │   ├── legacy_analyzer.py  # 의도적으로 지저분한 레거시 코드 (실습 대상)
20: │   └── data/
21: │       ├── sample_data.csv # 정상 데이터 (25행)
22: │       ├── edge_case.csv   # 결측값/이상치 포함 데이터
23: │       └── empty.csv       # 빈 파일 (헤더만)
24: ├── solution/
25: │   ├── config.py           # 매직 넘버 → 설정으로 추출
26: │   ├── main.py             # 진입점
27: │   ├── analyzer/
28: │   │   ├── __init__.py
29: │   │   ├── reader.py       # CSV 읽기
30: │   │   ├── statistics.py   # 통계 계산
31: │   │   ├── outlier.py      # 이상치 탐지
32: │   │   └── reporter.py     # 출력 및 저장
33: │   └── test_analyzer.py    # 포괄적 테스트 (17개)
34: └── artifacts/
35:     └── quality-checklist.md  # 에이전트 테스트 품질 평가 체크리스트
36: ```
37: 
38: ---
39: 
40: ## I DO: 강사 시연 (10분)
41: 
42: ### 목표
43: 레거시 코드에 에이전트가 테스트를 생성하면 어떤 문제가 생기는지 보여준다.
44: 
45: ### 시연 순서
46: 
47: **1. 레거시 코드 살펴보기**
48: 
49: ```bash
50: just run   # 실제로 동작하는 코드 확인
51: ```
52: 
53: `src/legacy_analyzer.py`를 열고 문제점들을 짚어본다:
54: - 하나의 `analyze_data()` 함수에 모든 로직 (약 200줄)
55: - `scoreList`, `avg2`, `total3` 같은 일관성 없는 네이밍
56: - 평균/중앙값/표준편차 계산 블록이 score, salary, age에 걸쳐 3번 중복
57: - `85`, `90`, `1.5` 같은 매직 넘버
58: - 에러 핸들링 전혀 없음 (`just run-empty` 실행 → ZeroDivisionError 발생)
59: 
60: **2. 에이전트에게 테스트 요청**
61: 
62: 에이전트(Opencode)에서 다음 프롬프트를 실행한다:
63: 
64: ```
65: src/legacy_analyzer.py 파일에 대한 단위 테스트를 작성해줘.
66: 파일명은 test_legacy.py로 저장해줘.
67: ```
68: 
69: **3. 생성된 테스트의 문제점 찾기**
70: 
71: 에이전트가 생성한 테스트에서 아래 패턴을 찾아 학생들에게 보여준다:
72: 
73: ```python
74: # 동어반복 테스트 예시 (에이전트가 자주 생성하는 패턴)
75: def test_analyze_runs():
76:     analyze_data("data/sample_data.csv")  # 단순 실행만 확인, 결과 검증 없음
77: 
78: def test_file_loaded():
79:     analyze_data("data/sample_data.csv")
80:     assert results != {}  # 전역변수 참조, 실제 값 검증 없음
81: ```
82: 
83: **핵심 메시지**: 에이전트는 "코드가 실행된다"는 테스트는 잘 만들지만,
84: "비즈니스 요구사항을 올바르게 구현했는가"를 검증하는 테스트는 스스로 만들기 어렵다.
85: 
86: ---
87: 
88: ## WE DO: 함께 실습 (15분)
89: 
90: ### 목표
91: 에이전트에게 리팩토링을 요청하고, AGENTS.md로 품질을 제어한다.
92: 
93: ### 단계별 진행
94: 
95: **Step 1: AGENTS.md 작성 (5분)**
96: 
97: `src/` 디렉토리에 `AGENTS.md` 파일을 직접 작성한다:
98: 
99: ```markdown
100: # 리팩토링 규칙
101: 
102: ## 코드 스타일
103: - 모든 변수명은 snake_case를 사용한다
104: - 함수 하나는 하나의 역할만 담당한다 (Single Responsibility)
105: - 매직 넘버는 반드시 이름 있는 상수로 추출한다
106: 
107: ## 에러 핸들링
108: - 파일 읽기는 반드시 try-except로 감싼다
109: - 빈 데이터에 대해 ValueError를 발생시킨다
110: 
111: ## 테스트 요구사항
112: - 단순 실행 확인이 아닌 예상값을 하드코딩해서 검증한다
113: - 엣지 케이스(빈 파일, 결측값)를 반드시 테스트한다
114: - assert 메시지에 예상값과 실제값을 포함한다
115: ```
116: 
117: **Step 2: 에이전트에게 리팩토링 요청 (5분)**
118: 
119: ```
120: AGENTS.md의 규칙을 따라서 legacy_analyzer.py를 리팩토링해줘.
121: 다음 구조로 분리해:
122: - analyzer/reader.py: CSV 읽기
123: - analyzer/statistics.py: 통계 계산
124: - analyzer/outlier.py: 이상치 탐지
125: - analyzer/reporter.py: 출력
126: - config.py: 설정값
127: - main.py: 진입점
128: ```
129: 
130: **Step 3: 테스트 실행 및 확인 (5분)**
131: 
132: ```bash
133: # 리팩토링 전 레거시 코드 실행
134: just run
135: 
136: # 리팩토링 후 솔루션 실행 — 같은 결과인지 확인
137: just run-solution
138: 
139: # 테스트 통과 확인
140: just test
141: ```
142: 
143: 결과를 나란히 비교하며 **같은 분석 결과**가 나오는지 확인한다.
144: 
145: ### 세션 추적으로 에이전트 분석 전략 관찰 (선택 사항)
146: 
147: 세션을 내보내면 에이전트가 레거시 코드를 어떤 순서로 분석했는지 확인할 수 있다.
148: 
149: ```bash
150: opencode session list
151: opencode export <session-id> > legacy-session.json
152: ```
153: 
154: 확인 포인트:
155: - 에이전트가 **어떤 파일을 먼저 읽었는가?** (테스트 파일? 소스 코드?)
156: - AGENTS.md 규칙이 에이전트의 **탐색 순서**에 영향을 주었는가?
157: - 에이전트가 테스트를 **몇 번 실행**했는가? (피드백 루프 횟수)
158: 
159: > 세션 추적 방법은 [부록: 세션 추적 가이드](../../guide/appendix-session-tracking.md)를 참고하라.
160: 
161: ---
162: 
163: ## YOU DO: 독립 실습 (15분)
164: 
165: ### 과제 1: 에이전트가 놓친 엣지 케이스 추가
166: 
167: `solution/test_analyzer.py`를 열고, 에이전트가 놓쳤을 법한 테스트를 직접 추가한다.
168: 
169: 추가해야 할 테스트:
170: 
171: ```python
172: # 힌트 1: 모든 값이 같을 때 표준편차는 0이어야 한다
173: def test_compute_stats_동일값_표준편차_0():
174:     pass  # 직접 구현
175: 
176: # 힌트 2: 홀수 개 데이터의 중앙값 정확성
177: def test_compute_stats_홀수개_중앙값():
178:     pass  # 직접 구현
179: 
180: # 힌트 3: 부서가 하나뿐인 데이터의 그룹화
181: def test_group_by_category_단일부서():
182:     pass  # 직접 구현
183: ```
184: 
185: 추가 후 테스트를 실행해 통과하는지 확인:
186: ```bash
187: just test
188: ```
189: 
190: ### 과제 2: 커스텀 리뷰어 에이전트 설정
191: 
192: `.opencode/agents/reviewer.md` 또는 에이전트 설정 파일을 만들어,
193: 리팩토링 결과를 자동으로 검토하는 리뷰어 에이전트를 구성한다.
194: 
195: 리뷰어가 확인할 항목 예시:
196: - 매직 넘버가 남아있지 않은가?
197: - 각 함수가 20줄 이내인가?
198: - 에러 핸들링이 모든 IO 작업에 적용되었는가?
199: 
200: 에이전트에게 `@reviewer 이 리팩토링 결과를 검토해줘`를 요청하고 결과를 확인한다.
201: 
202: ### 완료 기준
203: 
204: - [ ] 추가한 테스트 3개가 모두 통과한다
205: - [ ] 커스텀 리뷰어 에이전트가 리팩토링 결과를 검토했다
206: - [ ] `artifacts/quality-checklist.md`로 에이전트 생성 테스트를 직접 평가했다
207: 
208: ---
209: 
210: ## 참고: 레거시 코드의 의도적 문제점 목록
211: 
212: | 문제 | 위치 | 리팩토링 후 |
213: |------|------|------------|
214: | 단일 거대 함수 | `analyze_data()` 전체 | 4개 모듈로 분리 |
215: | camelCase 변수 | `scoreList`, `avg2`, `total3` | `score_values`, `score_mean` 등 |
216: | 중복 코드 | 평균/중앙값/표준편차 3번 반복 | `compute_stats()` 함수 1개 |
217: | 매직 넘버 | `1.5`, `0.25`, `0.75`, `85`, `90` | `config.py`의 상수 |
218: | 에러 핸들링 없음 | 파일 읽기, 형변환 | try-except + ValueError |
219: | 전역 변수 | `data`, `results`, `fileName` | 함수 반환값으로 대체 |
220: | 오래된 주석 | `# 2019년 인턴이 작성` | 타입힌트 + 독스트링 |
221: 
222: ---
223: 
224: ## 빠른 명령어 참고
225: 
226: ```bash
227: just setup          # 환경 확인
228: just run            # 레거시 코드 실행
229: just run-edge       # 엣지 케이스 실행
230: just run-empty      # 빈 파일 실행 (에러 발생)
231: just run-solution   # 솔루션 코드 실행
232: just test           # 테스트 실행
233: just compare        # 레거시 vs 솔루션 출력 비교
234: just stats          # 코드 통계 (줄 수)
235: just clean          # 결과 파일 정리
236: ```

(End of file - total 236 lines)
</content>
```

---

## Assistant (Build · gpt-5.4 · 10.8s)

_Thinking:_

**Considering behavior analysis**

I'm thinking we can assert the current behavior, especially if an empty file might raise a ZeroDivisionError. It's a good idea to test the output results of analyze_data to see if the dictionary looks correct. I need to be careful to avoid tautological tests, so perhaps I should just read the data files to see if that’s sufficient for my purposes. Let’s keep it simple and effective!

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/src/data/sample_data.csv"
}
```

**Output:**
```
<path>/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/src/data/sample_data.csv</path>
<type>file</type>
<content>1: id,name,age,score,salary,department
2: 1,김철수,28,85.5,3500000,engineering
3: 2,이영희,34,92.0,4200000,marketing
4: 3,박민준,25,78.3,2800000,engineering
5: 4,최수진,41,88.7,5100000,hr
6: 5,정대호,30,65.2,3200000,marketing
7: 6,한지현,27,91.4,3100000,engineering
8: 7,오승환,38,74.8,4500000,hr
9: 8,윤미래,33,83.6,3800000,marketing
10: 9,강동원,29,96.1,3300000,engineering
11: 10,임서연,45,70.5,5600000,hr
12: 11,신민아,26,88.9,2900000,engineering
13: 12,류준열,31,79.2,3600000,marketing
14: 13,전지현,36,93.8,4700000,hr
15: 14,공유,42,67.4,5200000,marketing
16: 15,손예진,28,86.3,3100000,engineering
17: 16,현빈,37,81.7,4400000,hr
18: 17,이병헌,44,72.9,5300000,marketing
19: 18,김태희,32,89.5,3700000,engineering
20: 19,원빈,35,77.1,4100000,hr
21: 20,송혜교,29,94.2,3400000,engineering
22: 21,이민호,27,83.0,3000000,marketing
23: 22,박보검,24,88.4,2600000,engineering
24: 23,아이유,30,91.7,3500000,marketing
25: 24,수지,28,76.5,3200000,engineering
26: 25,BTS진,26,85.8,2900000,engineering

(End of file - total 26 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/src/data/edge_case.csv"
}
```

**Output:**
```
<path>/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/src/data/edge_case.csv</path>
<type>file</type>
<content>1: id,name,age,score,salary,department
2: 1,정상데이터,30,85.0,3500000,engineering
3: 2,결측값있음,25,,3200000,marketing
4: 3,나이없음,,78.5,2900000,engineering
5: 4,,이름없음,90.0,4000000,hr
6: 5,급여없음,35,82.3,,marketing
7: 6,정상데이터2,28,88.0,3100000,engineering
8: 7,,,,,
9: 8,이상치점수,32,150.0,3400000,engineering
10: 9,음수급여,27,75.5,-1000000,marketing
11: 10,정상데이터3,33,79.8,3800000,hr

(End of file - total 11 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/src/data/empty.csv"
}
```

**Output:**
```
<path>/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/src/data/empty.csv</path>
<type>file</type>
<content>1: id,name,age,score,salary,department

(End of file - total 1 lines)
</content>
```

---

## Assistant (Build · gpt-5.4 · 12.0s)

_Thinking:_

**Considering sample stats computation**

I’m weighing the options for computing expected sample statistics. I could either do it manually, which might be tedious, or I could use Python to run a snippet. Using an independent calculator sounds handy, but I want to ensure whatever method I choose is robust enough. I’m thinking of using Bash with Python for this. That might streamline the process and ensure accuracy. Let’s see how it goes!

**Tool: bash**

**Input:**
```json
{
  "command": "python3 - <<'PY'\nimport csv, math, json\nfrom pathlib import Path\np = Path('src/data/sample_data.csv')\nrows = list(csv.DictReader(p.open(encoding='utf-8')))\nfor key in ['score','salary','age']:\n    vals=[float(r[key]) for r in rows]\n    avg=sum(vals)/len(vals)\n    s=sorted(vals)\n    n=len(s)\n    med=(s[n//2-1]+s[n//2])/2 if n%2==0 else s[n//2]\n    var=sum((v-avg)**2 for v in vals)/len(vals)\n    std=math.sqrt(var)\n    q1_idx=int(n*0.25); q3_idx=int(n*0.75)\n    q1=s[q1_idx]; q3=s[q3_idx]; iqr=q3-q1\n    lo=q1-1.5*iqr; hi=q3+1.5*iqr\n    out=[{'index':i,'value':vals[i],'name':rows[i]['name']} for i in range(len(vals)) if vals[i] < lo or vals[i] > hi]\n    print(key, {'mean':round(avg,2),'median':round(med,2),'std':round(std,2),'min':min(vals),'max':max(vals),'outliers':out})\n\ndept={}\nfor r in rows:\n    dept.setdefault(r['department'],[]).append(float(r['score']))\nprint('dept_avg', {k:sum(v)/len(v) for k,v in dept.items()})\n\ngrades={'A':[],'B':[],'C':[],'D':[]}\nfor r in rows:\n    sc=float(r['score']); name=r['name']\n    if sc >= 90: grades['A'].append(name)\n    elif sc >= 80: grades['B'].append(name)\n    elif sc >= 70: grades['C'].append(name)\n    else: grades['D'].append(name)\nprint('grades', grades)\nprint('high', [r['name'] for r in rows if float(r['score']) >= 85 and float(r['age']) >= 30])\nPY",
  "workdir": "/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring",
  "description": "Computes expected sample statistics"
}
```

**Output:**
```
score {'mean': 83.3, 'median': 85.5, 'std': 8.49, 'min': 65.2, 'max': 96.1, 'outliers': []}
salary {'mean': 3788000.0, 'median': 3500000.0, 'std': 850562.17, 'min': 2600000.0, 'max': 5600000.0, 'outliers': []}
age {'mean': 32.2, 'median': 30.0, 'std': 5.98, 'min': 24.0, 'max': 45.0, 'outliers': []}
dept_avg {'engineering': 87.35454545454546, 'marketing': 79.375, 'hr': 81.10000000000001}
grades {'A': ['이영희', '한지현', '강동원', '전지현', '송혜교', '아이유'], 'B': ['김철수', '최수진', '윤미래', '신민아', '손예진', '현빈', '김태희', '이민호', '박보검', 'BTS진'], 'C': ['박민준', '오승환', '임서연', '류준열', '이병헌', '원빈', '수지'], 'D': ['정대호', '공유']}
high ['이영희', '최수진', '전지현', '김태희', '아이유']

```

---

## Assistant (Build · gpt-5.4 · 33.7s)

_Thinking:_

**Exploring error handling**

I'm thinking capturing empty file crashes might be a good idea. Ideally, the README should mention issues with empty file errors as part of the business requirements. I could test to see if it raises a ZeroDivisionError. Also, I want to ensure the result JSON file contents match the results dictionary and that the `outputFile` override works properly. Perhaps I can set a custom path for `module.outputFile`, analyze the data, and then read the JSON file.

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: /Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/test_legacy.py\n+import importlib.util\n+import json\n+import math\n+import sys\n+from pathlib import Path\n+\n+\n+ROOT = Path(__file__).resolve().parent\n+LEGACY_PATH = ROOT / \"src\" / \"legacy_analyzer.py\"\n+SAMPLE_CSV = ROOT / \"src\" / \"data\" / \"sample_data.csv\"\n+EDGE_CASE_CSV = ROOT / \"src\" / \"data\" / \"edge_case.csv\"\n+EMPTY_CSV = ROOT / \"src\" / \"data\" / \"empty.csv\"\n+\n+\n+def load_legacy_module(monkeypatch, tmp_path, bootstrap_csv=SAMPLE_CSV):\n+    monkeypatch.chdir(tmp_path)\n+    monkeypatch.setattr(sys, \"argv\", [str(LEGACY_PATH), str(bootstrap_csv)])\n+\n+    spec = importlib.util.spec_from_file_location(\"legacy_analyzer_under_test\", LEGACY_PATH)\n+    module = importlib.util.module_from_spec(spec)\n+    assert spec.loader is not None\n+    spec.loader.exec_module(module)\n+    return module\n+\n+\n+def test_sample_data_results_match_expected_statistics(monkeypatch, tmp_path):\n+    module = load_legacy_module(monkeypatch, tmp_path)\n+    result = module.results\n+\n+    assert result[\"file\"] == str(SAMPLE_CSV)\n+    assert result[\"total_records\"] == 25\n+\n+    assert result[\"score\"] == {\n+        \"mean\": 83.3,\n+        \"median\": 85.5,\n+        \"std_dev\": 8.49,\n+        \"min\": 65.2,\n+        \"max\": 96.1,\n+        \"outliers\": [],\n+    }\n+    assert result[\"salary\"] == {\n+        \"mean\": 3788000.0,\n+        \"median\": 3500000.0,\n+        \"std_dev\": 850562.17,\n+        \"min\": 2600000.0,\n+        \"max\": 5600000.0,\n+        \"outliers\": [],\n+    }\n+    assert result[\"age\"] == {\n+        \"mean\": 32.2,\n+        \"median\": 30.0,\n+        \"std_dev\": 5.98,\n+    }\n+    assert result[\"department_avg_score\"] == {\n+        \"engineering\": 87.35454545454546,\n+        \"marketing\": 79.375,\n+        \"hr\": 81.10000000000001,\n+    }\n+    assert result[\"grades\"] == {\n+        \"A\": [\"이영희\", \"한지현\", \"강동원\", \"전지현\", \"송혜교\", \"아이유\"],\n+        \"B\": [\"김철수\", \"최수진\", \"윤미래\", \"신민아\", \"손예진\", \"현빈\", \"김태희\", \"이민호\", \"박보검\", \"BTS진\"],\n+        \"C\": [\"박민준\", \"오승환\", \"임서연\", \"류준열\", \"이병헌\", \"원빈\", \"수지\"],\n+        \"D\": [\"정대호\", \"공유\"],\n+    }\n+    assert result[\"high_performers\"] == [\"이영희\", \"최수진\", \"전지현\", \"김태희\", \"아이유\"]\n+\n+\n+def test_writes_json_report_to_configured_output_file(monkeypatch, tmp_path):\n+    module = load_legacy_module(monkeypatch, tmp_path)\n+    output_path = tmp_path / \"custom-report.json\"\n+\n+    module.results = {}\n+    module.outputFile = str(output_path)\n+    module.analyze_data(str(SAMPLE_CSV))\n+\n+    saved = json.loads(output_path.read_text(encoding=\"utf-8\"))\n+    assert saved == module.results\n+    assert saved[\"score\"][\"mean\"] == 83.3\n+    assert saved[\"salary\"][\"median\"] == 3500000.0\n+\n+\n+def test_invalid_numeric_rows_raise_value_error(monkeypatch, tmp_path):\n+    module = load_legacy_module(monkeypatch, tmp_path)\n+\n+    module.results = {}\n+    with __import__(\"pytest\").raises(ValueError):\n+        module.analyze_data(str(EDGE_CASE_CSV))\n+\n+\n+def test_empty_csv_raises_zero_division_error(monkeypatch, tmp_path):\n+    module = load_legacy_module(monkeypatch, tmp_path)\n+\n+    module.results = {}\n+    with __import__(\"pytest\").raises(ZeroDivisionError):\n+        module.analyze_data(str(EMPTY_CSV))\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A lectures/agentic-coding-basic/labs/02-legacy-refactoring/test_legacy.py
```

---

## Assistant (Build · gpt-5.4 · 11.0s)

_Thinking:_

**Improving pytest import**

I’m thinking about my code and how I need to clean up the imports. It’s probably better to import pytest at the top of the file rather than using `__import__`. Also, I just realized I have an unused math library imported, which I should fix too. It's important to keep my code clean and efficient, so tackling these small issues will help improve overall readability and maintainability. Getting this right feels good!

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Update File: /Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring/test_legacy.py\n@@\n import importlib.util\n import json\n-import math\n import sys\n from pathlib import Path\n \n+import pytest\n+\n@@\n def test_invalid_numeric_rows_raise_value_error(monkeypatch, tmp_path):\n     module = load_legacy_module(monkeypatch, tmp_path)\n \n     module.results = {}\n-    with __import__(\"pytest\").raises(ValueError):\n+    with pytest.raises(ValueError):\n         module.analyze_data(str(EDGE_CASE_CSV))\n@@\n def test_empty_csv_raises_zero_division_error(monkeypatch, tmp_path):\n     module = load_legacy_module(monkeypatch, tmp_path)\n \n     module.results = {}\n-    with __import__(\"pytest\").raises(ZeroDivisionError):\n+    with pytest.raises(ZeroDivisionError):\n         module.analyze_data(str(EMPTY_CSV))\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
M lectures/agentic-coding-basic/labs/02-legacy-refactoring/test_legacy.py
```

---

## Assistant (Build · gpt-5.4 · 5.8s)

_Thinking:_



**Tool: bash**

**Input:**
```json
{
  "command": "pytest test_legacy.py",
  "workdir": "/Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring",
  "timeout": 120000,
  "description": "Runs legacy analyzer unit tests"
}
```

**Output:**
```
============================= test session starts ==============================
platform darwin -- Python 3.11.6, pytest-9.0.2, pluggy-1.6.0
rootdir: /Users/taekkim/auto-lecture/lectures/agentic-coding-basic/labs/02-legacy-refactoring
plugins: anyio-4.12.1, dash-2.17.1, asyncio-1.3.0, Faker-40.1.2, cov-7.0.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 4 items

test_legacy.py ....                                                      [100%]

============================== 4 passed in 0.05s ===============================

```

---

## Assistant (Build · gpt-5.4 · 6.4s)

_Thinking:_

**Creating concise Korean output**

I need to finalize a concise version in Korean. It seems important to mention the file that was created and the testing that was conducted. I should also include the test command that was used. Keeping everything clear and concise will be key here. This way, I ensure the user has all the necessary information without excess detail. Let's keep it straightforward and to the point!

`src/legacy_analyzer.py`용 테스트를 `test_legacy.py`로 추가했어.

- 생성 파일: `test_legacy.py`
- 검증 내용:
  - `sample_data.csv` 기준 통계값, 부서별 평균, 등급 분류, 고성과자 목록 검증
  - `outputFile` 변경 시 JSON 결과 파일 저장 내용 검증
  - `edge_case.csv`의 비정상 숫자 데이터에서 `ValueError` 발생 검증
  - `empty.csv`에서 현재 레거시 동작대로 `ZeroDivisionError` 발생 검증

실행도 확인했어.

- 실행 명령: `pytest test_legacy.py`
- 결과: `4 passed`

원하면 다음도 해줄 수 있어:
1. 이 테스트를 `just test` 흐름에 포함되게 정리
2. 레거시 코드가 import 시 바로 실행되는 문제를 리팩토링해서 테스트를 더 단순하게 개선

---

