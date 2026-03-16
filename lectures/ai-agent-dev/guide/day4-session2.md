# Prompt · RAG · Tool 성능 개선 전략

## 학습 목표
1. 프롬프트 버전 관리와 A/B 테스트를 설계하여 체계적인 프롬프트 최적화 파이프라인을 구축할 수 있다
2. RAG 검색 품질 향상, 컨텍스트 최적화, 캐싱 전략을 적용하여 RAG 성능을 개선할 수 있다
3. Tool 호출 지연 최소화, 병렬 호출, 결과 캐싱을 통해 Agent 전체 응답 속도를 최적화할 수 있다

---

## 개념 1: 프롬프트 최적화 전략

### 개념 설명

**왜 이것이 중요한가**: 프롬프트는 Agent 성능의 가장 직접적인 레버다. 하지만 체계적인 관리 없이 프롬프트를 수정하면 "어제까지 잘 되던 것이 오늘 갑자기 안 된다"는 회귀(regression)가 발생한다. 프롬프트 최적화가 어려운 근본적인 이유는 **변경의 영향을 사전에 예측할 수 없다**는 점이다. 전통 코드에서는 타입 시스템과 컴파일러가 변경의 영향 범위를 알려주지만, 프롬프트 변경은 LLM의 비결정적 특성과 맞물려 예상치 못한 부작용을 일으킨다.

**핵심 원리**: "컨텍스트에 없는 내용은 답변하지 마세요"라는 규칙 하나를 추가했을 때, 할루시네이션은 줄어들지만 특정 유형의 질문에서 과도하게 보수적인 답변("확인할 수 없습니다")이 급증할 수 있다. 이런 트레이드오프를 사전에 파악하려면 **체계적인 A/B 테스트**가 필수적이다. A/B 테스트의 핵심은 기존 프롬프트(control)와 새 프롬프트(treatment)를 동시에 운영하면서 실제 트래픽의 일부를 새 프롬프트로 라우팅하여 성과를 비교하는 것이다. 이때 반드시 **사용자 ID 기반의 결정론적 할당**을 사용해야 한다. 해시 함수로 동일 사용자를 항상 같은 variant에 배정하여 경험의 일관성을 보장한다.

**실무에서의 의미**: 프롬프트 최적화는 세 가지 축으로 접근한다.

| 축 | 목적 | 핵심 기법 |
|------|------|-----------|
| **버전 관리** | 변경 이력 추적, 롤백 가능 | Git 기반 프롬프트 저장소, 시맨틱 버저닝 |
| **A/B 테스트** | 개선 효과를 정량적으로 검증 | 트래픽 분할, 통계적 유의성 검정 |
| **프롬프트 체이닝** | 복잡한 작업을 단계별로 분해 | 단계별 프롬프트 연결, 중간 결과 검증 |

**다른 접근법과의 비교**: 또 하나의 강력한 기법은 **프롬프트 체이닝(Prompt Chaining)** 이다. 하나의 복잡한 프롬프트로 "분석 + 판단 + 실행"을 한꺼번에 요구하면 품질이 떨어지지만, 각 단계를 분리하면 중간 결과를 검증하고 보정할 수 있다. 다만 체이닝은 LLM 호출 횟수와 지연이 증가하므로, 단일 프롬프트 품질이 80% 미만일 때 검토하는 것이 실무 기준이다.

다음은 프롬프트 버전 관리와 A/B 테스트를 결합한 시스템이다:

```python
import os
import json
import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

@dataclass
class PromptVersion:
    version: str           # 시맨틱 버전 (e.g., "1.2.0")
    template: str          # 프롬프트 템플릿
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def content_hash(self) -> str:
        return hashlib.sha256(self.template.encode()).hexdigest()[:12]

class PromptRegistry:
    """프롬프트 버전을 중앙에서 관리하는 레지스트리."""

    def __init__(self):
        self._prompts: dict[str, dict[str, PromptVersion]] = {}
        self._active: dict[str, str] = {}

    def register(self, name: str, prompt: PromptVersion) -> None:
        if name not in self._prompts:
            self._prompts[name] = {}
        self._prompts[name][prompt.version] = prompt
        if name not in self._active:
            self._active[name] = prompt.version

    def activate(self, name: str, version: str) -> None:
        if name not in self._prompts or version not in self._prompts[name]:
            raise ValueError(f"Prompt {name}@{version} not found")
        self._active[name] = version

    def get_active(self, name: str) -> PromptVersion:
        version = self._active.get(name)
        if not version:
            raise ValueError(f"No active prompt for {name}")
        return self._prompts[name][version]

    def diff(self, name: str, v1: str, v2: str) -> dict:
        """두 버전 간의 변경 여부를 비교한다."""
        p1, p2 = self._prompts[name][v1], self._prompts[name][v2]
        return {"changed": p1.content_hash != p2.content_hash,
                "description": p2.description}
```

`PromptRegistry`는 프롬프트를 이름과 버전으로 관리한다. `activate()`로 특정 버전을 활성화하고, `diff()`로 두 버전 간 변경 여부를 비교한다. 이를 Git 저장소와 연동하면 프롬프트 변경 이력을 완전히 추적할 수 있다.

**A/B 테스트 시스템**

