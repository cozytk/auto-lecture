# Screenshot Tool Selection — Playwright vs agent-browser

agent-browser CLI는 AI 에이전트의 **인터랙티브 웹 탐색**용이고, Playwright 프로그래밍 API는 **배치 캡처 파이프라인**용이다.

## 판단 기준표

| 시나리오 | 도구 | 이유 |
|----------|------|------|
| Slidev 슬라이드 배치 캡처 | **Playwright** (`capture-slide.mjs`) | 정확한 뷰포트, 2.3초/장, 서버 내장, 다크모드 이중 토글 |
| 교육용 어노테이션 (빨간 박스, 밑줄) | **Playwright + Pillow 하이브리드** | 자유로운 그래픽 커스터마이즈, DOM 좌표 → Pillow 그리기 |
| 외부 웹사이트 탐색/캡처 | **agent-browser** | 세션 유지, 쿠키 배너 클릭, 인터랙션 체이닝 |
| AI가 웹 UI 요소를 파악 | **agent-browser `--annotate`** | 클릭 가능 요소 자동 번호 매핑 |

## agent-browser의 구체적 한계 (벤치마크)

1. **`--viewport` 플래그 무시**: 실제 출력 높이가 잘림 (800→633). DPR 보정 없음
2. **`--annotate` 노이즈**: 모든 interactive 요소에 빨간 번호 라벨 자동 부착 — 교육용 부적합
3. **`get box` 명령 무용**: "Done"만 출력하고 좌표값 미반환. `eval` + `getBoundingClientRect`로 우회 필수
4. **속도 오버헤드**: 매 커맨드마다 `npx` CLI 프로세스 재실행. 5장 기준 4.1초/장 vs Playwright 2.3초/장
5. **다크모드 불완전**: `--color-scheme dark`는 CSS만 제어. Slidev 내부 상태는 별도 `eval` 필요
6. **파일 크기**: 뷰포트가 커서 평균 27.8KB vs Playwright 20.6KB → 비전 분석 시 토큰 ~35% 추가 소비

## agent-browser가 유리한 경우

- 외부 웹사이트에서 팝업/쿠키 배너를 클릭으로 닫고 캡처할 때
- 로그인 → 탐색 → 캡처 같은 멀티스텝 인터랙션
- `snapshot` 명령으로 접근성 트리를 얻어 AI가 페이지 구조를 이해할 때
