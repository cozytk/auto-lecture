# 시나리오 5: 코드 스니펫 매니저

**난이도**: ★★☆
**예상 완성 시간**: 35~45분
**언어**: Python (표준 라이브러리만 사용)

---

## 앱 개요

자주 쓰는 코드 조각을 저장하고, 태그로 분류하고, 빠르게 검색해서 클립보드에 복사하는 CLI 도구.
개발자의 개인 코드 사전.

---

## 필수 기능 (30점 만점 기준)

### 기능 1: 스니펫 저장
- `python snippet.py add` — 대화형 입력 모드
  - 제목 입력
  - 언어 입력 (python, js, bash, sql 등)
  - 태그 입력 (쉼표 구분)
  - 코드 입력 (EOF 또는 특정 구분자로 종료)
- `python snippet.py add --file script.py --title "파일 읽기" --tags "io,file"` — 파일에서 추가

### 기능 2: 검색 및 조회
- `python snippet.py list` — 전체 스니펫 목록 (ID, 제목, 언어, 태그)
- `python snippet.py search "파일 읽기"` — 제목/태그/내용으로 검색
- `python snippet.py show 3` — 스니펫 #3 내용 출력
  - 터미널에서 언어별 구문 강조 (ANSI 컬러 코드 활용)

### 기능 3: 클립보드 복사
- `python snippet.py copy 3` — 스니펫 #3을 클립보드에 복사
  - macOS: `pbcopy`, Linux: `xclip` 또는 `xsel` 활용 (subprocess)
  - 복사 성공 메시지 출력

---

## 선택 기능 (도전 정신 15점)

- `python snippet.py delete 3` — 스니펫 삭제 (확인 프롬프트)
- `python snippet.py edit 3` — 스니펫 수정
- `python snippet.py export --format json` — JSON/Markdown으로 전체 내보내기
- 태그 자동완성 (기존 태그 목록 표시)
- 최근 사용 스니펫 우선 표시

---

## 구문 강조 구현 방법

외부 라이브러리 없이 ANSI 이스케이프 코드로 간단한 하이라이팅:
- 키워드 (`def`, `class`, `if`, `return` 등) → 노란색
- 문자열 (`"..."`, `'...'`) → 초록색
- 주석 (`#`, `//`) → 회색
- 숫자 → 파란색

```python
# 예시
YELLOW = "\033[33m"
GREEN = "\033[32m"
RESET = "\033[0m"
```

---

## 데이터 저장 형식

```json
{
  "snippets": [
    {
      "id": 1,
      "title": "파일 읽기",
      "language": "python",
      "tags": ["io", "file"],
      "code": "with open('file.txt', 'r') as f:\n    content = f.read()",
      "created_at": "2024-01-15T10:30:00",
      "used_count": 3
    }
  ]
}
```

---

## 테스트 요구사항

- 스니펫 추가/검색/삭제
- 태그 필터링
- 검색 결과 정확성 (부분 일치)
- 구문 강조 함수 단위 테스트

---

## 프로젝트 구조 예시

```
my-snippet-manager/
├── AGENTS.md
├── snippet.py        # 메인 진입점 (CLI)
├── storage.py        # 저장/불러오기
├── search.py         # 검색 로직
├── highlight.py      # ANSI 구문 강조
├── clipboard.py      # 클립보드 복사
├── test_snippet.py   # 테스트
└── snippets.json     # 데이터 파일 (자동 생성)
```