```python
import random

class PromptABTester:
    """프롬프트 A/B 테스트를 관리한다."""

    def __init__(self, registry: PromptRegistry, prompt_name: str,
                 control_version: str, treatment_version: str, traffic_ratio: float = 0.3):
        self.registry = registry
        self.prompt_name = prompt_name
        self.control_version = control_version
        self.treatment_version = treatment_version
        self.traffic_ratio = traffic_ratio
        self.results: dict[str, list[dict]] = {"control": [], "treatment": []}

    def assign_variant(self, user_id: str) -> str:
        """사용자 ID 기반 결정론적 할당."""
        hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        return "treatment" if (hash_val % 100) < (self.traffic_ratio * 100) else "control"

    def get_prompt(self, user_id: str) -> tuple[str, PromptVersion]:
        variant = self.assign_variant(user_id)
        version = self.treatment_version if variant == "treatment" else self.control_version
        return variant, self.registry._prompts[self.prompt_name][version]

    def record_result(self, variant: str, score: float, latency_ms: float) -> None:
        self.results[variant].append({"score": score, "latency_ms": latency_ms})

    def analyze(self) -> dict:
        """A/B 테스트 결과를 분석한다."""
        summary = {}
        for variant in ["control", "treatment"]:
            data = self.results[variant]
            if data:
                scores = [d["score"] for d in data]
                summary[variant] = {
                    "count": len(data),
                    "avg_score": round(sum(scores) / len(scores), 3),
                }
        if summary.get("control") and summary.get("treatment"):
            improvement = summary["treatment"]["avg_score"] - summary["control"]["avg_score"]
            summary["improvement"] = round(improvement, 3)
            summary["winner"] = "treatment" if improvement > 0 else "control"
        return summary
```

`PromptABTester`는 사용자 ID의 해시 값으로 variant를 결정론적으로 할당한다. 동일 사용자는 항상 같은 variant를 받으므로 경험의 일관성이 보장된다. `analyze()`는 양쪽의 평균 점수를 비교하여 승자를 판정한다.

### 예제

프롬프트 체이닝으로 복잡한 고객 문의를 단계별로 처리하는 파이프라인을 구현한다.

```python
class PromptChain:
    """프롬프트 체이닝: 복잡한 작업을 단계별로 분해한다."""

    def __init__(self, steps: list[dict]):
        self.steps = steps  # [{"name": str, "template": str}, ...]

    def execute(self, initial_input: str) -> dict:
        context = {"input": initial_input}
        results = []

        for step in self.steps:
            prompt = step["template"].format(**context)
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            result = resp.choices[0].message.content
            context[step["name"]] = result
            results.append({"step": step["name"], "output_preview": result[:100]})
        return {"steps": results, "final_output": result}

# 사용 예시
chain = PromptChain(steps=[
    {"name": "classify", "template": "다음 고객 문의를 분류하세요(환불/배송/기타): {input}"},
    {"name": "extract", "template": "문의: {input}\n분류: {classify}\n핵심 정보(주문번호, 날짜, 금액)를 추출하세요."},
    {"name": "respond", "template": "분류: {classify}\n정보: {extract}\n고객에게 친절한 답변을 작성하세요."},
])
```

체이닝의 핵심은 각 단계의 출력이 다음 단계의 입력 컨텍스트에 누적된다는 것이다. 분류 -> 정보 추출 -> 응답 생성으로 분리하면 각 단계를 독립적으로 검증하고 개선할 수 있다. 단일 프롬프트로 모든 것을 처리하면 어느 단계에서 품질이 떨어지는지 파악할 수 없다.

### Q&A

**Q: 프롬프트 A/B 테스트에서 통계적 유의성은 어떻게 확보하나요?**

A: 최소 샘플 크기를 사전에 계산해야 한다. 일반적으로 검출하고자 하는 효과 크기(예: 5% 개선)와 원하는 유의수준(p < 0.05)에 따라 결정한다. 실무에서는 최소 100건 이상의 요청을 각 variant에 할당하고, 두 그룹의 점수 차이에 대해 t-test를 수행한다. 트래픽이 적은 서비스에서는 베이지안 A/B 테스트가 더 적합한데, 적은 샘플로도 의사결정을 내릴 수 있기 때문이다.

<details>
<summary>퀴즈: 프롬프트 체이닝에서 "분류 -> 추출 -> 응답"을 3단계로 분리하는 것과 단일 프롬프트로 처리하는 것의 트레이드오프는 무엇인가요?</summary>

**힌트**: LLM 호출 횟수, 지연 시간, 디버깅 용이성의 관점에서 생각해 보자.

**정답**: 체이닝의 장점은 (1) 각 단계를 독립적으로 검증/개선할 수 있고, (2) 중간 결과가 잘못되면 즉시 발견할 수 있으며, (3) 각 단계에 다른 모델/temperature를 적용할 수 있다. 단점은 (1) LLM 호출이 3배로 늘어 비용과 지연이 증가하고, (2) 단계 간 컨텍스트 전달에서 정보 손실이 발생할 수 있다. 단일 프롬프트의 품질이 80% 이상이면 체이닝이 불필요하고, 미만이면 체이닝을 고려하는 것이 실무 기준이다.
</details>

---

## 개념 2: RAG 성능 개선

### 개념 설명

