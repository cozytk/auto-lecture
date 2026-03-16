# Lab 2 — 운영 아키텍처 설계

> **목표**: 실제 서비스 수준의 Agent 운영 아키텍처를 설계한다.
> 환경 분리, Scaling 전략, 비용 추정, 카나리 배포 계획을 포함한 전체 설계서를 작성한다.

**소요 시간**: 약 2시간
**형태**: README 중심 설계 실습 (코드 없음)
**산출물**: `artifacts/ops-architecture-design.md` + `artifacts/config-prod-example.yaml`

---

## 디렉토리 구조

```
day4-ops-architecture-design/
├── README.md          # 이 파일 (실습 가이드)
└── artifacts/
    ├── worksheet.md           # WE DO 워크시트 (빈칸 채우기)
    ├── ops-architecture-design.md   # YOU DO 산출물 (직접 작성)
    ├── config-prod-example.yaml     # YOU DO 산출물 (직접 작성)
    └── reference-answer.md          # 모범 답안 예시
```

---

## 시나리오

> **B2B 고객 지원 Agent 서비스**를 설계한다.

- **트래픽**: 일평균 50,000 요청
- **SLA**: P95 응답 시간 5초 이내, 오류율 1% 미만
- **비용 목표**: 월 LLM 비용 $5,000 이하
- **고객**: 기업 고객 20곳, 각 500~5,000명 직원
- **현재 상태**: 단일 서버, Dev/Prod 미분리, 모든 요청에 gpt-4o 사용 중

---

## I DO — 강사 시연

> 강사가 `artifacts/reference-answer.md`의 일부를 화면에 보여주며 설계 사고 과정을 설명한다.

### 시연 1: 환경 분리 설계 사고 과정 (15분)

**강사가 보여주는 것**:
- 현재 상태(단일 서버) → 목표 상태(3환경 분리)의 차이
- Dev에서 gpt-4o-mini를 쓰는 이유 (비용 절감)
- Staging 데이터 익명화 방법

**핵심 질문**: "Staging과 Prod의 설정이 다르면 Staging 테스트 결과를 신뢰할 수 있는가?"
→ 모델은 동일하게, 데이터만 익명화한다.

### 시연 2: 비용 추정 계산 (10분)

**강사가 보여주는 계산**:

```
일평균 50,000 요청
× 평균 입력 토큰 1,500 (시스템 프롬프트 + 컨텍스트 + 질문)
× 출력 토큰 300
× 30일

gpt-4o 단가 (2026년 기준 예시):
  입력: $0.005 / 1K tokens
  출력: $0.015 / 1K tokens

계산:
  입력 비용: 50,000 × 1,500 / 1,000 × $0.005 × 30 = $11,250/월
  출력 비용: 50,000 × 300 / 1,000 × $0.015 × 30 = $6,750/월
  합계: $18,000/월 → 목표 $5,000 초과!

모델 계층화 적용 후:
  단순 분류 (70%): gpt-4o-mini → $0.00015/1K
  일반 응답 (25%): gpt-4o → $0.005/1K
  복잡 추론 (5%):  o3 → $0.06/1K
  → 약 $4,200/월 (목표 달성)
```

### 시연 3: 카나리 배포 판단 기준 (5분)

**강사가 설명하는 것**:
- 5% 트래픽에서 오류율·응답 시간이 기준을 넘으면 롤백한다.
- 기준을 어떻게 정하는가? → 현재 Prod 기준의 120% (20% 여유)

---

## WE DO — 함께 실습

> 팀별로 `artifacts/worksheet.md`를 채우며 강사가 단계별로 안내한다.

### Step 1: 환경 분리 설계 (20분)

`artifacts/worksheet.md`의 **섹션 1**을 팀이 함께 채운다.

**채워야 할 항목**:
- Dev / Staging / Prod 각 환경의 LLM 모델명
- 각 환경의 데이터 정책 (실제 데이터 / 익명화 / 합성)
- 환경 전환 방법 (환경 변수 키 이름)
- 로깅 정책 (전수 / 샘플링 비율)

**팀 토론 질문**:
- Dev 환경에서 gpt-4o를 써야 하는 경우가 있는가?
- Staging 데이터 익명화 파이프라인은 누가 관리하는가?

### Step 2: Scaling 전략 결정 (15분)

`artifacts/worksheet.md`의 **섹션 2**를 채운다.

**채워야 할 항목**:
- 현재 병목 지점 (LLM API 대기 / 서버 CPU / DB?)
- 선택한 Scaling 방식 (수평 / 수직 / 서버리스)
- Auto-scaling 트리거 기준 (CPU % / 요청 큐 길이)
- Stateless 설계를 위해 외부화할 상태 목록

