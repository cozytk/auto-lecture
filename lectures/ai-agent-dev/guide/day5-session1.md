# Session 1: 프로젝트 설계 확정 (2h)

## 학습 목표
1. 실무 문제를 AI Agent로 해결할 수 있는 문제 정의서를 완성할 수 있다
2. MCP/RAG/Hybrid 아키텍처 중 문제에 적합한 구조를 선택하고 기술적 근거를 설명할 수 있다
3. Golden Test Set과 평가 기준을 포함한 MVP 범위를 정의하고 프로젝트 설계서를 작성할 수 있다

---

## 활동 1: MVP 프로젝트 주제 선정

### 설명

Day 5는 프로젝트 데이다. Day 1~4에서 학습한 모든 내용을 종합하여 실제 동작하는 Agent MVP를 완성한다. 가장 흔한 실패 원인은 **"범위가 너무 넓은 주제 선정"**이다. 2시간 구현 + 1시간 개선 + 1시간 발표라는 시간 제약 안에서 동작하는 결과물을 만들려면, 주제를 극단적으로 좁혀야 한다.

**MVP 방법론의 본질: 왜 범위 축소가 프로젝트 성공의 핵심인가**

MVP(Minimum Viable Product)라는 용어는 에릭 리스(Eric Ries)의 린 스타트업(Lean Startup) 방법론에서 유래했다. 핵심 아이디어는 "완벽한 제품을 오래 만드는 것보다, 핵심 가설을 검증할 수 있는 최소한의 제품을 빠르게 만들어 피드백을 받는 것이 낫다"는 것이다. 이 원리를 AI Agent 프로젝트에 적용하면, "Agent가 모든 상황에서 완벽하게 동작하는 것"이 아니라 "Agent가 핵심 시나리오 하나에서 확실하게 동작하는 것"을 목표로 삼아야 한다.

소프트웨어 프로젝트의 실패 원인을 분석한 연구들(Standish Group CHAOS Report 등)은 일관되게 "범위 초과(scope creep)"를 최대 실패 요인으로 꼽는다. 특히 시간이 제한된 프로젝트에서는 이 경향이 극대화된다. "많은 기능을 절반만 구현한 프로젝트"와 "하나의 기능을 완벽하게 구현한 프로젝트" 사이에서, 실무 평가와 사용자 만족도 모두 후자가 압도적으로 높다. 그 이유는 절반만 구현된 기능은 데모조차 불가능하지만, 완벽하게 구현된 하나의 기능은 전체 시스템의 가능성을 보여주기 때문이다.

문제를 좁힐 때는 세 가지 축을 기준으로 한다. 첫째, 데이터 범위를 제한한다(전체 문서가 아닌 특정 도메인 50건). 둘째, 사용자 시나리오를 단일 흐름으로 고정한다(멀티턴이 아닌 싱글턴). 셋째, 출력 형식을 최소화한다(답변 + 출처만 반환, 요약이나 추천은 제외). 이 세 축을 동시에 좁히면 구현 복잡도가 기하급수적으로 줄어들며, 2시간이라는 제약 안에서 실제로 동작하는 결과물을 만들 수 있게 된다. "이 Agent가 반드시 해결해야 하는 단 하나의 시나리오는 무엇인가?"라는 질문에 한 문장으로 답할 수 있을 때까지 범위를 좁혀야 한다.

**5가지 추천 MVP 주제**

| # | 주제 | 아키텍처 | 2h 구현 범위 | 핵심 도전 |
|---|------|---------|-------------|-----------|
| 1 | 사내 문서 Q&A Agent | RAG | FAQ 50건 대상, 단일 도메인 | Chunking + Retrieval 품질 |
| 2 | DevOps 장애 진단 Agent | MCP | 로그 조회 + 원인 분류 3종 | Tool 설계 + 에러 핸들링 |
| 3 | 코드 리뷰 Agent | Hybrid | Python 파일 1개 대상 리뷰 | RAG(규칙 문서) + MCP(GitHub API) |
| 4 | 데이터 분석 Agent | MCP | CSV 1개 대상 기본 분석 | Tool 체이닝 + 시각화 |
| 5 | 고객 문의 분류/응답 Agent | RAG | 카테고리 5종, 응답 템플릿 10종 | Intent 분류 + 적합 응답 매칭 |

각 주제를 구체적으로 살펴보자.

```python
from dataclasses import dataclass


@dataclass
class MVPProject:
    """MVP 프로젝트 주제 정의."""
    name: str
    architecture: str       # "MCP" | "RAG" | "Hybrid"
    pain_point: str
    mvp_scope: str
    must_have: list[str]
    nice_to_have: list[str]
    estimated_difficulty: str  # "기초" | "중급" | "심화"


recommended_projects = [
    MVPProject(
        name="사내 문서 Q&A Agent",
        architecture="RAG",
        pain_point="신입 개발자가 사내 위키에서 답을 찾는 데 평균 15분 소요",
        mvp_scope="특정 팀 문서 50건 대상, 단일 질문 -> 답변 + 출처",
        must_have=[
            "문서 로딩 + 청킹 + 임베딩 파이프라인",
            "자연어 질문 -> 관련 문서 검색",
            "검색 결과 기반 답변 생성 + 출처 표시",
        ],
        nice_to_have=[
            "멀티턴 대화 지원",
            "답변 신뢰도 점수 표시",
            "문서 업데이트 자동 감지",
        ],
        estimated_difficulty="중급",
    ),
    MVPProject(
        name="DevOps 장애 진단 Agent",
        architecture="MCP",
        pain_point="장애 발생 시 로그 분석 -> 원인 파악에 평균 30분 소요",
        mvp_scope="3가지 장애 유형(OOM, 타임아웃, 인증 실패) 진단",
        must_have=[
            "로그 조회 Tool (mock API)",
            "장애 유형 분류 로직",
            "원인 분석 + 해결 방안 제시",
        ],
        nice_to_have=[
            "실시간 메트릭 연동",
            "자동 복구 명령 실행",
            "Slack 알림 전송",
        ],
        estimated_difficulty="중급",
    ),
    MVPProject(
        name="코드 리뷰 Agent",
        architecture="Hybrid",
        pain_point="코드 리뷰에 평균 40분 소요, 반복되는 패턴 지적이 많음",
        mvp_scope="Python 파일 1개 대상, 보안/성능/스타일 3관점 리뷰",
        must_have=[
            "코드 파일 읽기 Tool",
            "코딩 컨벤션 문서 RAG 검색",
            "3관점 리뷰 코멘트 생성",
        ],
        nice_to_have=[
            "GitHub PR 연동",
            "자동 수정 제안",
            "리뷰 히스토리 학습",
        ],
        estimated_difficulty="심화",
    ),
    MVPProject(
        name="데이터 분석 Agent",
        architecture="MCP",
        pain_point="비개발자가 데이터 분석을 요청할 때마다 개발자 시간 소요",
        mvp_scope="CSV 1개 대상, 기본 통계 + 차트 생성",
        must_have=[
            "CSV 로딩 + 기본 통계 Tool",
            "자연어 질문 -> 분석 코드 생성",
            "결과 요약 텍스트 생성",
        ],
        nice_to_have=[
            "차트 시각화",
            "복합 질문 처리",
            "분석 보고서 자동 생성",
        ],
        estimated_difficulty="중급",
    ),
    MVPProject(
        name="고객 문의 분류/응답 Agent",
        architecture="RAG",
        pain_point="고객 문의 분류와 초기 응답에 CS팀 시간의 40% 소요",
        mvp_scope="카테고리 5종, 응답 템플릿 10종 대상",
        must_have=[
            "문의 내용 -> 카테고리 분류",
            "카테고리별 응답 템플릿 RAG 검색",
            "맞춤 응답 생성",
        ],
        nice_to_have=[
            "감성 분석 (긴급도 판단)",
            "에스컬레이션 자동 라우팅",
            "응답 만족도 피드백 수집",
        ],
        estimated_difficulty="기초",
    ),
]

for p in recommended_projects:
    print(f"[{p.architecture}] {p.name} ({p.estimated_difficulty})")
    print(f"  Pain: {p.pain_point}")
    print(f"  MVP: {p.mvp_scope}")
    print(f"  Must Have: {len(p.must_have)}개 | Nice to Have: {len(p.nice_to_have)}개")
    print()
```

