# 외부 API · 데이터 연동 최적화

## 학습 목표
1. REST API 연동 시 Latency를 최소화하는 비동기 처리 패턴을 설계하고 구현할 수 있다
2. Schema Validation과 Guardrail을 적용하여 LLM의 API 호출 안전성을 보장할 수 있다
3. 인증, 보안, Rate Limit 전략을 설계하여 운영 환경에서 안정적인 API 연동을 구축할 수 있다

---

## 개념 1: REST API 연동 및 Latency 최소화

### 개념 설명

**왜 이것이 중요한가**: AI Agent가 실질적으로 유용하려면 외부 세계와 연결되어야 한다. 날씨 정보를 조회하고, 데이터베이스에서 상품을 검색하고, 결제 시스템에 주문을 전달하는 것 모두 외부 API 호출을 통해 이루어진다. 그런데 Agent의 응답 파이프라인에서 외부 API 호출은 가장 큰 병목 지점이 된다. LLM 추론 자체가 1~3초 소요되고, 여기에 외부 API 호출(0.5~2초), 후처리까지 더해지면 사용자 체감 응답 시간이 쉽게 5초를 넘긴다. 대화형 서비스에서 5초 이상의 응답 대기는 사용자 이탈의 주요 원인이므로, API 연동의 Latency를 최소화하는 것은 Agent의 실용성을 결정하는 핵심 엔지니어링 과제다.

**핵심 원리**: Latency 최소화 전략은 네트워크 통신의 비용 구조를 이해하면 자연스럽게 도출된다. HTTP 요청 하나를 보내려면 TCP 3-way 핸드셰이크(~50ms), TLS 핸드셰이크(~100ms), 요청 전송 및 응답 수신 과정을 거쳐야 한다. 매 요청마다 이 과정을 반복하면 핸드셰이크 비용만으로 수백 밀리초가 낭비된다. 세 가지 핵심 전략이 있다:

- **Connection Pooling**: 한번 맺은 TCP/TLS 연결을 재사용하여 핸드셰이크 비용을 제거하는 기법이다. 동일 서버에 반복 호출이 잦은 Agent 패턴에서 특히 효과적이다. `httpx.Client`는 내부적으로 connection pool을 관리하므로, 동일 Client 인스턴스를 재사용하면 자동으로 연결이 재사용된다.
- **병렬 API 호출**: Agent가 "서울 날씨"와 "서울 맛집"을 동시에 조회해야 할 때, 순차적으로 보내면 두 API의 응답 시간을 합산해야 하지만, 병렬로 보내면 가장 느린 API의 응답 시간만 기다리면 된다. Python의 `asyncio`와 `httpx.AsyncClient`를 사용하면 이 패턴을 쉽게 구현할 수 있다. 3개의 독립 API를 순차로 호출하면 약 1.8초, 병렬로 호출하면 약 0.6초로 약 3배의 성능 개선이 가능하다.
- **응답 캐싱**: Agent 대화에서 동일한 정보를 여러 번 참조하는 패턴이 빈번하다. 예를 들어 사용자가 "이 상품 가격 얼마야?" -> "색상은?" -> "재고 있어?"를 연속으로 물으면, 상품 기본 정보를 매번 API로 조회할 필요 없이 첫 응답을 캐시하여 재사용할 수 있다. TTL(Time-To-Live) 캐시를 적용하면 일정 시간 내의 동일 요청에 대해 API 호출 없이 즉시 응답을 반환하며, 캐시 만료 후에는 자동으로 최신 데이터를 갱신한다.

**실무에서의 의미**: 실무에서는 이 세 가지 전략을 개별적으로 사용하기보다 **조합**하여 사용한다. Connection Pool을 유지하면서, 캐시 미스가 발생한 요청들만 병렬로 API를 호출하고, 결과를 캐시에 저장하는 구조가 표준적인 고성능 Agent API 클라이언트 패턴이다. 특히 대화형 Agent에서는 사용자가 같은 주제에 대해 연속 질문을 하는 패턴이 매우 흔하므로, 캐시 히트율이 40~60%에 달하는 경우가 많다. 이는 곧 API 호출 비용의 40~60%를 절약할 수 있다는 의미이기도 하다.

**다른 접근법과의 비교**: Latency 최소화의 다른 접근으로 API 결과를 사전에 모두 가져와 로컬에 저장하는 "Pre-fetching" 방식이 있다. 이 방식은 응답이 즉각적이라는 장점이 있지만, 데이터가 실시간이 아니라는 치명적 단점이 있다. 재고, 가격, 배송 상태처럼 자주 변하는 데이터에는 적합하지 않다. 반면 TTL 캐시는 설정한 시간(보통 30초~5분) 내에서만 캐시를 사용하므로 실시간성과 성능의 균형을 맞출 수 있다. 또 다른 접근으로 GraphQL을 사용하여 필요한 데이터만 정확히 요청하는 방법도 있다. REST API는 불필요한 필드까지 모두 반환하는 over-fetching 문제가 있지만, GraphQL은 필요한 필드만 지정하므로 응답 크기가 줄어들고 네트워크 전송 시간이 단축된다.

이를 코드로 표현하면 다음과 같다:

