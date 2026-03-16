# 로그 · 모니터링 · 장애 대응 설계

## 학습 목표
1. Agent 실행 흐름을 추적할 수 있는 구조화된 로그 시스템을 설계하고 Trace ID 기반 디버깅을 구현할 수 있다
2. 응답 시간, 토큰 사용량, Tool 호출 성공률 등 핵심 메트릭을 수집하고 Grafana/Prometheus 기반 대시보드를 설계할 수 있다
3. LLM 장애, Tool 장애, 데이터 장애를 분류하고 각 유형에 맞는 대응 플레이북과 에스컬레이션 정책을 수립할 수 있다

---

## 개념 1: Agent 로그 설계

### 개념 설명

**왜 AI Agent에는 전통적 로깅이 통하지 않는가**

전통적인 웹 서비스의 로깅은 "요청이 들어오고, 처리하고, 응답을 내보내는" 단일 흐름을 기록하면 충분했다. 에러가 발생하면 스택 트레이스를 보고 코드의 어느 줄에서 문제가 생겼는지 바로 찾을 수 있었다. 하지만 AI Agent는 근본적으로 다르다. 하나의 사용자 요청이 LLM 호출, Tool 실행, RAG 검색, 다시 LLM 호출이라는 복잡한 다단계 파이프라인을 거친다. 각 단계가 비결정적(non-deterministic)이고, 같은 입력에도 다른 출력이 나올 수 있으며, "에러는 없는데 결과가 틀린" 상황이 빈번하게 발생한다. 기존 로깅으로는 "어디서 잘못되었는지"를 추적할 수 없다.

**Observability의 세 기둥과 Agent 시스템에서의 의미**

소프트웨어 관측성(Observability)은 Logs, Metrics, Traces 세 가지 기둥으로 구성된다. Agent 시스템에서 이 세 기둥은 전통 시스템과 다른 의미를 갖는다. Logs는 단순히 "무엇이 일어났는가"를 넘어 LLM의 입출력 전문, 프롬프트 해시, 모델 버전까지 포함해야 한다. Metrics는 HTTP 상태 코드 기반의 에러율 외에 "응답 품질"이라는 새로운 차원이 추가된다. Traces는 가장 핵심적인데, Agent의 다단계 실행 흐름을 하나의 Trace ID로 묶어 "이 사용자의 이 질문이 어떤 경로를 거쳐 어떤 답변에 도달했는지"를 추적할 수 있어야 한다. OpenTelemetry에서 차용한 Span/Trace 구조가 Agent 로깅의 표준이 되고 있는 이유가 바로 이것이다.

**구조화된 로깅이 Agent 디버깅에 필수인 이유**

Agent 시스템에서 "응답이 틀렸다"는 신고가 들어왔을 때, 원인은 검색 단계(잘못된 문서 검색), 컨텍스트 조합 단계(관련 없는 문서 포함), LLM 생성 단계(환각) 중 어디에든 있을 수 있다. 구조화된 로그가 없으면 이 세 가지 원인을 구별할 방법이 없다. 구조화된 로그란 각 실행 단계를 독립된 Span으로 분리하고, 부모-자식 관계로 연결하며, 각 Span에 입력/출력/소요 시간/에러 정보를 정형화된 형태로 기록하는 것이다. 이를 통해 "상류에서 하류로" 문제를 추적하는 체계적 디버깅이 가능해진다. 다른 접근법으로는 단순 텍스트 로그나 printf 디버깅이 있지만, 프로덕션 환경에서 수천 건의 동시 요청을 처리하는 Agent에서는 Trace ID 없이는 특정 요청의 로그를 찾아내는 것조차 불가능하다.

**Trace 구조**

```
Trace (trace_id: "tr-abc123")
├── Span: "llm_call" (span_id: "sp-001", parent: null)
│   ├── input: {prompt, model, temperature}
│   ├── output: {response, tokens_used}
│   ├── duration: 1200ms
│   └── metadata: {model_version, prompt_hash}
├── Span: "tool_call:search_docs" (span_id: "sp-002", parent: "sp-001")
│   ├── input: {query, top_k}
│   ├── output: {documents: [...]}
│   ├── duration: 350ms
│   └── metadata: {index_name, embedding_model}
├── Span: "tool_call:calculate" (span_id: "sp-003", parent: "sp-001")
│   ├── input: {expression}
│   ├── output: {result}
│   ├── duration: 15ms
│   └── error: null
└── Span: "llm_call_final" (span_id: "sp-004", parent: null)
    ├── input: {prompt_with_context}
    ├── output: {final_response}
    └── duration: 800ms
```

이제 이 Trace 구조를 코드로 구현해보자. Span 단위로 실행을 기록하고, 컨텍스트 매니저를 활용해 시작/종료를 자동으로 관리하는 TraceLogger를 만든다.

```python
import os
import uuid
import time
import json
from dataclasses import dataclass, field
from datetime import datetime
from contextlib import contextmanager
from typing import Any
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

@dataclass
class Span:
    """실행 단위를 나타내는 Span."""
    span_id: str
    trace_id: str
    parent_span_id: str | None
    operation: str
    start_time: float
    end_time: float | None = None
    duration_ms: float | None = None
    input_data: dict = field(default_factory=dict)
    output_data: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    error: str | None = None
    status: str = "running"  # running, success, error

    def finish(self, output: dict = None, error: str = None) -> None:
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000
        if error:
            self.error = error
            self.status = "error"
        else:
            self.output_data = output or {}
            self.status = "success"

    def to_dict(self) -> dict:
        return {
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "parent_span_id": self.parent_span_id,
            "operation": self.operation,
            "duration_ms": round(self.duration_ms, 2) if self.duration_ms else None,
            "status": self.status,
            "error": self.error,
            "metadata": self.metadata,
        }

class TraceLogger:
    """Agent 실행 흐름을 Trace 단위로 기록한다."""

    def __init__(self):
        self.traces: dict[str, list[Span]] = {}
        self._current_trace_id: str | None = None

    def start_trace(self, metadata: dict = None) -> str:
        trace_id = f"tr-{uuid.uuid4().hex[:12]}"
        self.traces[trace_id] = []
        self._current_trace_id = trace_id
        return trace_id

    @contextmanager
    def span(self, operation: str, parent_span_id: str = None, input_data: dict = None, metadata: dict = None):
        """Span 컨텍스트 매니저: with 블록 내에서 자동으로 시작/종료한다."""
        span = Span(
            span_id=f"sp-{uuid.uuid4().hex[:8]}",
            trace_id=self._current_trace_id,
            parent_span_id=parent_span_id,
            operation=operation,
            start_time=time.time(),
            input_data=input_data or {},
            metadata=metadata or {},
        )
        self.traces[self._current_trace_id].append(span)

        try:
            yield span
            if span.status == "running":
                span.finish(output=span.output_data)
        except Exception as e:
            span.finish(error=str(e))
            raise

    def get_trace(self, trace_id: str) -> list[dict]:
        spans = self.traces.get(trace_id, [])
        return [s.to_dict() for s in spans]

    def get_trace_summary(self, trace_id: str) -> dict:
        spans = self.traces.get(trace_id, [])
        if not spans:
            return {}

        total_duration = sum(s.duration_ms or 0 for s in spans)
        error_spans = [s for s in spans if s.status == "error"]

        return {
            "trace_id": trace_id,
            "total_spans": len(spans),
            "total_duration_ms": round(total_duration, 2),
            "error_count": len(error_spans),
            "operations": [s.operation for s in spans],
            "status": "error" if error_spans else "success",
        }
```

```
# 실행 결과
logger = TraceLogger()
trace_id = logger.start_trace()

with logger.span("llm_call", input_data={"model": MODEL}) as sp1:
    time.sleep(0.1)  # LLM 호출 시뮬레이션
    sp1.output_data = {"response": "Docker는 컨테이너 기술입니다.", "tokens": 150}

with logger.span("tool_call:search_docs", parent_span_id=sp1.span_id) as sp2:
    time.sleep(0.05)  # 검색 시뮬레이션
    sp2.output_data = {"doc_count": 3}

summary = logger.get_trace_summary(trace_id)
print(f"Trace: {summary['trace_id']}")
print(f"총 Span: {summary['total_spans']}, 총 지연: {summary['total_duration_ms']:.0f}ms")
print(f"상태: {summary['status']}")
print(f"실행 흐름: {' -> '.join(summary['operations'])}")
# Trace: tr-a1b2c3d4e5f6
# 총 Span: 2, 총 지연: 152ms
# 상태: success
# 실행 흐름: llm_call -> tool_call:search_docs
```

**로그 레벨 전략**

Agent 로그는 기존 애플리케이션보다 세밀한 레벨 설계가 필요하다. LLM 입출력은 데이터 크기가 크므로, 레벨에 따라 기록하는 정보량을 조절한다.

