# Session 3: Agent 기획서 구조화 (2h)

## 학습 목표

1. 비즈니스 문제를 체계적인 Agent 기획서로 변환할 수 있다
2. 기획서의 핵심 구성요소(목적, 입출력, 제약조건, 성공 기준)를 정의하고 작성할 수 있다
3. 기획서를 기반으로 기술 설계 문서로 전환하는 프로세스를 수행할 수 있다

---

## 개념 1: 비즈니스 문제에서 Agent 기획서로의 변환

### 왜 이것이 중요한가

Session 1에서 Pain-Task-Skill-Tool로 Agent 후보를 도출했다.
이제 그 후보를 **실제 구현 가능한 기획서**로 변환해야 한다.

기획서 없이 코딩에 들어가면 "무엇을 만들어야 하는지"가 불명확해진다.
2024년 Gartner 보고서: AI 프로젝트 실패 원인 1위 → **불명확한 요구사항**

> 기획서 없이 시작하면 4가지 문제가 반드시 발생한다.

**기획서 부재 시 발생하는 문제:**

| 문제 | 증상 |
|------|------|
| 범위 무한 확장 | FAQ 봇이 어느새 주문 관리까지 담당 |
| 성공 기준 부재 | "잘 되는 건지" 아무도 판단 불가 |
| 입출력 불일치 | 개발자는 JSON, 기획자는 자연어 기대 |
| 제약조건 누락 | Agent가 고객 개인정보를 외부 API로 전송 |

---

### 핵심 원리

> 기획서 = 비즈니스 문제와 기술 구현 사이의 **번역 문서**

**비즈니스팀**: "고객 문의 응답 시간을 줄이고 싶다"
**개발팀**: "LLM API를 호출하여 JSON을 반환하는 시스템"
→ 기획서가 이 두 세계를 연결한다

**변환 3단계:**

① **비즈니스 문제 정의** → 고통점과 현재 프로세스를 수치로 파악
② **Agent 기회 식별** → 자동화 대상 vs 사람 개입 필요 구분
③ **Agent 기획서 생성** → 6가지 구성요소로 명세화

---

### 실무에서의 의미

기획서 없이 만든 Agent의 결말은 항상 같다.
→ 완성 후 "이건 우리가 원한 게 아닙니다" 피드백

**변환 핵심 원칙:**

| 원칙 | 위반 시 문제 |
|------|------------|
| Pain-first | 기술 중심 사고로 불필요한 Agent 구현 |
| 이해관계자 합의 | 구현 후 "이건 우리가 원한 게 아니다" |
| MVP 범위 | 범위 무한 확장으로 프로젝트 지연 |
| 정량적 목표 | "잘 되는 건지 모른다" 상태 지속 |

---

### 다른 접근법과의 비교

| 구분 | 전통 PRD | Agent 기획서 |
|------|---------|------------|
| 동작 명세 | 결정론적 (버튼 클릭 → 주문 생성) | 확률적 동작 포함 |
| Fallback | 불필요 | 필수 (confidence 0.7 미만 → 에스컬레이션) |
| LLM 비용 | 고려 없음 | 비용 제약 명시 |

---

### 주의사항

> **완벽한 기획서를 쓰려고 시간을 낭비하지 말 것.**
> 처음부터 모든 시나리오 예측은 불가능하다.
> **MVP 범위 → 운영 데이터 수집 → 기획서 업데이트** 사이클로 접근한다.
> 기획서는 한 번 쓰고 끝나는 문서가 아닌 **살아있는 문서(Living Document)**다.

---

### 코드 예제

이를 코드로 표현하면:

```python
from dataclasses import dataclass, field

@dataclass
class BusinessProblem:
    """Step 1: 비즈니스 문제 정의"""
    pain: str                      # 현재 고통점
    stakeholders: list[str]        # 이해관계자
    current_process: list[str]     # 현재 수동 프로세스
    cost_of_status_quo: dict       # 현 상태 유지 비용

@dataclass
class AgentSpec:
    """Step 3: Agent 기획서"""
    purpose: str                   # 목적 (한 문장)
    inputs: list[dict]             # 입력 정의
    outputs: list[dict]            # 출력 정의
    constraints: list[str]         # 제약조건
    success_criteria: list[dict]   # 성공 기준 (정량)
    scope_boundary: dict           # 범위 경계 (하는 것 / 안 하는 것)

# 실제 시나리오: 고객 문의 자동 응답 Agent
problem = BusinessProblem(
    pain="CS팀 5명이 하루 200건 문의를 처리. 70%가 반복 질문. 평균 응답 2시간.",
    stakeholders=["CS팀장", "고객", "CTO", "개인정보보호 담당자"],
    current_process=[
        "1. 고객 채팅/이메일로 문의 (수동 접수)",
        "2. CS 담당자가 카테고리 분류 (수동 판단)",
        "3. FAQ DB에서 답변 검색 (수동 반복)",
        "4. 답변 초안 작성 후 전송 (수동 반복)",
        "5. 복잡한 문의는 에스컬레이션 (수동 판단)",
        "6. 처리 결과를 CRM에 기록 (수동 반복)",
    ],
    cost_of_status_quo={
        "인건비": "CS 담당자 5명 x 월 400만원 = 월 2000만원",
        "기회비용": "야간/주말 미응답으로 인한 고객 이탈",
    },
)

for step in problem.current_process:
    tag = "자동화 대상" if "수동 반복" in step else "사람 개입"
    print(f"  {step}  --> [{tag}]")
```

