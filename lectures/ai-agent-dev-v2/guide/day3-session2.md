# Day 3 Session 2 — 외부 API · 데이터 연동 최적화

> **목표**: REST API 연동의 지연시간 최소화, 비동기 설계, 보안·검증 패턴 완성
> **시간**: 2시간 | **대상**: AI 개발자, 데이터 엔지니어, 기술 리더

---

## 1. 왜 중요한가

Agent가 아무리 뛰어나도 외부 API가 느리면 쓸 수 없다.
응답 지연 1초마다 사용자 이탈률이 11% 증가한다(Google 연구).
→ **API 연동 최적화 = Agent 상용화의 핵심**

인증 취약점, 잘못된 입력 허용, Rate Limit 무시는
프로덕션 장애의 주요 원인이다.
설계 단계에서 이를 다루지 않으면 운영 중 대가를 치른다.

---

## 2. 핵심 원리

### 2.1 REST API 연동 및 Latency 최소화

**Latency 발생 지점 분석**

```
사용자 요청
  → [1] Agent 처리 (LLM 추론)
  → [2] API 호출 (네트워크 RTT)
  → [3] 외부 서버 처리
  → [4] 응답 파싱
  → [5] 결과 반환
```

| 지점 | 최적화 방법 | 예상 절감 |
|------|------------|-----------|
| [1] | 불필요한 Tool 호출 제거 | 0.5~2초 |
| [2] | HTTP/2, Connection Pool | 50~200ms |
| [3] | CDN, 엣지 서버 활용 | 100~500ms |
| [4] | 스트리밍 파싱 | 50~100ms |
| [5] | 캐싱 | 전체 절감 |

**Connection Pool 설정**

```python
import httpx
from contextlib import asynccontextmanager

# 전역 HTTP 클라이언트 (재사용)
http_client = httpx.AsyncClient(
    limits=httpx.Limits(
        max_keepalive_connections=20,
        max_connections=100,
        keepalive_expiry=30
    ),
    timeout=httpx.Timeout(
        connect=2.0,   # 연결 타임아웃
        read=10.0,     # 읽기 타임아웃
        write=5.0,     # 쓰기 타임아웃
        pool=1.0       # 풀 대기 타임아웃
    )
)
```

→ 매 요청마다 새 연결을 만들면 100ms+ 낭비된다.
→ Connection Pool로 연결을 재사용하면 RTT를 대폭 줄인다.

**캐싱 전략**

```python
from functools import lru_cache
import time

class APICache:
    def __init__(self, ttl_seconds: int = 300):
        self._cache = {}
        self._ttl = ttl_seconds

    def get(self, key: str):
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self._ttl:
                return value
            del self._cache[key]
        return None

    def set(self, key: str, value):
        self._cache[key] = (value, time.time())

cache = APICache(ttl_seconds=300)

async def get_weather_cached(city: str) -> dict:
    cache_key = f"weather:{city}"
    cached = cache.get(cache_key)
    if cached:
        return cached  # 캐시 히트: 0ms

    result = await fetch_weather_api(city)  # 실제 API 호출
    cache.set(cache_key, result)
    return result
```

---

### 2.2 비동기 vs 동기 처리 설계

**언제 비동기를 쓰는가**

| 상황 | 동기 | 비동기 |
|------|------|--------|
| 단일 API 호출 | 충분 | 과잉 설계 |
| 다중 독립 API 호출 | 느림 | 필수 |
| DB 쿼리 포함 | 느림 | 권장 |
| CPU 집약 작업 | 비동기 불필요 | multiprocessing 고려 |

**동기 방식 문제점**

```python
# 나쁜 예: 순차 실행 (총 3초)
weather = requests.get("https://api.weather.com/seoul")  # 1초
news = requests.get("https://api.news.com/today")        # 1초
stocks = requests.get("https://api.stocks.com/SAMSUNG")  # 1초
```

**비동기 방식 (병렬, 총 ~1초)**

```python
import asyncio
import httpx

async def fetch_all():
    async with httpx.AsyncClient() as client:
        # 세 API를 동시 호출
        weather_task = client.get("https://api.weather.com/seoul")
        news_task = client.get("https://api.news.com/today")
        stocks_task = client.get("https://api.stocks.com/SAMSUNG")

        weather, news, stocks = await asyncio.gather(
            weather_task, news_task, stocks_task,
            return_exceptions=True  # 하나 실패해도 다른 결과 반환
        )

    return {
        "weather": weather.json() if not isinstance(weather, Exception) else None,
        "news": news.json() if not isinstance(news, Exception) else None,
        "stocks": stocks.json() if not isinstance(stocks, Exception) else None
    }
```