```python
import logging
from enum import IntEnum

class AgentLogLevel(IntEnum):
    TRACE = 5       # 모든 LLM 입출력 원문 (디버깅 시에만)
    DEBUG = 10      # 각 Span의 입출력 요약
    INFO = 20       # Trace 시작/종료, 주요 이벤트
    WARNING = 30    # 성능 저하, 임계치 초과
    ERROR = 40      # Tool 실패, LLM 오류
    CRITICAL = 50   # 서비스 중단 수준 장애

class AgentLogger:
    """Agent 전용 구조화 로거."""

    def __init__(self, name: str, level: int = AgentLogLevel.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.name = name

        # 구조화 포맷
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        )
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def trace_start(self, trace_id: str, query: str) -> None:
        self.logger.info(json.dumps({
            "event": "trace_start",
            "trace_id": trace_id,
            "query_preview": query[:100],
        }, ensure_ascii=False))

    def span_complete(self, span: Span) -> None:
        log_data = {
            "event": "span_complete",
            "trace_id": span.trace_id,
            "span_id": span.span_id,
            "operation": span.operation,
            "duration_ms": round(span.duration_ms, 2) if span.duration_ms else None,
            "status": span.status,
        }

        if span.status == "error":
            log_data["error"] = span.error
            self.logger.error(json.dumps(log_data, ensure_ascii=False))
        elif span.duration_ms and span.duration_ms > 3000:
            log_data["warning"] = "slow_span"
            self.logger.warning(json.dumps(log_data, ensure_ascii=False))
        else:
            self.logger.info(json.dumps(log_data, ensure_ascii=False))

    def token_usage(self, trace_id: str, model: str, prompt_tokens: int, completion_tokens: int) -> None:
        self.logger.info(json.dumps({
            "event": "token_usage",
            "trace_id": trace_id,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        }, ensure_ascii=False))

    def alert(self, trace_id: str, alert_type: str, message: str) -> None:
        self.logger.error(json.dumps({
            "event": "alert",
            "trace_id": trace_id,
            "alert_type": alert_type,
            "message": message,
        }, ensure_ascii=False))
```

```
# 실행 결과
agent_logger = AgentLogger("qa-agent", level=AgentLogLevel.INFO)

agent_logger.trace_start("tr-abc123", "Docker 컨테이너와 VM의 차이는?")
# 2025-01-15 10:30:00 | INFO     | qa-agent | {"event": "trace_start", "trace_id": "tr-abc123", "query_preview": "Docker 컨테이너와 VM의 차이는?"}

agent_logger.token_usage("tr-abc123", MODEL, prompt_tokens=500, completion_tokens=200)
# 2025-01-15 10:30:01 | INFO     | qa-agent | {"event": "token_usage", "trace_id": "tr-abc123", "model": "moonshotai/kimi-k2", "prompt_tokens": 500, "completion_tokens": 200, "total_tokens": 700}
```

### 예제

Trace 기반 디버깅 워크플로우를 구현한다. 사용자 불만이 접수되었을 때 해당 요청의 전체 실행 흐름을 추적하는 과정이다.

```python
class TraceDebugger:
    """Trace 기반 디버깅 도우미."""

    def __init__(self, trace_logger: TraceLogger):
        self.trace_logger = trace_logger

    def find_bottleneck(self, trace_id: str) -> dict:
        """가장 오래 걸린 Span을 찾아 병목을 식별한다."""
        spans = self.trace_logger.traces.get(trace_id, [])
        if not spans:
            return {"error": "Trace not found"}

        slowest = max(spans, key=lambda s: s.duration_ms or 0)
        total = sum(s.duration_ms or 0 for s in spans)

        return {
            "bottleneck_span": slowest.operation,
            "bottleneck_duration_ms": round(slowest.duration_ms, 2),
            "total_duration_ms": round(total, 2),
            "bottleneck_pct": round((slowest.duration_ms / total) * 100, 1) if total > 0 else 0,
        }

    def find_errors(self, trace_id: str) -> list[dict]:
        """에러가 발생한 Span을 모두 찾는다."""
        spans = self.trace_logger.traces.get(trace_id, [])
        return [
            {
                "span_id": s.span_id,
                "operation": s.operation,
                "error": s.error,
                "duration_ms": round(s.duration_ms, 2) if s.duration_ms else None,
            }
            for s in spans if s.status == "error"
        ]

    def reconstruct_flow(self, trace_id: str) -> str:
        """실행 흐름을 시각적으로 재구성한다."""
        spans = self.trace_logger.traces.get(trace_id, [])
        if not spans:
            return "Trace not found"

        lines = [f"Trace: {trace_id}"]
        for i, span in enumerate(spans):
            prefix = "├──" if i < len(spans) - 1 else "└──"
            status_icon = "OK" if span.status == "success" else "ERR"
            duration = f"{span.duration_ms:.0f}ms" if span.duration_ms else "N/A"
            lines.append(f"  {prefix} [{status_icon}] {span.operation} ({duration})")
            if span.error:
                lines.append(f"  │   Error: {span.error}")

        return "\n".join(lines)

# 디버깅 시나리오
debugger = TraceDebugger(logger)

# 병목 분석
bottleneck = debugger.find_bottleneck(trace_id)
print(f"병목: {bottleneck['bottleneck_span']} ({bottleneck['bottleneck_duration_ms']}ms, 전체의 {bottleneck['bottleneck_pct']}%)")

# 실행 흐름 재구성
print(debugger.reconstruct_flow(trace_id))
```

```
# 실행 결과
병목: llm_call (101.23ms, 전체의 66.5%)
Trace: tr-a1b2c3d4e5f6
  ├── [OK] llm_call (101ms)
  └── [OK] tool_call:search_docs (51ms)
```

### Q&A

**Q: Trace 로그에 LLM 입출력 전문을 기록하면 스토리지 비용이 너무 크지 않나요?**

A: 그렇다. LLM 한 번 호출의 입출력이 수 KB에 달하므로, 모든 요청의 전문을 저장하면 비용이 급증한다. 실무에서는 레벨별로 차등 저장한다. (1) **INFO 레벨**: 요청 메타데이터만 저장 (trace_id, 모델, 토큰 수, 지연 시간). (2) **DEBUG 레벨**: 입출력 요약 (처음 200자 + 해시). (3) **TRACE 레벨**: 전문 저장. TRACE 레벨은 디버깅 시에만 활성화하고, 보존 기간을 7일로 짧게 설정한다. INFO는 90일, DEBUG는 30일이 일반적이다.

**Q: OpenTelemetry 같은 기존 트레이싱 프레임워크를 Agent에도 쓸 수 있나요?**

A: 쓸 수 있고 권장된다. OpenTelemetry는 Span, Trace 개념을 표준화하고 있어 Agent 로깅에도 적합하다. 다만 Agent 특화 정보(토큰 사용량, 프롬프트 해시, 모델 버전 등)는 Custom Attribute로 추가해야 한다. LangSmith, Arize, Weights & Biases 등 LLM 관측(Observability) 전문 도구도 있다. 직접 구축할지 외부 도구를 쓸지는 규모와 예산에 따라 결정한다.

<details>
<summary>퀴즈: Agent가 사용자 질문에 잘못된 답변을 했다는 불만이 접수되었습니다. Trace 로그에서 가장 먼저 확인해야 할 것은 무엇인가요?</summary>

**힌트**: 잘못된 답변의 원인이 검색 단계인지, LLM 생성 단계인지 구분해야 한다.

**정답**: Retrieval(검색) Span을 먼저 확인한다. 검색된 문서가 질문과 관련이 있는지 확인하여 (1) 관련 문서가 검색되지 않았다면 Retrieval 문제 (쿼리 매칭, 인덱스 이슈), (2) 관련 문서가 검색되었는데 답변이 틀렸다면 LLM Generation 문제 (프롬프트, 모델 이슈)로 원인을 분리한다. 이것이 데이터 흐름의 "상류부터 추적하라"는 원칙의 실제 적용이다.
</details>

---

## 개념 2: 모니터링 메트릭 설계

### 개념 설명

**전통적 모니터링과 AI Agent 모니터링의 근본적 차이**

전통적인 웹 서비스 모니터링은 RED 메트릭(Rate, Errors, Duration)이면 충분했다. 요청이 몇 건 들어오고, 몇 건이 실패하고, 얼마나 걸리는지만 알면 서비스 상태를 판단할 수 있었다. 그러나 AI Agent 시스템은 여기에 "품질(Quality)"이라는 완전히 새로운 차원이 추가된다. HTTP 200을 반환했지만 답변이 환각(hallucination)인 경우, 기존 에러율 모니터링으로는 전혀 감지할 수 없다. 이것이 AI Agent 모니터링을 근본적으로 어렵게 만드는 요인이다.

**메트릭 설계의 핵심 원칙: USE와 RED를 넘어서**

인프라 모니터링의 USE(Utilization, Saturation, Errors)와 마이크로서비스의 RED(Rate, Errors, Duration)는 AI Agent에도 기반이 되지만, 추가적인 메트릭 카테고리가 필요하다. 첫째, 토큰 사용량은 비용과 직결되므로 실시간 추적이 필수다. 전통 서비스에서 CPU/메모리에 해당하는 리소스 메트릭이 AI 시스템에서는 토큰으로 대체된다. 둘째, Tool 호출 성공률은 Agent의 기능적 완전성을 나타낸다. 검색 Tool이 실패하면 Agent는 지식 없이 답변하게 되어 품질이 급격히 저하되지만, 에러로 보고되지 않을 수 있다. 셋째, 사용자 만족도는 궁극적인 품질 지표다. 다른 모든 메트릭이 정상이어도 사용자가 불만족하면 서비스에 문제가 있는 것이다.