```python
import httpx
import asyncio
import time

# Connection Pooling - 동기 방식
with httpx.Client(
    base_url="https://api.example.com",
    timeout=httpx.Timeout(10.0, connect=5.0),
    limits=httpx.Limits(max_connections=20, max_keepalive_connections=10)
) as client:
    response1 = client.get("/products/1")
    response2 = client.get("/products/2")  # 기존 연결 재사용


# 병렬 API 호출 - 비동기 방식
async def fetch_parallel():
    async with httpx.AsyncClient(
        base_url="https://api.example.com", timeout=10.0
    ) as client:
        start = time.time()
        results = await asyncio.gather(
            client.get("/products/1"),
            client.get("/products/2"),
            client.get("/products/3"),
        )
        elapsed = time.time() - start
        print(f"병렬 호출 소요 시간: {elapsed:.2f}초")
        return results
```

**실행 결과**:
```
순차 호출 소요 시간: 1.85초
병렬 호출 소요 시간: 0.67초
```

병렬 호출은 순차 호출 대비 약 3배 빠르다. 독립적인 API 호출이 많을수록 효과가 크다.

### 예제

다음 예제는 Connection Pooling, 병렬 호출, TTL 캐시를 하나의 클래스에 통합한 실전 패턴이다. `CachedAPIClient`는 캐시 히트율을 추적하여 캐시 효과를 모니터링할 수 있도록 설계되었다.

```python
import httpx
import asyncio
import json
from cachetools import TTLCache


class CachedAPIClient:
    def __init__(self, base_url: str, cache_ttl: int = 300):
        self.cache = TTLCache(maxsize=1000, ttl=cache_ttl)
        self.client = httpx.AsyncClient(
            base_url=base_url, timeout=10.0,
            limits=httpx.Limits(max_connections=20)
        )
        self.stats = {"hits": 0, "misses": 0}

    async def get(self, path: str, params: dict | None = None) -> dict:
        cache_key = f"{path}:{json.dumps(params, sort_keys=True)}"
        if cache_key in self.cache:
            self.stats["hits"] += 1
            return self.cache[cache_key]

        self.stats["misses"] += 1
        response = await self.client.get(path, params=params)
        response.raise_for_status()
        data = response.json()
        self.cache[cache_key] = data
        return data

    async def get_many(self, requests: list[tuple[str, dict | None]]) -> list[dict]:
        """병렬 + 캐시 결합 API 호출"""
        return await asyncio.gather(
            *[self.get(path, params) for path, params in requests]
        )

    def get_stats(self) -> dict:
        total = self.stats["hits"] + self.stats["misses"]
        hit_rate = self.stats["hits"] / total if total > 0 else 0
        return {**self.stats, "total": total, "hit_rate": f"{hit_rate:.1%}"}

    async def close(self):
        await self.client.aclose()
```

**실행 결과**:
```
첫 호출: {'hits': 0, 'misses': 1, 'total': 1, 'hit_rate': '0.0%'}
두 번째 호출: {'hits': 1, 'misses': 1, 'total': 2, 'hit_rate': '50.0%'}
병렬 호출 후: {'hits': 2, 'misses': 3, 'total': 5, 'hit_rate': '40.0%'}
```

### Q&A
**Q: Agent에서 asyncio를 사용하면 LangGraph와 호환되나요?**
A: LangGraph는 내부적으로 asyncio 기반이므로 완벽히 호환된다. `async def` 노드를 정의하고 내부에서 `httpx.AsyncClient`를 사용하면 된다. 다만 `asyncio.run()`은 이미 이벤트 루프가 실행 중이면 에러가 발생하므로, LangGraph 노드 내부에서는 `await`를 직접 사용한다.

<details>
<summary>퀴즈: Connection Pooling과 캐싱을 동시에 적용했을 때, 어떤 상황에서 효과가 가장 클까요?</summary>

**힌트**: Agent가 동일한 API를 반복 호출하는 시나리오를 생각해보세요.

**정답**: 사용자 대화 중 동일한 정보를 여러 번 참조하는 경우에 가장 효과적이다. 예를 들어 고객이 "이 상품 가격 얼마야?" -> "색상은?" -> "재고 있어?" 연속 질문을 하면, 상품 정보를 매번 API로 조회하지 않고 캐시에서 즉시 반환할 수 있다. Connection Pooling은 캐시 미스 시 새 API 호출의 latency를 줄이므로, 두 전략은 보완적이다.
</details>

---

## 개념 2: 비동기 vs 동기 처리 설계

### 개념 설명

**왜 이것이 중요한가**: Agent의 외부 API 연동에서 동기(synchronous)와 비동기(asynchronous) 중 어떤 방식을 선택할 것인가는 아키텍처 전체에 영향을 미치는 핵심 설계 결정이다. 잘못된 선택은 불필요한 복잡도를 초래하거나, 반대로 심각한 성능 병목을 만든다. 이 선택을 올바르게 하려면, 먼저 두 방식의 근본적인 차이를 이해해야 한다.

