# 실습 03: MCP Tool 기반 Agent 구현 (Function Calling)

## 실습 목적

Function Calling 기반 Agent의 전체 흐름을 직접 구현하고,
LLM이 "어떤 Tool을 선택할지 결정"하고 애플리케이션이 "실제로 실행"하는 역할 분리를 체험한다.

- **연관 세션**: Session 4 - MCP·RAG·Hybrid 구조 판단
- **난이도**: 중급
- **예상 소요 시간**: 30분 (I DO 8분 / WE DO 10분 / YOU DO 12분)

## 사전 준비

```bash
export OPENROUTER_API_KEY="your-api-key"
export MODEL="moonshotai/kimi-k2"
just setup
```

---

## I DO: 시연 관찰 (약 8분)

강사가 시연하는 코드를 관찰하세요. 직접 코드를 작성하지 않아도 됩니다.

### 시연 내용

- `search_orders`, `get_order_detail` Tool 2개 정의
- Agent 루프: LLM 호출 → tool_calls 확인 → Tool 실행 → 결과 추가 → 반복
- Tool 호출이 필요 없는 질문에는 직접 답변하는 것 확인

### 시연 코드 실행

```bash
just run-i-do
```

### 관찰 포인트

- `description`이 Tool 선택의 핵심이다. "언제/왜 사용하는지"를 명확히 적어야 한다
- LLM은 `tool_calls` 필드로 응답하고, 애플리케이션이 실제 실행한다
- Tool 결과는 `role: "tool"`로 대화 이력에 추가된다
- Tool 호출이 필요 없으면 `tool_calls`가 없고 바로 `content`를 반환한다

---

## WE DO: 함께 실습 (약 10분)

강사와 함께 `src/we-do/agent.py`에 `cancel_order` Tool을 추가하고 Agent 루프를 완성합니다.

### 1단계: cancel_order Tool 정의

```python
{
    "type": "function",
    "function": {
        "name": "cancel_order",
        "description": (
            "주문을 취소합니다. "
            "배송 완료(delivered) 주문은 취소 불가합니다. "
            "취소 가능 여부 확인 후 사용하세요."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "취소할 주문 ID"},
                "reason": {"type": "string", "description": "취소 사유 (선택)"},
            },
            "required": ["order_id"],
        },
    },
}
```

### 2단계: execute_tool에 cancel_order 처리 추가

```bash
just run-we-do
```

### 3단계: Agent 루프 구현 (while 루프)

---

## YOU DO: 독립 과제 (약 12분)

`src/you-do/agent.py`를 완성하세요.

### 과제 설명

주간 보고서 자동화 Agent를 구현하세요:

1. Tool 3개 완성 (`get_jira_tickets`, `get_git_commits`, `save_report`)
   - 각 description은 30자 이상으로 "언제/왜 사용하는지" 명시
   - required 파라미터를 올바르게 지정
2. `execute_tool` 함수에 각 Tool의 더미 응답 구현
3. `run_agent` 함수에 Agent 루프 구현

### 시작 방법

```bash
just run
```

### 검증 기준

- Tool description이 30자 이상인가
- "Tool 호출이 필요 없는 질문"에 직접 답변하는가
- "여러 Tool 순차 호출" 질문에서 Jira → Git → save 순서로 호출되는가

### 힌트

<details>
<summary>힌트 1: Tool 정의 필수 필드</summary>

```python
{
    "type": "function",
    "function": {
        "name": "함수명",
        "description": "언제 왜 사용하는지 상세 설명 (30자 이상)",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "파라미터 설명"},
            },
            "required": ["param1"],  # 필수 파라미터 목록
        },
    },
}
```
</details>

<details>
<summary>힌트 2: Agent 루프 구조</summary>

```python
while True:
    response = client.chat.completions.create(
        model=MODEL, messages=messages,
        tools=tools, tool_choice="auto",
    )
    msg = response.choices[0].message
    if not msg.tool_calls:
        return msg.content          # 최종 답변
    messages.append(msg)
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        result = execute_tool(tc.function.name, args)
        messages.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "content": json.dumps(result, ensure_ascii=False),
        })
```
</details>

<details>
<summary>힌트 3: 더미 데이터 예시</summary>

```python
if name == "get_jira_tickets":
    return {
        "tickets": [
            {"id": "BE-101", "title": "API 구현", "status": "Done"},
        ]
    }
```
</details>

### 정답 확인

```bash
just run-solution
```

---

## 검증 방법

```bash
just test
```

## 트러블슈팅

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| Tool이 호출되지 않음 | description이 너무 짧거나 모호함 | "언제 사용해야 하는지" 명시 |
| 무한 루프 | Tool 결과를 messages에 추가 안 함 | `role: "tool"` 메시지 추가 확인 |
| `json.JSONDecodeError` | `arguments` 파싱 실패 | `json.loads(tc.function.arguments)` 확인 |
| Tool 선택 오류 | 유사한 이름의 Tool 혼동 | Tool 이름을 명확하게 구분하거나 description 보강 |
