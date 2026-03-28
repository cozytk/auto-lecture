# 에이전틱 코딩 입문: 코드 에이전트의 이해와 활용

> CLI 코드 에이전트의 핵심 개념을 학습하고, OpenCode를 통해 실습한다.
> 오늘 배우는 개념들은 Claude Code, Codex, Gemini CLI 등 어떤 코드 에이전트에도 적용된다.

## 실습 환경

- **OS**: WSL2 + Ubuntu 24.04 LTS (학생 대부분의 환경)
- **실습 도구**: OpenCode (무료 모델 사용)
- 각자 구독 중인 도구(Claude Code, Codex, Gemini CLI 등)가 있으면 자유롭게 사용 가능하나, 수업은 OpenCode를 위주로 진행
- 무료로 쓸 수 있는 대안: [free-claude-code](https://github.com/Alishahryar1/free-claude-code) — Claude Code를 무료 모델로 사용하는 오픈소스 래퍼

## 시간표

| 구분 | 시간 | 형태 | 주제 |
|------|------|------|------|
| 오프닝 | 09:30 ~ 09:45 (15분) | 강의 | 왜 코드 에이전트를 제대로 알아야 하는가 |
| 1교시 | 09:45 ~ 10:35 (50분) | 강의 20 + 실습 30 | 코드 에이전트란 무엇인가 |
| 2교시 | 10:50 ~ 11:45 (55분) | 강의 20 + 실습 35 | 에이전틱 루프와 컨텍스트 엔지니어링 |
| 점심 | 11:45 ~ 13:00 | - | - |
| 3교시 | 13:00 ~ 13:55 (55분) | 강의 20 + 실습 35 | 프로젝트 규칙과 에이전트 확장 |
| 4교시 | 14:10 ~ 15:00 (50분) | 강의 25 + 시연 10 + 실습 15 | 보안 · MCP · 자동화 · Ralph |
| 과제 | 15:15 ~ 16:15 (60분) | 팀 과제 | 나만의 에이전트 툴킷 만들기 |
| 발표 | 16:30 ~ 17:00 (30분) | 발표 + 마무리 | 팀 발표 + 더 알아보기 |

- **총 강의·시연**: 100분 (30%) / **총 실습·과제**: 235분 (70%)

---

## 오프닝: 왜 코드 에이전트를 제대로 알아야 하는가 (15분)

> 수업의 동기 부여와 전체 방향을 잡는 시간. 뒤에 진행할 내용과의 연결고리를 명확히 설명한다.

### 1. 환기: 요즘 코드 에이전트가 핫합니다

- "요즘 Claude Code 너무 핫하죠? 써보신 분들도 있고, 안 써보신 분들도 있으실 것 같습니다."
- "카카오톡 × ChatGPT Pro 29,000원 대란 때, 사신 분들 계시죠? 저도 사두었는데, 막상 Codex를 어떻게 쓸까 고민하시는 분들이 있을 것 같습니다."
  - 참고: [뉴시스 — 카카오톡 ChatGPT Pro 대란](https://www.newsis.com/view/NISX20260219_0003518383)
- 코드 에이전트 시장이 폭발적으로 성장 중: Claude Code, Codex, Gemini CLI, OpenCode, Aider, Copilot CLI...

### 2. 하네스(Harness)의 등장과 딜레마

- oh-my-claudecode, oh-my-codex, oh-my-openagent 같은 **하네스(Harness)** 프로젝트가 등장
- **Agent = Model + Harness**: 하네스란 AI 모델을 감싸는 런타임 인프라(도구 실행, 컨텍스트 관리, 안전 장치, 워크플로우 자동화)
- 하네스를 쓰면 성능이 확실히 좋아진다 — LangChain은 모델 변경 없이 하네스만 개선하여 벤치마크 52.8% → 66.5% 달성
  - 참고: [The Anatomy of an Agent Harness (LangChain)](https://blog.langchain.com/the-anatomy-of-an-agent-harness/)
  - 참고: [하네스 엔지니어링 (OpenAI)](https://openai.com/index/harness-engineering/)

### 3. 딜레마: "하네스가 뭘 해주는 건지 모르겠다"

- 실제 경험: "코드 에이전트를 공부하기 귀찮아서 하네스를 썼는데, 더 잘 쓰려면 결국 하네스 자체를 공부해야 하는 상황이 벌어진다"
- 하네스가 해주는 일이 **무엇인지** 이해하려면, 기본 동작을 먼저 알아야 한다
- **오늘의 목표**: 코드 에이전트의 기본적인 개념과 동작 원리를 정리하고, 하네스가 도와주는 게 무엇인지를 정확히 이해하는 시간

### 4. 오늘 수업의 흐름

1. **코드 에이전트 기본**: 에이전틱 루프, 도구, 어떻게 동작하는가
2. **컨텍스트 엔지니어링**: 에이전트의 "기억력"을 설계하는 기술
3. **커스터마이징**: 프로젝트 규칙, 에이전트, 스킬로 에이전트를 내 프로젝트에 맞게 제어
4. **생태계**: MCP, 보안, 자동화, Ralph — 실전에서 필요한 것들
5. **팀 과제**: 직접 에이전트 환경을 구성하고 시연

---

## 수업 목표

1. "코드 에이전트"가 단순 LLM 챗봇과 어떻게 다른지 설명할 수 있다
2. 에이전틱 루프(도구 사용 → 검증 → 반복)의 작동 원리를 이해한다
3. 컨텍스트 엔지니어링의 중요성을 이해하고 실천할 수 있다
4. 프로젝트 규칙(AGENTS.md), 커스텀 에이전트, 스킬로 에이전트를 제어할 수 있다
5. **커스텀 에이전트와 서브에이전트의 차이**를 설명하고 적절히 선택할 수 있다
6. MCP, 플러그인, CLI 도구의 차이를 이해하고 언제 무엇을 쓸지 판단할 수 있다
7. Ralph, 하네스, 샌드박스 등 에이전트 생태계의 주요 개념을 안다
8. 실제 프로젝트에서 "탐색 → 계획 → 구현 → 검증" 워크플로우를 수행할 수 있다

---

## 핵심 개념 체계

> 아래 개념들은 특정 도구에 국한되지 않는 **코드 에이전트의 보편적 원리**다.
> OpenCode로 실습하지만, 이 개념을 이해하면 Claude Code, Codex 등 어떤 코드 에이전트든 빠르게 적응할 수 있다.

### 개념 1: 에이전틱 루프 (Agentic Loop)

코드 에이전트는 단순히 "질문 → 답변"이 아니라 **자율적으로 도구를 사용하며 반복적으로 문제를 해결**한다.

```
사용자 요청 → [코드 읽기] → [계획 수립] → [코드 수정] → [명령 실행] → [결과 검증] → 완료/재시도
                  ↑                                                        ↓
                  └────────────────── 피드백 루프 ──────────────────────────┘
```

에이전트는 "생각하고(Think), 행동하고(Act), 관찰하는(Observe)" **ReAct 패턴**을 따른다. 이 루프가 코드 에이전트의 핵심이다.

- 참고: [Claude Code 아키텍처 — 에이전틱 루프](https://code.claude.com/docs/ko/overview)

### 개념 2: 도구 (Tools)

에이전트가 실제로 작업을 수행하는 수단. 모든 코드 에이전트는 유사한 도구 세트를 제공한다.

| 기능 | OpenCode | Claude Code | 하는 일 |
|------|----------|-------------|---------|
| 파일 읽기 | `read` | `Read` | 코드 파일의 내용을 읽어 컨텍스트에 추가 |
| 파일 수정 | `edit`, `write` | `Edit`, `Write` | 코드를 직접 수정하거나 새 파일 생성 |
| 파일 검색 | `grep`, `glob` | `Grep`, `Glob` | 코드베이스에서 패턴·파일명 검색 |
| 셸 실행 | `bash` | `Bash` | 빌드, 테스트, git 등 터미널 명령 실행 |
| 웹 검색 | `websearch` | `WebSearch` | 문서·API 레퍼런스 등 외부 정보 검색 |
| 웹 가져오기 | `webfetch` | `WebFetch` | URL의 내용을 직접 가져오기 |
| 사용자 질문 | `question` | `AskUserQuestion` | 모호한 상황에서 사용자에게 확인 |
| 서브에이전트 | `task` | `Agent` | 독립적인 하위 작업을 별도 에이전트에 위임 |
| 스킬 로딩 | `skill` | `Skill` | 미리 정의된 절차/지식을 필요할 때 로드 |

에이전트는 "마법"이 아니라 **제한된 도구를 조합**하여 작업한다. 도구를 이해하면 에이전트의 능력과 한계를 파악할 수 있다.

#### WebSearch/WebFetch는 단순한 curl인가?

> 자주 묻는 질문이다. WebSearch/WebFetch는 단순한 `curl` 래퍼가 아니다.

| 구분 | curl / fetch | WebSearch | WebFetch |
|------|-------------|-----------|---------|
| 반환 형식 | 원시 HTML | URL+제목 목록 (본문 아님) | HTML → **마크다운 변환** |
| 검색 기능 | 없음 | 검색 엔진 통합 | 없음 (URL 필요) |
| 컨텍스트 최적화 | 없음 | 결과 필터링 | 광고·네비게이션 제거 |
| 토큰 효율 | 낮음 (HTML 전체) | 높음 | 높음 (핵심 콘텐츠만) |
| 보안 제약 | 없음 | - | **대화에 나온 URL만** 접근 가능 (임의 URL 생성 불가) |
| 동적 필터링 | 없음 | Opus 4.6/Sonnet 4.6에서 코드 기반 필터링 | Opus 4.6/Sonnet 4.6에서 코드 기반 필터링 |
| 비용 | 무료 | **$10/1,000건** + 토큰 | 토큰 비용만 |

- **WebSearch → WebFetch 파이프라인**: WebSearch로 URL 후보를 찾고, WebFetch로 본문을 가져오는 2단계 구조
- **보안**: Claude는 대화에 나온 URL만 fetch 가능 — 임의 URL 생성 방지 (데이터 유출 차단)
- 참고: [WebFetch Tool (Anthropic API)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)
- 참고: [WebSearch Tool (Anthropic API)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)
- 참고: [Claude Code 기능 개요 — 내장 도구](https://code.claude.com/docs/ko/features-overview)

### 개념 3: 컨텍스트 엔지니어링 (Context Engineering)

2026년, 프롬프트 엔지니어링은 **컨텍스트 엔지니어링**으로 진화했다. 프롬프트 텍스트뿐 아니라 에이전트에게 제공하는 **전체 정보 환경**(메모리, 도구 정의, 대화 이력, 파일 내용)을 설계하는 것이 핵심이다.

- 참고: [Context Engineering for AI Agents (Anthropic)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

#### 컨텍스트 윈도우란?

에이전트의 컨텍스트 윈도우는 **작업 메모리**와 같다. 대화, 파일 내용, 명령 출력이 모두 토큰을 소비한다.

- Claude의 컨텍스트 윈도우에 대한 설명 참고 (이미지 포함):
  - [Context Windows — Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/context-windows)
  - `[📊 다이어그램]` 컨텍스트 윈도우의 입력/출력 구조 (platform.claude.com 문서의 이미지 캡처 삽입)

#### Claude Opus 4.6의 1M 컨텍스트 — 왜 중요한가?

- Claude Opus 4.6이 1M 토큰 컨텍스트로 확장 — 코드 에이전트 사용자들이 오래 기다려온 업데이트
- **왜 필요했는가?**
  - 대규모 코드베이스를 한 세션에서 탐색하려면 기존 200K 토큰은 부족했다
  - 에이전틱 루프가 반복될수록 컨텍스트가 빠르게 소진되는 문제
  - 서브에이전트에 위임하지 않고도 복잡한 작업을 한 세션에서 완료할 수 있게 됨
- 참고: [Claude Opus 4.6 — 1M Context GA](https://claude.com/blog/1m-context-ga)

#### 컨텍스트가 차면 성능이 떨어지는가? — 실전 논쟁

> 이 주제는 커뮤니티에서 활발히 논쟁 중이다. 양쪽 시각을 모두 다룬다.

**"/compact 로 충분하다" 진영**:
- 자동 압축(compaction)이 핵심 정보를 유지하면서 공간을 확보한다
- Claude Code는 자동으로 컨텍스트를 요약·압축하는 메커니즘이 있다
- `/compact` 후 작업을 계속하면 충분히 효과적이라는 의견
- 수동 `/compact`를 60~65% 시점에 사용하면 가장 깨끗한 요약 생성

**"새 세션을 시작하는 게 낫다" 진영**:
- **"Lost in the Middle" 현상** (Stanford/Google 연구): LLM은 긴 컨텍스트의 중간 부분 정보 검색 시 성능이 **30% 이상 하락** — 이는 어텐션 아키텍처에 내재된 위치 편향
  - 참고: [Lost in the Middle: How Language Models Use Long Contexts (arXiv)](https://arxiv.org/abs/2307.03172)
- **"Context Rot" 연구** (Chroma Research, 2025): 18개 프론티어 모델 전부 입력 길이 증가에 따라 성능 저하. 200K 윈도우 모델도 50K 토큰에서부터 유의미한 저하 시작
  - 참고: [Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://research.trychroma.com/context-rot)
- **실사용자 경험** (GitHub Issue #34685): Claude Opus 4.6 1M 사용자들이 보고 — "실효 품질은 300~400K 수준", "1M은 그냥 진행률 바가 길어졌을 뿐"
  - 참고: [Claude Opus 4.6 1M Context 사용자 보고](https://github.com/anthropics/claude-code/issues/34685)
- 압축 과정에서 미묘한 컨텍스트(코드의 의도, 이전 시도와 실패 이유)가 손실될 수 있다
- 참고: [Context Rot in Claude Code: Automatic Rotation](https://vincentvandeth.nl/blog/context-rot-claude-code-automatic-rotation)
- 참고: [Why Your Claude Code Sessions Keep Dying](https://www.turboai.dev/blog/claude-code-context-window-management)

**실전 권장안**:
- 하나의 명확한 작업 → 하나의 세션 (세션을 작게 유지)
- 무관한 작업을 한 세션에 혼합하지 않는다 ("주방 싱크" 지양)
- 2회 이상 같은 실패를 반복하면 새 세션에서 재시작
- `/compact`는 장기 작업 중간에 사용, 하지만 완전히 새로운 맥락의 작업은 새 세션

#### 컨텍스트 윈도우 실습: 실제로 확인하기

> 컨텍스트 윈도우가 어떻게 모델의 입력으로 들어가는지 직접 확인하는 실습

**확인 방법**:
1. **OpenCode의 디버그 모드**: 실제로 모델에 전송되는 메시지를 로그로 확인
2. **Anthropic API 직접 호출**: 시스템 프롬프트 + 도구 정의 + 대화 히스토리가 어떻게 구성되는지 확인
3. **토큰 카운터**: 현재 세션이 몇 토큰을 사용하고 있는지 확인

- `[💡 간단 실습]` API를 직접 호출하여 컨텍스트 윈도우 구성 요소 확인

**실전 전략**:
- **초기화**: 무관한 작업 간 `/clear`로 컨텍스트 정리
- **위임**: 탐색 작업은 서브에이전트에 맡겨 메인 컨텍스트 보호
- **압축**: 컨텍스트가 가득 차면 자동으로 요약·압축 (compaction)
- **세션 관리**: 2회 이상 실패 시 새 세션에서 재시작
- **"주방 싱크" 지양**: 하나의 세션에 무관한 작업을 혼합하지 않음

### 개념 4: 프로젝트 규칙 (Project Rules)

에이전트에게 "이 프로젝트에서는 이렇게 해"라고 지시하는 마크다운 파일. 모든 코드 에이전트가 지원하는 핵심 기능이다.

- 참고: [How to Write a Great AGENTS.md (GitHub Blog)](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)

#### 학술적 근거: ETH Zurich 연구 (2026)

> 프로젝트 규칙의 효과는 학술 연구로 검증되었다 — 그리고 결과는 놀랍다.

- 논문: ["Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"](https://arxiv.org/abs/2602.11988)
  - 저자: Gloaguen, Mündler, Müller, Raychev, Vechev (ETH Zurich SRI Lab)
  - 60,000+ 리포지토리에서 사용되는 프로젝트 규칙 파일의 **첫 대규모 실증 연구**

**핵심 발견**:
- **LLM이 자동 생성한 규칙 파일**: 성능 **-0.5~-2%** 하락, 인퍼런스 비용 **+20%** 증가
- **인간이 작성한 규칙 파일**: 성능 **+4%** 향상 (그러나 비용은 여전히 +19%)
- **차이**: 인간 작성 (+4%) vs LLM 생성 (-2%) = **6%p 차이** — 인간의 판단이 핵심

**효과적인 규칙 작성 가이드라인** (논문 기반):
1. LLM으로 자동 생성하지 말 것 — 8개 실험 중 5개에서 오히려 성능 저하
2. **최소한으로** 작성 — 규칙이 길수록 "불필요한 탐색"을 유발하여 비용만 증가
3. **도구 지시에 집중** — `uv` 사용 지시 시 에이전트의 도구 사용률 1.6배 증가
4. 코드베이스 개요(디렉토리 구조)는 쓰지 말 것 — 에이전트가 스스로 탐색하며, 개요가 도움이 되지 않음
5. README와 중복하지 말 것

> **"순응의 역설"**: 에이전트는 규칙을 충실히 따르지만, 나쁜 규칙도 따른다. 규칙이 불필요한 탐색을 유발하면 비용만 올리고 성공률은 떨어진다.

- 참고: [논문 전문](https://arxiv.org/html/2602.11988v1)
- 참고: [관련 논문 — AGENTS.md의 효율성 영향](https://arxiv.org/html/2601.20404v1) — 잘 작성된 규칙은 런타임 28.64% 감소, 출력 토큰 20% 감소

**OpenCode에서**:
- 파일명: `AGENTS.md` (CLAUDE.md도 호환)
- 전역: `~/.config/opencode/AGENTS.md`
- 프로젝트: 루트 디렉토리의 `AGENTS.md`
- 하위 디렉토리: 디렉토리별 `AGENTS.md`
- 자동 생성: `/init` 명령
- 참고: [OpenCode 규칙 문서](https://opencode.ai/docs/rules/)

**공통 원칙**:
- 모든 세션 시작 시 로드되어 시스템 프롬프트에 포함
- 간결하고 구체적일수록 잘 따름 (200줄 이하 권장)
- Git에 커밋하여 팀 전체가 공유
- 계층적 병합: 전역 → 프로젝트 → 디렉토리 (더 가까운 파일이 우선)

**작성 팁**:
- ✅ 에이전트가 추측할 수 없는 정보 (빌드 명령, 테스트 방법, 금지 사항)
- ✅ 프로젝트 고유 컨벤션 (코드 스타일, 네이밍, 아키텍처 결정)
- ❌ 에이전트가 코드를 읽어서 파악할 수 있는 정보
- ❌ 자명한 관행 ("깨끗한 코드를 작성하세요")

> **다른 도구에서**: Claude Code는 `CLAUDE.md`, Codex는 `AGENTS.md`(+`AGENTS.override.md`), Gemini CLI는 `GEMINI.md`

### 개념 5: 커스텀 에이전트 vs 서브에이전트

> 이 두 개념은 자주 혼동된다. 명확히 구분하자.

#### 커스텀 에이전트 (Custom Agent) — "역할을 정의한다"

**역할별로 특화된 에이전트를 정의**하여 도구 접근, 모델, 프롬프트를 분리한다. 사용자가 직접 호출하여 특정 역할을 수행하게 한다.

| 패턴 | 역할 | 도구 제한 | 누가 호출? |
|------|------|----------|-----------|
| **Build** | 코드 작성·수정 | 모든 도구 활성화 | 사용자가 `@build` |
| **Plan** | 분석·설계 | 읽기 전용 (edit/bash 비활성화) | 사용자가 `@plan` 또는 Tab |
| **Reviewer** | 코드 리뷰 | 읽기 전용 | 사용자가 `@reviewer` |
| **Explorer** | 코드베이스 탐색 | 읽기 + 검색만 | 사용자가 `@explorer` |

- 파일 위치: `.opencode/agents/*.md` (OpenCode), `.claude/agents/*.md` (Claude Code)
- 참고: [Claude Code 커스텀 에이전트](https://code.claude.com/docs/ko/sub-agents)

#### 서브에이전트 (Sub-agent) — "작업을 위임한다"

에이전트가 **자율적으로** 독립적인 하위 작업을 별도 컨텍스트에서 실행한다. 사용자가 아니라 **에이전트가** 필요할 때 호출한다.

| 특성 | 커스텀 에이전트 | 서브에이전트 |
|------|---------------|------------|
| **호출 주체** | 사용자 (`@reviewer`) | 에이전트 (자동으로) |
| **목적** | 역할 강제 (리뷰어는 수정 불가) | 컨텍스트 분리 (메인 오염 방지) |
| **컨텍스트** | 메인과 공유 가능 | 독립적 (별도 컨텍스트 윈도우) |
| **수명** | 사용자가 전환할 때까지 | 작업 완료 시 종료 |
| **비유** | 팀의 **직책** (리뷰어, 설계자) | 회의 중 **잠깐 나가서 확인** 해오는 사람 |

- `[📊 다이어그램]` 커스텀 에이전트 vs 서브에이전트 흐름도

#### 언제 무엇을 쓰나?

| 상황 | 선택 | 이유 |
|------|------|------|
| 코드 리뷰 시 수정을 방지하고 싶다 | **커스텀 에이전트** | 도구 제한으로 역할 강제 |
| 코드베이스 탐색 결과가 메인 컨텍스트를 오염시키지 않게 | **서브에이전트** | 독립 컨텍스트에서 실행 후 결과만 반환 |
| 프로젝트 표준 코드 스타일을 강제하고 싶다 | **커스텀 에이전트 + 프로젝트 규칙** | |
| 10개 파일을 병렬로 분석하고 싶다 | **서브에이전트** | 병렬 위임으로 속도 향상 |

### 개념 6: 스킬 (Skills)

재사용 가능한 절차/지식을 패키징하여 에이전트가 필요할 때 로드한다.
- 규칙(AGENTS.md)은 **항상** 적용, 스킬은 **필요할 때** 적용
- SKILL.md 형식: YAML frontmatter(name, description) + Markdown 절차
- 하나의 스킬 = 하나의 작업 (범위를 좁게)
- 참고: [Claude Code 스킬](https://code.claude.com/docs/en/skills), [OpenCode 스킬](https://opencode.ai/docs/skills/)

#### npx로 커뮤니티 스킬 설치

```bash
# 스킬 설치 명령 (npm 기반)
npx skills add vercel-labs/agent-browser

# 설치 과정:
# 1. npm으로 프로젝트를 다운로드
# 2. 각 코드 에이전트(Claude Code, Codex, OpenCode 등)에 맞는 경로에 자동 설치
#    - Claude Code → .claude/skills/{name}/SKILL.md
#    - OpenCode → .opencode/skills/{name}/SKILL.md
#    - Codex → .agents/skills/{name}/SKILL.md
# 3. 바로 사용 가능
```

- 커뮤니티 스킬 모음: [awesome-agent-skills (500+ 스킬)](https://github.com/VoltAgent/awesome-agent-skills)

#### 비슷한 개념들의 구분

| 개념 | 범위 | 언제 쓰나? | 비유 |
|------|------|-----------|------|
| **프로젝트 규칙** (AGENTS.md) | 항상 로드 | 프로젝트 컨벤션, 금지사항 | 사무실 규칙 |
| **스킬** (SKILL.md) | 필요할 때 로드 | 반복되는 워크플로우 | 매뉴얼 |
| **커스텀 에이전트** | 역할별 분리 | 역할을 강제 (리뷰어는 수정 불가) | 직책 |
| **서브에이전트** | 독립 컨텍스트 | 메인 컨텍스트 보호 + 병렬 처리 | 잠깐 확인해올 동료 |
| **MCP** | 외부 연동 | 코드 저장소 밖의 데이터/서비스 | USB 포트 |
| **플러그인** | 하네스 확장 | 하네스 자체의 동작 확장 | 브라우저 확장 프로그램 |
| **CLI 도구** | 로컬 실행 | 빌드, 테스트, 린트 등 | 도구 상자 |

### 개념 7: 권한과 보안

에이전트가 수행할 수 있는 작업의 범위를 제어한다.

#### 3단계 권한: `deny` > `ask` > `allow` (거부가 최우선)

- **allow**: 자동으로 실행 (신뢰하는 명령)
- **ask**: 실행 전 사용자 승인 요청 (기본값)
- **deny**: 절대 실행 불가

#### 샌드박스 격리 — 초보자를 위한 설명

> `[📊 다이어그램]` 샌드박스 격리 개념을 단계별로 설명하는 다이어그램 (슬라이드 제작 시 삽입)

**비유**: 에이전트를 "방 안에 가두는 것"

1. **격리 없음 (위험)**: 에이전트가 컴퓨터의 모든 파일에 접근 가능 — 잘못된 명령으로 시스템 파일 삭제 가능
2. **권한 제어 (기본)**: 에이전트가 뭔가 하기 전에 "이거 해도 돼?" 물어봄 — `ask` 모드
3. **OS 수준 샌드박스 (최상)**: 에이전트가 물리적으로 특정 디렉토리 밖에 접근 불가
   - **macOS**: Seatbelt — 커널 수준에서 파일 시스템 접근 제한
   - **Linux**: seccomp, namespaces — 시스템 콜 단위로 제한
   - Claude Code는 이 수준의 격리를 기본 제공
   - Codex는 OS 수준 격리 + 2단계 런타임 보호

- 참고: [Claude Code 보안 모델](https://code.claude.com/docs/ko/security)

#### 보안 위협: 프롬프트 주입 (Prompt Injection)

- OWASP Top 10 LLM 취약점 1위 (2025)
- 에이전트가 읽는 외부 데이터에 악의적 명령이 숨겨질 수 있음
- 방어: 샌드박스 격리, 네트워크 제한, 권한 최소화, 출력 검증

#### --dangerously-skip-permissions: 현실적 사용과 보안

> Ralph를 사용하면 사실상 이 플래그를 사용하는 것과 같다. 컨테이너/VM에서만 쓰라는 원칙은 현실적으로 지키기 어렵다.

**왜 사용하게 되는가?**
- Ralph (자율 루프) 실행 시 매번 승인을 누를 수 없음
- 비대화형 CI/CD 파이프라인에서 사용자 상호작용이 불가
- 반복적인 승인이 생산성을 크게 저해

**사용 시 보안 원칙**:
- ✅ 컨테이너/VM 내에서 사용하면 가장 안전 (격리된 환경)
- ✅ 신뢰할 수 있는 프로젝트에서만 사용 (외부 코드가 포함된 프로젝트는 주의)
- ✅ 네트워크 접근을 제한 (외부 서버로 데이터 유출 방지)
- ⚠️ 로컬 환경에서도 사용 가능하지만: 프로젝트 디렉토리 밖의 파일은 접근 차단 확인
- ❌ 공개 리포지토리를 클론한 직후 무조건 실행하지 말 것 (프롬프트 주입 위험)

- 참고: [Claude Code 보안 모델 — Sandboxing](https://code.claude.com/docs/en/sandboxing)
- 참고: [Claude Code 공식 Devcontainer](https://code.claude.com/docs/en/devcontainer) — Anthropic 권장 격리 환경
- 참고: [Thomas Wiegold — Why It's Dangerous (실제 사고 사례)](https://thomas-wiegold.com/blog/claude-code-dangerously-skip-permissions/)

**문서화된 실제 사고 사례** (3건):
1. **Wolak 사건** (2025.10): `rm -rf /` 실행 — 전체 사용자 파일 손실 (GitHub #10077)
2. **Reddit 사건** (2025.12): `rm -rf ~/` — 홈 디렉토리 전체 삭제 (키체인, 앱 데이터 포함)
3. **틸드 디렉토리 트릭** (2025.11): `~` 이름의 디렉토리 생성 후 `rm -rf *` 확장 시 홈 디렉토리 삭제

**Tier별 안전 사용 원칙**:
- **Tier 1 (필수)**: 반드시 Docker 컨테이너/VM 내에서 실행. Anthropic 공식 devcontainer 사용 권장
- **Tier 2 (강력 권장)**: 최소 권한 자격증명만 전달, `--disallowedTools` 백스톱, 세션 전 git commit
- **Tier 3 (대안 먼저 검토)**: `acceptEdits` 모드, `--allowedTools` 스코프 허용목록, Plan 모드

### 개념 8: MCP (Model Context Protocol)

외부 도구·서비스를 에이전트에 연결하는 개방형 표준 프로토콜. "AI의 USB-C"라고 불린다.

- 워크플로우에 **실제로 필요한 도구만** 연결 (무분별 추가 지양)
- 필요한 정보가 코드 저장소 밖에 있을 때 사용
- 예시: GitHub, Slack, Jira, 데이터베이스, 브라우저 DevTools 연동
- **주의**: MCP 도구 정의만으로 컨텍스트의 40~50%를 소비할 수 있음 — 꼭 필요한 것만

> **설정 방법**: OpenCode는 `opencode mcp add`, Claude Code는 `claude mcp add`
> 참고: [MCP 공식 사이트](https://modelcontextprotocol.io/)

#### MCP vs 플러그인 vs CLI 도구 — 무엇이 다른가?

| 구분 | MCP 서버 | 플러그인 | CLI 도구 |
|------|---------|---------|---------|
| **설치** | `claude mcp add` / `opencode mcp add` | `npm install` / 하네스 설정 | `apt/brew install` |
| **실행 위치** | 별도 프로세스 (JSON-RPC) | 하네스 내부 (라이프사이클 훅) | 셸에서 직접 실행 |
| **에이전트 연결** | 도구(tool)로 자동 등록 | 하네스 동작을 확장/수정 | `bash` 도구로 호출 |
| **컨텍스트 영향** | 도구 정의만큼 소비 (40~50%) | 최소 (훅이므로) | 없음 (실행 결과만) |
| **용도** | 외부 서비스 연동 (DB, API) | 하네스 워크플로우 자동화 | 빌드, 테스트, 린트 |
| **예시** | GitHub MCP, Slack MCP | Ralph Wiggum, oh-my-claudecode | git, npm, docker |

**Context7 — MCP vs 플러그인의 실제 차이** (구체적 사례):
- **MCP 형태**: `claude mcp add context7` — `resolve-library-id`와 `query-docs` 2개 도구 등록. **명시적 호출 필요** ("context7으로 검색해줘"). 도구 정의가 세션 시작 시 로드되어 컨텍스트 소비.
- **플러그인 형태**: 스킬 + docs-researcher 에이전트 + MCP 번들. "How do I configure X?" 같은 패턴 감지 시 **자동 트리거**. 독립 컨텍스트에서 문서 조회하여 메인 세션 오염 방지.
- **핵심 차이**: MCP는 "직접 호출해야 동작", 플러그인은 "알아서 동작" + 컨텍스트 격리
- **이점**: 에이전트의 학습 데이터 컷오프 이후의 최신 라이브러리 문서에 접근 가능. hallucination 방지.
- 참고: [Context7 Claude Code Plugin 분석](https://deepwiki.com/upstash/context7/9-claude-code-plugin)

> **컨텍스트 비용 주의**: MCP Tool Search (Sonnet 4+, Opus 4+)가 도구 정의를 지연 로드하여 컨텍스트 오버헤드를 줄여준다. 하지만 Tool Search가 없는 모델에서는 MCP 서버 하나당 수백~수천 토큰을 상시 소비한다.

#### CLI 에이전트의 우위 — 왜 터미널인가?

> 에이전틱 코딩에서 터미널 기반 CLI 에이전트가 IDE 기반 에이전트보다 유리하다는 논의가 활발하다.

| 장점 | 설명 |
|------|------|
| **전체 파일시스템 접근** | IDE는 열린 프로젝트만, CLI는 전체 시스템 |
| **셸 실행** | 빌드, 테스트, git, docker 등 네이티브 실행 |
| **파이프라인 통합** | `cat log | agent "분석해"` 등 Unix 파이프 활용 |
| **자동화** | 비대화형 모드로 CI/CD, cron 등에 통합 |
| **서버 환경** | SSH를 통해 원격 서버에서 직접 실행 |
| **리소스 효율** | IDE 없이 가볍게 실행, 여러 인스턴스 병렬 가능 |
| **MCP 활용** | CLI 에이전트는 MCP를 통해 외부 서비스와 직접 연동 |

- 참고: [The New Stack — AI Coding Tools in 2025: Welcome to the Agentic CLI Era](https://thenewstack.io/ai-coding-tools-in-2025-welcome-to-the-agentic-cli-era/)
- 참고: [InfoQ — Agentic Terminal: How Your Terminal Comes Alive with CLI Agents](https://www.infoq.com/articles/agentic-terminal-cli-agents/)
- 참고: [DevToolsAcademy — Cursor vs Claude Code](https://www.devtoolsacademy.com/blog/cursor-vs-claudecode/)
- 참고: [Qodo — Claude Code vs Cursor](https://www.qodo.ai/blog/claude-code-vs-cursor/)

**3가지 핵심 우위** (연구/아티클 종합):
1. **조합성(Composability)**: CLI 에이전트는 Unix 도구 — 파이프, 스크립트, CI에 내장 가능. IDE 에이전트는 GUI 앱
2. **인프라 근접성**: 터미널은 배포, 컨테이너, 시스템 운영이 이루어지는 곳. IDE는 이 계층과 단절
3. **대규모 자율성**: 여러 에이전트를 여러 리포에서 동시에 탭으로 관리 — IDE는 한 번에 한 프로젝트

### 개념 9: 비대화형 모드와 자동화

에이전트를 스크립트, CI/CD, 파이프라인에서 프로그래밍 방식으로 실행한다.

```bash
# OpenCode
opencode run "test_app.py를 실행하고 실패하면 수정해줘"

# 파이프라인 예시
cat error.log | opencode run "이 에러를 분석하고 수정 방안을 제시해"
```

> **다른 도구에서**: Claude Code는 `claude -p "..."`, Codex는 `codex exec "..."`
> 참고: [Claude Code 비대화형 사용](https://code.claude.com/docs/ko/features-overview)

### 개념 10: 코드 에이전트 확장 기능 (Features Overview)

> 아래는 [Claude Code 기능 개요](https://code.claude.com/docs/ko/features-overview)를 기반으로 정리한 코드 에이전트 확장 기능이다.
> 대부분의 CLI 코드 에이전트에서 유사하게 지원된다.

| 기능 | 설명 | 언제 사용? |
|------|------|-----------|
| **멀티에이전트** | 여러 에이전트를 병렬로 실행하여 작업 분담 | 대규모 리팩토링, 코드 리뷰 + 구현 병렬 |
| **Git 워크트리** | 독립된 브랜치에서 병렬 작업 | 서로 다른 접근법 동시 시도 |
| **훅 (Hooks)** | 도구 실행 전후에 커스텀 로직 삽입 | 자동 린팅, 보안 검사, 알림 |
| **메모리** | 프로젝트/사용자 정보를 세션 간 유지 | 사용자 선호도, 프로젝트 컨텍스트 축적 |
| **비대화형 모드** | 스크립트에서 에이전트 실행 | CI/CD, 자동화 파이프라인 |
| **Plan 모드** | 읽기 전용으로 분석·계획만 수행 | 코드 작성 전 전략 수립 |

- 참고: [Claude Code 기능 개요](https://code.claude.com/docs/ko/features-overview)

### 개념 11: Ralph — 자율 에이전트 루프

**Ralph**(Ralph Wiggum Loop)는 코드 에이전트를 bash 루프에서 반복 실행하여 **작업이 완료될 때까지 자율적으로 작업**하게 하는 기법이다.

```bash
# 가장 단순한 형태
while :; do cat PROMPT.md | claude-code ; done
```

**기원**: 2025년 7월, Geoffrey Huntley가 발표. 심슨 캐릭터 Ralph Wiggum의 "무지하지만 끈질긴" 특성에서 이름을 따왔다.

**핵심 원리**:
- 각 반복마다 새로운 컨텍스트 윈도우를 받지만, 파일시스템(코드, git 히스토리)을 통해 이전 작업을 관찰
- "무차별적이지만 끈질긴" 접근: 한 번에 완벽하게 하기보다 반복적으로 개선
- **실적**: $50,000 계약을 API 비용 $297로 완수한 사례

**공식 지원**:
- **Claude Code**: Anthropic이 공식 Ralph Wiggum 플러그인 제작. Stop Hook으로 에이전트 종료를 가로채 원래 프롬프트를 재주입
- **Codex**: `codex exec`의 장시간 자율 실행(25시간 무중단 사례) + Approval 모드
- **커뮤니티 도구**: Ralph TUI, Ralphy 등 에이전트 무관한 범용 루프 오케스트레이터

> **수업에서**: 학생들이 직접 Ralph를 실습하기는 어려우므로, 강사가 시연으로 보여준다.
>
> **출처**:
> - [Geoffrey Huntley의 Ralph 소개](https://ghuntley.com/ralph/)
> - [A Brief History of Ralph](https://www.humanlayer.dev/blog/brief-history-of-ralph)
> - [Claude Code 공식 Ralph 플러그인](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum)

### 개념 12: 하네스 엔지니어링 (Harness Engineering)

> 오프닝에서 소개한 하네스 개념을 좀 더 깊이 다룬다.

**Agent = Model + Harness**. 하네스란 AI 모델을 감싸는 **런타임 인프라**를 말한다.

**왜 알아야 하나?**
- "모델 문제가 아니라 설정 문제" — 하네스만 잘 구성해도 성능이 크게 달라진다
- LLM이 자동 생성한 하네스 설정은 오히려 성능을 해칠 수 있음 (ETH Zurich 연구)
- **인간이 의도적으로 설계한 하네스**만이 측정 가능한 개선을 가져온다

**대표적인 하네스 프로젝트**:

| 프로젝트 | 대상 | 역할 |
|----------|------|------|
| oh-my-claudecode (OMC) | Claude Code | 32개 전문 에이전트, 40+ 스킬, 멀티에이전트 오케스트레이션 |
| oh-my-codex (OMX) | Codex CLI | 작업 검사·재개·반복 자동화 |
| oh-my-openagent (OMO) | OpenCode | 멀티모델 라우팅, 40+ 라이프사이클 훅 |

**하네스 엔지니어링의 3가지 기둥** (OpenAI 발표, 2026.02):
1. **컨텍스트 엔지니어링**: 구조화된 문서가 Single Source of Truth
2. **아키텍처 제약**: 솔루션 공간을 제한하면 에이전트가 오히려 더 생산적
3. **엔트로피 관리**: 주기적 정리 에이전트로 코드 품질 유지

> **출처**:
> - [하네스 엔지니어링: 에이전트 우선 세계에서 Codex 활용하기](https://openai.com/index/harness-engineering/)
> - [Software 3.0 시대, Harness를 통한 조직 생산성 저점 높이기](https://toss.tech/article/harness-for-team-productivity)
> - [The Anatomy of an Agent Harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/)

### 개념 13: 효과적인 프롬프팅과 에이전틱 패턴

| 원칙 | 설명 |
|------|------|
| **검증 수단 제공** | 테스트, 예상 출력을 포함해 에이전트가 스스로 확인하게 한다 |
| **탐색 → 계획 → 구현** | 바로 코딩하지 않고 먼저 코드를 읽고 계획을 세운다 (Plan 모드) |
| **구체적 컨텍스트** | 파일, 제약사항, 기존 패턴을 명시한다. 모호한 요청은 모호한 결과를 낳는다 |
| **작업 분해** | 큰 작업을 독립적인 작은 단위로 나눈다 |
| **TDD + 에이전트** | 테스트를 먼저 작성하면 에이전트가 스펙으로 활용 — 결과 품질 극적 향상 |
| **검토 후 적용** | 에이전트 결과를 맹신하지 않고 diff를 검토하고 테스트를 실행한다 |

- 참고: [Claude Code 모범 사례](https://code.claude.com/docs/ko/best-practices)

**2026년 주요 에이전틱 패턴**:
- **Spec-Driven Development (SDD)**: 스펙 문서를 먼저 작성하고 에이전트에게 구현을 맡기는 패턴
- **Writer-Reviewer**: 하나의 에이전트가 생성, 다른 에이전트가 검증하는 이중 루프
- **Fan-out/Fan-in**: 독립 작업을 여러 서브에이전트에 병렬 위임 후 결과 합산
- **Orchestrator-Worker**: 조정자가 전문 작업자들에게 일을 분배

### 개념 14: 유용한 플러그인/MCP 소개

#### Context7

최신 라이브러리 문서를 실시간으로 에이전트에게 제공한다.
- **문제**: 에이전트의 학습 데이터 컷오프 이후 업데이트된 API를 모른다
- **해결**: Context7이 실시간으로 최신 문서를 검색하여 에이전트에게 주입
- MCP 또는 플러그인 형태로 설치 가능
- 참고: [Context7 GitHub](https://github.com/upstash/context7)

#### Agent Browser

에이전트가 웹 브라우저를 직접 조작할 수 있게 한다.
- 웹 페이지 방문, 폼 입력, 버튼 클릭, 스크린샷 캡처
- 웹앱 테스트 자동화에 유용
- `npx skills add vercel-labs/agent-browser`로 설치
- 참고: [Agent Browser GitHub](https://github.com/vercel-labs/agent-browser)

---

## 교시별 상세 계획

### 1교시 (09:45~10:35): 코드 에이전트란 무엇인가

#### 강의 (20분)

**1. LLM과 코드 에이전트의 차이**

| 구분 | LLM 채팅 (ChatGPT, Claude 등) | 코드 에이전트 (CLI Agent) |
|------|------------------------------|-------------------------|
| 상호작용 | 질문 → 답변 (1회) | 요청 → 자율적 다단계 실행 |
| 파일 접근 | 없음 (복사-붙여넣기) | 직접 읽기·쓰기·검색 |
| 명령 실행 | 없음 | 셸 명령 직접 실행 |
| 검증 | 사용자가 직접 | 에이전트가 테스트 실행·결과 확인 |
| 컨텍스트 | 대화 창에 붙여넣은 것만 | 전체 코드베이스 탐색 가능 |

**2. 에이전틱 루프 개념 소개** (→ 개념 1)

**3. 코드 에이전트 생태계 개관**
- VSCode 플러그인형: GitHub Copilot, Continue
- IDE 통합형: Cursor, Windsurf
- **CLI Code Agent** (오늘의 주제): Claude Code, Codex, OpenCode, Gemini CLI, Copilot CLI, Aider
  - Gemini CLI도 있지만 오늘은 다루지 않음 — 개념은 동일하므로 자유롭게 적용 가능
- CLI 에이전트의 장점: 프로젝트 전체 접근, 셸 실행, 자동화·파이프 가능, 버전관리 통합

**4. 어떤 모델을 선택할 것인가**
- 벤치마크 사이트: [LMArena](https://lmarena.ai/), [Artificial Analysis](https://artificialanalysis.ai/), [OpenRouter Rankings](https://openrouter.ai/rankings)
- 코딩 벤치마크: SWE-bench, Aider Polyglot, LiveCodeBench
- 2026년 3월 기준 주요 모델: Claude Opus 4.6 (1M context), GPT-5.3-Codex, Gemini 3.1 Pro

**5. 오늘의 실습 도구: OpenCode**
- 오픈소스 CLI 코드 에이전트 (Go 기반) — [github.com/anomalyco/opencode](https://github.com/anomalyco/opencode)
- 75+ LLM 프로바이더 지원 (Anthropic, OpenAI, Google, OpenRouter, Zen 무료)
- TUI (터미널 UI) + CLI 모드
- **무료 모델을 사용**: OpenCode Zen 또는 OpenRouter 무료 모델
- 각자 구독 중인 도구가 있으면 자유롭게 사용 가능하나, 수업은 OpenCode 위주로 진행
- 참고: 무료 대안 — [free-claude-code](https://github.com/Alishahryar1/free-claude-code)

#### 실습 0: OpenCode 설치 및 첫 대화 (30분)

**I DO (5분)**: 강사가 설치 및 모델 연결 시연
```bash
# WSL2 + Ubuntu 24.04 환경
npm install -g opencode   # 또는 curl 설치
opencode                   # TUI 진입
# /connect → OpenCode Zen 선택 → API 키 입력
# /models → 무료 모델 선택
```

**WE DO (10분)**: 학생들이 함께 설치하고 첫 대화
```
안녕하세요. 간단한 Python 함수를 하나 만들어주세요.
```
- 에이전트가 도구를 사용하는 과정 관찰 (어떤 도구가 호출되는지 확인)

**YOU DO (15분)**: 자유 탐색
- 에이전트에게 다양한 요청 시도 (파일 읽기, 코드 수정, 테스트 실행 등)
- **관찰 포인트**: 에이전트가 어떤 도구를 어떤 순서로 사용하는지 기록
- 도구 사용 패턴과 개념 1(에이전틱 루프)을 연결지어 생각하기

---

### 2교시 (10:50~11:45): 에이전틱 루프와 컨텍스트 엔지니어링

#### 강의 (20분)

**1. 에이전틱 루프 심화** (→ 개념 1, 2)
- 도구 호출 흐름 실제 시연: 에이전트가 `read → grep → edit → bash` 순으로 사용하는 과정
- 각 도구가 하는 역할과 에이전트가 선택하는 이유
- WebSearch/WebFetch vs curl 차이 설명 (→ 개념 2)

**2. 컨텍스트 엔지니어링** (→ 개념 3)
- 프롬프트 엔지니어링의 진화: 프롬프트만이 아니라 **전체 정보 환경**을 설계
- 컨텍스트 윈도우 = 에이전트의 "작업 메모리", 유한하다
  - [Context Windows — Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/context-windows)의 이미지 캡처 활용
- Claude Opus 4.6의 1M 컨텍스트가 왜 중요한가 (→ 개념 3)
  - [Claude Opus 4.6 — 1M Context GA](https://claude.com/blog/1m-context-ga)
- 컨텍스트 성능 논쟁: /compact vs 새 세션 (→ 개념 3)
- 실전 전략: 초기화, 위임, 압축, 세션 관리

**3. 효과적인 프롬프팅** (→ 개념 13)
- 나쁜 예 vs 좋은 예:
  - ❌ "로그인 버그 수정해줘"
  - ✅ "세션 타임아웃 후 로그인 실패 현상. src/auth/ 토큰 리프레시 로직 확인. 재현 테스트 작성 후 수정해줘"
- **검증 수단 제공**: 에이전트가 스스로 성공을 확인할 수 있는 테스트나 기준 포함
- **Plan 모드**: 바로 코딩하지 않고, 먼저 코드를 읽고 계획을 세운 뒤 실행

#### 실습 1: 프롬프팅 비교 체험 + 컨텍스트 확인 (35분)

미리 준비된 Python 프로젝트(간단한 TODO 앱)에서 실습.

**I DO (10분)**: 강사가 같은 작업을 다른 프롬프트로 시연
1. **나쁜 프롬프트**: "할 일 삭제 기능 추가해" → 결과 관찰
2. **좋은 프롬프트**: "todo_app.py에 delete_todo(todo_id) 함수를 추가해. 존재하지 않는 ID면 ValueError를 발생시켜. test_app.py에 테스트를 추가하고 실행해서 통과하는지 확인해" → 결과 관찰
3. **차이 비교**: 같은 작업이지만 결과의 품질이 다르다
4. **컨텍스트 윈도우 확인**: 현재 세션이 사용 중인 토큰 수 확인, 디버그 로그로 모델 입력 구조 확인

**WE DO (10분)**: 함께 진행
- 에이전트에게 "할 일 완료 표시 기능을 추가해. 테스트도 작성해" 요청
- **관찰 포인트**: 에이전트가 어떤 도구를 어떤 순서로 사용하는지
- 결과 검증: `python test_app.py`
- 컨텍스트 관리 체험: `/clear` 후 새 작업 시작

**YOU DO (15분)**: 독립 실습
- 에이전트에게 자신만의 기능 추가 요청 (필터링, 정렬, 우선순위 등)
- **도전**: 같은 요청을 모호한 프롬프트 → 구체적 프롬프트로 두 번 시도하고 결과 비교
- Plan 모드 체험: Plan 에이전트(Tab)로 먼저 계획 → Build 에이전트로 구현

---

### 3교시 (13:00~13:55): 프로젝트 규칙과 에이전트 확장

#### 강의 (20분)

**1. 프로젝트 규칙** (→ 개념 4)
- AGENTS.md가 무엇인지, 왜 필요한지
- 학술적 근거: [arxiv 2602.11988](https://arxiv.org/pdf/2602.11988) 논문 인사이트
- 계층적 설정: 전역 → 프로젝트 → 디렉토리
- 효과적인 규칙 작성법 (구체적, 간결, 검증 가능)
- [How to Write a Great AGENTS.md (GitHub Blog)](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- `/init`으로 자동 생성

**2. 커스텀 에이전트 vs 서브에이전트** (→ 개념 5 — 명확히 구분)
- 커스텀 에이전트: 역할 정의 (사용자가 호출)
- 서브에이전트: 작업 위임 (에이전트가 자율적으로 호출)
- `[📊 다이어그램]` 두 개념의 차이를 시각적으로 설명
- 도구 제한으로 역할 강제
- 참고: [Claude Code 서브에이전트](https://code.claude.com/docs/ko/sub-agents)

**3. 스킬과 확장 기능** (→ 개념 6, 10)
- 규칙 vs 스킬: "항상 적용" vs "필요할 때 로드"
- npx로 커뮤니티 스킬 설치: `npx skills add vercel-labs/agent-browser`
- 코드 에이전트 확장 기능 개요 (멀티에이전트, 훅, 메모리, Plan 모드 등)
- 참고: [Claude Code 기능 개요](https://code.claude.com/docs/ko/features-overview)

#### 실습 2: 코드 에이전트 커스터마이징 (35분)

**I DO (10분)**: AGENTS.md 유무에 따른 행동 차이 시연
- 같은 코드 수정 요청을 AGENTS.md **없이** 실행 → 결과 관찰
- AGENTS.md에 "모든 함수에 타입 힌트와 한국어 docstring을 작성할 것" 추가 후 **같은 요청** 실행
- **핵심 포인트**: 같은 요청이지만 규칙의 유무로 결과의 품질이 달라진다

**WE DO (15분)**: 함께 진행
1. AGENTS.md 직접 작성 (코드 컨벤션, 테스트 규칙, 금지사항)
2. 커스텀 리뷰 에이전트 정의 (write/edit/bash 비활성화)
3. `@reviewer`로 코드 리뷰 요청
4. 도구가 차단되어 수정 없이 리뷰만 하는지 확인

**YOU DO (10분)**: 독립 실습
1. 자신만의 AGENTS.md 규칙 추가 (예: "테스트 없이 코드를 수정하지 말 것")
2. 규칙이 적용되는지 확인 — 의도적으로 테스트 없이 수정 요청을 해보고 에이전트의 반응 관찰
3. (도전) 간단한 스킬 파일 작성: `.opencode/skills/add-feature/SKILL.md`
4. (도전) `npx skills add` 로 커뮤니티 스킬 설치 체험

---

### 4교시 (14:10~15:00): 보안 · MCP · 자동화 · Ralph

#### 강의 (25분)

**1. 권한과 샌드박스** (→ 개념 7)
- `[📊 다이어그램]` 샌드박스 격리 3단계 다이어그램 (슬라이드에서 단계별 애니메이션)
  - 격리 없음 → 권한 제어 → OS 수준 샌드박스
- --dangerously-skip-permissions: 현실적 사용과 보안 원칙 (→ 개념 7)
- 프롬프트 주입 위협과 방어

**2. MCP와 도구 생태계** (→ 개념 8, 14)
- MCP vs 플러그인 vs CLI 도구 — 무엇이 다른가 (→ 개념 8 테이블)
- Context7: MCP와 플러그인 두 가지 형태의 차이
- CLI 에이전트의 우위 — 왜 터미널이 유리한가 (→ 개념 8)
- 유용한 플러그인 소개: Context7, Agent Browser (→ 개념 14)
- 주의: MCP 도구 정의의 컨텍스트 소비 문제

**3. 비대화형 모드와 자동화** (→ 개념 9)
- `opencode run`으로 스크립트에서 에이전트 실행
- 파이프라인: `cat log | opencode run "분석해"`
- CI/CD 자동화 가능성

**4. 하네스 엔지니어링 심화** (→ 개념 12)
- 하네스 엔지니어링의 3가지 기둥
- 오프닝에서 제기한 "하네스를 이해하려면 기본을 알아야 한다"의 결론

**5. Ralph — 자율 에이전트 루프** (→ 개념 11)
- Ralph의 기원과 원리
- 공식 지원: Claude Code 플러그인, Codex의 장시간 자율 실행

#### 시연: Ralph와 하네스 (10분)

강사가 직접 보여주는 시연 (학생은 관찰):
1. **Ralph 루프 시연**: Claude Code에서 Ralph Wiggum 플러그인으로 자율 작업 수행
   - PROMPT.md 작성 → Ralph 루프 실행 → 에이전트가 반복적으로 개선하는 과정 관찰
2. **하네스 시연**: oh-my-claudecode의 멀티에이전트 오케스트레이션
   - 하네스가 없을 때 vs 있을 때의 작업 효율 비교

#### 실습 3: 자동화와 MCP 체험 (15분)

**WE DO (10분)**: 함께 진행
- 비대화형 모드로 테스트 자동화: `opencode run "test_app.py를 실행하고 실패하면 수정해줘"`
- Build → Reviewer 에이전트 워크플로우: 기능 구현 → 리뷰 → 피드백 반영
- (선택) MCP 서버 추가 체험: Context7 MCP 추가

**YOU DO (5분)**: 독립 실습
- 자신만의 비대화형 자동화 명령 작성
- (선택) Agent Browser 스킬 설치: `npx skills add vercel-labs/agent-browser`

---

### 과제 시간 (15:15~16:15): 나만의 에이전트 툴킷

#### 과제 개요 (60분)

**주제**: 팀별로 특정 시나리오를 선택하고, 그 시나리오에 최적화된 에이전트 환경을 구성하여 시연한다.

**시나리오 예시** (택 1 또는 자유 주제):
- 데이터 분석팀의 코드 리뷰 자동화
- 오픈소스 프로젝트 관리자의 이슈 트리아지
- 주니어 개발자를 위한 코드 멘토링 에이전트
- DevOps 엔지니어의 인프라 코드 관리
- 기술 문서 자동 생성 파이프라인

**필수 산출물**:
1. **AGENTS.md** — 시나리오에 맞는 프로젝트 규칙 (구체적 컨벤션, 빌드/테스트 명령 포함)
2. **커스텀 에이전트 1개 이상** — 역할에 맞는 도구 제한 설정
3. **Before/After 시연** — 설정 전/후로 같은 요청의 결과 차이 보여주기
4. **노하우 정리** — 효과적이었던 프롬프트, 규칙 작성 팁 등

**선택 산출물** (가산점):
- 스킬 1개 이상 작성
- 비대화형 자동화 스크립트
- 멀티에이전트 워크플로우
- MCP 또는 플러그인 연동

**제출 방법**:
- 노션 갤러리에 제출 (스크린샷 + 설정 파일 + 노하우 포함)
- 제출 후 다른 팀의 과제에 👍 댓글로 투표

---

### 발표 · 마무리 (16:30~17:00)

#### 팀 발표 (20분)

- 👍 투표 상위 3팀이 앞에서 발표 (각 5~7분)
- **발표 내용**: 선택한 시나리오, 구성한 에이전트 환경, Before/After 시연, 핵심 노하우
- 다른 팀원들과 Q&A

#### 더 알아보기 · 마무리 (10분)

**수업 핵심 복습**:
- 코드 에이전트 = 에이전틱 루프 + 도구 + 컨텍스트 엔지니어링
- AGENTS.md, 커스텀 에이전트, 스킬로 에이전트를 내 프로젝트에 맞게 제어
- 커스텀 에이전트 ≠ 서브에이전트: 역할 정의 vs 작업 위임
- MCP, 플러그인, CLI 도구 — 상황에 맞는 선택
- Ralph, 하네스로 자동화 레벨업
- 오늘 OpenCode로 배운 개념은 Claude Code, Codex 등 어디서든 적용 가능

---

## 실습 목록

| # | 실습명 | 교시 | 시간 | 핵심 개념 | 형태 |
|---|--------|------|------|----------|------|
| 0 | OpenCode 설치 및 첫 대화 | 1 | 30분 | 도구, 에이전틱 루프 | I DO → WE DO → YOU DO |
| 1 | 프롬프팅 비교 체험 + 컨텍스트 확인 | 2 | 35분 | 컨텍스트 엔지니어링, 프롬프팅 | I DO → WE DO → YOU DO |
| 2 | 코드 에이전트 커스터마이징 | 3 | 35분 | AGENTS.md, 에이전트, 스킬, 권한 | I DO → WE DO → YOU DO |
| 3 | 자동화와 MCP 체험 | 4 | 15분 | 비대화형, MCP, 멀티에이전트 | WE DO → YOU DO |
| - | 시연: Ralph와 하네스 | 4 | 10분 | Ralph, 하네스 | I DO (시연) |
| 4 | 나만의 에이전트 툴킷 | 과제 | 60분 | 전체 통합 | 팀 과제 |

---

## 도구 비교 부록

> 부록 레퍼런스. "OpenCode로 배우지만, 다른 도구에도 동일한 개념이 있다"는 점을 보여준다.

| 개념 | Claude Code | Codex | OpenCode |
|------|-------------|-------|----------|
| **프로젝트 규칙** | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` |
| **전역 설정** | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` | `~/.config/opencode/AGENTS.md` |
| **커스텀 에이전트** | `.claude/agents/*.md` | `config.toml [agents]` | `.opencode/agents/*.md` |
| **스킬** | `.claude/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` | `.opencode/skills/*/SKILL.md` |
| **권한** | allow/ask/deny (설정·CLI) | prefix_rule (Starlark) | allow/ask/deny (JSON) |
| **샌드박스** | OS 수준 (Seatbelt/seccomp) | OS 수준 + 2단계 런타임 | 권한 기반 |
| **컨텍스트 관리** | /clear, /compact, subagent | /compact, /fork, threads | 세션, Compaction 에이전트 |
| **MCP** | `claude mcp add` | `config.toml [mcp_servers]` | `opencode mcp add` |
| **비대화형** | `claude -p "..."` | `codex exec "..."` | `opencode run "..."` |
| **Plan 모드** | Shift+Tab / `/plan` | Shift+Tab / `/plan` | Tab → Plan 에이전트 |
| **훅** | PreToolUse/PostToolUse | Rules (Starlark) | - |
| **멀티에이전트** | Agent teams, background tasks | max_threads, CSV 배치 | @subagent, 서브세션 |
| **설치** | `curl -fsSL claude.ai/install.sh \| bash` | `npm i -g @openai/codex` | `npm i -g opencode` |

---

## 참고 자료

### 공식 문서

- **Claude Code**: https://code.claude.com/docs/ko/overview
- **Claude Code 기능 개요**: https://code.claude.com/docs/ko/features-overview
- **Claude Code 모범 사례**: https://code.claude.com/docs/ko/best-practices
- **Claude Code 서브에이전트**: https://code.claude.com/docs/ko/sub-agents
- **Claude Code 스킬**: https://code.claude.com/docs/en/skills
- **Claude Code 훅**: https://code.claude.com/docs/en/hooks
- **Claude Code 보안**: https://code.claude.com/docs/ko/security
- **Claude 컨텍스트 윈도우**: https://platform.claude.com/docs/en/build-with-claude/context-windows
- **Claude Opus 4.6 1M Context GA**: https://claude.com/blog/1m-context-ga
- **Codex**: https://developers.openai.com/codex/overview
- **Codex AGENTS.md**: https://developers.openai.com/codex/guides/agents-md/
- **Codex 모범 사례**: https://developers.openai.com/codex/learn/best-practices/
- **OpenCode**: https://opencode.ai/docs/
- **OpenCode 규칙**: https://opencode.ai/docs/rules/
- **OpenCode 스킬**: https://opencode.ai/docs/skills/
- **MCP 공식**: https://modelcontextprotocol.io/

### 학술 논문 / 연구

- **프로젝트 규칙의 효과 (ETH Zurich)**: https://arxiv.org/abs/2602.11988
- **AGENTS.md 효율성 영향**: https://arxiv.org/html/2601.20404v1
- **Lost in the Middle (Stanford/Google)**: https://arxiv.org/abs/2307.03172
- **Context Rot (Chroma Research)**: https://research.trychroma.com/context-rot

### 핵심 블로그/아티클

- **Context Engineering for AI Agents (Anthropic)**: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- **How to Write a Great AGENTS.md (GitHub Blog)**: https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/
- **하네스 엔지니어링 (OpenAI)**: https://openai.com/index/harness-engineering/
- **Software 3.0 시대 Harness (Toss Tech)**: https://toss.tech/article/harness-for-team-productivity
- **The Anatomy of an Agent Harness (LangChain)**: https://blog.langchain.com/the-anatomy-of-an-agent-harness/
- **카카오톡 ChatGPT Pro 대란 (뉴시스)**: https://www.newsis.com/view/NISX20260219_0003518383

### 더 알아보기

**한국어 학습 자료**:
- Claude Code 마스터 가이드 (AI영끌맨): https://claudeguide-dv5ktqnq.manus.space/
- Claude Code 위키독스: https://wikidocs.net/book/19104

**커뮤니티 자료**:
- awesome-claude-code (28.7k stars): https://github.com/hesreallyhim/awesome-claude-code
- awesome-agent-skills (500+ 스킬): https://github.com/VoltAgent/awesome-agent-skills
- free-claude-code (무료 래퍼): https://github.com/Alishahryar1/free-claude-code

**하네스 / Ralph**:
- Geoffrey Huntley의 Ralph 소개: https://ghuntley.com/ralph/
- A Brief History of Ralph: https://www.humanlayer.dev/blog/brief-history-of-ralph
- Claude Code 공식 Ralph 플러그인: https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum

**CLI 에이전트 / 컨텍스트 엔지니어링**:
- Agentic CLI Era (The New Stack): https://thenewstack.io/ai-coding-tools-in-2025-welcome-to-the-agentic-cli-era/
- Agentic Terminal (InfoQ): https://www.infoq.com/articles/agentic-terminal-cli-agents/
- Context Rot in Claude Code (vincentvandeth.nl): https://vincentvandeth.nl/blog/context-rot-claude-code-automatic-rotation
- Why Your Claude Code Sessions Keep Dying (turboai.dev): https://www.turboai.dev/blog/claude-code-context-window-management
- --dangerously-skip-permissions 보안 (Thomas Wiegold): https://thomas-wiegold.com/blog/claude-code-dangerously-skip-permissions/

**에이전틱 코딩 트렌드**:
- 2026 Agentic Coding Trends Report (Anthropic): https://resources.anthropic.com/2026-agentic-coding-trends-report
- Complete Guide to Agentic Coding 2026: https://www.teamday.ai/blog/complete-guide-agentic-coding-2026

**플러그인/MCP**:
- Context7: https://github.com/upstash/context7
- Agent Browser: https://github.com/vercel-labs/agent-browser

**벤치마크/모델 선택**:
- OpenRouter Rankings: https://openrouter.ai/rankings
- LMArena: https://lmarena.ai/
- Artificial Analysis: https://artificialanalysis.ai/

---

## 참고사항

- 수업은 1일 과정이다 (09:30~17:00)
- **실습 환경**: WSL2 + Ubuntu 24.04 LTS
- OpenCode를 실습 도구로 사용하되, 배우는 개념은 어떤 코드 에이전트에도 적용되는 보편적 원리이다
- **무료 모델**(OpenCode Zen)을 사용하므로 학생에게 비용 부담이 없다
- 각자 구독 중인 도구(Claude Code, Codex, Gemini CLI 등)가 있으면 자유롭게 사용 가능
- Gemini CLI는 앞부분에서 간단히 언급만 하고, 이후 개념 설명에서는 별도로 다루지 않음
- 실습 프로젝트는 Python 기반 TODO 앱을 사용한다
- 과제는 노션 갤러리에 제출하고 👍 투표로 최우수 3팀을 선정하여 발표한다
