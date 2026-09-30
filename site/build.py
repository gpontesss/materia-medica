#!/usr/bin/env python3
"""Generates the materia medica website from the Typst source entries.

Every substance entry in materia-medica/*.typ is compiled to HTML with
Typst's own (experimental) HTML backend, then wrapped in this script's page
template and indexed for client-side search. Nothing under out/ is ever
committed -- this script is the only source of truth for the generated
site, and it is meant to be re-run on every push (see
.github/workflows/pages.yml).
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ENTRIES_DIR = REPO_ROOT / "materia-medica"
FONTS_DIR = REPO_ROOT / "fonts"
SITE_SRC_DIR = Path(__file__).resolve().parent
ASSETS_DIR = SITE_SRC_DIR / "assets"

GLOSSARY_SLUG = "zz-glossary"
REFERENCE_SLUGS = {"climates", "tibb-al-arabi"}

SITE_TITLE = "Materia Medica"
SITE_TAGLINE = "A comparative materia medica of foods and medicinals"

HEADING_RE = re.compile(r"<(h[1-6])([^>]*)>(.*?)</\1>", re.DOTALL)
ANY_TAG_RE = re.compile(r"<[^>]+>")
BODY_RE = re.compile(r"<body>\n?(.*)</body>", re.DOTALL)


class BuildError(RuntimeError):
    pass


def run_typst_html(src: Path, dest: Path) -> None:
    result = subprocess.run(
        [
            "typst",
            "compile",
            "--features",
            "html",
            "--format",
            "html",
            "--font-path",
            str(FONTS_DIR),
            str(src),
            str(dest),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise BuildError(
            f"typst compile failed for {src.name}:\n{result.stderr}"
        )


def extract_body(raw_html: str, src_name: str) -> str:
    match = BODY_RE.search(raw_html)
    if not match:
        raise BuildError(f"could not find <body> in typst html output for {src_name}")
    return match.group(1)


def plain_text(fragment: str) -> str:
    text = ANY_TAG_RE.sub(" ", fragment)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text, flags=re.UNICODE).strip("-")
    return text or "section"


def demote_headings(fragment: str) -> str:
    """Typst's top-level `=` heading compiles to <h2>; shift everything up
    one level so the entry title becomes the page's single <h1>."""

    def repl(m: re.Match) -> str:
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        level = int(tag[1])
        new_level = max(1, level - 1)
        return f"<h{new_level}{attrs}>{inner}</h{new_level}>"

    return HEADING_RE.sub(repl, fragment)


def add_heading_ids_and_toc(fragment: str) -> tuple[str, list[dict]]:
    """Adds an id to every heading (for deep links) and returns a table of
    contents built from the top two heading levels actually used."""
    seen: dict[str, int] = {}
    toc: list[dict] = []
    levels_present: set[int] = set()

    for m in HEADING_RE.finditer(fragment):
        levels_present.add(int(m.group(1)[1]))
    toc_levels = sorted(levels_present)[:2]

    def repl(m: re.Match) -> str:
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        level = int(tag[1])
        text = plain_text(inner)
        base = slugify(text)
        n = seen.get(base, 0)
        seen[base] = n + 1
        anchor = base if n == 0 else f"{base}-{n}"
        if level in toc_levels:
            toc.append({"level": level, "text": text, "anchor": anchor})
        return f'<{tag} id="{anchor}"{attrs}>{inner}</{tag}>'

    new_fragment = HEADING_RE.sub(repl, fragment)
    return new_fragment, toc


def first_excerpt(fragment: str, limit: int = 220) -> str:
    m = re.search(r"<p[^>]*>(.*?)</p>", fragment, re.DOTALL)
    text = plain_text(m.group(1)) if m else ""
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "…"
    return text


def category_for(slug: str) -> str:
    if slug == GLOSSARY_SLUG:
        return "glossary"
    if slug in REFERENCE_SLUGS:
        return "reference"
    return "entry"