동기 처리에서는 API 호출을 보내면 응답이 돌아올 때까지 프로그램의 실행이 멈춘다(blocking). 코드가 직관적이고 디버깅이 쉽다는 장점이 있지만, API 응답을 기다리는 동안 CPU는 아무 일도 하지 않고 유휴 상태가 된다. 비동기 처리에서는 API 호출을 보낸 뒤 응답을 기다리지 않고 다른 작업을 먼저 수행한다(non-blocking). CPU 효율이 높고 여러 API를 동시에 호출할 수 있지만, 코드 구조가 복잡해지고 에러 추적이 어려워진다.

**핵심 원리**: Agent 시나리오에서 이 선택은 **API 호출 간 의존성**에 의해 결정된다. 이를 비유하면, 식당에서 주문하는 상황과 같다. "메뉴판을 받아야 주문할 수 있고, 주문해야 음식이 나온다"는 순차 의존적이다. 반면 "음료와 디저트는 메인 요리와 별도로 준비된다"는 독립적이다. API 호출도 마찬가지다:

- **순차 의존적 호출**: "주문 정보 조회 -> 배송 추적 -> 예상 도착일 계산"처럼 각 단계가 이전 단계의 결과에 의존하는 경우, 비동기로 작성해도 실질적 성능 이점이 없다. 어차피 순차적으로 실행해야 하기 때문이다. 이 경우 동기 코드가 더 명확하고 유지보수하기 쉽다.
- **독립적 호출**: "상품 정보 + 리뷰 + 가격 이력"처럼 서로 독립적인 API 호출은 비동기 병렬로 실행하면 총 소요 시간이 가장 느린 API 하나의 응답 시간으로 줄어든다.
- **혼합 패턴(Semi-parallel)**: 현실의 Agent 워크플로우에서 가장 흔한 패턴이다. "주문 조회(선행) -> (배송 추적 + 환불 정책 조회)(병렬)" 같은 구조다. 첫 번째 API는 동기적으로 실행하고, 그 결과에 의존하되 서로 독립적인 후속 API들은 비동기 병렬로 실행하는 것이 최적이다.

**실무에서의 의미**: 실무에서 자주 하는 실수는 "모든 것을 비동기로 만들면 빠르겠지"라고 생각하는 것이다. 비동기 코드는 동기 코드보다 에러 스택 트레이스가 복잡하고, race condition이 발생할 수 있으며, 테스트 작성이 까다롭다. 따라서 원칙은 "성능이 필요한 곳에만 비동기를 사용하고, 나머지는 동기로 유지하라"이다. 구체적인 기준으로는 독립적 API 호출이 3개 이상일 때, 빠른 응답 시간이 UX에 직결될 때 비동기를 선택한다. 독립 API가 1~2개뿐이라면 동기 코드의 단순함이 비동기의 성능 이점을 상회한다.

**다른 접근법과의 비교**: Python의 `asyncio` 외에도 `threading`이나 `multiprocessing`으로 병렬 처리를 할 수 있다. 하지만 I/O 바운드 작업(API 호출)에서는 `asyncio`가 가장 효율적이다. 스레드는 GIL(Global Interpreter Lock) 제약이 있고, 프로세스는 메모리 오버헤드가 크다. `asyncio`는 단일 스레드에서 이벤트 루프를 통해 I/O 대기 시간을 효율적으로 활용하므로, API 호출 병렬화에 최적이다. 다만 CPU 바운드 작업(대량 데이터 처리)에서는 `multiprocessing`이 더 적합하다.

| 기준 | 동기(Sync) | 비동기(Async) |
|------|-----------|--------------|
| API 호출 수 | 1~2개 | 3개 이상 |
| 의존성 | 순차 의존적 | 독립적 |
| 응답 시간 요구 | 느려도 됨 | 빠를수록 좋음 |
| 구현 복잡도 | 낮음 | 중간~높음 |

이를 코드로 표현하면 다음과 같다:

```python
import httpx
import asyncio


# 패턴 1: 순차 의존적 -> 동기 처리
def sync_dependent_calls():
    """주문 조회 -> 배송 추적 -> 예상 도착일 (순차 의존)"""
    with httpx.Client(base_url="https://api.example.com") as client:
        order = client.get("/orders/ORD-123").json()
        shipping = client.get(f"/shipping/{order['shipping_id']}").json()
        eta = client.get(f"/carriers/{shipping['carrier']}/eta").json()
        return {"order": order, "shipping": shipping, "eta": eta}


# 패턴 2: 독립적 -> 비동기 병렬 처리
async def async_independent_calls():
    """상품 정보 + 리뷰 + 가격 이력 병렬 조회 (독립적)"""
    async with httpx.AsyncClient(base_url="https://api.example.com") as client:
        product, reviews, history = await asyncio.gather(
            client.get("/products/PROD-456"),
            client.get("/products/PROD-456/reviews"),
            client.get("/products/PROD-456/price-history"),
        )
        return {
            "product": product.json(),
            "reviews": reviews.json(),
            "price_history": history.json(),
        }


# 패턴 3: 혼합 (Semi-parallel)
async def mixed_calls():
    """주문 조회(선행) -> (배송 추적 + 환불 정책) 병렬"""
    async with httpx.AsyncClient(base_url="https://api.example.com") as client:
        order = (await client.get("/orders/ORD-123")).json()
        shipping, refund = await asyncio.gather(
            client.get(f"/shipping/{order['shipping_id']}"),
            client.get(f"/products/{order['product_id']}/refund-policy"),
        )
        return {"order": order, "shipping": shipping.json(), "refund": refund.json()}
```

