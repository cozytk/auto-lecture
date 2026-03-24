---

name: slide-reviewer

description: Slidev 슬라이드를 렌더링하고 스크린샷을 찍어 시각적으로 검토한 뒤, 피드백을 생성하고 자동 수정하는 파이프라인

model: opus

context: fork

disable-model-invocation: true

allowed-tools: Read, Write, Edit, Grep, Glob, Bash

argument-hint: "[topic] [--fix] [--slides N-M] [--max-rounds 3]"

---

# Slide Reviewer — 시각 피드백 파이프라인

Slidev 슬라이드를 실제로 렌더링 → 스크린샷 캡처 → Claude 비전 분석 → 피드백 리포트 생성 → (옵션) 자동 수정을 수행한다.

## 입력

- `topic`: 강의 주제 (kebab-case). `lectures/{topic}/slides/` 디렉토리 필수
- `--fix`: 피드백 기반 자동 수정 활성화 (기본: 리포트만 생성)
- `--slides N-M`: 특정 슬라이드 범위만 검토 (기본: 전체)
- `--max-rounds 3`: 수정-재검토 최대 반복 횟수 (기본 3)

## 사전 조건

- `lectures/{topic}/slides/slides.md` 파일 존재
- `lectures/{topic}/slides/node_modules/` 에 `playwright`와 `@slidev/cli` 설치됨
- `playwright` 브라우저 설치됨 (`npx playwright install chromium`)

사전 조건이 충족되지 않으면 에러 메시지를 출력하고 중단한다.

## Slidev 서버 관리

Claude Code의 각 Bash 호출은 별도 셸이므로 백그라운드 프로세스가 유지되지 않는다.
**tmux 세션**으로 Slidev 서버를 관리한다.

### 서버 관리 스크립트: `scripts/slidev-serve.sh`

```bash
# 시작 (tmux 세션에서 실행, 서버 준비까지 대기)
scripts/slidev-serve.sh start lectures/{topic}/slides [slides.md] [--port 3030]

# 상태 확인
scripts/slidev-serve.sh status

# 중지
scripts/slidev-serve.sh stop

# 재시작
scripts/slidev-serve.sh restart lectures/{topic}/slides [slides.md] [--port 3030]
```

사용자가 직접 브라우저로 확인할 때도 이 스크립트를 사용한다.

## 파이프라인

### Phase 1: 스크린샷 캡처

**프로그래밍 방식** — `scripts/capture-slide.mjs`가 서버 시작→캡처→종료를 단일 프로세스에서 처리:

```bash
# 전체 슬라이드 캡처 (기본: 다크모드)
node scripts/capture-slide.mjs lectures/{topic}/slides

# 특정 슬라이드만 캡처
node scripts/capture-slide.mjs lectures/{topic}/slides 3 5 10

# 라이트모드로 캡처 (필요 시)
node scripts/capture-slide.mjs lectures/{topic}/slides --light 1 2 3
```

**인터랙티브 미리보기** — 사용자가 브라우저에서 직접 확인할 때:

```bash
scripts/slidev-serve.sh start lectures/{topic}/slides slides.md --port 3030
# → http://localhost:3030 에서 확인
# 완료 후: scripts/slidev-serve.sh stop
```

캡처 스크립트 동작:
- 내부적으로 Slidev dev 서버를 포트 3098에서 시작 (tmux 불필요)
- **다크모드**(기본)로 `980x552` 뷰포트에서 Playwright 캡처 (`?clicks=99`로 v-click 펼침)
- `screenshots-review/slide-{NNN}.png`에 저장
- 캡처 완료 후 서버 자동 종료

### Phase 2: 시각 분석

스크린샷을 **5장씩 배치**로 Read 도구로 읽으며 아래 체크리스트를 검증한다:

#### 검증 체크리스트