**왜 이것이 중요한가**: RAG(Retrieval-Augmented Generation)의 성능은 "검색 품질"에 결정적으로 의존한다. 아무리 강력한 LLM이라도 잘못된 문서를 검색하면 정확한 답변을 생성할 수 없다. RAG 성능 개선의 80%는 검색 품질 향상에서 나온다는 것이 실무 경험칙이다.

**핵심 원리**: 검색 품질을 높이는 세 가지 핵심 전략이 있다.

- **Hybrid Search(하이브리드 검색)**: BM25(키워드 매칭)와 Semantic Search(의미 유사도)를 결합한다. "Docker 컨테이너 포트 포워딩"처럼 기술 용어가 포함된 질문은 BM25가 강하고, "프로그램을 격리해서 실행하는 방법"처럼 개념적 질문은 Semantic Search가 강하다. 둘을 결합하면 양쪽의 강점을 취할 수 있다.
- **Query Expansion(쿼리 확장)**: 사용자의 원본 쿼리를 LLM으로 다각도 확장하여 검색 재현율(recall)을 높인다. "Docker 네트워킹"이라는 쿼리를 "Docker 컨테이너 간 통신", "Docker bridge network" 등으로 확장하면 단일 쿼리로는 놓칠 수 있는 관련 문서를 추가로 검색할 수 있다.
- **Context Optimization(컨텍스트 최적화)**: 검색된 문서를 그대로 LLM에 전달하면 토큰 낭비와 노이즈가 발생한다. 핵심 정보만 추출하여 압축하면 비용을 절감하면서도 답변 품질을 유지할 수 있다.

**실무에서의 의미**: Hybrid Search에서 BM25와 Semantic의 가중치 비율은 도메인에 따라 조정해야 한다. 기술 문서 검색에서는 BM25 비중을 높이고(0.6:0.4), 일반 Q&A에서는 Semantic 비중을 높이는(0.3:0.7) 것이 경험적으로 효과적이다. 가중치는 Golden Test Set으로 최적 비율을 탐색한다.

**다른 접근법과의 비교**: 순수 Semantic Search만 사용하는 팀도 있지만, 이 방식은 고유명사나 코드 스니펫처럼 정확한 매칭이 필요한 경우에 취약하다. 반대로 BM25만 사용하면 의미적으로 관련 있지만 표현이 다른 문서를 놓친다. Hybrid가 실무에서 가장 안정적인 성능을 보이는 이유는 두 방식의 약점이 서로 상보적이기 때문이다.

다음은 Hybrid Search를 구현한 코드이다:

```python
import os
import math
import re
from dataclasses import dataclass
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

@dataclass
class Document:
    id: str
    content: str
    metadata: dict = None

class HybridSearcher:
    """BM25 + Semantic Search를 결합한 하이브리드 검색기."""

    def __init__(self, documents: list[Document], bm25_weight: float = 0.4):
        self.documents = documents
        self.bm25_weight = bm25_weight
        self.semantic_weight = 1.0 - bm25_weight
        self._build_bm25_index()

    def _build_bm25_index(self):
        """BM25 인덱스를 구축한다."""
        self.doc_freqs: dict[str, int] = {}
        self.doc_tokens: list[list[str]] = []
        self.avg_dl = 0.0

        for doc in self.documents:
            tokens = doc.content.lower().split()
            self.doc_tokens.append(tokens)
            self.avg_dl += len(tokens)
            for token in set(tokens):
                self.doc_freqs[token] = self.doc_freqs.get(token, 0) + 1
        self.avg_dl /= max(len(self.documents), 1)

    def _bm25_score(self, query: str, doc_idx: int, k1: float = 1.5, b: float = 0.75) -> float:
        tokens = self.doc_tokens[doc_idx]
        query_terms = query.lower().split()
        n = len(self.documents)
        score = 0.0
        for term in query_terms:
            df = self.doc_freqs.get(term, 0)
            if df == 0:
                continue
            idf = math.log((n - df + 0.5) / (df + 0.5) + 1)
            tf = tokens.count(term)
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * len(tokens) / self.avg_dl)
            score += idf * numerator / denominator
        return score

    def _semantic_score(self, query: str, doc: Document) -> float:
        """간단한 토큰 겹침 기반 유사도 (실무에서는 임베딩 모델 사용)."""
        q_tokens = set(query.lower().split())
        d_tokens = set(doc.content.lower().split())
        if not q_tokens or not d_tokens:
            return 0.0
        return len(q_tokens & d_tokens) / len(q_tokens | d_tokens)

    def search(self, query: str, top_k: int = 3) -> list[tuple[float, Document]]:
        """Hybrid 검색을 수행한다."""
        scores = []
        for i, doc in enumerate(self.documents):
            bm25 = self._bm25_score(query, i)
            semantic = self._semantic_score(query, doc)
            combined = self.bm25_weight * bm25 + self.semantic_weight * semantic
            scores.append((combined, doc))
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:top_k]
```

`HybridSearcher`는 BM25와 Semantic Score를 가중 합산한다. 실무에서는 `_semantic_score`를 임베딩 모델(e.g., `text-embedding-3-small`)의 코사인 유사도로 교체한다. `bm25_weight` 파라미터로 두 방식의 비중을 조절할 수 있으며, Golden Test Set으로 최적 비율을 탐색한다.

