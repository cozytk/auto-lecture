# Notion-flavored Markdown 레퍼런스

guide-writer가 산출물(.md)을 작성할 때 참조하는 Notion 호환 마크다운 문법이다.
이 문법으로 작성하면 Notion API(`notion-create-pages`)를 통해 그대로 업로드할 수 있다.

> 이 문서는 Notion Enhanced Markdown Spec (`notion://docs/enhanced-markdown-spec`)을 교안 작성 맥락에 맞게 정리한 것이다.

## 핵심 인사이트

노션에는 **두 가지** 마크다운 처리 경로가 있다:

1. **복사-붙여넣기**: 표준 마크다운만 지원. 토글, 콜아웃, 컬럼, 색상 없음. `<details>` 태그 무시됨. `>`는 인용 블록(토글 아님).
2. **Notion API** (`notion-create-pages`): "Notion-flavored Markdown" 지원. 토글, 콜아웃, 컬럼, 색상 텍스트, 토글 헤딩 등 모든 리치 블록 사용 가능.

**원칙: 리치 콘텐츠를 노션에 넣으려면 복사-붙여넣기가 아닌 반드시 API를 사용한다.**

최신 스펙은 MCP 리소스로 확인 가능:
```
ReadMcpResourceTool(server="claude.ai Notion", uri="notion://docs/enhanced-markdown-spec")
```

---

## 기본 블록 (표준 마크다운과 동일)

### 헤딩

```markdown
# 헤딩 1
## 헤딩 2
### 헤딩 3
#### 헤딩 4
```

- H5, H6은 노션에서 H4로 변환된다.

### 텍스트 서식

```markdown
**볼드** *이탤릭* ~~취소선~~ `인라인 코드`
[링크 텍스트](URL)
```

밑줄은 노션 전용 문법:
```markdown
<span underline="true">밑줄 텍스트</span>
```

### 리스트

```markdown
- 불릿 리스트
  - 중첩 (탭으로 들여쓰기)

1. 번호 리스트
   1. 중첩

- [ ] 체크박스 미완료
- [x] 체크박스 완료
```

### 코드 블록

````markdown
```python
def hello():
    print("Hello")
```
````

- 언어 지정 시 자동 구문 강조
- **코드 블록 안에서는 이스케이프(`\`)하지 않는다.** 있는 그대로 작성.

### 구분선

```markdown
---
```

### 인용 블록

```markdown
> 인용 텍스트 {color="gray_bg"}
```

- 여러 줄: `<br>` 사용 (줄바꿈하면 별도 블록이 됨)
```markdown
> 첫째 줄<br>둘째 줄<br>셋째 줄
```

### 수학 수식

```markdown
$$
E = mc^2
$$
```

인라인: `$a^2 + b^2 = c^2$` (앞뒤에 공백 필요)

---

## 노션 전용 블록

### 콜아웃

```markdown
<callout icon="💡" color="blue_bg">
	콜아웃 본문. **볼드**, `코드` 등 서식 가능.
	여러 블록을 포함할 수 있다.
	- 리스트도 가능
</callout>
```

교안에서 자주 쓰는 콜아웃 패턴:

| 용도 | icon | color | 예시 |
|------|------|-------|------|
| 학습 목표 | 📖 | blue_bg | 세션 시작부 |
| 팁/참고 | 💡 | gray_bg | 보충 설명 |
| 주의사항 | ⚠️ | yellow_bg | 흔한 실수 |
| 에러/금지 | ❌ | red_bg | 잘못된 패턴 |
| 성공/완료 | ✅ | green_bg | 올바른 패턴 |
| 요구사항 | 📋 | yellow_bg | 과제 조건 |
| macOS 안내 | 🍎 | gray_bg | OS별 차이 |

### 토글 (접이식)

```markdown
<details>
<summary>클릭하면 열리는 토글</summary>
	토글 안의 내용 (반드시 탭 들여쓰기!)
	- 리스트도 가능
	```python
	print("코드도 가능")
	```
</details>
```

**핵심: 자식 블록은 반드시 탭(`\t`)으로 들여쓰기해야 토글 안에 포함된다.**

컬러 토글:
```markdown
<details color="blue_bg">
<summary>파란 배경 토글</summary>
	내용
</details>
```

### 토글 헤딩 ⭐

교안에서 가장 많이 쓰는 패턴. 헤딩에 `{toggle="true"}`를 추가하면 접이식 헤딩이 된다.

```markdown
### 힌트: 문제 풀이 접근법 {toggle="true"}
	숨겨진 내용 (반드시 탭 들여쓰기!)
	- 핵심 포인트 1
	- 핵심 포인트 2
```

색상 지정:
```markdown
### 🔍 I DO: 시연 코드 {toggle="true" color="blue"}
	내용

### 🤝 WE DO: 함께 실습 {toggle="true" color="green"}
	내용

### 🚀 YOU DO: 독립 과제 {toggle="true" color="purple"}
	내용
```

**H1~H3 모두 토글 헤딩 가능:**
```markdown
# 대주제 토글 {toggle="true"}
	내용

## 중주제 토글 {toggle="true"}
	내용

### 소주제 토글 {toggle="true"}
	내용
```

### 테이블

노션 전용 테이블은 색상, 헤더 행/열 지정이 가능하다:

```markdown
<table header-row="true" fit-page-width="true">
	<tr>
		<td>**헤더 1**</td>
		<td>**헤더 2**</td>
	</tr>
	<tr>
		<td>데이터 1</td>
		<td>데이터 2</td>
	</tr>
</table>
```

- `header-row="true"`: 첫 행을 헤더로
- `header-column="true"`: 첫 열을 헤더로
- `fit-page-width="true"`: 페이지 너비에 맞춤
- 셀 안에는 리치 텍스트만 가능 (블록 불가)
- 셀 색상: `<td color="red">`, 행 색상: `<tr color="blue_bg">`

**간단한 테이블은 표준 마크다운도 가능** (노션이 자동 변환):
```markdown
| 구분 | 설명 |
|------|------|
| A | 내용 |
```

### 컬럼 레이아웃

```markdown
<columns>
	<column>
		왼쪽 컬럼 내용
	</column>
	<column>
		오른쪽 컬럼 내용
	</column>
</columns>
```

### 색상

**블록 색상** (블록 전체에 적용):
```markdown
이 블록은 파란색 텍스트 {color="blue"}
이 블록은 노란 배경 {color="yellow_bg"}
```

**인라인 색상** (텍스트 일부에 적용):
```markdown
이것은 <span color="red">빨간색</span>이고 <span color="blue">파란색</span>입니다.
```

사용 가능한 색상:
- 텍스트: gray, brown, orange, yellow, green, blue, purple, pink, red
- 배경: gray_bg, brown_bg, orange_bg, yellow_bg, green_bg, blue_bg, purple_bg, pink_bg, red_bg

### 빈 줄

```markdown
<empty-block/>
```

일반 빈 줄은 노션에서 제거된다. 명시적 빈 줄이 필요하면 `<empty-block/>`을 사용한다.

---

## 교안 작성 패턴

### 퀴즈 패턴

```markdown
**Q1. Docker 컨테이너와 가상머신의 가장 큰 차이는?**

A) 운영체제 공유 여부
B) 네트워크 격리
C) 파일시스템 격리
D) CPU 할당 방식