```
실행 결과:
[RAG] 사내 문서 Q&A Agent (중급)
  Pain: 신입 개발자가 사내 위키에서 답을 찾는 데 평균 15분 소요
  MVP: 특정 팀 문서 50건 대상, 단일 질문 -> 답변 + 출처
  Must Have: 3개 | Nice to Have: 3개

[MCP] DevOps 장애 진단 Agent (중급)
  Pain: 장애 발생 시 로그 분석 -> 원인 파악에 평균 30분 소요
  MVP: 3가지 장애 유형(OOM, 타임아웃, 인증 실패) 진단
  Must Have: 3개 | Nice to Have: 3개

[Hybrid] 코드 리뷰 Agent (심화)
  Pain: 코드 리뷰에 평균 40분 소요, 반복되는 패턴 지적이 많음
  MVP: Python 파일 1개 대상, 보안/성능/스타일 3관점 리뷰
  Must Have: 3개 | Nice to Have: 3개

[MCP] 데이터 분석 Agent (중급)
  Pain: 비개발자가 데이터 분석을 요청할 때마다 개발자 시간 소요
  MVP: CSV 1개 대상, 기본 통계 + 차트 생성
  Must Have: 3개 | Nice to Have: 3개

[RAG] 고객 문의 분류/응답 Agent (기초)
  Pain: 고객 문의 분류와 초기 응답에 CS팀 시간의 40% 소요
  MVP: 카테고리 5종, 응답 템플릿 10종 대상
  Must Have: 3개 | Nice to Have: 3개
```

**주제 선정 의사결정 트리**

```
[경험 수준 확인]
    |
    +-- LLM API 처음 --> 고객 문의 분류/응답 Agent (기초, RAG)
    |
    +-- LLM API 경험 있음
    |   |
    |   +-- 외부 API 연동 경험 --> DevOps 장애 진단 Agent (중급, MCP)
    |   |                         데이터 분석 Agent (중급, MCP)
    |   |
    |   +-- RAG 경험 있음 --> 사내 문서 Q&A Agent (중급, RAG)
    |
    +-- 둘 다 경험 있음 --> 코드 리뷰 Agent (심화, Hybrid)
```

**자체 주제를 정할 때의 체크리스트**

추천 주제 대신 자체 주제를 선정할 경우, 반드시 아래 기준을 충족해야 한다.

| # | 체크 항목 | 통과 기준 |
|---|----------|----------|
| 1 | 2시간 내 구현 가능한가? | Must Have 기능 3개 이하 |
| 2 | 데이터/API가 준비되어 있는가? | Mock이라도 즉시 사용 가능 |
| 3 | 테스트 가능한가? | 입력 -> 출력이 명확하여 자동 평가 가능 |
| 4 | Agent가 적합한가? | 멀티스텝 + 동적 판단 + 도구 활용 중 2개 이상 충족 |
| 5 | 데모 가능한가? | 30초 내에 핵심 기능을 시연 가능 |

### Q&A

**Q: 추천 주제 중에 제 업무와 맞는 게 없으면 어떡하나요?**
A: 추천 주제는 출발점이지 제약이 아니다. 자체 주제를 정해도 좋다. 다만 위의 체크리스트를 반드시 통과해야 한다. 실무에서 가장 흔한 실패는 "내 실제 업무 전체를 Agent로 만들겠다"는 범위 확장이다. 실제 업무의 **가장 작은 반복 단위 하나**만 선택하라.

**Q: 팀 프로젝트도 가능한가요?**
A: 이 과정에서는 개인 프로젝트를 기본으로 한다. 개인 프로젝트여야 각자의 설계 판단과 구현 능력을 온전히 평가할 수 있다. 다만 설계 단계에서 동료와 아이디어를 논의하고 피드백을 주고받는 것은 적극 권장한다.

<details>
<summary>퀴즈: 다음 중 MVP 주제로 가장 부적합한 것은?</summary>

**보기:**
1. "Slack 채널의 미해결 질문을 모아서 정리해주는 Agent"
2. "모든 사내 시스템을 통합 관리하는 범용 AI 비서"
3. "이력서 PDF에서 핵심 정보를 추출하는 Agent"
4. "Git 커밋 메시지를 분석하여 주간 보고서를 생성하는 Agent"

**힌트**: MVP의 핵심은 "가장 작은 동작하는 단위"이다. 범위가 명확하지 않은 주제를 찾아보자.

**정답**: 2번. "모든 사내 시스템을 통합 관리"는 범위가 무한정 넓다. "범용 AI 비서"는 성공 기준 정의가 불가능하다. 나머지는 모두 입력/출력이 명확하고 2시간 내 MVP 구현이 가능한 범위로 좁힐 수 있다.
</details>

---

## 활동 2: 아키텍처 결정 -- MCP / RAG / Hybrid 선택

### 설명

Day 1 Session 4에서 학습한 아키텍처 판단 기준을 실제 프로젝트에 적용한다. 핵심은 **"내 문제에 왜 이 구조가 적합한가"를 명확히 설명하는 것**이다. 가장 복잡한 구조를 선택하는 것이 좋은 점수를 받는 것이 아니라, 문제에 가장 적합한 구조를 선택하고 그 근거를 논리적으로 설명할 수 있어야 한다.

**아키텍처 결정의 본질: 트레이드오프 사고와 ADR**

소프트웨어 아키텍처에는 "정답"이 존재하지 않는다. 모든 아키텍처는 트레이드오프를 수반하며, 좋은 아키텍트는 자신의 선택이 무엇을 얻고 무엇을 포기하는지를 명확하게 설명할 수 있는 사람이다. 이를 체계적으로 문서화하는 방법이 ADR(Architecture Decision Record)이다.