**실행 결과 비교**:
```
sync_dependent_calls: 1.5초 (3개 순차)
async_independent_calls: 0.5초 (3개 병렬)
mixed_calls: 1.0초 (1개 순차 + 2개 병렬)
```

### 예제

아래 예제는 Tool 간 의존성 그래프를 분석하여 자동으로 병렬/순차 실행을 결정하는 `AgentAPIExecutor`다. 의존성이 충족된 Tool들을 매 라운드마다 병렬 실행하고, 이전 실행 결과를 `$참조` 문법으로 후속 Tool의 인자에 주입하는 구조다.

```python
import httpx
import asyncio
from typing import Any


class AgentAPIExecutor:
    """Tool 실행에서 동기/비동기를 자동 판단하는 실행기"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.dependency_graph: dict[str, list[str]] = {}

    def register_dependency(self, tool: str, depends_on: list[str]):
        self.dependency_graph[tool] = depends_on

    async def execute_tools(self, tool_calls: list[dict]) -> dict[str, Any]:
        results: dict[str, Any] = {}
        executed: set[str] = set()
        remaining = list(tool_calls)

        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            while remaining:
                ready = [c for c in remaining
                         if all(d in executed for d in self.dependency_graph.get(c["name"], []))]
                not_ready = [c for c in remaining if c not in ready]

                if not ready:
                    raise RuntimeError("순환 의존성 감지")

                batch = await asyncio.gather(
                    *[self._execute_single(client, c, results) for c in ready]
                )
                for call, result in zip(ready, batch):
                    results[call["name"]] = result
                    executed.add(call["name"])
                remaining = not_ready

        return results

    async def _execute_single(self, client, call, prior_results):
        args = call["arguments"].copy()
        for key, value in args.items():
            if isinstance(value, str) and value.startswith("$"):
                ref_tool, ref_field = value[1:].split(".")
                if ref_tool in prior_results:
                    args[key] = prior_results[ref_tool].get(ref_field)
        response = await client.get(call["endpoint"], params=args)
        return response.json()


# 사용: get_order -> (get_shipping + get_refund_policy) 병렬 -> calculate_eta
executor = AgentAPIExecutor("https://api.example.com")
executor.register_dependency("get_shipping", depends_on=["get_order"])
executor.register_dependency("get_refund_policy", depends_on=["get_order"])
executor.register_dependency("calculate_eta", depends_on=["get_shipping"])
```

**실행 결과**:
```
실행 순서:
  1. get_order (선행 조건)
  2. get_shipping + get_refund_policy (병렬)
  3. calculate_eta (get_shipping에 의존)
```

### Q&A
**Q: 모든 API 호출을 비동기로 하면 안 되나요?**
A: 기술적으로는 가능하지만 권장하지 않는다. 비동기 코드는 디버깅이 어렵고, 에러 추적이 복잡하다. 단일 API 호출이나 순차 의존적 호출은 동기가 더 명확하다. "성능이 필요한 곳에만 비동기"가 원칙이다.

<details>
<summary>퀴즈: 3개의 API 호출이 A->B, A->C 의존성을 가질 때, 최적의 실행 방식은?</summary>

**힌트**: B와 C의 관계를 생각해보세요.

**정답**: A를 먼저 동기적으로 실행한 뒤, B와 C를 비동기 병렬로 실행한다(Semi-parallel 패턴). A의 결과가 B와 C 모두에 필요하지만, B와 C는 서로 독립적이므로 병렬 실행이 가능하다. 총 소요 시간은 A + max(B, C)이다.
</details>

---

## 개념 3: Schema Validation / Guardrail

### 개념 설명

**왜 이것이 중요한가**: AI Agent 아키텍처에서 LLM과 외부 API 사이에는 근본적인 신뢰 문제가 존재한다. LLM은 확률적으로 텍스트를 생성하는 시스템이므로, Tool 호출 시 생성하는 파라미터가 항상 올바르다는 보장이 없다. 존재하지 않는 필드를 만들어내거나, 타입을 잘못 지정하거나, 범위를 벗어난 값을 생성하거나, 심지어 악의적 패턴(SQL Injection, XSS)이 포함된 문자열을 생성할 수도 있다. 이는 LLM의 "결함"이 아니라 확률적 생성 모델의 본질적 특성이다. 따라서 LLM의 출력을 "검증 없이 그대로 외부 시스템에 전달"하는 것은 보안과 안정성 모두에서 위험하다.

**핵심 원리**: 이 문제를 해결하는 것이 **Schema Validation**과 **Guardrail**이다. 이 둘은 LLM과 외부 API 사이에 위치하는 안전 장치(safety layer)로, 각각 다른 수준의 검증을 담당한다:

- **Schema Validation**은 **데이터 형식 수준**의 검증이다. 파라미터의 타입이 올바른지, 필수 필드가 있는지, 값의 범위가 허용 범위 내인지를 확인한다. Python에서는 Pydantic이 이 역할의 사실상 표준 라이브러리로, 타입 힌트 기반의 선언적 검증을 제공한다.
- **Guardrail**은 **비즈니스 정책 수준**의 검증이다. 개인정보(PII)가 API 요청에 포함되지 않았는지, 호출 비용이 예산을 초과하지 않는지, 위험한 작업(삭제, 권한 변경)이 적절한 승인 없이 실행되지 않는지를 확인한다.

왜 두 단계가 모두 필요한가? Schema Validation만으로는 비즈니스 로직 위반을 잡을 수 없다. 예를 들어 `{"query": "kim@email.com 주문"}` 같은 입력은 타입도 올바르고 길이도 적절하지만, 개인정보(이메일)가 검색 쿼리에 포함되어 있어 외부 API에 전달되면 안 된다. 반대로 Guardrail만으로는 기본적인 타입 오류나 누락 필드를 검증하기 어렵다.

**실무에서의 의미**: 실무에서는 Pydantic으로 형식을 먼저 검증한 뒤, 통과한 데이터에 Guardrail 정책을 적용하는 **2단계 파이프라인**이 표준 패턴이다. Guardrail의 동작 방식(action)은 위반의 심각도에 따라 세 가지로 분류된다. **Block(차단)**은 SQL Injection, PII 노출처럼 보안에 직결되는 위반에 적용한다. **Warn(경고)**은 고비용 API 호출처럼 허용은 하되 관리자가 인지해야 하는 경우에 적용한다. **Modify(수정)**는 검색 쿼리 길이 초과처럼 자동으로 수정 가능한 형식 위반에 적용한다. 보안 관련 위반은 "수정 후 통과"가 위험하므로 반드시 차단해야 한다는 원칙을 지켜야 한다.

**다른 접근법과의 비교**: Guardrail의 대안으로 LLM 자체에게 "안전한 파라미터만 생성하라"고 프롬프트에 지시하는 방법이 있다. 그러나 이 방식은 확률적 특성상 100% 보장이 불가능하며, 프롬프트 인젝션(Prompt Injection) 공격에도 취약하다. 코드 레벨의 검증(Pydantic + Guardrail)은 프롬프트 지시와 독립적으로 동작하므로, 프롬프트가 어떻게 조작되더라도 안전성을 보장한다. 보안 분야의 원칙인 "Defense in Depth(심층 방어)"를 적용하는 것이다. 프롬프트 지시는 1차 방어선이고, Schema Validation + Guardrail은 2차 방어선이다.

이를 코드로 표현하면 다음과 같다:

```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal
import json


class ProductSearchParams(BaseModel):
    """상품 검색 파라미터 스키마"""
    query: str = Field(..., min_length=1, max_length=200, description="검색 키워드")
    category: Literal["electronics", "clothing", "food", "furniture"] | None = None
    min_price: int = Field(default=0, ge=0)
    max_price: int = Field(default=10_000_000, le=10_000_000)

    @field_validator("query")
    @classmethod
    def sanitize_query(cls, v: str) -> str:
        dangerous_patterns = ["'", '"', ";", "--", "<script>", "DROP TABLE"]
        for pattern in dangerous_patterns:
            if pattern.lower() in v.lower():
                raise ValueError(f"위험한 패턴 감지: {pattern}")
        return v.strip()


def validate_tool_call(tool_name: str, raw_arguments: str) -> dict:
    SCHEMA_MAP = {"search_product": ProductSearchParams}
    schema_class = SCHEMA_MAP.get(tool_name)
    if not schema_class:
        raise ValueError(f"알 수 없는 Tool: {tool_name}")
    args = json.loads(raw_arguments)
    validated = schema_class(**args)
    return validated.model_dump()


# 정상 케이스
result = validate_tool_call("search_product", '{"query": "무선 이어폰", "category": "electronics"}')
print(f"정상: {result}")

# SQL Injection 시도 -> 차단
try:
    validate_tool_call("search_product", '{"query": "이어폰\'; DROP TABLE products;--"}')
except ValueError as e:
    print(f"차단: {e}")
```

**실행 결과**:
```
정상: {'query': '무선 이어폰', 'category': 'electronics', 'min_price': 0, 'max_price': 10000000}
차단: 파라미터 검증 실패: 위험한 패턴 감지: '
```

### 예제

다음 예제는 비즈니스 정책 수준의 Guardrail 시스템을 구현한 것이다. PII 필터링, 비용 제한, 쿼리 길이 자동 수정 등 여러 규칙을 파이프라인으로 연결하여, 모든 Tool 호출이 이 안전 장치를 거치도록 한다.