실행 결과:

```
1. 고객 채팅/이메일로 문의 (수동 접수)  --> [사람 개입]
2. CS 담당자가 카테고리 분류 (수동 판단)  --> [사람 개입]
3. FAQ DB에서 답변 검색 (수동 반복)  --> [자동화 대상]
4. 답변 초안 작성 후 전송 (수동 반복)  --> [자동화 대상]
5. 복잡한 문의는 에스컬레이션 (수동 판단)  --> [사람 개입]
6. 처리 결과를 CRM에 기록 (수동 반복)  --> [자동화 대상]
```

---

### Q&A

**Q: 기획서를 누가 작성해야 하나요?**
A: 기획자(또는 PM)가 주도하고, 개발자가 검토하는 구조가 이상적이다.
AI Agent 기획은 LLM의 한계를 이해해야 한다.
→ 개발자가 기획 단계부터 반드시 참여해야 한다.

**Q: 기획서의 적정 분량은?**
A: MVP 기준으로 **A4 2-5장**이면 충분하다.
핵심은 분량이 아닌 **구성요소의 완전성**이다.
목적이 명확하고, 입출력이 예시와 함께 정의되고, 성공 기준이 수치화되면 2장도 충분하다.

<details>
<summary>퀴즈: Agent 기획서 작성 전에 반드시 확인해야 하는 것은?</summary>

**보기:**
1. 사용할 LLM 모델의 벤치마크 점수
2. 현재 수동 프로세스의 구체적 단계와 비용
3. 경쟁사의 AI Agent 도입 현황
4. 최신 프롬프트 엔지니어링 논문

**힌트**: 기획서의 목적은 "비즈니스 문제를 해결하는 Agent의 명세"를 정의하는 것이다.

**정답**: 2번. 현재 수동 프로세스를 파악해야 (1) 어디를 자동화할지 식별하고, (2) Agent 도입 후 비용 절감을 정량화할 수 있다.
1번, 3번, 4번은 기술 설계 단계에서 고려할 사항이다.
</details>

---

## 개념 2: Agent 기획서의 핵심 구성요소

### 왜 이것이 중요한가

Agent 기획서는 **6가지 핵심 구성요소**로 이루어진다.
각 구성요소는 기획자, 개발자, 이해관계자 간의 **계약(Contract)** 역할을 한다.

> 어느 한 구성요소라도 누락되면 계약이 불완전해진다.
> 불완전한 계약은 프로젝트 실패로 이어진다.

---

### 핵심 원리

6가지 구성요소는 **연쇄적으로 연결**되어 있다.

**목적** → 범위를 결정
→ **범위** → 입출력을 결정
→ **입출력** → 제약조건을 도출
→ **제약조건** → 성공 기준의 측정 방식을 결정

**각 구성요소 정의:**

| 구성요소 | 역할 | 좋은 예 | 나쁜 예 |
|---------|------|--------|--------|
| 목적 | Agent의 존재 이유 한 문장 | "응답 시간 2시간→30초 단축" | "고객 서비스 개선" |
| 입력 | 받는 데이터와 트리거 | "텍스트, 최대 2000자, 한국어/영어" | "고객 데이터" |
| 출력 | 생성하는 결과 | "JSON 형식 분류 결과 + confidence" | "적절한 답변" |
| 제약조건 | 해서는 안 될 것 | "고객 PII를 LLM 프롬프트에 포함 금지" | "보안을 지킨다" |
| 성공 기준 | 측정 가능한 목표 | "정확도 90% 이상, 주간 50건 샘플링" | "잘 동작한다" |
| 범위 경계 | In/Out of Scope | "환불 처리: Out of Scope" | (미정의) |

---

### 실무에서의 의미

실제 프로젝트에서 가장 많은 논쟁이 벌어지는 것: **범위 경계(Scope Boundary)**

"이 기능도 넣으면 좋지 않아요?"라는 요청이 끊임없이 들어온다.
→ 범위 경계를 명시적으로 문서화하면 "기획서에 Out of Scope"라고 객관적으로 대응 가능하다.

> 범위 경계 없이 시작한 프로젝트는 100% 범위 팽창(Scope Creep)을 경험한다.

---

### 다른 접근법과의 비교

