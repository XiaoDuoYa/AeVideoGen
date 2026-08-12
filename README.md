# AeVideoGen Skill

用于制作商业级 AE 风格产品发布片、功能介绍、UI 交互演示、插件宣传片和音乐卡点视频。它强调真实产品源码、因果叙事、参考视频运动语言、确定性网页渲染、浏览器预览验收和稳定 MP4 导出。

AeVideoGen Skill creates commercial-grade AE-style product launches, feature explainers, UI interaction demos, feature promos, and music-synced product films. It is built around source-backed product truth, causal storytelling, reference-motion analysis, deterministic web rendering, browser-preview approval, and stable final export.

## 快速安装 / Quick install

### Codex

```bash
git clone https://github.com/XiaoDuoYa/AeVideoGen.git
mkdir -p ~/.codex/skills/ae-video-gen-by-hxdlabs
cp -R AeVideoGen/SKILL.md AeVideoGen/references AeVideoGen/scripts AeVideoGen/assets AeVideoGen/agents ~/.codex/skills/ae-video-gen-by-hxdlabs/
```

安装后，在 Codex 中直接说：

> 使用 ae-video-gen-by-hxdlabs，为我的产品制作一支 30 秒宣传片。

### Claude Code / Claude Agent

```bash
git clone https://github.com/XiaoDuoYa/AeVideoGen.git
mkdir -p ~/.claude/skills/ae-video-gen-by-hxdlabs
cp -R AeVideoGen/SKILL.md AeVideoGen/references AeVideoGen/scripts AeVideoGen/assets AeVideoGen/agents ~/.claude/skills/ae-video-gen-by-hxdlabs/
```

然后在 Claude Code 中输入：

> Use the ae-video-gen-by-hxdlabs skill to create a commercial product video from this repository and the attached reference video.

项目级 Agent 也可以把整个仓库复制到 `.agents/skills/ae-video-gen-by-hxdlabs/`，并确保 `SKILL.md` 位于该目录根部。

## 推荐调用方式 / Recommended prompt

```text
使用 AeVideoGen Skill 制作一支 [时长] 秒的 [产品类型] 宣传片。
产品源码：[本地路径或仓库 URL]
核心卖点：[1 个主卖点 + 2 个辅助卖点]
目标观众：[受众]
品牌风格：[颜色、字体、情绪、参考视频]
输出平台：[官网 / 发布会 / 社交媒体]
素材：[logo、音乐、参考视频、产品截图或浏览器扩展]
请先执行完整性检查，列出缺失信息和推荐选项；不要直接开始渲染。
```

## 标准工作流 / Workflow

1. 先检查 brief、产品源码、参考视频、音乐和品牌素材；缺失信息先提问。
2. 创建并验证 `brief.json`：`python3 scripts/validate_brief.py brief.json`。
3. 分析参考视频的镜头、节奏、转场、文字和相机运动，不复制第三方资产。
4. 用“用户场景 → 痛点 → 产品动作 → 可见结果 → 记忆点”组织叙事。
5. 使用真实 UI、确定性 fixture 和真实交互状态；运行 `python3 scripts/validate_timeline.py production.json --strict`。
6. 在 localhost 播放完整预览，检查每个点击、缩放、文字停留、转场和音乐高潮。
7. 获得用户对精确浏览器预览的明确批准后，再确认导出规格并渲染 MP4。

## 使用技巧 / Practical tips

- 一个场景只服务一个视觉重点；不要用功能卡片堆砌替代真实产品行为。
- 主卖点应该落在音乐高潮，不要把高潮留给次要功能。
- 参考视频用于学习节奏、镜头和动效语法；界面、图标和文案必须来自真实产品。
- 保持 UI 原始比例，统一缩放，避免拉伸；重要文字要有足够阅读时间。
- 先做可审阅的浏览器预览，再导出；预览批准和导出批准是两个独立决定。
- 遇到素材、源码或需求不完整时，让 Agent 给出 2–3 个具体选项，不要凭空发明产品功能。

## 目录 / Contents

- `SKILL.md` — 完整技能规则与生产流程
- `references/` — 需求澄清、参考分析、创意方向、源码重构和 QA 指南
- `scripts/` — brief/timeline 校验、音乐与视频分析、网页渲染和预览审计脚本
- `assets/web-motion-starter/` — 网页动效起始模板
- `agents/openai.yaml` — Agent 元数据

## License

本仓库暂未指定许可证。公开分发前，请根据你的使用和授权需求补充合适的 LICENSE 文件。
