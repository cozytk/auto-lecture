# Lab 00: 낯선 코드베이스 탐험

> **Session 1 실습 | 소요 시간: 30분**
> 처음 보는 코드베이스를 에이전트와 함께 탐색하고, 에이전트의 행동 패턴을 분석한다.

---

## 학습 목표

- 에이전트가 코드를 읽고 분석하는 **실제 도구 호출 순서**를 관찰한다
- 에이전트가 발견한 것과 **놓친 것**을 비교하며 한계를 이해한다
- 에이전트에게 탐색 작업을 위임하는 방법을 익힌다
- 에이전트와 함께 기존 코드에 새 기능을 추가하는 경험을 한다

---

## 프로젝트 소개: studylog

`src/` 디렉토리에는 **CLI 학습 세션 트래커** 프로젝트가 있다.
7개 파일, 약 400줄의 Python 코드로 구성된 실제 규모의 작은 앱이다.

```
src/
  studylog.py    # 메인 CLI 진입점 (argparse)
  session.py     # 세션 시작/종료 관리
  store.py       # JSON 파일 기반 저장소
  engine.py      # 통계 계산 (이름만으로는 역할이 불명확)
  display.py     # 터미널 출력 포맷팅
  config.py      # 설정 관리
  test_studylog.py  # 단위 테스트 (25개)
```

**현재 지원 명령어:** `start`, `stop`, `current`, `list`, `stats`, `export`

> **참고:** 이 프로젝트에는 에이전트가 발견할 수 있는 몇 가지 숨겨진 특징이 있다.
> 에이전트가 무엇을 찾고 무엇을 놓치는지 관찰하는 것이 이 실습의 핵심이다.

---

## 환경 설정

```bash
# Python 표준 라이브러리만 사용 — 별도 설치 불필요
python3 --version    # 3.10 이상

# 테스트 실행
just test
# 또는 직접:
cd src && python3 -m unittest test_studylog -v

# 샘플 데이터 생성 (선택)
just seed
```

---

## I DO — 실제 세션 로그 분석 (10분)

> 아래는 에이전트에게 이 프로젝트를 분석하라고 요청했을 때의 **실제 세션 기록**이다.
> 강사는 이 로그를 보여주며 에이전트의 행동을 단계별로 설명한다.

### 실행한 프롬프트

```
이 프로젝트의 구조를 분석해줘.
어떤 앱인지, 주요 파일의 역할이 무엇인지,
현재 어떤 기능이 있는지 코드를 직접 읽고 파악해줘.
```

### 세션 요약

| 항목 | 메인 에이전트 (build) | @explore 서브에이전트 |
|------|----------------------|----------------------|
| 모델 | gpt-5.4 | gpt-5.4 |
| 소요 시간 | 2분 24초 | 48초 |
| 토큰 | 140,611 | 73,294 |
| 도구 호출 | 12회 | 12회 |
| 사용한 도구 | task, glob, bash, read, todowrite | glob, grep, read |

### 에이전트 행동 타임라인

```
[0:00] 사용자 → "이 프로젝트의 구조를 분석해줘..."
    │
[0:02] build 에이전트: TODO 리스트 생성
    │  todowrite → [
    │    "Survey repository structure",
    │    "Read core source files",
    │    "Summarize app purpose"
    │  ]
    │
[0:03] build → @explore 서브에이전트 위임
    │
    ├─── @explore 서브에이전트 시작 ───────────────────
    │ [0:04] glob * → 7개 파일 발견 (config.py, display.py,
    │        engine.py, session.py, store.py, studylog.py,
    │        test_studylog.py)
    │ [0:05] glob **/* → 동일 (하위 디렉토리 없음)
    │ [0:06] read studylog.py → CLI 진입점 확인
    │ [0:08] read engine.py → "통계 계산 모듈이구나"
    │ [0:10] read session.py → 세션 상태 전이 파악
    │ [0:12] read store.py → JSON 저장소 이해
    │ [0:14] read display.py → 출력 포맷팅 확인
    │ [0:16] read config.py → 설정 로딩 파악
    │ [0:18] read test_studylog.py → 테스트 구조 이해
    │ [0:20] grep "if __name__" → 진입점 2개 발견
    │ [0:22] grep "paused|import|export|..." → 기능 키워드 140개 매칭
    │ [0:24] read src/ → 디렉토리 구조 확인
    ├─── @explore 완료 (48초, 12회 도구 호출) ──────────
    │
[0:52] build: @explore 결과 수신 후 직접 파일 재확인
    │  glob **/* → 13개 파일
    │  bash "ls -la" → 파일 크기/날짜 확인
    │  read studylog.py, session.py, store.py,
    │       engine.py, display.py, config.py,
    │       test_studylog.py → 전부 다시 읽음 (!)
    │
[2:10] build: TODO 완료 처리 + 최종 답변 생성
    │
[2:24] 답변 출력
```