| 구분 | User Story | Agent 기획서 |
|------|-----------|------------|
| 사용자 관점 | ✅ 잘 포착 | ✅ 포함 |
| LLM 비용 제약 | ❌ 담기 어려움 | ✅ 포함 |
| Hallucination 대응 | ❌ 없음 | ✅ Fallback 전략 |
| 권장 사용 방식 | 단독 | User Story를 보완하여 함께 사용 |

---

### 주의사항

> **구체성이 핵심이다.**
> "적절한 답변" → "JSON 형식의 분류 결과 (category, confidence, suggested_reply)"
> "보안을 지킨다" → "고객 PII(이름, 전화번호, 주소)를 LLM 프롬프트에 포함하지 않는다"
> 모호한 기획서는 없는 것보다 위험하다. 각자 다르게 해석하여 논쟁만 추가된다.

---

### 코드 예제

이를 코드로 표현하면:

```python
from dataclasses import dataclass, field
from enum import Enum

class Priority(str, Enum):
    MUST = "MUST"     # 필수: 없으면 Agent 가치 없음
    SHOULD = "SHOULD" # 권장: 있으면 가치 향상
    COULD = "COULD"   # 선택: 여유 있으면 추가

@dataclass
class AgentSpecTemplate:
    """Agent 기획서 표준 템플릿"""
    purpose: str                                          # 1. 목적
    inputs: list[dict] = field(default_factory=list)      # 2. 입력
    outputs: list[dict] = field(default_factory=list)     # 3. 출력
    constraints: list[dict] = field(default_factory=list) # 4. 제약조건
    success_criteria: list[dict] = field(default_factory=list) # 5. 성공 기준
    in_scope: list[str] = field(default_factory=list)     # 6. 범위 - In
    out_of_scope: list[str] = field(default_factory=list) # 6. 범위 - Out

# 완성된 기획서 예시: 고객 문의 자동 응답 Agent
cs_agent_spec = AgentSpecTemplate(
    purpose="CS팀의 반복 문의(FAQ 답변, 주문 상태 조회)를 자동 처리하여 "
            "평균 응답 시간을 2시간에서 30초 이내로 단축한다.",
    inputs=[
        {"name": "customer_message", "type": "string", "required": True,
         "max_length": 2000, "language": ["ko", "en"],
         "example": "주문번호 12345 배송이 언제 되나요?"},
        {"name": "customer_id", "type": "string", "required": True,
         "format": "UUID", "example": "cust-a1b2c3d4"},
    ],
    outputs=[
        {"name": "classification",
         "fields": {"category": "FAQ|주문조회|환불|기술지원|기타",
                    "confidence": "float (0.0~1.0)"}},
        {"name": "response",
         "fields": {"message": "답변 텍스트", "sources": "근거 문서 목록"}},
    ],
    constraints=[
        {"type": "보안", "rule": "고객 PII를 LLM 프롬프트에 포함하지 않는다",
         "violation_impact": "개인정보보호법 위반"},
        {"type": "비즈니스", "rule": "환불/결제 관련은 반드시 사람에게 에스컬레이션",
         "violation_impact": "잘못된 환불 처리 시 재무 손실"},
        {"type": "기술", "rule": "LLM 응답 10초 초과 시 타임아웃 처리",
         "violation_impact": "고객 대기 시간 증가"},
    ],
    success_criteria=[
        {"metric": "자동 응답률", "target": "60% 이상", "measurement": "일간"},
        {"metric": "응답 정확도", "target": "90% 이상", "measurement": "주간 50건 샘플링"},
        {"metric": "평균 응답 시간", "target": "30초 이내", "measurement": "중앙값"},
    ],
    in_scope=["FAQ 자동 답변", "주문 상태 조회", "문의 카테고리 분류",
              "처리 불가 문의 에스컬레이션"],
    out_of_scope=["환불/결제 처리", "고객 감정 케어", "실시간 음성 통화"],
)

print(f"[목적] {cs_agent_spec.purpose}")
print(f"[제약] {len(cs_agent_spec.constraints)}개, [성공기준] {len(cs_agent_spec.success_criteria)}개")
```

실행 결과:

```
[목적] CS팀의 반복 문의(FAQ 답변, 주문 상태 조회)를 자동 처리하여 평균 응답 시간을 2시간에서 30초 이내로 단축한다.
[제약] 3개, [성공기준] 3개
```

---

### Q&A

**Q: 성공 기준의 목표 수치를 어떻게 정해야 하나요?**
A: 3단계 접근법을 사용한다.
① 현재 수준 측정: 수동 프로세스의 현재 성능을 먼저 측정한다.
② 업계 벤치마크 참고: 유사 서비스의 공개 지표를 참고한다.
③ MVP 목표 분리: MVP에서는 "현재 수준과 동등 이상"을 목표로 설정한다.
처음부터 99%를 목표로 잡으면 프로젝트가 영원히 완료되지 않는다.

