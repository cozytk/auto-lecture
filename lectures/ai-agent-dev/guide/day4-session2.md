# Day 4 Session 2 — Prompt · RAG · Tool 성능 개선 전략

> **세션 목표**: 성능 저하 원인을 체계적으로 진단하고, Prompt 버전 관리·Retrieval Drift 대응·Tool 호출 정확도 개선 전략을 실무에 적용한다.

---

## 1. 왜 중요한가

### 배포 후 성능이 떨어지는 이유

Agent를 처음 배포하면 잘 동작한다.
시간이 지나면 서서히, 혹은 갑자기 품질이 떨어진다.
원인을 모르면 "프롬프트를 바꿔보자"는 감에 의존하게 된다.

**성능 저하의 3가지 주요 원인**:
- **Prompt Drift**: 프롬프트가 여러 번 수정되며 의도가 흐려진다.
- **Retrieval Drift**: 문서가 업데이트되며 검색 결과가 달라진다.
- **Tool Drift**: 외부 API·스키마가 변경되며 호출 실패가 늘어난다.

> 원인을 모르면 고칠 수 없다. 진단이 개선의 시작이다.

---

## 2. 핵심 원리

### 2.1 성능 저하 진단 프레임워크

```
1단계: 증상 확인
   → 어느 지표가 떨어졌는가? (Accuracy? Faithfulness? 호출 성공률?)

2단계: 계층 격리
   → LLM 응답 자체의 문제인가?
   → 검색 결과의 문제인가?
   → Tool 호출 파라미터의 문제인가?

3단계: 시점 특정
   → 언제부터 떨어졌는가?
   → 그 시점에 무엇이 바뀌었는가? (코드? 문서? 모델?)

4단계: 재현
   → 문제 케이스를 Golden Test로 추가
   → 수정 전후 점수 비교
```

### 2.2 Prompt 버전 관리

**왜 필요한가**: 프롬프트가 코드처럼 관리되지 않으면 "이전 버전이 더 좋았는데"라는 상황에서 복구할 수 없다.

**버전 관리 핵심 원칙**:
- 프롬프트를 코드 저장소에 파일로 관리한다.
- 변경마다 `v1.0.0 → v1.1.0` 식으로 SemVer를 부여한다.
- 변경 이유와 테스트 결과를 CHANGELOG에 기록한다.
- A/B 테스트로 신버전 성능을 검증 후 전환한다.

**프롬프트 변경 유형별 버전 규칙**:
| 변경 유형 | 버전 증가 | 예시 |
|---|---|---|
| 의미 변경 없는 형식 수정 | Patch (v1.0.0→v1.0.1) | 줄바꿈 조정 |
| 동작 개선·추가 | Minor (v1.0.0→v1.1.0) | 예시 추가 |
| 역할·목적 변경 | Major (v1.0.0→v2.0.0) | 시스템 프롬프트 전면 교체 |

### 2.3 Retrieval Drift 대응

**Retrieval Drift란**: 문서 업데이트·인덱스 변경으로 검색 결과가 시간에 따라 달라지는 현상이다.

**측정 방법**:
```
Retrieval Stability Score
= (t2에서 top-k 결과) ∩ (t1에서 top-k 결과) / k
```
예: t1에서 [doc_A, doc_B, doc_C]를 반환했는데, t2에서 [doc_A, doc_D, doc_E]를 반환하면 Stability = 1/3.

**원인별 대응**:
| 원인 | 대응 |
|---|---|
| 문서 추가/삭제 | 인덱스 변경 로그 추적 + 재평가 |
| 임베딩 모델 변경 | 전체 재인덱스 + 성능 비교 |
| 청크 크기 변경 | 변경 전후 Faithfulness 비교 |
| 쿼리 패턴 변화 | 최신 쿼리로 Golden Set 갱신 |

### 2.4 Tool 호출 정확도 개선

**Tool 호출 실패 유형**:
```
Type 1 — Wrong Tool Selected : 엉뚱한 Tool 선택
Type 2 — Wrong Parameters   : 올바른 Tool, 잘못된 파라미터
Type 3 — Missing Validation : 파라미터 범위/타입 오류
Type 4 — Schema Mismatch    : API 스키마 변경 미반영
```

**개선 전략**:
- Tool 설명을 명확하게 작성한다. (언제 쓰는가, 언제 쓰지 않는가)
- Few-shot 예시를 Tool 정의에 포함한다.
- 파라미터마다 validation 레이어를 추가한다.
- Tool 호출 로그를 주간 단위로 분석한다.

---

## 3. 실무 의미

### 3.1 성능 개선 우선순위 결정 방법

모든 문제를 한 번에 고치려 하면 안 된다.
**영향도 × 발생 빈도** 매트릭스로 우선순위를 정한다.