### 관찰 포인트

#### 1. 에이전트가 TODO 리스트로 계획을 세웠다

```
[ ] Survey repository structure and identify app entry points
[ ] Read core source files to infer responsibilities and existing features
[ ] Summarize app purpose, architecture, and key files for the user
```

에이전트는 바로 코드를 읽지 않고, 먼저 계획을 세운 뒤 체계적으로 진행했다.
이는 에이전틱 루프의 핵심 패턴인 **"계획 → 실행 → 검증"** 의 실제 사례다.

#### 2. engine.py의 불투명한 이름을 코드를 읽어서 파악했다

> "engine.py — 통계 계산 모듈입니다. 총 공부 시간, 주제별 집계, 일별 집계, 연속 학습일(streak), 평균 세션 길이를 계산합니다."

파일 이름만으로는 역할을 알 수 없었지만, **코드를 직접 읽고** 정확히 파악했다.
이것이 에이전트의 강점이다: 수백 줄의 코드를 빠르게 읽고 요약할 수 있다.

#### 3. 에이전트가 발견한 숨겨진 특징 (4/6)

| 특징 | 발견 여부 | 에이전트의 설명 |
|------|:---------:|----------------|
| `cmd_import()` — 구현되었지만 파서에 미등록 | ✅ | "코드상 import 기능은 있지만 실제 CLI 명령으로는 못 씁니다" |
| `_validate_transition()` — 호출되지 않는 상태 전이 검사 | ✅ | "상태 전이 규칙을 갖고 있지만 현재 호출되지 않습니다" |
| `_render_progress_bar()` — 미사용 프로그레스 바 | ✅ | "준비만 되어 있고 현재 기능에서는 사용되지 않습니다" |
| `by_day()` — 구현되었지만 stats 출력에 미연결 | ✅ | "구현돼 있지만 현재 stats 출력에는 연결되지 않았습니다" |
| `STUDYLOG_DEBUG` 환경변수 — 문서화되지 않은 디버그 모드 | ❌ | 언급 없음 |
| streak 계산의 자정 근처 타임존 이슈 | ❌ | 언급 없음 |

> **핵심 교훈**: 에이전트는 **구조적 패턴** (미사용 함수, 미등록 명령)은 잘 찾지만,
> **런타임 동작** (환경변수 분기, 경계값 버그)은 놓치기 쉽다.

#### 4. build 에이전트가 모든 파일을 두 번 읽었다

@explore 서브에이전트가 이미 모든 파일을 읽었는데, build 에이전트가 **같은 파일을 전부 다시 읽었다**.
이는 서브에이전트의 요약만으로는 충분하지 않다고 판단한 것이다.

> **비효율이지만 의미 있는 행동**: 서브에이전트의 결과를 검증하기 위해 원본을 직접 확인하는 패턴이다.
> 실제 개발에서도 "누군가의 요약"보다 "직접 코드를 읽는 것"이 더 정확할 때가 있다.

---

## WE DO — 기능 추가 + 세션 분석 (15분)

> 강사의 안내에 따라 에이전트에게 새 기능 추가를 요청하고, 세션 로그를 분석한다.

### 실습 목표: `list` 명령에 `--topic` 필터 추가

현재 `list` 명령은 모든 세션을 보여준다.
에이전트와 함께 `--topic` 옵션을 추가하여 주제별 필터링을 구현한다.

### Step 1: 현재 코드 파악

먼저 에이전트에게 관련 코드를 분석하게 한다:
```
list 명령이 어떻게 구현되어 있는지 설명해줘.
studylog.py의 cmd_list 함수와 store.py의 list_sessions 함수를 분석해줘.
```

### Step 2: 기능 추가 요청

```
list 명령에 --topic 옵션을 추가해줘.
예: python3 studylog.py list --topic python
대소문자 무시하고 부분 일치로 필터링해줘.
기존 테스트가 깨지지 않도록 주의해줘.
```

### Step 3: 동작 확인

```bash
# 샘플 데이터 생성
just seed

# 전체 목록
python3 src/studylog.py list

# 주제별 필터링
python3 src/studylog.py list --topic python
```

### 실제 세션에서 관찰된 에이전트 행동

아래는 위 프롬프트를 실행했을 때의 **실제 세션 요약**이다:

| 항목 | 값 |
|------|-----|
| 소요 시간 | 1분 32초 |
| 도구 호출 | 13회 |
| 파일 변경 | 2개 (studylog.py, test_studylog.py) |
| 변경량 | +45줄, -2줄 |
| 테스트 결과 | 27개 통과 (기존 25 + 신규 2) |

