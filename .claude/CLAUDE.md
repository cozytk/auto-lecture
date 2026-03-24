# auto-lecture

강의 자료 자동 생성 시스템. 전문 에이전트(blueprint-writer, guide-writer, slide-master, lab-manager, script-writer)가 협업하여 설계안, 가이드, 슬라이드, 실습을 생성한다. 오케스트레이터는 별도 에이전트가 아닌 Claude Code 메인 Claude가 담당한다.

## 사용 가능한 스킬

| 스킬 | 설명 | 호출 |
|------|------|------|
| **blueprint-writer** | **수업 설계안 작성 — 모든 산출물의 단일 Source of Truth** | `/blueprint-writer [topic] [audience] [duration] [curriculum?]` |
| guide-writer | Blueprint 기반 상세 강의 가이드 작성 | `/guide-writer [topic] [audience] [curriculum?]` |
| slide-master | Blueprint 기반 slidev 슬라이드 장표 생성 (대본 미포함) | `/slide-master [topic]` |
| script-writer | 슬라이드 발표자 대본 작성 (가이드+슬라이드 기반) | `/script-writer [topic]` |
| slide-reviewer | 슬라이드 스크린샷 기반 시각 피드백 + 자동 수정 | `/slide-reviewer [topic] [--fix]` |
| lab-manager | Blueprint 기반 실습 제작 | `/lab-manager [topic]` |
| tui-screenshot-capture | VHS로 TUI 앱 스크린샷 캡처 | `/tui-screenshot-capture [command] [output-dir]` |
| oc-trace | OpenCode 세션 로그 추적·정리 및 교안 검증 | `/oc-trace <mode> [session_id] [lab_path]` |

## 슬라이드 기본 설정

- **다크모드 기본**: 모든 슬라이드는 다크모드를 기준으로 제작하고 검증한다
- 스크린샷 캡처도 다크모드가 기본 (`--light` 플래그로 라이트모드 전환 가능)
- 색상 선택 시 다크 배경 위에서의 가독성을 우선 고려한다
- `dark:` 접두사로 다크모드 전용 스타일을 적용할 수 있다 (예: `bg-blue-50 dark:bg-blue-900/30`)

## 수업 구성 원칙

- **비율**: 강의(슬라이드+가이드 설명) 30% / 실습 70%
- **수업 단위**: 1일 8시간, 최대 5일(40시간) 과정 대응
- **가이드 분할**: 하나의 guide.md가 아닌 교시/세션별로 파일을 분리
- **실행 환경**: Colab 실습과 로컬 실습을 구분. 로컬은 Linux 환경 가정 (macOS 호환 안내 포함)
- **파일 형식**: Python 코드 실행 위주 내용은 `.ipynb` 파일로 작성
- **실습 3단계**: 모든 실습은 **I DO → WE DO → YOU DO** 단계를 거친다
  - **I DO** (시연): 강사가 완성된 코드를 보여주며 시연. 학생은 관찰하며 이해
  - **WE DO** (함께): 강사가 이끌고 학생이 따라하며 함께 실습. 핵심 단계마다 멈추고 설명
  - **YOU DO** (독립): 학생이 스스로 도전하는 과제. 코드 실습이면 `solution/` 정답 코드를 제공하고, README 중심 실습이면 `artifacts/` 예시 산출물 또는 README 내 모범 답안 예시를 제공

## 산출물 디렉토리 구조

```
lectures/
  {topic}/                    # kebab-case (예: docker-intro, git-workflow)
    blueprint.md              # 수업 설계안 — 단일 Source of Truth
    research-brief.md         # 리서치 브리프 (모든 에이전트 공유)
    guide/
      README.md               # 전체 커리큘럼 개요, 수업 일정표
      day1-session1.md         # 교시별 가이드 (또는 .ipynb)
      day1-session2.ipynb      # Python 실행 위주면 노트북
      day2-session1.md
      ...
    slides/
      slides.md               # slidev 형식 슬라이드 (발표자 노트 포함)
      assets/                 # 이미지 등 리소스
    labs/
      {lab-name}/             # 실습 3단계 (I DO → WE DO → YOU DO)
        README.md             # 실습 가이드 (3단계 구조)
        Justfile              # 코드/자동화 실습일 때만 사용 (setup, run, test, clean)
        src/                  # 코드 실습일 때만 사용 (I DO 시연 코드 + WE DO 스캐폴드 + YOU DO 템플릿)
        solution/             # 코드 실습의 YOU DO 정답 코드 (필수)
        artifacts/            # README 중심 실습일 때 사용하는 워크시트, 템플릿, 산출물 예시
      feedback.md             # 실습 관리자의 가이드 피드백
```