**비용이라는 새로운 운영 변수**

전통적 서비스에서 요청 하나를 처리하는 비용은 거의 무시할 수 있었다. 서버 비용은 고정적이고 요청량에 따라 선형적으로 증가할 뿐이었다. 반면 AI Agent는 요청마다 LLM API 비용이 직접 발생한다. 복잡한 질문은 여러 번의 LLM 호출과 Tool 사용을 유발하여 단일 요청의 비용이 10배 이상 차이날 수 있다. 이 때문에 비용 메트릭은 단순히 "일간 총비용"을 넘어 "요청당 비용 분포", "모델별 비용 비율", "기능별 비용 기여도"까지 추적해야 한다. 비용 폭주(cost runaway)를 방지하기 위한 실시간 예산 모니터링은 AI 시스템 운영에서 전통 서비스에 없던 필수 요소다.

**Agent 핵심 메트릭 4가지**

| 메트릭 카테고리 | 지표 | 측정 방법 | 임계치 예시 |
|---------------|------|----------|------------|
| **응답 시간** | P50/P95/P99 지연 | Span duration 집계 | P95 < 5초 |
| **토큰 사용량** | 요청당 토큰, 일간 총 토큰 | LLM 응답 메타데이터 | 일 100만 토큰 이내 |
| **Tool 호출** | 호출 성공률, 평균 호출 횟수 | Tool Span 집계 | 성공률 > 95% |
| **사용자 만족도** | 피드백 점수, 재질문 비율 | 사용자 이벤트 수집 | 만족도 > 4.0/5.0 |

이제 이 4가지 메트릭을 수집하고 집계하는 MetricsCollector를 구현해보자.

```python
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict

@dataclass
class MetricPoint:
    """단일 메트릭 관측값."""
    name: str
    value: float
    timestamp: float = field(default_factory=time.time)
    labels: dict = field(default_factory=dict)

class MetricsCollector:
    """Agent 메트릭을 수집하고 집계한다."""

    def __init__(self):
        self._metrics: list[MetricPoint] = []
        self._counters: dict[str, float] = defaultdict(float)
        self._histograms: dict[str, list[float]] = defaultdict(list)

    def record_latency(self, operation: str, duration_ms: float, labels: dict = None) -> None:
        """지연 시간을 히스토그램으로 기록한다."""
        self._histograms[f"latency:{operation}"].append(duration_ms)
        self._metrics.append(MetricPoint(
            name=f"agent_latency_ms",
            value=duration_ms,
            labels={"operation": operation, **(labels or {})},
        ))

    def record_tokens(self, model: str, prompt_tokens: int, completion_tokens: int) -> None:
        """토큰 사용량을 기록한다."""
        total = prompt_tokens + completion_tokens
        self._counters[f"tokens:{model}:prompt"] += prompt_tokens
        self._counters[f"tokens:{model}:completion"] += completion_tokens
        self._counters[f"tokens:{model}:total"] += total
        self._metrics.append(MetricPoint(
            name="agent_tokens_total",
            value=total,
            labels={"model": model},
        ))

    def record_tool_call(self, tool_name: str, success: bool, duration_ms: float) -> None:
        """Tool 호출 결과를 기록한다."""
        status = "success" if success else "failure"
        self._counters[f"tool_calls:{tool_name}:{status}"] += 1
        self._histograms[f"tool_latency:{tool_name}"].append(duration_ms)
        self._metrics.append(MetricPoint(
            name="agent_tool_call",
            value=1,
            labels={"tool": tool_name, "status": status},
        ))

    def record_user_feedback(self, score: float, trace_id: str) -> None:
        """사용자 피드백 점수를 기록한다."""
        self._histograms["user_feedback"].append(score)
        self._metrics.append(MetricPoint(
            name="agent_user_feedback",
            value=score,
            labels={"trace_id": trace_id},
        ))

    def get_percentile(self, metric_key: str, percentile: float) -> float:
        """히스토그램에서 백분위수를 계산한다."""
        values = sorted(self._histograms.get(metric_key, []))
        if not values:
            return 0.0
        idx = int(len(values) * percentile / 100)
        return values[min(idx, len(values) - 1)]

    def tool_success_rate(self, tool_name: str) -> float:
        """특정 Tool의 성공률을 계산한다."""
        success = self._counters.get(f"tool_calls:{tool_name}:success", 0)
        failure = self._counters.get(f"tool_calls:{tool_name}:failure", 0)
        total = success + failure
        return success / total if total > 0 else 0.0

    def summary(self) -> dict:
        """전체 메트릭 요약."""
        return {
            "latency": {
                "p50": self.get_percentile("latency:agent_request", 50),
                "p95": self.get_percentile("latency:agent_request", 95),
                "p99": self.get_percentile("latency:agent_request", 99),
            },
            "tokens": {
                k: v for k, v in self._counters.items() if k.startswith("tokens:")
            },
            "tool_calls": {
                k: v for k, v in self._counters.items() if k.startswith("tool_calls:")
            },
            "user_feedback": {
                "mean": sum(self._histograms.get("user_feedback", [0])) / max(len(self._histograms.get("user_feedback", [1])), 1),
                "count": len(self._histograms.get("user_feedback", [])),
            },
        }
```

```
# 실행 결과
collector = MetricsCollector()

# 요청 처리 시뮬레이션
for i in range(100):
    # 전체 요청 지연
    latency = 1500 + (i % 20) * 100
    collector.record_latency("agent_request", latency)

    # 토큰 사용량
    collector.record_tokens(MODEL, prompt_tokens=500, completion_tokens=200)

    # Tool 호출 (95% 성공)
    import random
    collector.record_tool_call("search_docs", success=random.random() < 0.95, duration_ms=300 + random.random() * 200)
    collector.record_tool_call("calculate", success=random.random() < 0.99, duration_ms=10 + random.random() * 20)

    # 사용자 피드백 (일부만)
    if random.random() < 0.3:
        collector.record_user_feedback(random.uniform(3.0, 5.0), f"tr-{i:04d}")

summary = collector.summary()
print(f"지연 P50: {summary['latency']['p50']:.0f}ms")
print(f"지연 P95: {summary['latency']['p95']:.0f}ms")
print(f"search_docs 성공률: {collector.tool_success_rate('search_docs'):.1%}")
print(f"calculate 성공률: {collector.tool_success_rate('calculate'):.1%}")
print(f"사용자 피드백 평균: {summary['user_feedback']['mean']:.2f}/5.0 ({summary['user_feedback']['count']}건)")
# 지연 P50: 2400ms
# 지연 P95: 3300ms
# search_docs 성공률: 95.0%
# calculate 성공률: 99.0%
# 사용자 피드백 평균: 4.02/5.0 (30건)
```

**비용 메트릭: 토큰 사용량 추적**

Agent 운영에서 비용 관리는 필수다. 모델별, 기능별 토큰 사용량을 추적하여 예산을 관리한다.

```python
@dataclass
class CostTracker:
    """토큰 기반 비용을 추적한다."""

    # 모델별 토큰당 비용 (USD per 1K tokens)
    PRICING = {
        "moonshotai/kimi-k2": {"prompt": 0.0006, "completion": 0.002},
        "openai/gpt-4o": {"prompt": 0.005, "completion": 0.015},
        "openai/gpt-4o-mini": {"prompt": 0.00015, "completion": 0.0006},
        "anthropic/claude-sonnet-4": {"prompt": 0.003, "completion": 0.015},
    }

    def __init__(self, daily_budget_usd: float = 10.0):
        self.daily_budget = daily_budget_usd
        self.daily_usage: dict[str, dict[str, int]] = defaultdict(lambda: {"prompt": 0, "completion": 0})

    def record(self, model: str, prompt_tokens: int, completion_tokens: int) -> dict:
        today = datetime.now().strftime("%Y-%m-%d")
        self.daily_usage[today]["prompt"] += prompt_tokens
        self.daily_usage[today]["completion"] += completion_tokens

        cost = self.calculate_cost(model, prompt_tokens, completion_tokens)
        daily_total = self.get_daily_cost(today, model)

        return {
            "request_cost_usd": round(cost, 6),
            "daily_total_usd": round(daily_total, 4),
            "budget_remaining_usd": round(self.daily_budget - daily_total, 4),
            "budget_used_pct": round(daily_total / self.daily_budget * 100, 1),
        }

    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        pricing = self.PRICING.get(model, {"prompt": 0.001, "completion": 0.003})
        return (prompt_tokens * pricing["prompt"] + completion_tokens * pricing["completion"]) / 1000

    def get_daily_cost(self, date: str, model: str) -> float:
        usage = self.daily_usage.get(date, {"prompt": 0, "completion": 0})
        return self.calculate_cost(model, usage["prompt"], usage["completion"])

    def is_budget_exceeded(self, model: str) -> bool:
        today = datetime.now().strftime("%Y-%m-%d")
        return self.get_daily_cost(today, model) >= self.daily_budget

# 사용 예시
cost_tracker = CostTracker(daily_budget_usd=5.0)

result = cost_tracker.record(MODEL, prompt_tokens=1500, completion_tokens=500)
print(f"요청 비용: ${result['request_cost_usd']}")
print(f"일간 누적: ${result['daily_total_usd']}")
print(f"예산 사용: {result['budget_used_pct']}%")
print(f"잔여 예산: ${result['budget_remaining_usd']}")
```

