<p align="center">
  <img src="docs/assets/hero.png" alt="SkillShowcase：把 Skill 源文件变成清晰的浏览器展示页" width="100%">
</p>

<p align="center">
  <strong>把 Agent Skill 链接变成清晰、可搜索的能力展示页。</strong><br>
  让每个 Skill 一眼看懂。
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-155eef" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Python-%E4%BB%85%E6%A0%87%E5%87%86%E5%BA%93-18202a" alt="仅使用 Python 标准库">
  <img src="https://img.shields.io/badge/%E8%BE%93%E5%87%BA-%E9%9D%99%E6%80%81%20HTML-65707d" alt="输出静态 HTML">
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="https://hskelp9527-pixel.github.io/SkillShowcase/">在线展示</a> ·
  <a href="examples/popular-skills.bilingual.html">真实仓库双语示例</a> ·
  <a href="examples/skill-showcase.example.html">最小示例</a>
</p>

## Skill 是写给 Agent 的，但人也需要看懂

一个仓库可能只有一个 Skill，也可能有上百个。README 通常介绍项目，而用户真正关心的信息散落在各个 `SKILL.md` 里：它能做什么、要提供什么、最终产出什么、有哪些限制，以及应该怎样发出请求。

**SkillShowcase 把这些来源整理成一个可分享的 HTML 页面。** 用户只需提供一个或多个 Skill 链接，Agent 就能生成面向人的能力展厅：说明有依据、案例能直接使用、每项都能回到原始来源。

<p align="center">
  <a href="https://hskelp9527-pixel.github.io/SkillShowcase/">
    <img src="docs/assets/product-demo.png" alt="SkillShowcase 生成页面，包含项目标签、搜索和能力卡片" width="92%">
  </a>
</p>

## 最终会得到什么

| 从来源中读取 | 在展示页中呈现 |
|---|---|
| 仓库和 `SKILL.md` 地址 | 每个仓库或 Skill 集合一个项目 Tab |
| Skill 指令和声明的行为 | 普通用户能看懂的用途与能力说明 |
| 所需上下文和限制条件 | 最少输入、补充输入、预期输出和使用限制 |
| 原始案例和有来源的归纳 | 可以直接照着问的真实请求案例 |
| 翻译版或运行时镜像 | 合并为一个逻辑能力并列出版本，不重复刷屏 |

最终文件是响应式、自包含的静态 HTML，带搜索和来源链接，不需要前端框架、数据库或后端服务。

## 一句话开始

安装 Skill 后，直接用自然语言发送链接：

```text
使用 $agent-skill-showcase 分析下面这些仓库，生成一个中英双语 HTML 总览。
逐个说明每个 Skill 的用途、输入、输出、限制，并给两个真实使用案例。

https://github.com/owner/repo-one
https://github.com/owner/repo-two
```

SkillShowcase 默认跟随用户交流语言：

| 用户怎样提问 | 生成什么页面 |
|---|---|
| 中文交流 | 仅中文（`zh-CN`） |
| 英文交流 | 仅英文（`en`） |
| 明确要求双语 | 一个文件内提供中文 / English 切换（`both`） |

## 从链接到展示页

1. **发现**：读取仓库说明和所有可发现的 `SKILL.md`。
2. **解释**：去掉技术噪声，说明能力、输入、输出、限制和使用案例。
3. **整理**：生成有来源依据的目录；合并翻译版和运行时镜像，但不隐藏真正不同的 Skill。
4. **生成与验证**：渲染静态页面，核对来源覆盖；浏览器工具可用时检查 Tab、搜索、语言、移动端和控制台。

SkillShowcase 不执行远程脚本，仓库内容始终按不可信资料处理。

## 真实仓库验证

仓库内的展示页来自公开 Skill 项目，不是手写几张演示卡片：

| 来源 | 检查的源文件 | 展示的逻辑能力 |
|---|---:|---:|
| [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) | 9 | 9 |
| [Planning with Files](https://github.com/OthmanAdi/planning-with-files) | 17 | 1，多个版本合并展示 |
| [GPT Image 2 Skill](https://github.com/wuyoscar/GPT-Image2-Skill) | 1 | 1 |
| **合计** | **27** | **11** |

可以直接打开[在线展示](https://hskelp9527-pixel.github.io/SkillShowcase/)，或阅读[真实仓库测试报告](reports/real-world-test-2026-07-15.md)。

## 安装

克隆或下载仓库，然后复制或链接到 Agent Skill 目录：

```bash
git clone https://github.com/hskelp9527-pixel/SkillShowcase.git
mkdir -p ~/.agents/skills
cp -R SkillShowcase ~/.agents/skills/agent-skill-showcase
```

- **Codex：** `~/.codex/skills/agent-skill-showcase`
- **Claude Code：** `~/.claude/skills/agent-skill-showcase`
- **其他兼容环境：** 使用其配置的 Agent Skills 目录

标准入口是 [`SKILL.md`](SKILL.md)，完整中文维护版位于 [`docs/SKILL.zh-CN.md`](docs/SKILL.zh-CN.md)。

## 直接渲染已有目录

确定性渲染器仅使用 Python 标准库：

```bash
python3 scripts/render_showcase.py examples/catalog.example.json \
  --output examples/skill-showcase.example.html \
  --language both
```

目录数据格式见 [`references/catalog-contract.md`](references/catalog-contract.md)。

## 能力边界

SkillShowcase **不会**安装、执行、排名、背书或安全审计读取到的 Skill。展示页解释的是来源声明的能力，不代表第三方 Skill 已经安全或可用于生产。完整信任边界见 [SECURITY.md](SECURITY.md)。

## 项目结构

```text
SkillShowcase/
├── SKILL.md                       # 标准 Agent Skill 入口
├── docs/SKILL.zh-CN.md            # 完整中文维护版
├── scripts/render_showcase.py     # 确定性 HTML 渲染器
├── references/                    # 调研、数据和页面规范
├── examples/                      # 示例目录与生成页面
├── tests/                         # 渲染器测试
└── agents/interface.yaml          # 运行环境元数据
```

## 质量检查

```bash
python3 -m unittest discover -s tests -v
```

当前版本已经通过渲染器测试、Skill 规范校验、触发评估、资源边界检查，以及桌面端和移动端浏览器验收。详细证据见[真实仓库测试报告](reports/real-world-test-2026-07-15.md)。

## 参与贡献

欢迎提交 Issue 和 Pull Request。请保持核心承诺简单：来源覆盖完整、说明让人看懂、案例能够使用、页面值得分享。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

如果 SkillShowcase 让一个 Skill 仓库变得更容易理解，欢迎点 Star，或把生成页面分享给对应项目的维护者。

## 许可证

[MIT](LICENSE)
