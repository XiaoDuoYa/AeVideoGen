# Intake and clarification gate

## Contents

1. Artifact-first discovery
2. Blocking brief fields
3. Question protocol
4. Assumption protocol
5. Contradictions and revisions
6. Completion criteria

## 1. Artifact-first discovery

Before asking anything:

- inspect supplied source, URLs, screenshots, videos, music, brand assets, and previous accepted versions;
- read file metadata and repository version evidence;
- recover requirements already stated in the conversation;
- distinguish facts from guesses;
- avoid asking the user to repeat discoverable information.

Record findings in `brief.json` with `evidence` or `assumptions`.

Then show a kickoff report. Do not wait for the user to ask what the skill needs.

- **Received:** enumerate useful files, facts, and confirmed decisions.
- **Still needed:** enumerate blocking gaps with their production impact.
- **Recommended uploads:** name the source archive/repository, logo pack, fonts, music, reference video, screenshots, or exact copy that would improve fidelity.
- **Next questions:** ask only the next one to three highest-impact items.
- **Goal recommendation:** for multi-stage work, provide the ready-to-paste Goal brief from `guided-production.md`.

## 2. Blocking brief fields

Do not begin creative implementation while any applicable item is unknown:

- product name, product type, and exact source/version;
- target audience and intended platform;
- primary promise and feature priority;
- must-show user journey and required product states;
- forbidden methods, assets, interactions, and claims;
- target duration or acceptable range;
- aspect ratio, resolution, frame rate, language, and delivery format;
- music source, rights status, permitted edit range, and climax intent;
- brand assets, typography, color constraints, and required end card/URL;
- reference material and whether it is for pace, layout, animation grammar, or close recreation;
- privacy/licensing restrictions;
- review and explicit approval requirement.

Fields may be marked `not-applicable` only when the reason is recorded.

## 3. Question protocol

- Ask one to three related questions at a time.
- Lead with the highest-impact unknown that could change story, truth, duration, or output.
- Give two or three mutually exclusive choices for each decision. Put the recommended option first and explain its effect.
- Include a simple reply path such as “回复 1，或回复‘按推荐方案’.”
- Avoid a bare open-ended question when useful defaults exist.
- Continue asking in later turns until every blocking field is complete.
- Do not mistake a partial answer for complete authorization.
- When an answer creates a new contradiction, ask about the contradiction before implementation.
- When the user says “you decide” only for one field, do not assume that permission covers all remaining fields.
- If the user supplied almost nothing, explain the standard input package and ask whether they can provide each applicable category; do not respond with a vague “tell me more.”
- If the user says “不知道,” recommend a safe default and ask for confirmation instead of repeating the same question.
- Keep product truth, licensing, credentials, privacy, and destructive/external actions explicit; never default these silently.

Useful order:

1. source/version and primary promise;
2. must-show interaction and feature priority;
3. music, climax, duration, and platform;
4. brand/end card/reference role;
5. output and approval.

## 4. Assumption protocol

Proceed with incomplete information only when the user explicitly authorizes best judgment, asks to skip questions, or requests an exploratory draft.

Then:

- put every inferred value in `assumptions`;
- label confidence and impact;
- keep product claims and features source-backed regardless of permission;
- keep the preview status `exploratory` and final approval `pending`;
- surface high-impact assumptions before review.

Never treat impatience, silence, insults, or a request for speed as permission to invent product truth.

## 5. Contradictions and revisions

- Prefer the latest explicit user instruction over an earlier preference.
- Preserve still-valid earlier requirements.
- Ask when two current requirements cannot coexist.
- Record changed fields and affected scenes in `brief.json`.
- Revalidate the timeline when duration, feature priority, music range, climax, or end card changes.

## 6. Completion criteria

The brief is ready only when:

- `scripts/validate_brief.py brief.json` returns zero errors;
- the primary promise is one unambiguous sentence;
- feature priority is ordered;
- every must-show interaction has a source/version path;
- output specifications and approval gate are explicit;
- remaining uncertainty is either non-blocking or explicitly authorized as an assumption.
