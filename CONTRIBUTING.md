# Contributing

Thanks for improving SkillShowcase.

## Before opening a pull request

1. Keep `SKILL.md` focused on routing and the core workflow; move detail into `references/`.
2. Do not add runtime dependencies unless the standard library cannot solve the problem cleanly.
3. Preserve Chinese, English, and bilingual rendering.
4. Never execute or embed remote repository code.
5. Add or update tests for renderer behavior.
6. Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/render_showcase.py examples/catalog.example.json \
  --output examples/skill-showcase.example.html --language both
```

For visual changes, check the generated page at desktop and 375 px widths, exercise project tabs and search, and confirm the browser console is clean.
