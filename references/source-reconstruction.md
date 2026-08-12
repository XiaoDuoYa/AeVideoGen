# Source-backed product reconstruction

## Contents

1. Evidence order
2. Repository audit
3. Reconstruction rules
4. Interaction fidelity
5. Proportion and typography
6. Deterministic rendering
7. Privacy and licensing

## 1. Evidence order

Use evidence in this priority:

1. requested source version or commit;
2. supplied source files and bundled assets;
3. authenticated live product state;
4. public product documentation;
5. user-confirmed inference.

Do not let a reference film, competitor, or inspiration site override the product source. References provide motion language, not assets to copy.

## 2. Repository audit

Before animation, record:

- repository root, dirty state, branch, commit, and product version;
- entry route and relevant feature routes;
- component files for each filmed state;
- state/store/API logic that causes transitions;
- base panel dimensions and responsive breakpoints;
- CSS variables, fonts, icons, SVGs, and image assets;
- exact labels, answer content, empty/loading/error/success states;
- target elements and their actual hit areas.

Create an evidence ledger such as:

| Claim or shot | Source evidence | State needed | Verified |
|---|---|---|---|
| “Ask Memory” opens a query panel | `src/...` | memory detail | yes |

If a filmed claim has no evidence, remove it or ask the user.

## 3. Reconstruction rules

- Prefer importing or copying real components into an isolated local composition.
- Reuse actual CSS, SVGs, icons, and fonts where permitted.
- Replace network data with deterministic local fixtures that match real schema and copy.
- Keep component state transitions intact when feasible.
- If the product stack is difficult to embed, recreate the smallest faithful DOM from the source, not from a screenshot.
- Do not ship credentials, private API responses, personal messages, or unrelated user data in fixtures.
- Remove runtime dependence on external APIs before frame rendering.
- Record every intentional deviation from the source.

## 4. Interaction fidelity

- Derive target rectangles after fonts and layout have settled.
- Use the element center or a deliberate in-control point:

```js
const rect = element.getBoundingClientRect();
const x = rect.left + rect.width / 2;
const y = rect.top + rect.height / 2;
```

- Convert the point into composition-normalized coordinates only after the final scale and layout are known.
- Make the pointer, ripple, pressed state, and camera focus agree on the same point.
- React within 2–5 frames after the click.
- Test with the actual rendered control, not an invisible oversized proxy.
- When the real control has a small hit area, enlarge the browser interaction region without visually moving the control, then keep the animated click on the visible center.

## 5. Proportion and typography

- Record every native surface dimension, for example `380×900`.
- Apply one uniform scale:

```css
transform: translate(...) scale(var(--uniform-scale));
transform-origin: center;
```

- Never use independent `scaleX`/`scaleY` for product UI.
- Do not resize internal type merely to fill the video canvas.
- Use high pixel density for validation screenshots.
- Compose negative space with background, depth, typography, or supporting graphics rather than distorting the product.

## 6. Deterministic rendering

- Expose a pure time render hook such as `window.__AE_VIDEO__.render(t)`.
- Derive every visual state from `t`, not from wall-clock timers.
- Wait for `document.fonts.ready` and all images before capture.
- Disable random behavior or seed it.
- Keep local fixtures stable.
- Use versioned frame directories; stale frames can silently corrupt a new render.
- Test both direct time seeking and uninterrupted playback.

## 7. Privacy and licensing

- Use only assets the user owns, supplies, or is permitted to reuse.
- Do not copy images or source from inspiration products.
- Redact credentials, tokens, personal data, analytics identifiers, and private conversations.
- Prefer synthetic but schema-faithful fixtures for private product data.
- Preserve attribution or notices required by bundled assets.