### 예제

쿼리 확장과 시맨틱 캐시를 결합한 고급 RAG 파이프라인을 구현한다.

```python
import hashlib
import time

class QueryExpander:
    """LLM을 활용한 쿼리 확장."""

    def expand(self, query: str, n_expansions: int = 3) -> list[str]:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": (
                f"다음 검색 쿼리를 {n_expansions}가지 다른 표현으로 변환하세요.\n"
                f"원본: {query}\nJSON: {{\"expansions\": [\"표현1\", ...]}}"
            )}],
            response_format={"type": "json_object"}, temperature=0.3,
        )
        import json
        result = json.loads(resp.choices[0].message.content)
        return [query] + result.get("expansions", [])

class SemanticCache:
    """의미적으로 유사한 쿼리의 결과를 캐싱한다."""

    def __init__(self, ttl_seconds: int = 3600):
        self.cache: dict[str, dict] = {}
        self.ttl = ttl_seconds

    def _normalize(self, query: str) -> str:
        return re.sub(r'\s+', ' ', query.lower().strip())

    def get(self, query: str) -> dict | None:
        key = self._normalize(query)
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry["timestamp"] < self.ttl:
                return entry["result"]
            del self.cache[key]
        return None

    def put(self, query: str, result: dict) -> None:
        key = self._normalize(query)
        self.cache[key] = {"result": result, "timestamp": time.time()}

    @property
    def hit_rate(self) -> str:
        return f"캐시 항목 수: {len(self.cache)}"

class OptimizedRAGPipeline:
    """쿼리 확장 + 하이브리드 검색 + 캐시를 결합한 RAG 파이프라인."""

    def __init__(self, searcher: HybridSearcher):
        self.searcher = searcher
        self.expander = QueryExpander()
        self.cache = SemanticCache()

    def query(self, user_query: str, use_cache: bool = True) -> dict:
        if use_cache:
            cached = self.cache.get(user_query)
            if cached:
                return {**cached, "from_cache": True}

        expanded = self.expander.expand(user_query)
        all_results = []
        seen_ids = set()
        for q in expanded:
            for score, doc in self.searcher.search(q, top_k=3):
                if doc.id not in seen_ids:
                    all_results.append((score, doc))
                    seen_ids.add(doc.id)

        all_results.sort(key=lambda x: x[0], reverse=True)
        top_docs = [doc.content for _, doc in all_results[:3]]

        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": (
                f"컨텍스트:\n{'---'.join(top_docs)}\n\n질문: {user_query}\n"
                "컨텍스트에 기반하여 답변하세요."
            )}], temperature=0,
        )
        result = {"answer": resp.choices[0].message.content,
                  "sources": [doc.id for _, doc in all_results[:3]],
                  "expanded_queries": expanded, "from_cache": False}
        if use_cache:
            self.cache.put(user_query, result)
        return result
```

이 파이프라인은 세 가지 최적화를 결합한다. (1) 쿼리 확장으로 검색 재현율을 높이고, (2) 하이브리드 검색으로 정밀도를 확보하며, (3) 시맨틱 캐시로 동일/유사 쿼리의 반복 처리 비용을 제거한다. 캐시 미스 시에만 LLM 호출이 발생하므로, 반복 쿼리가 많은 서비스에서 비용을 크게 절감할 수 있다.

### Q&A

**Q: Hybrid Search에서 BM25와 Semantic의 최적 가중치는 어떻게 찾나요?**

A: Golden Test Set의 검색 관련 테스트 케이스를 활용한다. BM25 가중치를 0.0에서 1.0까지 0.1 단위로 변화시키면서 검색 결과의 Recall@K와 NDCG를 측정한다. 도메인에 따라 최적 비율이 다르므로 일반적인 정답은 없지만, 기술 문서는 BM25를 높이고(0.5~0.6), 일반 Q&A는 Semantic을 높이는(0.6~0.7) 경향이 있다. 중요한 것은 이 비율을 한 번 정하고 끝내는 것이 아니라, 문서 코퍼스가 변경될 때마다 재검증하는 것이다.

<details>
<summary>퀴즈: 순수 Semantic Search만 사용할 때 "kubectl apply -f deployment.yaml" 같은 명령어 검색이 잘 안 되는 이유는 무엇인가요?</summary>

**힌트**: 임베딩 모델이 코드/명령어를 어떻게 처리하는지 생각해 보자.

**정답**: 임베딩 모델은 자연어의 의미를 벡터로 변환하도록 학습되었기 때문에, 코드나 CLI 명령어 같은 구조화된 텍스트의 토큰 수준 정보를 잘 포착하지 못한다. "kubectl"이라는 정확한 키워드 매칭이 필요한 경우, BM25가 훨씬 효과적이다. 이것이 기술 문서 검색에서 Hybrid Search가 필수인 이유이며, 특히 코드 스니펫, 설정 파일, 오류 메시지 검색에서 BM25의 비중을 높여야 한다.
</details>

---

## 개념 3: Tool 성능 개선

### 개념 설명

**왜 이것이 중요한가**: Agent의 Tool 호출은 외부 API, 데이터베이스, 파일 시스템 등 다양한 외부 시스템과 상호작용한다. 이 외부 호출이 Agent 전체 응답 시간의 병목이 되는 경우가 빈번하다. LLM 추론이 1초 걸리더라도 Tool 호출에서 5초가 소요되면 사용자 체감 지연은 6초이다. Tool 성능 개선은 Agent 전체의 응답 속도를 직접적으로 개선한다.

