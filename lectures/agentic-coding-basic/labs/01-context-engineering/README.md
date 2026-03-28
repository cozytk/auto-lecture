# Lab 01: 컨텍스트 엔지니어링 챌린지

> **2교시 실습 (40분)** | Session 2: 에이전틱 루프와 컨텍스트 엔지니어링

## 실습 목표

**같은 요청, 다른 컨텍스트** — 에이전트에게 동일한 작업을 3번 요청하되, 매번 제공하는 컨텍스트를 달리한다.
결과의 차이를 직접 측정하며 컨텍스트 엔지니어링의 효과를 체감한다.

## 실습 구성

```
01-context-engineering/
├── README.md                          # 이 파일
├── Justfile                           # 환경 준비, 테스트, 서버 실행
├── src/                               # 참조용 원본 코드 (북마크 REST API)
│   ├── app.py                         # HTTP 서버 (라우팅)
│   ├── models.py                      # Bookmark dataclass
│   ├── database.py                    # JSON 저장소
│   ├── validators.py                  # 입력 유효성 검사
│   └── test_api.py                    # API 테스트
├── round1/                            # Round 1: AGENTS.md 없음
│   └── src/                           # (원본과 동일한 코드)
├── round2/                            # Round 2: 기본 AGENTS.md 있음
│   ├── AGENTS.md                      # 코딩 컨벤션 + 테스트 규칙
│   └── src/
├── round3/                            # Round 3: 풍부한 컨텍스트
│   ├── AGENTS.md                      # 상세 규칙 + 예시 참조
│   ├── architecture.md                # 아키텍처 문서
│   ├── examples/                      # 코드 예시 파일
│   │   ├── add_field.py               # 필드 추가 패턴
│   │   ├── error_handling.py          # 에러 핸들링 패턴
│   │   └── docstring_style.py         # docstring 스타일
│   └── src/
└── artifacts/
    └── comparison-template.md         # 비교 기록 양식
```

## 사전 준비

```bash
# Python 3.8 이상 필요
python3 --version

# 환경 확인
just setup
# 또는
python3 -c "import http.server, json, uuid, dataclasses; print('OK')"
```

---

## I DO: 강사 시연 (10분)

> 강사가 Round 1(규칙 없음)과 Round 2(규칙 있음)를 시연하며 차이를 보여줍니다.

### 시연 과제
모든 라운드에서 **동일한 요청**을 에이전트에게 보냅니다:

```
북마크에 category 필드를 추가하고, 카테고리별 필터링 API를 만들어줘.

요구사항:
- Bookmark 모델에 category 필드 추가 (선택 필드, 기본값 None)
- POST /bookmarks 시 category 값 저장 가능
- GET /bookmarks?category=tech 처럼 쿼리 파라미터로 필터링 가능
- 테스트 추가
```

### 시연 절차

**Round 1 시연** (규칙 없음):
1. 에이전트를 `round1/` 디렉토리에서 실행
2. 위 요청을 그대로 전달
3. 에이전트가 어떻게 접근하는지 관찰 (어떤 파일을 먼저 여는지, 판단 기준이 없을 때 무엇을 임의로 결정하는지)

**Round 2 시연** (기본 AGENTS.md):
1. 에이전트를 `round2/` 디렉토리에서 실행
2. 동일한 요청 전달
3. `round2/AGENTS.md`를 먼저 읽는지 확인
4. 코딩 컨벤션 준수 여부 확인 (에러 핸들링, 로깅, docstring)

### 관찰 포인트
- AGENTS.md 유무에 따라 **첫 행동**이 달라지는가?
- 에러 핸들링 스타일이 일관되게 나오는가?
- `print()` vs `logging` 사용 여부
- 테스트 함수명 패턴 (`test_<동작>_<조건>_<기댓값>`)

---

## WE DO: 함께 실습 (15분)

> 학생들이 Round 2를 직접 진행하고 결과를 기록합니다.

### 단계별 진행

**1단계: 코드 살펴보기 (3분)**

```bash
# round2/src/ 코드 구조 확인
ls round2/src/

# AGENTS.md 읽기 (중요!)
cat round2/AGENTS.md
```

**2단계: 기존 테스트 통과 확인 (2분)**

```bash
just test-r2
```

모든 테스트가 통과하면 준비 완료.

**3단계: 에이전트에게 과제 요청 (8분)**

에이전트를 `round2/` 디렉토리에서 실행하고 다음 요청을 보내세요:

```
북마크에 category 필드를 추가하고, 카테고리별 필터링 API를 만들어줘.

요구사항:
- Bookmark 모델에 category 필드 추가 (선택 필드, 기본값 None)
- POST /bookmarks 시 category 값 저장 가능
- GET /bookmarks?category=tech 처럼 쿼리 파라미터로 필터링 가능
- 테스트 추가
```

**4단계: 결과 확인 (2분)**

```bash
# 테스트 실행
just test-r2

# 서버 실행 후 curl로 확인
just serve-r2 &
curl -s -X POST http://localhost:8002/bookmarks \
  -H "Content-Type: application/json" \
  -d '{"title":"파이썬","url":"https://python.org","category":"docs"}'
curl -s "http://localhost:8002/bookmarks?category=docs"
kill %1
```

**5단계: 기록 (진행 중에 작성)**

