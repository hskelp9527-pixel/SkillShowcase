# Real-world release test — 2026-07-15

## Scope

SkillShowcase was tested against three public GitHub repositories selected for visible adoption and manageable logical skill count.

| Repository | Stars at test time | SKILL.md files inspected | Logical skills shown |
|---|---:|---:|---:|
| vercel-labs/agent-skills | 29,074 | 9 | 9 |
| OthmanAdi/planning-with-files | 25,367 | 17 | 1 |
| wuyoscar/GPT-Image2-Skill | 3,740 | 1 | 1 |
| **Total** | — | **27** | **11** |

## Language routing verified

- Chinese request → Chinese-only display, no language switch.
- English request → English-only display, no language switch.
- Explicit bilingual request → one page with Chinese and English switch.

Generated artifacts:

- `examples/popular-skills.zh-CN.html`
- `examples/popular-skills.en.html`
- `examples/popular-skills.bilingual.html`
- `examples/popular-skills.catalog.json`

## Issue found and fixed

Planning with Files contains canonical copies, runtime-specific mirrors, and five translations. Counting every `SKILL.md` as a separate capability would incorrectly show 17 skills. SkillShowcase now groups exact runtime mirrors and translation-only editions into one logical skill, lists their editions under `variants`, and preserves distinct skills separately.

## Checks

- All 27 source files accounted for.
- 11 logical entries rendered.
- Three project tabs work.
- Chinese and English single-language routing works.
- Bilingual language switching works.
- Search works across names, capabilities, inputs, outputs, examples, and variants.
- Planning with Files renders as one logical skill with runtime and translation variants.
- 375 px viewport has no document-level horizontal overflow.
- Browser console has zero errors and zero warnings.
- Generated HTML contains no absolute local paths.
- Renderer unit suite passes.

## Release decision

**Recommend push.** The test found one meaningful cataloging problem, it was corrected, and the final package now handles single-skill repositories, multi-skill repositories, runtime mirrors, translations, Chinese-only output, English-only output, and explicit bilingual output.

The target repository `hskelp9527-pixel/SkillShowcase` is public and empty at the time of this test. No push was performed during the test phase.
