**lf_config# Day 4 Session 4 — 확장 가능한 서비스 아키텍처

> **세션 목표**: Dev–Staging–Prod 환경 분리, 수평/수직 Scaling 전략, Multi-Agent 구조 설계, 운영 비용 최적화를 실무에 적용한다.

---

## 1. 왜 중요한가

### 아키텍처 없이 성장하면 무슨 일이 생기나

초기에는 단일 서버에서 Agent가 잘 동작한다.
사용자가 늘어나면 응답이 느려지고 오류가 증가한다.
긴급 패치가 운영 서버에 바로 배포되며 장애가 난다.

**기술 부채가 쌓이면 리팩터링 비용이 기능 개발 비용을 초과한다.**

실제 사례: 스타트업이 RAG Agent를 빠르게 출시했다.
3개월 뒤 B2B 고객사 20곳이 붙었다.
Dev/Prod 분리가 없어서 개발 중 실험이 운영 데이터에 영향을 줬다.
환경 분리에 6주가 걸렸고 그 기간 동안 기능 개발이 멈췄다.

---

## 2. 핵심 원리

### 2.1 Dev–Staging–Prod 환경 분리

**세 환경의 역할**:

| 환경 | 목적 | 데이터 | 모델 | 접근 |
|---|---|---|---|---|
| Dev | 개발·실험 | 합성/샘플 | 저비용 (gpt-4o-mini) | 개발팀 |
| Staging | 검증·QA | 운영 익명화 복사본 | 운영과 동일 | 개발+QA팀 |
| Prod | 실제 서비스 | 실제 운영 데이터 | 운영 모델 | 읽기만 허용 |

**환경별 설정 분리 원칙**:
- 환경 변수로 모델명, API 키, 인덱스 엔드포인트를 분리한다.
- 코드에 환경명을 하드코딩하지 않는다.
- `config/dev.yaml`, `config/staging.yaml`, `config/prod.yaml`로 관리한다.

```yaml
# config/prod.yaml
llm:
  model: "gpt-4o"
  temperature: 0.0
  max_tokens: 2048

vector_store:
  endpoint: "https://prod-vector.internal"
  index: "prod-docs-v3"

guardrail:
  enabled: true
  pii_masking: true

logging:
  level: "INFO"
  sample_rate: 0.1  # 정상 트래픽 10% 샘플링
```

### 2.2 Scaling 전략

**수직 Scaling(Scale Up)**:
- 서버 사양(CPU/메모리)을 올린다.
- 한계가 명확하고 비용이 급격히 증가한다.
- 단기 임시방편으로만 사용한다.

**수평 Scaling(Scale Out)**:
- 동일 서비스 인스턴스를 여러 개 실행한다.
- Agent 서버는 Stateless하게 설계해야 Scaling이 가능하다.
- 세션 상태는 서버가 아닌 Redis/DB에 저장한다.

**Agent Stateless 설계 원칙**:
```
❌ 상태를 서버 메모리에 저장
   → Scale Out 시 요청이 다른 서버에 가면 상태 유실

✅ 상태를 외부 저장소에 저장
   → 모든 서버가 동일 Redis/DB에서 상태를 읽음
   → 어느 서버도 요청을 처리할 수 있음
```

**Auto-scaling 트리거 기준**:
```
CPU 사용률 > 70% → 인스턴스 추가
요청 큐 길이 > 100 → 인스턴스 추가
CPU 사용률 < 20% (10분) → 인스턴스 축소
```

### 2.3 Multi-Agent 구조

**단일 Agent의 한계**:
- 너무 많은 책임이 하나의 Agent에 집중된다.
- 컨텍스트 윈도우가 빠르게 차오른다.
- 한 부분의 실패가 전체를 멈춘다.

**Multi-Agent 패턴**:

```
패턴 1: Orchestrator-Worker
  Orchestrator가 작업을 분해해 Worker에게 위임
  Worker는 전문화된 단일 책임
  → 복잡한 장문 Task에 적합

패턴 2: Pipeline (순차 처리)
  Intake → Classify → Retrieve → Generate → Validate
  각 단계가 독립 Agent
  → 명확한 처리 흐름이 있는 Task에 적합

패턴 3: Parallel Fan-out
  동일 입력을 여러 Agent가 병렬 처리
  결과를 합산해 최종 응답
  → 다각도 분석, 교차 검증에 적합
```