ADR은 "왜 이 결정을 내렸는가"를 기록하는 짧은 문서이다. 제목, 상태, 맥락(Context), 결정(Decision), 결과(Consequences)의 다섯 요소로 구성된다. 예를 들어 "MCP 구조를 선택한다"라는 결정만 남기면, 나중에 "왜 RAG를 안 쓰고 MCP를 택했지?"라는 의문에 답할 수 없다. 하지만 ADR에 "문서 검색이 필요 없고 외부 API 3개를 호출하는 것이 핵심이므로 MCP가 적합하다. RAG를 택하면 불필요한 임베딩 파이프라인이 추가된다"고 적어두면, 이 결정의 배경과 근거가 명확해진다. MVP처럼 빠르게 진행하는 프로젝트에서도 ADR을 남기면, Session 3에서 구조를 변경해야 할 때 과거 판단을 빠르게 리뷰할 수 있다.

세 가지 아키텍처 선택지의 트레이드오프를 구체적으로 비교해보자. MCP(Function Calling)는 Agent가 외부 시스템을 "행동"하는 데 초점이 맞춰져 있다. API 호출, DB 쿼리, 파일 조작처럼 LLM이 직접 수행할 수 없는 작업을 도구(Tool)로 위임하는 패턴이다. 핵심 장점은 구현이 직관적이고 디버깅이 용이하다는 것이며, 핵심 단점은 도구가 늘어날수록 LLM의 도구 선택 정확도가 떨어진다는 것이다. RAG는 Agent가 외부 지식을 "참조"하는 데 초점이 맞춰져 있다. 대량의 문서에서 관련 정보를 검색하고 이를 기반으로 답변을 생성하는 패턴이다. 핵심 장점은 LLM의 지식 한계를 극복할 수 있다는 것이며, 핵심 단점은 데이터 전처리(청킹, 임베딩)에 상당한 시간이 필요하다는 것이다. Hybrid는 양쪽의 장점을 결합하지만 복잡도가 급격히 상승한다. MVP에서 Hybrid를 선택하려면 반드시 범위를 극도로 좁혀야 한다. 예를 들어 "문서를 검색한 뒤 API를 호출하는" 단일 워크플로우 하나에 집중하는 것이 현실적이다.

이 선택에서 흔히 저지르는 실수가 있다. 바로 "미래의 확장성"을 고려하여 처음부터 Hybrid를 선택하는 것이다. MVP 단계에서는 확장성보다 동작 가능성이 우선이다. 단순한 MCP 구조로 시작하여 핵심 기능을 검증한 뒤, 필요시 RAG를 추가하는 것이 실패 리스크를 최소화하는 접근이다.

**아키텍처 선택 의사결정 트리**

```
[문제 유형 판별]
    |
    +-- 외부 시스템 제어가 핵심인가? --YES--> MCP (Function Calling) 중심
    |   예: DB 조회, API 호출, 파일 조작, 명령 실행
    |
    +-- 대량 문서에서 정보 추출이 핵심인가? --YES--> RAG 중심
    |   예: 문서 Q&A, 지식 검색, 매뉴얼 안내
    |
    +-- 둘 다 필요한가? --YES--> Hybrid
        예: 문서 검색 후 API로 예약, 매뉴얼 참조 후 설정 변경
```

**구조별 MVP 구현 비교**

| 구조 | 2h MVP 난이도 | 핵심 구현 포인트 | 주의사항 |
|------|-------------|----------------|---------|
| MCP | 중 | Tool 정의 3~5개 + Router | Tool 정의 품질이 성능 좌우 |
| RAG | 중~상 | Chunking + Embedding + Retrieval | 데이터 전처리 시간 확보 필요 |
| Hybrid | 상 | RAG + MCP 통합 + 분기 로직 | 범위를 극도로 좁혀야 가능 |

**구조별 아키텍처 다이어그램 템플릿**

```python
architectures = {
    "MCP": """
    [사용자 입력]
         |
         v
    +----------+    +--------------------------+
    |  Agent   |--->|  Tool Router (LLM 판단)  |
    |  (LLM)  |    +------------+-------------+
    +----------+                |
                    +-----------+-----------+
                    v           v           v
              [Tool A]   [Tool B]   [Tool C]
                    |           |           |
                    +-----------+-----------+
                                v
                          [최종 응답]
    """,
    "RAG": """
    [사용자 질문]
         |
         v
    +----------+    +--------------+    +----------+
    | Embedding|--->|  Vector DB   |--->| Top-K    |
    |          |    |  (검색)      |    | 문서     |
    +----------+    +--------------+    +----+-----+
                                             |
                                             v
                                   +--------------+
                                   |  LLM 답변    |
                                   |  (컨텍스트   |
                                   |   기반 생성) |
                                   +--------------+
    """,
    "Hybrid": """
    [사용자 입력]
         |
         v
    +--------------+
    |  Intent      |
    |  Classifier  |
    +------+-------+
           |
     +-----+-----+
     v           v
  [정보 검색]  [작업 실행]
     |           |
     v           v
  [RAG]       [MCP Tool]
     |           |
     +-----+-----+
           v
     [결과 통합]
     [최종 응답]
    """,
}

for name, diagram in architectures.items():
    print(f"=== {name} 아키텍처 ===")
    print(diagram)
```

**아키텍처 선택 근거 작성 템플릿**

```markdown
## 아키텍처 선택: {MCP / RAG / Hybrid}

### 선택 근거
1. **문제 특성**: {왜 이 구조가 적합한지}
2. **데이터 특성**: {입력 데이터의 형태와 양}
3. **시간 제약**: {2h 내 구현 가능한 이유}

### 대안 검토
- **{대안 구조}를 선택하지 않은 이유**: {구체적 근거}

### 핵심 컴포넌트
| 컴포넌트 | 역할 | 구현 방법 |
|---------|------|----------|
| {컴포넌트1} | {역할} | {구현 기술} |
| {컴포넌트2} | {역할} | {구현 기술} |

### 아키텍처 다이어그램
```
{텍스트 기반 다이어그램}
```
```

### Q&A

**Q: Hybrid가 가장 좋은 구조 아닌가요? 왜 단일 구조를 추천하나요?**
A: Hybrid는 가장 유연하지만 가장 복잡하다. MVP에서는 "동작하는 것"이 최우선이다. MCP만으로 충분한 문제에 RAG를 추가하면 불필요한 복잡도만 늘어난다. 발표 평가의 "아키텍처 적합성"은 "가장 복잡한 구조"가 아니라 "문제에 가장 적합한 구조"를 선택했는지를 평가한다. 단순한 MCP 구조라도 선택 근거가 명확하면 높은 점수를 받는다.

**Q: 아키텍처를 구현 중간에 바꿔도 되나요?**
A: 가능은 하지만 시간 리스크가 크다. 설계 단계에서 충분히 고민하는 것이 중요하다. 만약 구현 중 아키텍처 변경이 필요하다면, (1) Must Have 기능 중 완성된 것을 보존하면서 변경하고, (2) 변경 사유를 발표 시 설명하면 오히려 "적응적 의사결정"으로 긍정적으로 평가받을 수 있다.

<details>
<summary>퀴즈: "사내 회의실 예약 Agent"에 적합한 아키텍처는?</summary>

**힌트**: 이 Agent가 다루는 핵심 동작(예약 생성, 조회, 취소)의 성격을 생각해보자.

