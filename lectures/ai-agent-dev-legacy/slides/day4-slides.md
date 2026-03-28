---
theme: default
title: 'Day 4 — 평가 · 운영 · 확장 아키텍처 전략'
info: AI Agent 전문 개발 과정 Day 4
transition: slide-left
mdc: true
---

# Day 4
## 평가 · 운영 · 확장 아키텍처 전략

AI Agent 전문 개발 과정

<!-- [스크립트]
오늘은 만든 Agent를 제대로 측정하고, 운영하고, 확장하는 방법을 다룹니다.
개발보다 운영이 더 오래 걸립니다. 오늘 배우는 내용이 실무에서 가장 자주 써먹는 부분입니다.
[Q&A 대비] "왜 운영을 Day 4에 배우나요?" → 개발을 이해해야 운영 설계가 가능하기 때문입니다.
전환: 첫 세션인 품질 평가부터 시작합니다.
시간: 3분
-->

---
transition: fade
layout: section
---

# Session 1
## Agent 품질 평가 체계 설계

<!-- [스크립트]
"측정할 수 없으면 개선할 수 없다." 이 원칙을 Agent에 적용하는 시간입니다.
시간: 1분
-->

---

# 품질 평가 없이 일어나는 일

<v-clicks>

- "잘 되는 것 같다"는 직관만 남는다
- 버그가 생겨도 언제부터인지 알 수 없다
- 개선 방향을 숫자 없이 결정한다
- 신뢰할 수 없는 시스템이 된다

</v-clicks>

<v-click>

> 금융 기업 사례: Faithfulness 0.6 → 원인 불명 → 평가 도입 후 청크 크기 조정으로 0.85 달성

</v-click>

<!-- [스크립트]
[click] 직관에 의존하는 팀의 공통점입니다. 숫자가 없으면 논쟁도 끝이 없습니다.
[click] 버그 발생 시점을 특정 못하면 원인 분석이 불가능합니다.
[click] 근거 없는 개선은 운이 좋아야 효과가 납니다.
[click] 결국 시스템에 대한 신뢰가 사라집니다.
[click] 실제 사례입니다. 평가 체계 하나로 문제를 정확히 찾았습니다.
전환: 무엇을 측정해야 하는지 살펴봅시다.
시간: 4분
-->

---

# 품질 평가 3축

<div class="grid grid-cols-3 gap-6 mt-8">
<div class="bg-blue-50 border-2 border-blue-400 rounded-xl p-6 text-center">
  <div class="text-3xl mb-3">🎯</div>
  <strong class="text-blue-700 text-lg">Accuracy</strong>
  <p class="mt-2 text-sm">정답과 얼마나 일치하는가</p>
  <p class="mt-1 text-xs text-gray-500">최종 응답 vs. 기대 응답</p>
</div>
<div class="bg-green-50 border-2 border-green-400 rounded-xl p-6 text-center">
  <div class="text-3xl mb-3">📄</div>
  <strong class="text-green-700 text-lg">Faithfulness</strong>
  <p class="mt-2 text-sm">출처에 근거한 응답인가</p>
  <p class="mt-1 text-xs text-gray-500">응답 vs. 검색된 문서</p>
</div>
<div class="bg-purple-50 border-2 border-purple-400 rounded-xl p-6 text-center">
  <div class="text-3xl mb-3">🛡</div>
  <strong class="text-purple-700 text-lg">Robustness</strong>
  <p class="mt-2 text-sm">입력 변형에 일관된가</p>
  <p class="mt-1 text-xs text-gray-500">표현 바꿔도 같은 답?</p>
</div>
</div>

<!-- [스크립트]
세 축을 독립적으로 측정해야 합니다. 하나가 좋아도 나머지가 나쁠 수 있습니다.
Accuracy만 높고 Faithfulness가 낮으면 환각 위험이 있는 시스템입니다.
전환: 각 축을 어떻게 측정하는지 봅시다.
시간: 3분
-->

---

# 평가 레벨 구조

```
Unit Level    → 단일 LLM 호출 품질
Step Level    → 하나의 Agent 스텝 (Tool 호출 포함)
Task Level    → 전체 Task 완료 여부
System Level  → 비용 · 안전성 · UX
```

<v-clicks>

- **Unit/Step** → CI/CD에서 자동화
- **Task** → 스테이징 Golden Test Set 통과 기준
- **System** → 주간/월간 리뷰

</v-clicks>

<!-- [스크립트]
레벨마다 측정 주기와 담당자가 다릅니다.
[click] 개발 단계에서 자동화로 빠르게 피드백 받습니다.
[click] 스테이징에서는 전체 Task를 통과해야 배포합니다.
[click] 시스템 수준은 경영진과 함께 검토합니다.
전환: 정량 vs. 정성 평가의 차이를 봅시다.
시간: 3분
-->

---

# 정량 vs. 정성 평가

<div class="grid grid-cols-2 gap-8 mt-6">
<div class="bg-blue-50 rounded-xl p-6">
  <strong class="text-blue-700 text-lg">정량 평가</strong>
  <v-clicks>
  <ul class="mt-3 space-y-2 text-sm">
    <li>자동화 가능 · 빠른 피드백</li>
    <li>ROUGE, BLEU, EM, F1</li>
    <li>재현 가능</li>
    <li class="text-red-500">의미적 정확성을 놓칠 수 있음</li>
  </ul>
  </v-clicks>