```
# 실행 결과
요청 비용: $0.0019
일간 누적: $0.0019
예산 사용: 0.0%
잔여 예산: $4.9981
```

### 예제

Prometheus 호환 형식으로 메트릭을 노출하는 Exporter를 구현한다. Grafana에서 수집할 수 있는 형식이다.

```python
class PrometheusExporter:
    """Prometheus 형식으로 메트릭을 노출한다."""

    def __init__(self, collector: MetricsCollector, cost_tracker: CostTracker):
        self.collector = collector
        self.cost_tracker = cost_tracker

    def export(self) -> str:
        """Prometheus scrape 엔드포인트 응답을 생성한다."""
        lines = []

        # 지연 시간 히스토그램
        lines.append("# HELP agent_request_duration_ms Agent request latency in milliseconds")
        lines.append("# TYPE agent_request_duration_ms summary")
        for p in [50, 95, 99]:
            val = self.collector.get_percentile("latency:agent_request", p)
            lines.append(f'agent_request_duration_ms{{quantile="{p/100}"}} {val:.2f}')

        # Tool 호출 카운터
        lines.append("")
        lines.append("# HELP agent_tool_calls_total Total tool call count")
        lines.append("# TYPE agent_tool_calls_total counter")
        for key, value in self.collector._counters.items():
            if key.startswith("tool_calls:"):
                parts = key.split(":")
                tool_name, status = parts[1], parts[2]
                lines.append(f'agent_tool_calls_total{{tool="{tool_name}",status="{status}"}} {int(value)}')

        # 토큰 사용량
        lines.append("")
        lines.append("# HELP agent_tokens_total Total token usage")
        lines.append("# TYPE agent_tokens_total counter")
        for key, value in self.collector._counters.items():
            if key.startswith("tokens:"):
                parts = key.split(":")
                model, token_type = parts[1], parts[2]
                lines.append(f'agent_tokens_total{{model="{model}",type="{token_type}"}} {int(value)}')

        # 비용
        lines.append("")
        lines.append("# HELP agent_daily_cost_usd Daily cost in USD")
        lines.append("# TYPE agent_daily_cost_usd gauge")
        today = datetime.now().strftime("%Y-%m-%d")
        daily_cost = self.cost_tracker.get_daily_cost(today, MODEL)
        lines.append(f'agent_daily_cost_usd{{model="{MODEL}"}} {daily_cost:.6f}')

        # 사용자 피드백
        lines.append("")
        lines.append("# HELP agent_user_feedback_score User feedback score")
        lines.append("# TYPE agent_user_feedback_score gauge")
        feedback = self.collector._histograms.get("user_feedback", [])
        if feedback:
            avg = sum(feedback) / len(feedback)
            lines.append(f'agent_user_feedback_score{{type="mean"}} {avg:.2f}')

        return "\n".join(lines)

exporter = PrometheusExporter(collector, cost_tracker)
print(exporter.export())
```

```
# 실행 결과
# HELP agent_request_duration_ms Agent request latency in milliseconds
# TYPE agent_request_duration_ms summary
agent_request_duration_ms{quantile="0.5"} 2400.00
agent_request_duration_ms{quantile="0.95"} 3300.00
agent_request_duration_ms{quantile="0.99"} 3400.00

# HELP agent_tool_calls_total Total tool call count
# TYPE agent_tool_calls_total counter
agent_tool_calls_total{tool="search_docs",status="success"} 95
agent_tool_calls_total{tool="search_docs",status="failure"} 5
agent_tool_calls_total{tool="calculate",status="success"} 99
agent_tool_calls_total{tool="calculate",status="failure"} 1

# HELP agent_tokens_total Total token usage
# TYPE agent_tokens_total counter
agent_tokens_total{model="moonshotai/kimi-k2",type="total"} 70000

# HELP agent_daily_cost_usd Daily cost in USD
# TYPE agent_daily_cost_usd gauge
agent_daily_cost_usd{model="moonshotai/kimi-k2"} 0.001900

# HELP agent_user_feedback_score User feedback score
# TYPE agent_user_feedback_score gauge
agent_user_feedback_score{type="mean"} 4.02
```

### Q&A

**Q: Agent 모니터링에서 가장 중요한 단일 메트릭은 무엇인가요?**

A: 하나만 골라야 한다면 **사용자 만족도(User Satisfaction)** 이다. 다른 메트릭(지연, 토큰, 에러율)은 모두 "사용자가 만족하는지"를 간접적으로 측정하는 프록시에 불과하다. 지연이 2초여도 답변이 정확하면 만족하고, 지연이 500ms여도 답변이 틀리면 불만이다. 다만 사용자 만족도는 수집이 어렵고 지연이 있으므로(피드백을 주기까지 시간), 실시간 대시보드에는 P95 지연 + Tool 성공률을 주 지표로, 일간 리포트에는 사용자 만족도를 보는 것이 현실적이다.

**Q: Grafana 대시보드에서 어떤 패널을 배치해야 하나요?**

A: 실무에서 검증된 Agent 대시보드 레이아웃은 다음과 같다. **상단 (요약)**: 현재 서비스 상태 (정상/경고/장애), 일간 요청 수, 일간 비용. **중단 (성능)**: 응답 시간 P50/P95 시계열 그래프, Tool 호출 성공률 게이지, 토큰 사용량 시계열. **하단 (품질)**: 사용자 만족도 트렌드, 에러 로그 실시간 피드, Top-5 실패 쿼리 테이블. 핵심은 "한눈에 서비스 건강 상태를 파악"할 수 있어야 한다는 것이다.

<details>
<summary>퀴즈: Agent의 P50 지연이 2초인데 P99 지연이 15초라면, 어떤 문제가 있을 가능성이 높을까요?</summary>

**힌트**: P50과 P99의 차이가 매우 크다는 것은 일부 요청만 극단적으로 느리다는 뜻이다.

**정답**: 일부 요청에서 **Tool 호출 타임아웃** 또는 **LLM 재시도**가 발생하고 있을 가능성이 높다. 가능한 원인: (1) 특정 유형의 질문에서 Tool 호출이 실패하여 재시도가 반복되는 경우, (2) 컨텍스트 윈도우가 큰 요청에서 LLM 응답 시간이 급증하는 경우, (3) 외부 API의 간헐적 지연(cold start 등). P99 지연의 Trace를 샘플링하여 어떤 Span에서 지연이 집중되는지 확인해야 한다.
</details>

---

## 개념 3: 대시보드 설계

### 개념 설명

**대시보드는 왜 "설계"해야 하는가**

대시보드를 단순히 "메트릭을 화면에 보여주는 것"이라고 생각하면 실패한다. 잘못 설계된 대시보드는 정보 과잉(information overload)을 유발하여 오히려 문제 파악을 방해한다. 좋은 대시보드는 "이 화면을 보는 사람이 다음에 무엇을 해야 하는지"를 즉시 판단할 수 있게 해준다. 이를 위해 대시보드는 인지적 부하를 최소화하는 방향으로 설계되어야 한다. 가장 중요한 정보가 가장 먼저 눈에 들어오고, 이상 상태가 즉각적으로 구별되며, 문제가 발생했을 때 원인 추적을 위한 drill-down 경로가 명확해야 한다.

**계층적 대시보드 설계의 원칙: 글랜스 -> 분석 -> 디버깅**

실무에서 검증된 대시보드 설계 패턴은 3계층 구조다. Level 1(글랜스)은 경영진이나 당직자가 10초 안에 "서비스가 정상인가?"를 판단하는 화면으로, 신호등 색상과 핵심 숫자 3-4개만 보여준다. Level 2(분석)는 엔지니어가 "어디가 문제인가?"를 파악하는 화면으로, 시계열 그래프와 Tool별/모델별 세부 메트릭을 제공한다. Level 3(디버깅)은 특정 요청의 Trace를 따라가며 근본 원인을 찾는 화면이다. 이 계층 구조가 중요한 이유는 각 계층의 사용자가 다르기 때문이다. 당직자에게 Trace 상세 정보는 불필요하고, 개발자에게 경영 요약은 도움이 되지 않는다.

**SLI/SLO 기반 대시보드: 주관적 판단을 객관적 기준으로 대체하기**

"서비스가 괜찮은 것 같다"는 주관적 판단은 장애를 놓치게 만든다. SLI(Service Level Indicator)는 서비스 품질을 측정 가능한 숫자로 정의하고, SLO(Service Level Objective)는 그 숫자의 목표치를 설정한다. AI Agent 시스템에서 핵심 SLI는 전통 서비스의 가용성(uptime)을 넘어, 응답 품질 점수, Tool 호출 성공률, 토큰 효율성(답변 품질 대비 소모 토큰)까지 포함해야 한다. SLO를 기반으로 대시보드를 구성하면 "현재 SLO를 달성하고 있는가? Error Budget이 얼마나 남았는가?"라는 명확한 질문에 대시보드가 답할 수 있게 된다. 이 접근법은 Google SRE에서 시작되었으며, AI Agent 운영에서도 그 가치가 동일하게 적용된다.