**Multi-Agent 설계 시 결정 기준**:
| 조건 | 단일 Agent | Multi-Agent |
|---|---|---|
| Task 복잡도 | 단순 (~3 스텝) | 복잡 (5+ 스텝) |
| 컨텍스트 길이 | 짧음 | 길거나 누적됨 |
| 도메인 전문성 | 범용 | 여러 전문 영역 |
| 오류 격리 필요 | 낮음 | 높음 |

### 2.4 운영 비용 최적화

**LLM 비용 구조**:
```
총 비용 = 입력 토큰 × 입력 단가
        + 출력 토큰 × 출력 단가
        + Tool 호출 횟수 × 호출 비용
```

**비용 최적화 전략 (효과 큰 순)**:

1. **모델 계층화**: 모든 호출에 같은 모델을 쓰지 않는다.
   ```
   단순 분류/필터 → gpt-4o-mini (저비용)
   RAG 응답 생성 → gpt-4o (중간)
   복잡한 추론   → o3 (고비용, 최소화)
   ```

2. **캐싱**: 동일·유사 쿼리는 캐시에서 반환한다.
   - Exact Cache: 동일 입력 → 저장된 응답 반환.
   - Semantic Cache: 유사 쿼리 → 임베딩 유사도로 캐시 히트.

3. **컨텍스트 압축**: 긴 히스토리를 요약해 토큰을 절감한다.

4. **배치 처리**: 실시간이 아닌 요청은 배치로 묶어 처리한다.

---

## 3. 실무 의미

### 3.1 배포 파이프라인 설계

```
코드 커밋
  ↓
CI (단위 테스트 + Golden Test Set)
  ↓
Dev 배포 (자동)
  ↓
Staging 배포 (자동) + 통합 테스트
  ↓
Prod 배포 (수동 승인 또는 자동)
  ↓
카나리 배포 (트래픽 5% → 50% → 100%)
```

**카나리 배포**:
- 전체 트래픽의 5%에 신버전을 배포한다.
- 오류율·응답 시간을 1시간 관찰한다.
- 정상이면 50%, 이후 100%로 확대한다.
- 이상 감지 시 즉시 이전 버전으로 롤백한다.

### 3.2 비용 예측 및 예산 관리

**월간 비용 추정 공식**:
```
일일 요청 수 × 평균 입력 토큰 × 입력 단가
+ 일일 요청 수 × 평균 출력 토큰 × 출력 단가
× 30일
```

**예산 초과 방지**:
- Hard Limit: 일일 예산 초과 시 서비스 일시 중단.
- Soft Limit: 예산 80% 도달 시 알림 발송.
- 모델 계층화로 예산 내에서 최대 품질 유지.

---

## 4. 비교: Scaling 아키텍처 패턴

| 패턴 | 비용 | 복잡도 | 적합한 규모 |
|---|---|---|---|
| 단일 서버 | 낮음 | 낮음 | 프로토타입, < 100 RPS |
| 수평 Scaling | 중간 | 중간 | 100~10,000 RPS |
| 마이크로서비스 | 높음 | 높음 | > 10,000 RPS |
| 서버리스 (Lambda) | 가변 | 중간 | 간헐적 대용량 |

**Agent 서비스는 수평 Scaling을 기본으로 설계하라.**
LLM API 자체가 외부 서비스이므로 서버는 경량 Proxy 역할이다.

---

## 5. 주의사항

### 5.1 Prod 데이터를 Dev에서 사용하는 문제

개발 편의를 위해 실제 사용자 데이터를 Dev 환경에서 쓰는 경우가 많다.
GDPR·개인정보보호법 위반이다.
Dev/Staging에는 반드시 익명화·합성 데이터를 사용한다.

### 5.2 Multi-Agent 오버엔지니어링

처음부터 5개 Agent로 설계하면 디버깅이 매우 어려워진다.
단일 Agent로 시작해 병목이 생기면 분리한다.
"지금 당장 필요한가?"를 항상 물어라.

### 5.3 캐시 무효화 전략 부재

문서가 업데이트됐는데 캐시가 구버전 응답을 반환한다.
캐시 TTL을 적절히 설정하고, 문서 업데이트 시 관련 캐시를 즉시 무효화한다.

### 5.4 비용 모니터링 부재

LLM API 비용은 트래픽에 따라 급격히 오를 수 있다.
일별·주별 비용 대시보드를 의무화한다.
이상 비용 급증 시 즉시 알림을 받도록 설정한다.

