# External Source Screenshot Capture — Site Suitability Heuristic

모든 웹사이트가 Playwright 캡처에 적합하지 않다. **사이트를 선택하는 단계가 캡처 품질의 80%를 결정**한다.

## 1단계: 사이트 적합성 사전 판단

```
이 사이트가 정적 서버 렌더링(SSR)인가?
  → YES (HN, The New Stack, OneUptime, 정적 블로그): 캡처 적합 ✅
  → NO: SPA인가?
    → YES (일부 블로그, React 기반): 본문 지연 로딩 위험 ⚠️
      → wait_for_timeout(5000) + scroll_into_view 시도
    → Cloudflare/reCAPTCHA 차단?
      → YES (Medium, 일부 기업 블로그): 캡처 불가 ❌ → 대체 소스

봇 차단 사이트 대체 우선순위:
  1. DEV.to (같은 글의 크로스포스트 검색)
  2. The New Stack, OneUptime, Builder.io 등 개발자 블로그
  3. 원문의 archive.org 캐시
  4. 텍스트 인용 + 링크 (스크린샷 포기)
```

## 2단계: 캡처 품질 티어

| 티어 | 사이트 예시 | 특징 | 대응 |
|------|-----------|------|------|
| **A (완벽)** | Hacker News, GitHub Gist | 정적 HTML, 팝업 없음, h1 명확 | 그대로 캡처 |
| **B (쿠키만)** | The New Stack, OneUptime | SSR이지만 쿠키 배너 있음 | Accept 클릭 → 캡처 |
| **C (다중 배너)** | DEV.to | 쿠키+로그인+커뮤니티 배너 중첩 | 3단계 제거 필요, 결과 불안정 |
| **D (SPA)** | Jannik Reinhard 블로그 | 히어로만 보이고 본문 미렌더링 | scroll + 대기, 그래도 불안정 |
| **F (차단)** | Medium, 일부 기업 사이트 | Cloudflare/reCAPTCHA | 캡처 불가, 대체 소스 필수 |

## 3단계: 캡처 vs 텍스트 인용 의사결정

```
사이트가 A~B 티어인가?
  → YES: 캡처하여 슬라이드에 이미지로 삽입
  → NO (C~F): 텍스트 인용 + 클릭 가능 링크로 대체
    → 같은 주제의 A~B 티어 대체 소스가 있는가?
      → YES: 대체 소스 캡처
      → NO: 텍스트 인용으로 충분
```

**핵심 원칙: 캡처 품질이 낮은 스크린샷보다 텍스트 인용이 낫다.**

## 검증된 A~B 티어 사이트 (2026-03 기준)

| 사이트 | 티어 | 비고 |
|--------|------|------|
| news.ycombinator.com | A | 정적 HTML, 팝업 없음 |
| thenewstack.io | B | Accept 클릭 1회로 해결 |
| oneuptime.com/blog | B | Accept all 클릭 1회로 해결 |
| www.scalifiai.com/blog | B | 상단 광고 배너 있지만 콘텐츠 가리지 않음 |
| github.com, gist.github.com | A | 정적, 로그인 불필요 페이지 한정 |

## 어노테이션 위치 결정

```
바운딩 박스 오른쪽에 공간이 충분한가? (x2 + 300 < img.width)
  → YES: 오른쪽에 어노테이션 (tx = x2 + 12)
  → NO: 바운딩 박스 아래에 어노테이션 (tx = x1, ty = y2 + 10)
```
