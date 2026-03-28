# 오프닝: 왜 코드 에이전트를 제대로 알아야 하는가

<callout icon="📖" color="blue_bg">
	**학습 목표:** 수업의 동기를 이해하고, 코드 에이전트의 현재 위상과 오늘 배울 내용의 전체 흐름을 파악한다.
</callout>

> 이 시간은 수업의 방향을 잡는 15분짜리 오프닝이다.
> 뒤에 진행할 내용과의 연결고리를 명확히 설정한다.

---

## 1. 환기: 요즘 코드 에이전트가 핫합니다

"요즘 Claude Code 너무 핫하죠?"
써보신 분들도 있고, 안 써보신 분들도 있을 것이다.

"카카오톡 × ChatGPT Pro 29,000원 대란 때, 사신 분들 계시죠?"
막상 Codex를 어떻게 쓸지 고민하시는 분들이 있을 것이다.

→ 참고: [뉴시스 — 카카오톡 ChatGPT Pro 대란](https://www.newsis.com/view/NISX20260219_0003518383)

---

### 코드 에이전트 시장이 폭발적으로 성장 중이다

| 유형 | 도구 |
|------|------|
| **CLI 코드 에이전트** (오늘의 주제) | Claude Code, Codex, OpenCode, Gemini CLI, Aider |
| IDE 통합형 | Cursor, Windsurf |
| VSCode 플러그인형 | GitHub Copilot, Continue |

2026년 3월, Anthropic의 [2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)에 따르면:
- 엔지니어의 역할이 **"코드 작성자"에서 "에이전트 오케스트레이터"**로 전환 중
- TELUS는 13,000개 AI 솔루션을 만들며 코드 배포 속도 **30% 향상**
- Zapier는 **89% AI 도입률** 달성, 800개 이상의 에이전트를 내부 배포

MIT Missing Semester 2026에도 [Agentic Coding 강의](https://missing.csail.mit.edu/2026/agentic-coding/)가 추가되었다.
에이전틱 코딩은 이제 정규 CS 교육과정의 일부다.

---

## 2. 하네스(Harness)의 등장과 딜레마

oh-my-claudecode, oh-my-codex, oh-my-openagent 같은 **하네스(Harness)** 프로젝트가 등장했다.

> **Agent = Model + Harness**

**하네스**란 AI 모델을 감싸는 런타임 인프라다.
→ 도구 실행, 컨텍스트 관리, 안전 장치, 워크플로우 자동화를 담당한다.

하네스를 쓰면 성능이 확실히 좋아진다.
LangChain은 모델 변경 없이 **하네스만 개선**하여 벤치마크 **52.8% → 66.5%**를 달성했다.

→ 참고: [The Anatomy of an Agent Harness (LangChain)](https://blog.langchain.com/the-anatomy-of-an-agent-harness/)
→ 참고: [하네스 엔지니어링 (OpenAI)](https://openai.com/index/harness-engineering/)

---

## 3. 딜레마: "하네스가 뭘 해주는 건지 모르겠다"

실제 경험을 공유한다.

"코드 에이전트를 공부하기 귀찮아서 하네스를 썼는데, 더 잘 쓰려면 결국 하네스 자체를 공부해야 하는 상황이 벌어진다."

하네스가 해주는 일이 **무엇인지** 이해하려면 → 기본 동작을 먼저 알아야 한다.

> **오늘의 목표**: 코드 에이전트의 기본적인 개념과 동작 원리를 정리하고, 하네스가 도와주는 게 무엇인지를 정확히 이해하는 시간

---

## 4. 오늘 수업의 흐름

| 순서 | 주제 | 핵심 질문 |
|------|------|-----------|
| **1교시** | 코드 에이전트 기본 | 에이전트는 어떻게 동작하는가? |
| **2교시** | 컨텍스트 엔지니어링 | 에이전트의 "기억력"을 어떻게 설계하는가? |
| **3교시** | 프로젝트 규칙과 확장 | 에이전트를 내 프로젝트에 어떻게 맞추는가? |
| **4교시** | 보안 · MCP · 자동화 · Ralph | 실전에서 필요한 것들은? |
| **과제** | 나만의 에이전트 툴킷 | 직접 구성하고 시연하기 |

<callout icon="💡" color="gray_bg">
	**핵심 메시지**: OpenCode로 실습하지만, 오늘 배우는 개념은 Claude Code, Codex, Gemini CLI 등 **어떤 코드 에이전트에도** 적용된다.
</callout>

---

## 핵심 정리

- 코드 에이전트 시장이 폭발적으로 성장 중이다 (CLI 에이전트가 주류로 부상)
- 하네스가 성능을 높여주지만, 기본을 모르면 하네스도 제대로 쓸 수 없다
- 오늘 배우는 개념은 특정 도구에 종속되지 않는 **보편적 원리**다