**정답**: MCP(Function Calling) 중심이 적합하다. 회의실 예약은 (1) 예약 시스템 API 호출이 핵심이고, (2) 대량 문서 검색이 불필요하며, (3) Tool 정의(예약 조회, 생성, 취소, 빈 회의실 검색)가 명확하다. RAG가 필요한 경우는 "회의실 이용 규정"을 참조해야 할 때인데, 이는 MVP 범위에서 제외하고 규정을 System Prompt에 포함하는 것으로 충분하다.
</details>

---

## 활동 3: 프로젝트 설계 문서 작성

### 설명

아키텍처를 선택했으면, 구체적인 설계 문서를 작성한다. 설계 문서는 Session 2~3의 구현 가이드이자, Session 4 발표의 근거 자료가 된다. **설계서 작성에 30분을 투자하면 구현 시간을 1시간 이상 절약한다.**

**Walking Skeleton: MVP보다 먼저 세워야 할 뼈대**

설계 문서를 작성하기 전에 반드시 이해해야 할 개념이 Walking Skeleton(걷는 뼈대)이다. 앨리스터 코번(Alistair Cockburn)이 제안한 이 개념은 "아키텍처의 모든 주요 레이어를 관통하는, 가장 얇은 end-to-end 구현"을 뜻한다. 예를 들어 RAG Agent라면, 입력 -> 임베딩 -> 검색 -> LLM 호출 -> 출력이라는 전체 파이프라인을 하드코딩된 더미 데이터로라도 먼저 관통시키는 것이다. 이 단계에서는 각 레이어의 품질이 아닌 연결이 핵심이다.

Walking Skeleton을 먼저 세우는 이유는 크게 세 가지이다. 첫째, 통합 리스크의 조기 발견이다. 개별 모듈을 완벽하게 만들어놓고 나중에 합치면 인터페이스 불일치, 데이터 형식 차이 등으로 통합에 예상 외의 시간이 걸린다. Walking Skeleton은 이 통합 문제를 프로젝트 초반에 드러내준다. 둘째, 심리적 안전감이다. 전체 파이프라인이 연결되어 "돌아가는 것"을 확인하면, 이후 각 모듈을 개선하는 과정에서 자신감이 생긴다. 셋째, 데모 가능성이다. Walking Skeleton만으로도 기본적인 데모가 가능하므로, 최악의 경우 시간이 부족해도 발표할 결과물이 존재한다.

설계서에서 "Must Have"와 "Nice to Have"를 구분하는 것은 단순한 우선순위 분류가 아니다. 이 구분은 시간 압박 속에서 의사결정 비용을 줄이는 장치이다. 구현 도중 "이 기능을 넣을까 말까"를 고민하는 시간 자체가 낭비이다. 사전에 명확하게 분류해두면, 남은 시간에 따라 기계적으로 판단할 수 있다. Must Have는 "이것이 없으면 Agent가 아니다"라고 말할 수 있는 기능만 포함해야 하며, 보통 2~3개를 넘지 않는다. 타임라인 설계에서도 구현에 모든 시간을 쏟고 테스트와 발표 준비에 시간이 부족해지는 실수를 피해야 한다. 경험적으로 가장 효과적인 시간 배분은 구현 50%, 테스트/개선 25%, 발표 준비 25%이다.

**MVP 프로젝트 설계서 전체 템플릿**

```markdown
# MVP 프로젝트 설계서

## 프로젝트 개요
- **프로젝트명**: {이름}
- **한 줄 설명**: {Agent가 하는 일을 한 문장으로}
- **팀원**: {이름}
- **날짜**: {작성일}

## 1. 문제 정의
- **Pain Point**: {구체적 고통 서술 + 수치}
- **현재 해결 방식**: {수동/기존 방식의 한계}
- **목표 사용자**: {구체적 페르소나}
- **입력**: {사용자가 제공하는 것}
- **출력**: {Agent가 반환하는 것}
- **핵심 가치**: {왜 Agent여야 하는가}

## 2. 아키텍처
- **선택**: {MCP / RAG / Hybrid}
- **선택 근거**: {왜 이 구조인가}
- **대안 검토**: {다른 구조를 배제한 이유}
- **아키텍처 다이어그램**:
```
{텍스트 다이어그램}
```

## 3. 기술 스택
| 항목 | 선택 | 이유 |
|------|------|------|
| LLM | Kimi-K2 (OpenRouter) | 과정 표준 |
| Framework | {LangGraph / 직접 구현} | {이유} |
| Vector DB | {FAISS / ChromaDB / 없음} | {이유} |
| 외부 API | {사용할 API 목록} | {이유} |

## 4. MVP 기능 목록
### 반드시 구현 (Must Have)
- [ ] {기능 1}: {상세 설명}
- [ ] {기능 2}: {상세 설명}
- [ ] {기능 3}: {상세 설명}

### 가능하면 구현 (Nice to Have)
- [ ] {기능 4}: {상세 설명}
- [ ] {기능 5}: {상세 설명}

## 5. API 설계
### 주요 함수 시그니처
```python
def run_agent(query: str) -> AgentResponse:
    """Agent 메인 실행 함수."""
    ...
```

### Tool 정의 (MCP/Hybrid)
| Tool 이름 | 입력 | 출력 | 설명 |
|----------|------|------|------|

### 데이터 스키마 (RAG/Hybrid)
| 필드 | 타입 | 설명 |
|------|------|------|

## 6. 평가 체계
### 평가 기준
| 항목 | 가중치 | 측정 방법 | 목표값 |
|------|--------|----------|--------|

### Golden Test Set
| ID | 카테고리 | 질문 | 기대 답변 | 난이도 |
|----|---------|------|----------|--------|

## 7. 타임라인
| 시간 | 활동 | 산출물 |
|------|------|--------|
| Session 2 전반 (1h) | 핵심 기능 구현 | 동작하는 프로토타입 |
| Session 2 후반 (1h) | Validation + 테스트 | 기본 테스트 통과 |
| Session 3 전반 (1h) | Golden Test 평가 + 개선 | 평가 리포트 v1 |
| Session 3 후반 (1h) | 안정화 + 발표 준비 | 최종 코드 + 발표자료 |

## 8. 리스크
| 리스크 | 영향 | 대응 방안 |
|--------|------|----------|
```

**설계 문서 작성 예시 -- DevOps 장애 진단 Agent**