CATEGORY_LABELS = {
    "entry": "Substance entries",
    "reference": "Foundational references",
    "glossary": "Glossary",
}


def load_entries(work_dir: Path) -> list[dict]:
    entries = []
    for src in sorted(ENTRIES_DIR.glob("*.typ")):
        slug = src.stem
        tmp = work_dir / f"_{slug}.raw.html"
        run_typst_html(src, tmp)
        raw = tmp.read_text(encoding="utf-8")
        tmp.unlink()

        fragment = extract_body(raw, src.name)
        fragment = demote_headings(fragment)
        fragment, toc = add_heading_ids_and_toc(fragment)

        title_match = HEADING_RE.search(fragment)
        title = plain_text(title_match.group(3)) if title_match else slug.replace("-", " ").title()

        entries.append(
            {
                "slug": slug,
                "title": title,
                "category": category_for(slug),
                "content": fragment,
                "toc": toc,
                "excerpt": first_excerpt(fragment),
                "text": plain_text(fragment),
            }
        )
    return entries


TOP_FAB_HTML = (
    '<button id="top-fab" class="fab-circle top-fab" type="button" aria-label="Back to top">'
    '<svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<line x1="12" y1="19" x2="12" y2="5"></line>'
    '<polyline points="5 12 12 5 19 12"></polyline>'
    "</svg>"
    "</button>"
)


def render_shell(*, title: str, body: str, active_slug: str = "", toc_fab_html: str = "") -> str:
    page_title = f"{title} — {SITE_TITLE}" if title != SITE_TITLE else SITE_TITLE
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(page_title)}</title>
<link rel="stylesheet" href="style.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..700;1,400..700&display=swap" rel="stylesheet">
</head>
<body>
<header class="site-header">
  <a class="site-title" href="index.html">{html.escape(SITE_TITLE)}</a>
  <div class="search-wrap">
    <input id="search-input" type="search" placeholder="Search entries…" autocomplete="off" aria-label="Search the materia medica">
    <div id="search-results" class="search-results" hidden></div>
  </div>
</header>
<main class="site-main">
{body}
</main>
<footer class="site-footer">
  <p>{html.escape(SITE_TAGLINE)}. Generated from the Typst sources in <code>materia-medica/</code>.</p>
</footer>

<div class="fab-stack">
  <button id="nav-fab" class="fab-circle nav-fab" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="nav-panel">A–Z</button>
  {toc_fab_html}
  {TOP_FAB_HTML}
</div>
<div id="nav-overlay" class="nav-overlay" hidden>
  <div id="nav-panel" class="nav-panel" role="dialog" aria-modal="true" aria-label="Jump to an entry">
    <div class="nav-panel-header">
      <span>All entries</span>
      <button id="nav-close" class="nav-close" type="button" aria-label="Close">&times;</button>
    </div>
    <div class="nav-panel-body">
      <ol id="nav-list" class="nav-list" aria-label="Entries, alphabetically"></ol>
      <nav id="nav-az" class="nav-az" aria-label="Jump to letter"></nav>
    </div>
  </div>
</div>

<script src="search.js" data-base=""></script>
<script src="nav.js" data-base="" data-active="{html.escape(active_slug)}"></script>
</body>
</html>
"""


def render_entry_page(entry: dict) -> str:
    toc_html = ""
    toc_fab_html = ""
    if len(entry["toc"]) > 1:
        items = "\n".join(
            f'<li class="toc-l{item["level"]}"><a href="#{item["anchor"]}">{html.escape(item["text"])}</a></li>'
            for item in entry["toc"]
        )
        toc_html = f'<nav id="entry-toc" class="entry-toc" aria-label="Sections in this entry"><h2 class="toc-heading">Contents</h2><ol>{items}</ol></nav>'
        toc_fab_html = (
            '<button id="toc-fab" class="fab-circle toc-fab" type="button" '
            'aria-haspopup="true" aria-expanded="false" aria-controls="entry-toc" '
            'aria-label="Table of contents">'
            '<svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<circle cx="4" cy="6" r="1"></circle>'
            '<circle cx="4" cy="12" r="1"></circle>'
            '<circle cx="4" cy="18" r="1"></circle>'
            '<line x1="9" y1="6" x2="20" y2="6"></line>'
            '<line x1="9" y1="12" x2="20" y2="12"></line>'
            '<line x1="9" y1="18" x2="20" y2="18"></line>'
            "</svg>"
            "</button>"
        )

    body = f"""<div class="entry-layout">
  {toc_html}
  <article class="entry">
{entry["content"]}
  </article>