```python
import re


class Guardrail:
    def __init__(self):
        self.rules: list[dict] = []

    def add_rule(self, name: str, check_fn, action: str = "block"):
        self.rules.append({"name": name, "check": check_fn, "action": action})

    def evaluate(self, tool_name: str, arguments: dict) -> dict:
        result = {"allowed": True, "arguments": arguments.copy(), "warnings": []}
        for rule in self.rules:
            violation = rule["check"](tool_name, result["arguments"])
            if violation:
                if rule["action"] == "block":
                    result["allowed"] = False
                    result["block_reason"] = f"[{rule['name']}] {violation}"
                    return result
                elif rule["action"] == "warn":
                    result["warnings"].append(f"[{rule['name']}] {violation}")
                elif rule["action"] == "modify":
                    result["warnings"].append(f"[{rule['name']}] 자동 수정: {violation}")
        return result


guardrail = Guardrail()

# PII 차단 규칙
def check_pii(tool_name, args):
    patterns = {"email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "phone": r"\d{2,3}-\d{3,4}-\d{4}"}
    for key, value in args.items():
        if isinstance(value, str):
            for pii_type, pattern in patterns.items():
                if re.search(pattern, value):
                    return f"PII 감지({pii_type}): {key} 필드"

guardrail.add_rule("pii_filter", check_pii, action="block")

# 테스트
print(guardrail.evaluate("search_product", {"query": "노트북"}))
print(guardrail.evaluate("search_product", {"query": "kim@email.com 주문"}))
```

**실행 결과**:
```
{'allowed': True, 'arguments': {'query': '노트북'}, 'warnings': []}
{'allowed': False, 'block_reason': '[pii_filter] PII 감지(email): query 필드', ...}
```

### Q&A
**Q: Pydantic validation과 Guardrail은 어떻게 다른가요?**
A: Pydantic은 데이터 형식(타입, 범위, 필수 필드)을 검증하는 "스키마 레벨" 검증이다. Guardrail은 비즈니스 로직(PII 차단, 비용 제한, 권한 확인)을 적용하는 "정책 레벨" 검증이다. 실무에서는 Pydantic으로 형식을 먼저 검증한 뒤, Guardrail로 정책을 적용하는 2단계 구조가 표준이다.

<details>
<summary>퀴즈: LLM이 SQL Injection 패턴이 포함된 검색어를 생성했을 때, 차단(block)과 수정(modify) 중 어떤 전략이 더 안전할까요?</summary>

**힌트**: 보안 관련 위반의 기본 원칙은 무엇인가요?

**정답**: 차단(block)이 더 안전하다. SQL Injection 같은 보안 위반은 "수정 후 통과"가 위험하다. 공격 패턴을 정교하게 변형하면 단순 치환으로는 방어할 수 없기 때문이다. 보안 위반은 항상 차단하고, 길이 초과나 기본값 누락 같은 형식 위반만 자동 수정하는 것이 원칙이다.
</details>

---

## 개념 4: 인증 · 보안 · Rate Limit 설계

### 개념 설명

**왜 이것이 중요한가**: Agent가 외부 API를 호출할 때 인증(Authentication), 보안(Security), 속도 제한(Rate Limiting)은 선택 사항이 아니라 필수 인프라다. 이 세 가지를 빠뜨리면 실제 운영에서 치명적인 문제가 발생한다. API Key가 노출되면 타인이 과금을 발생시킬 수 있고, 보안이 없으면 민감 데이터가 유출될 수 있으며, Rate Limit을 관리하지 않으면 API 제공자로부터 서비스가 차단될 수 있다. 이 세 가지는 개발 단계에서는 무시하기 쉽지만, 프로덕션에서는 하나라도 빠지면 서비스가 위험에 노출된다.

**핵심 원리**: 각 요소의 핵심 원리를 살펴보자:

- **인증(Authentication)**: API Key를 안전하게 관리하는 것이 핵심이다. 가장 흔한 실수는 API Key를 소스 코드에 직접 하드코딩하는 것이다. 코드가 Git 저장소에 커밋되면 API Key가 노출되는데, GitHub에서는 매일 수백만 개의 노출된 API Key가 탐지된다. 안전한 방법은 환경 변수(`os.environ`), Secret Manager(AWS Secrets Manager, HashiCorp Vault), 또는 `.env` 파일(반드시 `.gitignore`에 등록)을 사용하는 것이다. 로그에 API Key가 출력되지 않도록 마스킹(masking) 처리하는 것도 중요하다.
- **Rate Limiting**: Agent가 외부 API를 과도하게 호출하지 않도록 제어하는 메커니즘이다. 대부분의 외부 API는 분당/시간당 호출 횟수를 제한하며, 초과 시 HTTP 429(Too Many Requests) 응답을 반환한다. Agent는 대화 흐름에 따라 API 호출이 불규칙적으로 발생(burst)하므로, **Token Bucket** 알고리즘이 가장 적합하다. Token Bucket은 버킷에 토큰이 일정 속도로 충전되고, API 호출 시 토큰을 소비하는 구조다. 버킷에 토큰이 있으면 즉시 호출이 가능하고(burst 허용), 토큰이 없으면 충전될 때까지 대기한다.
- **비용 관리**: LLM API 호출, Embedding API 호출, 외부 데이터 API 호출 등이 모두 과금 대상이므로, Agent가 무한 루프에 빠지거나 예기치 못한 대량 호출을 하면 비용이 폭발할 수 있다. 일일 예산 한도를 설정하고 예산 초과 시 호출을 차단하는 안전 장치가 반드시 필요하다.