</div>
<div class="bg-orange-50 rounded-xl p-6">
  <strong class="text-orange-700 text-lg">정성 평가</strong>
  <v-clicks>
  <ul class="mt-3 space-y-2 text-sm">
    <li>사람이 직접 판단</li>
    <li>높은 신뢰도</li>
    <li>LM-as-a-Judge로 부분 대체</li>
    <li class="text-red-500">비용·시간 소모 큼</li>
  </ul>
  </v-clicks>
</div>
</div>

<!-- [스크립트]
[click×4] 정량 평가는 빠르지만 의미를 놓칩니다.
[click×4] 정성 평가는 정확하지만 비쌉니다.
두 가지를 조합하는 것이 실무 표준입니다.
전환: LM-as-a-Judge가 이 둘의 균형을 맞춰줍니다.
시간: 4분
-->

---

# LM-as-a-Judge

<!-- IMAGE: LLM이 심판 역할로 두 응답을 저울에 올리는 일러스트레이션. 검색 키워드: "LLM judge evaluation AI illustration" -->

<v-clicks>

- GPT-4/Claude 급 모델이 **평가자 역할**
- 사람 판단과 상관관계 **0.8 이상**
- 비용은 사람보다 **10~100배 저렴**
- 서술형·다단계 평가에 강점

</v-clicks>

<!-- [스크립트]
[click] 강력한 모델을 평가자로 쓰는 아이디어입니다.
[click] 학술 연구에서 사람과의 일치도가 검증됐습니다.
[click] 비용 효율이 핵심 장점입니다.
[click] 단답형보다 서술형에서 진가를 발휘합니다.
전환: LM-as-a-Judge를 쓸 때 주의사항이 있습니다.
시간: 3분
-->

---

# LM-as-a-Judge 편향 제거

<v-clicks>

- **위치 편향** → 응답 순서를 무작위로 바꿔 두 번 평가
- **자기 선호 편향** → 평가 모델 ≠ 생성 모델
- **보상 해킹** → 평가 기준 주기적 변경 + 사람 교차 검증

</v-clicks>

```python {all|4-5|7-8}
def pairwise_judge(question, response_a, response_b):
    # 순서 무작위화로 위치 편향 제거
    result1 = single_eval(response_a, response_b, "A", "B")
    result2 = single_eval(response_b, response_a, "B", "A")
    # 두 판정 일치 여부로 신뢰도 판단
    if result1["winner"] == "A" and result2["winner"] == "B":
        return {"winner": "A", "confidence": "high"}
    return {"winner": "tie", "confidence": "low"}
```

<!-- [스크립트]
[click] 위치 편향은 순서만 바꿔도 해결됩니다.
[click] 자기 선호 편향은 평가 모델을 다르게 쓰면 됩니다.
[click] 보상 해킹은 정기적인 기준 갱신으로 억제합니다.
코드에서 핵심은 result1과 result2가 일치할 때만 high confidence를 줍니다.
전환: Golden Test Set을 어떻게 만드는지 봅시다.
시간: 4분
-->

---

# Golden Test Set 설계

<v-clicks>

- **최소 50건**, 이상적으로 200~500건
- 카테고리별 균형 (Accuracy / Faithfulness / Robustness)
- **격리된 저장소**에서 버전 관리
- 6개월마다 갱신

</v-clicks>

```python
@dataclass
class GoldenTestCase:
    id: str
    category: str   # "accuracy" | "faithfulness" | "robustness"
    input: dict
    expected_output: str
    tolerance: float = 0.8  # 합격 기준 점수
```

<!-- [스크립트]
[click] 건수는 많을수록 좋지만 20~30건으로 시작해도 됩니다.
[click] 카테고리 편중이 생기면 편향된 평가가 됩니다.
[click] 학습 데이터와 섞이면 측정값이 오염됩니다. 반드시 격리합니다.
[click] 사용자 패턴이 바뀌므로 주기적 갱신이 필수입니다.
전환: 퀴즈로 세션 1을 정리합시다.
시간: 3분
-->

---
layout: center
---

# 퀴즈

Faithfulness 지표가 낮다는 것은 무엇을 의미하는가?

<div class="relative mt-8">
<div class="grid grid-cols-2 gap-4">
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">A. 응답 속도가 느리다</div>
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">B. 정답 데이터와 일치하지 않는다</div>
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">C. 문서에 근거하지 않는 환각이 많다</div>
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">D. 모델 크기가 작다</div>
</div>
<div v-click-hide class="absolute inset-0 bg-white/0"></div>
<div v-click class="absolute inset-0 flex items-center justify-center">
  <div class="bg-green-100 border-2 border-green-500 rounded-xl p-6 text-center">
    <strong class="text-green-700 text-xl">C. 문서에 근거하지 않는 환각이 많다</strong>
  </div>
</div>
</div>

<!-- [스크립트]
Faithfulness는 검색 문서와 응답의 관계입니다.
[click] C가 정답입니다. 모델이 문서를 무시하고 자체 지식으로 답변한다는 의미입니다.
전환: 다음 세션은 성능 개선 전략입니다.
시간: 3분
-->

