# 시나리오 3: Markdown → HTML 변환기

**난이도**: ★★☆
**예상 완성 시간**: 35~45분
**언어**: Python (표준 라이브러리만 사용)

---

## 앱 개요

Markdown 파일을 읽어 스타일이 적용된 HTML로 변환하는 CLI 도구.
외부 라이브러리 없이 정규식과 문자열 처리만으로 구현한다.

---

## 필수 기능 (30점 만점 기준)

### 기능 1: 기본 Markdown 파싱
아래 요소를 모두 변환해야 한다:

| Markdown | HTML |
|----------|------|
| `# 제목` ~ `### 제목` | `<h1>` ~ `<h3>` |
| `**볼드**` | `<strong>` |
| `*이탤릭*` | `<em>` |
| `` `인라인 코드` `` | `<code>` |
| ` ```코드블록``` ` | `<pre><code>` |
| `[링크](url)` | `<a href="url">` |
| `- 목록` | `<ul><li>` |
| `1. 순서 목록` | `<ol><li>` |
| `---` | `<hr>` |
| 빈 줄 구분 단락 | `<p>` |

### 기능 2: HTML 출력
- `python mdconv.py input.md` — `input.html` 생성
- `python mdconv.py input.md -o output.html` — 출력 파일 지정
- CSS 스타일 내장 (읽기 좋은 기본 스타일)

### 기능 3: 파일 감시(watch) 모드
- `python mdconv.py input.md --watch` — 파일 변경 감지 시 자동 재변환
- 변환 성공/실패 메시지 출력

---

## 선택 기능 (도전 정신 15점)

- `> 인용구` → `<blockquote>` 변환
- `![이미지](url)` → `<img>` 변환
- `--theme dark` 옵션으로 다크 테마 CSS 적용
- 변환 통계 출력 (줄 수, 이미지 수, 링크 수)

---

## CSS 스타일 요구사항

생성된 HTML은 별도 CSS 파일 없이도 브라우저에서 바로 읽기 좋아야 한다.
최소 요구사항:
- 최대 너비 800px, 중앙 정렬
- 코드블록 배경색 구분
- 글꼴 가독성 (system font 또는 monospace for code)

---

## 테스트 요구사항

- 각 Markdown 요소별 변환 결과 단위 테스트
- 중첩 요소 처리 (볼드 안에 이탤릭 등)
- 빈 파일, 특수문자 포함 파일 처리

---

## 프로젝트 구조 예시

```
my-md-converter/
├── AGENTS.md
├── mdconv.py         # 메인 진입점 (CLI + watch 모드)
├── parser.py         # Markdown 파싱 로직
├── renderer.py       # HTML 렌더링 + CSS
├── watcher.py        # 파일 감시
├── test_parser.py    # 파싱 단위 테스트
└── sample.md         # 테스트용 샘플 파일
```
