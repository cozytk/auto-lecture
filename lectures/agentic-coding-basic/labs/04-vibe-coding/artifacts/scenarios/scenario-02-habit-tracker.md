# 시나리오 2: 터미널 습관 트래커

**난이도**: ★★☆
**예상 완성 시간**: 35~45분
**언어**: Python (표준 라이브러리만 사용)

---

## 앱 개요

매일 실천할 습관을 등록하고, 터미널에서 체크하며 꾸준함을 추적하는 앱.
연속 달성일(streak)이 오르는 것을 보며 동기부여를 얻는다.

---

## 필수 기능 (30점 만점 기준)

### 기능 1: 습관 관리
- `python habit.py add "운동 30분"` — 새 습관 등록
- `python habit.py list` — 오늘 해야 할 습관 목록 출력 (완료 여부 표시)
- `python habit.py done "운동 30분"` — 오늘 습관 완료 체크

### 기능 2: 통계 조회
- `python habit.py stats` — 전체 습관별 통계 출력
  - 연속 달성일 (streak)
  - 전체 달성률 (%)
  - 최장 연속 달성일

### 기능 3: CSV 내보내기
- `python habit.py export` — `habits_export.csv` 파일 생성
- 컬럼: 날짜, 습관명, 완료 여부

---

## 선택 기능 (도전 정신 15점)

- `python habit.py stats --week` — 주간 달성 현황 (ASCII 캘린더)
- `python habit.py remove "운동 30분"` — 습관 삭제
- 달성률 100% 시 축하 메시지 출력
- 습관 카테고리(건강/학습/생산성 등) 분류

---

## 데이터 저장 방식

```json
{
  "habits": ["운동 30분", "독서 20분", "물 2L 마시기"],
  "records": {
    "2024-01-15": ["운동 30분", "물 2L 마시기"],
    "2024-01-16": ["운동 30분", "독서 20분", "물 2L 마시기"]
  }
}
```

---

## 테스트 요구사항

- `pytest` 또는 `unittest`로 아래 항목 검증:
  - 습관 추가/삭제
  - streak 계산 정확성 (연속 달성일 끊김 처리 포함)
  - CSV 내보내기 형식

---

## 프로젝트 구조 예시

```
my-habit-tracker/
├── AGENTS.md
├── habit.py          # 메인 진입점 (CLI 파싱)
├── storage.py        # 데이터 저장/불러오기
├── stats.py          # streak 계산, 통계
├── export.py         # CSV 내보내기
├── test_habit.py     # 테스트
└── habits.json       # 데이터 파일 (자동 생성)
```
