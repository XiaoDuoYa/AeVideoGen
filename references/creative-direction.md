# Creative direction rules

## Contents

1. Narrative grammar
2. Visual-subject discipline
3. Motion continuity
4. Camera and zoom
5. Typography
6. Product interaction
7. Transition grammar
8. Music structure
9. Timing heuristics
10. Failure patterns

## 1. Narrative grammar

Build a causal argument, not a feature carousel:

`context → friction → action → result → meaning`

- State the user's problem before presenting the control that solves it.
- Let each interaction answer the question created by the previous scene.
- Finish by restating the product value, not by replaying a feature list.
- Give the primary selling point the strongest musical, typographic, and camera emphasis.
- Treat secondary features as proof of breadth, not as competing climaxes.
- Follow an explicit user request for a more typographic film. Pure text can carry multiple transitions or sections when it remains readable and causally connected to product states.

Useful scene roles:

- **Hook:** establish a recognizable behavior or friction.
- **Discovery:** reveal the product entry point.
- **Proof:** perform the real action.
- **Payoff:** show the state change or answer.
- **Meaning:** name why the result matters.
- **Signature:** end with product identity and one remembered phrase.

## 2. Visual-subject discipline

- Assign one dominant subject per scene.
- Keep the dominant subject stable for at least 1.2 seconds unless a beat-driven burst is intentionally unreadable.
- Do not recenter more than once inside a short action. Move the world around the subject when possible.
- Allow a new subject to inherit position, shape, color, text, or motion from the previous one.
- Avoid repeatedly swapping unrelated center objects; it creates nausea and erases hierarchy.
- Keep supporting material dimmer, softer, smaller, or farther from the camera.

## 3. Motion continuity

Do not confuse “continuous” with “fast.”

- Avoid completely unchanged frames longer than 0.65 seconds.
- During readable holds, use one restrained living signal: 0.5–2% scale drift, 2–10 px camera travel, cursor settling, glow breathing, scroll inertia, parallax, or focus falloff.
- Keep micro-motion subordinate to reading. Never animate every property.
- Enter with acceleration, settle with damping, and leave by inheriting velocity or geometry.
- Avoid simultaneous unrelated movements. Sequence attention: camera → pointer → result.
- Use overlapping action by 3–8 frames to avoid robotic start/stop rhythm.
- Do not cut merely because the current scene has “finished.” Find a visual handoff.

## 4. Camera and zoom

- Zoom where the user clicks or where the audience must read.
- Compute the target center from final layout, not from memory.
- Use uniform scaling around a deliberate transform origin.
- Recommended focus scales for a 1280×720 composition:
  - context: 1.0–1.25×;
  - actionable UI: 1.55–2.25×;
  - deep detail: 2.25–2.8× only when text and native proportions survive.
- A strong zoom is preferable to an apologetic zoom that leaves the target unreadable.
- Use asymmetric easing: quicker intent, softer arrival, controlled release.
- Keep the clicked control inside the central safe area after zoom unless composition requires a deliberate offset.
- Never stretch a vertical panel to fill 16:9. Scale it uniformly and compose the negative space.

## 5. Typography

- Use at most three functional levels: statement, supporting line, UI text.
- Keep sizes consistent within each level.
- Forbid meaningless small copy added only to fill a panel or imitate complexity.
- Show one thought per title card. Large text earns its size through meaning.
- Declare every important headline `single-line` or `exact-lines`; test the actual rendered line count.
- Never allow responsive width, late font loading, or transform scale to create an accidental wrap.
- Do not impose a fixed text-to-UI ratio. When the user wants more pure typography, vary scale, mask, tracking, depth, line-breaking, and shared-element motion instead of repeating identical title cards.
- Estimate reading time before styling:
  - 4–8 Chinese characters: about 0.8–1.3 s;
  - 9–18 Chinese characters: about 1.4–2.5 s;
  - a sentence or two-line claim: about 2.5–4 s.