**Semaphore로 동시 요청 제한**

```python
# Rate Limit 대응: 최대 5개 동시 요청
semaphore = asyncio.Semaphore(5)

async def fetch_with_limit(url: str) -> dict:
    async with semaphore:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()
```

---

### 2.3 Schema Validation / Guardrail

**입력 검증 (Pydantic)**

```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class WeatherRequest(BaseModel):
    city: str = Field(
        min_length=1,
        max_length=100,
        description="도시명"
    )
    unit: str = Field(
        default="celsius",
        pattern="^(celsius|fahrenheit)$"
    )
    days: Optional[int] = Field(
        default=1,
        ge=1,
        le=14,
        description="예보 일수 (1~14)"
    )

    @validator("city")
    def sanitize_city(cls, v):
        # SQL Injection, XSS 방어
        forbidden = ["'", '"', ";", "<", ">", "DROP", "SELECT"]
        for char in forbidden:
            if char.upper() in v.upper():
                raise ValueError(f"허용되지 않는 문자: {char}")
        return v.strip()
```

**출력 검증 (Guardrail)**

```python
from pydantic import BaseModel
from typing import Optional

class WeatherResponse(BaseModel):
    city: str
    temperature: float = Field(ge=-100, le=100)
    humidity: int = Field(ge=0, le=100)
    description: str
    source: str

def validate_api_response(raw: dict) -> WeatherResponse:
    try:
        return WeatherResponse(**raw)
    except Exception as e:
        # 검증 실패 시 구조화된 오류 반환
        raise ValueError(f"API 응답 형식 오류: {e}")
```

**Agent Tool에 Guardrail 통합**

```python
async def weather_tool_with_guardrail(city: str, unit: str = "celsius") -> dict:
    # 1. 입력 검증
    try:
        req = WeatherRequest(city=city, unit=unit)
    except ValueError as e:
        return {"error": f"잘못된 입력: {e}"}

    # 2. API 호출
    raw = await fetch_weather_api(req.city, req.unit)

    # 3. 출력 검증
    try:
        validated = validate_api_response(raw)
        return validated.dict()
    except ValueError as e:
        return {"error": f"응답 검증 실패: {e}"}
```

---

### 2.4 인증 · 보안 · Rate Limit 설계

**API 키 관리 원칙**

```python
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def get_api_keys() -> dict:
    # 환경변수에서만 로드 (코드에 하드코딩 금지)
    keys = {
        "weather": os.environ.get("WEATHER_API_KEY"),
        "news": os.environ.get("NEWS_API_KEY"),
        "openai": os.environ.get("OPENAI_API_KEY")
    }
    missing = [k for k, v in keys.items() if not v]
    if missing:
        raise RuntimeError(f"API 키 누락: {missing}")
    return keys
```

**토큰 갱신 패턴 (OAuth2)**

```python
import time

class TokenManager:
    def __init__(self):
        self._token = None
        self._expires_at = 0

    async def get_token(self) -> str:
        # 만료 60초 전에 갱신
        if time.time() > self._expires_at - 60:
            await self._refresh_token()
        return self._token

    async def _refresh_token(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://auth.example.com/token",
                data={"grant_type": "client_credentials"},
                auth=(CLIENT_ID, CLIENT_SECRET)
            )
            data = response.json()
            self._token = data["access_token"]
            self._expires_at = time.time() + data["expires_in"]
```

**Rate Limit 처리**

```python
import asyncio

class RateLimiter:
    def __init__(self, calls_per_minute: int):
        self.calls_per_minute = calls_per_minute
        self._calls = []

    async def acquire(self):
        now = time.time()
        # 1분 이내 호출 기록만 유지
        self._calls = [t for t in self._calls if now - t < 60]

        if len(self._calls) >= self.calls_per_minute:
            # 가장 오래된 호출 후 1분까지 대기
            wait_until = self._calls[0] + 60
            await asyncio.sleep(wait_until - now)

        self._calls.append(time.time())

# 사용 예
rate_limiter = RateLimiter(calls_per_minute=60)

async def call_api_safely(url: str) -> dict:
    await rate_limiter.acquire()
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            await asyncio.sleep(retry_after)
            return await call_api_safely(url)  # 재시도
        return response.json()
```

