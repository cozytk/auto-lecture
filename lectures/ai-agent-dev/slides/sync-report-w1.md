# Week 1 Slide Sync Report

검토 대상: [slides.md](/Users/taekkim/auto-lecture/lectures/ai-agent-dev/slides/slides.md)

범위
- `slides.md` 전체를 처음부터 끝까지 재검토했습니다.
- 최종 기준 파일 길이: `5196` lines

수정 요약
- Session 1의 `개념 1/2/3/4` 표기를 `1./2./3./4.`로 통일하고, 관련 스크립트 호칭도 `주제` 중심으로 맞췄습니다.
- Session 1 표지/정리 슬라이드의 오래된 연도성 멘트와 보이지 않는 근거성 문장을 줄여서 화면 내용과 발표 흐름을 맞췄습니다.
- Session 2 도입 스크립트의 `네 가지` 표현을 실제 agenda 기준 `여섯 가지`로 수정했습니다.
- Token/Context Window 예시를 최신 모델 기준으로 갱신했습니다.
  - `gpt-4` tokenizer 예시를 `o200k_base`로 교체
  - 모델 비교를 `GPT-5.2 / GPT-5.4 / Claude Opus 4.6` 기준으로 갱신
  - 출력 예시 수와 코드 모델 수를 일치시킴
- 비용 최적화 파트의 모델 라우팅, 프롬프트 캐싱 설명, 코드 예시를 최신 명칭과 현재 설명에 맞게 정리했습니다.
- Session 2 실습의 `AgentAction` 명칭을 실제 강의 본문과 같은 `AgentDecision`으로 통일했습니다.
- Session 3의 `2024년 Gartner`식 오래된 근거 문구를 일반화된 2026 문맥으로 바꿨습니다.
- Session 3의 기획서 예시/검증 슬라이드에서 보이는 코드와 스크립트가 어긋나던 부분을 맞췄습니다.
  - 대표 필드만 채운 예시라고 명시
  - 검증 코드를 `3개 대표 체크` 기준으로 정리
  - 점수 표기 `5/6` → `3/3`
  - `Golden Test Set 50건`으로 화면/스크립트 일치
  - Out of Scope 예시와 fallback 코드의 범위를 `환불 처리`로 일치
- Session 3의 `다음 Session 4` 예고를 실제 다음 세션 내용인 구조 판단 세션에 맞게 전면 수정했습니다.
- Session 4는 `Tool Use · RAG · Hybrid`를 중심 용어로 잡고, `Function Calling`과 `MCP`를 그 하위 설명으로 정리했습니다.
  - 세션 제목, 요약, 실습명, 의사결정 딕셔너리 값, 단독 아키텍처 표기까지 일관화
  - `MCP 단독` → `Tool Use 단독`
- Session 4의 RAG 코드 예시는 화면과 스크립트 불일치를 함께 수정했습니다.
  - `OpenRouter` 언급 제거
  - `OpenAI(api_key="...")`로 단순화
  - 프롬프트에 `문서에 없는 내용은 '확인 불가'` 지시 추가
  - 실행 결과 `14일` → 문서와 맞는 `7일`
- Day 1 종합 정리 슬라이드와 발표 스크립트를 실제 Day 1 세션 내용에 맞게 다시 썼습니다.
  - 기존의 `OpenRouter`, `Multi-agent`, `Human-in-the-loop`, `Perception → Reasoning → Action` 등 본문과 안 맞는 요약 제거

검증 메모
- 패턴 검색으로 아래 잔존 여부를 다시 확인했습니다.
  - `GPT-4`, `GPT-4o`, `Claude 3.7`, `OpenRouter`, `AgentAction`
  - `개념 1/2/3/4`
  - `2025년 1분기`, `2024년 이후 정보`, `14일 이내`, `MCP 단독`
- 위 항목들은 본문 기준 제거 또는 최신/일관 표현으로 정리되었습니다.
- `2024년`은 Function Calling 역사 슬라이드의 연표 설명에만 남겼습니다. 이 부분은 과거 사건 설명이라 유지했습니다.

비고
- 최신 모델/캐싱 관련 표현은 2026 기준 공식 문서 흐름에 맞춰 갱신했습니다.
