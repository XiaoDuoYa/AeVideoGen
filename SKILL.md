---
name: ae-video-gen-by-hxdlabs
description: Create commercial-grade AE-style product launch, explainer, UI interaction, and feature-promo videos through deterministic web rendering from real product source code, websites, browser extensions, apps, music, brand assets, selling points, and reference videos. Use for 产品宣传片、发布会卖点总结、网页渲染视频、UI 动效演示、插件功能宣传、音乐卡点视频、参考视频动画复刻、类似 AE 的产品视频, especially when Codex must clarify an incomplete brief, densely analyze a reference video, preserve source-backed UI and proportions, build a causal story, align the primary promise with the music climax, obtain browser-preview approval, and export a stable MP4 without HyperFrames.
---

# AeVideoGen By HxdLabs_ v1.0.1

Create a product film that could be shipped commercially. Keep product behavior truthful, story causal, typography readable, focus intentional, motion alive, review exact, and export stable.

## Enforce the production contract

- Never use HyperFrames.
- Treat the requested product version and its source as visual and behavioral truth.
- Use reference videos for timing, motion grammar, camera language, typography, and transition structure; never copy third-party product assets or pretend another product is the user's.
- Preserve native UI proportions. Scale uniformly; never stretch.
- Make every pointer click the visible real control and make the camera focus the same target.
- Do not invent unsupported features, claims, source states, copy, icons, or layouts.
- Do not render a final video until the user explicitly approves the exact browser preview.
- Back up the accepted baseline before substantial changes and use versioned output paths.
- Do not silently downgrade resolution, frame rate, duration, source version, story priority, or music alignment.

## Run the completeness gate before implementation

Inspect the user's prompt and every supplied artifact first. Do not ask for facts already present in files, source, metadata, or conversation.

Immediately return a guided kickoff before implementation:

1. summarize what has already been received;
2. list blocking gaps and explain how each affects commercial quality;
3. proactively offer the exact assets or decisions the user can provide;
4. ask the next one to three highest-impact questions;
5. recommend Goal mode for multi-stage production and provide a paste-ready Goal objective, inputs, constraints, stages, and completion criteria.

For every blocking or useful missing decision, offer two or three concrete choices. Put the recommended choice first, explain the visible consequence of each choice, and let the user reply with “按推荐方案” when appropriate. Never block with an unexplained open-ended question.

Do not create a Goal unless the user explicitly asks to create/start/use Goal. The recommendation and ready-to-paste Goal brief are mandatory for substantial film work; automatic Goal creation is forbidden.

Create `brief.json` from `assets/web-motion-starter/brief.json`, then run:

```bash
python3 scripts/validate_brief.py brief.json
```

If a blocking field remains unknown, ask concise questions and continue asking in later turns until the brief is complete. Ask one to three related questions at a time. Do not begin creative implementation merely because some requirements were mentioned.

Proceed with recorded assumptions only when the user explicitly says to use best judgment, skip questions, or start with an incomplete brief. Mark every such field in `assumptions` and keep high-impact facts source-backed.

Read [references/intake-and-clarification.md](references/intake-and-clarification.md) completely whenever the brief is new, incomplete, contradictory, or materially revised.
Read [references/guided-production.md](references/guided-production.md) completely at kickoff and use its progress-report format throughout production.
Read [references/decision-options.md](references/decision-options.md) when requirements are missing or the user asks what to choose.

## Execute the workflow

### 1. Protect and audit

- Inspect repository state, version, routes, components, stores, styles, dimensions, fonts, icons, state transitions, target hit areas, and private data.
- Create a recoverable baseline before large edits.
- Build an evidence ledger mapping every filmed claim and state to source evidence or explicit user confirmation.
- Send a short progress report after audit: completed evidence, remaining risk, and the next reviewable artifact.
- Read [references/source-reconstruction.md](references/source-reconstruction.md) completely before reconstructing a product UI.

### 2. Analyze references without copying them

For every supplied reference video:

1. Read duration, resolution, frame rate, audio, and shot structure.
2. Extract frames densely enough to see animation—not multi-second thumbnails.
3. Add 8–12fps windows around cuts, morphs, zooms, text entrances, clicks, and transitions.
4. Watch the full reference at normal speed with audio.
5. Produce a motion-language ledger: subject, camera path, easing, duration, handoff, mask/shape, typography, hold, and sound cue.
6. Translate that grammar to the user's real product and brand.

Run `scripts/analyze_reference_video.py` for deterministic extraction. Read [references/reference-video-analysis.md](references/reference-video-analysis.md) completely before claiming a style match or recreation.

### 3. Write the causal film

Use this narrative chain:

`user context → friction → product action → visible result → remembered value`

- Give each scene one purpose and one dominant visual subject.
- Put the primary promise—not a secondary feature—inside the musical climax.
- Use pure text as meaningful punctuation or a shared element, never filler.
- Show a large question long enough to read, then morph/dock that same element into the actual input.
- Plan every headline line break. Never allow an accidental wrap.
- Create `production.json` before animation and keep it current.
- Run `scripts/validate_timeline.py production.json --strict` after timing changes.
- Report the proposed scene chain, climax placement, and unresolved creative decisions before full implementation.

Read [references/creative-direction.md](references/creative-direction.md) completely before designing the scene graph. Read [references/commercial-quality.md](references/commercial-quality.md) before declaring a direction commercially ready.