```python
"""설계 문서 예시: DevOps 장애 진단 Agent의 핵심 부분."""

design_doc = {
    "project_name": "DevOps 장애 진단 Agent",
    "one_liner": "로그를 분석하여 장애 원인을 자동 진단하고 해결 방안을 제시하는 Agent",
    "problem": {
        "pain_point": "장애 발생 시 로그 분석 -> 원인 파악에 평균 30분 소요",
        "current_solution": "수동으로 여러 시스템의 로그를 확인하며 원인 파악",
        "target_user": "주니어~미드레벨 백엔드 개발자 (온콜 담당)",
        "input": "장애 상황 설명 (자연어)",
        "output": "장애 원인 분류 + 근거 로그 + 해결 방안",
    },
    "architecture": {
        "type": "MCP",
        "reason": "외부 시스템(로그 저장소) 조회가 핵심. 문서 검색 불필요",
        "alternative": "RAG는 장애 매뉴얼 검색에 유용하나, MVP에서는 System Prompt로 대체 가능",
    },
    "tools": [
        {"name": "search_logs", "input": "service_name, time_range, level", "output": "로그 목록"},
        {"name": "get_metrics", "input": "service_name, metric_type", "output": "메트릭 값"},
        {"name": "check_health", "input": "service_name", "output": "헬스체크 결과"},
    ],
    "must_have": [
        "로그 조회 Tool 3개 정의 및 구현 (mock)",
        "장애 유형 3종 분류 (OOM, 타임아웃, 인증 실패)",
        "원인 분석 + 해결 방안 텍스트 생성",
    ],
    "nice_to_have": [
        "실제 API 연동",
        "자동 복구 명령 제안",
        "진단 히스토리 저장",
    ],
}

# 설계 문서 검증
assert len(design_doc["must_have"]) <= 5, "Must Have는 5개 이하로 제한"
assert len(design_doc["tools"]) >= 2, "Tool은 최소 2개 필요"
print("설계 문서 검증 통과")
print(f"  프로젝트: {design_doc['project_name']}")
print(f"  아키텍처: {design_doc['architecture']['type']}")
print(f"  Must Have: {len(design_doc['must_have'])}개")
print(f"  Tools: {len(design_doc['tools'])}개")
```

```
실행 결과:
설계 문서 검증 통과
  프로젝트: DevOps 장애 진단 Agent
  아키텍처: MCP
  Must Have: 3개
  Tools: 3개
```

**프로젝트 디렉토리 구조 (권장)**

```
my-agent-project/
+-- main.py              # Agent 실행 진입점
+-- agent.py             # Agent 핵심 로직 (LangGraph 그래프)
+-- tools.py             # MCP Tool 정의 (MCP/Hybrid)
+-- retriever.py         # RAG 검색 로직 (RAG/Hybrid)
+-- prompts.py           # System/User Prompt 관리
+-- eval/
|   +-- golden_test.yaml # Golden Test Set
|   +-- evaluator.py     # 평가 실행기
|   +-- report.json      # 평가 결과
+-- data/                # 원본 데이터 (RAG용)
+-- docs/
|   +-- design.md        # 프로젝트 설계서
+-- .env                 # API 키 (git ignore)
+-- requirements.txt     # 의존성
```

다음은 Walking Skeleton의 출발점이 될 보일러플레이트 코드이다. 이 코드는 환경변수 설정, LLM 연동, 기본 Agent 함수라는 세 가지 핵심 요소만 포함하고 있다. 여기서 시작하여 설계서의 아키텍처에 따라 Tool이나 Retrieval 로직을 점진적으로 추가하면 된다.

```python
"""main.py - Agent 실행 진입점 보일러플레이트."""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


def run_agent(query: str) -> str:
    """Agent 실행 함수. 프로젝트에 맞게 수정한다."""
    messages = [
        {"role": "system", "content": "당신은 {역할}을 수행하는 AI Agent입니다."},
        {"role": "user", "content": query},
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    result = run_agent("테스트 질문")
    print(result)
```

### Q&A

**Q: 프로젝트 설계서를 이렇게 자세히 쓸 시간이 있나요?**
A: 설계서 작성에 30분을 투자하면 구현 시간을 1시간 이상 절약한다. 설계서 없이 바로 코딩을 시작하면 중간에 방향을 바꾸거나 불필요한 기능을 구현하는 경우가 많다. 특히 "Must Have"와 "Nice to Have" 구분은 시간 압박 시 스코프를 줄이는 의사결정을 빠르게 해준다.

**Q: 아키텍처 다이어그램은 어떤 도구로 그리나요?**
A: MVP에서는 텍스트 기반 다이어그램(ASCII Art)으로 충분하다. 위의 템플릿을 참고하여 박스와 화살표로 그리면 된다. 발표 시 Mermaid나 draw.io를 사용하면 보기 좋지만, 설계서 단계에서는 텍스트로 빠르게 작성하는 것이 효율적이다.

<details>
<summary>퀴즈: MVP 설계에서 "Nice to Have" 기능을 미리 정의하는 이유는?</summary>

**힌트**: 시간이 남을 때와 부족할 때 각각 어떤 의사결정을 하게 되는지 생각해보자.

**정답**: (1) 시간이 남을 때: 미리 정의된 "Nice to Have"에서 우선순위 높은 것을 바로 구현할 수 있다. 즉흥적으로 기능을 추가하면 일관성이 깨진다. (2) 시간이 부족할 때: "Nice to Have"를 과감히 제거하고 "Must Have"에 집중하는 근거가 된다. 발표에서 "시간 제약으로 X 기능은 Nice to Have로 분류하여 제외했다"고 설명하면 프로젝트 관리 능력으로 평가받는다.
</details>

---

## 활동 4: MVP 스코프 정의와 Golden Test Set 설계

### 설명

설계 문서의 핵심은 **"무엇을 만들 것인가"보다 "무엇을 만들지 않을 것인가"**를 정하는 것이다. MVP 스코프를 명확히 정의하고, 동작을 검증할 Golden Test Set을 설계한다.

**Golden Test Set의 설계 철학: 왜 5~10개의 테스트가 시스템 품질을 대표할 수 있는가**

Golden Test Set은 "최소한의 테스트 케이스로 시스템의 핵심 동작을 검증하는 것"을 목표로 한다. 수백 개의 테스트를 무작정 만드는 것이 아니라, 전략적으로 설계된 소수의 테스트가 시스템의 품질을 효과적으로 대표할 수 있다는 원리에 기반한다.

이 원리는 소프트웨어 테스팅의 "동치 분할(Equivalence Partitioning)"과 "경계값 분석(Boundary Value Analysis)" 기법에서 비롯된다. 동치 분할은 입력을 동일한 결과를 낳는 그룹으로 나누고, 각 그룹에서 대표 케이스 하나만 테스트하는 기법이다. 예를 들어 FAQ Agent가 다루는 질문 유형이 "제품 정보 문의", "반품/교환 절차", "배송 현황 확인" 세 가지라면, 각 유형에서 하나씩 테스트하면 세 개의 테스트로 전체 동작을 커버할 수 있다. 여기에 경계값 케이스(질문이 극히 짧은 경우, 두 유형에 걸치는 모호한 질문)와 실패 케이스(범위 밖 질문, 답이 없는 질문)를 추가하면 5~10개의 테스트로 시스템의 핵심 품질을 측정할 수 있다.

Golden Test Set 설계에서 가장 흔한 실수는 "Happy Path만 모아두는 것"이다. 정상적인 질문만 모으면 테스트 통과율이 높게 나오지만, 실제 사용 환경에서 마주치는 엣지 케이스에서 시스템이 무너진다. 반드시 전체의 20% 이상을 실패 케이스로 구성해야 한다. 실패 케이스란 Agent가 "모르겠다"고 답하거나, "이 질문은 제 범위 밖입니다"라고 안내하는 것이 올바른 동작인 경우를 뜻한다. Agent의 진정한 품질은 답을 잘 하는 것뿐 아니라 모를 때 모른다고 말하는 능력에서 드러난다.