---

## 6. 코드 예제

### 6.1 환경 설정 관리자

```python
import os
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class LLMConfig:
    model: str
    temperature: float
    max_tokens: int

@dataclass
class VectorStoreConfig:
    endpoint: str
    index: str

@dataclass
class AppConfig:
    env: str
    llm: LLMConfig
    vector_store: VectorStoreConfig
    log_level: str
    log_sample_rate: float
    guardrail_enabled: bool

def load_config(env: str = None) -> AppConfig:
    env = env or os.getenv("APP_ENV", "dev")
    config_path = Path(f"config/{env}.yaml")

    if not config_path.exists():
        raise FileNotFoundError(f"설정 파일 없음: {config_path}")

    with open(config_path) as f:
        raw = yaml.safe_load(f)

    return AppConfig(
        env=env,
        llm=LLMConfig(**raw["llm"]),
        vector_store=VectorStoreConfig(**raw["vector_store"]),
        log_level=raw["logging"]["level"],
        log_sample_rate=raw["logging"]["sample_rate"],
        guardrail_enabled=raw["guardrail"]["enabled"]
    )

# 사용
config = load_config()
print(f"환경: {config.env}, 모델: {config.llm.model}")
```

### 6.2 Semantic Cache

```python
import hashlib
import json
import time
from typing import Optional
import numpy as np

class SemanticCache:
    def __init__(self, embedding_fn, redis_client, similarity_threshold=0.92,
                 ttl_seconds=3600):
        self.embed = embedding_fn
        self.redis = redis_client
        self.threshold = similarity_threshold
        self.ttl = ttl_seconds

    def _cache_key(self, text: str) -> str:
        return f"cache:query:{hashlib.sha256(text.encode()).hexdigest()[:16]}"

    def get(self, query: str) -> Optional[str]:
        query_vec = self.embed(query)

        # 최근 캐시 항목들과 유사도 비교
        cache_keys = self.redis.keys("cache:query:*")
        for key in cache_keys[:100]:  # 최대 100개만 비교
            cached = json.loads(self.redis.get(key))
            cached_vec = np.array(cached["embedding"])
            similarity = np.dot(query_vec, cached_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(cached_vec)
            )
            if similarity >= self.threshold:
                return cached["response"]
        return None

    def set(self, query: str, response: str):
        key = self._cache_key(query)
        embedding = self.embed(query)
        value = json.dumps({
            "query": query,
            "response": response,
            "embedding": embedding.tolist(),
            "cached_at": time.time()
        })
        self.redis.setex(key, self.ttl, value)


# 사용 예시
cache = SemanticCache(
    embedding_fn=get_embedding,
    redis_client=redis_client,
    similarity_threshold=0.92,
    ttl_seconds=3600
)

def cached_agent(query: str) -> str:
    # 캐시 확인
    cached = cache.get(query)
    if cached:
        return cached  # 캐시 히트

    # Agent 실행
    response = run_agent(query)
    cache.set(query, response)
    return response
```

### 6.3 모델 계층화 라우터

```python
from enum import Enum
from typing import Callable

class TaskComplexity(Enum):
    SIMPLE = "simple"      # 분류, 필터, 단답
    MEDIUM = "medium"      # RAG 응답 생성
    COMPLEX = "complex"    # 다단계 추론, 코드 생성

@dataclass
class ModelRoute:
    model: str
    max_tokens: int
    estimated_cost_per_1k: float  # USD

MODEL_ROUTES = {
    TaskComplexity.SIMPLE: ModelRoute(
        model="gpt-4o-mini",
        max_tokens=512,
        estimated_cost_per_1k=0.00015
    ),
    TaskComplexity.MEDIUM: ModelRoute(
        model="gpt-4o",
        max_tokens=2048,
        estimated_cost_per_1k=0.005
    ),
    TaskComplexity.COMPLEX: ModelRoute(
        model="o3",
        max_tokens=4096,
        estimated_cost_per_1k=0.06
    )
}

def classify_complexity(query: str, context_length: int) -> TaskComplexity:
    """쿼리와 컨텍스트 길이로 복잡도를 판단한다."""
    if context_length > 10_000:
        return TaskComplexity.COMPLEX
    # 간단한 규칙 기반 분류
    simple_patterns = ["무엇인가", "언제", "몇 개", "있나요"]
    if any(p in query for p in simple_patterns) and len(query) < 50:
        return TaskComplexity.SIMPLE
    if len(query) > 200 or "분석" in query or "설계" in query:
        return TaskComplexity.COMPLEX
    return TaskComplexity.MEDIUM

class ModelRouter:
    def __init__(self, llm_client, cost_tracker=None):
        self.client = llm_client
        self.cost_tracker = cost_tracker

    def call(self, query: str, context: str, system_prompt: str) -> str:
        complexity = classify_complexity(query, len(context))
        route = MODEL_ROUTES[complexity]

        response = self.client.chat.completions.create(
            model=route.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"컨텍스트:\n{context}\n\n질문: {query}"}
            ],
            max_tokens=route.max_tokens,
            temperature=0.0
        )

        if self.cost_tracker:
            tokens_used = response.usage.total_tokens
            estimated_cost = tokens_used / 1000 * route.estimated_cost_per_1k
            self.cost_tracker.record(route.model, tokens_used, estimated_cost)

        return response.choices[0].message.content
```

