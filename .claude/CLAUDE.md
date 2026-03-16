# auto-lecture

강의 자료 자동 생성 시스템. 3개 전문 에이전트(guide-writer, slide-master, lab-manager)가 협업하여 가이드, 슬라이드, 실습을 생성한다. 오케스트레이터는 별도 에이전트가 아닌 Claude Code 메인 Claude가 담당한다.

## 사용 가능한 스킬

| 스킬 | 설명 | 호출 |
|------|------|------|
| guide-writer | Source of Truth 강의 가이드 작성 | `/guide-writer [topic] [audience] [curriculum?]` |
| slide-master | 가이드 기반 slidev 슬라이드 생성 | `/slide-master [topic]` |
| lab-manager | 가이드 기반 실습 제작 | `/lab-manager [topic]` |

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

### 실행 순서
1. **guide-writer** 먼저 실행 → `lectures/{topic}/guide/` 생성
2. 가이드 완료 후 **slide-master**와 **lab-manager**를 병렬 실행
3. 가이드가 Source of Truth: 슬라이드와 실습은 반드시 가이드를 참조

### 단일 에이전트 실행
각 스킬은 독립적으로 호출 가능하다. 예:
- 가이드만 수정: `/guide-writer docker-intro "주니어 개발자"`
- 슬라이드만 재생성: `/slide-master docker-intro`
- 실습만 추가: `/lab-manager docker-intro`

### 팀 모드 병렬 실행

```
# OMC 팀 모드 (oh-my-claudecode 플러그인)
/team 2:slide-master "가이드 기반 슬라이드 생성", 2:lab-manager "가이드 기반 실습 생성"

# 네이티브 Claude Code: 자연어로 병렬 실행 요청
"slide-master와 lab-manager를 병렬로 실행해서 가이드 기반으로 슬라이드와 실습을 생성해줘"
```

### 전체 파이프라인 예시
```
# Step 1: 가이드 생성
/guide-writer docker-intro "주니어 백엔드 개발자"

# Step 2: 슬라이드 + 실습 병렬 생성
/slide-master docker-intro
/lab-manager docker-intro
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
  - `lecture/{topic}/guide` (guide-writer)
  - `lecture/{topic}/slides` (slide-master)
  - `lecture/{topic}/labs` (lab-manager)
- 에이전트 산출물 완료 시 PR 생성
- Commit message 규칙: `[{agent}] {action}: {detail}`
  - 예: `[guide-writer] feat: Docker 입문 가이드 초안`
  - 예: `[slide-master] fix: 슬라이드 3번 오버플로 수정`
  - 예: `[lab-manager] test: Docker 실습 컨테이너 테스트 통과`
- 모든 작업을 Commit Message / Issue / PR로 추적 가능하도록 관리