**대시보드 계층 구조**

```
Level 1: 서비스 헬스 (전체 요약)
├── 현재 상태: 정상 / 경고 / 장애
├── 일간 요청 수, 성공률
├── 일간 비용
└── 핵심 SLI 달성률

Level 2: 성능 분석 (상세 메트릭)
├── 응답 시간 분포 (P50/P95/P99 시계열)
├── Tool 호출 성공률 (Tool별)
├── 토큰 사용량 (모델별, 시간별)
└── 검색 품질 (Recall, 컨텍스트 관련도)

Level 3: 디버깅 (개별 요청 추적)
├── 에러 로그 실시간 피드
├── 느린 요청 Top-N
├── Trace 상세 조회
└── 특정 사용자/세션 추적
```

이 계층 구조를 SLI 기반으로 코드로 구현해보자. 각 SLI에 대해 목표 달성 여부를 자동으로 판단하는 대시보드를 만든다.

```python
from dataclasses import dataclass

@dataclass
class SLI:
    """Service Level Indicator: 서비스 수준 지표."""
    name: str
    description: str
    target: float
    current: float
    unit: str

    @property
    def achieved(self) -> bool:
        return self.current >= self.target

    @property
    def margin(self) -> float:
        return self.current - self.target

class AgentSLIDashboard:
    """Agent SLI를 모니터링하는 대시보드."""

    def __init__(self, collector: MetricsCollector):
        self.collector = collector

    def compute_slis(self) -> list[SLI]:
        """핵심 SLI를 계산한다."""
        return [
            SLI(
                name="응답 시간 P95",
                description="95번째 백분위수 응답 시간이 목표 이내",
                target=5000,
                current=self.collector.get_percentile("latency:agent_request", 95),
                unit="ms (lower is better)",
            ),
            SLI(
                name="Tool 성공률",
                description="Tool 호출 전체 성공률",
                target=95.0,
                current=self._overall_tool_success_rate(),
                unit="% (higher is better)",
            ),
            SLI(
                name="사용자 만족도",
                description="사용자 피드백 평균 점수",
                target=4.0,
                current=self._avg_feedback(),
                unit="/5.0 (higher is better)",
            ),
            SLI(
                name="에러율",
                description="전체 요청 대비 에러 비율",
                target=2.0,  # 2% 이하
                current=self._error_rate(),
                unit="% (lower is better)",
            ),
        ]

    def _overall_tool_success_rate(self) -> float:
        total_success = sum(v for k, v in self.collector._counters.items() if "success" in k and "tool_calls" in k)
        total_failure = sum(v for k, v in self.collector._counters.items() if "failure" in k and "tool_calls" in k)
        total = total_success + total_failure
        return (total_success / total * 100) if total > 0 else 100.0

    def _avg_feedback(self) -> float:
        feedback = self.collector._histograms.get("user_feedback", [])
        return sum(feedback) / len(feedback) if feedback else 0.0

    def _error_rate(self) -> float:
        total_failure = sum(v for k, v in self.collector._counters.items() if "failure" in k and "tool_calls" in k)
        total = sum(v for k, v in self.collector._counters.items() if "tool_calls" in k)
        return (total_failure / total * 100) if total > 0 else 0.0

    def render(self) -> str:
        """대시보드를 텍스트로 렌더링한다."""
        slis = self.compute_slis()
        lines = ["=" * 60, "         Agent Service Health Dashboard", "=" * 60]

        all_achieved = all(s.achieved for s in slis)
        status = "HEALTHY" if all_achieved else "DEGRADED"
        lines.append(f"  Status: [{status}]")
        lines.append("")

        for sli in slis:
            icon = "OK" if sli.achieved else "!!"
            lines.append(f"  [{icon}] {sli.name}")
            lines.append(f"       Target: {sli.target} {sli.unit}")
            lines.append(f"       Current: {sli.current:.2f}")
            lines.append(f"       Margin: {sli.margin:+.2f}")
            lines.append("")

        lines.append("=" * 60)
        return "\n".join(lines)
```

```
# 실행 결과
dashboard = AgentSLIDashboard(collector)
print(dashboard.render())
# ============================================================
#          Agent Service Health Dashboard
# ============================================================
#   Status: [HEALTHY]
#
#   [OK] 응답 시간 P95
#        Target: 5000 ms (lower is better)
#        Current: 3300.00
#        Margin: -1700.00
#
#   [OK] Tool 성공률
#        Target: 95.0 % (higher is better)
#        Current: 97.00
#        Margin: +2.00
#
#   [OK] 사용자 만족도
#        Target: 4.0 /5.0 (higher is better)
#        Current: 4.02
#        Margin: +0.02
#
#   [OK] 에러율
#        Target: 2.0 % (lower is better)
#        Current: 1.50
#        Margin: -0.50
#
# ============================================================
```

**Grafana 대시보드 구성 (JSON 모델)**

```python
def generate_grafana_dashboard_config() -> dict:
    """Grafana 대시보드 JSON 설정을 생성한다."""
    return {
        "dashboard": {
            "title": "AI Agent Monitoring",
            "refresh": "30s",
            "rows": [
                {
                    "title": "Service Health",
                    "panels": [
                        {"type": "stat", "title": "Current Status", "query": "agent_health_status"},
                        {"type": "stat", "title": "Daily Requests", "query": "sum(increase(agent_requests_total[24h]))"},
                        {"type": "stat", "title": "Daily Cost (USD)", "query": "agent_daily_cost_usd"},
                        {"type": "gauge", "title": "SLI Achievement", "query": "agent_sli_achievement_pct"},
                    ],
                },
                {
                    "title": "Performance",
                    "panels": [
                        {"type": "timeseries", "title": "Response Latency (P50/P95)", "queries": [
                            "histogram_quantile(0.5, agent_request_duration_ms)",
                            "histogram_quantile(0.95, agent_request_duration_ms)",
                        ]},
                        {"type": "timeseries", "title": "Tool Success Rate", "query": "rate(agent_tool_calls_total{status='success'}[5m]) / rate(agent_tool_calls_total[5m]) * 100"},
                        {"type": "timeseries", "title": "Token Usage", "query": "rate(agent_tokens_total[1h])"},
                    ],
                },
                {
                    "title": "Quality & Cost",
                    "panels": [
                        {"type": "timeseries", "title": "User Feedback Trend", "query": "avg_over_time(agent_user_feedback_score[1h])"},
                        {"type": "timeseries", "title": "Hourly Cost", "query": "increase(agent_daily_cost_usd[1h])"},
                        {"type": "table", "title": "Top Failed Queries", "query": "topk(10, agent_error_queries)"},
                    ],
                },
            ],
        },
    }

config = generate_grafana_dashboard_config()
print(json.dumps(config["dashboard"]["rows"][0], indent=2, ensure_ascii=False))
```

```
# 실행 결과
{
  "title": "Service Health",
  "panels": [
    {"type": "stat", "title": "Current Status", "query": "agent_health_status"},
    {"type": "stat", "title": "Daily Requests", "query": "sum(increase(agent_requests_total[24h]))"},
    {"type": "stat", "title": "Daily Cost (USD)", "query": "agent_daily_cost_usd"},
    {"type": "gauge", "title": "SLI Achievement", "query": "agent_sli_achievement_pct"}
  ]
}
```

### 예제

이상 징후를 자동 탐지하는 알림 시스템을 구현한다.

```python
@dataclass
class AlertRule:
    """알림 규칙."""
    name: str
    metric: str
    condition: str       # "gt" (greater than) 또는 "lt" (less than)
    threshold: float
    window_minutes: int  # 평가 기간
    severity: str        # "warning" 또는 "critical"
    message_template: str

@dataclass
class Alert:
    """발생한 알림."""
    rule_name: str
    severity: str
    current_value: float
    threshold: float
    message: str
    fired_at: str

class AlertManager:
    """알림 규칙을 관리하고 평가한다."""

    def __init__(self, rules: list[AlertRule]):
        self.rules = rules
        self.fired_alerts: list[Alert] = []

    def evaluate(self, metrics: dict[str, float]) -> list[Alert]:
        """현재 메트릭으로 모든 규칙을 평가한다."""
        new_alerts = []

        for rule in self.rules:
            value = metrics.get(rule.metric)
            if value is None:
                continue

            triggered = False
            if rule.condition == "gt" and value > rule.threshold:
                triggered = True
            elif rule.condition == "lt" and value < rule.threshold:
                triggered = True

            if triggered:
                alert = Alert(
                    rule_name=rule.name,
                    severity=rule.severity,
                    current_value=value,
                    threshold=rule.threshold,
                    message=rule.message_template.format(value=value, threshold=rule.threshold),
                    fired_at=datetime.now().isoformat(),
                )
                new_alerts.append(alert)
                self.fired_alerts.append(alert)

        return new_alerts

    def format_alerts(self, alerts: list[Alert]) -> str:
        """알림을 포맷팅한다 (Slack/PagerDuty 전송용)."""
        if not alerts:
            return "No alerts"

        lines = []
        for alert in alerts:
            severity_tag = "CRITICAL" if alert.severity == "critical" else "WARNING"
            lines.append(f"[{severity_tag}] {alert.rule_name}")
            lines.append(f"  {alert.message}")
            lines.append(f"  Current: {alert.current_value:.2f}, Threshold: {alert.threshold:.2f}")
            lines.append("")
        return "\n".join(lines)

# 알림 규칙 설정
rules = [
    AlertRule("High Latency P95", "latency_p95_ms", "gt", 5000, 5, "critical",
              "P95 응답 시간이 {threshold}ms를 초과했습니다. 현재: {value:.0f}ms"),
    AlertRule("Low Tool Success Rate", "tool_success_rate", "lt", 95.0, 5, "critical",
              "Tool 성공률이 {threshold}% 미만입니다. 현재: {value:.1f}%"),
    AlertRule("High Token Usage", "daily_tokens", "gt", 500000, 60, "warning",
              "일간 토큰 사용량이 {threshold}을 초과했습니다. 현재: {value:.0f}"),
    AlertRule("Low User Satisfaction", "user_satisfaction", "lt", 3.5, 60, "warning",
              "사용자 만족도가 {threshold}점 미만입니다. 현재: {value:.2f}점"),
    AlertRule("Budget Exceeded", "daily_cost_pct", "gt", 80.0, 30, "warning",
              "일간 비용 예산의 {threshold}%를 초과했습니다. 현재: {value:.1f}%"),
]

alert_manager = AlertManager(rules)

# 현재 메트릭으로 알림 평가
current_metrics = {
    "latency_p95_ms": 6200,       # 임계치 5000 초과
    "tool_success_rate": 93.5,    # 임계치 95.0 미달
    "daily_tokens": 350000,       # 정상
    "user_satisfaction": 4.1,     # 정상
    "daily_cost_pct": 45.0,       # 정상
}

alerts = alert_manager.evaluate(current_metrics)
print(alert_manager.format_alerts(alerts))
```

