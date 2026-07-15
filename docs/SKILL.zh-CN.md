# SkillShowcase 中文版执行说明

> 标准入口是仓库根目录的 `SKILL.md`。本文件是等价的中文维护版，便于中文用户审阅和修改。

## 什么时候使用

当用户提供一个或多个 Agent Skill 链接、GitHub 仓库或本地 Skill 目录，希望了解、展示、比较、整理或分享其中的能力时使用。

不要用于安装 Skill、执行 Skill、安全审计、质量评分或排行榜。

## 输入

- 一个或多个 GitHub 仓库链接、直接 `SKILL.md` 链接或本地目录。
- 输出语言：`zh-CN`、`en` 或 `both`。自动路由规则：中文交流默认 `zh-CN`，英文交流默认 `en`，明确要求双语时才用 `both`；用户明确指定语言时以指定值为准。交流语言已经清楚时不要再提问。
- 可选：页面标题和目标读者。缺失时不要阻塞执行。

## 执行流程

1. 确认来源和语言。只有来源无法访问或语言确实不明确时才提问。
2. 只读取来源资料。远程仓库优先查看 README、所有可发现的 `SKILL.md`；仅在理解能力确有需要时查看 examples 或 references。绝不执行远程脚本。
3. 按 `references/catalog-contract.md` 生成 `catalog.json`，保留准确的 Skill 名称和来源链接。重复文件、翻译版以及保持相同用户任务和输出的运行时适配版合并为一个逻辑 Skill，并把路径和平台差异列为版本；主要能力或输出不同的版本必须分开。
4. 每个 Skill 都用非技术语言说明：
   - 它解决什么问题；
   - 主要能力；
   - 最少输入与补充输入；
   - 用户最终能获得什么；
   - 至少一个真实可用的请求案例；
   - 影响使用的前置条件与限制。
5. 不大段复制原文，不编造能力。无法确认时明确标记“待核验”。
6. 生成 HTML：

```bash
python3 scripts/render_showcase.py catalog.json --output skill-showcase.html --language both
```

7. 运行测试，并检查每个条目都有真实对应的来源。浏览器可用时，实际验证项目 Tab、搜索、语言切换、窄屏布局和控制台。

## 输出

- `catalog.json`：可复用的结构化资料。
- `skill-showcase.html`：一个自包含、可搜索、响应式的展示页。每个项目一个 Tab，每个 Skill 包含用途、能力、输入、输出、案例和来源。
- `both` 模式在同一个 HTML 中提供中英文切换；单语言模式只包含所选语言。

详细规则见：

- `references/catalog-contract.md`
- `references/research-and-writing.md`
- `references/html-quality.md`

## 边界

- 不安装、不执行被调研的 Skill。
- 来源没有证明的安全性、质量、流行度、兼容性或生产可用性，不得自行宣称。
- 一个仓库含多个不同 Skill 时必须逐个列出；相同运行时镜像和纯翻译版应去重，不能虚增能力数量。
- HTML 中不得泄露本地绝对路径、凭证、Token 或无关仓库内容。
