### 프롬프트 및 검색 튜닝 실습

프롬프트 버전 관리, Retrieval Drift 감지, Tool 호출 정확도 개선을 다루는 세 가지 실습으로 구성된다.

---

### 02a. Prompt 버전 관리와 A/B 테스트

프롬프트를 SemVer로 버전 관리하고 A/B 테스트로 검증하는 방법을 학습한다.

- 딕셔너리 기반 Prompt Registry 패턴 구현
- LM Judge로 프롬프트 버전 간 성능을 정량 비교
- 해시 기반 A/B 테스트로 트래픽 분배
- Langfuse에서 버전별 트레이스 필터링 및 비교

---

### 02b. Retrieval Drift 감지와 대응

문서 업데이트 시 RAG 검색 결과가 달라지는 Retrieval Drift를 감지하고 대응하는 방법을 학습한다.

- InMemoryVectorStore로 RAG 파이프라인 구축
- 문서 업데이트 전후 검색 결과 비교
- Retrieval Stability Score, RBO(Rank-Biased Overlap) 계산
- LLM Judge로 검색 품질 정성 평가
- 검색 변화가 RAG 응답에 미치는 영향 분석

---

### 02c. Tool 호출 정확도 개선

Tool 설명(description)의 품질이 Agent의 Tool 선택 정확도에 미치는 영향을 확인하고 개선하는 방법을 학습한다.

- 나쁜 Tool 설명 vs 좋은 Tool 설명의 정확도 비교
- Tool 호출 실패 4가지 유형 식별 (Wrong Tool, Wrong Params, Missing Validation, Schema Mismatch)
- 파라미터 Validation 레이어 추가
- Langfuse로 Tool 호출 패턴 분석

### 사전 준비

- OpenAI API Key
- Langfuse 환경 (트레이스 기록용)