또한 각 테스트 케이스에는 반드시 "기대 답변(expected_output)"을 미리 정의해야 한다. 이것이 없으면 테스트 실행 후 "이 답변이 좋은 건가, 나쁜 건가"를 매번 사람이 판단해야 하므로 자동화가 불가능하다. 기대 답변은 정확한 텍스트 매칭이 아니라 "이 내용이 포함되어야 한다" 수준으로 정의하면 충분하다.

**Must-have vs Nice-to-have 분류 기준**

| 기준 | Must Have | Nice to Have |
|------|----------|-------------|
| 사용자 가치 | 없으면 Agent가 무의미 | 있으면 좋지만 없어도 핵심 동작 |
| 구현 시간 | 1시간 이내 | 추가 1시간 이상 |
| 의존성 | 다른 기능의 전제 조건 | 독립적으로 추가 가능 |
| 데모 영향 | 데모에서 반드시 보여줘야 함 | 보여주면 플러스 |

다음 코드는 Golden Test Set을 구조화하고 최소 요건을 자동 검증하는 유틸리티이다. 이를 활용하면 테스트 케이스의 카테고리 분포와 난이도 분포를 빠르게 확인할 수 있다.

```python
import os
import json
from dataclasses import dataclass, asdict
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


@dataclass
class GoldenTestCase:
    """Golden Test Set 개별 케이스."""
    id: str
    category: str          # "happy_path" | "edge_case" | "failure_case"
    query: str             # 사용자 입력
    expected_behavior: str # 기대 동작 설명
    expected_output: str   # 기대 출력 (정답)
    difficulty: str        # "easy" | "medium" | "hard"
    eval_criteria: list[str]  # 적용할 평가 항목


@dataclass
class GoldenTestSet:
    """프로젝트 Golden Test Set."""
    project_name: str
    test_cases: list[GoldenTestCase]

    def summary(self) -> dict:
        categories = {}
        difficulties = {}
        for tc in self.test_cases:
            categories[tc.category] = categories.get(tc.category, 0) + 1
            difficulties[tc.difficulty] = difficulties.get(tc.difficulty, 0) + 1
        return {
            "total": len(self.test_cases),
            "categories": categories,
            "difficulties": difficulties,
        }

    def validate(self) -> list[str]:
        """최소 요건 검증."""
        issues = []
        if len(self.test_cases) < 3:
            issues.append(f"최소 3개 필요 (현재 {len(self.test_cases)}개)")
        categories = {tc.category for tc in self.test_cases}
        if "happy_path" not in categories:
            issues.append("happy_path 케이스 필수")
        if "failure_case" not in categories:
            issues.append("failure_case 케이스 필수")
        return issues


# Golden Test Set 예시: DevOps 장애 진단 Agent
devops_golden_tests = GoldenTestSet(
    project_name="DevOps 장애 진단 Agent",
    test_cases=[
        GoldenTestCase(
            id="gt-0001",
            category="happy_path",
            query="payment-service에서 OOM 에러가 발생하고 있습니다",
            expected_behavior="로그 조회 -> OOM 패턴 감지 -> 메모리 관련 해결 방안 제시",
            expected_output="OOM(Out of Memory) 장애 진단: 메모리 사용량 증가 추세 확인, JVM 힙 사이즈 조정 또는 메모리 누수 지점 확인 권장",
            difficulty="easy",
            eval_criteria=["tool_selection", "response_quality"],
        ),
        GoldenTestCase(
            id="gt-0002",
            category="happy_path",
            query="user-auth 서비스 응답이 5초 이상 걸립니다",
            expected_behavior="로그 조회 -> 타임아웃 패턴 감지 -> 병목 지점 분석",
            expected_output="타임아웃 장애 진단: DB 커넥션 풀 소진 또는 외부 API 응답 지연 확인 필요",
            difficulty="medium",
            eval_criteria=["tool_selection", "param_accuracy", "response_quality"],
        ),
        GoldenTestCase(
            id="gt-0003",
            category="happy_path",
            query="API Gateway에서 401 에러가 급증하고 있어요",
            expected_behavior="로그 조회 -> 인증 실패 패턴 감지 -> 토큰/인증서 확인 안내",
            expected_output="인증 실패 장애 진단: JWT 토큰 만료 또는 API 키 갱신 필요",
            difficulty="easy",
            eval_criteria=["tool_selection", "response_quality"],
        ),
        GoldenTestCase(
            id="gt-0004",
            category="edge_case",
            query="전체적으로 좀 느린 것 같은데 확인해주세요",
            expected_behavior="모호한 입력 -> 추가 정보 요청 또는 전체 서비스 헬스체크",
            expected_output="구체적인 서비스명이나 증상을 알려주시면 정확한 진단이 가능합니다. 또는: 전체 서비스 헬스체크를 실행하겠습니다.",
            difficulty="hard",
            eval_criteria=["response_quality", "error_handling"],
        ),
        GoldenTestCase(
            id="gt-0005",
            category="failure_case",
            query="내일 날씨 어때?",
            expected_behavior="Agent 범위 밖 질문 -> 범위 안내",
            expected_output="저는 DevOps 장애 진단 전문 Agent입니다. 서비스 장애와 관련된 질문을 해주세요.",
            difficulty="easy",
            eval_criteria=["error_handling"],
        ),
    ],
)

# 검증 실행
issues = devops_golden_tests.validate()
summary = devops_golden_tests.summary()

print(f"프로젝트: {devops_golden_tests.project_name}")
print(f"테스트 케이스: {summary['total']}개")
print(f"카테고리 분포: {summary['categories']}")
print(f"난이도 분포: {summary['difficulties']}")
print(f"검증 이슈: {issues if issues else '없음 (통과)'}")
```

```
실행 결과:
프로젝트: DevOps 장애 진단 Agent
테스트 케이스: 5개
카테고리 분포: {'happy_path': 3, 'edge_case': 1, 'failure_case': 1}
난이도 분포: {'easy': 3, 'medium': 1, 'hard': 1}
검증 이슈: 없음 (통과)
```

**Golden Test Set 최소 요건**

| 요건 | 최소 기준 | 권장 |
|------|----------|------|
| 전체 케이스 수 | 5개 | 10개 이상 |
| 카테고리 | happy_path + failure_case 필수 | 3종 모두 포함 |
| 난이도 분포 | easy/medium 포함 | easy 30%, medium 50%, hard 20% |
| 실패 케이스 | 1개 이상 | 전체의 20% |

**YAML 형식 Golden Test Set 예시**

```yaml
# eval/golden_test.yaml
project: DevOps 장애 진단 Agent
version: "1.0"
test_cases:
  - id: gt-0001
    category: happy_path
    query: "payment-service에서 OOM 에러가 발생하고 있습니다"
    expected_behavior: "로그 조회 -> OOM 패턴 감지 -> 메모리 관련 해결 방안 제시"
    expected_output: "OOM 장애 진단 + 메모리 관련 해결 방안"
    difficulty: easy
    eval_criteria:
      - tool_selection
      - response_quality
  - id: gt-0002
    category: failure_case
    query: "내일 날씨 어때?"
    expected_behavior: "범위 밖 질문 -> 범위 안내"
    expected_output: "DevOps 장애 진단 관련 질문을 해달라는 안내"
    difficulty: easy
    eval_criteria:
      - error_handling
```

