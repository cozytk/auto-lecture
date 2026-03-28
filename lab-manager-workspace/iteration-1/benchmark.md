# Lab Manager Skill Benchmark — Iteration 1

## Summary

| Metric | New Skill (v2) | Old Skill (v1) | Delta |
|--------|----------------|----------------|-------|
| **Pass Rate** | **100%** | 87.5% | **+12.5%p** |
| Avg Tokens | 78,535 | 68,766 | +14.2% |
| Avg Duration | 515s (8.6min) | 497s (8.3min) | +3.7% |

## Per-Eval Breakdown

### Eval 0: Basic Lab Creation
| Assertion | New | Old |
|-----------|-----|-----|
| ≥2 lab dirs | PASS | PASS |
| All READMEs exist | PASS | PASS |
| I DO/WE DO/YOU DO | PASS | PASS |
| Time estimates | PASS | PASS |
| feedback.md | PASS | PASS |
| Format mix (code+README) | PASS | PASS |
| solution/ exists | PASS | PASS |
| MCP technical accuracy | PASS | PASS |
| Research evidence | PASS | PASS |

**Score**: New 9/9, Old 9/9

### Eval 1: Constrained Format Selection
| Assertion | New | Old |
|-----------|-----|-----|
| MCP = code lab | PASS | PASS |
| Comparison = README lab | PASS | PASS |
| I DO/WE DO/YOU DO | PASS | PASS |
| i-do code executable | PASS | PASS |
| TODO markers | PASS | PASS |
| feedback.md | PASS | PASS |
| **Outline present** | **PASS** | **FAIL** |
| **Hints (details)** | **PASS** | **FAIL** |

**Score**: New 8/8, Old 6/8

## Analysis

### Where New Skill Wins
1. **아웃라인 단계 (a1-outline)**: 새 스킬만 Phase 2에서 실습 설계표를 출력. 시간 합산이 70%를 만족하는지 사전 검증. 구 스킬은 바로 제작에 들어가서 시간 초과 발생 (eval-1 old: 총 70분/60분 수업).
2. **힌트 일관성 (a1-hints)**: 새 스킬은 코드/README 실습 모두에 details 힌트를 포함. 구 스킬은 README 중심 실습에서 힌트를 누락.
3. **리서치 체계성**: 새 스킬은 Phase 1에서 Context7 + WebFetch를 체계적으로 사용. 구 스킬에서도 모델이 자발적으로 Context7를 사용했지만, 스킬이 지시하지 않아 일관성이 낮음.

### Where Old Skill Wins
1. **토큰 효율성**: 구 스킬이 평균 14.2% 적은 토큰 사용. 리서치/아웃라인 단계가 없어 오버헤드가 적음.
2. **Docker 테스트**: 구 스킬(eval-1)은 `uv` + `mcp[cli]` 설치까지 성공하여 실제 MCP SDK import 테스트를 통과. 새 스킬은 AST 구문 검사만 수행.

### Non-Discriminating Assertions
- 구조적 assertions (README 존재, 3단계, feedback.md 등)는 양쪽 모두 통과. 이는 양쪽 스킬 모두 기본 구조를 잘 정의하고 있음을 의미.

### Key Observation: Time Budget
- eval-1 old skill의 시간 합산이 70분으로 60분 수업을 초과. 이는 아웃라인 단계 없이 개별 실습을 만들 때 발생하는 전형적 문제.
- eval-1 new skill은 아웃라인 단계에서 45분/60분(75%)으로 사전 계획하여 현실적 시간 배분 달성.