```
높은 영향 + 높은 빈도 → 즉시 수정 (P0)
높은 영향 + 낮은 빈도 → 다음 스프린트 (P1)
낮은 영향 + 높은 빈도 → 자동화로 억제 (P2)
낮은 영향 + 낮은 빈도 → 백로그 (P3)
```

### 3.2 A/B 테스트 설계

Prompt를 바꾸기 전에 A/B 테스트를 설계한다.
트래픽을 50:50으로 분리하고 48~72시간 운영한다.
통계적 유의성(p < 0.05)을 확인한 뒤 전환한다.

```python
# 트래픽 분배 예시
import hashlib

def get_prompt_version(user_id: str) -> str:
    hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    return "v2" if hash_val % 100 < 50 else "v1"
```

---

## 4. 비교: 성능 개선 접근법

| 접근법 | 효과 속도 | 리스크 | 적합한 상황 |
|---|---|---|---|
| Prompt 조정 | 빠름 | 낮음 | 응답 품질 미세 조정 |
| 청크 크기 변경 | 중간 | 중간 | Faithfulness 저하 |
| 임베딩 모델 교체 | 느림 | 높음 | 전반적 검색 품질 하락 |
| Fine-tuning | 매우 느림 | 높음 | 특수 도메인 장기 개선 |
| Tool 스키마 개선 | 빠름 | 낮음 | Tool 호출 실패율 높을 때 |

**우선 Prompt와 Tool 스키마부터 시작하라.**
비용과 리스크 대비 효과가 가장 빠르다.

---

## 5. 주의사항

### 5.1 성급한 Fine-tuning

성능이 떨어지면 바로 Fine-tuning을 떠올리는 경향이 있다.
Fine-tuning은 Prompt 최적화와 RAG 개선을 모두 시도한 뒤 마지막 수단이다.
잘못된 Fine-tuning은 오히려 성능을 고착화시킨다.

### 5.2 Prompt 변경 없는 재배포

모델 버전이 바뀌면 같은 프롬프트의 동작이 달라진다.
모델 버전 업그레이드 전 반드시 Golden Test Set으로 회귀 테스트를 실행한다.

### 5.3 Tool 설명 부실

"이 Tool은 검색에 사용한다"는 설명은 불충분하다.
LLM이 어떤 상황에서 이 Tool을 선택해야 하는지를 명시한다.

```
# 나쁜 예
"search_docs": "문서를 검색한다"

# 좋은 예
"search_docs": "사용자가 사내 정책, 매뉴얼, 절차서에 대해 묻는 경우 사용한다.
일반 상식 질문이나 날짜/시간 조회에는 사용하지 않는다."
```

### 5.4 단기 Fix와 장기 해결책 혼용 주의

단기 Fix(프롬프트에 예외 처리 추가)가 쌓이면 프롬프트가 복잡해진다.
6개월 후 아무도 이유를 모르는 조건문이 쌓인다.
주기적으로 프롬프트를 리팩터링하고 이유를 문서화한다.

---

## 6. 코드 예제

### 6.1 Prompt 버전 관리 시스템

```python
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path

@dataclass
class PromptVersion:
    version: str        # "v1.2.0"
    content: str
    author: str
    created_at: str
    change_reason: str
    test_results: dict  # {"accuracy": 0.85, "faithfulness": 0.82}

class PromptRegistry:
    def __init__(self, registry_path: str = "prompts/registry.json"):
        self.path = Path(registry_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self):
        if self.path.exists():
            with open(self.path) as f:
                self.registry = json.load(f)
        else:
            self.registry = {}

    def save_version(self, prompt_name: str, version: PromptVersion):
        if prompt_name not in self.registry:
            self.registry[prompt_name] = []
        self.registry[prompt_name].append({
            "version": version.version,
            "content": version.content,
            "author": version.author,
            "created_at": version.created_at,
            "change_reason": version.change_reason,
            "test_results": version.test_results
        })
        with open(self.path, "w") as f:
            json.dump(self.registry, f, ensure_ascii=False, indent=2)

    def get_latest(self, prompt_name: str) -> str:
        versions = self.registry.get(prompt_name, [])
        if not versions:
            raise ValueError(f"프롬프트 없음: {prompt_name}")
        return versions[-1]["content"]

    def rollback(self, prompt_name: str, version: str) -> str:
        versions = self.registry.get(prompt_name, [])
        for v in versions:
            if v["version"] == version:
                return v["content"]
        raise ValueError(f"버전 없음: {version}")


# 사용 예시
registry = PromptRegistry()

registry.save_version("qa_agent", PromptVersion(
    version="v1.1.0",
    content="당신은 사내 정책 전문가입니다. 제공된 문서만 참조해 답변하세요.",
    author="kim@company.com",
    created_at=datetime.now().isoformat(),
    change_reason="Faithfulness 점수 0.72 → 0.85 개선을 위해 문서 참조 강조 추가",
    test_results={"accuracy": 0.85, "faithfulness": 0.85}
))

prompt = registry.get_latest("qa_agent")
```

