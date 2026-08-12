# Guided production and Goal-mode handoff

## Contents

1. Mandatory kickoff
2. Goal-mode recommendation
3. Paste-ready Goal template
4. Progress-report protocol
5. Review guidance
6. Plain-language rule
7. Export confirmation

## 1. Mandatory kickoff

Before implementation, actively guide the user through the production standard. The user should never need to guess what the skill can accept.

Present:

- the source package or URL needed for truthful UI reconstruction;
- the exact product/version evidence needed;
- the ordered selling points and must-show flow needed;
- music and reference-video options, including dense motion analysis;
- brand assets, fonts, logo, copy, and end-card URL;
- duration, platform, ratio, resolution, frame rate, and language;
- privacy, licensing, forbidden methods, and approval expectations;
- what the skill will produce: brief, evidence ledger, music map, scene plan, localhost preview, QA report, and approved export.

For each missing category, immediately show a recommended route and alternatives. Do not make the user invent the vocabulary of filmmaking.

State why missing items matter. Prefer “Without the exact source version, UI and feature claims cannot be verified” over “Please provide more details.”

## 2. Goal-mode recommendation

Recommend Goal mode when the request includes multiple stages such as source audit, reference analysis, music editing, implementation, revisions, preview approval, and export.

- Explain that Goal mode preserves the concrete objective and completion criteria across a long production.
- Provide a ready-to-paste Goal prompt before implementation.
- Never call a Goal-creation tool without the user's explicit instruction to create, start, or use Goal.
- If the user declines Goal mode, continue normally while keeping `brief.json` and `production.json` as the task contract.

## 3. Paste-ready Goal template

Fill every known value and leave explicit brackets only for unresolved fields:

```text
目标：为【产品名】【准确版本】制作一支可商用的 AE 风格网页渲染产品宣传片。

输入：
- 产品源码/地址：【路径或 URL】
- 版本：【版本/commit】
- 核心卖点：【唯一主卖点】
- 次要卖点：【按优先级】
- 必须演示：【真实交互链】
- 音乐：【路径、许可、允许截取范围】
- 参考视频：【路径；参考维度】
- 品牌资产：【Logo/字体/图标/颜色/官网】
- 输出：【时长、比例、分辨率、FPS、语言、平台】

强制约束：
- 禁止 HyperFrames；禁止截图冒充真实 UI；禁止拉伸；禁止虚空点击；禁止意外换行；禁止无意义小字。
- 参考视频需密集抽帧并在关键转场加密分析。
- 主卖点必须落在音乐高潮；场景保持可读、连续且非钉死。
- 最终渲染前必须由用户验证并明确批准 localhost 预览。

阶段：需求门禁 → 源码/参考/音乐审计 → 故事板与时间线 → 真实 UI 重建 → 动画与卡点 → localhost 验收 → 稳定导出与 QA。

完成标准：需求完整；产品行为可追溯；重点可读；点击/缩放/中心正确；转场无缝；高潮正确；无闪帧；最终文件通过全解码与视觉抽检。
```

## 4. Progress-report protocol

Report progress at meaningful boundaries, not every minor edit. Each report should contain:

- **Done:** concrete artifacts or validations completed;
- **Now:** current stage and exact focus;
- **Risk/question:** only unresolved blockers or decisions;
- **Next review:** what the user will be able to inspect and where;
- **Contract impact:** whether timing, climax, output specs, or approval baseline changed.
- **What this means:** explain technical terms and why the current step matters to the user.

Send a progress report at least after:

1. brief completion;
2. source/reference/music audit;
3. scene plan and climax map;
4. first playable preview;
5. each material revision batch;
6. pre-render approval;
7. final export QA.

During long tool work, give concise updates often enough that the user is not left guessing whether work is active.

## 5. Review guidance

- Give the localhost URL and exact query parameters.
- Point to specific timestamps and state what changed.
- Tell the user what to judge: logic, readability, visual center, click target, zoom strength, transition inheritance, music sync, and ending hold.
- Ask for explicit approval only after all blocking gates pass.
- If feedback is ambiguous, ask which timestamp or scene it refers to rather than applying a global change.

## 6. Plain-language rule

Assume the user should not need production knowledge.

- Before every major action, explain what will happen, why it is needed, what it changes, and what the user will receive or review.
- Translate terms on first use: for example, “60fps means smoother motion but roughly doubles frame-rendering work compared with 30fps.”
- Do not say only “running QA”; say what is being checked, such as whether clicks hit buttons, text wraps, frames tear, and audio stays synchronized.
- Give a recommendation instead of presenting unexplained settings.
- When a decision is needed, provide two or three options, put the recommendation first, and explain the visible result or tradeoff.
- Distinguish required decisions from optional improvements.
- Warn before long, compute-heavy, storage-heavy, destructive, or externally visible actions.
- Keep explanations concise and actionable; beginner-friendly guidance must not become jargon flooding.

## 7. Export confirmation

Preview approval does not authorize export. Run a separate confirmation after the exact preview is approved.

Explain:

- export turns the browser animation into a normal shareable MP4/MOV file;
- rendering is compute-heavy and may take much longer than real-time;
- higher resolution increases image detail and load;
- higher FPS improves smoothness and increases frame count;
- codec choice affects compatibility, file size, and transparency;
- audio inclusion and loudness must be confirmed;
- export creates a new versioned file and does not alter the approved source.

Offer an understandable menu adapted to the project:

- **1080p30 draft:** quickest review copy; lowest load; not the premium final choice.
- **1080p60 social:** smooth and broadly compatible; moderate load.
- **2K60 recommended:** sharper UI text and smooth motion with substantially less load than 4K60.
- **4K30 detail:** high detail with less motion load than 4K60.
- **4K60 maximum:** highest detail and smoothness; heavy CPU/GPU, long render time, large frame cache, and higher compositor-instability risk on weak hardware.

Recommend the smallest quality that visibly satisfies the target screen and distribution channel. Do not assume these exact options fit every platform.

Ask in plain language:

```text
预览已经通过。现在要把网页动画导出成可发送的视频文件吗？
我建议【2K / 60fps / MP4 / H.264 + AAC】，因为 UI 字体清晰、动画顺滑，同时比 4K60 少约 56% 像素计算量。
预计影响：渲染负载【中/高】、临时帧空间【估计值】、兼容性【说明】。
如果确认，请回复“按推荐规格导出”；也可以告诉我要 1080p60、4K30 或 4K60。
```

Before launching the render, restate the selected specification and obtain explicit confirmation. Record:

- `approval.exportRequested: true`;
- `approval.exportSpecConfirmed: true`;
- `approval.exportSpec`: width, height, fps, format, codecs, audio, platform, and filename.

If the user has not chosen, stop before render. Never interpret “preview looks good” as “export it.”