---

## 3. 실무 의미

**API 연동 설계 체크리스트**

```
□ Connection Pool: 전역 클라이언트 재사용
□ Timeout: connect/read/write 별도 설정
□ 캐싱: TTL 기반 캐시 (변화 빈도에 따라 설정)
□ 비동기: 독립적인 다중 API 호출은 asyncio.gather
□ 입력 검증: Pydantic으로 모든 입력 검증
□ 출력 검증: 응답 형식 및 값 범위 검증
□ API 키: 환경변수, 코드 하드코딩 금지
□ Rate Limit: 호출 빈도 제한 및 429 처리
□ 오류 처리: 유형별 처리 (Timeout/Auth/RateLimit)
```

**성능 목표**

| 지표 | 목표 | 측정 방법 |
|------|------|-----------|
| API P95 지연 | ≤ 2초 | APM 도구 |
| 캐시 히트율 | ≥ 60% | 캐시 로그 |
| 오류율 | ≤ 1% | 오류 로그 |
| Rate Limit 초과 | 0회/일 | 429 카운트 |

---

## 4. 비교

### 동기 vs 비동기 API 호출

| 항목 | 동기 (requests) | 비동기 (httpx/aiohttp) |
|------|-----------------|----------------------|
| 단일 호출 지연 | 동일 | 동일 |
| 다중 병렬 호출 | N배 느림 | ~1배 (동시 실행) |
| 코드 복잡도 | 낮음 | 중간 |
| 서버 리소스 | 스레드 블로킹 | 비블로킹 |
| 적합한 상황 | 단순 스크립트 | 프로덕션 Agent |

### 캐싱 전략 비교

| 전략 | TTL | 적합한 데이터 | 단점 |
|------|-----|--------------|------|
| In-memory | 짧음 (1~5분) | 날씨, 환율 | 서버 재시작 시 소실 |
| Redis | 중간 (1시간) | 뉴스, 제품 정보 | 인프라 필요 |
| CDN | 김 (1일) | 정적 데이터 | 실시간성 낮음 |

---

## 5. 주의사항

**Timeout을 반드시 설정해야 하는 이유**

> Timeout 없이 API를 호출하면 응답 없는 서버에 무한 대기한다.
> Agent 전체가 응답 불가 상태가 된다.
> connect/read 각각 설정해야 모든 상황을 커버한다.

**환경변수 관리**

> API 키를 코드에 직접 쓰면 Git에 노출된다.
> `.env` 파일도 `.gitignore`에 반드시 추가해야 한다.
> 프로덕션에서는 Secret Manager (AWS Secrets Manager, Vault 등) 사용을 권장한다.

**return_exceptions=True의 중요성**

> `asyncio.gather()`의 기본 동작은 하나라도 실패하면 예외를 던진다.
> `return_exceptions=True`를 설정하면 실패한 항목만 Exception 객체로 반환된다.
> 나머지 성공한 결과를 활용할 수 있어 부분 실패 처리가 가능하다.

**Pydantic v1 vs v2 차이**

> 2026년 기준 Pydantic v2가 표준이다.
> `@validator` 대신 `@field_validator`, `dict()` 대신 `model_dump()` 사용.
> 이 가이드의 코드는 개념 설명용으로 v1 스타일을 일부 사용했다.

---

## 6. 코드 예제

### 완성된 API 연동 레이어