---
transition: fade
layout: section
---

# Session 2
## Prompt · RAG · Tool 성능 개선 전략

<!-- [스크립트]
배포 후 성능이 떨어지는 상황, 경험해 보셨나요? 오늘 그 원인을 체계적으로 찾는 방법을 배웁니다.
시간: 1분
-->

---

# 성능 저하의 3가지 원인

<div class="grid grid-cols-3 gap-6 mt-8">
<div class="bg-red-50 border-l-4 border-red-400 p-5 rounded-r-xl">
  <strong class="text-red-700">Prompt Drift</strong>
  <p class="mt-2 text-sm">여러 번 수정되며 의도가 흐려진다</p>
</div>
<div class="bg-orange-50 border-l-4 border-orange-400 p-5 rounded-r-xl">
  <strong class="text-orange-700">Retrieval Drift</strong>
  <p class="mt-2 text-sm">문서 업데이트로 검색 결과가 달라진다</p>
</div>
<div class="bg-yellow-50 border-l-4 border-yellow-400 p-5 rounded-r-xl">
  <strong class="text-yellow-700">Tool Drift</strong>
  <p class="mt-2 text-sm">API·스키마 변경으로 호출 실패가 늘어난다</p>
</div>
</div>

<v-click>

> 원인을 모르면 고칠 수 없다. 진단이 개선의 시작이다.

</v-click>

<!-- [스크립트]
세 가지 Drift가 동시에 일어나는 경우도 많습니다.
[click] 진단 없이 직관으로 수정하면 오히려 나빠질 수 있습니다.
전환: 체계적인 진단 프레임워크를 봅시다.
시간: 3분
-->

---

# 성능 저하 진단 4단계

```
1단계: 증상 확인
   → 어느 지표가 떨어졌는가?

2단계: 계층 격리
   → LLM 자체? 검색? Tool 호출?

3단계: 시점 특정
   → 언제부터? 그 시점에 무엇이 바뀌었나?

4단계: 재현
   → Golden Test로 추가 → 수정 전후 점수 비교
```

<v-click>

**4단계를 지키면 "감으로 고치는" 함정을 피할 수 있다**

</v-click>

<!-- [스크립트]
이 4단계는 의사가 환자를 진단하는 방식과 동일합니다.
증상(열)만 보고 치료하면 틀릴 수 있습니다. 원인을 찾아야 합니다.
[click] 4단계를 따르면 논리적 근거가 생깁니다.
전환: Prompt 버전 관리를 봅시다.
시간: 3분
-->

---

# Prompt 버전 관리

<div class="grid grid-cols-2 gap-8 mt-4">
<div>

**SemVer 규칙**

| 변경 유형 | 버전 |
|---|---|
| 형식만 수정 | Patch (v1.0.1) |
| 동작 개선 | Minor (v1.1.0) |
| 목적 변경 | Major (v2.0.0) |

</div>
<div>

<v-clicks>

- 코드 저장소에 **파일로 관리**
- CHANGELOG에 변경 이유 기록
- A/B 테스트로 성능 검증 후 전환
- 롤백 기능 필수

</v-clicks>

</div>
</div>

<!-- [스크립트]
프롬프트가 코드처럼 관리되지 않으면 "이전이 더 좋았는데"에서 복구할 수 없습니다.
[click×4] 네 가지 원칙을 함께 지켜야 효과가 있습니다.
전환: Retrieval Drift를 측정하는 방법을 봅시다.
시간: 3분
-->

---

# Retrieval Drift 감지

```
Retrieval Stability Score
= |t2 top-k| ∩ |t1 top-k| / k
```

<v-clicks>

- t1에서 [A, B, C] → t2에서 [A, D, E] → Score = 1/3
- **임계값 0.7 이하** → 드리프트 경보 발생
- 원인별 대응:
  - 문서 추가/삭제 → 인덱스 변경 로그 추적
  - 임베딩 모델 변경 → 전체 재인덱스 + 성능 비교

</v-clicks>

<!-- [스크립트]
[click] 수식은 단순합니다. 교집합을 k로 나눕니다.
[click] 임계값은 도메인마다 다를 수 있지만 0.7이 일반적 시작점입니다.
[click] 원인별로 대응 방법이 다릅니다. 진단 후 맞는 처방을 씁니다.
전환: Tool 호출 실패 유형을 봅시다.
시간: 3분
-->

---

# Tool 호출 실패 4유형

<div class="grid grid-cols-2 gap-5 mt-6">
<div class="bg-red-50 rounded-xl p-4">
  <strong class="text-red-700">Type 1 — Wrong Tool</strong>
  <p class="text-sm mt-1">엉뚱한 Tool 선택</p>
  <p class="text-xs text-gray-500 mt-1">→ Tool 설명 개선</p>
</div>
<div class="bg-orange-50 rounded-xl p-4">
  <strong class="text-orange-700">Type 2 — Wrong Params</strong>
  <p class="text-sm mt-1">잘못된 파라미터</p>
  <p class="text-xs text-gray-500 mt-1">→ Few-shot 예시 추가</p>
