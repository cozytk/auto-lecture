### Agent 품질 평가 실습

Accuracy, Faithfulness, Robustness 세 가지 축으로 AI Agent의 품질을 체계적으로 평가하는 방법을 학습한다.

### 학습 목표

- Golden Test Set을 직접 작성하고 구조를 이해한다
- 정량 평가 지표(Keyword Match, Token F1)를 구현하고 적용한다
- LM-as-a-Judge로 서술형 응답을 자동 평가한다
- Faithfulness(근거 기반 응답 여부)를 측정한다
- Robustness(입력 변형에 대한 일관성)를 테스트한다
- Pairwise 비교로 위치 편향을 제거한다
- 복합 지표 대시보드로 배포 기준을 설정한다

### 실습 구성

| 단계 | 내용 |
|------|------|
| 환경 설정 | SQL Agent + Judge LLM 준비 |
| Golden Test Set | Chinook DB에서 정답 확인 후 테스트 케이스 작성 |
| 정량 평가 | Keyword Match, Token F1로 자동 채점 |
| LM-as-a-Judge | LLM이 서술형 응답을 0.0~1.0으로 채점 |
| Faithfulness | 응답이 DB 쿼리 결과에만 근거하는지 확인 |
| Robustness | 같은 질문의 변형에 일관된 답을 내는지 확인 |
| Pairwise 비교 | 위치 편향 제거 + 프롬프트 A/B 테스트 |
| 복합 대시보드 | 배포 가능 여부를 종합 판단 |

### 사전 준비

- Chinook DB (`Chinook.db`)
- OpenAI API Key
- Langfuse 환경 (트레이스 기록용)