- Add transition time on top of reading time; do not count entry animation as full reading time.
- Complete a title entrance promptly enough to preserve most of the scene for unobstructed reading.
- For a question-to-input transition, show the question large first, then use the same element or a FLIP/shared-layout transform to dock it into the field.
- Do not crossfade two mismatched copies of the same text.
- Blur, dim, or defocus unimportant text while keeping enough context to understand the page.

## 6. Product interaction

- Focus first, click second, show feedback third.
- Make the pointer approach visible; do not teleport it onto the target.
- Use the real target center or a validated hotspot.
- Use the meaningful result group as the scene's visual center. A chat scene centers question plus response; a plugin overview centers the plugin, not only its send button.
- Trigger feedback promptly. A responsive target should react within roughly 2–5 frames.
- Keep the pressed, loading, success, and result states source-backed.
- Let the resulting content remain readable before moving on.
- When demonstrating a text-selection feature, show the selection, contextual island, chosen action, and result as one continuous interaction.

## 7. Transition grammar

Prefer transitions that explain why the next scene exists:

- **Shared element:** a card, icon, word, or button becomes the next composition.
- **Text docking:** a large question moves into the real input.
- **Shape inheritance:** a pill, panel, or highlight expands into a new surface.
- **Scroll continuity:** camera travel follows the page to the next feature.
- **Focus pull:** the current result blurs while the next control resolves.
- **Mask reveal:** use a native UI shape as the reveal boundary.
- **Value echo:** the result phrase becomes the closing brand statement.
- **Reference-derived handoff:** reproduce the reference video's spatial/easing logic with source-backed product elements.

Avoid:

- arbitrary zoom-to-black;
- unrelated scale pops;
- repeated center swaps;
- full-frame fades between states that could share geometry;
- cuts that interrupt an unfinished pointer or camera movement.

## 8. Music structure

- Analyze onset, energy, section changes, and climax candidates, then listen.
- Cut a coherent musical phrase; do not begin or end mid-breath unless intentional.
- Use beats to confirm motion, not to dictate every movement.
- Map major music events:
  - entry phrase → hook;
  - lift → discovery;
  - pre-climax tension → friction or “forgotten” state;
  - climax → primary promise;
  - release → proof, source, or signature.
- Give the climax a basin: 0.5–1.0 s approach, 1.2–2.5 s readable payoff, then release.
- If lyrics conflict with the product story, choose another segment or reduce semantic competition.

## 9. Timing heuristics

- 24–30 seconds usually supports 6–10 meaningful scenes.
- A UI scene typically needs 2.0–4.5 seconds.
- A simple click needs about 0.7–1.3 seconds including approach and feedback.
- A result or answer needs 1.8–3.5 seconds depending on text.
- Most seamless transitions need 10–24 frames at 30 fps.
- A product surface should not dominate unchanged for many seconds, but shortening it is not a substitute for motion design.
- If the audience cannot read the sentence at normal playback, timing is wrong even when still frames look beautiful.
- Keep scene duration and beat accents separate: elements may hit beats while the scene remains long enough to understand.

## 10. Failure patterns

Treat these as blocking defects:

- **Dead hold:** no motion, no reading intention, no tension.
- **Rush without work:** fast cuts that show no completed action.
- **Virtual click:** pointer misses the control or feedback appears elsewhere.
- **Miserly zoom:** focus scale changes but the important UI stays unreadable.
- **Wrong-center zoom:** the camera highlights empty space.
- **Subject pinball:** unrelated subjects repeatedly jump to center.
- **Aspect-ratio fraud:** a source surface is stretched to fit the canvas.
- **Typography roulette:** similar claims use arbitrary sizes.
- **Accidental wrap:** a designed one-line title breaks because layout was not measured.
- **Decorative microcopy:** tiny text exists without meaning or legibility.
- **Fake morph:** large text and input text differ in size, position, or wording during transition.
- **Feature soup:** multiple selling points compete in one scene.
- **Climax waste:** the strongest music moment is assigned to a minor feature.
- **Screenshot theater:** static media is scaled instead of rendering the real interface and states.