</div>
<div class="bg-yellow-50 rounded-xl p-4">
  <strong class="text-yellow-700">Type 3 — No Validation</strong>
  <p class="text-sm mt-1">파라미터 범위/타입 오류</p>
  <p class="text-xs text-gray-500 mt-1">→ Validation 레이어 추가</p>
</div>
<div class="bg-purple-50 rounded-xl p-4">
  <strong class="text-purple-700">Type 4 — Schema Mismatch</strong>
  <p class="text-sm mt-1">API 스키마 변경 미반영</p>
  <p class="text-xs text-gray-500 mt-1">→ 스키마 변경 자동 감지</p>
</div>
</div>

<!-- [스크립트]
Tool 실패는 유형마다 원인과 해결책이 다릅니다.
로그를 보면 어떤 유형인지 바로 알 수 있습니다.
전환: 성능 개선 우선순위를 어떻게 정하는지 봅시다.
시간: 3분
-->

---

# 성능 개선 우선순위

<!-- IMAGE: 2x2 매트릭스 차트 - 영향도(Y축) vs 발생 빈도(X축). 4사분면에 P0/P1/P2/P3 레이블. 검색 키워드: "priority matrix impact frequency quadrant chart" -->

<div class="grid grid-cols-2 gap-4 mt-4">
<div class="bg-red-100 rounded-xl p-4">
  <strong class="text-red-700">P0 — 즉시 수정</strong>
  <p class="text-sm">높은 영향 + 높은 빈도</p>
</div>
<div class="bg-orange-100 rounded-xl p-4">
  <strong class="text-orange-700">P1 — 다음 스프린트</strong>
  <p class="text-sm">높은 영향 + 낮은 빈도</p>
</div>
<div class="bg-yellow-100 rounded-xl p-4">
  <strong class="text-yellow-700">P2 — 자동화로 억제</strong>
  <p class="text-sm">낮은 영향 + 높은 빈도</p>
</div>
<div class="bg-gray-100 rounded-xl p-4">
  <strong class="text-gray-700">P3 — 백로그</strong>
  <p class="text-sm">낮은 영향 + 낮은 빈도</p>
</div>
</div>

<!-- [스크립트]
모든 문제를 동시에 고치려다 번아웃이 옵니다.
매트릭스로 팀이 합의된 우선순위를 가져야 합니다.
전환: 세션 2 퀴즈입니다.
시간: 3분
-->

---
layout: center
---

# 퀴즈

모델 버전 업그레이드 전 반드시 해야 할 것은?

<div class="relative mt-8">
<div class="grid grid-cols-2 gap-4">
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">A. Fine-tuning 재수행</div>
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">B. Golden Test Set 회귀 테스트</div>
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">C. 임베딩 모델 교체</div>
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">D. 서버 스케일 업</div>
</div>
<div v-click-hide class="absolute inset-0 bg-white/0"></div>
<div v-click class="absolute inset-0 flex items-center justify-center">
  <div class="bg-green-100 border-2 border-green-500 rounded-xl p-6 text-center">
    <strong class="text-green-700 text-xl">B. Golden Test Set 회귀 테스트</strong>
    <p class="text-sm mt-2">같은 프롬프트도 모델 버전마다 다르게 동작한다</p>
  </div>
</div>
</div>

<!-- [스크립트]
[click] 모델이 바뀌면 동작이 달라질 수 있습니다. 회귀 테스트가 안전망입니다.
전환: 세션 3, 로그와 모니터링입니다.
시간: 2분
-->

---
transition: fade
layout: section
---

# Session 3
## 로그 · 모니터링 · 장애 대응 설계

<!-- [스크립트]
운영 중 장애가 나면 제일 먼저 찾는 것이 로그입니다. 로그가 없으면 수사가 불가능합니다.
시간: 1분
-->

---

# 로그 없이 장애 대응하면

<v-clicks>

- 언제 문제가 생겼는지 모른다
- 영향 범위를 파악할 수 없다
- 재현이 안 되면 수정도 안 된다
- "다시 배포하면 되겠지"가 반복된다

</v-clicks>

<v-click>

> 이커머스 사례: Tool 무한 루프 → 로그 없음 → 영향 범위 파악에 **6시간** 소요
> 로그 설계 후 동일 장애 → **15분** 해결

</v-click>

<!-- [스크립트]
[click×4] 로그 없는 팀의 공통 패턴입니다.
[click] 6시간 vs 15분. 차이는 로그 설계 하나입니다.
전환: Trace 로그 구조를 설계합시다.
시간: 3분
-->

---

# Trace 계층 구조

```
Trace (요청 단위, trace_id)
  └── Span (스텝 단위)
        ├── LLM Span  → 모델 호출
        ├── Tool Span → Tool 실행
        └── RAG Span  → 검색 + 청크 반환
```

<v-clicks>

- 하나의 **요청 = 하나의 Trace**
- 하나의 **처리 단계 = 하나의 Span**
- `trace_id`로 전체 흐름을 추적
- `parent_span_id`로 계층 관계 표현

</v-clicks>

<!-- [스크립트]
일반 API 로그와의 차이점입니다.
Agent 요청 하나가 수십 개의 LLM·Tool 호출로 이어집니다.
이 전체를 하나의 Trace로 묶어야 "어디서 느려졌는지" 알 수 있습니다.
[click×4] 네 가지 개념을 기억하세요.
전환: Trace 로그에 어떤 필드가 들어가야 하는지 봅시다.
시간: 3분
-->