| # | 항목 | 설명 | 심각도 |
|---|------|------|--------|
| 1 | **오버플로** | 텍스트/코드가 캔버스(980×552) 밖으로 넘치거나 하단이 잘리는가 | 🔴 Critical |
| 2 | **가독성** | 글자 크기가 너무 작거나, 대비가 부족하거나, 텍스트가 과밀한가 | 🔴 Critical |
| 3 | **레이아웃 균형** | 콘텐츠가 한쪽에 치우치거나 여백이 비대칭인가 | 🟡 Warning |
| 4 | **코드+배경박스 공존** | 코드 블록이 있는 슬라이드에 배경 색상 박스가 함께 있는가 (규칙 7) | 🟡 Warning |
| 5 | **번호 목록 사용** | `1.`, `2.` 등 markdown 번호 목록이 본문에 사용되었는가 (규칙 12) | 🟡 Warning |
| 6 | **제목 길이** | 제목이 2줄 이상으로 줄바꿈되는가 (규칙 3) | 🟡 Warning |
| 7 | **시각 자료 연속 부재** | 텍스트 전용 슬라이드가 3장 연속되는가 (규칙 9) | 🟡 Warning |
| 8 | **이미지 누락** | `<!-- IMAGE: -->` 플레이스홀더가 보이는가 | 🟡 Warning |
| 9 | **빈 슬라이드** | 내용이 거의 없는 불필요한 슬라이드인가 | ℹ️ Info |
| 10 | **폰트 렌더링** | 폰트가 깨지거나 fallback 폰트로 표시되는가 | ℹ️ Info |

### Phase 3: 피드백 리포트 생성

분석 결과를 `lectures/{topic}/slides/feedback.md`에 저장한다:

```markdown
# Slide Review Feedback — {topic}

**검토 일시**: {날짜}
**총 슬라이드**: N장
**이슈 요약**: 🔴 Critical: N / 🟡 Warning: N / ℹ️ Info: N

## 이슈 목록

### 🔴 Critical

| 슬라이드 | 이슈 | 설명 | 수정 제안 |
|---------|------|------|----------|
| #5 | 오버플로 | 코드 블록이 하단을 넘침 | 코드를 15줄 이하로 분할하거나 maxHeight 추가 |

### 🟡 Warning
...

### ℹ️ Info
...

## 수정 완료 내역 (--fix 모드)

| 슬라이드 | 수정 내용 | 라운드 |
|---------|----------|--------|
| ... | ... | ... |
```

### Phase 4: 자동 수정 (--fix 모드)

`--fix` 플래그가 있을 때만 실행한다.

1. 🔴 Critical 이슈부터 순서대로 `slides.md`를 수정한다
2. 수정 후 Phase 1~2를 다시 실행하여 수정이 올바른지 검증한다
3. 새로운 이슈가 없거나 `--max-rounds`에 도달하면 종료한다

**수정 시 주의사항:**
- 발표자 노트는 수정하지 않는다 (구조 변경만)
- 슬라이드를 삭제하지 않는다 (분할은 허용)
- 수정 전 원본 슬라이드 내용을 기록한다
- 한 라운드에서 수정할 이슈는 최대 10개

### Phase 5: 완료 보고

```
슬라이드 리뷰 완료: lectures/{topic}/slides/
- 검토 슬라이드: N장
- 발견 이슈: 🔴 N / 🟡 N / ℹ️ N
- 수정 완료: N건 (--fix 모드 시)
- 리포트: lectures/{topic}/slides/feedback.md
- 스크린샷: lectures/{topic}/slides/screenshots-review/
```

## 수정 가이드 (이슈별 대응 방법)

| 이슈 | 수정 방법 |
|------|----------|
| 오버플로 — 코드 | `{maxHeight:'380px'}` 추가 또는 슬라이드 분할 |
| 오버플로 — 텍스트 | 불릿 줄이기, `zoom: 0.9` 적용, 또는 슬라이드 분할 |
| 코드+배경박스 | 배경 박스를 제거하고 `text-{color}-600` 텍스트로 대체 |
| 번호 목록 | 원기호(①②③) 또는 불릿(`-`)으로 변환 |
| 제목 줄바꿈 | 제목을 20자 이내로 축약 |
| 시각 자료 부재 | 중간에 Mermaid 다이어그램 또는 이미지 슬라이드 삽입 |
| 이미지 플레이스홀더 | WebSearch로 이미지 검색하여 교체 |