**실무에서의 의미**: 이 세 가지 요소(인증 + Rate Limit + 비용 추적)를 하나의 통합 미들웨어로 구현하면, 모든 API 호출이 자동으로 이 안전망을 거치게 된다. Token Bucket 알고리즘에서 Fixed Window 방식 대신 Token Bucket을 사용하는 이유는 "boundary burst" 문제 때문이다. Fixed Window는 시간 창(예: 1분) 경계에서 2배 트래픽이 발생할 수 있지만(59초에 60회 + 61초에 60회 = 2초간 120회), Token Bucket은 토큰이 연속적으로 충전되므로 이 문제가 없다.

**다른 접근법과의 비교**: API Key 관리의 대안으로 OAuth 2.0 토큰 기반 인증이 있다. API Key는 영구적이고 노출 시 즉시 교체해야 하지만, OAuth 토큰은 만료 시간이 있어 노출되더라도 피해가 제한적이다. 다만 OAuth는 구현 복잡도가 높으므로, 내부 서비스 간 통신에는 API Key, 외부 사용자 대면 서비스에는 OAuth를 사용하는 것이 일반적이다. Rate Limiting에서도 클라이언트 측과 서버 측을 모두 고려해야 한다. 클라이언트 측 Rate Limiter(Token Bucket)는 서버의 429 응답을 사전 방지하고, 서버의 `Retry-After` 헤더는 서버 측 제한에 대응하는 것이다.

이를 코드로 표현하면 다음과 같다:

```python
import os
import time
from dataclasses import dataclass, field


class SecureAPIKeyManager:
    """API Key 안전 관리"""
    def __init__(self):
        self._keys: dict[str, str] = {}

    def load_from_env(self, key_name: str, env_var: str):
        value = os.environ.get(env_var)
        if not value:
            raise ValueError(f"환경 변수 {env_var}가 설정되지 않았습니다")
        self._keys[key_name] = value

    def get_masked(self, key_name: str) -> str:
        key = self._keys[key_name]
        return f"{key[:4]}****{key[-4:]}"


@dataclass
class TokenBucketRateLimiter:
    """Token Bucket 기반 Rate Limiter"""
    max_tokens: int
    refill_rate: float          # 초당 토큰 충전량
    tokens: float = field(init=False)
    last_refill: float = field(init=False)

    def __post_init__(self):
        self.tokens = float(self.max_tokens)
        self.last_refill = time.time()

    def _refill(self):
        now = time.time()
        self.tokens = min(self.max_tokens, self.tokens + (now - self.last_refill) * self.refill_rate)
        self.last_refill = now

    def acquire(self, tokens: int = 1) -> bool:
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


# 테스트
limiter = TokenBucketRateLimiter(max_tokens=3, refill_rate=1.0)
for i in range(5):
    if limiter.acquire():
        print(f"요청 {i+1}: 허용")
    else:
        print(f"요청 {i+1}: 대기 필요")
        time.sleep(1)
        limiter.acquire()
        print(f"요청 {i+1}: 대기 후 허용")
```

**실행 결과**:
```
요청 1: 허용
요청 2: 허용
요청 3: 허용
요청 4: 대기 필요
요청 4: 대기 후 허용
요청 5: 대기 필요
요청 5: 대기 후 허용
```

### 예제

다음 예제는 API 사용량 추적과 일일 예산 관리 기능을 갖춘 프로덕션 레벨의 Agent API 클라이언트다.

```python
from dataclasses import dataclass, field


@dataclass
class APIUsageTracker:
    """API 사용량 추적 및 비용 관리"""
    budget_limit: float
    cost_per_request: dict = field(default_factory=dict)
    usage: dict = field(default_factory=lambda: {"total_cost": 0.0, "requests": 0})

    def track(self, api_name: str) -> bool:
        cost = self.cost_per_request.get(api_name, 0.001)
        if self.usage["total_cost"] + cost > self.budget_limit:
            return False
        self.usage["total_cost"] += cost
        self.usage["requests"] += 1
        return True

    def get_summary(self) -> dict:
        remaining = self.budget_limit - self.usage["total_cost"]
        return {
            "total_cost": f"${self.usage['total_cost']:.4f}",
            "total_requests": self.usage["requests"],
            "remaining_budget": f"${remaining:.4f}",
        }


tracker = APIUsageTracker(budget_limit=1.0, cost_per_request={"openai": 0.01, "weather": 0.001})
for i in range(5):
    if tracker.track("openai"):
        print(f"호출 {i+1}: 허용")
    else:
        print(f"호출 {i+1}: 예산 초과")
        break
print(f"\n사용량 요약: {tracker.get_summary()}")
```

**실행 결과**:
```
호출 1: 허용
호출 2: 허용
호출 3: 허용
호출 4: 허용
호출 5: 허용

사용량 요약: {'total_cost': '$0.0500', 'total_requests': 5, 'remaining_budget': '$0.9500'}
```

### Q&A
**Q: API Key를 코드에 직접 넣으면 안 되나요?**
A: 절대 안 된다. 코드가 Git에 커밋되면 API Key가 노출된다. GitHub에서는 매일 수백만 개의 노출된 API Key가 탐지된다. 반드시 환경 변수, Secret Manager(AWS Secrets Manager, HashiCorp Vault), 또는 `.env` 파일(`.gitignore`에 등록)을 사용해야 한다.