### 6.4 Multi-Agent Orchestrator (간단 구현)

```python
from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed

class AgentTask:
    def __init__(self, name: str, fn: Callable, input: Any):
        self.name = name
        self.fn = fn
        self.input = input

class MultiAgentOrchestrator:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def run_sequential(self, tasks: list[AgentTask]) -> list[Any]:
        """순차 Pipeline 패턴"""
        result = None
        results = []
        for task in tasks:
            input_data = result if result is not None else task.input
            result = task.fn(input_data)
            results.append({"name": task.name, "output": result})
        return results

    def run_parallel(self, tasks: list[AgentTask]) -> dict[str, Any]:
        """병렬 Fan-out 패턴"""
        results = {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(task.fn, task.input): task.name
                for task in tasks
            }
            for future in as_completed(futures):
                name = futures[future]
                try:
                    results[name] = future.result()
                except Exception as e:
                    results[name] = {"error": str(e)}
        return results


# 사용 예시: 병렬 분석
orchestrator = MultiAgentOrchestrator(max_workers=3)

results = orchestrator.run_parallel([
    AgentTask("보안_검토", security_agent, user_requirement),
    AgentTask("성능_분석", performance_agent, user_requirement),
    AgentTask("비용_추정", cost_agent, user_requirement),
])

# 결과 통합
final_report = synthesize_agent(results)
```

---

## Q&A

**Q: Staging 환경 데이터는 어떻게 만드는가?**
A: 운영 데이터를 익명화(PII 제거 또는 합성 대체)해서 복사한다. 또는 데이터 생성 스크립트로 현실적인 합성 데이터를 만든다. 핵심은 운영 데이터 구조와 분포를 최대한 따르되 실제 사용자 정보는 포함하지 않는 것이다.

**Q: 카나리 배포에서 몇 %부터 시작해야 하는가?**
A: 일반적으로 1~5%로 시작한다. 리스크가 높은 변경이면 1%, 신뢰도 높은 변경이면 10%도 가능하다. 중요한 것은 비율보다 관찰 시간(최소 30분~1시간)이다.

**Q: Multi-Agent 구조는 얼마나 복잡해질 수 있는가?**
A: 실무에서는 3~5개 Agent로 구성하는 것이 일반적이다. 10개 이상이 되면 디버깅과 모니터링이 매우 어려워진다. 필요한 만큼만 분리한다는 원칙을 유지한다.

**Q: Semantic Cache의 유사도 임계값은 어떻게 정하는가?**
A: 0.90~0.95가 일반적이다. 낮으면 관련 없는 쿼리가 캐시 히트돼 오답을 반환한다. 높으면 캐시 효율이 떨어진다. 도메인별 샘플 쿼리로 실험해 조정한다.

---

## 퀴즈

**Q1. [단답형] Agent 서비스가 수평 Scaling을 위해 반드시 지켜야 하는 설계 원칙은?**

<details>
<summary>힌트</summary>
세션 상태를 어디에 저장해야 하는가?
</details>

<details>
<summary>정답</summary>
Stateless 설계. 세션 상태와 컨텍스트를 서버 메모리가 아닌 외부 저장소(Redis, DB)에 저장해, 어느 서버 인스턴스도 요청을 처리할 수 있게 한다.
</details>

---