---

# Trace 필수 필드

<div class="grid grid-cols-2 gap-4 mt-4 text-sm">
<div>

| 필드 | 설명 |
|---|---|
| `trace_id` | 요청 전체 ID |
| `span_id` | 개별 스텝 ID |
| `parent_span_id` | 상위 Span |
| `timestamp` | ISO 8601 |
| `latency_ms` | 처리 시간 |

</div>
<div>

| 필드 | 설명 |
|---|---|
| `input_tokens` | 입력 토큰 수 |
| `output_tokens` | 출력 토큰 수 |
| `model` | 사용 모델 |
| `status` | success/error |
| `user_id` | 사용자 ID (마스킹) |

</div>
</div>

<!-- [스크립트]
이 10개 필드가 있으면 대부분의 장애를 추적할 수 있습니다.
user_id는 반드시 마스킹하거나 해시 처리해 저장합니다.
전환: 장애 유형을 분류합시다.
시간: 2분
-->

---

# 장애 유형 4분류

<div class="grid grid-cols-2 gap-5 mt-6">
<div class="bg-red-50 rounded-xl p-4">
  <strong class="text-red-700">Type A — LLM 품질</strong>
  <p class="text-sm mt-1">환각, 형식 오류, 부적절한 응답</p>
  <p class="text-xs text-gray-500 mt-1">감지: Faithfulness/Accuracy 모니터링</p>
</div>
<div class="bg-orange-50 rounded-xl p-4">
  <strong class="text-orange-700">Type B — Tool 실행</strong>
  <p class="text-sm mt-1">호출 실패, 무한 루프, 잘못된 파라미터</p>
  <p class="text-xs text-gray-500 mt-1">감지: Tool 성공률, 타임아웃</p>
</div>
<div class="bg-blue-50 rounded-xl p-4">
  <strong class="text-blue-700">Type C — RAG</strong>
  <p class="text-sm mt-1">검색 결과 없음, 무관한 문서 반환</p>
  <p class="text-xs text-gray-500 mt-1">감지: Retrieval 품질 지표</p>
</div>
<div class="bg-purple-50 rounded-xl p-4">
  <strong class="text-purple-700">Type D — 시스템</strong>
  <p class="text-sm mt-1">타임아웃, OOM, 서비스 다운</p>
  <p class="text-xs text-gray-500 mt-1">감지: 인프라 메트릭</p>
</div>
</div>

<!-- [스크립트]
장애 유형을 분류하면 대응 담당자와 절차가 달라집니다.
Type A는 ML 팀, Type B는 백엔드 팀, Type D는 인프라 팀이 주도합니다.
전환: 5-Why로 근본 원인을 찾는 방법을 봅시다.
시간: 3분
-->

---

# 5-Why: 근본 원인 분석

```
문제: 잘못된 정책 정보를 반환했다.

Why 1 → 구버전 정책 문서가 검색됐다.
Why 2 → 정책 업데이트 시 인덱스가 갱신되지 않았다.
Why 3 → 문서 업데이트 파이프라인에 인덱스 트리거가 없다.
Why 4 → 초기 설계 시 문서 업데이트 빈도를 과소평가했다.
Why 5 → 정책 담당자가 개발팀과 연결되지 않았다.

근본 원인: 부서 간 프로세스 미정의
```

<v-click>

**증상이 아닌 근본 원인을 고쳐야 재발이 없다**

</v-click>

<!-- [스크립트]
5단계를 따라가면 버그가 아니라 조직 프로세스 문제가 드러납니다.
이것이 5-Why의 진짜 가치입니다.
[click] 재발 방지는 근본 원인 수준에서만 가능합니다.
전환: Guardrail 설계를 봅시다.
시간: 4분
-->

---

# Guardrail 적용 위치

```
[사용자 입력]
    ↓
[Input Guardrail]    ← PII · 인젝션 · 유해 콘텐츠 감지
    ↓
[Agent 처리]
    ↓
[Tool Call Validation]  ← 파라미터 타입/범위 검증
    ↓
[Output Guardrail]   ← 민감 정보 필터링 · 형식 검증
    ↓
[사용자 응답]
```

<v-click>

입력·출력 양쪽에서 모두 검사해야 한다

</v-click>

<!-- [스크립트]
Guardrail은 방화벽과 같습니다. 입력에서 한 번, 출력에서 한 번 검사합니다.
중간 Tool 호출도 검증 레이어가 필요합니다.
[click] 한쪽만 막으면 우회 경로가 생깁니다.
전환: 알림 임계값 설계를 봅시다.
시간: 3분
-->

---

# 알림 임계값 설계

| 임계값 | 채널 | 대응 시간 |
|---|---|---|
| 오류율 > 5% (5분) | PagerDuty | 즉시 (On-call) |
| Faithfulness < 0.6 | Slack | 2시간 내 |
| 평균 응답 > 10s | Slack | 업무 시간 내 |
| 토큰 비용 > 예산 80% | 이메일 | 다음날 |

<v-click>

**알림이 너무 많으면 알림 피로(Alert Fatigue)가 생긴다**

</v-click>

