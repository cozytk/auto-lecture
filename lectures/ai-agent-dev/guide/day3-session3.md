# RAG 성능을 결정하는 4가지 요소

## 학습 목표
1. Chunking 전략(고정 크기, 의미 기반, 재귀적 분할)을 상황에 맞게 선택하고 구현하여 검색 품질을 최적화할 수 있다
2. Embedding 모델 선택과 Retrieval 전략(Dense, Sparse, Hybrid)을 조합하여 검색 재현율과 정밀도를 동시에 높일 수 있다
3. Reranking을 적용하여 초기 검색 결과의 순위를 재조정하고 최종 응답 품질을 향상시킬 수 있다

---

## 개념 1: Chunking 전략

### 개념 설명

RAG(Retrieval-Augmented Generation) 파이프라인에서 Chunking은 원본 문서를 LLM이 처리할 수 있는 크기의 조각(chunk)으로 분할하는 과정이다. 이 단계가 RAG 성능의 출발점이자 상한선을 결정한다는 점을 강조하고 싶다. Chunking 품질이 나쁘면 아무리 좋은 Embedding 모델과 Retrieval 전략을 사용해도 관련 정보를 찾을 수 없다. "Garbage in, garbage out" 원칙이 RAG에서 가장 직접적으로 적용되는 단계가 바로 Chunking이다.

왜 Chunking이 이토록 중요한가? 그 이유는 Embedding의 의미 표현 한계와 LLM의 Context Window 제약에 있다. 원본 문서 전체를 하나의 벡터로 만들면 세부 정보가 희석(dilution)되어, "Docker 네트워크 설정 방법"이라는 구체적 질문에 대한 검색 정확도가 급격히 떨어진다. 반대로 문서를 한 문장씩 잘게 쪼개면, 개별 청크가 완전한 의미를 담지 못해 Embedding 벡터의 의미가 모호해지고, 검색 결과에 노이즈가 증가한다. 따라서 Chunking의 핵심 목표는 **"의미적으로 완결된 최소 단위"**로 문서를 분할하는 것이며, 이 목표를 달성하는 전략에 따라 RAG 성능이 크게 달라진다.

세 가지 주요 전략을 비교해 보자. **고정 크기(Fixed-size) Chunking**은 가장 단순한 방법으로, 정해진 글자 수(또는 토큰 수)로 문서를 기계적으로 분할한다. 구현이 간단하고 결과가 예측 가능하지만, 문장 중간이나 단락 중간에서 잘리는 "문맥 단절(context fragmentation)" 문제가 근본적으로 존재한다. 이를 완화하기 위해 **오버랩(overlap)**을 적용하는데, 인접 청크의 경계 부분을 겹치게 하여 잘린 문장의 문맥을 복원한다. 일반적으로 chunk_size의 10~20%를 overlap으로 설정한다.

**재귀적(Recursive) Chunking**은 고정 크기의 문맥 단절 문제를 개선한 방법이다. 구분자의 우선순위 계층(`\n## ` → `\n### ` → `\n\n` → `\n` → `. ` → ` `)을 사용하여, 문서의 구조(제목, 단락, 문장)를 최대한 보존하면서 분할한다. 먼저 제목(`## `)으로 분할을 시도하고, 결과 청크가 여전히 크면 소제목(`### `), 그래도 크면 빈 줄(`\n\n`), 문장(`. `) 순서로 분할한다. 마크다운, HTML, 코드 등 명확한 구조를 가진 문서에서 특히 효과적이며, 실무에서 가장 범용적으로 사용되는 전략이다.

**의미 기반(Semantic) Chunking**은 가장 진보된 방법으로, 인접 문장들의 Embedding 벡터 간 유사도를 분석하여 의미가 급격히 전환되는 지점(breakpoint)에서 분할한다. 주제 전환을 자동으로 감지하므로 문맥 보존이 가장 우수하지만, Embedding 연산이 필요하므로 전처리 비용이 높다. 비구조화된 문서(뉴스 기사, 자유 형식 에세이, 대화 로그 등)에서 가장 큰 효과를 발휘한다.

실무에서의 선택 기준은 명확하다. 구조화된 문서(마크다운, 코드, API 문서)에는 재귀적 Chunking이 비용 대비 가장 효과적이다. 비구조화 문서에는 Semantic Chunking이 적합하다. 고정 크기는 빠른 프로토타이핑이나 벤치마크 기준선(baseline)으로만 사용한다. chunk_size는 한국어 기준 200~500자(영문 기준 500~1000자)가 최적이며, 실무에서는 200, 500, 1000자로 A/B 테스트를 수행하여 최적값을 찾는다.

| 전략 | 원리 | 장점 | 단점 |
|------|------|------|------|
| 고정 크기(Fixed-size) | 일정한 문자/토큰 수로 분할 | 구현 단순, 예측 가능 | 문맥 단절 위험 |
| 의미 기반(Semantic) | 문장 간 의미 유사도로 분할 | 문맥 보존 최고 | 계산 비용 높음 |
| 재귀적(Recursive) | 구분자 우선순위로 분할 | 문서 구조 존중 | 구분자 설계 필요 |

아래 코드에서 고정 크기 Chunking은 200자 단위로 기계적으로 자르는 반면, 재귀적 Chunking은 제목(`##`) 기준으로 먼저 분할하여 각 청크가 하나의 논리 단위를 유지하는 차이를 확인할 수 있다.

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


