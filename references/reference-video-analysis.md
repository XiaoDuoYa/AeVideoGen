# Reference video analysis and recreation

## Contents

1. Purpose and limits
2. Extraction density
3. Analysis passes
4. Motion-language ledger
5. Recreation method
6. Validation

## 1. Purpose and limits

Use a reference video to learn:

- narrative rhythm and scene duration;
- camera targets, travel, zoom scale, and easing character;
- subject continuity and visual-center discipline;
- typography scale, planned line breaks, masks, and entrances;
- shared elements, shapes, focus pulls, blur, depth, and transitions;
- interaction staging and response latency;
- relationship between sound, accents, climax, hold, and release.

Do not copy third-party logos, photographs, UI, source, proprietary copy, or other protected product identity. Recreate the motion grammar with the user's real product and permitted assets.

## 2. Extraction density

Never analyze animation style from thumbnails spaced multiple seconds apart.

- For reference clips up to 90 seconds, use at least 4 overview frames per second by default.
- For longer clips, keep overview sampling at 2fps or higher unless the user explicitly accepts less detail.
- Extract 8–12fps around cuts, morphs, clicks, zoom arrivals, text entrances, masks, and other key transitions.
- For a suspicious 0.25–0.75 second transition, inspect every frame when practical.
- Keep original frame timestamps and do not infer duration from contact-sheet position.
- Watch the full video at normal speed with audio after frame analysis.

Run:

```bash
python3 scripts/analyze_reference_video.py reference.mp4 --output-dir reference-analysis
```

Use `--overview-fps`, `--dense-fps`, `--dense-radius`, and `--scene-threshold` when the default extraction needs adjustment.

## 3. Analysis passes

Perform separate passes:

1. **Story pass:** identify context, friction, action, result, value, and signature.
2. **Shot pass:** mark scene boundaries, dominant subject, and visual center.
3. **Motion pass:** inspect trajectories, easing, overlap, settling, and continuous motion.
4. **Typography pass:** record size class, exact line count, entrance, hold, exit, and readability.
5. **Transition pass:** identify shared geometry, mask, inherited velocity, focus, color, or meaning.
6. **Audio pass:** mark accents, section lifts, climax, silence, and release.
7. **Product-truth pass:** separate transferable style from reference-specific assets and claims.

## 4. Motion-language ledger

For every important shot or transition, record:

| Field | What to capture |
|---|---|
| Time range | Exact start, readable hold, and end |
| Subject | One dominant object or group |
| Center | Start and end normalized coordinates |
| Camera | Scale, travel, transform origin, and arrival |
| Easing | Quick intent, soft settle, spring, linear, or custom |
| Shared element | Text, card, button, icon, mask, or none |
| Typography | Level, line policy, size, tracking, and contrast |
| Background | Blur, parallax, dimming, texture, or motion |
| Interaction | Pointer path, target, pressed state, and latency |
| Audio cue | Beat, lift, climax, lyric, or release |
| Transfer | How to express this with the user's real product |

## 5. Recreation method

- Match structure and perceptual effect before copying exact numbers.
- Rebuild the user's source-backed UI first; apply the reference motion language second.
- Preserve scene logic even when exact reference assets are unavailable.
- Use a shared-element transition only when both user-product states contain a truthful counterpart.
- When the user requests a close recreation, state what can match: timing, layout logic, camera, easing, transitions, typography behavior, and sound synchronization.
- Record intentional deviations caused by aspect ratio, product geometry, copy length, or missing rights.

## 6. Validation

- Compare corresponding timestamps side by side.
- Check transition start, midpoint, and arrival—not just endpoint stills.
- Compare perceived subject size and visual center.
- Ensure the recreated product remains truthful and readable.
- Ask the user whether fidelity should favor exact motion, product legibility, or brand adaptation when those goals conflict.
- Never claim a percentage match without defining the compared dimensions and reviewing the preview.