**핵심 원리**: Tool 성능 개선의 세 가지 핵심 전략이 있다.

- **Timeout + Retry + Circuit Breaker**: 외부 API는 언제든 느려지거나 실패할 수 있다. Timeout으로 무한 대기를 방지하고, Retry로 일시적 오류를 복구하며, Circuit Breaker로 장애 전파를 차단한다.
- **병렬 실행**: 서로 의존성이 없는 Tool 호출은 동시에 실행한다. A와 B가 각각 500ms라면 순차 실행은 1000ms이지만 병렬 실행은 500ms이다.
- **결과 캐싱**: 동일한 인자로 반복 호출되는 Tool의 결과를 캐싱하여 불필요한 외부 호출을 제거한다.

**실무에서의 의미**: Circuit Breaker는 "연속 N회 실패하면 일정 시간 동안 호출을 차단"하는 패턴이다. 장애 상태의 외부 서비스에 계속 요청을 보내면 타임아웃 대기로 인해 전체 시스템이 느려진다. 차단 상태에서는 즉시 에러를 반환하거나 대체 응답을 제공하여 사용자 경험을 보호한다.

**다른 접근법과의 비교**: 일부 팀은 모든 Tool 호출을 순차적으로 실행한다. 구현이 간단하지만, 독립적인 Tool 3개를 순차 호출하면 지연이 3배로 늘어난다. 의존성 그래프를 분석하여 병렬 실행 가능한 호출을 식별하면 지연을 크게 줄일 수 있다. 다만 병렬 실행은 동시 API 호출 수 증가로 Rate Limit에 걸릴 수 있으므로 동시성 제한(semaphore)을 함께 사용해야 한다.

다음은 Timeout, Retry, Circuit Breaker를 통합한 Tool 실행기이다:

```python
import time
import asyncio
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed

class CircuitState(Enum):
    CLOSED = "closed"      # 정상
    OPEN = "open"          # 차단
    HALF_OPEN = "half_open"  # 시험적 허용

@dataclass
class CircuitBreaker:
    failure_threshold: int = 3
    recovery_timeout: float = 30.0
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    last_failure_time: float = 0.0

    def record_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def can_execute(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        return True  # HALF_OPEN

class ResilientToolExecutor:
    """Timeout + Retry + Circuit Breaker를 통합한 Tool 실행기."""

    def __init__(self, timeout_seconds: float = 10.0, max_retries: int = 2):
        self.timeout = timeout_seconds
        self.max_retries = max_retries
        self.breakers: dict[str, CircuitBreaker] = {}

    def _get_breaker(self, tool_name: str) -> CircuitBreaker:
        if tool_name not in self.breakers:
            self.breakers[tool_name] = CircuitBreaker()
        return self.breakers[tool_name]

    def execute(self, tool_name: str, func, **kwargs) -> dict:
        breaker = self._get_breaker(tool_name)
        if not breaker.can_execute():
            return {"error": f"Circuit OPEN for {tool_name}", "fallback": True}

        for attempt in range(self.max_retries + 1):
            try:
                start = time.time()
                result = func(**kwargs)
                elapsed = (time.time() - start) * 1000
                if elapsed > self.timeout * 1000:
                    raise TimeoutError(f"{tool_name} timeout: {elapsed:.0f}ms")
                breaker.record_success()
                return {"result": result, "latency_ms": round(elapsed), "attempts": attempt + 1}
            except Exception as e:
                breaker.record_failure()
                if attempt == self.max_retries:
                    return {"error": str(e), "attempts": attempt + 1}
                time.sleep(0.1 * (2 ** attempt))  # Exponential backoff
```

`ResilientToolExecutor`는 세 가지 방어 메커니즘을 계층적으로 적용한다. Timeout으로 무한 대기를 방지하고, Retry(exponential backoff)로 일시적 오류를 복구하며, Circuit Breaker로 반복 장애 시 빠른 실패를 반환한다. `execute()` 메서드는 모든 Tool 호출에 동일하게 적용할 수 있는 범용 래퍼이다.

### 예제

의존성 그래프를 분석하여 Tool을 병렬로 실행하는 시스템을 구현한다.

```python
class ParallelToolExecutor:
    """의존성 그래프 기반 병렬 Tool 실행기."""

    def __init__(self, executor: ResilientToolExecutor):
        self.executor = executor

    def execute_parallel(self, tools: list[dict], max_workers: int = 4) -> dict:
        """의존성이 없는 Tool들을 병렬로 실행한다.

        tools: [{"name": str, "func": callable, "kwargs": dict, "depends_on": list[str]}]
        """
        completed = {}
        remaining = list(tools)

        while remaining:
            # 의존성이 충족된 Tool 찾기
            ready = [t for t in remaining
                     if all(dep in completed for dep in t.get("depends_on", []))]
            if not ready:
                break

            # 병렬 실행
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                futures = {}
                for tool in ready:
                    kwargs = dict(tool.get("kwargs", {}))
                    # 의존성 결과를 kwargs에 주입
                    for dep in tool.get("depends_on", []):
                        kwargs[f"{dep}_result"] = completed[dep]
                    futures[pool.submit(
                        self.executor.execute, tool["name"], tool["func"], **kwargs
                    )] = tool["name"]

                for future in as_completed(futures):
                    name = futures[future]
                    completed[name] = future.result()

            remaining = [t for t in remaining if t["name"] not in completed]

        return completed
```

