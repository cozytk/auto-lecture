# Day 5 MVP 프로젝트

## 개요

Day 1~4에서 학습한 Agent 설계·구현·평가 역량을 총동원하여, 개인별 AI Agent MVP를 완성하는 종합 프로젝트이다.

## 일정

| 시간 | 세션 | 활동 | 산출물 |
|------|------|------|--------|
| 09:00~11:00 | Session 1 | 프로젝트 설계 확정 | 설계서, Golden Test Set |
| 11:00~13:00 | Session 2 | 핵심 기능 구현 | 동작하는 MVP 코드 |
| 14:00~16:00 | Session 3 | 성능 개선 & 안정화 | 성능 리포트, 개선된 코드 |
| 16:00~18:00 | Session 4 | 최종 시연 및 발표 | 발표 완료, 평가표 |

## 프로젝트 구조

```
day5-mvp-project/
├── README.md                              # 이 파일
├── src/
│   ├── main.py                            # Agent 진입점
│   ├── agent.py                           # LangGraph Agent 정의
│   ├── tools.py                           # Tool 정의
│   ├── rag.py                             # RAG 파이프라인 (ChromaDB)
│   ├── config.py                          # 설정 관리
│   └── evaluation.py                      # 평가 스크립트
├── data/
│   └── golden_test_set.json               # Golden Test Set
└── artifacts/
    ├── project-design-template.md         # 프로젝트 설계서 템플릿
    ├── performance-report-template.md     # 성능 리포트 템플릿
    └── presentation-template.md           # 발표 구성 템플릿
```

## 시작하기

### 1. 환경 설정

```bash
cd labs/day5-mvp-project

# 가상환경 생성 (uv 사용)
uv venv
source .venv/bin/activate

# 의존성 설치
uv pip install langchain langchain-openai langchain-anthropic langgraph chromadb langsmith pydantic python-dotenv

# 환경변수 설정
cp .env.example .env
# .env 파일을 열어 API 키 입력
```

### 2. 환경변수 (.env)

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
LANGSMITH_API_KEY=lsv2_...
LANGSMITH_PROJECT=day5-mvp
LANGCHAIN_TRACING_V2=true
```

### 3. 실행

```bash
python src/main.py
```

### 4. 평가

```bash
python src/evaluation.py
```

## 체크리스트

### Session 1: 설계 확정

```
[ ] artifacts/project-design-template.md 작성 완료
[ ] 아키텍처 선택 (MCP / RAG / Hybrid) 및 근거 기술
[ ] MoSCoW 분류 (Must 3개 이하)
[ ] 평가 기준 설정 (정량 지표 3개 이상)
[ ] data/golden_test_set.json에 테스트 케이스 10개 작성
[ ] 강사 확인 완료
```

### Session 2: 핵심 기능 구현

```
[ ] Agent 기본 루프 동작 (agent.py)
[ ] 핵심 Tool/RAG 기능 구현 (tools.py / rag.py)
[ ] End-to-end 연결 (main.py)
[ ] 수동 테스트 3개 케이스 통과
[ ] Must 항목 전부 완성
```

### Session 3: 성능 개선 & 안정화

```
[ ] Golden Test Set 최초 실행 (baseline 기록)
[ ] 개선 루프 최소 1회 완료
[ ] 안정화 체크리스트 통과
[ ] 시연 시나리오 3개 준비 및 테스트
[ ] artifacts/performance-report-template.md 작성 완료
```

### Session 4: 발표

```
[ ] 발표 환경 준비 (터미널, API 키, 데이터)
[ ] 10분 Demo + 5분 Q&A 완료
[ ] 평가표 제출
```

## 제출물

1. **프로젝트 코드**: `src/` 디렉토리 전체
2. **설계서**: `artifacts/project-design-template.md`
3. **성능 리포트**: `artifacts/performance-report-template.md`
4. **Golden Test Set**: `data/golden_test_set.json`
