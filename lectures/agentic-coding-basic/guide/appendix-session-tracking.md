# 부록: OpenCode 세션 추적 가이드

> 에이전트의 내부 동작을 분석하기 위한 세션 데이터 추출 및 활용 방법

---

## 1. 세션 데이터 저장 구조

OpenCode는 모든 세션 데이터를 로컬에 저장한다.

| 항목 | 위치 |
|------|------|
| 메인 데이터베이스 | `~/.local/share/opencode/opencode.db` (SQLite) |
| 로그 파일 | `~/.local/share/opencode/log/` |
| 세션별 diff | `~/.local/share/opencode/storage/session_diff/` |
| 메시지 파일 | `~/.local/share/opencode/storage/message/` |
| 메시지 파트 | `~/.local/share/opencode/storage/part/` |
| Git 스냅샷 | `~/.local/share/opencode/snapshot/` |

---

## 2. CLI 명령으로 세션 관리

### 세션 목록 조회

```bash
opencode session list
```

최근 세션 목록을 테이블 형태로 출력한다.
세션 ID, 제목, 작업 디렉토리, 생성 시간이 표시된다.

### 세션 내보내기

```bash
opencode export <session-id>
```

지정한 세션을 JSON 형식으로 내보낸다.
내보낸 데이터에는 다음이 포함된다:
- 사용자 메시지 (입력)
- 어시스턴트 메시지 (응답)
- 도구 호출과 결과 (tool calls + tool results)
- 서브에이전트 세션 (부모-자식 관계)

### 세션 이어서 사용

```bash
opencode --continue              # 마지막 세션 이어서
opencode --session <session-id>   # 특정 세션 이어서
opencode --fork                   # 마지막 세션을 복제하여 새 세션 시작
```

### 사용량 통계

```bash
opencode stats                    # 전체 사용량
opencode stats --days 7           # 최근 7일
opencode stats --models           # 모델별 사용량
opencode stats --project          # 프로젝트별 사용량
```

---

## 3. 디버그 모드

에이전트의 내부 동작을 실시간으로 확인하려면 디버그 모드를 활성화한다.

```bash
opencode --log-level DEBUG     # 또는 opencode -d
opencode --print-logs          # stderr로 로그 스트리밍
```

로그에는 다음이 포함된다:
- 서비스 초기화 과정
- MCP 서버 연결 상태
- 도구 호출 전후 이벤트
- 모델 API 요청/응답

---

## 4. SQLite 직접 조회 (고급)

세션 데이터를 더 상세히 분석하려면 SQLite 데이터베이스를 직접 조회할 수 있다.

```bash
sqlite3 ~/.local/share/opencode/opencode.db
```

### 주요 테이블

| 테이블 | 내용 |
|--------|------|
| `session` | 세션 메타데이터 (ID, 제목, 디렉토리, 생성/수정 시간) |
| `message` | 세션별 메시지 (role: user/assistant, 세션 ID) |
| `part` | 메시지의 구성 요소 (텍스트, 도구 호출, 도구 결과, 추론) |

### 유용한 쿼리

```sql
-- 최근 5개 세션 조회
SELECT id, title, directory, created_at
FROM session ORDER BY created_at DESC LIMIT 5;

-- 특정 세션의 메시지 흐름
SELECT m.role, substr(p.content, 1, 200) as preview
FROM message m JOIN part p ON p.message_id = m.id
WHERE m.session_id = '<session-id>'
ORDER BY m.created_at, p.id;

-- 특정 세션의 도구 호출만 추출
SELECT p.type, substr(p.content, 1, 300) as content
FROM message m JOIN part p ON p.message_id = m.id
WHERE m.session_id = '<session-id>' AND p.type LIKE '%tool%'
ORDER BY p.id;
```

### 서브에이전트 세션 추적

서브에이전트는 별도 세션으로 생성된다. 부모 세션과의 관계를 확인하려면:

```sql
-- 부모 세션의 자식 세션 찾기 (parentID 컬럼 활용)
SELECT id, title, created_at
FROM session
WHERE parent_id = '<parent-session-id>';
```

---

## 5. 실습에서의 활용

### Lab 00 (코드베이스 탐험)
- `@explore` 실행 후 세션을 내보내어 서브에이전트의 도구 사용 순서 분석
- Glob → Read → Grep 패턴이 에이전틱 루프의 Observe → Think → Act에 매핑됨을 확인

### Lab 01 (컨텍스트 엔지니어링)
- Round 1/2/3 각각의 세션을 내보내어 정량적 비교
- 컨텍스트(AGENTS.md) 유무에 따른 도구 호출 횟수, 소요 시간, 토큰 사용량 차이 분석

### Lab 02 (레거시 리팩토링)
- 에이전트가 레거시 코드를 분석할 때 어떤 파일을 먼저 읽는지 추적
- AGENTS.md 규칙이 에이전트의 탐색 순서에 미치는 영향 확인

### Lab 03 (피드백 루프)
- 비대화형 실행(`opencode run`)의 세션 데이터로 피드백 루프 반복 횟수 확인
- 자동 수정 스크립트의 각 반복에서 에이전트가 어떤 도구를 사용했는지 분석

---

## 참고 자료

- [OpenCode 공식 문서 — CLI](https://opencode.ai/docs/cli/)
- [OpenCode 공식 문서 — Agents](https://opencode.ai/docs/agents/)
- [How Coding Agents Actually Work: Inside OpenCode](https://cefboud.com/posts/coding-agents-internals-opencode-deepdive/)