이 실행기는 의존성 그래프를 레이어별로 분석하여 각 레이어 내의 Tool들을 병렬 실행한다. 예를 들어 `get_user`와 `get_orders`가 독립적이고 `get_recommendations`가 둘 다 의존한다면, 첫 레이어에서 `get_user`와 `get_orders`를 병렬 실행하고, 두 번째 레이어에서 `get_recommendations`를 실행한다. 순차 대비 33% 이상의 지연 감소를 기대할 수 있다.

### Q&A

**Q: Circuit Breaker의 failure_threshold를 어떻게 설정해야 하나요?**

A: 외부 서비스의 특성에 따라 다르다. 안정적인 서비스(자체 DB)는 threshold를 높게(5~10), 불안정한 서비스(외부 API)는 낮게(2~3) 설정한다. recovery_timeout도 서비스 복구 시간에 맞춰야 한다. 실무에서는 초기에 보수적으로 설정(threshold=3, recovery=30s)하고, 프로덕션 로그를 분석하여 조정한다.

<details>
<summary>퀴즈: Tool A(500ms)와 Tool B(500ms)가 독립적이고, Tool C(300ms)가 A와 B에 의존할 때, 순차 실행과 병렬 실행의 총 지연 시간 차이는?</summary>

**힌트**: 순차는 A+B+C, 병렬은 max(A,B)+C로 계산한다.

**정답**: 순차 실행: 500 + 500 + 300 = 1300ms. 병렬 실행: max(500, 500) + 300 = 800ms. 차이는 500ms(38% 감소)이다. Tool 수가 많아질수록 병렬 실행의 효과는 더 커지며, 특히 외부 API 호출처럼 I/O 바운드 작업에서 효과적이다.
</details>

---

## 개념 4: 성능 개선 통합 파이프라인

### 개념 설명

**왜 이것이 중요한가**: Prompt, RAG, Tool 세 영역의 성능 개선은 독립적이지 않다. 프롬프트를 최적화하면 Tool 호출 패턴이 변하고, RAG 검색 품질이 올라가면 프롬프트에 전달되는 컨텍스트가 달라진다. 따라서 세 영역을 개별적으로 최적화한 뒤, 통합 파이프라인에서 전체 성능을 측정하고 병목을 식별해야 한다. 전체를 관통하는 성능 측정 없이 개별 최적화만 하면 "부분 최적화의 합이 전체 최적화가 아닌" 상황이 발생한다.

**핵심 원리**: 통합 성능 측정의 핵심은 각 단계의 지연 시간과 품질을 독립적으로 기록하는 것이다. Prompt 렌더링에 10ms, RAG 검색에 500ms, Tool 실행에 2000ms, LLM 추론에 1500ms가 소요된다면, Tool 실행이 전체 4010ms의 50%를 차지하므로 Tool 최적화가 우선 과제임을 데이터로 판단할 수 있다. 감이 아닌 데이터 기반의 우선순위 결정이 핵심이다.

**실무에서의 의미**: 성능 개선은 반복적 과정이다. 측정 -> 병목 식별 -> 개선 -> 재측정의 사이클을 반복해야 한다. 첫 번째 병목을 해결하면 두 번째 병목이 드러나고, 이를 해결하면 세 번째가 드러난다. 이 과정을 CI/CD에 통합하여 배포마다 자동으로 성능 회귀를 감지하는 것이 최종 목표이다.

**다른 접근법과의 비교**: 일부 팀은 "가장 느린 부분을 먼저 최적화"하는 단순 전략을 사용한다. 대부분의 경우 유효하지만, 예외가 있다. Tool 실행이 2000ms로 가장 느리더라도, 해당 Tool이 전체 요청의 10%에서만 호출된다면 영향이 제한적이다. 반면 RAG 검색이 500ms지만 100%의 요청에서 호출된다면 RAG 최적화의 총 효과가 더 클 수 있다. "지연 x 호출 빈도"로 가중치를 부여하는 것이 올바른 우선순위 결정 방법이다.

다음은 세 영역을 통합 측정하는 파이프라인이다:

```python
import time
from dataclasses import dataclass, field

@dataclass
class StageMetrics:
    stage: str
    latency_ms: float
    success: bool
    metadata: dict = field(default_factory=dict)

class PerformanceProfiler:
    """Agent 파이프라인의 각 단계별 성능을 프로파일링한다."""

    def __init__(self):
        self.stages: list[StageMetrics] = []

    def measure(self, stage: str, func, **kwargs) -> tuple:
        start = time.time()
        try:
            result = func(**kwargs)
            elapsed = (time.time() - start) * 1000
            self.stages.append(StageMetrics(stage, elapsed, True))
            return result, elapsed
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            self.stages.append(StageMetrics(stage, elapsed, False, {"error": str(e)}))
            raise

    def report(self) -> dict:
        total = sum(s.latency_ms for s in self.stages)
        return {
            "total_latency_ms": round(total, 1),
            "stages": [
                {"stage": s.stage, "latency_ms": round(s.latency_ms, 1),
                 "pct": round(s.latency_ms / total * 100, 1) if total > 0 else 0,
                 "success": s.success}
                for s in self.stages
            ],
            "bottleneck": max(self.stages, key=lambda s: s.latency_ms).stage
                if self.stages else None,
        }
```