### Q&A

**Q: 시간이 부족해서 Golden Test Set을 3개밖에 못 만들겠습니다. 괜찮나요?**
A: 최소 기준은 5개이지만, 시간이 정말 부족하면 3개로도 핵심 동작을 검증할 수 있다. 단, 3개를 만들 때도 전략적으로 구성해야 한다. (1) Happy Path 1개: 가장 전형적인 성공 케이스, (2) Edge Case 1개: 경계 조건이나 모호한 입력, (3) Failure Case 1개: Agent가 거부하거나 에스컬레이션해야 하는 케이스.

**Q: Golden Test Set의 "기대 답변"은 얼마나 구체적으로 써야 하나요?**
A: 정확한 문자열 매칭이 아닌 **의미적 일치**를 기준으로 작성한다. "OOM 관련 진단 내용이 포함되어 있는가"처럼 핵심 키워드와 의미를 기준으로 정의한다. LLM-as-a-Judge를 사용할 경우, 기대 답변이 구체적일수록 평가 정확도가 높아진다.

<details>
<summary>퀴즈: RAG Agent의 Golden Test Set에서 "실패 케이스"란 구체적으로 어떤 것인가요?</summary>

**힌트**: Agent가 "모르겠다"고 답해야 올바른 상황을 생각해보자.

**정답**: RAG Agent의 실패 케이스는 (1) 색인된 문서에 답이 없는 질문 -- "해당 정보를 찾을 수 없습니다"가 올바른 응답, (2) 모호하여 확인이 필요한 질문 -- 추가 정보를 요청하는 것이 올바른 응답, (3) Agent 범위 밖의 질문(예: 기술 문서 Agent에 날씨 질문) -- 범위 밖임을 안내하는 것이 올바른 응답. 실패 케이스의 `expected_output`에 거부/에스컬레이션 응답을 명시한다.
</details>

---

## 활동 5: 설계 리뷰

### 설명

설계서를 완성한 후, 동료 또는 자기 자신의 설계를 체계적으로 리뷰한다. 설계 리뷰는 구현 전에 문제를 발견하는 가장 효율적인 방법이다.

**설계 리뷰의 가치: 왜 구현 전 30분 리뷰가 구현 후 2시간 수정보다 나은가**

설계 리뷰는 "결함 발견 비용의 비대칭성"이라는 소프트웨어 공학의 핵심 원리에 기반한다. 배리 보엠(Barry Boehm)의 연구에 따르면, 설계 단계에서 발견된 결함을 수정하는 비용은 구현 단계의 1/5, 테스트 단계의 1/15에 불과하다. MVP 프로젝트에서 이 원리는 더욱 극적으로 적용된다. 2시간이라는 구현 시간 중 설계 결함을 발견하고 방향을 수정하면 남은 시간이 부족해지기 때문이다.

설계 리뷰에서 가장 중요한 관점은 "이 설계대로 구현했을 때, 30분 내에 Walking Skeleton이 동작하는가"이다. 이를 판단하려면 다음 세 가지를 확인해야 한다. 첫째, 입력에서 출력까지의 데이터 흐름이 끊김 없이 연결되는가? 둘째, 각 컴포넌트의 인터페이스(입출력 형식)가 명확하게 정의되어 있는가? 셋째, 외부 의존성(API 키, 데이터 파일, 라이브러리)이 모두 준비되어 있는가? 이 세 가지 중 하나라도 불명확하면 구현 단계에서 반드시 병목이 발생한다.

피어 리뷰를 할 때는 "비판"이 아닌 "질문"의 형태로 피드백하는 것이 효과적이다. "이 설계는 잘못됐다"보다 "이 부분에서 데이터가 어떤 형식으로 전달되나요?"가 건설적인 개선으로 이어진다. MVP 프로젝트에서 피어 리뷰의 목적은 완벽한 설계를 만드는 것이 아니라, 구현을 시작하기 전에 치명적인 빈틈을 메우는 것이다.

**설계 리뷰 체크리스트**

```python
from dataclasses import dataclass


@dataclass
class ReviewItem:
    """설계 리뷰 체크 항목."""
    category: str
    question: str
    pass_criteria: str
    weight: str  # "필수" | "권장"


review_checklist = [
    # 문제 정의
    ReviewItem(
        category="문제 정의",
        question="Pain Point가 구체적인 수치로 표현되어 있는가?",
        pass_criteria="'평균 N분 소요', '주 N회 발생' 등 정량적 표현 포함",
        weight="필수",
    ),
    ReviewItem(
        category="문제 정의",
        question="입력/출력이 명확하게 정의되어 있는가?",
        pass_criteria="입력 형태, 출력 형태, 예시가 모두 포함",
        weight="필수",
    ),
    ReviewItem(
        category="문제 정의",
        question="Agent가 적합한 문제인가? (멀티스텝/동적 판단/도구 활용)",
        pass_criteria="3가지 조건 중 2개 이상 충족 + 근거 설명",
        weight="필수",
    ),
    # 아키텍처
    ReviewItem(
        category="아키텍처",
        question="MCP/RAG/Hybrid 선택 근거가 논리적인가?",
        pass_criteria="대안 구조를 검토하고 배제 이유를 명시",
        weight="필수",
    ),
    ReviewItem(
        category="아키텍처",
        question="아키텍처 다이어그램이 포함되어 있는가?",
        pass_criteria="입력 -> 처리 -> 출력 흐름이 시각적으로 표현됨",
        weight="필수",
    ),
    # 스코프
    ReviewItem(
        category="스코프",
        question="Must Have 기능이 3~5개인가?",
        pass_criteria="각 기능이 30분~1시간 내 구현 가능한 단위",
        weight="필수",
    ),
    ReviewItem(
        category="스코프",
        question="Must Have와 Nice to Have가 구분되어 있는가?",
        pass_criteria="Nice to Have에 시간이 남을 때 추가할 기능 목록 있음",
        weight="필수",
    ),
    # 평가
    ReviewItem(
        category="평가",
        question="Golden Test Set이 최소 5개 이상인가?",
        pass_criteria="happy_path, edge_case, failure_case 포함",
        weight="필수",
    ),
    ReviewItem(
        category="평가",
        question="성공 기준이 측정 가능한 수치로 정의되어 있는가?",
        pass_criteria="'정확도 80% 이상' 등 정량적 목표 포함",
        weight="권장",
    ),
    # 리스크
    ReviewItem(
        category="리스크",
        question="주요 리스크와 대응 방안이 식별되어 있는가?",
        pass_criteria="최소 2개 리스크 + 각각의 대응 방안 명시",
        weight="권장",
    ),
]

# 리뷰 실행
print("=== 설계 리뷰 체크리스트 ===\n")
for item in review_checklist:
    marker = "[필수]" if item.weight == "필수" else "[권장]"
    print(f"{marker} [{item.category}]")
    print(f"  질문: {item.question}")
    print(f"  통과 기준: {item.pass_criteria}")
    print()
```