</div>
<p class="back-link"><a href="index.html">← Back to index</a></p>"""
    return render_shell(
        title=entry["title"], body=body, active_slug=entry["slug"], toc_fab_html=toc_fab_html
    )


def render_index_page(entries: list[dict]) -> str:
    by_category: dict[str, list[dict]] = {"reference": [], "entry": [], "glossary": []}
    for e in entries:
        by_category[e["category"]].append(e)
    for group in by_category.values():
        group.sort(key=lambda e: e["title"].lower())

    sections = []
    for cat in ("reference", "entry", "glossary"):
        group = by_category[cat]
        if not group:
            continue
        multi = " entry-list-multi" if len(group) > 8 else ""
        items = "\n".join(
            f'<li><a href="{e["slug"]}.html">{html.escape(e["title"])}</a></li>' for e in group
        )
        sections.append(
            f'<section class="entry-group"><h2>{html.escape(CATEGORY_LABELS[cat])}</h2>'
            f'<ul class="entry-list{multi}">{items}</ul></section>'
        )

    body = f"""<p class="index-intro">{len(entries)} entries, synthesizing Classical Chinese Medicine, Ayurvedic dravyaguna,
Tibb (Greco-Arabic medicine), and modern nutrition &amp; pharmacology. Use the search box above
to look across every entry's full text.</p>
{''.join(sections)}"""
    return render_shell(title=SITE_TITLE, body=body)


def build(out_dir: Path) -> None:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    entries = load_entries(out_dir)
    if not entries:
        raise BuildError("no materia-medica/*.typ entries found")

    for entry in entries:
        page = render_entry_page(entry)
        (out_dir / f"{entry['slug']}.html").write_text(page, encoding="utf-8")

    (out_dir / "index.html").write_text(render_index_page(entries), encoding="utf-8")

    search_index = [
        {
            "slug": e["slug"],
            "title": e["title"],
            "category": e["category"],
            "excerpt": e["excerpt"],
            "text": e["text"],
        }
        for e in entries
    ]
    (out_dir / "search-index.json").write_text(
        json.dumps(search_index, ensure_ascii=False), encoding="utf-8"
    )

    nav_index = sorted(
        (
            {"slug": e["slug"], "title": e["title"], "category": e["category"]}
            for e in entries
        ),
        key=lambda e: e["title"].lower(),
    )
    (out_dir / "nav-index.json").write_text(
        json.dumps(nav_index, ensure_ascii=False), encoding="utf-8"
    )

    shutil.copy(ASSETS_DIR / "style.css", out_dir / "style.css")
    shutil.copy(ASSETS_DIR / "search.js", out_dir / "search.js")
    shutil.copy(ASSETS_DIR / "nav.js", out_dir / "nav.js")

    fonts_out = out_dir / "fonts"
    fonts_out.mkdir()
    for font_file in FONTS_DIR.glob("*.ttf"):
        shutil.copy(font_file, fonts_out / font_file.name)

    print(f"Built {len(entries)} entries into {out_dir}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "out" / "site",
        help="output directory (default: out/site)",
    )
    args = parser.parse_args()

    if shutil.which("typst") is None:
        print("error: typst binary not found on PATH", file=sys.stderr)
        return 1

    try:
        build(args.out)
    except BuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