`artifacts/comparison-template.md`의 Round 2 섹션을 채워주세요.

### Step 4: 세션 추적 (선택 사항)

에이전트의 내부 동작을 정량적으로 비교하고 싶다면, 각 Round 실행 후 세션을 내보낸다.

```bash
# 세션 ID 확인
opencode session list

# 세션 내보내기
opencode export <session-id> > round2-session.json
```

내보낸 데이터에서 확인할 수 있는 것:
- 도구 호출 횟수 (Read, Edit, Bash, Grep, Glob)
- 서브에이전트 사용 여부
- 총 소요 시간
- 첫 번째 Edit까지의 시간 (탐색 → 구현 전환 시점)

---

## YOU DO: 독립 실습 (15분)

> Round 3(풍부한 컨텍스트)를 직접 구성하고, 자신만의 AGENTS.md 규칙을 실험합니다.

### 과제 A: Round 3 실행 및 비교 (10분)

1. **Round 3 환경 탐색**

```bash
# Round 3에는 무엇이 있나?
ls round3/
cat round3/AGENTS.md
cat round3/architecture.md
ls round3/examples/
```

2. **에이전트를 `round3/` 디렉토리에서 실행**

동일한 요청을 전달하고 아래를 관찰하세요:
- `examples/add_field.py`를 참조하는가?
- `architecture.md`의 확장 포인트를 따르는가?
- Round 2보다 코드 품질이 개선되었는가?

3. **테스트 확인**

```bash
just test-r3
```

4. **비교 기록표 완성**

`artifacts/comparison-template.md`의 Round 3 섹션과 "라운드 비교 요약" 섹션을 채우세요.

### 과제 B: 나만의 AGENTS.md 규칙 실험 (5분)

Round 2 또는 Round 3의 AGENTS.md에 **자신만의 규칙을 추가**하고 에이전트 동작이 달라지는지 확인하세요.

아이디어 예시:
```markdown
## 추가 규칙 아이디어
- category 허용 값을 enum으로 정의하라: tech, news, blog, video, docs, other
- 북마크 URL은 중복 저장 금지
- 삭제 시 실제 삭제 대신 deleted_at 필드를 설정하는 소프트 삭제 방식 사용
- 응답에 항상 X-Total-Count 헤더 포함
```

추가한 규칙과 결과를 `artifacts/comparison-template.md`의 "나의 인사이트" 섹션에 기록하세요.

---

## 빠른 참고: curl 명령어

```bash
# 헬스 체크
curl http://localhost:8000/health

# 북마크 생성 (category 없음)
curl -X POST http://localhost:8000/bookmarks \
  -H "Content-Type: application/json" \
  -d '{"title":"Python","url":"https://python.org"}'

# 북마크 생성 (category 있음 - 에이전트가 기능 추가 후)
curl -X POST http://localhost:8000/bookmarks \
  -H "Content-Type: application/json" \
  -d '{"title":"GitHub","url":"https://github.com","category":"tech"}'

# 전체 목록 조회
curl http://localhost:8000/bookmarks

# 카테고리 필터링 (에이전트가 기능 추가 후)
curl "http://localhost:8000/bookmarks?category=tech"

# 단건 조회
curl http://localhost:8000/bookmarks/{id}

# 수정
curl -X PUT http://localhost:8000/bookmarks/{id} \
  -H "Content-Type: application/json" \
  -d '{"title":"새 제목","url":"https://new.com"}'

# 삭제
curl -X DELETE http://localhost:8000/bookmarks/{id}
```

---

## 세션 데이터로 Round 비교 (선택 사항)

3개 Round의 세션을 내보냈다면, 다음을 비교하라:

| 지표 | Round 1 (규칙 없음) | Round 2 (기본 규칙) | Round 3 (풍부한 컨텍스트) |
|------|---------------------|---------------------|--------------------------|
| 총 도구 호출 횟수 | | | |
| Read 횟수 | | | |
| Edit 횟수 | | | |
| Bash 횟수 | | | |
| 첫 Edit까지 시간 | | | |
| 총 소요 시간 | | | |
| 서브에이전트 사용 | | | |

> **예상 패턴**: Round 3(풍부한 컨텍스트)에서는 탐색(Read/Grep) 횟수가 줄고, 바로 구현(Edit)으로 진입하는 경향이 있다. 컨텍스트가 탐색을 대체하기 때문이다.

> 세션 추적 방법의 자세한 내용은 [부록: 세션 추적 가이드](../../guide/appendix-session-tracking.md)를 참고하라.

---

## 정리: 컨텍스트 엔지니어링의 핵심

| 컨텍스트 수준 | 에이전트에게 주어진 것 | 기대 효과 |
|--------------|----------------------|-----------|
| **Round 1** | 코드만 | 에이전트가 스타일을 자유 결정 |
| **Round 2** | 코드 + AGENTS.md | 컨벤션 준수, 일관성 향상 |
| **Round 3** | 코드 + AGENTS.md + 아키텍처 + 예시 | 패턴 재사용, 최소 판단, 고품질 출력 |

**핵심 교훈**: 에이전트는 **판단 비용이 높을수록** 불일관하거나 틀린 선택을 한다.
컨텍스트 엔지니어링은 "에이전트가 판단해야 할 것"을 줄이는 기술이다.