**Q2. [객관식] 모델 계층화 전략에서 "단순 분류 Task"에 가장 적합한 모델은?**

A) o3 (최고 성능)
B) gpt-4o (운영 표준)
C) gpt-4o-mini (저비용)
D) 임베딩 모델

<details>
<summary>힌트</summary>
비용 대비 충분한 성능을 내는 모델을 선택한다.
</details>

<details>
<summary>정답</summary>
C. 단순 분류·필터·단답 Task에는 gpt-4o-mini로 충분하며 비용이 gpt-4o 대비 수십 배 저렴하다.
</details>

---

**Q3. [OX] Staging 환경에 실제 운영 사용자 데이터를 그대로 복사해도 된다.**

<details>
<summary>힌트</summary>
개인정보보호법과 데이터 격리 원칙을 생각하라.
</details>

<details>
<summary>정답</summary>
X. Staging에는 익명화·합성된 데이터만 사용해야 한다. 실제 PII가 포함된 운영 데이터를 개발 환경에 복사하면 개인정보보호법 위반이다.
</details>

---

**Q4. [단답형] Semantic Cache가 Exact Cache보다 유용한 이유를 설명하라.**

<details>
<summary>힌트</summary>
사용자가 완전히 동일한 문장을 입력하는 경우가 얼마나 많은가?
</details>

<details>
<summary>정답</summary>
사용자는 같은 의미의 질문을 다른 표현으로 입력한다. Exact Cache는 글자가 완전히 일치해야 히트하지만, Semantic Cache는 임베딩 유사도로 의미가 같은 쿼리를 같은 캐시 항목으로 처리해 캐시 히트율이 훨씬 높다.
</details>

---

**Q5. [서술형] 처음부터 Multi-Agent 구조로 설계하는 것의 위험성을 설명하고, 올바른 접근 방식을 제시하라.**

<details>
<summary>힌트</summary>
디버깅 복잡도, 오버엔지니어링, 점진적 확장을 생각하라.
</details>

<details>
<summary>정답</summary>
처음부터 Multi-Agent 구조를 선택하면, 어느 Agent에서 오류가 발생했는지 추적하기 어렵고, Agent 간 통신 오버헤드가 발생하며, 아직 필요하지 않은 복잡성을 도입하는 오버엔지니어링이 된다. 올바른 접근은 단일 Agent로 시작해 실제 병목(컨텍스트 초과, 성능 저하, 유지보수 어려움)이 발생할 때 해당 부분만 분리하는 것이다. "지금 당장 필요한가?"를 항상 먼저 묻는다.
</details>

---

## 실습 명세

### I DO — 강사 시연 (30분)

**목표**: 환경별 설정 관리 + 모델 라우터를 실제로 구현하고 실행한다.

**순서**:
1. `config/dev.yaml`, `config/prod.yaml` 작성
2. `load_config()` 구현 및 환경 전환 시연
3. `ModelRouter` 구현 및 3개 복잡도별 호출 비용 비교
4. Semantic Cache 캐시 히트율 실험

### WE DO — 함께 실습 (40분)

**목표**: 팀별 운영 아키텍처 다이어그램을 설계하고 발표한다.

**단계**:
1. 팀별 시나리오 선정 (B2B SaaS / 내부 도구 / 소비자 앱)
2. Dev/Staging/Prod 환경 분리 설계
3. Scaling 전략 결정 (수평/수직/서버리스)
4. Multi-Agent 구조 필요 여부 판단
5. 비용 최적화 3가지 방안 도출
6. 팀별 발표 (5분/팀)

### YOU DO — 독립 과제 (50분)

**목표**: 실무 Agent 서비스의 전체 운영 아키텍처 설계서를 작성한다.

**시나리오**: 일평균 50,000 요청을 처리하는 B2B 고객 지원 Agent 서비스를 설계한다. 월 LLM 비용 목표는 $5,000 이하다.

**요구사항**:
- Dev/Staging/Prod 환경 분리 설계 (설정 파일 포함)
- Scaling 전략 및 Auto-scaling 트리거 기준
- 모델 계층화 계획 (Task 유형별 모델 지정)
- 월간 비용 추정 계산서
- 카나리 배포 계획 (단계별 트래픽 비율 + 판단 기준)
- Multi-Agent 여부 결정 및 근거

**산출물**: `ops-architecture-design.md` + `config/prod.yaml` (예시)