```
# 실행 결과
[CRITICAL] High Latency P95
  P95 응답 시간이 5000ms를 초과했습니다. 현재: 6200ms
  Current: 6200.00, Threshold: 5000.00

[CRITICAL] Low Tool Success Rate
  Tool 성공률이 95.0% 미만입니다. 현재: 93.5%
  Current: 93.50, Threshold: 95.00
```

### Q&A

**Q: 알림이 너무 많이 발생하면(Alert Fatigue) 어떻게 해야 하나요?**

A: Alert Fatigue는 실무에서 가장 흔한 모니터링 문제다. 해결 방법은 세 가지이다. (1) **알림 계층화**: Critical(즉시 대응), Warning(업무 시간 내 확인), Info(일간 리포트에 포함)로 분리하고, Critical만 알림을 보낸다. (2) **Deduplication**: 같은 알림이 5분 내 재발생하면 한 번만 통지한다. (3) **임계치 보정**: 초기 임계치가 너무 민감하면 점진적으로 완화한다. 목표는 "알림 = 즉시 행동이 필요하다"라는 신뢰를 유지하는 것이다.

<details>
<summary>퀴즈: Tool 성공률이 95%에서 갑자기 70%로 떨어졌는데, Agent의 최종 응답 품질은 크게 변하지 않았습니다. 어떻게 설명할 수 있을까요?</summary>

**힌트**: Agent가 Tool 실패에 대응하는 방법을 생각해 보자.

**정답**: Agent에 **재시도(Retry) 로직**이 구현되어 있어, Tool 호출이 실패해도 재시도로 성공하고 있는 것이다. Tool 호출 총 횟수는 증가했지만(실패 + 재시도), 최종 성공률은 유지된다. 다만 이 상황은 (1) 응답 지연이 증가하고 (2) 비용이 증가하며 (3) 외부 서비스에 추가 부하를 주므로, 근본 원인을 해결해야 한다. Tool 성공률과 별도로 "재시도 비율" 메트릭을 추가로 모니터링하는 것이 좋다.
</details>

---

## 개념 4: 장애 유형 분류와 대응 플레이북

### 개념 설명

**왜 AI Agent에는 별도의 장애 분류 체계가 필요한가**

전통적 소프트웨어 장애는 대부분 결정적(deterministic)이다. 같은 입력에 같은 에러가 재현되고, 스택 트레이스를 따라가면 원인을 찾을 수 있다. 반면 AI Agent 시스템의 장애는 여러 겹의 비결정성 위에서 발생한다. LLM의 출력 자체가 확률적이고, Tool 호출 결과는 외부 시스템에 의존하며, RAG 검색 품질은 데이터 상태에 따라 변한다. 더 까다로운 것은 "장애"의 정의 자체가 모호하다는 점이다. HTTP 500이 발생하면 명확한 장애이지만, "Agent가 질문에 대해 정확하지만 불완전한 답변을 한 경우"는 장애인가? 이러한 경계 사례(edge case)가 AI 시스템에서는 일상적으로 발생한다. 따라서 전통적인 "정상/장애" 이분법을 넘어, AI Agent 특유의 장애 유형 분류 체계가 필요하다.

**장애 대응 플레이북이라는 사고방식**

장애가 발생했을 때 가장 위험한 것은 "패닉"이다. 새벽 3시에 알림이 울리면 당직 엔지니어는 무엇을 해야 할지 즉시 떠올릴 수 없다. 플레이북(Playbook)은 "이런 장애가 발생하면 이 순서대로 대응하라"는 사전 정의된 절차서다. 군사 작전이나 항공기 비상 절차에서 차용한 개념으로, 장애 대응에서 개인의 기억이나 경험에 의존하지 않도록 하는 것이 핵심이다. AI Agent 시스템에서는 장애 유형이 전통 시스템보다 다양하므로(LLM 품질 저하, 프롬프트 회귀, 벡터 DB 인덱스 손상 등), 각 유형에 특화된 플레이북이 필요하다.

**자동 대응과 수동 대응의 경계: Runbook Automation의 원칙**

모든 장애 대응을 자동화할 수는 없고, 그래서도 안 된다. 자동화에 적합한 대응은 세 가지 조건을 만족해야 한다. 첫째, 원인이 명확하고 반복적이어야 한다(예: LLM Provider가 다운되면 폴백 모델로 전환). 둘째, 자동 실행의 부작용이 예측 가능해야 한다(폴백 모델의 품질 저하가 허용 범위 내). 셋째, 롤백이 쉬워야 한다(원래 모델로 즉시 복귀 가능). 이 조건을 만족하지 않는 대응 -- 예를 들어 "프롬프트를 수정해야 하는 품질 저하" -- 은 반드시 사람이 판단해야 한다. 실무에서는 "1단계 자동, 2단계 수동"이 표준이다. 1단계에서 서비스 가용성을 자동으로 확보하고(폴백, 캐시, Degraded Mode), 2단계에서 사람이 근본 원인을 분석하고 항구적으로 수정한다. 에스컬레이션 정책은 SLA에서 역산하여 설계하며, 각 단계에서 다음 단계로 넘어가는 시점을 미리 정해둔다.

**장애 유형 분류**

| 장애 유형 | 원인 | 증상 | 긴급도 |
|-----------|------|------|--------|
| **LLM 장애** | Provider API 다운, Rate Limit | 전체 응답 불가 | Critical |
| **LLM 품질 저하** | 모델 업데이트, 프롬프트 회귀 | 응답 품질 하락 | High |
| **Tool 장애** | 외부 API 다운, 스키마 변경 | 특정 기능 불가 | High |
| **데이터 장애** | 벡터 DB 장애, 인덱스 손상 | RAG 검색 실패 | High |
| **비용 장애** | 예산 초과, 토큰 폭주 | 서비스 중단 위험 | Medium |
| **성능 장애** | 트래픽 급증, 리소스 부족 | 응답 지연 급증 | Medium |

이 분류 체계를 코드로 구현하고, 각 유형에 대한 구체적인 플레이북을 정의해보자.

