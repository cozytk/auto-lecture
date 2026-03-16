# 예시 산출물: Refactor Boundary Workshop

## 현재 그래프 이름
- 매출 분석 Agent

| Node | 읽는 필드 | 쓰는 필드 | 테스트 난이도 | 분리 우선순위 |
|------|----------|----------|--------------|--------------|
| collect | `query`, `source_limit` | `raw_records`, `collection_status` | 중간 | 높음 |
| validate | `raw_records`, `retry_count` | `collection_status`, `validation_notes` | 중간 | 높음 |
| analyze | `raw_records`, `analysis_mode` | `insights`, `score` | 높음 | 높음 |
| report | `insights`, `score` | `report`, `messages` | 낮음 | 중간 |

## Subgraph 경계 초안

### 서브그래프 1
- 역할: 수집 + 검증 파이프라인
- 포함 Node: `collect`, `validate`
- 부모와 공유할 State 키: `query`, `raw_records`, `validation_notes`
- 내부에 숨길 State 키: `retry_count`, `collection_status`

### 서브그래프 2
- 역할: 분석 + 보고서 생성
- 포함 Node: `analyze`, `report`
- 부모와 공유할 State 키: `raw_records`, `insights`, `report`
- 내부에 숨길 State 키: `analysis_mode`, `score`

## 인터페이스 계약

| 호출 주체 | 입력 키 | 출력 키 | 계약 메모 |
|----------|--------|--------|----------|
| Parent -> CollectionSubgraph | `query` | `raw_records`, `validation_notes` | 수집 실패 시 validation_notes에 사유를 남긴다 |
| Parent -> AnalysisSubgraph | `raw_records` | `insights`, `report` | 빈 raw_records가 오면 보고서 대신 경고 메시지를 반환한다 |

## 체크포인트 전략

- checkpointer가 필요한 지점: 수집 완료 직후, 분석 완료 직후
- thread_id 단위로 분리해야 하는 이유: 사용자별 분석 요청이 동시에 여러 건 실행될 수 있기 때문
- 오래된 messages/state를 pruning할 기준: 보고서 생성 후 원시 로그는 요약본만 남기고 상세 로그는 audit 저장소로 이동