```python
import asyncio
import httpx
import time
import os
from pydantic import BaseModel, Field
from typing import Optional, Any

# ── 설정 ──────────────────────────────────────────
class APIConfig:
    BASE_URL = "https://api.example.com"
    API_KEY = os.environ.get("EXAMPLE_API_KEY", "")
    TIMEOUT = httpx.Timeout(connect=2.0, read=10.0, write=5.0)
    RATE_LIMIT = 60  # calls per minute


# ── HTTP 클라이언트 (싱글턴) ────────────────────────
_client: Optional[httpx.AsyncClient] = None

async def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            base_url=APIConfig.BASE_URL,
            headers={"Authorization": f"Bearer {APIConfig.API_KEY}"},
            timeout=APIConfig.TIMEOUT,
            limits=httpx.Limits(max_keepalive_connections=20)
        )
    return _client


# ── 캐시 ──────────────────────────────────────────
_cache: dict[str, tuple[Any, float]] = {}

def get_cached(key: str, ttl: int = 300) -> Optional[Any]:
    if key in _cache:
        value, ts = _cache[key]
        if time.time() - ts < ttl:
            return value
        del _cache[key]
    return None

def set_cached(key: str, value: Any):
    _cache[key] = (value, time.time())


# ── Rate Limiter ───────────────────────────────────
_call_times: list[float] = []

async def rate_limit_acquire():
    now = time.time()
    global _call_times
    _call_times = [t for t in _call_times if now - t < 60]

    if len(_call_times) >= APIConfig.RATE_LIMIT:
        wait = _call_times[0] + 60 - now
        await asyncio.sleep(max(wait, 0))

    _call_times.append(time.time())


# ── 스키마 ────────────────────────────────────────
class WeatherData(BaseModel):
    city: str
    temperature: float = Field(ge=-100, le=100)
    humidity: int = Field(ge=0, le=100)
    condition: str


# ── API 호출 함수 ──────────────────────────────────
async def fetch_weather(city: str) -> WeatherData:
    # 캐시 확인
    cache_key = f"weather:{city.lower()}"
    cached = get_cached(cache_key, ttl=300)
    if cached:
        return WeatherData(**cached)

    await rate_limit_acquire()
    client = await get_client()

    for attempt in range(3):
        try:
            response = await client.get(f"/weather/{city}")
            response.raise_for_status()
            data = response.json()

            # 출력 검증
            result = WeatherData(**data)
            set_cached(cache_key, data)
            return result

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                retry_after = int(e.response.headers.get("Retry-After", 60))
                await asyncio.sleep(retry_after)
            elif e.response.status_code in (401, 403):
                raise  # 인증 오류는 재시도 불필요
            else:
                if attempt == 2:
                    raise
        except httpx.TimeoutException:
            if attempt == 2:
                raise

    raise RuntimeError("최대 재시도 초과")


# ── 병렬 조회 예시 ─────────────────────────────────
async def fetch_multi_city_weather(cities: list[str]) -> dict:
    tasks = [fetch_weather(city) for city in cities]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return {
        city: result.dict() if isinstance(result, WeatherData) else {"error": str(result)}
        for city, result in zip(cities, results)
    }
```

---

## Q&A

**Q1. 비동기 코드를 FastAPI와 함께 쓸 때 주의사항이 있나요?**

> FastAPI는 기본적으로 async를 지원한다.
> `async def` 엔드포인트에서 `await`를 사용하면 된다.
> 단, 동기 함수(requests 등)를 async 컨텍스트에서 호출하면
> 이벤트 루프가 블로킹되므로 `run_in_executor`를 사용해야 한다.

**Q2. 캐시 TTL을 어떻게 결정하나요?**

> 데이터 변경 주기를 기준으로 설정한다.
> 날씨: 5분, 뉴스: 30분, 제품 정보: 1시간, 국가 코드: 1일.
> 너무 짧으면 캐시 효과가 없고, 너무 길면 오래된 데이터를 반환한다.

**Q3. 개발 환경에서 외부 API 없이 테스트하려면?**

> `httpx.MockTransport` 또는 `respx` 라이브러리로 API를 목킹한다.
> 실제 HTTP 요청 없이 단위 테스트를 작성할 수 있다.
> CI 환경에서 외부 의존성을 제거하여 안정적인 테스트를 보장한다.

---

## 퀴즈

**Q1. Connection Pool을 사용하는 가장 큰 이유는?**

> a) API 키 보안 강화
> b) 매 요청마다 TCP 연결 생성 비용 절감
> c) Rate Limit 우회
> d) 캐시 용량 증가

<details>
<summary>힌트 및 정답</summary>

**힌트**: TCP 연결을 새로 만드는 데는 얼마나 걸릴까? (3-way handshake)

**정답**: b) 매 요청마다 TCP 연결 생성 비용 절감

TCP 연결 수립(3-way handshake)에는 RTT 기준 50~200ms가 소요된다. Connection Pool로 연결을 재사용하면 이 비용을 절감한다.

</details>