<!-- [스크립트]
모든 로그에 알림을 보내면 아무도 보지 않게 됩니다.
중요도와 긴급성을 기준으로 임계값을 설계합니다.
[click] Alert Fatigue는 실제로 P0 장애 알림을 놓치는 원인이 됩니다.
전환: 퀴즈로 세션 3을 마무리합시다.
시간: 2분
-->

---
layout: center
---

# 퀴즈

대규모 운영 환경에서 권장하는 로깅 전략은?

<div class="relative mt-8">
<div class="grid grid-cols-2 gap-4">
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">A. 전수 로깅</div>
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">B. 오류만 로깅</div>
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">C. 오류 전수 + 정상 10% 샘플링</div>
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">D. 메트릭만 수집</div>
</div>
<div v-click-hide class="absolute inset-0 bg-white/0"></div>
<div v-click class="absolute inset-0 flex items-center justify-center">
  <div class="bg-green-100 border-2 border-green-500 rounded-xl p-6 text-center">
    <strong class="text-green-700 text-xl">C. 오류 전수 + 정상 10% 샘플링</strong>
    <p class="text-sm mt-2">비용과 디버깅 능력의 균형</p>
  </div>
</div>
</div>

<!-- [스크립트]
[click] 오류는 반드시 전부 저장해야 합니다. 정상 트래픽은 샘플링으로 비용을 줄입니다.
전환: 마지막 세션, 아키텍처입니다.
시간: 2분
-->

---
transition: fade
layout: section
---

# Session 4
## 확장 가능한 서비스 아키텍처

<!-- [스크립트]
오늘의 마지막이자 가장 실무적인 내용입니다. 지금 당장 배포하는 아키텍처가 6개월 후 발목을 잡지 않으려면 어떻게 해야 할까요?
시간: 1분
-->

---

# 환경 분리 없이 성장하면

<v-clicks>

- 개발 중 실험이 운영 데이터에 영향을 준다
- 긴급 패치가 Prod에 바로 배포된다
- 환경별 설정이 코드에 하드코딩된다
- 환경 분리 리팩터링에 **수 주**가 소요된다

</v-clicks>

<v-click>

> 스타트업 사례: B2B 고객 20곳 붙은 후 환경 분리에 6주 소요 → 기능 개발 전면 중단

</v-click>

<!-- [스크립트]
[click×4] 환경 분리 안 한 팀의 전형적인 패턴입니다.
[click] 6주는 스타트업에게 치명적입니다. 미리 분리해야 합니다.
전환: 세 환경의 역할을 정의합시다.
시간: 3분
-->

---

# Dev · Staging · Prod 역할

| 환경 | 목적 | 데이터 | 모델 |
|---|---|---|---|
| **Dev** | 개발·실험 | 합성/샘플 | gpt-4o-mini |
| **Staging** | 검증·QA | 익명화 복사본 | 운영과 동일 |
| **Prod** | 실제 서비스 | 실제 운영 | 운영 모델 |

<v-click>

- 환경 변수로 모델명·API 키·인덱스를 분리
- `config/dev.yaml`, `config/prod.yaml`로 관리
- 코드에 환경명 하드코딩 **절대 금지**

</v-click>

<!-- [스크립트]
세 환경은 목적, 데이터, 모델이 모두 달라야 합니다.
Dev에서 비싼 모델을 쓰면 개발 비용이 폭등합니다.
[click] 환경 변수와 설정 파일로 코드 변경 없이 환경을 전환합니다.
전환: Scaling 전략을 봅시다.
시간: 3분
-->

---

# Scaling 전략 비교

<div class="grid grid-cols-2 gap-8 mt-6">
<div class="bg-red-50 rounded-xl p-6">
  <strong class="text-red-700 text-lg">수직 Scaling (Scale Up)</strong>
  <v-clicks>
  <ul class="mt-3 space-y-2 text-sm">
    <li>서버 사양(CPU/메모리) 증가</li>
    <li>한계가 명확함</li>
    <li>비용이 급격히 증가</li>
    <li class="text-red-600">단기 임시방편</li>
  </ul>
  </v-clicks>
</div>
<div class="bg-blue-50 rounded-xl p-6">
  <strong class="text-blue-700 text-lg">수평 Scaling (Scale Out)</strong>
  <v-clicks>
  <ul class="mt-3 space-y-2 text-sm">
    <li>동일 인스턴스 여러 개 실행</li>
    <li>Stateless 설계가 전제</li>
    <li>세션 상태 → Redis/DB에 저장</li>
    <li class="text-blue-600">Agent 서비스 권장 방식</li>
  </ul>
  </v-clicks>
</div>
</div>

<!-- [스크립트]
[click×4] 수직 Scaling은 쉽지만 한계가 있습니다.
[click×4] 수평 Scaling이 Agent 서비스의 정답입니다.
핵심은 Stateless 설계입니다. 서버가 상태를 갖지 않아야 Scale Out이 가능합니다.
전환: Stateless 설계가 왜 중요한지 봅시다.
시간: 4분
-->

---

# Stateless 설계의 핵심