**Q: 범위 경계의 "회색 지대"는 어떻게 처리하나요?**
A: 명확하지 않은 영역은 **기본적으로 Out of Scope에 넣는다.**
회색 지대가 발견되면 이해관계자 회의를 소집하여 명시적으로 결정한다.
결정 근거를 기획서에 기록하지 않으면 "왜 이걸 안 해요?"라는 질문이 반복된다.

<details>
<summary>퀴즈: 다음 기획서의 성공 기준 중 문제가 있는 것은?</summary>

**보기:**
1. "자동 응답률 60% 이상 (일간 전체 문의 대비 자동 처리 비율)"
2. "고객이 만족할 만한 수준의 답변 품질"
3. "평균 응답 시간 30초 이내 (문의 접수 ~ 답변 전송, 중앙값)"
4. "에스컬레이션 비율 40% 이하"

**힌트**: 성공 기준은 "측정 가능"해야 한다. 누가 측정하더라도 같은 결과가 나와야 한다.

**정답**: 2번이 문제다.
"고객이 만족할 만한 수준"은 주관적이어서 측정할 수 없다.
개선: "자동 응답 후 CSAT 설문 4.0/5.0 이상 (월간, 응답 고객 기준)"
1번, 3번, 4번은 모두 수치 + 측정 방법이 포함되어 있다.
</details>

---

## 개념 3: 좋은 기획서 vs 나쁜 기획서 비교

### 왜 이것이 중요한가

기획서의 품질은 프로젝트 성패를 좌우한다.
같은 비즈니스 문제라도 기획서의 구체성에 따라 구현 결과가 완전히 달라진다.

**좋은 기획서**: "무엇을 만들어야 하는지"를 명확히 전달한다.
**나쁜 기획서**: "알아서 잘 만들어 주세요" 메시지를 전달한다.

---

### 핵심 원리

> 좋은 기획서와 나쁜 기획서의 차이: **단 하나, 구체성**

**구체성 판단 기준:**
"이 문장을 읽는 사람이 다르게 해석할 여지가 없는가?"

**나쁜 예**: "고객 서비스를 개선한다"
→ 10명이 읽으면 10가지 다른 해석이 가능

**좋은 예**: "CS팀의 FAQ 자동 답변으로 평균 응답 시간을 2시간에서 30초로 단축한다"
→ 모두가 동일하게 이해

---

### 실무에서의 의미

기획서 품질을 검증하는 가장 효과적인 방법: **"3인 해석 테스트"**

① 기획서를 3명에게 독립적으로 읽게 한다.
② 각자 이해한 내용을 설명하게 한다.
③ 3명의 설명이 일치하면 → 좋은 기획서.
④ 불일치하면 → 모호한 부분이 있다는 신호.

5분이면 가능하지만, 수주 간의 개발 낭비를 예방할 수 있다.

---

### 다른 접근법과의 비교

일부 애자일 팀: "문서보다 작동하는 소프트웨어"를 강조하며 기획서를 생략한다.

| 구분 | 일반 소프트웨어 | Agent 프로젝트 |
|------|--------------|--------------|
| 코드 수정 비용 | 낮음 | 중간 |
| 잘못된 행동(이메일 발송, DB 삭제) | 쉽게 롤백 | 비가역적 |
| LLM 호출 비용 | 해당 없음 | 매번 발생 |
| 권장 방식 | "일단 만들고 고치자" 가능 | 기획서 필수 |

---

### 주의사항

> **좋은 기획서 ≠ 완벽한 기획서**
> "6가지 구성요소가 각각 최소 1개의 구체적 예시를 포함하고, 성공 기준이 모두 수치화되어 있으면" 시작하기에 충분하다.
> 나머지는 운영하면서 보완한다.

---

### 코드 예제

이를 코드로 표현하면:

```python
def validate_spec_quality(spec: dict) -> dict:
    """Agent 기획서 품질 검증"""
    issues = []
    score = 0
    max_score = 6

    # 1. 목적: 구체적 행동 + 정량적 목표 포함 여부
    purpose = spec.get("purpose", "")
    has_action = any(w in purpose for w in ["하여", "위해", "단축", "향상", "자동"])
    if len(purpose) > 20 and has_action:
        score += 1
    else:
        issues.append("목적이 모호하거나 정량적 목표가 없습니다")

    # 2. 입력: 타입 + 예시 포함 여부
    inputs = spec.get("inputs", [])
    if inputs and all("type" in i and "example" in i for i in inputs):
        score += 1
    else:
        issues.append("입력에 타입 또는 예시가 없습니다")

    # 3. 출력: 타입 + 필드 정의 포함 여부
    outputs = spec.get("outputs", [])
    if outputs and all("fields" in o or "type" in o for o in outputs):
        score += 1
    else:
        issues.append("출력 형식이 정의되지 않았습니다")

    # 4. 제약조건: 보안 + 비즈니스 + 기술 3종 포함
    constraints = spec.get("constraints", [])
    types = {c.get("type") for c in constraints}
    if {"보안", "비즈니스", "기술"}.issubset(types):
        score += 1
    else:
        issues.append("제약조건에 보안/비즈니스/기술 유형이 필요합니다")

    # 5. 성공 기준: 수치 + 측정 방법 포함
    criteria = spec.get("success_criteria", [])
    if criteria and all("target" in c and "measurement" in c for c in criteria):
        score += 1
    else:
        issues.append("성공 기준에 수치 또는 측정 방법이 없습니다")

    # 6. 범위: In/Out 모두 정의
    if spec.get("in_scope") and spec.get("out_of_scope"):
        score += 1
    else:
        issues.append("In Scope 또는 Out of Scope가 정의되지 않았습니다")

    grade = "A" if score >= 5 else "B" if score >= 3 else "C"
    return {"score": f"{score}/{max_score}", "grade": grade, "issues": issues}

# 비교 검증
good_result = validate_spec_quality({
    "purpose": "CS팀의 반복 문의를 자동 처리하여 응답 시간을 단축한다",
    "inputs": [{"type": "string", "example": "배송 문의"}],
    "outputs": [{"fields": {"category": "string"}}],
    "constraints": [
        {"type": "보안", "rule": "PII 금지"},
        {"type": "비즈니스", "rule": "환불은 에스컬레이션"},
        {"type": "기술", "rule": "10초 타임아웃"},
    ],
    "success_criteria": [{"target": "60%", "measurement": "일간"}],
    "in_scope": ["FAQ 답변"],
    "out_of_scope": ["환불 처리"],
})
bad_result = validate_spec_quality({"purpose": "고객 서비스 개선"})
print(f"좋은 기획서: {good_result['grade']} ({good_result['score']})")
print(f"나쁜 기획서: {bad_result['grade']} ({bad_result['score']})")
```

실행 결과:

```
좋은 기획서: A (5/6)
나쁜 기획서: C (0/6)
```

---

### Q&A

**Q: 기획서를 LLM으로 자동 생성하면 품질이 괜찮은가요?**
A: LLM이 생성한 초안은 **출발점**으로만 사용해야 한다.
LLM은 일반적인 구조와 항목을 잘 잡아주지만, 도메인 특화 제약조건을 빠뜨린다.
LLM 초안 생성 → 도메인 전문가 검토 → 이해관계자 합의의 3단계를 거쳐야 한다.

**Q: 나쁜 기획서를 받았을 때 개발자는 어떻게 대응해야 하나요?**
A: 기획서 품질 검증 체크리스트를 만들어 **기획 리뷰 회의**에서 사용한다.
"목적에 정량적 목표가 없습니다" 같은 구체적 피드백을 주고, 기준을 통과해야 개발을 시작하는 게이트(Gate)를 설정한다.
이는 기획자 비판이 아닌 **프로젝트 실패를 예방하는 프로세스**다.

<details>
<summary>퀴즈: 다음 기획서 목적 문장의 문제점을 3가지 이상 지적하시오</summary>

**기획서 목적**: "AI를 활용하여 업무를 자동화하고 효율성을 높인다"

**힌트**: 좋은 목적 문장의 3가지 요소: "대상(누구를)", "행동(무엇을)", "목표(어느 수준까지)"

**정답**:
1. **대상 불명확**: "업무"가 어떤 업무인지 특정되지 않음
2. **행동 불명확**: "자동화"의 범위가 정의되지 않음
3. **정량적 목표 부재**: "효율성을 높인다"는 측정 불가
4. **수혜자 불명확**: 누가 혜택을 받는지 언급 없음
5. **기술 특정**: "AI를 활용하여"는 수단을 목적에 포함한 것

개선 예시: "CS팀의 반복 문의(FAQ, 주문 조회)를 자동 응답하여 평균 처리 시간을 2시간에서 30초로 단축하고, 24시간 고객 응대를 가능하게 한다"
</details>

---

## 개념 4: 기획서에서 기술 설계로의 전환

### 왜 이것이 중요한가

기획서: "무엇(What)을 만들 것인가"
기술 설계: "어떻게(How) 만들 것인가"

기획서의 각 구성요소가 기술 설계의 어떤 항목으로 매핑되는지 이해해야 한다.

> 기획서에 "보안을 지킨다"고 써 있는데 기술 설계에 보안 컴포넌트가 없는 상황이 발생해서는 안 된다.

---

### 핵심 원리

기획서 → 기술 설계는 **1:1 매핑**이 가능하다.

| 기획서 항목 | 기술 설계 항목 | 매핑 예시 |
|------------|--------------|----------|
| 목적 | 아키텍처 선택 | 멀티스텝 자동화 → Agent |
| 입력 | API 인터페이스 + 전처리 | 텍스트 2000자 → 토큰 제한 처리 |
| 출력 | 응답 스키마 (Pydantic) | JSON 출력 → BaseModel |
| 제약조건 | Guardrail + Validation | PII 제약 → 마스킹 레이어 |
| 성공 기준 | 테스트 + 모니터링 | 정확도 90% → Golden Test Set |
| 범위 경계 | 라우터 + Fallback | 환불 Out → 사람에게 라우팅 |

