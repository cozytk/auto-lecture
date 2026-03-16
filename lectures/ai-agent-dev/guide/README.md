# AI Agent 전문 개발 과정 강의 가이드

## 수강 대상

- AI 개발자: LLM 기반 애플리케이션 개발 경험이 있는 개발자
- 데이터 엔지니어: 데이터 파이프라인 구축 경험이 있고 AI Agent에 관심 있는 엔지니어
- 기술 리더: AI Agent 도입을 검토하는 팀/조직의 기술 의사결정자

## 학습 목표

1. AI Agent의 문제 정의부터 MVP 구현까지 전 과정을 직접 설계하고 구현할 수 있다
2. MCP(Function Calling), RAG, Hybrid 아키텍처의 차이를 이해하고 상황에 맞게 선택할 수 있다
3. LangGraph를 활용하여 Agent의 제어 흐름과 상태를 체계적으로 관리할 수 있다
4. Agent 품질 평가 체계를 설계하고 운영 환경에서의 모니터링·장애 대응 전략을 수립할 수 있다
5. 실무형 AI Agent MVP를 완성하고 아키텍처를 설명할 수 있다

## 사전 요구사항

- Python 프로그래밍 중급 이상
- REST API 개념 이해
- LLM(ChatGPT, Claude 등) 사용 경험
- Git 기본 사용법
- (권장) Docker 기본 사용법

## 실습 환경

### LLM API

본 과정은 **OpenRouter**를 통해 LLM API를 호출합니다. OpenRouter는 OpenAI 호환 API를 제공하므로, 다른 모델/프로바이더로 쉽게 교체할 수 있습니다.

| 항목 | 값 |
|------|-----|
| API Provider | [OpenRouter](https://openrouter.ai) |
| 기본 모델 | `moonshotai/kimi-k2` (Kimi-K2) |
| Base URL | `https://openrouter.ai/api/v1` |
| Python SDK | `openai` (OpenAI 호환) |

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")
```

> **다른 모델로 교체하려면** `MODEL` 환경변수만 변경하면 됩니다.
> 예: `MODEL=anthropic/claude-sonnet-4` 또는 `MODEL=openai/gpt-4o`

### 환경 변수 설정

```bash
export OPENROUTER_API_KEY="sk-or-..."
export MODEL="moonshotai/kimi-k2"  # 선택: 기본값 사용 시 생략 가능
```

### 실행 환경

- **기본**: Linux (Ubuntu 기준)
- **호환**: macOS (Homebrew 기반 안내 포함)
- **Python**: 3.10 이상

## 핵심 기술 스택

- LLM Strategy (프롬프트 엔지니어링, Structured Output)
- RAG (Chunking, Embedding, Retrieval)
- MCP (Function Calling, Tool 설계)
- LangGraph (제어 흐름, 상태 관리)
- Hybrid Architecture (MCP + RAG 통합)

## 수업 일정표

| 일차 | 교시 | 주제 | 시간 | 파일 |
|------|------|------|------|------|
| **Day 1** | 1교시 | Agent 문제 정의와 과제 도출 | 2h | [day1-session1.md](day1-session1.md) |
| | 2교시 | LLM 동작 원리 및 프롬프트 전략 심화 | 2h | [day1-session2.md](day1-session2.md) |
| | 3교시 | Agent 기획서 구조화 | 2h | [day1-session3.md](day1-session3.md) |
| | 4교시 | MCP · RAG · Hybrid 구조 판단 | 2h | [day1-session4.md](day1-session4.md) |
| **Day 2** | 1교시 | Agent 4요소 구조 설계 | 2h | [day2-session1.md](day2-session1.md) |
| | 2교시 | LangGraph 기반 제어 흐름 설계 | 2h | [day2-session2.md](day2-session2.md) |
| | 3교시 | Tool 호출 통제 & Validation | 2h | [day2-session3.md](day2-session3.md) |
| | 4교시 | 구조 리팩토링 & 확장성 설계 | 2h | [day2-session4.md](day2-session4.md) |
| **Day 3** | 1교시 | MCP(Function Calling) 고급 설계 | 2h | [day3-session1.md](day3-session1.md) |
| | 2교시 | 외부 API · 데이터 연동 최적화 | 2h | [day3-session2.md](day3-session2.md) |
| | 3교시 | RAG 성능을 결정하는 4가지 요소 | 2h | [day3-session3.md](day3-session3.md) |
| | 4교시 | Hybrid 아키텍처 설계 | 2h | [day3-session4.md](day3-session4.md) |
| **Day 4** | 1교시 | Agent 품질 평가 체계 설계 | 2h | [day4-session1.md](day4-session1.md) |
| | 2교시 | Prompt · RAG · Tool 성능 개선 전략 | 2h | [day4-session2.md](day4-session2.md) |
| | 3교시 | 로그 · 모니터링 · 장애 대응 설계 | 2h | [day4-session3.md](day4-session3.md) |
| | 4교시 | 확장 가능한 서비스 아키텍처 | 2h | [day4-session4.md](day4-session4.md) |
| **Day 5** | 1교시 | 프로젝트 설계 확정 | 2h | [day5-session1.md](day5-session1.md) |
| | 2교시 | 핵심 기능 구현 | 2h | [day5-session2.md](day5-session2.md) |
| | 3교시 | 성능 개선 & 안정화 | 2h | [day5-session3.md](day5-session3.md) |
| | 4교시 | 최종 시연 및 발표 | 2h | [day5-session4.md](day5-session4.md) |

## Day 2 운영 묶음

Day 2는 **이론 3 : 실습 7** 비율로 운영한다.
세션 가이드는 유지한다.
운영 동선은 별도 Day 2 묶음으로 연결한다.

| 구분 | 파일 | 설명 |
|------|------|------|
| 운영 개요 | [day2-overview.md](day2-overview.md) | Day 2 전체 진행 순서, 실습 맵, 종료 체크리스트 |
| Session 1 | [day2-session1.md](day2-session1.md) | Agent 4요소 구조 설계 |
| Session 2 | [day2-session2.md](day2-session2.md) | LangGraph 기반 제어 흐름 설계 |
| Session 3 | [day2-session3.md](day2-session3.md) | Tool 호출 통제 & Validation |
| Session 4 | [day2-session4.md](day2-session4.md) | 구조 리팩토링 & 확장성 설계 |
| Lab Pack | [`../labs/day2/README.md`](../labs/day2/README.md) | Day 2 실습 패키지 진입점 |
| Slide Deck | [`../slides/day2-slides.md`](../slides/day2-slides.md) | Day 2 전용 슬라이드 덱 |

## 핵심 산출물

- 아키텍처 다이어그램 (MCP/RAG/Hybrid 구조도)
- Golden Test Set & 평가표
- 실무형 Agent MVP (개인 프로젝트)

## 참고 자료

- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [Anthropic MCP 스펙](https://modelcontextprotocol.io/)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