### 6.2 Retrieval Drift 감지기

```python
from typing import Optional
import numpy as np

class RetrievalDriftDetector:
    def __init__(self, retriever_fn, threshold: float = 0.7):
        """
        threshold: Stability Score가 이 이하이면 경보 발생
        """
        self.retriever = retriever_fn
        self.threshold = threshold
        self.baseline: dict[str, list[str]] = {}  # query → doc_ids

    def set_baseline(self, queries: list[str], k: int = 5):
        """기준 시점의 검색 결과를 저장한다."""
        for q in queries:
            results = self.retriever(q, k=k)
            self.baseline[q] = [r.id for r in results]
        print(f"Baseline 설정 완료: {len(queries)}개 쿼리")

    def check_drift(self, k: int = 5) -> dict:
        if not self.baseline:
            raise RuntimeError("baseline을 먼저 설정하라.")

        drift_report = {}
        for query, baseline_ids in self.baseline.items():
            current_results = self.retriever(query, k=k)
            current_ids = [r.id for r in current_results]

            intersection = len(set(baseline_ids) & set(current_ids))
            stability = intersection / k

            drift_report[query] = {
                "stability_score": stability,
                "drifted": stability < self.threshold,
                "baseline_ids": baseline_ids,
                "current_ids": current_ids
            }

        avg_stability = np.mean([
            v["stability_score"] for v in drift_report.values()
        ])
        drifted_count = sum(
            1 for v in drift_report.values() if v["drifted"]
        )

        return {
            "avg_stability": avg_stability,
            "drifted_queries": drifted_count,
            "total_queries": len(self.baseline),
            "alert": avg_stability < self.threshold,
            "details": drift_report
        }
```

### 6.3 Tool 호출 정확도 분석기

```python
from collections import Counter
from enum import Enum

class ToolFailureType(Enum):
    WRONG_TOOL = "wrong_tool_selected"
    WRONG_PARAMS = "wrong_parameters"
    MISSING_VALIDATION = "missing_validation"
    SCHEMA_MISMATCH = "schema_mismatch"
    SUCCESS = "success"

@dataclass
class ToolCallLog:
    timestamp: str
    tool_name: str
    params: dict
    success: bool
    failure_type: Optional[ToolFailureType]
    error_message: Optional[str]

class ToolAccuracyAnalyzer:
    def __init__(self, logs: list[ToolCallLog]):
        self.logs = logs

    def summary(self) -> dict:
        total = len(self.logs)
        success = sum(1 for l in self.logs if l.success)
        failures = [l for l in self.logs if not l.success]

        failure_breakdown = Counter(
            l.failure_type.value for l in failures if l.failure_type
        )

        # Tool별 성공률
        tool_stats = {}
        for log in self.logs:
            if log.tool_name not in tool_stats:
                tool_stats[log.tool_name] = {"total": 0, "success": 0}
            tool_stats[log.tool_name]["total"] += 1
            if log.success:
                tool_stats[log.tool_name]["success"] += 1

        for name, stats in tool_stats.items():
            stats["success_rate"] = stats["success"] / stats["total"]

        return {
            "total_calls": total,
            "success_rate": success / total if total else 0,
            "failure_breakdown": dict(failure_breakdown),
            "tool_stats": tool_stats,
            "top_failures": [
                f for f in sorted(
                    failure_breakdown.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:3]
            ]
        }

    def get_improvement_recommendations(self) -> list[str]:
        summary = self.summary()
        recs = []

        failure_breakdown = summary["failure_breakdown"]
        if failure_breakdown.get("wrong_tool_selected", 0) > 0:
            recs.append("Tool 설명을 개선하라: 어떤 상황에서 사용하는지 구체적으로 명시")
        if failure_breakdown.get("wrong_parameters", 0) > 0:
            recs.append("Few-shot 예시를 Tool 정의에 추가하라")
        if failure_breakdown.get("schema_mismatch", 0) > 0:
            recs.append("외부 API 스키마 변경을 자동 감지하는 테스트를 추가하라")

        return recs
```

---

## Q&A

**Q: Prompt 버전 관리를 코드와 같은 저장소에 넣어야 하는가?**
A: 일반적으로 같은 저장소가 좋다. 코드 변경과 프롬프트 변경을 함께 추적할 수 있다. 단, 프롬프트가 민감한 비즈니스 로직을 포함하면 별도 저장소에 접근 제어를 추가한다.

**Q: Retrieval Drift는 얼마나 자주 점검해야 하는가?**
A: 문서 업데이트가 빈번하면 매일, 안정적이면 주 1회가 적당하다. 임베딩 모델이나 인덱스 변경 직후에는 반드시 전수 점검한다.