`PerformanceProfiler`는 각 단계를 `measure()`로 감싸서 지연 시간과 성공 여부를 기록한다. `report()`는 전체 지연, 단계별 비율, 병목 단계를 요약한다. 이 리포트를 CI/CD에서 자동 생성하면 배포마다 성능 변화를 추적할 수 있다.

**회귀 방지 가드**

```python
@dataclass
class PerformanceBudget:
    """성능 예산: 각 단계의 허용 지연 상한선."""
    max_total_ms: float = 5000
    max_prompt_ms: float = 100
    max_rag_ms: float = 1000
    max_tool_ms: float = 3000
    max_llm_ms: float = 2000

class RegressionGuard:
    """성능 회귀를 자동 감지한다."""

    def __init__(self, budget: PerformanceBudget):
        self.budget = budget
        self.history: list[dict] = []

    def check(self, profiler: PerformanceProfiler) -> dict:
        report = profiler.report()
        violations = []
        stage_budgets = {
            "prompt": self.budget.max_prompt_ms,
            "rag": self.budget.max_rag_ms,
            "tool": self.budget.max_tool_ms,
            "llm": self.budget.max_llm_ms,
        }
        for stage_info in report["stages"]:
            budget = stage_budgets.get(stage_info["stage"])
            if budget and stage_info["latency_ms"] > budget:
                violations.append({
                    "stage": stage_info["stage"],
                    "actual_ms": stage_info["latency_ms"],
                    "budget_ms": budget,
                    "overflow_pct": round((stage_info["latency_ms"] - budget) / budget * 100, 1),
                })
        self.history.append(report)
        return {
            "passed": len(violations) == 0,
            "violations": violations,
            "total_latency_ms": report["total_latency_ms"],
            "budget_ms": self.budget.max_total_ms,
        }
```

`RegressionGuard`는 각 단계의 지연이 사전 정의된 예산(budget)을 초과하면 위반 사항을 보고한다. CI/CD 파이프라인에서 `check()`가 `passed=False`를 반환하면 배포를 차단하는 방식으로 성능 회귀를 자동 방지한다. `overflow_pct`는 초과 비율을 표시하여 심각도를 판단할 수 있게 해준다.

### 예제

성능 측정과 회귀 가드를 결합한 실행 예시이다.

```python
# 파이프라인 프로파일링 + 회귀 가드 사용 예시
profiler = PerformanceProfiler()
budget = PerformanceBudget(max_total_ms=5000, max_rag_ms=1000, max_tool_ms=3000)
guard = RegressionGuard(budget)

# 각 단계를 측정 (실제로는 해당 함수를 호출)
import time

def mock_prompt():
    time.sleep(0.05)
    return "렌더링된 프롬프트"

def mock_rag():
    time.sleep(0.4)
    return ["문서1", "문서2"]

def mock_tool():
    time.sleep(1.0)
    return {"result": "Tool 결과"}

def mock_llm():
    time.sleep(0.8)
    return "최종 응답"

profiler.measure("prompt", mock_prompt)
profiler.measure("rag", mock_rag)
profiler.measure("tool", mock_tool)
profiler.measure("llm", mock_llm)

# 성능 리포트
report = profiler.report()
print(f"총 지연: {report['total_latency_ms']}ms")
print(f"병목: {report['bottleneck']}")
for s in report["stages"]:
    print(f"  {s['stage']}: {s['latency_ms']}ms ({s['pct']}%)")

# 회귀 가드 체크
result = guard.check(profiler)
print(f"\n회귀 테스트: {'PASS' if result['passed'] else 'FAIL'}")
for v in result.get("violations", []):
    print(f"  위반: {v['stage']} - {v['actual_ms']}ms > {v['budget_ms']}ms ({v['overflow_pct']}% 초과)")
```

```
# 실행 결과
총 지연: 2250.3ms
병목: tool
  prompt: 50.1ms (2.2%)
  rag: 400.2ms (17.8%)
  tool: 1000.5ms (44.5%)
  llm: 800.1ms (35.5%)

회귀 테스트: PASS
```

이 예시에서 Tool이 전체 지연의 44.5%를 차지하는 병목으로 식별된다. 모든 단계가 예산 내이므로 회귀 테스트는 PASS이다. 만약 Tool 지연이 3500ms로 증가하면 budget(3000ms)을 초과하여 FAIL이 되고, 배포가 차단된다.

### Q&A

**Q: 성능 예산(Performance Budget)은 어떤 기준으로 설정하나요?**

A: 두 가지 접근이 있다. 첫째, **SLA 기반**: 사용자에게 약속한 응답 시간(예: P95 < 5초)을 역으로 각 단계에 배분한다. 둘째, **베이스라인 기반**: 현재 성능을 측정하고, 각 단계의 P95 지연에 20% 마진을 더한 값을 예산으로 설정한다. 후자가 더 현실적이며, 성능 개선이 진행됨에 따라 예산을 점진적으로 줄여나간다. 핵심은 예산을 "희망 사항"이 아닌 "강제 제약"으로 CI/CD에 통합하는 것이다.

