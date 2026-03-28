# MCP vs CLI — 트렌드 리서치 브리프

> 리서치 날짜: 2026-03-16
> 검색 소스: 테크 블로그 (Medium, DEV, Substack), 커뮤니티 (Hacker News, Reddit), 공식 블로그 (Anthropic, Google), 보안 리서치, 벤치마크

## 핵심 트렌드 요약

2026년 3월 현재, MCP는 "업계 표준으로 자리 잡았지만 비판도 거세다"는 양면적 상황에 놓여 있다. OpenAI, Google, Microsoft가 모두 MCP를 채택하고 Linux Foundation 산하 Agentic AI Foundation(AAIF)에 거버넌스가 이관되면서 **프로토콜의 지위는 확고**해졌다. 그러나 동시에 "MCP is a fad"(Hacker News), "CLI가 MCP를 이기고 있다"(벤치마크), "95%의 MCP 서버가 쓰레기"(Reddit) 등 **실무 현장의 회의론**도 뚜렷하다. 핵심 논쟁은 "MCP가 정말 필요한가 vs CLI로 충분한가"에서 "둘을 어떻게 조합할 것인가"로 이동 중이다.

## 찬성 논거 (MCP 긍정적 시각)

- **업계 전체 채택**: OpenAI(2025.03), Google DeepMind(2025.04), Microsoft가 MCP 지원. 월간 SDK 다운로드 9,700만, 서버 10,000+개, 클라이언트 300+개. 출처: [Pento - A Year of MCP](https://www.pento.ai/blog/a-year-of-mcp-2025-review)
- **거버넌스 안정화**: 2025.12 Anthropic이 MCP를 Linux Foundation 산하 AAIF에 기부. Anthropic, Block, OpenAI 공동 설립, Google/MS/AWS 지원. 출처: [Anthropic 공식](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- **N×M → N+M 해결**: AI 앱과 도구 간 연동의 표준화. 한 번 만든 MCP 서버를 Claude, Cursor, VS Code 등에서 재사용. 출처: [CIO - Why MCP on Every Executive Agenda](https://www.cio.com/article/4136548/why-model-context-protocol-is-suddenly-on-every-executive-agenda.html)
- **비판이 오히려 성숙의 증거**: "공격할 가치가 있으니 공격당하고, 그 결과 더 안전해졌다." 보안 연구자들의 취약점 발견 → 커뮤니티 대응으로 프로토콜 개선. 출처: [StackOne - What a Year in Production Taught Us](https://www.stackone.com/blog/mcp-where-its-been-where-its-going/)

## 반대 논거 (비판/회의론)

- **"MCP is a fad" (유행일 뿐이다)**: Hacker News에서 MCP가 과대포장된 미들웨어에 불과하다는 주장. "over-engineered middleware destined for obsolescence." 출처: [HN - MCP is a fad](https://news.ycombinator.com/item?id=46552254)
- **CLI가 벤치마크에서 MCP를 압도**: CLI가 28% 더 높은 작업 완료율, 33% 더 높은 토큰 효율성(Token Efficiency Score: CLI 202 vs MCP 152). MCP는 3-4회 도구 호출 후 컨텍스트 윈도우 포화로 추론 품질 저하. 출처: [GitHub Gist - Benchmark Comparison](https://gist.github.com/szymdzum/c3acad9ea58f2982548ef3a9b2cdccce)
- **보안의 근본적 결함**: 인증 메커니즘 미비, 88%의 서버가 자격 증명 필요하지만 53%가 정적 API 키에 의존. Figma MCP 서버에서 RCE(원격 코드 실행) 취약점 발견(CVE-2025-53967). 출처: [Astrix Security Report](https://astrix.security/learn/blog/state-of-mcp-server-security-2025/), [ScalifiAI - Six Fatal Flaws](https://www.scalifiai.com/blog/model-context-protocol-flaws-2025)
- **"95%의 MCP 서버가 쓰레기"**: Reddit MCP 서브레딧의 공통 불만. 서버 퍼블리싱 장벽은 낮지만 좋은 서버의 기준은 높다. 출처: [StackOne](https://www.stackone.com/blog/mcp-where-its-been-where-its-going/)
- **토큰 낭비**: MCP 도구 메타데이터가 매 호출마다 LLM 컨텍스트에 반복 주입 → 토큰 소비 증가, 비용 상승. 출처: [arxiv - Smelly Tool Descriptions](https://arxiv.org/html/2602.14878v1)
- **"MCP는 충분하지 않다"**: Agent에는 identity, persistent state, lifecycle, delegation 능력이 필요. MCP는 이 중 아무것도 정의하지 않는다. 출처: [Medium - MCP Is Not Enough](https://medium.com/@thomas.scola/mcp-is-not-enough-the-missing-gaps-in-open-agent-standards-3bc31e7b4e59)

## 최근 주요 동향 (6개월 이내)

| 날짜 | 사건/발표 | 의미 |
|------|----------|------|
| 2025-12 | Anthropic, MCP를 Linux Foundation AAIF에 기부 | 특정 벤더 종속 탈피, 업계 공동 거버넌스 확립 |
| 2025-12 | Google, 관리형 MCP 서버 출시 (Maps, BigQuery 등) | 빅테크의 본격적 MCP 인프라 투자 |
| 2026-01 | MCP 2026 로드맵 발표 | 엔터프라이즈 인증, 감사 추적, 게이트웨이 기능 강화 예고 |
| 2026-02 | "Why CLI Tools Are Beating MCP" 시리즈 다수 게시 | CLI 우위론이 본격적 담론으로 부상 |
| 2026-02 | "The MCP vs CLI Debate Is the Wrong Fight" 반론 | "둘 다 써라"는 실용주의 시각 등장 |
| 2026-03 | MCP 보안 연구 보고서들 연이어 발표 | 88% 서버가 자격증명 필요, 53% 정적 시크릿 의존 |

## 주요 소스

| # | 제목 | 유형 | 핵심 주장 | URL |
|---|------|------|-----------|-----|
| 1 | MCP is a fad | HN 토론 | MCP는 과대포장된 유행 | https://news.ycombinator.com/item?id=46552254 |
| 2 | Why CLI Tools Are Beating MCP for AI Agents | 테크 블로그 | CLI가 벤치마크에서 MCP를 압도 | https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/ |
| 3 | The MCP vs. CLI Debate Is the Wrong Fight | Medium | 둘은 경쟁이 아니라 보완 관계 | https://medium.com/@tobias_pfuetze/the-mcp-vs-cli-debate-is-the-wrong-fight-a87f1b4c8006 |
| 4 | CLI vs MCP for AI Agents | Medium | CLI 에이전트 구축 실전 비교 | https://medium.com/@visrow/cli-vs-mcp-for-ai-agents-how-to-build-a-cli-tool-calling-agent-d3e7bb8252c2 |
| 5 | MCP vs CLI: Which is best for production? | DEV | 프로덕션 환경에서의 실전 비교 | https://dev.to/mathewpregasen/mcp-vs-cli-tools-which-is-best-for-production-applications-bd8 |
| 6 | Six Fatal Flaws of MCP | ScalifiAI | 보안, 인증, 거버넌스의 6가지 근본적 결함 | https://www.scalifiai.com/blog/model-context-protocol-flaws-2025 |
| 7 | Function Calling vs MCP vs A2A | Zilliz | 세 가지 프로토콜 비교 가이드 | https://zilliz.com/blog/function-calling-vs-mcp-vs-a2a-developers-guide-to-ai-agent-protocols |
| 8 | State of MCP Server Security 2025 | Astrix | 88% 자격증명 필요, 53% 정적 시크릿 | https://astrix.security/learn/blog/state-of-mcp-server-security-2025/ |
| 9 | A Year of MCP: Review | Pento | 1년간 MCP 성장 데이터와 분석 | https://www.pento.ai/blog/a-year-of-mcp-2025-review |
| 10 | MCP: What's Working, What's Broken | StackOne | 1년 프로덕션 경험에서 배운 것 | https://www.stackone.com/blog/mcp-where-its-been-where-its-going/ |
| 11 | Donating MCP to AAIF | Anthropic | MCP 거버넌스를 Linux Foundation에 이관 | https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation |
| 12 | MCP Is Not Enough | Medium | Agent 표준으로서 MCP의 한계 | https://medium.com/@thomas.scola/mcp-is-not-enough-the-missing-gaps-in-open-agent-standards-3bc31e7b4e59 |
| 13 | Why the Model Context Protocol Won | The New Stack | MCP가 표준이 된 이유 분석 | https://thenewstack.io/why-the-model-context-protocol-won/ |
| 14 | Why CLI is the New MCP | OneUptime | CLI가 다시 MCP를 대체할 것이라는 주장 | https://oneuptime.com/blog/post/2026-02-03-cli-is-the-new-mcp/view |

## 가이드 반영 포인트

### 본문 반영
- **"왜 중요한가" 섹션**: MCP가 2025.12에 Linux Foundation에 기부되고, OpenAI/Google/MS가 모두 채택한 사실 → "업계 표준" 근거
- **"주의사항과 흔한 오해" 섹션**: 벤치마크에서 CLI가 MCP를 이기는 상황, "MCP is a fad" 논쟁, 보안 결함 53% 정적 시크릿 문제
- **"실무에서의 의미" 섹션**: "95%의 MCP 서버가 쓰레기"라는 현실적 주의사항
- **비교 섹션**: CLI Token Efficiency Score 202 vs MCP 152 벤치마크 데이터 인용

### Q&A 반영
- Q: "MCP는 유행일 뿐 아닌가요?" → AAIF 거버넌스, 빅테크 채택 근거로 답변
- Q: "보안이 걱정되는데 프로덕션에 써도 되나요?" → 53% 정적 시크릿 문제, OAuth 채택률 8.5%에 불과, 2026 로드맵에서 개선 예고
- Q: "CLI로 충분하지 않나요?" → 벤치마크에서 CLI가 유리하지만, 도구 5개+ 규모에서 관리성 역전. "둘 다 쓰는 것이 현실적"

### 슬라이드/대본 반영
- 비교 슬라이드에 벤치마크 수치(CLI 202 vs MCP 152) 추가
- "MCP is a fad" 논쟁을 소개하고 양쪽 근거를 공정하게 다루는 슬라이드 추가
- "The MCP vs CLI Debate Is the Wrong Fight" 관점을 결론에 반영
