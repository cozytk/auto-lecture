# Day 4 실습: 운영 아키텍처 설계

> 소요 시간: 약 85분
> 형태: README 중심 설계 실습

## 개요

지금까지 만든 Agent를 프로덕션 환경에서 운영하기 위한 서비스 아키텍처를 설계한다. 아키텍처 다이어그램, 환경 분리 전략, Scaling 계획, 비용 산정을 포함한 종합 설계 문서를 작성한다.

## 디렉토리 구조

```
day4-service-architecture/
├── README.md                                  # 이 파일
└── artifacts/
    ├── architecture-template.md               # 아키텍처 설계 템플릿
    ├── example-architecture.md                # 모범 답안
    └── cost-estimation-template.md            # 비용 산정 워크시트
```

---

## I DO (시연) - 15분

강사가 프로덕션 Agent 아키텍처를 설계하는 과정을 시연한다.

### 시연 내용

1. **아키텍처 다이어그램 작성** (Mermaid)
   - 클라이언트, API Gateway, 애플리케이션, Agent, 외부 서비스 레이어
   - 각 컴포넌트의 역할과 통신 흐름

2. **환경별 설정 구성**
   - Dev / Staging / Prod 환경 차이
   - Feature Flag 활용 방법

3. **비용 산정**
   - LLM API 비용 계산 공식
   - 일간/월간 비용 추정

---

## WE DO (함께) - 30분

전체가 함께 Day 2-3에서 만든 Agent의 프로덕션 아키텍처를 설계한다.

### 진행 순서

1. `artifacts/architecture-template.md`를 열어 함께 채운다
2. 아키텍처 다이어그램을 Mermaid로 그린다
3. 환경 분리 전략을 결정한다
4. Scaling 전략을 토론한다
   - 동기 vs 비동기 처리
   - 캐싱 전략
   - 수평 확장 필요 시점

---

## YOU DO (독립) - 40분

개인 Agent 프로젝트의 프로덕션 아키텍처를 완성한다.

### 과제 내용

1. `artifacts/architecture-template.md`를 복사하여 자신의 아키텍처를 설계한다
2. 필수 작성 항목:
   - 전체 아키텍처 다이어그램 (Mermaid)
   - 환경 분리 전략 (Dev/Staging/Prod)
   - Scaling 전략
   - Multi-Agent 적용 여부 판단
   - 비용 산정 (`cost-estimation-template.md` 활용)
3. 모범 답안은 `artifacts/example-architecture.md` 참고

### 완료 기준

- [ ] 전체 아키텍처 Mermaid 다이어그램 작성
- [ ] 환경별 설정 차이 정의
- [ ] Scaling 전략 1가지 이상 구체적 설계
- [ ] 비용 산정 워크시트 완성
- [ ] Multi-Agent 필요 여부 판단 및 근거

### 산출물

- 완성된 아키텍처 설계 문서
- 비용 산정 워크시트