---

### 실무에서의 의미

가장 자주 발생하는 문제: **"기획서에 없는 결정을 개발자가 임의로 내리는 것"**

기획서에 "에러 시 적절히 처리한다"라고만 써 있으면:
- 개발자 A → 재시도 구현
- 개발자 B → 기본값 반환 구현
- 개발자 C → 에러 전파 구현

→ 기획서 단계에서 에러 시나리오와 Fallback 동작을 반드시 명시해야 한다.

---

### 다른 접근법과의 비교

| 구분 | 폭포수(Waterfall) | Agent 권장 방식 |
|------|-----------------|----------------|
| 흐름 | 기획 → 설계 → 구현 | 기획 → 설계 초안 → 프로토타입 → 검증 → 반복 |
| LLM 예측 가능성 | 결정론적 → 완전 예측 가능 | 비결정적 → 사전 예측 어려움 |
| 피드백 루프 | 느림 | 빠름 (권장) |

---

### 주의사항

> **기획서와 기술 설계는 양방향 추적(Traceability)이 되어야 한다.**
> 기획서의 각 항목에 ID를 부여한다 (예: SPEC-001).
> 기술 설계의 각 컴포넌트가 어떤 SPEC 항목에 대응하는지 매핑한다.
> Git을 활용하여 기획서도 버전 관리하는 것을 권장한다.

---

### 코드 예제

이를 코드로 표현하면:

```python
import re
from pydantic import BaseModel, Field
from dataclasses import dataclass, field

@dataclass
class TechnicalDesign:
    """기술 설계 문서"""
    architecture: str
    llm_config: dict = field(default_factory=dict)
    guardrails: list[dict] = field(default_factory=list)
    test_plan: list[dict] = field(default_factory=list)

def spec_to_technical_design(spec) -> TechnicalDesign:
    """기획서 → 기술 설계 자동 변환"""
    # 1. 아키텍처 결정 (목적/범위에서)
    has_knowledge = any("FAQ" in s or "검색" in s for s in spec.in_scope)
    has_actions = any("처리" in s or "분류" in s for s in spec.in_scope)
    architecture = "Hybrid (Agent+RAG)" if has_knowledge and has_actions else "Agent"

    # 2. Guardrail 도출 (제약조건에서)
    guardrails = [
        {"type": c["type"],
         "impl": "PII 마스킹" if c["type"] == "보안" else "금지 행동 분류기"}
        for c in spec.constraints
    ]

    # 3. 테스트 계획 도출 (성공 기준에서)
    test_plan = [
        {"metric": c["metric"], "target": c["target"],
         "test_type": "Golden Test" if "정확도" in c["metric"] else "부하 테스트"}
        for c in spec.success_criteria
    ]

    return TechnicalDesign(
        architecture=architecture, guardrails=guardrails, test_plan=test_plan,
        llm_config={"model": "moonshotai/kimi-k2", "temperature": 0.1},
    )

# 기획서 제약: "고객 PII를 LLM에 전송하지 않는다"
# → 기술 설계: PII 마스킹 전처리 레이어
class PIIMasker:
    PII_PATTERNS = {
        "phone": re.compile(r"01[016789]-?\d{3,4}-?\d{4}"),
        "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    }

    def mask(self, text: str) -> tuple[str, list[str]]:
        detected = []
        for pii_type, pattern in self.PII_PATTERNS.items():
            if pattern.search(text):
                detected.append(pii_type)
                text = pattern.sub(f"[{pii_type.upper()}_MASKED]", text)
        return text, detected

# 기획서 제약: "confidence 0.7 미만이면 에스컬레이션"
# → 기술 설계: 출력 검증 레이어
class AgentOutput(BaseModel):
    category: str = Field(description="문의 카테고리")
    confidence: float = Field(ge=0.0, le=1.0)
    response_message: str = Field(description="고객 답변")

    def should_escalate(self) -> bool:
        return self.confidence < 0.7 or self.category == "환불"

masker = PIIMasker()
masked, detected = masker.mask("전화번호는 010-1234-5678입니다")
print(f"마스킹: {masked}, 감지: {detected}")

output = AgentOutput(category="환불", confidence=0.99, response_message="답변")
print(f"에스컬레이션: {output.should_escalate()}")
```

실행 결과:

```
마스킹: 전화번호는 [PHONE_MASKED]입니다, 감지: ['phone']
에스컬레이션: True
```

---

### Q&A

**Q: 기획서에서 기술 설계로 변환할 때 가장 자주 발생하는 문제는?**
A: **기획서에 없는 결정을 개발자가 임의로 내리는 것**이다.
"에러 시 적절히 처리한다"는 3가지 서로 다른 구현으로 이어진다.
해결: "LLM 응답 실패 시 3회 재시도 후 실패하면 기본 안내 메시지를 반환한다"처럼 구체적으로 정의한다.