```
[0:00] 사용자 → "--topic 필터 추가해줘"
    │
[0:01] TODO 생성 → [탐색, 구현, 테스트]
    │
[0:02] 탐색 단계 (4개 파일 읽기):
    │  grep "list" → 관련 코드 위치 파악
    │  read studylog.py → cmd_list, build_parser 확인
    │  read store.py → list_sessions 함수 확인
    │  read test_studylog.py → 기존 테스트 패턴 파악
    │  read display.py → render_session_list 확인
    │
[0:30] 구현 단계 (2개 패치):
    │  apply_patch studylog.py → cmd_list에 필터 추가 + --topic 인자 등록
    │  apply_patch test_studylog.py → 테스트 2개 추가
    │
[1:10] 검증 단계:
    │  bash "python3 -m unittest test_studylog -v" → 27개 전부 OK
    │
[1:32] 완료 답변
```

### 에이전트의 설계 결정 분석

에이전트는 필터링을 `store.py`가 아닌 **`cmd_list` 함수 내부**에서 처리했다:

```python
# 에이전트의 선택: CLI 레벨 필터링
def cmd_list(args):
    sessions = store.list_sessions()
    if args.topic:
        topic_query = args.topic.casefold()
        sessions = [s for s in sessions if topic_query in s.get("topic", "").casefold()]
```

> **토론 포인트**: `store.list_sessions(topic=...)`으로 저장소 레벨에서 필터링하는 것과
> CLI 레벨에서 필터링하는 것 중 어느 쪽이 더 좋은 설계일까?

### 세션 분석 기록 양식

에이전트가 작업하는 동안 아래를 기록하라:

| 항목 | 관찰 내용 |
|------|-----------|
| 에이전트가 먼저 읽은 파일 | |
| 에이전트가 수정한 파일 | |
| store.py를 수정했는가? | |
| 테스트를 추가했는가? | |
| `casefold()` vs `lower()` 중 무엇을 사용했는가? | |
| 전체 소요 시간 | |

---

## YOU DO — 독립 실습 (15분)

> 에이전트와 함께 아래 과제 중 **하나 이상**을 자유롭게 수행한다.

### 도전 과제 (난이도 순)

#### ⭐ 기본: 일일 학습 목표

```
학습 목표를 설정하고 확인하는 goal 명령을 추가해줘.
- goal set 60 → 오늘 목표를 60분으로 설정
- goal show → 오늘 학습한 시간과 목표 대비 진행률 표시
- display.py의 _render_progress_bar 함수를 활용해줘
```

> **힌트:** `_render_progress_bar()`는 현재 미사용 함수다. 에이전트가 이걸 발견하고 활용하는지 관찰하라.

#### ⭐⭐ 중급: 일시정지/재개 기능

```
세션을 일시정지하고 재개하는 기능을 추가해줘.
- pause → 현재 세션을 일시정지
- resume → 일시정지된 세션을 재개
- session.py의 _validate_transition 함수를 활용해줘
```

> **힌트:** `_validate_transition()`은 상태 전이 규칙이 이미 정의되어 있다. 에이전트가 이 함수를 발견하고 활용하는지 관찰하라.

#### ⭐⭐⭐ 고급: 에이전트가 놓친 것 찾기

```
이 프로젝트에서 에이전트가 놓친 숨겨진 특징을 찾아보라.
1. config.py에서 문서화되지 않은 기능을 찾아라
2. engine.py의 streak() 함수에서 엣지 케이스 버그를 찾아라
```

> **힌트:** I DO에서 에이전트가 6개 중 4개만 발견했다. 나머지 2개를 직접 코드를 읽어서 찾아보라.

### 세션 로그 분석 과제 (선택)

자신의 에이전트 세션을 분석하고 싶다면:

```bash
# 세션 목록 확인
opencode session list
```

분석할 항목:
- 에이전트가 **어떤 파일을 먼저 읽었는가?**
- **탐색(Read) → 구현(Edit) 전환 시점**은 언제인가?
- 에이전트가 **테스트를 몇 번 실행**했는가?

---

## 정답 코드

`solution/` 디렉토리에 --topic 필터, 목표 설정, 일시정지/재개, import 명령이 모두 구현된 완성 버전이 있다.

```bash
# 솔루션 테스트 실행
cd solution && python3 -m unittest test_studylog -v
```

---

## 마무리 토론

실습 후 팀원과 공유하라:

1. **에이전트가 코드를 탐색하는 과정이 사람과 어떻게 달랐나?**
   - 에이전트는 `glob → read → grep` 순서로 기계적으로 탐색한다
   - 사람은 보통 README → 진입점 → 의존성 순서로 탐색한다

2. **에이전트가 발견한 것 vs 놓친 것의 패턴이 있는가?**
   - 구조적 패턴 (미사용 함수) → 잘 찾음
   - 런타임 동작 (환경변수, 경계값) → 놓침

3. **에이전트가 기능을 추가할 때 어떤 설계 결정을 했는가?**
   - 필터링 위치 (CLI vs 저장소)
   - 테스트 추가 여부
   - 기존 코드 변경 범위 최소화

4. **에이전트 없이 같은 작업을 했다면 얼마나 걸렸을까?**