<details>
<summary>퀴즈: Tool 실행이 2000ms로 가장 느리지만 전체 요청의 10%에서만 호출되고, RAG 검색이 500ms이지만 100%에서 호출된다면, 어느 쪽 최적화가 더 효과적인가요?</summary>

**힌트**: "지연 x 호출 빈도"로 가중 영향을 계산해 보자.

**정답**: Tool의 가중 영향: 2000ms x 0.1 = 200ms. RAG의 가중 영향: 500ms x 1.0 = 500ms. RAG 최적화가 2.5배 더 효과적이다. 단순히 "가장 느린 것"이 아니라 "가장 큰 총 영향"을 기준으로 우선순위를 정해야 한다. P50 기준에서 RAG를 200ms로 줄이면 전체 요청의 평균 지연이 300ms 감소하지만, Tool을 1000ms로 줄여도 평균 지연은 100ms만 감소한다.
</details>

---

## 실습

### 실습 1: RAG 검색 품질 최적화
- **연관 학습 목표**: 학습 목표 2
- **실습 목적**: Hybrid Search와 쿼리 확장을 적용하여 RAG 검색 품질을 측정 가능하게 개선한다
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 40분
- **선행 조건**: Python 기본, RAG 개념 이해
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

#### 실습 요구사항

1. **Hybrid Search 구현 (15분)**
   - `HybridSearcher` 클래스를 활용하여 BM25 + Semantic 검색을 구현하라
   - 기술 문서 10건 이상을 인덱싱하고 다양한 쿼리로 검색 결과를 비교하라
   - BM25 가중치를 0.2, 0.4, 0.6, 0.8로 변화시키며 결과 차이를 분석하라

2. **쿼리 확장 적용 (15분)**
   - `QueryExpander`를 구현하고 원본 쿼리 대비 검색 재현율 변화를 측정하라
   - 최소 5개 쿼리에 대해 확장 전/후 검색 결과를 비교하라

3. **성능 측정 (10분)**
   - 각 검색 방식(BM25 only, Semantic only, Hybrid, Hybrid+Expansion)의 Recall@5와 지연을 측정하라
   - 결과를 표로 정리하고 최적 설정을 도출하라

#### 기대 산출물
```
rag_optimization/
  hybrid_searcher.py       # Hybrid Search 구현
  query_expander.py        # 쿼리 확장 구현
  benchmark_results.json   # 벤치마크 결과
  analysis.md              # 분석 리포트
```

---

### 실습 2: Tool 호출 최적화 및 성능 회귀 가드
- **연관 학습 목표**: 학습 목표 3
- **실습 목적**: Tool 호출에 Circuit Breaker와 병렬 실행을 적용하고, 성능 회귀를 자동 감지하는 가드를 구현한다
- **실습 유형**: 코드 작성
- **난이도**: 심화
- **예상 소요 시간**: 50분
- **선행 조건**: 실습 1 완료, 비동기 프로그래밍 기본 이해
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

#### 실습 요구사항

1. **Resilient Tool Executor (20분)**
   - `ResilientToolExecutor`를 구현하고 다양한 장애 시나리오를 시뮬레이션하라
   - Timeout, Retry(exponential backoff), Circuit Breaker가 정상 동작하는지 검증하라
   - Circuit Breaker 상태 전이(CLOSED -> OPEN -> HALF_OPEN -> CLOSED)를 로깅하라

2. **병렬 Tool 실행 (15분)**
   - 의존성 그래프 기반 `ParallelToolExecutor`를 구현하라
   - 순차 실행 대비 병렬 실행의 지연 감소를 측정하라

3. **성능 회귀 가드 (15분)**
   - `RegressionGuard`를 CI/CD 스크립트로 통합하라
   - 예산 초과 시 exit code 1을 반환하여 배포를 차단하라
   - 10회 이상의 실행 결과를 히스토리로 기록하고 추이를 분석하라

#### 기대 산출물
```
tool_optimization/
  resilient_executor.py    # Resilient Tool Executor
  parallel_executor.py     # 병렬 실행기
  regression_guard.py      # 회귀 가드
  ci_check.sh              # CI/CD 스크립트
  performance_history.json # 성능 이력
```

---

## 핵심 정리
- **프롬프트 최적화**는 버전 관리 + A/B 테스트로 체계화하고, 프롬프트 체이닝으로 복잡한 작업을 단계별로 분해한다
- **RAG 성능 개선**은 Hybrid Search(BM25 + Semantic)로 검색 품질을 높이고, 쿼리 확장과 시맨틱 캐시로 재현율과 비용을 최적화한다
- **Tool 성능 개선**은 Timeout + Retry + Circuit Breaker로 안정성을 확보하고, 의존성 분석 기반 병렬 실행으로 지연을 줄인다
- 세 영역의 성능을 **통합 프로파일링**으로 측정하고, **성능 예산(Performance Budget)** 기반 회귀 가드를 CI/CD에 통합하여 배포 전 자동 검증한다
- 최적화 우선순위는 "지연 x 호출 빈도"의 가중 영향을 기준으로 결정한다