**Q: Fine-tuning 없이 Tool 호출 정확도를 올릴 수 있는가?**
A: 대부분 가능하다. Tool 설명 개선과 Few-shot 예시 추가만으로 10~20%p 향상되는 사례가 많다. 그 이후에도 부족하면 Fine-tuning을 검토한다.

---

## 퀴즈

**Q1. [단답형] Retrieval Drift란 무엇인가?**

<details>
<summary>힌트</summary>
문서 업데이트와 검색 결과의 관계를 생각하라.
</details>

<details>
<summary>정답</summary>
문서 추가·수정·삭제 또는 인덱스 변경으로 인해 동일한 쿼리에 대한 검색 결과가 시간에 따라 달라지는 현상이다.
</details>

---

**Q2. [객관식] Prompt 성능이 저하됐을 때 가장 먼저 시도해야 할 것은?**

A) 즉시 Fine-tuning 수행
B) 임베딩 모델 교체
C) 프롬프트 수정 후 A/B 테스트
D) 더 큰 모델로 교체

<details>
<summary>힌트</summary>
비용과 리스크 대비 효과를 생각하라.
</details>

<details>
<summary>정답</summary>
C. Prompt 수정은 비용과 리스크가 낮고 효과가 빠르다. Fine-tuning과 모델 교체는 마지막 수단이다.
</details>

---

**Q3. [OX] 모델 버전이 바뀌어도 같은 프롬프트는 동일하게 동작한다.**

<details>
<summary>힌트</summary>
LLM 모델 버전 업데이트의 영향을 생각하라.
</details>

<details>
<summary>정답</summary>
X. 모델 버전이 바뀌면 같은 프롬프트에서 다른 동작이 나올 수 있다. 모델 업그레이드 전 회귀 테스트가 필수다.
</details>

---

**Q4. [단답형] Tool 호출 실패 유형 4가지를 나열하라.**

<details>
<summary>힌트</summary>
어떤 Tool을 고를지, 파라미터가 맞는지, 검증이 있는지, 스키마가 최신인지를 생각하라.
</details>

<details>
<summary>정답</summary>
① Wrong Tool Selected (잘못된 Tool 선택), ② Wrong Parameters (잘못된 파라미터), ③ Missing Validation (파라미터 검증 누락), ④ Schema Mismatch (API 스키마 변경 미반영).
</details>

---

**Q5. [서술형] A/B 테스트 없이 Prompt를 교체할 때의 위험성을 설명하라.**

<details>
<summary>힌트</summary>
일부 사용자 그룹에서 성능이 달라질 때 어떻게 감지할 수 있는가?
</details>

<details>
<summary>정답</summary>
A/B 테스트 없이 전체 트래픽을 신버전으로 전환하면, 성능이 저하돼도 이전 버전과 비교할 대조군이 없다. 어떤 변경이 문제인지 특정하기 어렵고, 저하 시 롤백 시점도 늦어진다. A/B 테스트는 위험을 분산하고 데이터 기반 의사결정을 가능하게 한다.
</details>

---

## 실습 명세

### I DO — 강사 시연 (30분)

**목표**: 실제 Prompt 버전 관리 시스템을 구현하고, Retrieval Drift 감지기를 실행한다.

**순서**:
1. `PromptRegistry` 구현 및 v1.0.0 → v1.1.0 저장
2. 두 버전의 Golden Test 점수 비교
3. Mock retriever로 `RetrievalDriftDetector` 실행
4. 드리프트 발생 시뮬레이션 및 경보 확인

### WE DO — 함께 실습 (40분)

**목표**: Tool 호출 로그를 분석해 성능 개선 우선순위를 도출한다.

**단계**:
1. 샘플 Tool 호출 로그 20건 로드
2. `ToolAccuracyAnalyzer.summary()` 실행
3. 실패 유형별 원인 분석 및 토론
4. `get_improvement_recommendations()` 결과 검토
5. 팀별 개선 계획 발표 (3분/팀)

### YOU DO — 독립 과제 (50분)

**목표**: 실무 Agent의 성능 저하 시나리오에서 진단 → 개선 계획을 수립한다.

**시나리오**: RAG 기반 고객 지원 Agent의 Faithfulness가 0.85 → 0.62로 떨어졌다. 3주 전 문서 2,000건이 추가됐고, 지난주 임베딩 모델이 업그레이드됐다.

**요구사항**:
- 진단 4단계 적용 (증상→계층 격리→시점 특정→재현)
- 원인 가설 2개 이상 제시 및 검증 방법
- Prompt/RAG/Tool 각 관점의 개선 계획
- A/B 테스트 설계서 (트래픽 분배, 기간, 합격 기준)

**산출물**: `performance-improvement-plan.md`
