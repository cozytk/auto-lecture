# 00_basics -- 프레임워크 기초 실습

LangChain, LangGraph, Deep Agents 세 프레임워크의 전반적인 사용법을 익히는 기초 실습입니다.
본격적인 LangGraph 워크플로 설계에 들어가기 전, 각 프레임워크의 핵심 개념과 차이점을 빠르게 체험합니다.

## 학습 목표

- LLM 호출의 기본 구조(메시지 역할, 스트리밍, 배치)를 이해한다
- LangChain으로 Tool 기반 ReAct 에이전트를 만들고 실행한다
- LangGraph로 상태 기반 그래프 워크플로를 구성한다
- Deep Agents로 내장 도구가 포함된 올인원 에이전트를 체험한다
- 세 프레임워크의 차이점을 비교하고 적합한 상황을 판단한다

## 사전 준비

- Python 3.11+
- OpenAI API 키 (필수)
- Tavily API 키 (보너스 노트북용, 선택)
- 프로젝트 루트에서 `uv sync` 실행 후 `.env` 파일에 API 키 설정

## 노트북 구성

| 순서 | 파일 | 주제 | 핵심 내용 |
|------|------|------|-----------|
| 0 | `00_setup.ipynb` | 환경 설정 | `.env` 로드, ChatOpenAI 초기화, 모델 동작 확인 |
| 1 | `01_llm_basics.ipynb` | LLM 기초 | 메시지 역할(system/human/ai), `invoke`/`stream`/`batch` 세 가지 호출 방식 |
| 2 | `02_langchain_basics.ipynb` | LangChain 입문 | `@tool` 데코레이터, `create_agent()`, ReAct 루프 |
| 3 | `03_langchain_memory.ipynb` | 멀티턴 메모리 | `InMemorySaver`, `thread_id`로 세션 분리, 스트리밍 관찰 |
| 4 | `04_langgraph_basics.ipynb` | LangGraph 입문 | `StateGraph`, 노드/엣지 정의, `MessagesState`, 그래프 시각화 |
| 5 | `05_deep_agents_basics.ipynb` | Deep Agents 입문 | `create_deep_agent()`, 내장 도구(파일/셸/계획), 커스텀 도구 추가 |
| 6 | `06_comparison.ipynb` | 프레임워크 비교 | 세 프레임워크 특성 비교, 선택 기준, 학습 경로 안내 |
| Bonus | `bonus_mini_project.ipynb` | 미니 프로젝트 | Tavily 웹 검색 + 요약 에이전트 (Deep Agents & LangChain 비교) |

## 실습 흐름

```
00_setup ─── 환경 확인
    │
01_llm_basics ─── LLM 호출 기초 (메시지, 스트리밍, 배치)
    │
02_langchain_basics ─── Tool 정의 & ReAct 에이전트
    │
03_langchain_memory ─── 대화 기억 & 세션 관리
    │
04_langgraph_basics ─── 상태 그래프 워크플로
    │
05_deep_agents_basics ─── 올인원 에이전트 체험
    │
06_comparison ─── 세 프레임워크 비교 정리
    │
bonus_mini_project ─── 종합 프로젝트 (웹 검색 + 요약)
```

## 노트북별 상세 설명

### 00. 환경 설정

API 키를 `.env`에 설정하고 `ChatOpenAI`로 모델이 정상 동작하는지 확인합니다.
선택적으로 LangSmith/Langfuse 트레이싱을 연동할 수 있습니다.

### 01. LLM 기초

LLM과 소통하는 세 가지 메시지 역할(`SystemMessage`, `HumanMessage`, `AIMessage`)을 배웁니다.
같은 질문에 다른 시스템 메시지를 넣어 응답이 어떻게 달라지는지 실험하고,
`invoke()`, `stream()`, `batch()` 세 가지 호출 방식의 차이를 직접 확인합니다.

### 02. LangChain 입문

`@tool` 데코레이터로 Python 함수를 에이전트 도구로 변환합니다.
`create_agent()`로 ReAct 에이전트를 생성하고, 도구 호출 -> 관찰 -> 최종 답변의 흐름을 추적합니다.

### 03. 멀티턴 메모리

상태 없는 에이전트의 한계를 확인한 뒤, `InMemorySaver`로 대화 기억을 추가합니다.
`thread_id`로 세션을 분리하고, 스트리밍 모드로 에이전트의 내부 단계를 실시간 관찰합니다.

### 04. LangGraph 입문

`StateGraph`의 세 가지 구성 요소(State, Node, Edge)를 학습합니다.
단어 세기 단일 노드 -> 대문자 변환 + 카운팅 파이프라인 -> LLM 챗봇 그래프로 점진적으로 복잡도를 높여가며,
각 단계에서 그래프를 시각화합니다.

### 05. Deep Agents 입문

`create_deep_agent()`로 파일 관리, 셸 실행, 작업 계획 등 내장 도구가 포함된 에이전트를 생성합니다.
커스텀 도구를 추가하는 방법과 `system_prompt`로 에이전트 행동을 제어하는 방법을 실습합니다.

### 06. 프레임워크 비교

동일한 작업("3+4?")을 세 프레임워크로 구현하며 추상화 수준과 코드 구조를 비교합니다.
프레임워크 선택 가이드와 이후 학습 경로를 안내합니다.

### Bonus. 미니 프로젝트

Tavily 웹 검색 API를 커스텀 도구로 정의하고, Deep Agents와 LangChain 각각으로
"검색 + 요약" 에이전트를 구현합니다. 스트리밍으로 에이전트의 실행 과정을 실시간 관찰합니다.

## 주요 라이브러리

| 라이브러리 | 용도 |
|-----------|------|
| `langchain-openai` | ChatOpenAI 모델 |
| `langchain` | 도구, 에이전트, 메시지 |
| `langgraph` | StateGraph, 체크포인터 |
| `deepagents` | Deep Agents 하네스 |
| `tavily-python` | 웹 검색 API (보너스) |

## 소요 시간

전체 약 **2시간 30분** (보너스 포함 3시간)

| 구분 | 노트북 | 시간 |
|------|--------|------|
| I DO (강사 시연) | 00 ~ 04 | ~70분 |
| WE DO (함께 실습) | 05 | ~20분 |
| YOU DO (자율 실습) | 06 | ~10분 |
| Bonus | bonus_mini_project | ~30분 |