**Q: 기획서와 기술 설계의 변경 관리는 어떻게 하나요?**
A: 기획서 항목에 ID를 부여한다 (예: SPEC-001).
기술 설계의 각 컴포넌트가 어떤 SPEC 항목에 대응하는지 매핑한다.
기획서가 변경되면 영향받는 기술 설계 항목을 즉시 식별할 수 있다.

<details>
<summary>퀴즈: 다음 제약조건을 기술 설계로 변환하시오</summary>

**제약조건**: "Agent의 LLM 응답 시간이 10초를 초과하면 타임아웃 처리하고, 고객에게 '잠시 후 다시 시도해주세요' 메시지를 반환한다. 타임아웃 발생 횟수를 모니터링하여 일 50건 이상이면 알림을 발송한다."

**힌트**: 이 제약조건에는 3가지 기술 요소가 포함되어 있다.
(1) 타임아웃 처리, (2) Fallback 응답, (3) 모니터링 + 알림

**정답**:
1. **타임아웃 처리**: `asyncio.wait_for(llm_call(), timeout=10.0)`
2. **Fallback 응답**: `try-except TimeoutError` → 고정 메시지 반환
3. **모니터링**: 타임아웃 카운터 증가 (Prometheus/CloudWatch), 일 50건 임계값 알림

```python
import asyncio

async def agent_with_timeout(message: str) -> dict:
    try:
        result = await asyncio.wait_for(llm_call(message), timeout=10.0)
        return result
    except asyncio.TimeoutError:
        metrics.timeout_counter.inc()  # 모니터링
        return {"message": "잠시 후 다시 시도해주세요", "fallback": True}
```
</details>

---

## 실습

### 실습 1: Agent 기획서 작성

- **연관 학습 목표**: 학습 목표 1, 2
- **실습 목적**: 비즈니스 문제를 분석하여 6가지 구성요소를 갖춘 Agent 기획서를 직접 작성한다
- **실습 유형**: 분석 + 문서 작성
- **난이도**: 기초
- **예상 소요 시간**: 30분 (I DO 5분 / WE DO 10분 / YOU DO 15분)
- **선행 조건**: Session 1 실습 1 완료 (Pain-Task-Skill-Tool 분석)
- **실행 환경**: 로컬 (문서 작성)

**I DO**: 강사가 "주간 보고서 자동화" Pain을 6가지 구성요소로 변환하는 과정을 시연한다.
각 항목을 채우면서 "왜 이 구성요소가 필요한지"를 설명한다.

**WE DO**: "코드 리뷰 자동화 Agent" 시나리오를 함께 분석한다.
목적 문장 작성 → 입력 정의 → 제약조건 도출 순서로 단계마다 멈추고 질문을 받는다.

**YOU DO**: Session 1에서 도출한 Agent 후보 1개를 선택하여 아래 템플릿의 모든 항목을 채워 기획서를 완성한다.

```python
my_agent_spec = {
    "purpose": "",
    # → "누구를 위해 + 무엇을 + 정량적 목표" 형식으로 작성

    "inputs": [
        # 최소 2개: name, type, required, max_length(해당 시), example
    ],

    "outputs": [
        # 최소 2개: name, type, fields(JSON인 경우), example
    ],

    "constraints": [
        # 최소 3개 (보안 1개 + 비즈니스 1개 + 기술 1개)
        # 각 제약: type, rule, violation_impact
    ],

    "success_criteria": [
        # 최소 2개: metric, target(수치), measurement(측정 방법)
    ],

    "in_scope": [
        # 최소 3개: Agent가 하는 것
    ],
    "out_of_scope": [
        # 최소 2개: Agent가 하지 않는 것
    ],
}
```

작성 후 `validate_spec_quality()` 함수로 검증하여 등급 B 이상을 목표로 한다.

**정답 예시** (주간 보고서 자동화):

```python
my_agent_spec = {
    "purpose": "개발팀의 주간 보고서 작성에 소요되는 3시간을 자동화하여 10분 이내로 단축한다",
    "inputs": [
        {"name": "week_start", "type": "date", "required": True, "example": "2025-03-03"},
        {"name": "team_id", "type": "string", "required": True, "example": "team-backend"},
    ],
    "outputs": [
        {"name": "report", "fields": {"summary": "string", "jira_tickets": "list", "git_commits": "list"}},
        {"name": "confluence_url", "type": "string", "example": "https://confluence.../weekly-report"},
    ],
    "constraints": [
        {"type": "보안", "rule": "개인별 커밋 내역을 외부 서비스에 전송하지 않는다", "violation_impact": "개인정보 유출"},
        {"type": "비즈니스", "rule": "미완료 티켓은 '진행중'으로 표시하고 마감일 초과 시 강조", "violation_impact": "보고서 정확성 저하"},
        {"type": "기술", "rule": "모든 API 호출 30초 타임아웃", "violation_impact": "보고서 생성 지연"},
    ],
    "success_criteria": [
        {"metric": "보고서 생성 시간", "target": "10분 이내", "measurement": "금요일 오전 평균"},
        {"metric": "데이터 정확도", "target": "95% 이상", "measurement": "주간 수동 검토"},
    ],
    "in_scope": ["Jira 티켓 수집", "Git 커밋 요약", "Confluence 저장", "Slack 알림"],
    "out_of_scope": ["팀원 개별 성과 평가", "타팀 보고서 생성"],
}
```

