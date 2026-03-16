# 실습 피드백 (lab-manager → guide-writer)

**작성자**: lab-manager (worker-3)
**작성일**: 2026-03-08
**대상 가이드**: `lectures/ai-agent-dev/guide/`

---

## 실습 제작 완료 목록

| 실습 | 연관 세션 | 난이도 | 상태 |
|------|---------|--------|------|
| 01-prompt-strategy | Session 2 | 초중급 | 완료 |
| 02-structured-output | Session 2 | 중급 | 완료 |
| 03-function-calling | Session 4 | 중급 | 완료 |
| 04-rag-pipeline | Session 4 | 중급 | 완료 |
| day1/01-agent-opportunity-workshop | Session 1 | 기초~중급 | 완료 |
| day1/02-cost-latency-design-clinic | Session 2 | 중급 | 완료 |
| day1/03-agent-spec-studio | Session 3 | 중급 | 완료 |
| day1/04-architecture-decision-clinic | Session 4 | 중급 | 완료 |

---

## 가이드에 대한 피드백

### 전반적 평가

가이드 품질이 높습니다. 각 세션의 개념 설명 → 코드 예제 → Q&A 구조가 실습 설계에 바로 활용될 만큼 명확했습니다. 특히 코드 예제가 모두 OpenRouter API(`base_url="https://openrouter.ai/api/v1"`)를 사용하도록 통일되어 있어 실습 코드 작성이 수월했습니다.

---

### Session 1 (day1-session1.md)

**잘된 점**:
- Pain-Task-Skill-Tool 프레임워크가 학생이 실습에서 자신의 Agent를 설계할 때 명확한 기준을 제공합니다.

**피드백**:
- Session 1은 Agent 후보 도출 및 RAG vs Agent 구조 선택 분석 실습으로 설계하려 했으나, 내용이 분석/토론 중심이라 코드 실습으로 전환하기 어려웠습니다.
- **건의**: Session 1에 간단한 "Agent vs 단순 LLM 호출" 비교 코드 예제가 있으면 실습과 연결이 수월합니다. 예를 들어 `simple_llm_call()` vs `agent_with_tool()` 비교 코드 20줄 정도를 추가해주시면 세션 도입 실습으로 활용할 수 있습니다.

---

### Session 2 (day1-session2.md)

**잘된 점**:
- Zero-shot / Few-shot / CoT 비교 코드가 명확하여 I DO 시연 코드를 거의 그대로 활용했습니다.
- Pydantic `BaseModel` 기반 Structured Output 예제가 직관적입니다.

**피드백**:
- `AgentAction` 스키마에서 `confidence` 필드의 범위 검증(`ge=0.0, le=1.0`)이 가이드 코드에 누락되어 있습니다. 실습 solution에는 추가했으나 가이드 코드에도 반영해주시면 일관성이 유지됩니다.
- **건의**: WE DO 단계의 `validate_agent_action` 함수 과제에서 학생이 어떤 비즈니스 규칙을 구현해야 하는지 가이드에 한 줄 설명이 더 있으면 좋겠습니다.

---

### Session 3 (day1-session3.md)

**잘된 점**:
- Agent 기획서 템플릿이 구체적입니다. YOU DO 정답 예시(주간 보고서 자동화)가 Session 4 실습 03의 시나리오와 자연스럽게 연결됩니다.

**피드백**:
- Session 3은 문서 작성 실습이라 별도 코드 실습 디렉토리를 생성하지 않았습니다.
- **건의**: Session 3 기획서 산출물을 Session 4 실습 03(function-calling)의 YOU DO 입력으로 명시적으로 연결하는 문구가 가이드에 추가되면 흐름이 더 자연스럽습니다. 예: "이 기획서의 Sub-tasks 중 Tool로 구현할 항목을 실습 03 YOU DO에서 직접 구현합니다."

---

### Session 4 (day1-session4.md)

**잘된 점**:
- MCP/RAG/Hybrid 코드 예제 3개가 모두 실행 가능한 완성 코드입니다.
- 의사결정 트리가 `decide_architecture()` 함수로 코드화되어 있어 실습 아이디어로 바로 활용했습니다.

**피드백**:
- RAG 코드 예제에서 `doc_vecs = embed(documents)` 호출이 모듈 레벨에서 실행됩니다. 실습 파일에서 import 시 자동으로 API 호출이 발생하여 `test`/`lint` 단계에서 API 키 없이도 실행할 수 있도록 처리가 필요했습니다. 가이드 코드에 `if __name__ == "__main__":` 가드를 추가하거나, 임베딩을 lazy 초기화하는 패턴을 보여주시면 더 좋을 것 같습니다.
- **건의**: Hybrid 아키텍처(실습 없음) 관련하여 선택적 실습 05로 "RAG as Tool 패턴 구현"을 추가하면 심화 학습자용으로 좋겠습니다.

---

## 전체 건의사항

1. **실습 순서 명시**: 가이드 각 실습 섹션에 `labs/01-prompt-strategy` 등 정확한 디렉토리 경로를 명시하면 학생이 해당 폴더를 바로 찾을 수 있습니다.
2. **환경 변수 통일**: `OPENROUTER_API_KEY`와 `MODEL` 환경 변수가 모든 실습에서 동일하게 사용됩니다. 가이드 사전 준비 섹션에 한 번만 설정하면 모든 실습에서 동작한다는 것을 강조해주세요.
3. **Session 1·3 코드 실습 부재**: 코드 없는 분석/설계 실습이 두 세션에 걸쳐 있어 코드 실습과의 비율이 다소 불균형합니다. 향후 Session 1에 간단한 비교 코드 실습을 추가하는 것을 검토해주시면 좋겠습니다.

---

## Day 1 실습 팩 보강 내용

- Day 1 전체를 따라갈 수 있도록 `lectures/ai-agent-dev/labs/day1/README.md`를 추가했습니다.
- Session 1, Session 3, Session 2 실습 3, Session 4 실습 3은 **README 중심 실습**으로 외부화했습니다.
- 이 변경으로 Day 1은 기존 코드 실습 4개 + README 중심 실습 4개 조합으로 운영할 수 있어, 실습 총량을 크게 늘릴 수 있습니다.
- 특히 Session 1과 Session 3은 코드보다 **분석/설계 산출물의 품질**이 학습 효과를 좌우하므로, 억지 코드 실습 대신 워크숍형 README 실습으로 설계하는 편이 더 적합했습니다.
