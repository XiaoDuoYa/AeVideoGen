# Brief and production contracts

## Contents

1. Brief contract
2. Brief completion rules
3. Timeline manifest
4. Scene and interaction rules
5. Approval and render rules

## 1. Brief contract

Create `brief.json` before creative implementation:

```json
{
  "skillVersion": "1.0.1",
  "product": {
    "name": "EchoLand",
    "type": "browser-extension",
    "sourcePath": "/absolute/source/path",
    "sourceVersion": "v1.0.3"
  },
  "audience": { "primary": "knowledge workers", "platform": "social-video" },
  "story": {
    "primaryPromise": "看过的，不再丢失",
    "featurePriority": ["记住网页", "问 AI", "自动归纳合集"],
    "mustShow": ["真实保存流程", "围绕记忆提问", "合集一级与详情"]
  },
  "brand": {
    "assetsPath": "assets/brand",
    "language": "zh-CN",
    "endCard": "ECHOLAND.HEYXIAODUO.XYZ"
  },
  "music": {
    "path": "assets/music.mp3",
    "rightsConfirmed": true,
    "allowedRange": "full",
    "climaxIntent": "primary-promise"
  },
  "output": {
    "durationSeconds": 54.4,
    "aspectRatio": "16:9",
    "width": 2560,
    "height": 1440,
    "fps": 60,
    "format": "mp4"
  },
  "references": [
    { "path": "reference.mp4", "role": ["motion", "transitions"], "recreationLevel": "close" }
  ],
  "constraints": {
    "forbidden": ["HyperFrames", "stretched UI", "unapproved final render"],
    "privacy": "synthetic fixtures only",
    "approvalRequired": true
  },
  "assumptions": [],
  "status": "complete"
}
```

## 2. Brief completion rules

- Use `null`, an empty string, or an empty required array for an unknown field; never hide uncertainty behind vague copy.
- Set `status` to `complete` only after all applicable blocking fields are known.
- Add explicit best-judgment permissions to `assumptions` with field, value, reason, confidence, and impact.
- Use `not-applicable` only with a recorded reason.
- Re-run `scripts/validate_brief.py` after new user requirements.

## 3. Timeline manifest

Create `production.json` after the brief passes:

```json
{
  "project": {
    "title": "Product film",
    "sourceVersion": "v1.0.3",
    "duration": 54.4,
    "fps": 60,
    "width": 1280,
    "height": 720
  },
  "render": {
    "pixelScale": 2,
    "outputWidth": 2560,
    "outputHeight": 1440,
    "codec": "h264",
    "audioCodec": "aac"
  },
  "constraints": {
    "noHyperFrames": true,
    "approvalRequiredBeforeFinalRender": true,
    "maxStaticSeconds": 0.65,
    "minSubjectHoldSeconds": 1.2,
    "forbidAccidentalWrap": true,
    "minImportantFontPxAtOutput": 36
  },
  "audio": {
    "path": "assets/music-cut.mp3",
    "sourceOffset": 68.5,
    "climaxAt": 37.1
  },
  "scenes": [
    {
      "id": "remember-value",
      "start": 35.8,
      "end": 39.8,
      "kind": "text",
      "purpose": "State the primary promise",
      "subject": "忘记，也能找回",
      "visualGroup": "#memoryQuestionAndAnswer",
      "priority": "primary",
      "text": "忘记，也能找回",
      "linePolicy": { "mode": "single-line", "maxLines": 1 },
      "focus": { "x": 0.5, "y": 0.5, "scale": 1.25 },
      "motion": { "continuous": true, "cameraMoves": 1 },
      "readabilitySeconds": 2.4,
      "evidence": "src/components/memory/..."
    }
  ],
  "interactions": [
    {
      "time": 24.2,
      "action": "click",
      "target": "#ask-memory",
      "coordinateSource": "dom-rect",
      "x": 0.51,
      "y": 0.82,
      "focusScene": "ask-memory"
    }
  ],
  "approval": {
    "status": "pending",
    "approvedVersion": null,
    "exportRequested": false,
    "exportSpecConfirmed": false,
    "exportSpec": null
  }
}
```

Logical `width` and `height` multiplied by `render.pixelScale` must equal the output dimensions.

## 4. Scene and interaction rules

- Cover the full duration; overlaps are allowed, gaps are not.
- Keep scene IDs stable after review.
- Mark exactly one primary value scene and place the climax inside it.
- Record the complete meaningful `visualGroup`, not merely the clicked button.
- Set `motion.cameraMoves` to the number of intentional focus destinations; more than one needs a recorded reason.
- Define every important title as `single-line` or `exact-lines`. Store explicit text lines when using `exact-lines`.
- Set `readabilitySeconds` to unobstructed reading time, excluding entry and exit.
- Derive click coordinates from final DOM geometry and use `coordinateSource: dom-rect`.
- Record `evidence`, native dimensions, transition inheritance, music markers, and intentional deviations where applicable.

## 5. Approval and render rules

- Keep approval `pending` until the user approves the exact browser preview.
- Record the preview version in `approvedVersion`.
- Ask separately whether the user wants an export and explain quality/load tradeoffs in plain language.
- Set `exportRequested` only after the user asks to export.
- Set `exportSpecConfirmed` only after the user confirms resolution, FPS, format/codecs, audio, platform, and filename.
- Never infer export permission from preview approval.
- Any change affecting visible frames invalidates prior approval unless the user explicitly approves the change without re-preview.
- Keep output target and logical composition separate; do not accidentally export 2× the requested dimensions.
- Render to fresh frames and output paths.
