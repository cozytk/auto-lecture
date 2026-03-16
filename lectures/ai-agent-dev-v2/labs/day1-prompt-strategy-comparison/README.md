# 실습: 프롬프트 전략별 응답 비교

**유형**: 코드 실습 (Python)
**소요 시간**: Session 2 실습 60분
**관련 세션**: Day 1 Session 2

---

## 실습 목표

- Zero-shot / Few-shot / CoT 세 전략을 코드로 직접 구현한다
- 동일 태스크에 세 전략을 적용하고 결과를 정량적으로 비교한다
- Structured Output (Tool Use, JSON Schema)을 구현한다
- 비용과 지연 관점에서 최적 전략을 선택하는 판단력을 기른다

---

## 사전 요구사항

```bash
# Python 3.11 이상
python --version

# 의존성 설치
pip install anthropic python-dotenv

# API 키 설정
export ANTHROPIC_API_KEY="your-api-key"
```

---

## 디렉토리 구조

```
prompt-strategy-comparison/
├── README.md          # 이 파일
├── Justfile           # 실습 자동화 명령어
├── src/
│   ├── strategy_template.py    # 수강생이 채워야 할 템플릿
│   └── structured_output.py    # Structured Output 템플릿
└── solution/
    ├── strategy_comparison.py  # 전략 비교 정답 코드
    └── structured_output.py    # Structured Output 정답 코드
```

---

## I DO — 강사 시연 (15분)

강사가 리뷰 분류 태스크에 세 전략을 모두 적용하고 결과를 비교한다.

시연 순서:
1. `solution/strategy_comparison.py` 코드 설명
2. 세 전략 실행 결과 비교 (토큰, 지연, 응답 품질)
3. Structured Output Tool Use 구현 설명

---

## WE DO — 함께 실습 (20분)

강사와 함께 Structured Output을 구현한다.

### 단계 1: JSON Schema 설계

```python
# 분류 태스크를 위한 JSON Schema 설계
schema = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": ["긍정", "부정", "중립"]
        },
        "confidence": {
            "type": "number",
            "description": "0.0 ~ 1.0"
        },
        "reason": {
            "type": "string",
            "description": "분류 이유 (1문장)"
        }
    },
    "required": ["category", "confidence", "reason"]
}
```

### 단계 2: Tool Use 방식 구현

`src/structured_output.py` 파일을 열어 함께 구현한다.

### 단계 3: 에러 처리 추가

JSON 파싱 실패, API 오류 등의 에러 처리를 추가한다.

---

## YOU DO — 독립 실습 (25분)

### 과제: 세 전략 비교 구현

`src/strategy_template.py`를 열어 TODO 주석을 채운다.

**요구사항**:
1. 동일한 리뷰 분류 태스크에 Zero-shot, Few-shot, CoT 각각 구현
2. 각 전략의 토큰 수, 지연 시간, 응답 내용 출력
3. Structured Output (JSON) 방식으로 응답 받기
4. 결과를 비교하는 요약 출력

**완료 기준**:
- `just run` 명령어로 에러 없이 실행됨
- 세 전략의 결과가 모두 출력됨
- Structured Output 결과가 JSON으로 파싱됨

### 정답 확인

막히는 경우 `solution/strategy_comparison.py`를 참고한다.
단, 먼저 혼자 시도해볼 것.

---

## Justfile 명령어

```bash
# 의존성 설치
just setup

# 템플릿 실행 (YOU DO)
just run

# 정답 코드 실행
just solution

# 두 결과 비교
just compare
```