<details>
<summary>퀴즈: Token Bucket과 Fixed Window Rate Limiter의 차이는 무엇이고, Agent에는 어떤 것이 더 적합할까요?</summary>

**힌트**: 버스트(burst) 트래픽을 어떻게 처리하는지 비교해보세요.

**정답**: Fixed Window는 시간 창(예: 1분)을 고정하고 그 안에서 요청 수를 제한한다. 창 경계에서 2배 트래픽이 발생할 수 있다(59초에 60회 + 61초에 60회 = 2초간 120회). Token Bucket은 토큰이 연속적으로 충전되므로 이 문제가 없다. Agent는 대화 흐름에 따라 API 호출이 불규칙하게 발생(버스트)하므로, Token Bucket이 더 적합하다.
</details>

---

## 실습

### 실습 1: 비동기 API 클라이언트 구현
- **연관 학습 목표**: 학습 목표 1
- **실습 목적**: 동기/비동기 API 호출의 성능 차이를 측정하고, 병렬 + 캐시 결합 패턴을 구현한다
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 30분
- **선행 조건**: httpx, asyncio 기본 사용법
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**실습 내용**:

공개 API(JSONPlaceholder)를 사용하여 다음을 구현한다:
1. 동기 순차 호출: 10개의 사용자 정보를 순차적으로 조회
2. 비동기 병렬 호출: 동일 10개를 병렬로 조회
3. TTL 캐시 적용: 동일 요청 재호출 시 캐시에서 반환

```python
import httpx
import asyncio
import time
from cachetools import TTLCache

BASE_URL = "https://jsonplaceholder.typicode.com"

# TODO: 동기 순차 호출 구현
def fetch_users_sync(user_ids: list[int]) -> list[dict]:
    """동기 순차 호출로 사용자 정보 조회"""
    pass

# TODO: 비동기 병렬 호출 구현
async def fetch_users_async(user_ids: list[int]) -> list[dict]:
    """비동기 병렬 호출로 사용자 정보 조회"""
    pass

# TODO: TTL 캐시 적용 비동기 클라이언트 구현
class CachedUserClient:
    """TTL 캐시가 적용된 비동기 사용자 조회 클라이언트"""
    pass

# 성능 비교 실행
user_ids = list(range(1, 11))

start = time.time()
fetch_users_sync(user_ids)
sync_time = time.time() - start

start = time.time()
asyncio.run(fetch_users_async(user_ids))
async_time = time.time() - start

print(f"동기: {sync_time:.2f}초 | 비동기: {async_time:.2f}초 | 개선: {sync_time/async_time:.1f}배")
```

### 실습 2: API Guardrail 시스템 구축
- **연관 학습 목표**: 학습 목표 2
- **실습 목적**: LLM이 생성한 API 호출 파라미터를 검증하는 Guardrail 시스템을 구축한다
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 25분
- **선행 조건**: Pydantic 기본 사용법
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**실습 내용**:

다음 Guardrail 규칙을 구현한다:
1. PII 필터링 (이메일, 전화번호 차단)
2. 쿼리 길이 제한 (500자 초과 시 자동 잘라냄)
3. 비용 예산 관리 (일일 $1 한도)
4. 위험 API 차단 (delete, drop 키워드 포함 시)

10개 테스트 케이스로 Guardrail의 정확한 동작을 검증한다.

### 실습 3: Rate Limit이 적용된 Agent Tool Executor
- **연관 학습 목표**: 학습 목표 3
- **실습 목적**: Token Bucket Rate Limiter와 API Key 관리가 통합된 Tool Executor를 구현한다
- **실습 유형**: 코드 작성
- **난이도**: 심화
- **예상 소요 시간**: 30분
- **선행 조건**: 실습 1, 2 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**실습 내용**:

다음 기능을 갖춘 `ProductionToolExecutor`를 구현한다:
1. Token Bucket Rate Limiter (분당 10회)
2. API Key 마스킹 로깅
3. 요청별 비용 추적
4. Rate Limit 초과 시 자동 대기

```python
# TODO: ProductionToolExecutor 구현
# 요구사항:
# 1. TokenBucketRateLimiter: max_tokens=10, refill_rate=10/60
# 2. SecureAPIKeyManager: 환경 변수에서 키 로드
# 3. APIUsageTracker: 일일 예산 $1
# 4. 20회 연속 호출 테스트로 Rate Limit 동작 확인
```

---

## 핵심 정리
- httpx의 Connection Pooling과 비동기 병렬 호출을 조합하면 API Latency를 3배 이상 줄일 수 있다
- 동기/비동기 선택 기준: API 호출이 독립적이면 비동기 병렬, 순차 의존적이면 동기, 혼합이면 Semi-parallel 패턴을 사용한다
- Pydantic Schema Validation(형식 검증)과 Guardrail(정책 검증)을 2단계로 적용하여 LLM의 잘못된 API 호출을 사전 차단한다
- API Key는 반드시 환경 변수 또는 Secret Manager로 관리하고, 로그에는 마스킹하여 출력한다
- Token Bucket Rate Limiter는 Agent의 불규칙한 API 호출 패턴에 가장 적합하며, 서버의 429 응답에 대한 Retry-After 처리도 함께 구현해야 한다
