#!/usr/bin/env python3
"""Static site generator.  Usage: .venv/bin/python build.py

  content/posts/YYYY-MM-DD-slug.md   blog posts (frontmatter: title, date, tags)
  content/pages/<name>.html          standalone pages (frontmatter: title, description)
  templates/*.html                   page layouts
  static/                            copied as-is (css, images, resume.pdf)
  docs/                              OUTPUT - generated, never edit by hand
"""
import html
import re
import shutil
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
OUT = ROOT / "docs"

NAME = "Chanyut Lisawat"
EMAIL = "chanyut.lisawat25@gmail.com"
CURRENT = ' aria-current="page"'


def fail(msg):
    sys.exit(f"build.py: {msg}")


def template(name):
    return (TEMPLATES / f"{name}.html").read_text(encoding="utf-8")


def parse(path, required=()):
    """Split '--- key: value ---' frontmatter from the body."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    if not m:
        fail(f"{path.name}: missing frontmatter (--- ... ---)")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    for key in required:
        if not meta.get(key):
            fail(f"{path.name}: frontmatter missing '{key}'")
    meta["body"] = m.group(2)
    return meta


def render(out_path, root, body, title, description, current):
    """Wrap body in the base layout and write it to out_path."""
    page = template("base").format(
        title=title, description=description, root=root, body=body,
        email=EMAIL, name=NAME,
        cur_blog=CURRENT if current == "blog" else "",
        cur_about=CURRENT if current == "about" else "",
        cur_contact=CURRENT if current == "contact" else "",
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page, encoding="utf-8")


def load_posts():
    posts = []
    for path in sorted((CONTENT / "posts").glob("*.md")):
        p = parse(path, required=("title", "date"))
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", p["date"]):
            fail(f"{path.name}: date must be YYYY-MM-DD")
        p["tags"] = [t.strip() for t in p.get("tags", "").split(",") if t.strip()]
        posts.append(p)
    seen = set()
    for p in posts:
        if p["date"] in seen:
            fail(f"two posts share date {p['date']} (URL is /blog/YYYY/MM/DD/)")
        seen.add(p["date"])
    posts.sort(key=lambda p: p["date"], reverse=True)
    for p in posts:
        y, m, d = p["date"].split("-")
        p["url"] = f"blog/{y}/{m}/{d}/"
    return posts


def build_posts(posts):
    post_tpl = template("post")
    for i, p in enumerate(posts):
        content = markdown.markdown(p["body"], extensions=["fenced_code", "tables"])
        title = html.escape(p["title"])
        nav = ""
        if i + 1 < len(posts):
            older = posts[i + 1]
            nav = (f'<p class="post-nav"><a href="../../../{older["url"][5:]}" '
                   f'rel="prev">&laquo; {html.escape(older["title"])}</a></p>')
        tags = ""
        if p["tags"]:
            tags = '<p class="tags">' + " ".join(
                f"<span>{html.escape(t)}</span>" for t in p["tags"]) + "</p>"
        body = post_tpl.format(title=title, date=p["date"], content=content,
                               tags=tags, nav=nav)
        render(OUT / p["url"] / "index.html", "../../../../", body,
               f"{title} - {NAME}", title, "blog")


def build_index(posts):
    n = len(posts)
    items = "\n".join(
        f'                <li><span class="date">{p["date"]}</span> '
        f'<a href="{p["url"]}">{html.escape(p["title"])}</a></li>'
        for p in posts)
    count = f'There {"is" if n == 1 else "are"} {n} post{"" if n == 1 else "s"}.'
    body = template("index").format(count=count, items=items)
    render(OUT / "index.html", "", body, NAME, "Blog of Chanyut Lisawat.", "blog")


def build_pages():
    for path in sorted((CONTENT / "pages").glob("*.html")):
        p = parse(path, required=("title", "description"))
        render(OUT / f"{path.stem}.html", "", p["body"].rstrip("\n"),
               p["title"], p["description"], path.stem)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT)
    posts = load_posts()
    build_posts(posts)
    build_index(posts)
    build_pages()
    print(f"built {len(posts)} post(s) into docs/")


if __name__ == "__main__":
    main()
