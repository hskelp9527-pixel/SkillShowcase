#!/usr/bin/env python3
"""Render a self-contained SkillShowcase HTML file from catalog JSON."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any

LANGUAGES = {"zh-CN", "en", "both"}

UI = {
    "zh-CN": {
        "eyebrow": "AGENT SKILLS 能力目录",
        "repo": "查看项目",
        "source": "查看 Skill 来源",
        "search": "搜索名称、用途、能力、输入、输出或案例",
        "skills": "个 Skills",
        "showing": "当前显示",
        "purpose": "它能做什么",
        "capabilities": "主要能力",
        "inputs": "你需要提供",
        "minimum": "最少输入",
        "optional": "补充输入",
        "outputs": "你会得到",
        "examples": "可以这样问",
        "requirements": "使用条件与限制",
        "variants": "版本与镜像",
        "empty": "没有找到匹配的 Skill，请换一个关键词。",
        "language": "语言",
        "generated": "生成日期",
    },
    "en": {
        "eyebrow": "AGENT SKILLS CAPABILITY CATALOG",
        "repo": "View repository",
        "source": "View skill source",
        "search": "Search names, purposes, capabilities, inputs, outputs, or examples",
        "skills": " skills",
        "showing": "Showing",
        "purpose": "What it does",
        "capabilities": "Core capabilities",
        "inputs": "What you provide",
        "minimum": "Minimum input",
        "optional": "Optional input",
        "outputs": "What you get",
        "examples": "Try asking",
        "requirements": "Requirements and limits",
        "variants": "Variants and editions",
        "empty": "No matching skills. Try a different search.",
        "language": "Language",
        "generated": "Generated",
    },
}

REQUIRED_PROJECT = ("id", "name", "url", "summary", "skills")
REQUIRED_SKILL = ("name", "source_url", "purpose", "capabilities", "minimum_inputs", "outputs", "examples")


def localized(value: Any, language: str) -> Any:
    if not isinstance(value, dict):
        return value
    if language in value:
        return value[language]
    fallback = "en" if language == "zh-CN" else "zh-CN"
    return value.get(fallback, "")


def validate_catalog(data: dict[str, Any], language: str) -> None:
    if not isinstance(data, dict) or "title" not in data or not isinstance(data.get("projects"), list):
        raise ValueError("catalog must contain title and a projects array")
    if not data["projects"]:
        raise ValueError("catalog projects must not be empty")
    seen: set[str] = set()
    target_languages = ("zh-CN", "en") if language == "both" else (language,)
    for project in data["projects"]:
        missing = [key for key in REQUIRED_PROJECT if key not in project]
        if missing:
            raise ValueError(f"project is missing: {', '.join(missing)}")
        if project["id"] in seen:
            raise ValueError(f"duplicate project id: {project['id']}")
        seen.add(project["id"])
        if not isinstance(project["skills"], list) or not project["skills"]:
            raise ValueError(f"project {project['id']} has no skills")
        for skill in project["skills"]:
            missing = [key for key in REQUIRED_SKILL if key not in skill]
            if missing:
                raise ValueError(f"skill {skill.get('name', '<unknown>')} is missing: {', '.join(missing)}")
            for lang in target_languages:
                for key in ("purpose", "capabilities", "minimum_inputs", "outputs", "examples"):
                    if localized(skill[key], lang) in (None, "", []):
                        raise ValueError(f"skill {skill['name']} has no {key} for {lang}")


def render(data: dict[str, Any], language: str) -> str:
    validate_catalog(data, language)
    default_lang = "zh-CN" if language in {"zh-CN", "both"} else "en"
    safe_data = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    safe_ui = json.dumps(UI, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    title = html.escape(str(localized(data["title"], default_lang)))
    allowed = json.dumps(["zh-CN", "en"] if language == "both" else [language])
    return TEMPLATE.replace("__TITLE__", title).replace("__DATA__", safe_data).replace(
        "__UI__", safe_ui
    ).replace("__DEFAULT_LANG__", json.dumps(default_lang)).replace("__ALLOWED_LANGS__", allowed)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a SkillShowcase HTML page from catalog JSON.")
    parser.add_argument("catalog", type=Path, help="Path to catalog JSON")
    parser.add_argument("--output", "-o", type=Path, default=Path("skill-showcase.html"))
    parser.add_argument("--language", "-l", choices=sorted(LANGUAGES), default="both")
    args = parser.parse_args()
    data = json.loads(args.catalog.read_text(encoding="utf-8"))
    output = render(data, args.language)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(f"Rendered {args.output} ({sum(len(p['skills']) for p in data['projects'])} skills, {args.language})")
    return 0


TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <link rel="icon" href="data:,">
  <title>__TITLE__</title>
  <style>
    :root{--paper:#f6f4ee;--surface:#fff;--ink:#18202a;--muted:#65707d;--line:#d9d7d0;--accent:#155eef;--accent-soft:#eaf0ff;--code:#243246;--shadow:0 14px 42px rgba(28,38,51,.08);--radius:18px}
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.65 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}button,input{font:inherit}a{color:inherit}.wrap{width:min(1180px,calc(100% - 32px));margin:auto}.masthead{padding:64px 0 24px}.eyebrow{margin:0 0 12px;color:var(--accent);font-size:12px;font-weight:800;letter-spacing:.16em}.masthead h1{max-width:900px;margin:0;font:700 clamp(38px,7vw,76px)/.98 Georgia,"Times New Roman",serif;letter-spacing:-.045em}.subtitle{max-width:760px;margin:20px 0 0;color:var(--muted);font-size:18px}.meta{display:flex;gap:18px;flex-wrap:wrap;margin-top:28px;color:var(--muted);font-size:13px}.language{display:flex;align-items:center;gap:8px;margin-left:auto}.language button,.tabs button{border:1px solid var(--line);background:transparent;color:var(--muted);cursor:pointer}.language button{padding:6px 10px;border-radius:999px}.language button[aria-pressed="true"]{border-color:var(--accent);background:var(--accent);color:#fff}.tabs-shell{position:sticky;top:0;z-index:5;border-block:1px solid var(--line);background:rgba(246,244,238,.94);backdrop-filter:blur(12px)}.tabs{display:flex;gap:7px;overflow:auto;padding:10px 0}.tabs button{flex:0 0 auto;padding:9px 13px;border-radius:999px}.tabs button[aria-selected="true"]{border-color:var(--ink);background:var(--ink);color:#fff}.main{padding:32px 0 72px}.project{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:end;padding:30px;border:1px solid var(--line);border-radius:var(--radius);background:var(--surface);box-shadow:var(--shadow)}.project h2{margin:0;font:700 clamp(28px,4vw,46px)/1.05 Georgia,"Times New Roman",serif}.project p{max-width:780px;margin:12px 0 0;color:var(--muted);font-size:17px}.repo,.source{display:inline-flex;align-items:center;gap:7px;color:var(--accent);font-weight:750;text-decoration-thickness:1px;text-underline-offset:4px}.toolbar{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:14px;align-items:center;margin:26px 0 18px}.search{width:100%;min-height:50px;padding:12px 15px;border:1px solid var(--line);border-radius:12px;background:var(--surface);color:var(--ink)}.count{color:var(--muted);font-variant-numeric:tabular-nums}.skills{display:grid;gap:16px}.skill{padding:26px;border:1px solid var(--line);border-radius:var(--radius);background:var(--surface)}.skill-head{display:flex;justify-content:space-between;gap:18px;align-items:start}.skill h3{margin:0;font-size:22px;line-height:1.25}.slug{margin-top:4px;color:var(--muted);font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;overflow-wrap:anywhere}.source{flex:0 0 auto;font-size:13px}.purpose{margin:20px 0 0;padding:17px 19px;border-left:3px solid var(--accent);background:var(--accent-soft);font-size:17px}.sections{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px 34px;margin-top:24px}.section h4{margin:0 0 8px;color:var(--muted);font-size:12px;letter-spacing:.1em;text-transform:uppercase}.section ul{margin:0;padding-left:19px}.section li+li{margin-top:5px}.input-label{display:block;margin:10px 0 3px;color:var(--code);font-weight:750}.examples{grid-column:1/-1}.examples li{padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:#fafafa;list-style:none}.examples ul{display:grid;gap:8px;padding:0}.empty{padding:48px 20px;border:1px dashed var(--line);border-radius:var(--radius);color:var(--muted);text-align:center}.footer{padding:24px 0 44px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}.hidden{display:none!important}:focus-visible{outline:3px solid rgba(21,94,239,.35);outline-offset:2px}
    @media(max-width:720px){.wrap{width:min(100% - 22px,1180px)}.masthead{padding-top:38px}.meta{display:block}.meta>span{display:block}.meta>span+span{margin-top:4px}.language{margin-top:12px}.project{grid-template-columns:1fr;padding:22px}.toolbar{grid-template-columns:1fr}.skill{padding:20px}.skill-head{display:block}.source{margin-top:10px}.sections{grid-template-columns:1fr}.examples{grid-column:auto}}
  </style>
</head>
<body>
  <header class="masthead"><div class="wrap">
    <p class="eyebrow" id="eyebrow"></p><h1 id="title"></h1><p class="subtitle" id="subtitle"></p>
    <div class="meta"><span id="total"></span><span id="generated"></span><div class="language" id="language"></div></div>
  </div></header>
  <nav class="tabs-shell" aria-label="Projects"><div class="wrap"><div class="tabs" id="tabs" role="tablist"></div></div></nav>
  <main class="main"><div class="wrap"><section class="project" id="project"></section><div class="toolbar"><input class="search" id="search" type="search"><span class="count" id="count"></span></div><div class="skills" id="skills"></div><div class="empty hidden" id="empty"></div></div></main>
  <footer class="footer"><div class="wrap">SkillShowcase · Source-grounded Agent Skill explanations.</div></footer>
  <script>
  const DATA=__DATA__, UI=__UI__, ALLOWED=__ALLOWED_LANGS__; let lang=__DEFAULT_LANG__, active=0, query="";
  const $=id=>document.getElementById(id); const text=(el,value)=>{el.textContent=value??"";return el};
  function loc(value){if(value&&typeof value==="object"&&!Array.isArray(value))return value[lang]??value[lang==="en"?"zh-CN":"en"]??"";return value??""}
  function list(values){const ul=document.createElement("ul");for(const value of (loc(values)||[])){ul.append(text(document.createElement("li"),value))}return ul}
  function section(label,values,cls=""){if(!(loc(values)||[]).length)return null;const box=document.createElement("section");box.className=`section ${cls}`;const h=document.createElement("h4");text(h,label);box.append(h,list(values));return box}
  function searchable(skill){return [skill.name,loc(skill.title),loc(skill.purpose),...(loc(skill.capabilities)||[]),...(loc(skill.minimum_inputs)||[]),...(loc(skill.optional_inputs)||[]),...(loc(skill.outputs)||[]),...(loc(skill.examples)||[]),...(loc(skill.requirements)||[]),...(loc(skill.variants)||[])].join(" ").toLowerCase()}
  function renderHeader(){document.documentElement.lang=lang;document.title=loc(DATA.title);text($("eyebrow"),UI[lang].eyebrow);text($("title"),loc(DATA.title));text($("subtitle"),loc(DATA.subtitle));const n=DATA.projects.reduce((sum,p)=>sum+p.skills.length,0);text($("total"),`${n}${UI[lang].skills}`);text($("generated"),`${UI[lang].generated}: ${DATA.generated_at||"—"}`);const box=$("language");box.replaceChildren();if(ALLOWED.length>1){box.append(text(document.createElement("span"),UI[lang].language));for(const code of ALLOWED){const b=document.createElement("button");text(b,code==="zh-CN"?"中文":"English");b.setAttribute("aria-pressed",String(code===lang));b.onclick=()=>{lang=code;render()};box.append(b)}}}
  function renderTabs(){const tabs=$("tabs");tabs.replaceChildren();DATA.projects.forEach((project,index)=>{const b=document.createElement("button");b.type="button";b.role="tab";b.setAttribute("aria-selected",String(index===active));b.tabIndex=index===active?0:-1;text(b,`${project.name} · ${project.skills.length}`);b.onclick=()=>{active=index;query="";$("search").value="";render()};b.onkeydown=e=>{if(!["ArrowLeft","ArrowRight"].includes(e.key))return;e.preventDefault();active=(active+(e.key==="ArrowRight"?1:-1)+DATA.projects.length)%DATA.projects.length;render();$("tabs").children[active].focus()};tabs.append(b)})}
  function renderProject(){const p=DATA.projects[active],box=$("project");box.replaceChildren();const content=document.createElement("div");const h=document.createElement("h2");text(h,p.name);const summary=document.createElement("p");text(summary,loc(p.summary));content.append(h,summary);if(loc(p.note)){const note=document.createElement("p");note.className="project-note";text(note,loc(p.note));content.append(note)}const a=document.createElement("a");a.className="repo";a.href=p.url;a.target="_blank";a.rel="noopener noreferrer";text(a,`${UI[lang].repo} ↗`);box.append(content,a);$("search").placeholder=UI[lang].search;$("empty").textContent=UI[lang].empty}
  function renderSkills(){const p=DATA.projects[active],needle=query.trim().toLowerCase(),items=p.skills.filter(s=>!needle||searchable(s).includes(needle)),root=$("skills");root.replaceChildren();text($("count"),`${UI[lang].showing} ${items.length} / ${p.skills.length}`);$("empty").classList.toggle("hidden",items.length!==0);for(const skill of items){const card=document.createElement("article");card.className="skill";const head=document.createElement("div");head.className="skill-head";const names=document.createElement("div");const h=document.createElement("h3");text(h,loc(skill.title)||skill.name);const slug=document.createElement("div");slug.className="slug";text(slug,skill.name);names.append(h,slug);const a=document.createElement("a");a.className="source";a.href=skill.source_url;a.target="_blank";a.rel="noopener noreferrer";text(a,`${UI[lang].source} ↗`);head.append(names,a);const purpose=document.createElement("p");purpose.className="purpose";text(purpose,loc(skill.purpose));const sections=document.createElement("div");sections.className="sections";const caps=section(UI[lang].capabilities,skill.capabilities);if(caps)sections.append(caps);const inputs=document.createElement("section");inputs.className="section";inputs.append(text(document.createElement("h4"),UI[lang].inputs));const min=document.createElement("span");min.className="input-label";text(min,UI[lang].minimum);inputs.append(min,list(skill.minimum_inputs));if((loc(skill.optional_inputs)||[]).length){const opt=document.createElement("span");opt.className="input-label";text(opt,UI[lang].optional);inputs.append(opt,list(skill.optional_inputs))}sections.append(inputs);for(const s of [section(UI[lang].outputs,skill.outputs),section(UI[lang].examples,skill.examples,"examples"),section(UI[lang].requirements,skill.requirements),section(UI[lang].variants,skill.variants)])if(s)sections.append(s);card.append(head,purpose,sections);root.append(card)}}
  function render(){renderHeader();renderTabs();renderProject();renderSkills()}
  $("search").addEventListener("input",e=>{query=e.target.value;renderSkills()});render();
  </script>
</body>
</html>'''


if __name__ == "__main__":
    raise SystemExit(main())
