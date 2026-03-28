# 에이전틱 코딩 입문: 코드 에이전트의 이해와 활용

## 수강 대상

**주니어~미드레벨 개발자** (WSL2 + Ubuntu 24.04 LTS 환경)

- 프로그래밍 경험이 있으나 AI 코드 에이전트는 처음이거나 초보인 개발자
- ChatGPT, Claude 등 LLM 채팅은 사용해봤지만, CLI 코드 에이전트는 본격적으로 사용하지 않은 분
- Python 기초 문법을 알고 있으면 실습에 충분

## 학습 목표

1. "코드 에이전트"가 단순 LLM 챗봇과 어떻게 다른지 설명할 수 있다
2. 에이전틱 루프(도구 사용 → 검증 → 반복)의 작동 원리를 이해한다
3. 컨텍스트 엔지니어링의 중요성을 이해하고 실천할 수 있다
4. 프로젝트 규칙(AGENTS.md), 커스텀 에이전트, 스킬로 에이전트를 제어할 수 있다
5. 커스텀 에이전트와 서브에이전트의 차이를 설명하고 적절히 선택할 수 있다
6. MCP, 플러그인, CLI 도구의 차이를 이해하고 언제 무엇을 쓸지 판단할 수 있다
7. Ralph, 하네스, 샌드박스 등 에이전트 생태계의 주요 개념을 안다
8. 실제 프로젝트에서 "탐색 → 계획 → 구현 → 검증" 워크플로우를 수행할 수 있다

## 사전 요구사항

- WSL2 + Ubuntu 24.04 LTS 설치 완료
- Node.js 18+ 설치 (`npm` 사용 가능)
- Python 3.10+ 설치
- Git 기본 사용법 숙지
- 터미널 기본 조작 가능 (`cd`, `ls`, `cat` 등)

## 수업 일정표

| 일차 | 구분 | 주제 | 시간 | 시간대 | 형태 | 파일 |
|------|------|------|------|--------|------|------|
| 사전 | 세션 0 | 실습 환경 세팅 가이드 | 자율 | - | 사전 과제 | [day1-session0.md](day1-session0.md) |
| 1일차 | 1교시 | 오프닝 + 코드 에이전트란 무엇인가 | 60분 | 9:30 ~ 10:30 | 강의 20 + 실습 30 | [opening.md](opening.md), [day1-session1.md](day1-session1.md) |
| 1일차 | 2교시 | 에이전틱 루프와 컨텍스트 엔지니어링 | 55분 | 10:45 ~ 11:40 | 강의 20 + 실습 35 | [day1-session2.md](day1-session2.md) |
| 1일차 | (점심) | - | 80분 | 11:40 ~ 13:00 | - | - |
| 1일차 | 3교시 | 프로젝트 규칙과 에이전트 확장 | 45분 | 13:00 ~ 13:45 | 강의 20 + 실습 25 | [day1-session3.md](day1-session3.md) |
| 1일차 | 4교시 | 보안 · MCP · 자동화 · Ralph | 45분 | 14:00 ~ 14:45 | 강의 25 + 시연 10 + 실습 10 | [day1-session4.md](day1-session4.md) |
| 1일차 | 5교시 | 나만의 에이전트 툴킷 만들기 | 60분 | 15:00 ~ 16:00 | 팀 과제 | day1-session4.md 내 포함 |
| 1일차 | 발표 | 팀 발표 + 핵심 복습 | 30분 | 16:15 ~ 16:45 | 발표 | day1-session4.md 내 포함 |
| 1일차 | 사후테스트 | 사후테스트 | - | 17:00 ~ | 테스트 | - |

- **총 강의·시연**: 약 100분 (30%)
- **총 실습·과제**: 약 235분 (70%)

## 실습 환경

- **OS**: WSL2 + Ubuntu 24.04 LTS
- **실습 도구**: [OpenCode](https://opencode.ai/) (무료 모델 사용)
- 각자 구독 중인 도구(Claude Code, Codex, Gemini CLI 등)가 있으면 자유롭게 사용 가능
- 무료 대안: [free-claude-code](https://github.com/Alishahryar1/free-claude-code)

## 실습 목록

| # | 실습명 | 교시 | 시간 | 핵심 개념 |
|---|--------|------|------|----------|
| 0 | OpenCode 설치 및 첫 대화 | 1교시 | 30분 | 도구, 에이전틱 루프 |
| 1 | 프롬프팅 비교 체험 + 컨텍스트 확인 | 2교시 | 35분 | 컨텍스트 엔지니어링, 프롬프팅 |
| 2 | 코드 에이전트 커스터마이징 | 3교시 | 35분 | AGENTS.md, 에이전트, 스킬 |
| 3 | 자동화와 MCP 체험 | 4교시 | 15분 | 비대화형, MCP |
| - | 시연: Ralph와 하네스 | 4교시 | 10분 | Ralph, 하네스 |
| 4 | 나만의 에이전트 툴킷 | 과제 | 60분 | 전체 통합 |

## 참고 자료

### 공식 문서

- [Claude Code 개요](https://code.claude.com/docs/ko/overview)
- [Claude Code 기능 개요](https://code.claude.com/docs/ko/features-overview)
- [Claude Code 모범 사례](https://code.claude.com/docs/ko/best-practices)
- [Claude Code 서브에이전트](https://code.claude.com/docs/ko/sub-agents)
- [Claude 컨텍스트 윈도우](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Codex 개요](https://developers.openai.com/codex/overview)
- [OpenCode 문서](https://opencode.ai/docs/)
- [MCP 공식](https://modelcontextprotocol.io/)

### 학술 논문

- [Evaluating AGENTS.md (ETH Zurich, arxiv 2602.11988)](https://arxiv.org/abs/2602.11988)

### 핵심 블로그/아티클

- [Context Engineering for AI Agents (Anthropic)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [How to Write a Great AGENTS.md (GitHub Blog)](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- [하네스 엔지니어링 (OpenAI)](https://openai.com/index/harness-engineering/)
- [The Anatomy of an Agent Harness (LangChain)](https://blog.langchain.com/the-anatomy-of-an-agent-harness/)
- [The 80% Problem in Agentic Coding (Addy Osmani)](https://addyo.substack.com/p/the-80-problem-in-agentic-coding)
- [2026 Agentic Coding Trends Report (Anthropic)](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)

### 더 알아보기

- [awesome-claude-code (28.7k stars)](https://github.com/hesreallyhim/awesome-claude-code)
- [awesome-agent-skills (500+ 스킬)](https://github.com/VoltAgent/awesome-agent-skills)
- [Claude Code 마스터 가이드 (AI영끌맨)](https://claudeguide-dv5ktqnq.manus.space/)
- [Agentic Coding — MIT Missing Semester 2026](https://missing.csail.mit.edu/2026/agentic-coding/)
- [Geoffrey Huntley — Ralph](https://ghuntley.com/ralph/)
