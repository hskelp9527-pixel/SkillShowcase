# Catalog Contract

The renderer accepts UTF-8 JSON with this shape:

```json
{
  "title": {"zh-CN": "Agent Skills 能力总览", "en": "Agent Skills Showcase"},
  "subtitle": {"zh-CN": "面向使用者的能力说明与案例", "en": "User-focused capabilities and examples"},
  "generated_at": "2026-07-15",
  "projects": [
    {
      "id": "stable-project-id",
      "name": "Project Name",
      "url": "https://github.com/owner/repo",
      "summary": {"zh-CN": "项目说明", "en": "Project summary"},
      "note": {"zh-CN": "来源文件与去重说明", "en": "Source-file and deduplication note"},
      "skills": [
        {
          "name": "skill-name",
          "source_url": "https://github.com/owner/repo/blob/main/skills/name/SKILL.md",
          "source_path": "skills/name/SKILL.md",
          "title": {"zh-CN": "中文标题", "en": "English title"},
          "purpose": {"zh-CN": "解决的问题", "en": "The problem it solves"},
          "capabilities": {"zh-CN": ["能力一"], "en": ["Capability one"]},
          "minimum_inputs": {"zh-CN": ["最少输入"], "en": ["Minimum input"]},
          "optional_inputs": {"zh-CN": ["补充输入"], "en": ["Optional input"]},
          "outputs": {"zh-CN": ["用户可见成果"], "en": ["User-visible result"]},
          "examples": {"zh-CN": ["示例请求"], "en": ["Example request"]},
          "requirements": {"zh-CN": ["前置条件或限制"], "en": ["Requirement or limitation"]}
          ,"variants": {"zh-CN": ["其他运行时镜像或语言版"], "en": ["Runtime mirrors or language editions"]}
        }
      ]
    }
  ]
}
```

## Required fields

- Root: `title`, `projects`.
- Project: `id`, `name`, `url`, `summary`, `skills`.
- Skill: `name`, `source_url`, `purpose`, `capabilities`, `minimum_inputs`, `outputs`, `examples`.

Localized values use `zh-CN` and `en`. In a single-language run, only the selected language is required. Do not place Markdown or HTML in text fields.

## Source rules

- `source_url` must point to the inspected Skill file or the closest stable source page.
- `source_path` is repository-relative. Never store an absolute local path.
- Project IDs must be unique and stable within the catalog.
- Skill names must match frontmatter or the source's canonical name.
- Duplicates, translations, and runtime-specific editions should share one logical entry when they preserve the same user job and output. Record paths and platform differences in `variants`. Keep an edition separate when its primary capability or output changes.
