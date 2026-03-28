# 시나리오 4: 팀 회고 보드

**난이도**: ★★★
**예상 완성 시간**: 45~55분
**언어**: Python (표준 라이브러리만 사용)

---

## 앱 개요

스프린트/프로젝트 회고를 진행할 때 사용하는 Keep/Problem/Try 보드.
CLI에서 의견을 수집하고, 투표하고, 결과를 정리한다.

---

## 필수 기능 (30점 만점 기준)

### 기능 1: 항목 추가
- `python retro.py add keep "코드 리뷰 문화가 좋았다"` — Keep 항목 추가
- `python retro.py add problem "배포 프로세스가 너무 느렸다"` — Problem 항목 추가
- `python retro.py add try "자동화 배포 도입"` — Try 항목 추가
- 카테고리: `keep` / `problem` / `try`

### 기능 2: 보드 조회
- `python retro.py board` — 전체 보드 출력
- 각 항목에 ID, 카테고리, 내용, 투표 수 표시
- 투표 수 기준 정렬

```
===== 팀 회고 보드 =====

[KEEP] 👍 유지할 것
  #1 [3표] 코드 리뷰 문화가 좋았다
  #2 [1표] 데일리 스탠드업

[PROBLEM] 🔴 문제점
  #3 [5표] 배포 프로세스가 너무 느렸다
  #4 [2표] 문서화 부족

[TRY] 🚀 시도할 것
  #5 [4표] 자동화 배포 도입
```

### 기능 3: 투표
- `python retro.py vote 3` — 항목 #3에 투표
- 중복 투표 방지 (IP 또는 세션 기반)
- 투표 결과 즉시 반영

### 기능 4: 결과 내보내기
- `python retro.py export` — `retro_result.md` 생성
- Markdown 형식으로 회고 결과 정리

---

## 선택 기능 (도전 정신 15점)

- `python retro.py serve` — 간단한 웹 UI (http://localhost:8000) — Python `http.server` 활용
- 회고 세션 이름 지정: `python retro.py new "스프린트 15 회고"`
- 여러 회고 세션 관리
- 항목 삭제/수정

---

## 웹 UI 선택 구현 시 (http.server 활용)

외부 라이브러리 없이 Python `http.server` + `json` + 인라인 HTML로 구현.
아래 페이지를 단일 Python 파일로 서빙:
- 보드 조회 페이지
- 항목 추가 폼
- 투표 버튼

---

## 테스트 요구사항

- 항목 추가/조회
- 투표 집계 정확성
- 중복 투표 방지 로직
- Markdown 내보내기 형식

---

## 프로젝트 구조 예시

```
my-retro-board/
├── AGENTS.md
├── retro.py          # 메인 진입점
├── storage.py        # 데이터 저장
├── board.py          # 보드 출력 로직
├── vote.py           # 투표 로직
├── export.py         # Markdown 내보내기
├── server.py         # (선택) 웹 UI
├── test_retro.py     # 테스트
└── retro_data.json   # 데이터 파일 (자동 생성)
```
