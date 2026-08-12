# Review and delivery gates

## Contents

1. Brief gate
2. Reference gate
3. Source gate
4. Story gate
5. Frame gate
6. Continuous-play gate
7. Approval gate
8. Render gate
9. Delivery report

## 1. Brief gate

Block implementation when:

- `brief.json` has unresolved blocking fields;
- the primary promise or feature priority is ambiguous;
- output specifications, source version, music intent, or approval rule is missing;
- assumptions were made without explicit permission.

## 2. Reference gate

When a reference video exists, verify:

- metadata and audio were inspected;
- overview extraction is dense enough to understand motion;
- key transitions have 8–12fps or frame-by-frame inspection;
- the full reference was watched at normal speed;
- transferable motion language is separated from third-party assets.

## 3. Source gate

Block review when:

- the requested version is not identified;
- a visible claim lacks source or user evidence;
- a screenshot substitutes for available source-backed UI;
- external data, credentials, or private content remain in the composition;
- a native surface dimension is unknown or stretched.

## 4. Story gate

Verify:

- the scene chain has clear cause and effect;
- each scene has one purpose and dominant subject;
- the main selling point is unmistakable;
- the musical climax lands inside the main selling-point scene;
- secondary features do not steal the climax;
- pure text appears only where it improves understanding or transition.

## 5. Frame gate

Capture checkpoints:

- 3–6 frames around every click;
- before, middle, and after every zoom;
- both ends and midpoint of every shared-element transition;
- the first fully readable frame of each text scene;
- climax approach, payoff, and release;
- final logo/value lockup.

At every checkpoint verify:

- pointer and visible control centers agree;
- camera focus matches the interaction;
- UI aspect ratio equals the recorded native ratio;
- type hierarchy is consistent;
- text is sharp and unobstructed;
- important text has the intended line count and no accidental wrapping;
- no meaningless small copy is being used as visual filler;
- the complete visual group, rather than an isolated button, is centered;
- no element jumps because transform origins change;
- irrelevant content is dimmed without destroying context;
- the next scene inherits a visual property from the previous one.

## 6. Continuous-play gate

Play the full preview with audio at normal speed.

Block approval when:

- a frame feels dead for longer than the intentional reading hold;
- the film rushes past readable content;
- the same center is occupied by unrelated subjects in rapid succession;
- pointer, camera, and result start at the same instant with no attention sequence;
- a transition feels like a cut disguised by opacity;
- one action uses several visible corrective recenters instead of one camera path;
- the climax arrives early or late relative to the value statement;
- the ending has no release or remembered phrase.

## 7. Approval gate

- Serve the actual composition locally.
- Include a floating review dock with play/pause, scrubber, seconds input, frame input, ±1-frame controls, and scene markers.
- Confirm the dock is hidden in capture mode and cannot leak into final frames.
- Let the user review the exact version intended for export.
- Do not equate silence, partial approval, or approval of an earlier version with final approval.
- Record explicit approval in `production.json`.
- Preserve the approved baseline before further experimentation.
- Treat export as a second gate: explain quality/load tradeoffs, ask whether to export, and confirm the exact specification.
- Block rendering when `exportRequested` or `exportSpecConfirmed` is not true.

## 8. Render gate

Before final render:

```bash
python3 scripts/validate_timeline.py production.json --final
```

Render into a new frame directory. Then verify:

```bash
ffprobe -v error -show_entries \
  format=duration,size,bit_rate:stream=codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels \
  -of json output.mp4

ffmpeg -v error -i output.mp4 -f null -
```

Check:

- expected duration within one frame;
- expected resolution and frame rate;
- H.264 video and AAC audio unless the user requested otherwise;
- stereo/sample rate as expected;
- `yuv420p` compatibility;
- no decode errors;
- no stale frames from previous versions;
- audio starts at the intended edit point.
- every source frame completed the compositor-stability check;
- no horizontal tearing, partial frame, stale tile, flash frame, or isolated corruption appears in continuity analysis;
- a contact sheet and the user-reported problem ranges were visually inspected.

## 9. Delivery report

Report:

- clickable absolute output path;
- duration, resolution, frame rate, video/audio codecs, and file size;
- source version represented;
- music source offset and climax alignment;
- validation status and any intentional deviations;
- backup or approved baseline location when relevant.