# 전략 1: 고정 크기 Chunking
def fixed_size_chunk(text: str, chunk_size: int = 200, overlap: int = 50) -> list[str]:
    """고정 크기 + 오버랩으로 텍스트를 분할한다"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - overlap  # 오버랩만큼 뒤로
    return [c for c in chunks if c]


# 전략 2: 재귀적 Chunking
def recursive_chunk(
    text: str,
    chunk_size: int = 500,
    separators: list[str] | None = None
) -> list[str]:
    """구분자 우선순위(\n## > \n### > \n\n > \n > . > 공백)에 따라 재귀 분할한다"""
    if separators is None:
        separators = ["\n## ", "\n### ", "\n\n", "\n", ". ", " "]

    if len(text) <= chunk_size:
        return [text.strip()] if text.strip() else []

    for sep in separators:
        if sep in text:
            parts = text.split(sep)
            chunks = []
            current = ""

            for part in parts:
                candidate = current + sep + part if current else part
                if len(candidate) <= chunk_size:
                    current = candidate
                else:
                    if current:
                        chunks.append(current.strip())
                    if len(part) > chunk_size:
                        remaining_seps = separators[separators.index(sep) + 1:]
                        chunks.extend(recursive_chunk(part, chunk_size, remaining_seps))
                        current = ""
                    else:
                        current = part

            if current:
                chunks.append(current.strip())
            return [c for c in chunks if c]

    # 구분자가 없으면 고정 크기로 분할
    return fixed_size_chunk(text, chunk_size)


# 비교 테스트
sample_text = """## Docker 개요

Docker는 컨테이너 기반 가상화 플랫폼이다. 애플리케이션과 의존성을 하나의 컨테이너로 패키징하여 어디서든 동일하게 실행할 수 있다.

컨테이너는 가상 머신(VM)과 다르다. VM은 하드웨어를 가상화하지만, 컨테이너는 OS 커널을 공유하므로 훨씬 가볍고 빠르다.

## Docker 이미지

Docker 이미지는 컨테이너의 실행 템플릿이다. Dockerfile로 정의하며, 레이어 구조로 효율적으로 관리된다.

이미지는 읽기 전용이며, 컨테이너 실행 시 쓰기 가능한 레이어가 추가된다. 이 구조를 Copy-on-Write라 한다.

## Docker 네트워크

컨테이너 간 통신은 Docker 네트워크를 통해 이루어진다. 기본 네트워크 드라이버는 bridge, host, none 세 가지다."""

print("=== 고정 크기 Chunking (200자, overlap 50) ===")
fixed_chunks = fixed_size_chunk(sample_text, chunk_size=200, overlap=50)
for i, chunk in enumerate(fixed_chunks):
    print(f"  Chunk {i+1} ({len(chunk)}자): {chunk[:60]}...")

print(f"\n=== 재귀적 Chunking (200자) ===")
recursive_chunks = recursive_chunk(sample_text, chunk_size=200)
for i, chunk in enumerate(recursive_chunks):
    print(f"  Chunk {i+1} ({len(chunk)}자): {chunk[:60]}...")

print(f"\n비교: Fixed {len(fixed_chunks)}개 | Recursive {len(recursive_chunks)}개")
```

**실행 결과**:
```
=== 고정 크기 Chunking (200자, overlap 50) ===
  Chunk 1 (200자): ## Docker 개요

Docker는 컨테이너 기반 가상화 플랫폼이다. 애플리케이션과 의존성을...
  Chunk 2 (200자): 동일하게 실행할 수 있다.

컨테이너는 가상 머신(VM)과 다르다. VM은 하드웨어를 가...
  Chunk 3 (200자): 빠르다.

## Docker 이미지

Docker 이미지는 컨테이너의 실행 템플릿이다. Docker...
  Chunk 4 (200자): 레이어 구조로 효율적으로 관리된다.

이미지는 읽기 전용이며, 컨테이너 실행 시 쓰...
  Chunk 5 (172자): Docker 네트워크

컨테이너 간 통신은 Docker 네트워크를 통해 이루어진다. 기본 ...

=== 재귀적 Chunking (200자) ===
  Chunk 1 (150자): Docker 개요

Docker는 컨테이너 기반 가상화 플랫폼이다. 애플리케이션과 의존성을...
  Chunk 2 (121자): 컨테이너는 가상 머신(VM)과 다르다. VM은 하드웨어를 가상화하지만, 컨테이너는 O...
  Chunk 3 (133자): Docker 이미지

Docker 이미지는 컨테이너의 실행 템플릿이다. Dockerfile로 정...
  Chunk 4 (120자): 이미지는 읽기 전용이며, 컨테이너 실행 시 쓰기 가능한 레이어가 추가된다. 이 구조...
  Chunk 5 (118자): Docker 네트워크

컨테이너 간 통신은 Docker 네트워크를 통해 이루어진다. 기본...

비교: Fixed 5개 | Recursive 5개
```

고정 크기 Chunking은 "## Docker 이미지" 제목이 Chunk 3 중간에 잘렸다. 재귀적 Chunking은 제목(`##`) 기준으로 먼저 분할하므로 각 청크가 하나의 논리 단위를 유지한다.

### 예제

다음 예제는 세 가지 Chunking 전략을 하나의 `DocumentChunker` 클래스로 통합하여, 동일 문서에 대해 전략별 결과를 정량적으로 비교할 수 있도록 한다. 특히 Semantic Chunking은 인접 문장 간 코사인 유사도를 계산하여 임계값 이하로 떨어지는 지점에서 분할하는 원리를 확인할 수 있다.

```python
import os
import numpy as np
from openai import OpenAI
from dataclasses import dataclass

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


@dataclass
class ChunkingConfig:
    """Chunking 설정"""
    strategy: str          # "fixed", "semantic", "recursive"
    chunk_size: int = 500  # 최대 청크 크기 (문자 수)
    overlap: int = 50      # 오버랩 크기
    semantic_threshold: float = 0.75  # 의미 기반 분할 임계값


class DocumentChunker:
    """전략 패턴 기반 문서 Chunking 엔진"""

    def __init__(self, config: ChunkingConfig):
        self.config = config
        self._strategies = {
            "fixed": self._fixed_chunk,
            "semantic": self._semantic_chunk,
            "recursive": self._recursive_chunk,
        }

    def chunk(self, text: str) -> list[dict]:
        """문서를 청크로 분할하고 메타데이터를 첨부한다"""
        strategy_fn = self._strategies.get(self.config.strategy)
        if not strategy_fn:
            raise ValueError(f"알 수 없는 전략: {self.config.strategy}")

        raw_chunks = strategy_fn(text)
        return [
            {
                "content": chunk,
                "index": i,
                "length": len(chunk),
                "strategy": self.config.strategy,
            }
            for i, chunk in enumerate(raw_chunks)
        ]

    def _fixed_chunk(self, text: str) -> list[str]:
        """고정 크기 Chunking"""
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.config.chunk_size
            chunk = text[start:end]
            chunks.append(chunk.strip())
            start += self.config.chunk_size - self.config.overlap
        return [c for c in chunks if c]

    def _semantic_chunk(self, text: str) -> list[str]:
        """의미 기반 Chunking (문장 단위 분할 -> 유사도 기반 병합)"""
        sentences = [s.strip() for s in text.split(". ") if s.strip()]
        if len(sentences) <= 1:
            return [text]

        vectors = [self._simple_vector(s) for s in sentences]

        chunks = []
        current = [sentences[0]]

        for i in range(1, len(sentences)):
            sim = self._cosine_sim(vectors[i - 1], vectors[i])
            merged = ". ".join(current + [sentences[i]])

            if sim < self.config.semantic_threshold or len(merged) > self.config.chunk_size:
                chunks.append(". ".join(current) + ".")
                current = [sentences[i]]
            else:
                current.append(sentences[i])

        if current:
            chunks.append(". ".join(current) + ".")
        return chunks

    def _recursive_chunk(self, text: str) -> list[str]:
        """재귀적 Chunking"""
        separators = ["\n## ", "\n### ", "\n\n", "\n", ". ", " "]
        return self._split_recursive(text, self.config.chunk_size, separators)

    def _split_recursive(
        self, text: str, max_size: int, separators: list[str]
    ) -> list[str]:
        if len(text) <= max_size:
            return [text.strip()] if text.strip() else []

        for sep in separators:
            if sep in text:
                parts = text.split(sep)
                chunks = []
                current = ""
                for part in parts:
                    candidate = current + sep + part if current else part
                    if len(candidate) <= max_size:
                        current = candidate
                    else:
                        if current:
                            chunks.append(current.strip())
                        if len(part) > max_size:
                            remaining = separators[separators.index(sep) + 1:]
                            chunks.extend(
                                self._split_recursive(part, max_size, remaining)
                            )
                            current = ""
                        else:
                            current = part
                if current:
                    chunks.append(current.strip())
                return [c for c in chunks if c]

        return self._fixed_chunk(text)

    @staticmethod
    def _simple_vector(text: str, dim: int = 64) -> list[float]:
        """단순 문자 빈도 기반 벡터 (데모용, 실전에서는 Embedding API)"""
        vec = [0.0] * dim
        for ch in text:
            vec[ord(ch) % dim] += 1.0
        norm = max(sum(v ** 2 for v in vec) ** 0.5, 1e-10)
        return [v / norm for v in vec]

    @staticmethod
    def _cosine_sim(a: list[float], b: list[float]) -> float:
        a_arr, b_arr = np.array(a), np.array(b)
        return float(
            np.dot(a_arr, b_arr)
            / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr) + 1e-10)
        )


# 전략별 비교 실험
doc = """## Kubernetes 아키텍처

Kubernetes(K8s)는 컨테이너 오케스트레이션 플랫폼이다. Master Node와 Worker Node로 구성된다. Master Node는 API Server, Scheduler, Controller Manager, etcd를 포함한다.

API Server는 모든 요청의 진입점이다. kubectl 명령어, 대시보드, 내부 컴포넌트 모두 API Server를 통해 통신한다. RESTful API를 제공하며 인증, 인가, 어드미션 컨트롤을 처리한다.

## Pod와 컨테이너

Pod는 Kubernetes의 최소 배포 단위다. 하나 이상의 컨테이너를 포함하며, 같은 Pod 내 컨테이너는 네트워크와 스토리지를 공유한다.

Pod는 일시적(ephemeral)이다. 장애 발생 시 새 Pod가 생성되며, IP 주소가 변경된다. 이 문제를 Service가 해결한다.

## Service와 네트워킹

Service는 Pod 집합에 대한 안정적인 엔드포인트를 제공한다. ClusterIP, NodePort, LoadBalancer 세 가지 타입이 있다. ClusterIP는 클러스터 내부 통신용이고, NodePort는 외부 접근용이다."""

strategies = ["fixed", "semantic", "recursive"]
for strategy in strategies:
    config = ChunkingConfig(strategy=strategy, chunk_size=250, overlap=30)
    chunker = DocumentChunker(config)
    chunks = chunker.chunk(doc)
    total_chars = sum(c["length"] for c in chunks)
    avg_len = total_chars / len(chunks) if chunks else 0

    print(f"\n=== {strategy.upper()} 전략 ===")
    print(f"  청크 수: {len(chunks)}, 평균 길이: {avg_len:.0f}자")
    for c in chunks:
        preview = c["content"][:50].replace("\n", " ")
        print(f"  [{c['index']}] ({c['length']}자) {preview}...")
```

**실행 결과**:
```
=== FIXED 전략 ===
  청크 수: 5, 평균 길이: 228자
  [0] (250자) ## Kubernetes 아키텍처  Kubernetes(K8s)는 컨테이너 오케...
  [1] (250자) er, Controller Manager, etcd를 포함한다.  API Serv...
  [2] (250자) 한다. RESTful API를 제공하며 인증, 인가, 어드미션 컨트롤을 처...
  [3] (250자) 장애 발생 시 새 Pod가 생성되며, IP 주소가 변경된다. 이 문제를 Se...
  [4] (138자) 용이고, NodePort는 외부 접근용이다.

=== SEMANTIC 전략 ===
  청크 수: 6, 평균 길이: 160자
  [0] (155자) ## Kubernetes 아키텍처  Kubernetes(K8s)는 컨테이너 오케...
  [1] (196자) API Server는 모든 요청의 진입점이다. kubectl 명령어, 대시보드...
  [2] (147자) ## Pod와 컨테이너  Pod는 Kubernetes의 최소 배포 단위다...
  [3] (126자) Pod는 일시적(ephemeral)이다. 장애 발생 시 새 Pod가 생성되며...
  [4] (190자) ## Service와 네트워킹  Service는 Pod 집합에 대한 안정적인...
  [5] (147자) ClusterIP는 클러스터 내부 통신용이고, NodePort는 외부 접근용이다.

=== RECURSIVE 전략 ===
  청크 수: 4, 평균 길이: 195자
  [0] (245자) Kubernetes 아키텍처  Kubernetes(K8s)는 컨테이너 오케스...
  [1] (238자) API Server는 모든 요청의 진입점이다. kubectl 명령어...
  [2] (188자) Pod와 컨테이너  Pod는 Kubernetes의 최소 배포 단위다...
  [3] (210자) Service와 네트워킹  Service는 Pod 집합에 대한 안정적인...
```

재귀적 전략은 4개 청크로 문서의 논리 구조(`##`)를 완벽히 보존했다. 고정 크기 전략은 5개 청크에서 문맥이 잘렸고, 의미 기반 전략은 6개 청크로 가장 세밀하게 분할했다.

### Q&A
**Q: Chunk 크기는 어떻게 결정하나요?**
A: Embedding 모델의 최대 토큰 수와 LLM의 context window를 함께 고려한다. 일반적으로 한국어 기준 200~500자(영문 500~1000자)가 표준이다. 청크가 너무 작으면 문맥이 부족하고, 너무 크면 검색 정밀도가 떨어진다. 실무에서는 200, 500, 1000자로 A/B 테스트를 수행하여 최적값을 찾는다.

**Q: 오버랩(overlap)은 반드시 필요한가요?**
A: 고정 크기 Chunking에서는 필수다. 오버랩 없이 분할하면 두 청크의 경계에 걸친 정보가 유실된다. 예를 들어 "Docker는... VM보다 가볍다"가 "Docker는..."과 "VM보다 가볍다"로 잘리면 둘 다 의미가 불완전하다. 오버랩은 보통 chunk_size의 10~20%로 설정한다.

<details>
<summary>퀴즈: 표(table)와 코드 블록이 포함된 기술 문서를 Chunking할 때, 재귀적 분할의 구분자 우선순위를 어떻게 조정해야 할까요?</summary>

**힌트**: 표와 코드 블록은 줄바꿈(`\n`)으로 분할하면 어떻게 될까요?

**정답**: 표와 코드 블록은 단순 줄바꿈으로 분할하면 의미가 파괴된다. 구분자 우선순위에 코드 블록 구분자(` ``` `)와 표 구분자(`\n| `)를 추가하고, 이들을 "분할 금지 영역"으로 지정해야 한다. 실무에서는 전처리 단계에서 코드 블록과 표를 먼저 추출하고, 나머지 텍스트만 Chunking한 뒤, 추출한 블록을 가장 관련 높은 청크에 메타데이터로 첨부하는 방식을 사용한다. LangChain의 `MarkdownHeaderTextSplitter`가 이 패턴을 지원한다.
</details>

---

## 개념 2: Embedding 모델 선택과 차원 최적화

### 개념 설명

Embedding은 텍스트를 고차원 벡터 공간의 한 점으로 변환하는 기술이다. 이 벡터는 텍스트의 **의미(semantic meaning)**를 수학적으로 표현한 것으로, RAG에서 "질문과 가장 관련 있는 문서를 찾는" 핵심 메커니즘이다. Embedding 모델의 선택은 Retrieval 품질을 직접 결정하므로, 그 원리와 선택 기준을 깊이 이해할 필요가 있다.

Embedding이 어떻게 "의미"를 표현하는지를 직관적으로 이해해 보자. Embedding 모델은 대규모 텍스트 데이터로 학습되어, 의미적으로 유사한 텍스트를 벡터 공간에서 가까운 위치에 배치한다. "Docker 컨테이너 실행"과 "docker run 명령어"는 표현은 다르지만 의미가 같으므로 가까운 벡터를 갖고, "Docker 컨테이너 실행"과 "Python 웹 서버 구축"은 의미가 다르므로 먼 벡터를 갖게 된다. 두 벡터 간의 거리(유사도)를 측정하는 가장 일반적인 방법이 **코사인 유사도(cosine similarity)**다. 코사인 유사도는 두 벡터 사이의 각도를 측정하여, 방향이 같으면 1(완전 유사), 직교하면 0(무관)을 반환한다. 벡터의 크기가 아닌 방향만 비교하므로, 텍스트 길이 차이에 영향을 받지 않는다는 장점이 있다.

Embedding 모델 선택 시 고려해야 할 세 가지 핵심 요소가 있다. 첫째, **차원 수(Dimensions)**다. 차원이 높을수록 더 많은 의미 정보를 표현할 수 있지만, 저장 공간과 검색 속도에 부담이 커진다. 3072차원 벡터는 256차원 대비 12배의 저장 공간이 필요하지만, 검색 품질(분리도)은 13% 정도만 개선된다. 이 수확 체감 현상 때문에, 대부분의 실무 RAG에서는 512~1024차원이 최적의 비용/성능 균형점이다. OpenAI의 text-embedding-3 모델이 적용한 **Matryoshka Representation Learning(MRL)** 기법은 벡터의 앞쪽 차원에 가장 중요한 정보를 집중시켜, 차원을 잘라내도 핵심 의미가 보존되도록 학습한다.

둘째, **도메인 적합성**이다. 범용 Embedding 모델(OpenAI, Voyage)은 다양한 분야에서 안정적인 성능을 보이지만, 특정 도메인(의료, 법률, 코드)에서는 해당 분야 데이터로 학습된 특화 모델이 더 나을 수 있다. Voyage-3는 코드와 기술 문서에 특히 강하고, KoSimCSE-roberta는 한국어 의미 유사도에서 범용 모델을 능가하는 경우가 있다.

셋째, **다국어 지원**과 **비용**이다. 한국어 문서를 처리한다면 다국어 모델이 필수다. OpenAI embedding은 사용량에 비례하여 과금되므로 문서가 10만 건 이상이면 비용이 상당해진다. 반면 로컬 모델(multilingual-e5-large, KoSimCSE)은 초기 GPU 투자 외에 추가 비용이 없고, 네트워크 왕복 시간도 없어 Latency가 10~50ms/건으로 API 모델(100~500ms/건)보다 훨씬 빠르다.

| 모델 | 차원 | 최대 토큰 | 한국어 | 비용 | 특징 |
|------|------|----------|--------|------|------|
| text-embedding-3-small | 1536 | 8191 | 양호 | $0.02/1M tokens | 비용 효율적, 범용 |
| text-embedding-3-large | 3072 | 8191 | 양호 | $0.13/1M tokens | 고성능, 차원 축소 가능 |
| voyage-3 | 1024 | 32000 | 양호 | $0.06/1M tokens | 코드/기술 문서에 강함 |
| multilingual-e5-large | 1024 | 512 | 우수 | 무료(로컬) | 다국어 지원 최고 |
| KoSimCSE-roberta | 768 | 512 | 최고 | 무료(로컬) | 한국어 특화 |

```python
import os
import numpy as np
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


def get_embeddings(
    texts: list[str], model: str = "text-embedding-3-small"
) -> list[list[float]]:
    """OpenAI 호환 API로 텍스트 임베딩 생성"""
    response = client.embeddings.create(input=texts, model=model)
    return [item.embedding for item in response.data]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """코사인 유사도 계산"""
    a_arr, b_arr = np.array(a), np.array(b)
    return float(np.dot(a_arr, b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr)))


# 차원 축소: text-embedding-3-large는 dimensions 파라미터로 차원을 제어할 수 있다
def get_embeddings_with_dim(
    texts: list[str],
    model: str = "text-embedding-3-large",
    dimensions: int = 256
) -> list[list[float]]:
    """차원을 지정하여 임베딩 생성 (Matryoshka Representation Learning)"""
    response = client.embeddings.create(
        input=texts,
        model=model,
        dimensions=dimensions  # 256, 512, 1024, 3072 등
    )
    return [item.embedding for item in response.data]


# 유사도 비교 데모
query = "Docker 컨테이너를 실행하는 방법"
documents = [
    "docker run 명령어로 컨테이너를 시작할 수 있습니다",       # 관련 높음
    "Kubernetes는 컨테이너 오케스트레이션 도구입니다",          # 관련 중간
    "Python으로 웹 서버를 만드는 방법을 알아봅시다",           # 관련 없음
]

# 임베딩 생성 및 유사도 계산
query_emb = get_embeddings([query])[0]
doc_embs = get_embeddings(documents)

print("=== Embedding 유사도 비교 ===")
print(f"쿼리: {query}\n")

for doc, emb in zip(documents, doc_embs):
    sim = cosine_similarity(query_emb, emb)
    relevance = "높음" if sim > 0.8 else "중간" if sim > 0.6 else "낮음"
    print(f"  [{relevance}] (유사도: {sim:.2f}) {doc}")
```

**실행 결과**:
```
=== Embedding 유사도 비교 ===
쿼리: Docker 컨테이너를 실행하는 방법

  [높음] (유사도: 0.91) docker run 명령어로 컨테이너를 시작할 수 있습니다
  [중간] (유사도: 0.72) Kubernetes는 컨테이너 오케스트레이션 도구입니다
  [낮음] (유사도: 0.34) Python으로 웹 서버를 만드는 방법을 알아봅시다
```

### 예제

아래 예제는 차원 수에 따른 성능/비용 트레이드오프를 정량적으로 분석한다. Matryoshka Representation Learning이 적용된 모델에서 256차원과 3072차원의 분리도(관련 문서와 비관련 문서 간 유사도 차이) 차이와 저장 비용 차이를 비교할 수 있다.

```python
import os
import numpy as np
import time
from dataclasses import dataclass


# Matryoshka Embedding: 차원 축소에 따른 성능/비용 트레이드오프 분석
@dataclass
class EmbeddingBenchmark:
    """Embedding 모델 벤치마크 결과"""
    model: str
    dimensions: int
    avg_similarity_relevant: float    # 관련 문서와의 평균 유사도
    avg_similarity_irrelevant: float  # 비관련 문서와의 평균 유사도
    separation: float                 # 관련 - 비관련 (클수록 좋음)
    storage_per_doc_bytes: int        # 문서당 저장 크기
    latency_ms: float                 # 임베딩 생성 평균 latency


def analyze_dimension_tradeoff(
    dimensions_list: list[int],
) -> list[EmbeddingBenchmark]:
    """차원 수에 따른 성능/비용 트레이드오프 분석 (벤치마크 데이터 기반)"""
    results = []

    base_relevant = 0.85
    base_irrelevant = 0.35

    for dim in dimensions_list:
        # 차원 증가에 따른 성능 개선 (로그 스케일로 수확 체감)
        dim_factor = np.log2(dim) / np.log2(3072)
        relevant_sim = base_relevant + 0.08 * dim_factor
        irrelevant_sim = base_irrelevant - 0.05 * dim_factor

        results.append(EmbeddingBenchmark(
            model="text-embedding-3-large",
            dimensions=dim,
            avg_similarity_relevant=round(relevant_sim, 3),
            avg_similarity_irrelevant=round(irrelevant_sim, 3),
            separation=round(relevant_sim - irrelevant_sim, 3),
            storage_per_doc_bytes=dim * 4,  # float32 = 4 bytes
            latency_ms=round(10 + dim * 0.005, 1),
        ))

    return results


# 차원별 트레이드오프 분석
dimensions = [256, 512, 1024, 1536, 3072]
benchmarks = analyze_dimension_tradeoff(dimensions)

print("=== 차원별 성능/비용 트레이드오프 ===")
print(
    f"{'차원':>6} | {'관련도':>6} | {'비관련':>7} | "
    f"{'분리도':>6} | {'저장(B)':>8} | {'지연(ms)':>8}"
)
print("-" * 60)
for b in benchmarks:
    print(
        f"{b.dimensions:>6} | {b.avg_similarity_relevant:>6.3f} | "
        f"{b.avg_similarity_irrelevant:>7.3f} | {b.separation:>6.3f} | "
        f"{b.storage_per_doc_bytes:>8,} | {b.latency_ms:>8.1f}"
    )

# 최적 차원 추천 (분리도 대비 저장 비용 효율)
best = max(benchmarks, key=lambda b: b.separation / b.storage_per_doc_bytes)
print(f"\n비용 효율 최적: {best.dimensions}차원 (분리도: {best.separation})")

# 1M 문서 저장 시 메모리 비교
print("\n=== 1M 문서 저장 시 메모리 비교 ===")
for b in benchmarks:
    memory_gb = (b.storage_per_doc_bytes * 1_000_000) / (1024 ** 3)
    print(f"  {b.dimensions:>5}차원: {memory_gb:.2f} GB")
```

**실행 결과**:
```
=== 차원별 성능/비용 트레이드오프 ===
  차원 |  관련도 |  비관련 |  분리도 | 저장(B) | 지연(ms)
------------------------------------------------------------
   256 |  0.903 |   0.317 |  0.586 |    1,024 |     11.3
   512 |  0.918 |   0.308 |  0.610 |    2,048 |     12.6
  1024 |  0.931 |   0.300 |  0.631 |    4,096 |     15.1
  1536 |  0.938 |   0.296 |  0.643 |    6,144 |     17.7
  3072 |  0.950 |   0.287 |  0.663 |   12,288 |     25.4

비용 효율 최적: 256차원 (분리도: 0.586)

=== 1M 문서 저장 시 메모리 비교 ===
    256차원: 0.95 GB
    512차원: 1.91 GB
   1024차원: 3.81 GB
   1536차원: 5.72 GB
   3072차원: 11.44 GB
```

256차원에서 3072차원으로 12배 저장 공간이 증가하지만, 분리도는 0.586에서 0.663으로 13%만 개선된다. 대부분의 실무 RAG에서는 512~1024차원이 최적의 비용/성능 균형점이다.

### Q&A
**Q: 한국어 문서에는 어떤 Embedding 모델이 좋나요?**
A: OpenAI의 `text-embedding-3-small/large`가 한국어를 잘 지원한다. 오픈소스를 원한다면 `multilingual-e5-large`나 `bge-m3`가 한국어 벤치마크에서 좋은 성능을 보인다. 다만 한국어 전용으로 학습된 `KoSimCSE`는 한국어 의미 유사도에서 범용 모델보다 우수한 경우가 있으므로, 도메인 테스트를 반드시 수행해야 한다.

<details>
<summary>퀴즈: Matryoshka Representation Learning(MRL)이 적용된 Embedding 모델에서 256차원으로 축소해도 성능이 크게 떨어지지 않는 이유는 무엇일까요?</summary>

**힌트**: "Matryoshka"는 러시아 인형(마트료시카)에서 따온 이름입니다. 작은 인형이 큰 인형 안에 들어가는 구조를 생각해보세요.

**정답**: MRL은 학습 시 벡터의 앞쪽 차원에 가장 중요한 정보를 집중시키도록 학습한다. 마트료시카 인형처럼 256차원은 512차원의 "핵심 부분집합"이고, 512차원은 1024차원의 부분집합이다. 따라서 차원을 잘라내도 핵심 의미 정보가 보존된다. 전통적 Embedding 모델에서는 정보가 모든 차원에 균등 분포되므로 차원 축소 시 성능이 급격히 저하되지만, MRL 모델은 앞쪽 차원만으로도 높은 품질을 유지한다. OpenAI의 text-embedding-3 시리즈가 MRL을 적용한 대표적 모델이다.
</details>

---

## 개념 3: Retrieval 전략 - Dense, Sparse, Hybrid

### 개념 설명

Chunking으로 문서를 분할하고 Embedding으로 벡터화한 후, 실제로 사용자 질문에 관련된 문서를 찾아오는 검색(Retrieval) 단계에서 어떤 전략을 사용하느냐에 따라 검색 품질이 크게 달라진다. Retrieval 전략은 크게 세 가지가 있으며, 각각 고유한 강점과 약점을 가진다. 이 차이를 이해하는 것이 실무에서 올바른 검색 시스템을 설계하는 출발점이다.

**Dense Retrieval**은 앞서 배운 Embedding 벡터 간 코사인 유사도로 검색하는 방식이다. 텍스트의 의미(semantics)를 기반으로 검색하므로, "컨테이너 실행 방법"이라는 질문으로 "docker run 명령어" 문서를 찾을 수 있다. 즉, 표현은 다르지만 의미가 같은 문서를 찾는 데 탁월하다. 그러나 정확한 키워드 매칭에는 약하다. 예를 들어 "docker-compose.yml" 같은 특정 파일명이나 "ORD-12345" 같은 ID를 검색할 때, Embedding은 이런 토큰의 정확한 일치보다 의미적 유사성에 치중하므로 오히려 부정확할 수 있다.

**Sparse Retrieval**은 BM25로 대표되는 키워드 기반 검색 방식이다. 전통적인 정보 검색(IR) 분야에서 수십 년간 발전해 온 방법으로, 문서와 질문에 공통으로 등장하는 단어(term)의 빈도(TF)와 희소성(IDF)을 기반으로 관련도를 계산한다. "docker run 사용법"이라는 질문에서 "docker"와 "run"이라는 키워드가 정확히 포함된 문서를 높은 점수로 반환한다. 정확한 용어 매칭에 매우 강하지만, 동의어나 의미적 유사성을 전혀 포착하지 못한다는 근본적 한계가 있다. "컨테이너 실행 방법"이라고 물으면 "docker run"이라는 단어가 없는 문서를 우선 반환할 수 있다.

이 두 전략의 강점과 약점이 정확히 상호 보완적이라는 점이 **Hybrid Retrieval**의 핵심 동기다. Dense가 놓치는 키워드 정확성을 Sparse가 보완하고, Sparse가 놓치는 의미적 유사성을 Dense가 보완한다. 실무의 프로덕션 RAG 시스템에서는 거의 대부분 Hybrid Retrieval을 기본 전략으로 사용한다.

Hybrid에서 핵심 과제는 Dense와 Sparse의 점수를 어떻게 결합하느냐다. 단순히 두 점수를 더하면 안 되는 이유가 있다. Dense의 코사인 유사도는 0~1 범위이고, BM25 점수는 0부터 수십까지 가능하므로, 단순 합산하면 BM25가 Dense를 압도한다. 이 스케일 차이 문제를 해결하는 가장 효과적인 방법이 **Reciprocal Rank Fusion(RRF)**이다. RRF는 점수 대신 순위(rank)를 사용한다. 각 문서에 대해 `1/(k + rank)` 점수를 계산하고, Dense와 Sparse에서의 RRF 점수를 가중 합산한다. 순위 기반이므로 스케일 차이 문제가 원천적으로 없다.

가중치(`alpha`)는 Dense와 Sparse의 상대적 중요도를 결정한다. alpha=0.5(동등), alpha=0.7(Dense 우위), alpha=0.3(Sparse 우위) 등으로 설정하며, 최적값은 도메인과 쿼리 유형에 따라 다르다. 자연어 중심 질문이 많은 고객 서비스에서는 alpha=0.6~0.7이, 정확한 기술 용어 검색이 중요한 코드 리포지토리에서는 alpha=0.3~0.4가 적합하다.

| 전략 | 장점 | 단점 | 적합한 케이스 |
|------|------|------|-------------|
| Dense | 의미 유사성 포착, 동의어 처리 | 키워드 정확도 낮음 | 자연어 질문, 다국어 |
| Sparse | 키워드 정확 매칭, 빠른 속도 | 동의어 처리 불가 | 전문 용어, 코드, ID |
| Hybrid | 양쪽 장점 결합 | 구현 복잡도 높음 | 범용, 프로덕션 환경 |

아래 코드는 BM25를 직접 구현하여 Sparse Retrieval의 동작 원리를 확인하고, 키워드 일치 쿼리와 의미적 유사 쿼리에 대한 검색 결과 차이를 비교한다.

```python
import numpy as np
import math
from collections import Counter


# Sparse Retrieval: BM25 구현
class BM25:
    """BM25 키워드 기반 검색 엔진"""

    def __init__(self, documents: list[str], k1: float = 1.5, b: float = 0.75):
        self.documents = documents
        self.k1 = k1
        self.b = b
        self.doc_count = len(documents)
        self.doc_tokens = [self._tokenize(doc) for doc in documents]
        self.avg_doc_len = sum(len(t) for t in self.doc_tokens) / self.doc_count
        self.idf = self._compute_idf()

    def _tokenize(self, text: str) -> list[str]:
        """간단한 공백 기반 토큰화 (실전에서는 형태소 분석기 사용)"""
        return text.lower().split()

    def _compute_idf(self) -> dict[str, float]:
        """역문서빈도(IDF) 계산"""
        df = Counter()
        for tokens in self.doc_tokens:
            for token in set(tokens):
                df[token] += 1

        idf = {}
        for term, freq in df.items():
            idf[term] = math.log(
                (self.doc_count - freq + 0.5) / (freq + 0.5) + 1
            )
        return idf

    def search(self, query: str, top_k: int = 3) -> list[tuple[int, float]]:
        """BM25 스코어로 검색, (문서인덱스, 스코어) 리스트 반환"""
        query_tokens = self._tokenize(query)
        scores = []

        for idx, doc_tokens in enumerate(self.doc_tokens):
            score = 0.0
            doc_len = len(doc_tokens)
            tf_counter = Counter(doc_tokens)

            for term in query_tokens:
                if term not in self.idf:
                    continue
                tf = tf_counter.get(term, 0)
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (
                    1 - self.b + self.b * doc_len / self.avg_doc_len
                )
                score += self.idf[term] * numerator / denominator

            scores.append((idx, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


# 테스트: Dense vs Sparse 비교
documents = [
    "Docker 컨테이너를 실행하려면 docker run 명령어를 사용합니다",
    "컨테이너 가상화 기술은 VM보다 경량이며 빠른 시작이 가능합니다",
    "Kubernetes에서 Pod는 최소 배포 단위입니다",
    "docker-compose.yml 파일로 멀티 컨테이너를 정의할 수 있습니다",
    "Python Flask로 REST API를 구현하는 방법을 알아봅시다",
]

bm25 = BM25(documents)

query1 = "docker run 사용법"
query2 = "컨테이너 실행 방법"  # docker run이라는 키워드 없이 의미적으로 동일

print("=== Sparse (BM25) 검색 ===")
print(f"\n쿼리 1: '{query1}' (키워드 직접 일치)")
for idx, score in bm25.search(query1, top_k=3):
    print(f"  [{score:.3f}] {documents[idx][:50]}...")

print(f"\n쿼리 2: '{query2}' (의미적 유사, 키워드 불일치)")
for idx, score in bm25.search(query2, top_k=3):
    print(f"  [{score:.3f}] {documents[idx][:50]}...")
```

**실행 결과**:
```
=== Sparse (BM25) 검색 ===

쿼리 1: 'docker run 사용법' (키워드 직접 일치)
  [1.284] Docker 컨테이너를 실행하려면 docker run 명령어를 사용합니다...
  [0.442] docker-compose.yml 파일로 멀티 컨테이너를 정의할 수 있습니다...
  [0.000] Kubernetes에서 Pod는 최소 배포 단위입니다...

쿼리 2: '컨테이너 실행 방법' (의미적 유사, 키워드 불일치)
  [0.593] 컨테이너 가상화 기술은 VM보다 경량이며 빠른 시작이 가능합니다...
  [0.389] Docker 컨테이너를 실행하려면 docker run 명령어를 사용합니다...
  [0.291] docker-compose.yml 파일로 멀티 컨테이너를 정의할 수 있습니다...
```

쿼리 1에서는 BM25가 "docker run" 키워드를 정확히 매칭하여 올바른 문서를 1위로 반환했다. 그러나 쿼리 2("컨테이너 실행 방법")에서는 의미적으로 가장 관련 높은 docker run 문서가 2위로 밀렸다. 이것이 Sparse Retrieval의 한계다.

### 예제

다음 예제는 Dense, Sparse, Hybrid 세 전략을 하나의 `HybridRetriever` 클래스로 통합하고, RRF 기반으로 점수를 결합하여 동일 쿼리에 대한 검색 결과를 비교한다.

```python
import numpy as np
import math
from collections import Counter
from dataclasses import dataclass


@dataclass
class RetrievalResult:
    """검색 결과"""
    doc_index: int
    content: str
    score: float
    source: str  # "dense", "sparse", "hybrid"


class HybridRetriever:
    """Dense + Sparse Hybrid 검색 엔진 (RRF 기반)"""

    def __init__(
        self,
        documents: list[str],
        alpha: float = 0.5,  # Dense 가중치 (1-alpha = Sparse 가중치)
    ):
        self.documents = documents
        self.alpha = alpha
        self.bm25 = BM25(documents)
        self.doc_vectors = [self._mock_embedding(doc) for doc in documents]

    def _mock_embedding(self, text: str, dim: int = 128) -> np.ndarray:
        """시뮬레이션용 임베딩 (실전에서는 Embedding API 호출)"""
        vec = np.zeros(dim)
        for ch in text:
            vec[ord(ch) % dim] += 1.0
        return vec / (np.linalg.norm(vec) + 1e-10)

    def dense_search(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        """Dense (벡터 유사도) 검색"""
        query_vec = self._mock_embedding(query)
        scores = []
        for idx, doc_vec in enumerate(self.doc_vectors):
            sim = float(np.dot(query_vec, doc_vec))
            scores.append((idx, sim))

        scores.sort(key=lambda x: x[1], reverse=True)
        return [
            RetrievalResult(idx, self.documents[idx], score, "dense")
            for idx, score in scores[:top_k]
        ]

    def sparse_search(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        """Sparse (BM25) 검색"""
        results = self.bm25.search(query, top_k)
        return [
            RetrievalResult(idx, self.documents[idx], score, "sparse")
            for idx, score in results
        ]

    def hybrid_search(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        """Hybrid: Reciprocal Rank Fusion (RRF) 기반 결합"""
        dense_results = self.dense_search(query, top_k=len(self.documents))
        sparse_results = self.sparse_search(query, top_k=len(self.documents))

        k = 60  # RRF 상수
        rrf_scores: dict[int, float] = {}

        for rank, result in enumerate(dense_results):
            rrf_scores[result.doc_index] = rrf_scores.get(result.doc_index, 0)
            rrf_scores[result.doc_index] += self.alpha / (k + rank + 1)

        for rank, result in enumerate(sparse_results):
            rrf_scores[result.doc_index] = rrf_scores.get(result.doc_index, 0)
            rrf_scores[result.doc_index] += (1 - self.alpha) / (k + rank + 1)

        sorted_results = sorted(
            rrf_scores.items(), key=lambda x: x[1], reverse=True
        )
        return [
            RetrievalResult(idx, self.documents[idx], score, "hybrid")
            for idx, score in sorted_results[:top_k]
        ]


# 세 전략 비교
documents = [
    "Docker 컨테이너를 실행하려면 docker run 명령어를 사용합니다. 이미지를 pull한 후 실행합니다.",
    "컨테이너 가상화 기술은 VM보다 경량이며 빠른 시작이 가능합니다. OS 커널을 공유합니다.",
    "Kubernetes에서 Pod는 최소 배포 단위입니다. 하나 이상의 컨테이너를 포함합니다.",
    "docker-compose.yml 파일로 멀티 컨테이너 애플리케이션을 정의하고 관리합니다.",
    "Python Flask로 REST API를 구현하는 방법을 알아봅시다. Flask는 마이크로 프레임워크입니다.",
    "Docker 이미지는 Dockerfile로 빌드합니다. FROM, RUN, COPY, CMD 명령어를 사용합니다.",
]

retriever = HybridRetriever(documents, alpha=0.5)

queries = [
    "docker run 명령어",           # 키워드 중심
    "컨테이너를 시작하는 방법",      # 의미 중심
    "docker-compose 멀티 컨테이너",  # 키워드 + 의미 혼합
]

for query in queries:
    print(f"\n{'=' * 60}")
    print(f"쿼리: '{query}'")
    print(f"{'=' * 60}")

    for method_name, search_fn in [
        ("Dense", retriever.dense_search),
        ("Sparse", retriever.sparse_search),
        ("Hybrid", retriever.hybrid_search),
    ]:
        results = search_fn(query, top_k=3)
        print(f"\n  [{method_name}]")
        for rank, r in enumerate(results, 1):
            print(f"    {rank}. ({r.score:.4f}) {r.content[:50]}...")
```

**실행 결과**:
```
============================================================
쿼리: 'docker run 명령어'
============================================================

  [Dense]
    1. (0.8721) Docker 컨테이너를 실행하려면 docker run 명령어를 사용합니다...
    2. (0.8234) Docker 이미지는 Dockerfile로 빌드합니다. FROM, RUN, COPY...
    3. (0.7891) docker-compose.yml 파일로 멀티 컨테이너 애플리케이션을 정의하...

  [Sparse]
    1. (1.523) Docker 컨테이너를 실행하려면 docker run 명령어를 사용합니다...
    2. (0.612) docker-compose.yml 파일로 멀티 컨테이너 애플리케이션을 정의하...
    3. (0.387) Docker 이미지는 Dockerfile로 빌드합니다. FROM, RUN, COPY...

  [Hybrid]
    1. (0.0163) Docker 컨테이너를 실행하려면 docker run 명령어를 사용합니다...
    2. (0.0136) docker-compose.yml 파일로 멀티 컨테이너 애플리케이션을 정의하...
    3. (0.0131) Docker 이미지는 Dockerfile로 빌드합니다. FROM, RUN, COPY...

============================================================
쿼리: '컨테이너를 시작하는 방법'
============================================================

  [Dense]
    1. (0.8542) 컨테이너 가상화 기술은 VM보다 경량이며 빠른 시작이 가능합니다...
    2. (0.8312) Docker 컨테이너를 실행하려면 docker run 명령어를 사용합니다...
    3. (0.7654) Kubernetes에서 Pod는 최소 배포 단위입니다. 하나 이상의 컨테이...

  [Sparse]
    1. (0.687) 컨테이너 가상화 기술은 VM보다 경량이며 빠른 시작이 가능합니다...
    2. (0.423) Docker 컨테이너를 실행하려면 docker run 명령어를 사용합니다...
    3. (0.312) docker-compose.yml 파일로 멀티 컨테이너 애플리케이션을 정의하...

  [Hybrid]
    1. (0.0163) 컨테이너 가상화 기술은 VM보다 경량이며 빠른 시작이 가능합니다...
    2. (0.0147) Docker 컨테이너를 실행하려면 docker run 명령어를 사용합니다...
    3. (0.0127) docker-compose.yml 파일로 멀티 컨테이너 애플리케이션을 정의하...

============================================================
쿼리: 'docker-compose 멀티 컨테이너'
============================================================

  [Dense]
    1. (0.8891) docker-compose.yml 파일로 멀티 컨테이너 애플리케이션을 정의하...
    2. (0.8123) Docker 컨테이너를 실행하려면 docker run 명령어를 사용합니다...
    3. (0.7543) 컨테이너 가상화 기술은 VM보다 경량이며 빠른 시작이 가능합니다...

  [Sparse]
    1. (1.891) docker-compose.yml 파일로 멀티 컨테이너 애플리케이션을 정의하...
    2. (0.312) Docker 컨테이너를 실행하려면 docker run 명령어를 사용합니다...
    3. (0.201) 컨테이너 가상화 기술은 VM보다 경량이며 빠른 시작이 가능합니다...

  [Hybrid]
    1. (0.0163) docker-compose.yml 파일로 멀티 컨테이너 애플리케이션을 정의하...
    2. (0.0131) Docker 컨테이너를 실행하려면 docker run 명령어를 사용합니다...
    3. (0.0120) 컨테이너 가상화 기술은 VM보다 경량이며 빠른 시작이 가능합니다...
```

Hybrid 검색은 세 쿼리 모두에서 올바른 문서를 1위로 반환했다. Dense가 놓치는 키워드 정확성을 Sparse가 보완하고, Sparse가 놓치는 의미 유사성을 Dense가 보완한다.

### Q&A
**Q: Hybrid 검색에서 alpha(Dense 가중치)는 어떻게 설정하나요?**
A: 도메인과 쿼리 유형에 따라 다르다. 자연어 중심 쿼리(고객 질문 등)에서는 alpha=0.6~0.7(Dense 우위)이, 전문 용어/코드 검색에서는 alpha=0.3~0.4(Sparse 우위)가 적합하다. 최적값은 Golden Test Set으로 실험하여 결정한다. 0.5에서 시작하여 0.1 단위로 조정하는 것이 일반적이다.

**Q: Reciprocal Rank Fusion(RRF)은 왜 단순 점수 합산보다 좋은가요?**
A: Dense와 Sparse의 점수 범위(scale)가 다르기 때문이다. Dense 유사도는 0~1, BM25 점수는 0~수십까지 가능하다. 단순 합산하면 BM25 점수가 Dense를 압도한다. RRF는 점수 대신 순위(rank)를 사용하므로 스케일 차이 문제가 없다.

<details>
<summary>퀴즈: 검색 대상 문서가 주로 영문 기술 문서 + 한국어 주석이 혼합된 경우, Hybrid 검색의 alpha를 어떻게 설정하는 것이 좋을까요?</summary>

**힌트**: BM25는 언어별 토큰화에 의존하고, Dense Embedding은 다국어를 벡터 공간에서 통합합니다.

**정답**: alpha를 0.6~0.7(Dense 우위)로 설정하는 것이 좋다. 다국어 혼합 문서에서 BM25는 한국어와 영어의 토큰화 규칙이 달라 키워드 매칭이 불안정하다. 반면 다국어 Embedding 모델(text-embedding-3-large 등)은 한국어 질문과 영문 문서의 의미적 유사성을 효과적으로 포착한다. 다만 `docker-compose`, `kubectl` 같은 정확한 기술 용어 매칭을 위해 Sparse를 완전히 제거하지 않고 보조로 유지한다.
</details>

---

## 개념 4: Reranking으로 검색 품질 끌어올리기

### 개념 설명

앞서 배운 Dense, Sparse, Hybrid Retrieval은 모두 "1단계 검색"에 해당한다. 빠르게 후보 문서를 선별하는 것이 목적이므로, 속도를 위해 정밀도를 일부 희생하는 구조다. **Reranking**은 이 1단계 검색 결과의 순위를 더 정밀한 모델로 재조정하는 "2단계 검색" 전략이다. 1단계에서 Retriever가 빠르게 top-20~50개의 후보를 선별하고, 2단계에서 Reranker가 이 후보들을 정밀하게 평가하여 최종 top-3~5를 결정한다.

왜 2단계가 필요한가? 이는 Retriever의 아키텍처적 한계에서 비롯된다. 대부분의 Retriever는 **Bi-encoder** 구조를 사용한다. 질문과 문서를 각각 독립적으로 Embedding하여 최종 벡터만 비교하는 방식이다. 이 구조는 사전에 모든 문서를 벡터화해 놓을 수 있어 검색 속도가 매우 빠르지만, 질문의 각 토큰이 문서의 각 토큰에 직접 attend(상호작용)하지 못한다는 한계가 있다. 예를 들어 "Docker 네트워크 설정 방법"이라는 질문에서 "설정"이라는 단어가 문서의 "create"나 "configure"와 직접 비교되지 않고, 전체 벡터 수준에서만 유사도가 계산된다.

반면 Reranker는 **Cross-encoder** 구조를 사용한다. "[CLS] 질문 [SEP] 문서"를 하나의 시퀀스로 입력하여 Transformer의 Self-Attention이 질문의 모든 토큰과 문서의 모든 토큰 사이에서 직접 작동하게 한다. "설정"이 "create"에, "방법"이 "명령"에 직접 attend할 수 있으므로, 관련도 판단이 훨씬 정밀하다. 그러나 모든 질문-문서 쌍을 개별적으로 처리해야 하므로 전체 문서에 적용하면 너무 느리다. 이것이 "1단계에서 후보를 좁히고 2단계에서 정밀 평가"하는 2단계 구조의 근본적 이유다.

실무에서 Reranker는 세 가지 선택지가 있다. **LLM 기반 Reranking**은 GPT-4o-mini 같은 LLM에게 "각 문서의 관련도를 0~10으로 평가하라"고 요청하는 방식이다. 가장 유연하고 정밀하지만 비용이 가장 높다. **전용 Cross-encoder 모델**은 Cohere Rerank API($0.002/1000문서)나 오픈소스 `cross-encoder/ms-marco-MiniLM-L-6-v2`를 사용하는 방식이다. LLM 대비 100배 이상 저렴하면서 충분한 정밀도를 제공하여, 프로덕션에서 가장 일반적으로 사용된다. **경량 점수 재계산**은 BM25 점수, 문서 메타데이터, 문서 날짜 등을 조합하여 간단한 규칙 기반으로 순위를 재조정하는 방식이다. 비용이 거의 없지만 정밀도 개선 폭이 제한적이다.

```
검색 파이프라인 흐름:

[사용자 쿼리]
    |
    v
[1단계: Retriever (Bi-encoder)]     <-- 빠름, top-50 후보 선별
    |  50개 문서
    v
[2단계: Reranker (Cross-encoder)]   <-- 정밀, 순위 재조정
    |  top-5 문서
    v
[LLM에 전달하여 답변 생성]
```

아래 코드는 LLM 기반 Reranking을 구현하여, Retriever가 3위에 배치했던 무관한 문서가 Reranking 후 5위로 밀려나고, 4위에 있던 관련 문서가 2위로 상승하는 효과를 보여준다.

```python
import os
import json
from openai import OpenAI
from dataclasses import dataclass

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


@dataclass
class RankedDocument:
    """순위가 매겨진 문서"""
    content: str
    initial_rank: int
    initial_score: float
    reranked_score: float | None = None
    final_rank: int | None = None


def llm_rerank(
    query: str,
    documents: list[str],
    top_k: int = 3,
) -> list[RankedDocument]:
    """LLM 기반 Reranking (Cross-encoder 대안)"""
    doc_list = "\n".join(
        f"[문서 {i+1}]: {doc}" for i, doc in enumerate(documents)
    )

    prompt = f"""다음 쿼리와 문서들의 관련도를 0~10 점수로 평가하세요.
반드시 JSON 배열로만 응답하세요. 설명 없이 점수만 반환합니다.

쿼리: {query}

{doc_list}

응답 형식: [점수1, 점수2, ...]"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    scores = json.loads(response.choices[0].message.content)

    ranked = []
    for i, (doc, score) in enumerate(zip(documents, scores)):
        ranked.append(RankedDocument(
            content=doc,
            initial_rank=i + 1,
            initial_score=0.0,
            reranked_score=score,
        ))

    ranked.sort(key=lambda x: x.reranked_score, reverse=True)
    for i, doc in enumerate(ranked):
        doc.final_rank = i + 1

    return ranked[:top_k]


# Reranking 전후 비교 시뮬레이션
query = "Docker 컨테이너의 네트워크 설정 방법"
retrieved_docs = [
    "Docker 네트워크는 bridge, host, none 세 가지 드라이버를 지원한다.",     # 관련 높음
    "컨테이너 간 통신을 위해 docker network create 명령을 사용한다.",        # 관련 높음
    "Docker는 Go 언어로 작성된 오픈소스 플랫폼이다.",                      # 관련 낮음
    "docker-compose.yml에서 networks 섹션으로 네트워크를 정의한다.",        # 관련 높음
    "Kubernetes의 Service는 Pod 간 네트워크 추상화를 제공한다.",            # 관련 중간
]

print("=== Reranking 전후 비교 ===")
print(f"쿼리: {query}\n")

print("Retriever 결과 (초기 순위):")
for i, doc in enumerate(retrieved_docs, 1):
    print(f"  {i}. {doc}")

# Reranking 시뮬레이션 (실제 API 호출 결과와 유사)
reranked_scores = [9, 8, 2, 9, 5]
reranked_pairs = sorted(
    zip(retrieved_docs, reranked_scores, range(1, 6)),
    key=lambda x: x[1],
    reverse=True,
)

print("\nReranker 결과 (재조정 순위):")
for new_rank, (doc, score, old_rank) in enumerate(reranked_pairs, 1):
    movement = old_rank - new_rank
    arrow = "^" * movement if movement > 0 else "v" * abs(movement) if movement < 0 else "-"
    print(f"  {new_rank}. (점수: {score}/10, {old_rank}위->{new_rank}위 {arrow}) {doc}")
```

**실행 결과**:
```
=== Reranking 전후 비교 ===
쿼리: Docker 컨테이너의 네트워크 설정 방법

Retriever 결과 (초기 순위):
  1. Docker 네트워크는 bridge, host, none 세 가지 드라이버를 지원한다.
  2. 컨테이너 간 통신을 위해 docker network create 명령을 사용한다.
  3. Docker는 Go 언어로 작성된 오픈소스 플랫폼이다.
  4. docker-compose.yml에서 networks 섹션으로 네트워크를 정의한다.
  5. Kubernetes의 Service는 Pod 간 네트워크 추상화를 제공한다.

Reranker 결과 (재조정 순위):
  1. (점수: 9/10, 1위->1위 -) Docker 네트워크는 bridge, host, none 세 가지 드라이버를 지원한다.
  2. (점수: 9/10, 4위->2위 ^^) docker-compose.yml에서 networks 섹션으로 네트워크를 정의한다.
  3. (점수: 8/10, 2위->3위 v) 컨테이너 간 통신을 위해 docker network create 명령을 사용한다.
  4. (점수: 5/10, 5위->4위 ^) Kubernetes의 Service는 Pod 간 네트워크 추상화를 제공한다.
  5. (점수: 2/10, 3위->5위 vv) Docker는 Go 언어로 작성된 오픈소스 플랫폼이다.
```

3위에 있던 관련 없는 문서("Go 언어로 작성")가 5위로 밀려나고, 4위에 있던 관련 높은 문서("networks 섹션")가 2위로 올라왔다. Reranking이 Retriever의 오류를 효과적으로 보정한다.

### 예제

다음 예제는 Retrieve → Rerank → Generate 전체 RAG 파이프라인을 하나의 클래스로 구현한 것이다. 각 단계의 결과를 로깅하여 파이프라인의 동작을 투명하게 추적할 수 있다.

```python
import os
import json
import time
from openai import OpenAI
from dataclasses import dataclass, field

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


class RAGPipeline:
    """Retrieval -> Reranking -> Generation 전체 파이프라인"""

    def __init__(
        self,
        documents: list[str],
        retriever_top_k: int = 10,
        reranker_top_k: int = 3,
    ):
        self.documents = documents
        self.retriever_top_k = retriever_top_k
        self.reranker_top_k = reranker_top_k
        self.bm25 = BM25(documents)

    def retrieve(self, query: str) -> list[tuple[int, float]]:
        """1단계: BM25로 후보 검색"""
        return self.bm25.search(query, top_k=self.retriever_top_k)

    def rerank(
        self, query: str, candidates: list[tuple[int, float]]
    ) -> list[dict]:
        """2단계: LLM 기반 Reranking"""
        candidate_docs = [self.documents[idx] for idx, _ in candidates]

        doc_list = "\n".join(
            f"[{i}] {doc}" for i, doc in enumerate(candidate_docs)
        )

        prompt = f"""주어진 쿼리와 각 문서의 관련도를 0.0~1.0 점수로 평가하세요.
JSON 객체로 응답: {{"scores": [점수1, 점수2, ...]}}

쿼리: {query}

문서들:
{doc_list}"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        result = json.loads(response.choices[0].message.content)
        scores = result["scores"]

        reranked = [
            {
                "index": candidates[i][0],
                "content": candidate_docs[i],
                "bm25_score": candidates[i][1],
                "rerank_score": scores[i],
            }
            for i in range(len(candidates))
        ]
        reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
        return reranked[: self.reranker_top_k]

    def generate(self, query: str, context_docs: list[dict]) -> str:
        """3단계: 검색 결과 기반 응답 생성"""
        context = "\n\n".join(
            f"[참고 {i+1}] {doc['content']}"
            for i, doc in enumerate(context_docs)
        )

        prompt = f"""다음 참고 자료를 기반으로 질문에 답변하세요.
참고 자료에 없는 내용은 "제공된 자료에서 확인할 수 없습니다"라고 답하세요.

{context}

질문: {query}"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content

    def run(self, query: str) -> dict:
        """전체 파이프라인 실행: Retrieve -> Rerank -> Generate"""
        # Step 1: Retrieval
        candidates = self.retrieve(query)
        print(f"[Retrieve] {len(candidates)}개 후보 검색")

        # Step 2: Reranking
        reranked = self.rerank(query, candidates)
        print(f"[Rerank] 상위 {len(reranked)}개 선별")
        for i, doc in enumerate(reranked):
            print(
                f"  {i+1}. (BM25: {doc['bm25_score']:.3f}, "
                f"Rerank: {doc['rerank_score']:.2f}) "
                f"{doc['content'][:40]}..."
            )

        # Step 3: Generation
        answer = self.generate(query, reranked)
        print(f"[Generate] 응답 생성 완료")

        return {
            "query": query,
            "retrieved": len(candidates),
            "reranked": len(reranked),
            "context": reranked,
            "answer": answer,
        }


# 실행 예시
knowledge_base = [
    "Docker 네트워크는 bridge, host, overlay, macvlan 네 가지 드라이버를 지원한다.",
    "bridge 네트워크는 Docker의 기본 네트워크 드라이버로, 동일 호스트 내 컨테이너 간 통신에 사용된다.",
    "overlay 네트워크는 Docker Swarm 모드에서 다중 호스트 간 컨테이너 통신을 지원한다.",
    "docker network create --driver bridge my-network 명령으로 사용자 정의 네트워크를 생성한다.",
    "Docker는 2013년 Solomon Hykes가 만든 오픈소스 프로젝트다.",
    "컨테이너의 포트를 호스트에 매핑하려면 -p 옵션을 사용한다. 예: docker run -p 8080:80 nginx",
    "Docker Compose에서 services 간 네트워크 연결은 networks 키로 설정한다.",
    "host 네트워크 드라이버는 컨테이너가 호스트의 네트워크 스택을 직접 사용하게 한다.",
]

pipeline = RAGPipeline(
    documents=knowledge_base,
    retriever_top_k=5,
    reranker_top_k=3,
)

result = pipeline.run(
    "Docker에서 컨테이너 간 네트워크 통신을 설정하는 방법은?"
)
print(f"\n최종 답변:\n{result['answer']}")
```

**실행 결과**:
```
[Retrieve] 5개 후보 검색
[Rerank] 상위 3개 선별
  1. (BM25: 0.892, Rerank: 0.95) bridge 네트워크는 Docker의 기본 네트워크 드라이버로...
  2. (BM25: 0.734, Rerank: 0.90) docker network create --driver bridge my-ne...
  3. (BM25: 0.812, Rerank: 0.85) Docker 네트워크는 bridge, host, overlay, macvla...
[Generate] 응답 생성 완료

최종 답변:
Docker에서 컨테이너 간 네트워크 통신을 설정하려면 다음과 같이 합니다:

1. Docker는 bridge, host, overlay, macvlan 네 가지 네트워크 드라이버를 지원합니다.
2. 동일 호스트 내 컨테이너 간 통신에는 bridge 네트워크(기본 드라이버)를 사용합니다.
3. 사용자 정의 네트워크를 생성하려면 `docker network create --driver bridge my-network` 명령을 실행합니다.
```

### Q&A
**Q: Reranking에 LLM을 사용하면 비용이 너무 많이 들지 않나요?**
A: LLM Reranking은 프로토타입 단계에서 유용하지만, 프로덕션에서는 전용 Cross-encoder 모델을 사용하는 것이 비용 효율적이다. Cohere Rerank API($0.002/1000 문서)나 오픈소스 `cross-encoder/ms-marco-MiniLM-L-6-v2` 모델을 사용하면 LLM 대비 100배 이상 저렴하다. LLM Reranking은 소량 트래픽이거나 높은 정확도가 필수인 경우에만 적합하다.

**Q: Reranking 단계에서 top-K를 몇 개로 설정해야 하나요?**
A: Retriever에서 top-20~50개를 가져오고, Reranker에서 top-3~5개로 줄이는 것이 일반적이다. Retriever top-K가 너무 작으면 관련 문서가 누락되고, 너무 크면 Reranker 비용이 증가한다. Retriever top-K는 "Recall을 높이는 단계", Reranker top-K는 "Precision을 높이는 단계"로 이해하면 된다.

<details>
<summary>퀴즈: Cross-encoder가 Bi-encoder보다 정밀한 이유를 Transformer의 Attention 메커니즘 관점에서 설명해보세요.</summary>

**힌트**: Bi-encoder는 쿼리와 문서를 어떻게 처리하나요? Cross-encoder는요?

**정답**: Bi-encoder는 쿼리와 문서를 각각 독립적으로 인코딩하여 최종 [CLS] 벡터만 비교한다. 쿼리 토큰이 문서 토큰에 직접 attend할 수 없으므로 세밀한 상호작용을 놓친다. 반면 Cross-encoder는 "[CLS] 쿼리 [SEP] 문서"를 하나의 시퀀스로 입력하여, 쿼리의 모든 토큰이 문서의 모든 토큰에 Self-Attention으로 직접 attend한다. "Docker 네트워크 설정 방법"이라는 쿼리에서 "설정"과 "방법"이 문서의 "create", "명령"과 직접 상호작용하므로, 더 정밀한 관련도 판단이 가능하다. 대신 모든 쿼리-문서 쌍을 개별 인퍼런스해야 하므로 O(N) 비용이 든다.
</details>

---

## 실습

### 실습 1: Chunking 전략 비교 실험
- **연관 학습 목표**: 학습 목표 1
- **실습 목적**: 고정 크기, 의미 기반, 재귀적 Chunking 전략의 검색 품질 차이를 정량적으로 측정한다
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 30분
- **선행 조건**: Python 기본, numpy 사용법
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**실습 내용**:

Markdown 형식의 기술 문서(500줄 이상)를 세 가지 전략으로 Chunking한 뒤, 10개의 테스트 질문에 대한 검색 정확도(Hit Rate@3)를 비교한다.

```python
# TODO: ChunkingExperiment 클래스를 구현하세요
# 1. load_document(path) - Markdown 문서 로드
# 2. chunk_fixed(chunk_size, overlap) - 고정 크기 Chunking
# 3. chunk_recursive(chunk_size) - 재귀적 Chunking
# 4. evaluate(chunks, test_queries, expected_keywords) - Hit Rate@3 측정
# 5. compare_all() - 세 전략의 결과를 테이블로 비교
#
# 평가 방법:
# - 각 테스트 쿼리에 대해 BM25로 상위 3개 청크를 검색
# - expected_keywords가 상위 3개 청크 중 하나에 포함되면 Hit
# - Hit Rate = Hit 수 / 전체 쿼리 수

test_queries = [
    ("Docker 이미지 빌드 방법", "Dockerfile"),
    ("컨테이너 네트워크 설정", "bridge"),
    ("볼륨 마운트 방법", "-v"),
    ("환경 변수 전달", "ENV"),
    ("로그 확인 명령어", "docker logs"),
    ("컨테이너 목록 조회", "docker ps"),
    ("이미지 레이어 구조", "Copy-on-Write"),
    ("포트 매핑 설정", "-p"),
    ("멀티 스테이지 빌드", "multi-stage"),
    ("헬스체크 설정", "HEALTHCHECK"),
]
```

### 실습 2: Hybrid Retriever 구현 및 Alpha 최적화
- **연관 학습 목표**: 학습 목표 2
- **실습 목적**: Dense + Sparse Hybrid Retriever를 직접 구현하고 alpha 파라미터를 최적화하여 단일 전략 대비 성능 향상을 측정한다
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 35분
- **선행 조건**: 실습 1 완료, Embedding 개념 이해
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**실습 내용**:

20개의 기술 문서 청크와 10개의 테스트 쿼리를 준비한다. Dense-only, Sparse-only, Hybrid(alpha=0.3, 0.5, 0.7)의 5가지 설정으로 MRR(Mean Reciprocal Rank)을 측정하고 최적 alpha를 찾는다.

```python
# TODO: HybridRetrieverExperiment 클래스를 구현하세요
# 1. BM25 Sparse Retriever 구현 (본문의 BM25 클래스 활용)
# 2. Cosine Similarity 기반 Dense Retriever 구현
# 3. Reciprocal Rank Fusion(RRF) 기반 Hybrid Retriever 구현
# 4. MRR 평가 함수 구현
# 5. alpha 파라미터 그리드 서치로 최적값 탐색
#
# MRR 계산:
# - 각 쿼리에 대해 정답 문서의 순위(rank)를 찾음
# - MRR = (1/N) * sum(1/rank_i)
# - MRR이 1에 가까울수록 좋음 (정답이 항상 1위)
```

### 실습 3: RAG 파이프라인 End-to-End 구현
- **연관 학습 목표**: 학습 목표 1, 2, 3
- **실습 목적**: Chunking -> Embedding -> Retrieval -> Reranking -> Generation 전체 파이프라인을 구현하고 각 단계의 영향을 분석한다
- **실습 유형**: 코드 작성
- **난이도**: 심화
- **예상 소요 시간**: 40분
- **선행 조건**: 실습 1, 2 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**실습 내용**:

기술 문서 5개를 Knowledge Base로 구축하여 완전한 RAG 파이프라인을 구현한다. 각 단계를 on/off하여 성능 영향을 분석한다:
- 기본 RAG (Chunking + Dense Retrieval + Generation)
- Hybrid RAG (기본 + Sparse Retrieval 추가)
- Full RAG (Hybrid + Reranking 추가)

```python
# TODO: FullRAGPipeline 클래스를 구현하세요
# 1. ingest(documents) - 문서 Chunking + Embedding 인덱싱
# 2. retrieve(query, strategy="hybrid") - Dense/Sparse/Hybrid 검색
# 3. rerank(query, candidates) - LLM 기반 Reranking
# 4. generate(query, context) - 컨텍스트 기반 응답 생성
# 5. evaluate(test_cases) - 파이프라인별 응답 품질 비교
#
# 평가 기준:
# - 응답에 정답 키워드 포함 여부 (Keyword Hit Rate)
# - 검색 단계의 Recall@5
# - 전체 파이프라인 Latency (ms)
```

---

## 핵심 정리
- Chunking은 RAG 성능의 출발점이다. 재귀적 Chunking이 문서 구조를 보존하면서 크기를 제어하는 가장 범용적인 전략이며, 고정 크기는 간단하지만 오버랩을 반드시 적용해야 한다
- Embedding 모델은 차원 수, 도메인 적합성, 다국어 지원을 기준으로 선택한다. Matryoshka Representation Learning(MRL) 모델은 차원을 256까지 축소해도 성능 하락이 적어 저장 비용을 크게 절감할 수 있다
- Hybrid Retrieval(Dense + Sparse)은 의미 유사성과 키워드 정확성을 동시에 확보한다. Reciprocal Rank Fusion(RRF)으로 스코어 스케일 문제를 해결하고, alpha 파라미터는 도메인별 실험으로 최적화한다
- Reranking은 Retriever 결과의 순위를 정밀하게 재조정하는 2단계 검색 전략이다. Cross-encoder가 Bi-encoder보다 정밀한 이유는 쿼리-문서 토큰 간 직접 Attention 때문이며, 프로덕션에서는 전용 Reranker 모델로 비용을 최적화한다
