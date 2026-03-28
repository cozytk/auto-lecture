# Lab Manager 실행 결과 요약: mcp-vs-cli

## 실행 정보
- 실행일: 2026-03-21
- 스킬 버전: old (skill-snapshot/lab-manager/SKILL.md)
- 입력: topic = mcp-vs-cli
- 가이드 경로: lectures/mcp-vs-cli/guide/

## 생성된 실습 목록

### 01-build-mcp-server (코드 실습)
- **유형**: 코드 실습 (README + Justfile + src/ + solution/)
- **실습 목적**: 기존 CLI 도구(git)를 MCP 서버로 래핑하여 MCP의 동작 원리를 체득
- **3단계 구성**:
  - I DO (10분): 강사가 git status/log를 MCP 도구로 시연
  - WE DO (15분): git_status, git_log 도구를 함께 구현
  - YOU DO (15분): git_diff, git_branch_list 도구를 독립 구현
- **생성 파일**:
  - `labs/01-build-mcp-server/README.md` — 실습 가이드
  - `labs/01-build-mcp-server/Justfile` — setup, run, test, clean 자동화
  - `labs/01-build-mcp-server/src/i-do/server.py` — 완성 코드 (도구 4개)
  - `labs/01-build-mcp-server/src/we-do/server.py` — 스캐폴드 (TODO 2개)
  - `labs/01-build-mcp-server/src/you-do/server.py` — 템플릿 (TODO 2개)
  - `labs/01-build-mcp-server/solution/server.py` — YOU DO 정답 코드

### 02-cli-vs-mcp-comparison (README 중심 실습)
- **유형**: README 중심 실습 (README + artifacts/)
- **실습 목적**: CLI와 MCP의 구조적 차이를 비교 분석하고 시나리오별 선택 기준 수립
- **3단계 구성**:
  - I DO (5분): 강사가 Jira CLI vs MCP 의사결정 과정을 시연
  - WE DO (10분): CLI vs MCP 비교표를 함께 완성 + DB 조회 시나리오 분석
  - YOU DO (15분): 5개 시나리오에 대한 독립 의사결정 기록서 작성
- **생성 파일**:
  - `labs/02-cli-vs-mcp-comparison/README.md` — 실습 가이드
  - `labs/02-cli-vs-mcp-comparison/artifacts/comparison-table-example.md` — 비교표 모범 답안
  - `labs/02-cli-vs-mcp-comparison/artifacts/decision-record-example.md` — 의사결정 기록서 모범 답안 (2개 시나리오)

## 테스트 결과

| 항목 | 결과 |
|------|------|
| Docker 사용 가능 여부 | 가능 (Docker 28.5.2) |
| just setup | 통과 — 4개 환경 모두 uv init + mcp[cli] 설치 성공 |
| just test | 통과 — i-do, we-do, you-do, solution 서버 모두 로드 성공 |
| README 중심 실습 | 해당 없음 (코드 실행 불필요) |

## 실습 시간 배분

| 실습 | I DO | WE DO | YOU DO | 합계 |
|------|------|-------|--------|------|
| 01-build-mcp-server | 10분 | 15분 | 15분 | 40분 |
| 02-cli-vs-mcp-comparison | 5분 | 10분 | 15분 | 30분 |
| **전체** | **15분** | **25분** | **30분** | **70분** |

## 피드백

`lectures/mcp-vs-cli/labs/feedback.md`에 5개 보강 항목 기록:
1. Session 2에 MCP 서버 코드 스니펫 추가 필요
2. stdio vs SSE 실습 스코프 안내 필요
3. Session 3에 벤치마크 데이터(TES 202 vs 152) 반영 필요
4. 일정표에 실습 시간 배분 명시 필요 (현재 실습 총 70분 > 수업 1시간)
5. MCP Inspector 사전 준비 안내 추가 권장