- topic 이름은 kebab-case
- 모든 산출물은 한국어 기본
- 실습은 수업 시간의 약 70%를 차지해야 한다. 각 day 단위로 실습 총량을 충분히 확보한다.
- 실습은 반드시 코드일 필요가 없다. 분석/설계/토론/의사결정 실습은 `README.md` 중심으로 구성하고, 코드가 학습 효과를 높일 때만 `Justfile`, `src/`, `solution/`을 만든다.

## 오케스트레이션 규칙

### Source of Truth: Blueprint

**Blueprint(`blueprint.md`)가 모든 산출물의 단일 Source of Truth**다. 가이드, 슬라이드, 실습은 모두 blueprint를 참조하여 생성한다. 피드백 시 blueprint를 먼저 수정하고, 영향받는 산출물만 재생성한다.

### 실행 순서
1. **blueprint-writer** 먼저 실행 → `lectures/{topic}/blueprint.md` + `research-brief.md` 생성
2. Blueprint 승인 후 **guide-writer**, **slide-master**, **lab-manager**를 병렬 실행
3. slide-master + guide-writer 완료 후 **script-writer** 실행 → 슬라이드에 발표자 대본 추가

### 피드백 루프

산출물에 피드백이 오면 blueprint를 먼저 수정한다:

1. 산출물의 `<!-- source: block-id -->` 코멘트에서 관련 블록 확인
2. Blueprint의 해당 블록 수정
3. 영향받는 산출물만 재생성

| Blueprint 변경 유형 | 재생성 대상 |
|---------------------|------------|
| 블록 내용 (개념, 메시지) | 해당 가이드 섹션 + 해당 슬라이드 + 스크립트 |
| 블록 시간 변경 | 슬라이드 수 조정 + 실습 I/W/Y 시간 |
| 블록 유형 변경 (강의↔실습) | 가이드 + 슬라이드 + 실습 모두 |
| Q&A/혼동 포인트 변경 | 가이드 Q&A + Q&A 슬라이드 + 스크립트 |
| META 변경 (대상, 기간) | 전체 재생성 |

### 단일 에이전트 실행
각 스킬은 독립적으로 호출 가능하다. 예:
- 설계안 작성/수정: `/blueprint-writer docker-intro "주니어 개발자" "1일"`
- 가이드만 재생성: `/guide-writer docker-intro "주니어 개발자"`
- 슬라이드만 재생성: `/slide-master docker-intro`
- 발표자 대본만 작성: `/script-writer docker-intro`
- 실습만 재생성: `/lab-manager docker-intro`

### 팀 모드 병렬 실행

```
# OMC 팀 모드 (oh-my-claudecode 플러그인)
/team 2:guide-writer "blueprint 기반 가이드", 2:slide-master "blueprint 기반 슬라이드", 2:lab-manager "blueprint 기반 실습"

# 네이티브 Claude Code: 자연어로 병렬 실행 요청
"guide-writer, slide-master, lab-manager를 병렬로 실행해서 blueprint 기반으로 산출물을 생성해줘"
```

### 전체 파이프라인 예시
```
# Step 1: 설계안 생성 (사용자 승인 2회)
/blueprint-writer docker-intro "주니어 백엔드 개발자" "1일"

# Step 2: 가이드 + 슬라이드 + 실습 병렬 생성
/guide-writer docker-intro "주니어 백엔드 개발자"
/slide-master docker-intro
/lab-manager docker-intro

# Step 3: 발표자 대본 작성 (guide + slide 완료 후)
/script-writer docker-intro
```

## 실행 모드

### Full-Auto (기본)
모든 에이전트가 자율적으로 산출물을 완성한다. 사람의 승인 없이 진행.

### Human-in-the-loop (HITL)
사용자가 `--review` 또는 `HITL=true`를 지정하면 활성화.

**HITL 동작:**
- 각 에이전트의 주요 산출물 생성 후 PR 생성
- PR 병합은 사용자 승인 대기. 대기 중 다른 작업 먼저 진행
- 사용자 승인이 필요한 작업: 커리큘럼 결정, 최종 산출물 병합
- 사용자 승인이 불필요한 작업: 중간 초안, 이미지 검색, 테스트 실행

## GitHub 연동 규칙

- 각 강의 주제별 Issue 생성: `lecture: {topic}`
- 에이전트별 branch:
  - `lecture/{topic}/blueprint` (blueprint-writer)
  - `lecture/{topic}/guide` (guide-writer)
  - `lecture/{topic}/slides` (slide-master)
  - `lecture/{topic}/script` (script-writer)
  - `lecture/{topic}/labs` (lab-manager)
- 에이전트 산출물 완료 시 PR 생성
- Commit message 규칙: `[{agent}] {action}: {detail}`
  - 예: `[guide-writer] feat: Docker 입문 가이드 초안`
  - 예: `[slide-master] fix: 슬라이드 3번 오버플로 수정`
  - 예: `[lab-manager] test: Docker 실습 컨테이너 테스트 통과`
- 모든 작업을 Commit Message / Issue / PR로 추적 가능하도록 관리