<details>
<summary>💡 힌트</summary>
	컨테이너는 호스트 OS의 커널을 공유합니다. VM은요?
</details>

<details>
<summary>✅ 정답</summary>
	**A) 운영체제 공유 여부**
	**설명:** 컨테이너는 호스트 OS 커널을 공유하여 경량 실행됩니다. VM은 각자 게스트 OS를 포함하므로 무겁습니다.
</details>
```

### I DO / WE DO / YOU DO 패턴

```markdown
<callout icon="📖" color="blue_bg">
	**학습 목표:** Docker 컨테이너의 기본 개념을 이해하고 직접 실행할 수 있다.
</callout>

### 🔍 I DO: Docker 컨테이너 실행 {toggle="true" color="blue"}
	강사가 시연하는 코드를 관찰하세요.
	```bash
	docker run hello-world
	docker ps -a
	```
	<callout icon="💡" color="gray_bg">
		`docker run`은 이미지 다운로드 + 컨테이너 생성 + 실행을 한 번에 수행합니다.
	</callout>

### 🤝 WE DO: 함께 Nginx 띄우기 {toggle="true" color="green"}
	1. 아래 명령어를 함께 입력합니다
	```bash
	docker run -d -p 8080:80 nginx
	```
	2. 브라우저에서 `http://localhost:8080` 접속
	- [ ] Nginx 기본 페이지가 보이나요?
	- [ ] `docker ps`로 실행 중인 컨테이너를 확인했나요?

### 🚀 YOU DO: 독립 과제 {toggle="true" color="purple"}
	**과제:** Python Flask 앱을 Docker로 실행하세요.
	<callout icon="📋" color="yellow_bg">
		**요구사항:**
		- Flask 이미지를 사용하여 컨테이너 실행
		- 포트 5000을 호스트의 5000에 매핑
		- 브라우저에서 접속 확인
	</callout>

<details>
<summary>💡 힌트</summary>
	`docker run -d -p 5000:5000 python:3.11-slim` 을 기반으로 생각해보세요.
</details>

<details>
<summary>✅ 정답</summary>
	```bash
	docker run -d -p 5000:5000 flask-app
	```
</details>
```

### macOS 호환 안내 패턴

```markdown
<callout icon="🍎" color="gray_bg">
	**macOS 사용자 안내**
	`apt-get` 대신 `brew`를 사용하세요:
	```bash
	brew install {패키지명}
	```
</callout>
```

### 주의사항/오해 패턴

```markdown
<callout icon="⚠️" color="yellow_bg">
	**흔한 오해:** "컨테이너는 가상머신의 경량 버전이다"
	→ **실제:** 컨테이너는 VM과 근본적으로 다른 격리 기술입니다. 커널을 공유하므로 "경량 VM"이 아닙니다.
</callout>
```

---

## 노션 업로드

가이드 .md 파일을 Notion API로 업로드할 때:

1. `notion-create-pages` 도구를 사용한다
2. `content` 파라미터에 .md 파일 내용을 전달한다 (제목 제외)
3. `properties.title`에 페이지 제목을 지정한다
4. 특정 페이지 하위에 만들려면 `parent.page_id`를 지정한다

```json
{
  "parent": {"page_id": "상위 페이지 ID"},
  "pages": [{
    "properties": {"title": "Day 1 - Session 1: Docker 기초"},
    "icon": "📖",
    "content": "... Notion-flavored markdown 내용 ..."
  }]
}
```

### 들여쓰기 주의사항

Notion-flavored Markdown에서 **자식 블록의 들여쓰기는 반드시 탭(`\t`) 문자**를 사용한다.
스페이스 들여쓰기는 노션이 자식 블록으로 인식하지 못할 수 있다.

특히 토글, 콜아웃, 컬럼 안의 내용은 반드시 탭으로 들여써야 한다:

```
<details>
<summary>제목</summary>
→탭→이 내용이 토글 안에 들어간다
→탭→- 리스트도 탭 들여쓰기
→탭→```python
→탭→코드도 탭 들여쓰기
→탭→```
</details>
```