```
실행 결과:
=== 설계 리뷰 체크리스트 ===

[필수] [문제 정의]
  질문: Pain Point가 구체적인 수치로 표현되어 있는가?
  통과 기준: '평균 N분 소요', '주 N회 발생' 등 정량적 표현 포함

[필수] [문제 정의]
  질문: 입력/출력이 명확하게 정의되어 있는가?
  통과 기준: 입력 형태, 출력 형태, 예시가 모두 포함

[필수] [문제 정의]
  질문: Agent가 적합한 문제인가? (멀티스텝/동적 판단/도구 활용)
  통과 기준: 3가지 조건 중 2개 이상 충족 + 근거 설명

[필수] [아키텍처]
  질문: MCP/RAG/Hybrid 선택 근거가 논리적인가?
  통과 기준: 대안 구조를 검토하고 배제 이유를 명시

[필수] [아키텍처]
  질문: 아키텍처 다이어그램이 포함되어 있는가?
  통과 기준: 입력 -> 처리 -> 출력 흐름이 시각적으로 표현됨

[필수] [스코프]
  질문: Must Have 기능이 3~5개인가?
  통과 기준: 각 기능이 30분~1시간 내 구현 가능한 단위

[필수] [스코프]
  질문: Must Have와 Nice to Have가 구분되어 있는가?
  통과 기준: Nice to Have에 시간이 남을 때 추가할 기능 목록 있음

[필수] [평가]
  질문: Golden Test Set이 최소 5개 이상인가?
  통과 기준: happy_path, edge_case, failure_case 포함

[권장] [평가]
  질문: 성공 기준이 측정 가능한 수치로 정의되어 있는가?
  통과 기준: '정확도 80% 이상' 등 정량적 목표 포함

[권장] [리스크]
  질문: 주요 리스크와 대응 방안이 식별되어 있는가?
  통과 기준: 최소 2개 리스크 + 각각의 대응 방안 명시
```

**피어 리뷰 프로세스**

설계서를 완성한 후 옆자리 동료와 교환하여 리뷰한다. 리뷰어는 위 체크리스트의 "필수" 항목만 확인하면 된다.

| 단계 | 시간 | 내용 |
|------|------|------|
| 1. 설계서 교환 | 0분 | 옆자리 동료에게 설계서 전달 |
| 2. 무언 리뷰 | 5분 | 체크리스트 기반으로 개별 검토 |
| 3. 피드백 공유 | 5분 | "필수" 항목 중 미충족 항목 피드백 |
| 4. 반영 | 5분 | 피드백 반영하여 설계서 수정 |

### Q&A

**Q: 피어 리뷰에서 근본적인 설계 변경이 필요하다는 피드백을 받으면 어떡하나요?**
A: 시간을 고려하여 판단해야 한다. (1) 아키텍처 변경이 필요한 경우: 변경 범위가 작으면 즉시 수정, 크면 현재 설계를 유지하되 리스크 섹션에 기록, (2) 스코프 변경이 필요한 경우: Must Have에서 1~2개를 Nice to Have로 이동하는 것은 쉽게 가능, (3) 문제 정의 변경이 필요한 경우: 가장 리스크가 크다. 문제 정의가 흔들리면 전체가 흔들리므로, 확신이 없으면 추천 주제 중 하나로 전환하는 것도 방법이다.

<details>
<summary>퀴즈: 설계 리뷰에서 가장 치명적인 "필수" 미충족 항목은?</summary>

**힌트**: 구현 단계에서 가장 큰 혼란을 야기하는 항목을 생각해보자.

**정답**: "입력/출력이 명확하게 정의되어 있는가"가 가장 치명적이다. 입력/출력이 모호하면 (1) 무엇을 구현해야 하는지 알 수 없고, (2) Golden Test Set을 작성할 수 없으며, (3) 데모 시나리오를 설계할 수 없다. Pain Point가 모호한 것도 문제지만, 입력/출력이 명확하면 구현은 가능하다. 반대로 Pain Point가 명확해도 입력/출력이 모호하면 구현이 불가능하다.
</details>

---

## 실습

### 실습: 프로젝트 설계서 완성
- **연관 학습 목표**: 학습 목표 1, 2, 3
- **실습 목적**: Day 1~4에서 학습한 모든 내용을 종합하여 실제 구현할 MVP 프로젝트의 설계서를 완성한다
- **실습 유형**: 프로젝트 설계
- **난이도**: 심화
- **예상 소요 시간**: 90분
- **선행 조건**: Day 1~4 전체
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

#### 실습 단계

**1단계: 주제 선정 및 문제 정의 (20분)**

- 추천 주제 5개 또는 자체 주제 중 하나를 선정한다
- 문제 정의서 템플릿을 작성한다
- Pain Point를 수치로 표현한다
- 입력/출력을 명확하게 정의한다

**2단계: 아키텍처 선택 및 다이어그램 (20분)**

- MCP/RAG/Hybrid 중 선택하고 근거를 작성한다
- 대안 구조를 검토하고 배제 이유를 기술한다
- 텍스트 기반 아키텍처 다이어그램을 작성한다
- 핵심 컴포넌트 목록과 역할을 정의한다

**3단계: Golden Test Set 설계 (20분)**

- 최소 5개 테스트 케이스를 작성한다
- happy_path, edge_case, failure_case를 포함한다
- `eval/golden_test.yaml` 파일로 저장한다
- 검증 스크립트를 실행하여 최소 요건을 확인한다

**4단계: 설계서 완성 및 리뷰 (30분)**

- 전체 템플릿을 채워서 설계서를 완성한다
- Must Have / Nice to Have 기능을 분리한다
- 프로젝트 디렉토리를 생성한다
- 피어 리뷰 체크리스트로 상호 검토한다

#### 기대 산출물

```
my-agent-project/
+-- docs/
|   +-- design.md          # 프로젝트 설계서 (완성)
+-- eval/
|   +-- golden_test.yaml   # Golden Test Set (5개 이상)
+-- main.py                # 보일러플레이트 (동작 확인)
+-- .env                   # API 키 설정
+-- requirements.txt       # 의존성 목록
```

#### 검증 체크리스트

- [ ] 문제 정의서 완성 (Pain Point 수치 포함, 입력/출력 명확)
- [ ] 아키텍처 선택 및 근거 문서화 (대안 검토 포함)
- [ ] 아키텍처 다이어그램 작성
- [ ] Golden Test Set 5개 이상 작성 (3종 카테고리 포함)
- [ ] Must Have / Nice to Have 기능 분리
- [ ] 프로젝트 디렉토리 생성 및 보일러플레이트 실행 확인
- [ ] 피어 리뷰 완료 (필수 항목 전체 통과)

---

## 핵심 정리
- **문제를 좁혀라**: MVP는 "가장 작은 동작하는 단위"이다. 범위가 넓을수록 실패 확률이 높아진다
- **구조를 선택하고 근거를 남겨라**: MCP/RAG/Hybrid 중 "왜 이것인가"를 한 문장으로 설명할 수 있어야 한다
- **평가 없는 Agent는 데모 수준**: Golden Test Set 최소 5개와 측정 가능한 성공 기준이 있어야 MVP라 부를 수 있다
- **설계서가 시간을 절약한다**: 30분 설계 투자가 구현 시 1시간 이상의 삽질을 방지한다
- **Must Have / Nice to Have 구분**: 시간 압박 시 스코프를 조절하는 유일한 근거이다