---

### 실습 2: 좋은 기획서 vs 나쁜 기획서 개선

- **연관 학습 목표**: 학습 목표 2
- **실습 목적**: 품질이 낮은 기획서를 분석하고 개선점을 도출한다
- **실습 유형**: 분석 + 개선
- **난이도**: 중급
- **예상 소요 시간**: 25분 (I DO 5분 / WE DO 8분 / YOU DO 12분)
- **선행 조건**: 실습 1 완료
- **실행 환경**: 로컬 (문서 작성 + Python 코드 실행)

**I DO**: 강사가 아래 "나쁜 기획서"의 문제점을 항목별로 분석하고 개선 방향을 설명한다.

**WE DO**: 첫 3개 항목(목적, 입력, 출력)을 함께 개선한다. 매 항목마다 멈추고 "왜 이렇게 써야 하는가?"를 토론한다.

**YOU DO**: 나머지 항목(제약조건, 성공기준, 범위)을 스스로 개선하고, `validate_spec_quality()`로 개선 전후를 비교한다.

```python
bad_spec_to_fix = {
    "purpose": "AI 챗봇을 만들어서 고객 서비스를 개선한다",
    "inputs": [{"name": "user_input"}],
    "outputs": [{"name": "answer"}],
    "constraints": [{"rule": "적절하게 동작해야 한다"}],
    "success_criteria": [{"metric": "성능이 좋아야 한다"}],
    "in_scope": ["모든 고객 문의 처리"],
    "out_of_scope": [],
}
# 각 항목의 문제점을 분석하고 개선하세요
```

**검증 기준:**
- 모든 6개 항목에 대해 문제점이 분석되었는가
- 개선 후 기획서가 검증 등급 A를 받는가
- 개선 사유가 구체적으로 설명되었는가

---

### 실습 3: 기획서에서 기술 설계 초안 도출

- **연관 학습 목표**: 학습 목표 3
- **실습 목적**: 작성한 기획서를 기술 설계 문서로 변환하고, 아키텍처 선택을 정당화한다
- **실습 유형**: 설계
- **난이도**: 중급
- **예상 소요 시간**: 30분 (I DO 5분 / WE DO 10분 / YOU DO 15분)
- **선행 조건**: 실습 1 완료
- **실행 환경**: 로컬 (문서 작성 + Python 코드 실행)

**I DO**: 강사가 CS Agent 기획서를 `spec_to_technical_design()` 함수로 변환하고, 자동 생성된 기술 설계의 의미를 설명한다.

**WE DO**: "Guardrail 도출" 단계를 함께 수행한다. 제약조건 3개를 각각 어떤 기술 컴포넌트로 변환하는지 함께 토론한다.

**YOU DO**: 실습 1에서 작성한 기획서를 기술 설계로 변환하고, 아래 항목을 보완한다.

```python
design_supplement = {
    "아키텍처_선택_근거": {
        "선택": "Agent / RAG / Hybrid 중 하나",
        "근거": ["이유 1", "이유 2"],
        "대안_배제_이유": "...",
    },
    "에러_시나리오": [
        {"시나리오": "LLM 타임아웃", "대응": "기획서 제약조건 참고"},
        {"시나리오": "입력 언어 미지원", "대응": "..."},
        {"시나리오": "외부 API 장애", "대응": "..."},
    ],
}
```

**검증 기준:**
- 아키텍처 선택이 기획서의 목적/범위와 논리적으로 일치하는가
- 기획서의 모든 제약조건이 기술 설계의 구체적 컴포넌트에 매핑되었는가
- 에러 시나리오가 최소 3개 이상 정의되었는가

---

## 핵심 정리

- Agent 기획서는 **기획자-개발자-이해관계자 간의 계약**이다
- 기획서 없이 개발하면 → 범위 확장, 성공 기준 부재, 입출력 불일치가 발생한다
- 6가지 핵심 구성요소: **목적, 입력, 출력, 제약조건, 성공 기준, 범위 경계**
- 좋은 기획서의 핵심: **구체성과 측정 가능성** ("잘 동작한다" → "정확도 90% 이상, 주간 50건 샘플링")
- 기획서 → 기술 설계는 **1:1 매핑**: 목적→아키텍처, 제약→Guardrail, 성공 기준→테스트
