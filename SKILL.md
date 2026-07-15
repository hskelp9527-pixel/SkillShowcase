---
name: agent-skill-showcase
description: Turn one or more Agent Skill links, GitHub repositories, or local skill folders into a searchable HTML showcase that explains what every skill does, its inputs and outputs, and realistic usage examples. Use when users want to understand, present, compare, document, or share collections of SKILL.md-based capabilities. Supports Chinese, English, or bilingual output. Do not use for installing, executing, security-auditing, or ranking skills.
license: MIT
metadata:
  author: SkillShowcase Maintainers
  version: "0.1.0"
---

# SkillShowcase

## Inputs

- One or more GitHub repository URLs, direct `SKILL.md` URLs, or local paths.
- Output language: `zh-CN`, `en`, or `both`. Route automatically: Chinese conversation → `zh-CN`; English conversation → `en`; explicit bilingual request → `both`. An explicit language choice always wins. Do not ask when the conversation language is clear.
- Optional title/audience.

## Workflow

1. Confirm sources and language only when inaccessible or ambiguous.
2. Read READMEs, every discoverable `SKILL.md`, and only supporting files needed for understanding. Never execute remote scripts.
3. Build `catalog.json` using [the catalog contract](references/catalog-contract.md). Keep names and links exact. Group duplicates, translations, and runtime editions that preserve the same user job/output; record paths and platform differences as variants. Separate editions with different primary capabilities or outputs.
4. For each skill capture its purpose, capabilities, minimum/optional inputs, user-visible outputs, realistic requests, and usage requirements/limits.
5. Do not copy long passages or invent capabilities. Label unclear items `Needs verification` / `待核验`.
6. Render the page:

```bash
python3 scripts/render_showcase.py catalog.json --output skill-showcase.html --language both
```

7. Test the renderer and source mapping. When browser tools exist, verify tabs, search, language switching, narrow layout, and console.

## Output Contract

- `catalog.json`: reusable source data.
- `skill-showcase.html`: self-contained responsive page with project tabs, search, source links, capabilities, inputs, outputs, and examples.
- For `both`, the single HTML contains a Chinese/English switch. For one-language output, it contains only that language.

Follow [research and writing rules](references/research-and-writing.md), [HTML quality rules](references/html-quality.md), and [trigger cases](evals/trigger_cases.json). The full Chinese edition is in [docs/SKILL.zh-CN.md](docs/SKILL.zh-CN.md).

## Boundaries

- Do not install or execute the inspected skills.
- Do not claim security, quality, popularity, compatibility, or production readiness unless the source proves it.
- Do not turn one repository into one card when it contains multiple distinct skills; enumerate each logical skill while deduplicating mirrors and translations.
- Do not expose local absolute paths, credentials, tokens, or unrelated repository content in the HTML.