### Step 3: 비용 추정 (20분)

`artifacts/worksheet.md`의 **섹션 3**을 함께 계산한다.

**주어진 수치**:
- 일평균 50,000 요청
- 평균 입력 토큰: 1,500
- 평균 출력 토큰: 300

**계산 후 토론**:
- 어느 Task 유형이 가장 많은가?
- 모델 계층화로 얼마나 절감할 수 있는가?
- Semantic Cache 도입 시 추가 절감 효과는?

### Step 4: 팀별 발표 (15분)

각 팀이 설계 결과를 5분씩 발표한다.
- 환경 분리 방식
- 모델 계층화 계획
- 예상 월 비용

---

## YOU DO — 독립 과제

> 혼자 전체 운영 아키텍처 설계서를 작성한다.

### 산출물 1: `artifacts/ops-architecture-design.md`

아래 목차에 따라 직접 작성한다.

```markdown
# 운영 아키텍처 설계서
## 1. 환경 분리 설계
## 2. Scaling 전략
## 3. 모델 계층화 계획
## 4. 월간 비용 추정
## 5. 카나리 배포 계획
## 6. 비상 대응 계획 (롤백 기준)
```

**각 섹션 요구사항**:

**섹션 1 — 환경 분리**:
- Dev / Staging / Prod 환경별 표 (모델, 데이터, 로깅, 접근 권한)
- 환경 변수 목록 (최소 5개)
- 데이터 익명화 방침

**섹션 2 — Scaling**:
- 수평 Scaling 선택 근거
- Auto-scaling 트리거 기준 (숫자 포함)
- Stateless 설계 방안 (무엇을 Redis에 저장할지)

**섹션 3 — 모델 계층화**:
- Task 유형 3가지 이상 정의
- 각 Task에 사용할 모델 및 선택 근거
- 분류 로직 (어떻게 Task 유형을 판단할지)

**섹션 4 — 월간 비용 추정**:
- 계층화 전 예상 비용 계산
- 계층화 후 예상 비용 계산
- Semantic Cache 도입 시 추가 절감 추정
- 절감률 계산

**섹션 5 — 카나리 배포**:
- 단계별 트래픽 비율 (예: 5% → 20% → 100%)
- 각 단계별 관찰 시간
- 롤백 트리거 기준 (오류율, 응답 시간)
- 승격 기준

**섹션 6 — 비상 대응**:
- P0 장애 시 즉시 롤백 절차 (단계별)
- 롤백 소요 예상 시간
- 에스컬레이션 체계

### 산출물 2: `artifacts/config-prod-example.yaml`

아래 구조를 참고해 Prod 환경 설정 파일을 작성한다.

```yaml
# 참고 구조 (직접 값을 채워 완성하세요)
llm:
  # 기본 모델 (RAG 응답 생성용)
  model: ???
  temperature: ???
  max_tokens: ???
  # 단순 분류용 모델
  classifier_model: ???

vector_store:
  endpoint: ???
  index: ???
  top_k: ???

guardrail:
  enabled: ???
  pii_masking: ???
  input_check: ???
  output_check: ???

logging:
  level: ???
  sample_rate: ???   # 정상 트래픽 샘플링 비율

cache:
  enabled: ???
  similarity_threshold: ???
  ttl_seconds: ???

scaling:
  min_instances: ???
  max_instances: ???
  cpu_target_percent: ???
```

### 완료 기준

- [ ] `ops-architecture-design.md` 6개 섹션 모두 작성
- [ ] 월간 비용 추정에 실제 계산 과정 포함
- [ ] 카나리 배포 단계별 기준 수치 포함
- [ ] `config-prod-example.yaml` 모든 값 채움

**막히면**: `artifacts/reference-answer.md`를 참조한다.

---

## 채점 기준

| 항목 | 배점 | 기준 |
|---|---|---|
| 환경 분리 설계 | 20점 | 3환경 완전 분리, 데이터 정책 명확 |
| Scaling 전략 | 20점 | 수평 Scaling, Stateless 설계 포함 |
| 모델 계층화 | 20점 | 3개 이상 Task 유형, 비용 근거 |
| 비용 추정 | 20점 | 계산 과정 포함, 목표 달성 여부 |
| 카나리 배포 | 10점 | 단계별 기준 수치 포함 |
| 비상 대응 | 10점 | 롤백 절차 단계별 명시 |

---

## 참고 자료

- `guide/day4-session4.md` — 확장 가능한 서비스 아키텍처 이론
- `guide/day4-session3.md` — 로그·모니터링·장애 대응
- `artifacts/reference-answer.md` — 모범 답안 예시