<div class="grid grid-cols-2 gap-8 mt-6">
<div class="bg-red-50 border-2 border-red-300 rounded-xl p-6">
  <strong class="text-red-700">상태를 서버 메모리에 저장</strong>
  <div class="mt-4 text-sm space-y-2">
    <p>→ 서버 A에서 시작한 요청이</p>
    <p>→ 서버 B로 가면 상태 유실</p>
    <p>→ Scale Out 불가</p>
  </div>
</div>
<div class="bg-blue-50 border-2 border-blue-300 rounded-xl p-6">
  <strong class="text-blue-700">상태를 외부 저장소에 저장</strong>
  <div class="mt-4 text-sm space-y-2">
    <p>→ 모든 서버가 Redis/DB에서 읽음</p>
    <p>→ 어느 서버도 요청 처리 가능</p>
    <p>→ Scale Out 자유롭게 가능</p>
  </div>
</div>
</div>

<!-- [스크립트]
이 원칙 하나가 수평 Scaling의 전제입니다.
Agent의 대화 히스토리, 세션 상태는 Redis에 저장합니다.
전환: Multi-Agent 구조를 봅시다.
시간: 3분
-->

---

# Multi-Agent 3가지 패턴

```
패턴 1: Orchestrator-Worker
  Orchestrator → Task 분해 → Worker에게 위임
  적합: 복잡한 장문 Task

패턴 2: Pipeline (순차)
  Intake → Classify → Retrieve → Generate → Validate
  적합: 명확한 처리 흐름

패턴 3: Parallel Fan-out
  동일 입력 → 여러 Agent 병렬 처리 → 결과 합산
  적합: 다각도 분석, 교차 검증
```

<!-- [스크립트]
세 패턴은 서로 조합해서 쓸 수도 있습니다.
처음에는 Pipeline이 가장 이해하기 쉽습니다.
전환: 언제 Multi-Agent로 전환해야 하는지 기준을 봅시다.
시간: 3분
-->

---

# Multi-Agent 전환 기준

| 조건 | 단일 Agent | Multi-Agent |
|---|---|---|
| Task 복잡도 | 단순 (≤3 스텝) | 복잡 (5+ 스텝) |
| 컨텍스트 길이 | 짧음 | 길거나 누적됨 |
| 도메인 전문성 | 범용 | 여러 전문 영역 |
| 오류 격리 필요 | 낮음 | 높음 |

<v-click>

> "지금 당장 필요한가?" — 항상 이 질문을 먼저 한다

</v-click>

<!-- [스크립트]
조건 하나만 맞는다고 Multi-Agent로 가면 오버엔지니어링입니다.
여러 조건이 동시에 충족될 때 전환을 검토합니다.
[click] 이 질문이 오버엔지니어링을 막는 가장 좋은 방법입니다.
전환: 비용 최적화를 봅시다.
시간: 3분
-->

---

# 모델 계층화 전략

<div class="grid grid-cols-3 gap-5 mt-6">
<div class="bg-green-50 border-2 border-green-300 rounded-xl p-5 text-center">
  <strong class="text-green-700">단순 분류/필터</strong>
  <div class="mt-3 text-2xl font-bold text-green-600">gpt-4o-mini</div>
  <div class="mt-2 text-xs text-gray-500">저비용 · 빠름</div>
</div>
<div class="bg-blue-50 border-2 border-blue-300 rounded-xl p-5 text-center">
  <strong class="text-blue-700">RAG 응답 생성</strong>
  <div class="mt-3 text-2xl font-bold text-blue-600">gpt-4o</div>
  <div class="mt-2 text-xs text-gray-500">균형</div>
</div>
<div class="bg-purple-50 border-2 border-purple-300 rounded-xl p-5 text-center">
  <strong class="text-purple-700">복잡한 추론</strong>
  <div class="mt-3 text-2xl font-bold text-purple-600">o3</div>
  <div class="mt-2 text-xs text-gray-500">고비용 · 최소화</div>
</div>
</div>

<v-click>

**모든 호출에 같은 모델을 쓰면 비용이 10배 이상 늘어난다**

</v-click>

<!-- [스크립트]
실무에서 80% 이상의 요청은 단순합니다. gpt-4o-mini로 처리하면 됩니다.
복잡한 추론이 필요한 경우는 소수이므로 o3를 선택적으로 씁니다.
[click] 계층화만 잘 해도 월 비용을 수십 % 절감할 수 있습니다.
전환: Semantic Cache를 봅시다.
시간: 3분
-->

---

# 비용 최적화 3가지 전략

<div class="grid grid-cols-3 gap-5 mt-6">
<div class="bg-blue-50 rounded-xl p-5">
  <strong class="text-blue-700">모델 계층화</strong>
  <p class="mt-2 text-sm">Task별 최적 모델 사용</p>
  <p class="mt-1 text-xs text-gray-500">효과: ★★★★★</p>
</div>
<div class="bg-green-50 rounded-xl p-5">
  <strong class="text-green-700">Semantic Cache</strong>
  <p class="mt-2 text-sm">유사 쿼리 캐시 히트</p>
  <p class="mt-1 text-xs text-gray-500">효과: ★★★★☆</p>
</div>
<div class="bg-orange-50 rounded-xl p-5">
  <strong class="text-orange-700">컨텍스트 압축</strong>
  <p class="mt-2 text-sm">히스토리 요약으로 토큰 절감</p>
  <p class="mt-1 text-xs text-gray-500">효과: ★★★☆☆</p>