```python
from dataclasses import dataclass, field
from enum import Enum

class IncidentSeverity(Enum):
    CRITICAL = "critical"  # 서비스 중단
    HIGH = "high"          # 주요 기능 장애
    MEDIUM = "medium"      # 성능 저하
    LOW = "low"            # 경미한 이슈

class IncidentCategory(Enum):
    LLM_OUTAGE = "llm_outage"
    LLM_QUALITY = "llm_quality"
    TOOL_FAILURE = "tool_failure"
    DATA_FAILURE = "data_failure"
    COST_OVERRUN = "cost_overrun"
    PERFORMANCE = "performance"

@dataclass
class PlaybookStep:
    """플레이북의 단일 대응 단계."""
    order: int
    action: str
    responsible: str    # "on-call", "team-lead", "infra-team"
    automated: bool     # 자동 실행 가능 여부
    timeout_minutes: int

@dataclass
class IncidentPlaybook:
    """장애 유형별 대응 플레이북."""
    category: IncidentCategory
    severity: IncidentSeverity
    description: str
    detection_signals: list[str]
    steps: list[PlaybookStep]
    escalation_policy: dict

# LLM 장애 플레이북
LLM_OUTAGE_PLAYBOOK = IncidentPlaybook(
    category=IncidentCategory.LLM_OUTAGE,
    severity=IncidentSeverity.CRITICAL,
    description="LLM Provider API가 응답하지 않거나 Rate Limit에 도달한 경우",
    detection_signals=[
        "LLM API 에러율 > 50%",
        "LLM 응답 시간 P95 > 30초",
        "연속 5회 이상 API 호출 실패",
    ],
    steps=[
        PlaybookStep(1, "폴백 모델로 자동 전환 (예: kimi-k2 -> gpt-4o-mini)", "on-call", True, 1),
        PlaybookStep(2, "LLM Provider 상태 페이지 확인", "on-call", False, 5),
        PlaybookStep(3, "캐시된 응답으로 임시 서비스 유지", "on-call", True, 2),
        PlaybookStep(4, "사용자 공지: '일시적 응답 지연' 메시지 표시", "on-call", True, 3),
        PlaybookStep(5, "Provider 복구 시 자동 복귀 트리거 설정", "on-call", True, 5),
    ],
    escalation_policy={
        "5min": "on-call 엔지니어 알림 (Slack + PagerDuty)",
        "15min": "팀 리드 에스컬레이션",
        "30min": "CTO 보고 + 대체 Provider 전환 검토",
    },
)

# Tool 장애 플레이북
TOOL_FAILURE_PLAYBOOK = IncidentPlaybook(
    category=IncidentCategory.TOOL_FAILURE,
    severity=IncidentSeverity.HIGH,
    description="특정 외부 Tool/API가 실패하는 경우",
    detection_signals=[
        "특정 Tool 성공률 < 80%",
        "Tool 응답 시간 P95 > 10초",
        "서킷 브레이커 OPEN 상태",
    ],
    steps=[
        PlaybookStep(1, "서킷 브레이커 상태 확인 및 해당 Tool 격리", "on-call", True, 1),
        PlaybookStep(2, "Tool 없이 동작 가능한 Degraded Mode 활성화", "on-call", True, 2),
        PlaybookStep(3, "외부 API 상태 확인 및 담당팀 연락", "on-call", False, 10),
        PlaybookStep(4, "대체 Tool/API가 있으면 라우팅 전환", "on-call", True, 5),
        PlaybookStep(5, "영향 범위 분석: 해당 Tool을 사용하는 쿼리 비율 확인", "on-call", False, 15),
    ],
    escalation_policy={
        "10min": "on-call 엔지니어 알림",
        "30min": "외부 API 담당팀 연락",
        "60min": "팀 리드 에스컬레이션 + 임시 조치 결정",
    },
)

# 데이터 장애 플레이북
DATA_FAILURE_PLAYBOOK = IncidentPlaybook(
    category=IncidentCategory.DATA_FAILURE,
    severity=IncidentSeverity.HIGH,
    description="벡터 DB 장애 또는 RAG 인덱스 손상",
    detection_signals=[
        "RAG 검색 결과가 0건인 요청 비율 > 20%",
        "Retrieval Recall 급감 (baseline 대비 30% 이상 하락)",
        "벡터 DB 연결 오류",
    ],
    steps=[
        PlaybookStep(1, "벡터 DB 연결 상태 및 헬스체크 확인", "on-call", True, 2),
        PlaybookStep(2, "RAG 우회: LLM 자체 지식 기반 응답으로 Degraded Mode", "on-call", True, 3),
        PlaybookStep(3, "최근 인덱스 변경 이력 확인 (새 문서 추가, 임베딩 모델 변경)", "on-call", False, 10),
        PlaybookStep(4, "백업 인덱스가 있으면 전환", "on-call", True, 5),
        PlaybookStep(5, "인덱스 재구축 필요 시 시작 (백그라운드)", "infra-team", False, 30),
    ],
    escalation_policy={
        "5min": "on-call 엔지니어 알림",
        "15min": "데이터 엔지니어 에스컬레이션",
        "60min": "팀 리드 보고 + 복구 ETA 공유",
    },
)
```

```
# 실행 결과 - 플레이북 조회
def display_playbook(playbook: IncidentPlaybook) -> None:
    print(f"[{playbook.severity.value.upper()}] {playbook.category.value}")
    print(f"설명: {playbook.description}")
    print(f"\n탐지 신호:")
    for signal in playbook.detection_signals:
        print(f"  - {signal}")
    print(f"\n대응 단계:")
    for step in playbook.steps:
        auto = "(자동)" if step.automated else "(수동)"
        print(f"  {step.order}. {auto} {step.action} [{step.responsible}] ~{step.timeout_minutes}분")
    print(f"\n에스컬레이션 정책:")
    for timing, action in playbook.escalation_policy.items():
        print(f"  {timing}: {action}")

display_playbook(LLM_OUTAGE_PLAYBOOK)
# [CRITICAL] llm_outage
# 설명: LLM Provider API가 응답하지 않거나 Rate Limit에 도달한 경우
#
# 탐지 신호:
#   - LLM API 에러율 > 50%
#   - LLM 응답 시간 P95 > 30초
#   - 연속 5회 이상 API 호출 실패
#
# 대응 단계:
#   1. (자동) 폴백 모델로 자동 전환 (예: kimi-k2 -> gpt-4o-mini) [on-call] ~1분
#   2. (수동) LLM Provider 상태 페이지 확인 [on-call] ~5분
#   3. (자동) 캐시된 응답으로 임시 서비스 유지 [on-call] ~2분
#   4. (자동) 사용자 공지: '일시적 응답 지연' 메시지 표시 [on-call] ~3분
#   5. (자동) Provider 복구 시 자동 복귀 트리거 설정 [on-call] ~5분
#
# 에스컬레이션 정책:
#   5min: on-call 엔지니어 알림 (Slack + PagerDuty)
#   15min: 팀 리드 에스컬레이션
#   30min: CTO 보고 + 대체 Provider 전환 검토
```

### 예제

장애 자동 탐지 및 플레이북 실행을 연동하는 Incident Manager를 구현한다.

```python
class IncidentManager:
    """장애를 자동 탐지하고 플레이북을 실행한다."""

    def __init__(self, playbooks: list[IncidentPlaybook], alert_manager: AlertManager):
        self.playbooks = {pb.category: pb for pb in playbooks}
        self.alert_manager = alert_manager
        self.active_incidents: list[dict] = []

    def classify_incident(self, alerts: list[Alert]) -> IncidentCategory | None:
        """알림을 분석하여 장애 유형을 분류한다."""
        alert_names = {a.rule_name for a in alerts}

        if "High Latency P95" in alert_names and any("LLM" in a.message for a in alerts):
            return IncidentCategory.LLM_OUTAGE
        if "Low Tool Success Rate" in alert_names:
            return IncidentCategory.TOOL_FAILURE
        if any("retrieval" in a.rule_name.lower() or "recall" in a.rule_name.lower() for a in alerts):
            return IncidentCategory.DATA_FAILURE
        if "Budget Exceeded" in alert_names:
            return IncidentCategory.COST_OVERRUN
        if "High Latency P95" in alert_names:
            return IncidentCategory.PERFORMANCE

        return None

    def handle_incident(self, alerts: list[Alert]) -> dict:
        """장애를 처리한다: 분류 -> 플레이북 조회 -> 자동 단계 실행."""
        category = self.classify_incident(alerts)
        if category is None:
            return {"status": "no_incident", "alerts": len(alerts)}

        playbook = self.playbooks.get(category)
        if playbook is None:
            return {"status": "no_playbook", "category": category.value}

        # 자동 실행 가능한 단계 실행
        executed_steps = []
        pending_steps = []

        for step in playbook.steps:
            if step.automated:
                # 자동 실행 시뮬레이션
                executed_steps.append({
                    "order": step.order,
                    "action": step.action,
                    "status": "executed",
                })
            else:
                pending_steps.append({
                    "order": step.order,
                    "action": step.action,
                    "responsible": step.responsible,
                    "status": "pending_manual",
                })

        incident = {
            "id": f"INC-{datetime.now().strftime('%Y%m%d%H%M')}",
            "category": category.value,
            "severity": playbook.severity.value,
            "triggered_at": datetime.now().isoformat(),
            "alerts": [a.rule_name for a in alerts],
            "auto_executed": executed_steps,
            "pending_manual": pending_steps,
            "escalation": playbook.escalation_policy,
        }
        self.active_incidents.append(incident)
        return incident

# 실행 시나리오: Tool 장애 발생
incident_manager = IncidentManager(
    playbooks=[LLM_OUTAGE_PLAYBOOK, TOOL_FAILURE_PLAYBOOK, DATA_FAILURE_PLAYBOOK],
    alert_manager=alert_manager,
)

# 이전에 발생한 알림으로 장애 처리
result = incident_manager.handle_incident(alerts)

print(f"장애 ID: {result['id']}")
print(f"유형: {result['category']}, 긴급도: {result['severity']}")
print(f"\n자동 실행된 단계:")
for step in result["auto_executed"]:
    print(f"  {step['order']}. {step['action']} -> {step['status']}")
print(f"\n수동 대응 필요:")
for step in result["pending_manual"]:
    print(f"  {step['order']}. {step['action']} [{step['responsible']}]")
```

