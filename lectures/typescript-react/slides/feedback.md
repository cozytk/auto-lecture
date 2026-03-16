- `# 왜 TypeScript인가? (1/2)` 부분에서 발표자 대본 싱크가 안 맞아. 맨 처음부터 첫 번째 클릭(`[click]`)이 하이라이팅 되어야 하고 지금은 마지막 클릭은 아예 넘어가는 구조야.
- 아래 클래스("box-*")를 사용할 다크모드 지원이 안 돼.
```
<div class="box-red">
JavaScript는 <strong>런타임</strong>까지 오류를 알 수 없습니다 — 코드가 실행되어야 버그가 드러납니다
</div>
```
- 지금 `col-left`, `col-right` 적용이 안됐어. 그냥 위에서부터 아래로 쭉 나와
- `# 기본 타입 (2/3) — 타입 추론과 any` 이 페이지 내용이 넘쳤어. 방지할 수 있나? 일단 코드는 기본적으로 scrollable 하게 작성 가능해.
"""공식문서
Max Height
If the code doesn't fit into one slide, you use the maxHeight to set a fixed height and enable scrolling:


```ts {2|3|7|12}{maxHeight:'100px'}
function add(
  a: Ref<number> | number,
  b: Ref<number> | number
) {
  return computed(() => unref(a) + unref(b))
}
/// ...as many lines as you want
const c = add(1, 2)
```
Note that you can use {*} as a placeholder of ✨ Line Highlighting✨ Line Highlighting:


```ts {*}{maxHeight:'100px'}
// ...
```
```
"""
- 전체적으로 분량이 아래가 잘리는 장표가 많아. 내가 어떤 장표인지 일일이 다 알려줘야하나? 해결할 수 있는 방법이 있나?