---

**Q2. `asyncio.gather(*tasks, return_exceptions=True)`에서 `return_exceptions=True`의 역할은?**

> a) 예외 발생 시 전체 gather를 중단
> b) 예외 발생 시 해당 태스크 결과를 Exception 객체로 반환
> c) 예외를 무시하고 None으로 대체
> d) 예외 로그를 파일에 기록

<details>
<summary>힌트 및 정답</summary>

**힌트**: 10개 API 중 1개가 실패했을 때, 나머지 9개 결과를 살리려면?

**정답**: b) 예외 발생 시 해당 태스크 결과를 Exception 객체로 반환

`return_exceptions=True`를 설정하면 실패한 태스크의 결과가 Exception 객체로 반환되어 나머지 성공한 결과를 활용할 수 있다.

</details>

---

**Q3. API 키를 가장 안전하게 관리하는 방법은?**

> a) 코드에 직접 하드코딩
> b) Git 저장소의 config.json에 저장
> c) 환경변수 또는 Secret Manager 사용
> d) Base64로 인코딩하여 코드에 저장

<details>
<summary>힌트 및 정답</summary>

**힌트**: Git에 올라가면 안 되는 것들은 어디에 두어야 할까?

**정답**: c) 환경변수 또는 Secret Manager 사용

환경변수는 코드와 분리되어 Git에 노출되지 않는다. 프로덕션에서는 AWS Secrets Manager, HashiCorp Vault 등 전용 시스템을 사용한다. Base64 인코딩은 보안이 아니다.

</details>

---

**Q4. Rate Limit 오류 (HTTP 429) 발생 시 올바른 처리 방법은?**

> a) 즉시 오류를 사용자에게 반환
> b) `Retry-After` 헤더 확인 후 해당 시간 대기
> c) 요청을 무한 반복
> d) API 키를 변경하고 재시도

<details>
<summary>힌트 및 정답</summary>

**힌트**: 서버가 "언제 다시 시도할 수 있다"는 정보를 헤더에 담아 보낸다.

**정답**: b) `Retry-After` 헤더 확인 후 해당 시간 대기

`Retry-After` 헤더에 재시도 가능 시간(초)이 담겨 있다. 이를 읽고 대기한 후 재시도하는 것이 올바른 처리다. 무한 반복은 API 차단으로 이어진다.

</details>

---

**Q5. 날씨 API 응답의 TTL을 5분으로 설정한 이유로 가장 적합한 것은?**

> a) 날씨는 5분마다 정확히 업데이트된다
> b) 5분이 가장 빠른 캐시 주기이다
> c) 날씨 변화 빈도와 API 비용의 균형점이다
> d) 날씨 API 약관에서 요구하는 최소 주기이다

<details>
<summary>힌트 및 정답</summary>

**힌트**: TTL 설정은 "데이터 신선도"와 "API 호출 비용"의 트레이드오프다.

**정답**: c) 날씨 변화 빈도와 API 비용의 균형점이다

날씨는 분 단위로 급변하지 않는다. 5분 TTL은 충분한 신선도를 유지하면서 불필요한 API 호출(비용)을 줄이는 균형점이다.

</details>

---

## 실습 명세

### 실습 제목: API 연동 후 검증 로직 비교

**I DO (시연, 15분)**

강사가 직접 시연한다:
1. 동기 방식으로 3개 API 순차 호출 → 총 소요 시간 측정
2. 비동기 `asyncio.gather`로 동일 3개 API 병렬 호출 → 시간 비교
3. Pydantic 검증 없는 API 응답 처리 → 오류 발생 시연
4. Pydantic 검증 추가 후 동일 오류 처리 확인

**WE DO (함께, 30분)**

학생과 함께 단계별 구현:
1. `httpx.AsyncClient` 기반 API 클라이언트 구현
2. TTL 캐시 추가
3. Pydantic 입력/출력 검증 스키마 작성
4. Rate Limiter 구현 및 테스트

**YOU DO (독립, 30분)**

- 3개 이상 외부 API를 비동기로 병렬 호출하는 클라이언트 구현
- TTL 캐시와 Rate Limiter 통합
- 입력/출력 Pydantic 모델 정의
- 오류 유형별 처리 로직 구현 (Timeout, 401, 429, 500)
- `solution/` 폴더에 정답 코드 제공
