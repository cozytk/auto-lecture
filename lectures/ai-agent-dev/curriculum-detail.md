## 교육 개요
- MCP・RAG・Hybird 아키텍처 기반 AI Agent MVP 직접 설계, 구현하고 운영하는 역량까지 내재화

## 1일차 (문제 정의 & 설계)
### 1교시 - Agent 문제 정의와 과제 도출
- Agent 문제 정의와 과제 도출
    - 이 과정에서의 정의
        - RAG는 **기법(technique)**이고, Agent는 **아키텍처 패턴(architecture)**
        - 엄밀히는, RAG도 Agent 내부에서 하나의 도구로 쓰일 수 있음
        - 우리는 **고정 파이프라인(Fixed Pipeline)**이라는 관점에서 RAG를 이야기
            - 단순 RAG. 입력 -> 검색 -> 생성 -> 출력.
- LLM 동작 원리 및 프롬프트 전략 심화
    - 프롬프트 엔지니어링
        - Zero-shot, Few-shot, CoT 전략 소개
    - Structured Output 및 JSON Schema 응답 통제 전략 소개
    - 비용・Latency 관점의 호출 최적화 설계
    - 컨텍스트 엔지니어링
        - 프롬프트 엔지니어링에서 컨텍스트 엔지니어링으로의 확장
        - 컨텍스트 엔지니어링 대상
        - DeepAgents를 활용했을 때, 컨텍스트 엔지니어링 범위 

- MCP・RAG・Hybrid 구조 판단
    - MCP 구조 및 Tool 설계 기준 이해
        - [실습] MCP 간단 서버 및 클라이언트 코드
    - RAG 구성 요소 설계 전략
        - RAG 파이프라인 어떻게 구성할지
    - 

> 전체적으로 이 부분에서 LLM, RAG, Agent, MCP, CLI, SKILLS 등 구성 요소들 전부 소개하고 진행.

## 2일차 (제어 흐름 & 상태)
- LangGraph 기반 제어 흐름 설계
- Tool 호출 통제 및 Validation
- 구조 리팩토링 및 확장성 설계

> LangGraph의 그래프 자체에 집중하여 수업을 진행.
> LangGraph에서 제어 흐름을 어떻게 만드는지를 위주로 설명. Tool 호출을 통제하고 유효성을 검증. 확장이 가능하도록 설계.

## 3일차 (MCP・RAG 구현)
- 외부 API・데이터 연동 최적화
- RAG 성능 결정 4요소 및 튜닝
- Hybrid 아키텍처 설계 판단

> 외부 API, RAG 등 어떻게 붙이는지 위주로 설명
> CLI, Skills와도 비교해가면서 설명하면 좋을 듯.

## 4일차 (평가 & 운영전략)
- Agent 품질 평가 체계 설계
- 로그・모니터링・장애 대응 설계
- 확실 가능한 서비스 아키텍처

> Agent의 품질을 평가할 수 있는 체계를 설계
> Anthropic의 skill-creator를 기반으로 아이디어를 많이 얻을 수 있을 것으로 보임
> 로그, 모니터링, 장애 대응 체계에 대해서 설계

## 5일차 (MVP Day)
- 개인별 Agent 프로젝트 MVP 완성
- 성능 개선 및 안정화 집중 개발
- 최종 시연 및 구조 설명 발표
- Best Architecture 선정

### 산출물
- 아키텍처 다이어그램
- Golden Set & 평가표
- 실무형 Agent MVP