### 4. Analyze and edit music

Run:

```bash
python3 scripts/analyze_music.py music.mp3 --target-duration 30 --output music-map.json
```

- Listen to all candidate windows; algorithmic markers are proposals.
- Choose a musically coherent source range and record its offset.
- Map section lifts and major beats, not every beat.
- Preserve a climax basin: approach, readable payoff, release.
- Keep scene pacing readable while scene-internal accents may still hit beats.

### 5. Rebuild real product states

- Reuse actual source components, CSS, SVG, icons, fonts, copy, and state logic where permitted.
- Replace network state with deterministic, schema-faithful local fixtures.
- Keep the final composition independent of runtime network calls.
- Record each native surface dimension and scale it uniformly.
- Derive click centers after final layout from `getBoundingClientRect()`.
- Demonstrate actual state changes; do not scale a screenshot and call it interaction.

### 6. Choreograph focus and continuity

- Sequence attention: focus, pointer approach, click, feedback, result.
- When a scene arrives at its intended framing, use one continuous camera move—not three or four corrective recenters.
- Treat the complete meaningful group as the visual center: for chat, center question plus answer; for a plugin, center the plugin unless a specific control is the declared subject.
- Zoom decisively where the audience must read. Do not protect empty space at the cost of legibility.
- Keep readable holds alive with subordinate motion; do not pin the frame dead.
- Blur/dim irrelevant material when it cannot be read in time.
- Prefer shared-element, FLIP, shape inheritance, mask, focus-pull, and scroll-continuity transitions.
- Derive every state from deterministic time. Expose `window.__AE_VIDEO__.render(t)`.

### 7. Review on localhost

- Serve the exact composition with play/pause, scrubber, seconds, frame index, ±1-frame stepping, time readout, and scene markers.
- Hide all review controls in capture mode.
- Inspect checkpoints around every click, zoom, line transition, shared element, climax, and ending.
- Play the whole film with audio at normal speed.
- Verify real hit targets, native ratios, intended line breaks, reading time, visual center, continuous motion, source truth, and music sync.
- Show the exact preview to the user and wait for explicit approval.
- Report what changed since the last accepted preview and direct the user to the exact time ranges that need review.

Read [references/qa-gates.md](references/qa-gates.md) completely and pass every blocking gate.

### 8. Render only the approved version

- Treat preview approval and export permission as two separate decisions.
- After preview approval, explain in plain language that export converts the localhost animation into a shareable video file. Ask whether the user wants to export now.
- Before exporting, offer clear quality choices with consequences for clarity, smoothness, render load, time, storage, and compatibility. Recommend one option for the user's device and platform.
- Confirm resolution, frame rate, format/codecs, audio, platform, and filename. Do not export until the user explicitly confirms the export specification.
- Set `approval.status`, `approval.approvedVersion`, `approval.exportRequested`, and `approval.exportSpecConfirmed` only after their corresponding explicit decisions.
- Run `scripts/validate_brief.py brief.json --final` and `scripts/validate_timeline.py production.json --final --strict`.
- Render to a new frame directory and filename. Never mix old and new frames.
- Prefer the stable compositor handshake in `scripts/render_web_video.mjs`; stop on an unstable frame instead of exporting corruption.
- Treat 2560×1440 at 60fps as a strong default when 4K60 exceeds available hardware, but never change target specs without user approval.
- Encode H.264/AAC `yuv420p` with `faststart`, then run `ffprobe`, a full decode, continuity checks, and visual contact-sheet review.

## Block these failures

- incomplete brief without explicit permission to assume;
- virtual click, wrong-center zoom, or unsupported feature;
- repeated micro-recentering inside one action;
- stretched/cropped product surface or arbitrary internal type resizing;
- important text too small, too brief, obscured, or accidentally wrapped;
- meaningless small copy inserted to fill space;
- scene frozen dead or fast without completing a meaningful action;
- unrelated subjects repeatedly swapping into the center;
- large text and its destination field disagreeing during a morph;
- transition with no inherited geometry, motion, color, focus, or meaning;
- musical climax assigned to the wrong value;
- reference video sampled too sparsely to understand its motion;
- final page invented from generic feature cards instead of source-backed product evidence;
- final render started before approval or exported with torn/partial frames.
- export started without a separate plain-language quality choice and explicit export confirmation.

## Route bundled resources

- `references/intake-and-clarification.md`: required for brief completeness and follow-up behavior.
- `references/guided-production.md`: required for strong onboarding, Goal-mode handoff, and progress communication.
- `references/decision-options.md`: required for recommended choices, alternatives, and beginner-friendly tradeoffs.
- `references/reference-video-analysis.md`: required for reference-video analysis or style recreation.
- `references/source-reconstruction.md`: required for website, extension, app, or repository fidelity.
- `references/creative-direction.md`: required for scene, motion, transition, type, zoom, pacing, and music decisions.
- `references/commercial-quality.md`: required before commercial-ready claims or launch-summary design.
- `references/project-contract.md`: required when creating `brief.json` or `production.json`.
- `references/qa-gates.md`: required before preview approval and final delivery.
- `assets/web-motion-starter/`: copy as a framework-free starting point only when the product stack lacks a better composition shell.
- Patch copies of scripts inside the product project when environment-specific changes are necessary; keep the packaged originals reusable.