</div>
</div>

<!-- [스크립트]
세 전략 중 모델 계층화가 효과가 가장 큽니다.
Semantic Cache는 반복 쿼리가 많은 서비스에서 특히 효과적입니다.
전환: 카나리 배포를 봅시다.
시간: 3분
-->

---

# 카나리 배포 파이프라인

```
코드 커밋
  ↓
CI (단위 테스트 + Golden Test Set)
  ↓
Dev 배포 (자동)
  ↓
Staging 배포 (자동) + 통합 테스트
  ↓
Prod 카나리 5% → 50% → 100%
  ↓
이상 감지 시 자동 롤백
```

<v-click>

- 5%에서 **1시간 관찰**
- 오류율·응답 시간 기준 통과 후 확대
- 문제 발생 → 즉시 이전 버전 롤백

</v-click>

<!-- [스크립트]
카나리 배포는 리스크를 분산합니다.
5%에서 문제가 생기면 95% 사용자는 영향을 받지 않습니다.
[click] 비율보다 중요한 것은 관찰 시간입니다.
전환: 마지막 퀴즈입니다.
시간: 3분
-->

---
layout: center
---

# 퀴즈

Agent 서비스가 수평 Scaling을 위해 반드시 지켜야 하는 원칙은?

<div class="relative mt-8">
<div class="grid grid-cols-2 gap-4">
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">A. 모든 상태를 서버 메모리에 저장</div>
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">B. Stateless 설계 + 외부 저장소 사용</div>
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">C. 단일 서버에서 스펙을 높인다</div>
<div class="bg-gray-100 rounded-xl p-4 text-center text-gray-600">D. 모든 요청을 동기식으로 처리</div>
</div>
<div v-click-hide class="absolute inset-0 bg-white/0"></div>
<div v-click class="absolute inset-0 flex items-center justify-center">
  <div class="bg-green-100 border-2 border-green-500 rounded-xl p-6 text-center">
    <strong class="text-green-700 text-xl">B. Stateless 설계 + 외부 저장소</strong>
    <p class="text-sm mt-2">세션 상태는 Redis/DB에 저장해야 Scale Out이 가능</p>
  </div>
</div>
</div>

<!-- [스크립트]
[click] B가 정답입니다. Stateless가 수평 Scaling의 전제조건입니다.
전환: Day 4 전체를 정리합시다.
시간: 2분
-->

---
layout: section
transition: fade
---

# Day 4 정리

---

# Day 4 핵심 요약

<v-clicks>

- **평가 3축**: Accuracy · Faithfulness · Robustness를 독립 측정
- **LM-as-a-Judge**: 편향 제거(순서 무작위화, 모델 분리) 후 사용
- **Golden Test Set**: 격리 저장, 버전 관리, 6개월마다 갱신
- **진단 4단계**: 증상 → 계층 격리 → 시점 특정 → 재현
- **Trace 로그**: Trace/Span 계층 구조로 전체 흐름 추적
- **Guardrail**: 입력·Tool·출력 세 지점에서 검증
- **환경 분리**: Dev/Staging/Prod 데이터와 모델을 분리
- **모델 계층화**: Task 복잡도별 최적 모델로 비용 최적화

</v-clicks>

<!-- [스크립트]
[click×8] 오늘 배운 8가지입니다.
각각은 독립적으로 적용할 수 있습니다.
내일 자신의 Agent에 하나씩 적용해 보세요.
전환: 실습으로 넘어갑니다.
시간: 3분
-->

---

# Day 4 실습 안내

<div class="grid grid-cols-2 gap-8 mt-6">
<div class="bg-blue-50 rounded-xl p-6">
  <strong class="text-blue-700 text-lg">Lab 1 — Golden Test Evaluation</strong>
  <ul class="mt-3 space-y-2 text-sm">
    <li>Golden Test Set 20건 설계</li>
    <li>LM-as-a-Judge 평가 파이프라인</li>
    <li>Faithfulness 자동 측정</li>
    <li>결과 대시보드 출력</li>
  </ul>
</div>
<div class="bg-green-50 rounded-xl p-6">
  <strong class="text-green-700 text-lg">Lab 2 — 운영 아키텍처 설계</strong>
  <ul class="mt-3 space-y-2 text-sm">
    <li>환경 분리 설계서 작성</li>
    <li>Scaling 전략 결정</li>
    <li>월간 비용 추정 계산</li>
    <li>카나리 배포 계획</li>
  </ul>
</div>
</div>

<!-- [스크립트]
Lab 1은 코드 실습, Lab 2는 설계 워크시트입니다.
둘 다 실무에서 바로 쓸 수 있는 산출물을 만드는 것이 목표입니다.
파이팅하세요!
시간: 2분
-->

---
layout: center
---

# 수고하셨습니다

**Day 4 — 평가 · 운영 · 확장 아키텍처 전략**

> 만든 것을 측정하고, 운영하고, 확장하는 것이 진짜 엔지니어링이다.

<!-- [스크립트]
오늘 배운 내용이 실무에서 가장 많이 쓰이는 부분입니다.
내일 Day 5에서는 지금까지 배운 모든 것을 통합해 실제 Agent를 완성합니다.
시간: 1분
-->
