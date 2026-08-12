# AeVideoGen Skill

用于制作商业级 AE 风格产品发布片、功能介绍、UI 交互演示、插件宣传片和音乐卡点视频。AeVideoGen 强调真实产品源码、因果叙事、参考视频运动语言、确定性网页渲染、浏览器预览验收和稳定 MP4 导出。

AeVideoGen Skill creates commercial-grade AE-style product launches, feature explainers, UI interaction demos, feature promos, and music-synced product films.

## 安装方式一：手动安装

### Codex

```bash
git clone https://github.com/XiaoDuoYa/AeVideoGen.git
mkdir -p ~/.codex/skills/ae-video-gen-by-hxdlabs
cp -R AeVideoGen/SKILL.md AeVideoGen/references AeVideoGen/scripts AeVideoGen/assets AeVideoGen/agents ~/.codex/skills/ae-video-gen-by-hxdlabs/
```

### Claude Code / Claude Agent

```bash
git clone https://github.com/XiaoDuoYa/AeVideoGen.git
mkdir -p ~/.claude/skills/ae-video-gen-by-hxdlabs
cp -R AeVideoGen/SKILL.md AeVideoGen/references AeVideoGen/scripts AeVideoGen/assets AeVideoGen/agents ~/.claude/skills/ae-video-gen-by-hxdlabs/
```

项目级 Agent 也可以把仓库复制到 `.agents/skills/ae-video-gen-by-hxdlabs/`，并确保 `SKILL.md` 位于目录根部。

## 安装方式二：复制一句话给 Agent 自动安装

不会手动安装时，直接把下面整段 Prompt 复制给 Codex、Claude Code 或其他能执行本地命令的 Agent：

```text
请帮我自动安装 AeVideoGen Skill：
1. 从 https://github.com/XiaoDuoYa/AeVideoGen.git 克隆最新版本；
2. 判断当前环境是 Codex 还是 Claude Code；Codex 安装到 ~/.codex/skills/ae-video-gen-by-hxdlabs/，Claude Code 安装到 ~/.claude/skills/ae-video-gen-by-hxdlabs/；如果是项目级 Agent，则安装到当前项目的 .agents/skills/ae-video-gen-by-hxdlabs/；
3. 复制 SKILL.md、references、scripts、assets、agents，确保 SKILL.md 位于安装目录根部；
4. 检查安装目录和 SKILL.md 是否存在，并告诉我实际安装路径；
5. 安装完成后不要开始制作视频，先回复“已安装 AeVideoGen Skill”，并给出下一步调用示例。
```

安装完成后可以直接说：

```text
使用 AeVideoGen Skill，为我的产品制作一支 30 秒商业宣传片。请先执行完整性检查，列出缺失信息和推荐选项，不要直接开始渲染。
```

## 推荐创作 Prompt

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

## 使用技巧

- 一个场景只服务一个视觉重点；不要用功能卡片堆砌替代真实产品行为。
- 主卖点应该落在音乐高潮，不要把高潮留给次要功能。
- 参考视频只用于学习节奏、镜头和动效语法；界面、图标和文案必须来自真实产品。
- 保持 UI 原始比例，统一缩放，避免拉伸；重要文字要有足够阅读时间。
- 先做浏览器预览，再导出；预览批准和导出批准是两个独立决定。
- 需求不完整时，让 Agent 给出 2–3 个具体选项，不要凭空发明产品功能。

## 标准工作流

1. 检查 brief、源码、参考视频、音乐和品牌素材。
2. 运行 `python3 scripts/validate_brief.py brief.json`。
3. 分析参考视频并建立因果叙事：用户场景 → 痛点 → 产品动作 → 可见结果 → 记忆点。
4. 使用真实 UI 和确定性 fixture，运行 `python3 scripts/validate_timeline.py production.json --strict`。
5. 在 localhost 播放完整预览，检查点击、缩放、文字、转场和音乐高潮。
6. 获得精确预览的明确批准后，再确认导出规格并渲染 MP4。

## 目录

- `SKILL.md` — 技能规则与生产流程
- `references/` — 需求澄清、参考分析、创意方向、源码重构和 QA 指南
- `scripts/` — brief/timeline 校验、音乐与视频分析、网页渲染和预览审计脚本
- `assets/web-motion-starter/` — 网页动效起始模板
- `agents/openai.yaml` — Agent 元数据

## License

本项目采用 [MIT License](LICENSE)。