```
# 실행 결과
장애 ID: INC-202501151035
유형: tool_failure, 긴급도: high

자동 실행된 단계:
  1. 서킷 브레이커 상태 확인 및 해당 Tool 격리 -> executed
  2. Tool 없이 동작 가능한 Degraded Mode 활성화 -> executed
  4. 대체 Tool/API가 있으면 라우팅 전환 -> executed

수동 대응 필요:
  3. 외부 API 상태 확인 및 담당팀 연락 [on-call]
  5. 영향 범위 분석: 해당 Tool을 사용하는 쿼리 비율 확인 [on-call]
```

**LLM 폴백 체인**

LLM 장애 시 대체 모델로 자동 전환하는 폴백 체인을 구현한다.

```python
class LLMFallbackChain:
    """LLM 장애 시 대체 모델로 자동 전환한다."""

    def __init__(self, models: list[dict]):
        """
        models: [{"name": "moonshotai/kimi-k2", "priority": 1, "timeout_ms": 10000}, ...]
        """
        self.models = sorted(models, key=lambda m: m["priority"])
        self._failures: dict[str, int] = defaultdict(int)
        self._circuit_open: dict[str, float] = {}

    def call(self, messages: list[dict], temperature: float = 0) -> dict:
        """폴백 체인을 순회하며 첫 번째 성공하는 모델의 응답을 반환한다."""
        errors = []

        for model_config in self.models:
            model_name = model_config["name"]

            # 서킷 브레이커 확인
            if model_name in self._circuit_open:
                if time.time() < self._circuit_open[model_name]:
                    errors.append(f"{model_name}: circuit open")
                    continue
                else:
                    del self._circuit_open[model_name]

            try:
                start = time.time()
                resp = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=temperature,
                    timeout=model_config.get("timeout_ms", 10000) / 1000,
                )
                elapsed = (time.time() - start) * 1000

                self._failures[model_name] = 0
                return {
                    "model": model_name,
                    "response": resp.choices[0].message.content,
                    "latency_ms": elapsed,
                    "fallback_used": model_name != self.models[0]["name"],
                }
            except Exception as e:
                self._failures[model_name] += 1
                errors.append(f"{model_name}: {str(e)[:100]}")

                if self._failures[model_name] >= 3:
                    self._circuit_open[model_name] = time.time() + 60

        raise RuntimeError(f"모든 모델 실패: {errors}")

# 폴백 체인 설정
fallback_chain = LLMFallbackChain(models=[
    {"name": "moonshotai/kimi-k2", "priority": 1, "timeout_ms": 10000},
    {"name": "openai/gpt-4o-mini", "priority": 2, "timeout_ms": 8000},
    {"name": "anthropic/claude-sonnet-4", "priority": 3, "timeout_ms": 15000},
])
```

### Q&A

**Q: 모든 장애에 대해 자동 대응을 구현해야 하나요?**

A: 아니다. 자동 대응은 (1) 원인이 명확하고, (2) 대응 방법이 정형화되어 있으며, (3) 자동 실행 시 부작용이 적은 경우에만 적용한다. 예를 들어, LLM 장애 시 폴백 모델 전환은 자동화에 적합하지만, "프롬프트 품질 저하"는 원인이 불분명하므로 수동 분석이 필요하다. 실무 원칙은 **"1단계는 자동, 2단계부터 사람"** 이다. 1단계에서 서비스 가용성을 확보하고, 근본 원인 분석과 항구적 수정은 사람이 판단한다.

**Q: 에스컬레이션 정책에서 시간 기준은 어떻게 정하나요?**

A: SLA(Service Level Agreement)에서 역산한다. 예를 들어 "장애 발생 후 1시간 이내 복구"가 SLA라면: (1) 5분: 자동 탐지 + 1차 대응 시작, (2) 15분: 자동 대응 실패 시 팀 리드 에스컬레이션, (3) 30분: 여전히 미해결 시 상위 에스컬레이션. 핵심은 "각 단계에서 다음 단계로 넘어가기까지 충분한 대응 시간을 주되, SLA를 초과하지 않는 것"이다. 야간/주말에는 자동 대응 비율을 높이고 에스컬레이션 기준을 완화하는 것이 일반적이다.

<details>
<summary>퀴즈: Agent의 LLM Provider가 갑자기 응답을 반환하지만, 모든 응답이 비어있습니다(empty string). 이 장애는 어떤 유형에 해당하며, 기존 모니터링으로 탐지할 수 있을까요?</summary>

**힌트**: HTTP 상태 코드는 200(성공)이지만 내용이 비어있는 경우를 생각해보자.

**정답**: **LLM 품질 저하(LLM_QUALITY)** 유형이다. 기존 에러율 모니터링(HTTP 500 감시)으로는 탐지할 수 없다. 왜냐하면 API 호출 자체는 성공(200)이기 때문이다. 이를 탐지하려면 (1) 응답 길이(completion_tokens) 모니터링 -- 갑자기 0에 가까워지면 알림, (2) 응답 품질 점수 모니터링 -- LLM-as-a-Judge로 주기적 품질 체크, (3) 사용자 만족도 급감 감시가 필요하다. "API 성공 = 서비스 정상"이라는 가정은 LLM 시스템에서 통하지 않는다.
</details>

---

## 실습

### 실습 1: Agent 로그 시스템 구축 및 대시보드 설계
- **연관 학습 목표**: 학습 목표 1, 2
- **실습 목적**: 구조화된 Trace 로그 시스템을 구축하고 Prometheus/Grafana 기반 모니터링 대시보드를 설계한다
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 40분
- **선행 조건**: Python 기본, Day4 Session1 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

#### 실습 요구사항

1. **Trace 로그 시스템 구현 (15분)**
   - `TraceLogger`를 구현하고 Agent 요청의 전체 실행 흐름을 기록하라
   - 최소 3개 Span(LLM 호출, Tool 호출, RAG 검색)을 포함하라
   - `TraceDebugger`로 병목 분석과 에러 추적을 실행하라

2. **메트릭 수집기 구현 (15분)**
   - `MetricsCollector`를 구현하여 4가지 핵심 메트릭을 수집하라
   - 100건의 시뮬레이션 요청을 처리하고 P50/P95 지연을 계산하라
   - `CostTracker`를 추가하여 일간 비용을 추적하라

3. **대시보드 설계 (10분)**
   - `AgentSLIDashboard`로 SLI 현황을 출력하라
   - `PrometheusExporter`로 Prometheus 형식 메트릭을 생성하라
   - Grafana 대시보드 레이아웃(패널 배치)을 문서화하라

#### 기대 산출물
```
monitoring/
  trace_logger.py         # Trace 로그 시스템
  metrics_collector.py    # 메트릭 수집기
  prometheus_exporter.py  # Prometheus 형식 메트릭
  dashboard_design.md     # 대시보드 설계 문서
```

---

### 실습 2: 장애 대응 플레이북 및 자동화 시스템 구축
- **연관 학습 목표**: 학습 목표 2, 3
- **실습 목적**: Agent 장애 유형별 대응 플레이북을 작성하고 자동 탐지/대응 시스템을 구현한다
- **실습 유형**: 코드 작성
- **난이도**: 심화
- **예상 소요 시간**: 50분
- **선행 조건**: 실습 1 완료, OpenRouter API 키 설정
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

#### 실습 요구사항

1. **알림 규칙 설정 (10분)**
   - `AlertManager`에 최소 5개 알림 규칙을 등록하라
   - 각 규칙의 임계치와 심각도를 설정하라
   - 시뮬레이션 메트릭으로 알림 발생을 테스트하라

2. **장애 플레이북 작성 (20분)**
   - LLM 장애, Tool 장애, 데이터 장애 3가지 플레이북을 작성하라
   - 각 플레이북에 자동 실행 단계와 수동 대응 단계를 구분하라
   - 에스컬레이션 정책을 시간 기반으로 설계하라

3. **LLM 폴백 체인 구현 (20분)**
   - `LLMFallbackChain`을 구현하여 3개 모델 간 자동 전환을 구현하라
   - 1차 모델 장애 시 2차 모델로 전환하는 시나리오를 테스트하라
   - `IncidentManager`와 연동하여 장애 탐지 -> 플레이북 실행 -> 폴백 전환의 전체 흐름을 검증하라

#### 기대 산출물
```
incident_response/
  alert_rules.py           # 알림 규칙 설정
  playbooks.py             # 장애 대응 플레이북
  llm_fallback.py          # LLM 폴백 체인
  incident_manager.py      # 장애 자동 대응 시스템
  incident_test_report.md  # 장애 시뮬레이션 결과
```

---

## 핵심 정리
- Agent 로그는 **Trace ID 기반 구조화 로깅**으로 설계하고, 레벨별로 기록 정보량을 차등 관리한다(INFO=메타데이터, TRACE=전문)
- 핵심 모니터링 메트릭은 **응답 시간**, **토큰 사용량**, **Tool 호출 성공률**, **사용자 만족도** 4가지이며, Prometheus/Grafana로 시각화한다
- 대시보드는 **3계층**(서비스 헬스 -> 성능 분석 -> 디버깅)으로 구성하고, SLI 기반으로 서비스 상태를 한눈에 파악할 수 있어야 한다
- 장애는 **LLM/Tool/데이터/비용/성능** 유형으로 분류하고, 각 유형별 **대응 플레이북**을 사전에 준비한다
- **에스컬레이션 정책**은 SLA에서 역산하며, "1단계 자동 대응 + 2단계 수동 분석"이 실무 표준이다
