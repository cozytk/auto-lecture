# 실습 피드백: mcp-vs-cli

생성일: 2026-03-21
에이전트: lab-manager

## 실습 실행 요약

| 실습 이름 | 유형 | 상태 | 비고 |
|----------|------|------|------|
| 01-build-mcp-server | 코드 실습 | 통과 | `just setup && just test` 전체 통과. 4개 단계(i-do, we-do, you-do, solution) 모두 서버 로드 성공 |
| 02-cli-vs-mcp-comparison | README 중심 실습 | 통과 | 비교표, 시나리오 분석, 의사결정 기록서 템플릿 완비 |

## 가이드 보강 필요 항목

### Session 2: MCP 서버 구현 예시 부재
- **문제**: 가이드에서 "Python이나 TypeScript로 50줄이면 기본 서버를 만들 수 있다"고 언급하지만, 실제 코드 예시가 없다. 실습에서 `FastMCP`와 `@mcp.tool()` 데코레이터를 사용하는데, 가이드에서 이 패턴을 미리 소개하지 않는다.
- **제안**: Session 2의 "핵심 원리" 섹션에 간단한 MCP 서버 코드 스니펫(10줄 정도)을 추가하여, 실습 전에 코드 구조를 맛볼 수 있게 한다.

### Session 2: MCP 통신 방식 실습 연결
- **문제**: 가이드에서 "JSON-RPC 2.0 over stdio 또는 SSE" 통신 방식을 설명하지만, 실습에서는 stdio 방식만 다룬다. SSE 방식에 대한 실습 연결이 없다.
- **제안**: 가이드에 "이 수업에서는 stdio 방식을 실습하며, SSE(원격) 방식은 심화 과정에서 다룬다"는 스코프 안내를 추가한다.

### Session 3: 벤치마크 데이터 활용
- **문제**: research-brief.md에 CLI Token Efficiency Score 202 vs MCP 152 벤치마크 데이터가 있으나, 가이드 본문에는 반영되어 있지 않다. 실습(02-cli-vs-mcp-comparison)에서 이 수치를 사용하는데 가이드에서 먼저 소개해야 한다.
- **제안**: Session 3 비교표에 "토큰 효율성" 행을 추가하고, 벤치마크 수치와 출처를 명시한다.

### 전체: 실습 시간 배분
- **문제**: 가이드의 수업 일정표(1시간)에서 실습 시간이 명시되어 있지 않다. 강의 30% / 실습 70% 원칙을 적용하면 약 40분이 실습이어야 하나, 현재 일정표에서는 Session별 시간만 있고 실습 배분이 보이지 않는다.
- **제안**: 일정표에 각 Session의 강의/실습 비율을 표시하거나, 별도의 실습 타임라인을 추가한다. 현재 설계된 실습 시간: 01-build-mcp-server 약 40분 + 02-cli-vs-mcp-comparison 약 30분 = 총 70분. 1시간 수업에 맞추려면 실습을 선택적으로 운영하거나 수업 시간을 연장해야 한다.

## 추가 권장 사항

- 가이드에 MCP Inspector 설치 방법(`npx @modelcontextprotocol/inspector`)을 사전 준비 섹션에 추가하면 실습 진입이 원활해진다.
- Session 1의 Q&A에서 "Claude Code의 경우 사용자에게 명령어 실행 전 승인을 요청하는 방식"을 언급하는데, 이를 실습 01-build-mcp-server의 I DO 시연에서 직접 보여주면 강의-실습 연결이 강해진다.
- research-brief.md의 "95%의 MCP 서버가 쓰레기" 인사이트를 02-cli-vs-mcp-comparison 실습의 토론 소재로 활용할 수 있다.
