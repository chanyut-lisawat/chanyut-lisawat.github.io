#!/usr/bin/env python3
"""Static site generator.  Usage: python3 build.py

  content/posts/YYYY-MM-DD-slug.md   blog posts (frontmatter: title, date, tags)
  content/pages/<name>.html          standalone pages (frontmatter: title, description)
  templates/*.html                   page layouts
  static/                            copied as-is (css, images, resume.pdf)
  docs/                              OUTPUT - generated, never edit by hand
"""
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def ensure_markdown():
    """Make `python3 build.py` work anywhere: if `markdown` is missing, create
    .venv, install it there, and re-run this script with the venv's Python."""
    try:
        import markdown  # noqa: F401
        return
    except ImportError:
        pass
    venv_python = ROOT / ".venv" / "bin" / "python"
    if os.environ.get("BUILD_PY_REEXEC"):  # already re-ran once; don't loop
        sys.exit("build.py: could not install 'markdown'; try: .venv/bin/pip install markdown")
    os.environ["BUILD_PY_REEXEC"] = "1"
    if not venv_python.exists():
        print("Creating .venv and installing markdown (one-time)...")
        subprocess.check_call([sys.executable, "-m", "venv", str(ROOT / ".venv")])
    subprocess.check_call([str(venv_python), "-m", "pip", "install", "-q", "markdown"])
    os.execv(str(venv_python), [str(venv_python), *sys.argv])


ensure_markdown()
import markdown  # noqa: E402

CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
OUT = ROOT / "docs"

NAME = "Chanyut Lisawat"
EMAIL = "chanyut.lisawat25@gmail.com"
CURRENT = ' aria-current="page"'
HOME_POSTS = 10  # recent posts shown on the home page
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


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
        cur_home=CURRENT if current == "home" else "",
        cur_archive=CURRENT if current == "archive" else "",
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
        m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})-(.+)", path.stem)
        if not m:
            fail(f"{path.name}: filename must be YYYY-MM-DD-slug.md")
        if m.group(1) != p["date"]:
            fail(f"{path.name}: filename date does not match frontmatter date {p['date']}")
        y, mo, d = p["date"].split("-")
        p["url"] = f"blog/{y}/{mo}/{d}/{m.group(2)}/"
        posts.append(p)
    seen = set()
    for p in posts:
        if p["url"] in seen:
            fail(f"two posts share the URL {p['url']}")
        seen.add(p["url"])
    posts.sort(key=lambda p: (p["date"], p["url"]), reverse=True)
    return posts


def build_posts(posts):
    post_tpl = template("post")
    for i, p in enumerate(posts):
        content = markdown.markdown(p["body"], extensions=["fenced_code", "tables"])
        title = html.escape(p["title"])
        nav = ""
        if i + 1 < len(posts):
            older = posts[i + 1]
            nav = (f'<p class="post-nav"><a href="../../../../{older["url"][5:]}" '
                   f'rel="prev">&laquo; {html.escape(older["title"])}</a></p>')
        tags = ""
        if p["tags"]:
            tags = '<p class="tags">' + " ".join(
                f"<span>{html.escape(t)}</span>" for t in p["tags"]) + "</p>"
        body = post_tpl.format(title=title, date=p["date"], content=content,
                               tags=tags, nav=nav)
        render(OUT / p["url"] / "index.html", "../../../../../", body,
               f"{title} - {NAME}", title, None)


def long_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{MONTHS[m - 1]} {d}, {y}"


def excerpt(body, limit=280):
    """First plain paragraph of a post, flattened to one line. Links are reduced
    to their text because post-relative paths don't resolve from the home page."""
    for block in re.split(r"\n\s*\n", body.strip()):
        block = block.strip()
        if not block or block[0] in "#`|-*>" or re.match(r"\d+\.", block):
            continue
        text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", block)
        text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
        text = " ".join(text.split())
        if len(text) > limit:
            text = text[:limit]
            if " " in text:
                text = text.rsplit(" ", 1)[0]
        return markdown.markdown(text)[3:-4]  # drop the wrapping <p>...</p>
    return ""


def build_home(posts):
    entries = []
    for p in posts[:HOME_POSTS]:
        title = html.escape(p["title"])
        tags = ""
        if p["tags"]:
            tags = ('\n                <ul class="tags">'
                    + "".join(f"<li>{html.escape(t)}</li>" for t in p["tags"])
                    + "</ul>")
        entries.append(
            f'            <article class="home-post">\n'
            f'                <h2><a href="{p["url"]}">{title}</a></h2>\n'
            f'                <p class="post-date">{long_date(p["date"])}</p>\n'
            f'                <blockquote><p>{excerpt(p["body"])} '
            f'<a href="{p["url"]}">[&hellip;]</a></p></blockquote>{tags}\n'
            f"            </article>"
        )
    body = template("home").format(entries="\n".join(entries), total=len(posts))
    render(OUT / "index.html", "", body, NAME, "Blog of Chanyut Lisawat.", "home")


def build_archive(posts):
    n = len(posts)
    items = "\n".join(
        f'                <li><span class="date">{p["date"]}</span> '
        f'<a href="{p["url"]}">{html.escape(p["title"])}</a></li>'
        for p in posts)
    count = f'There {"is" if n == 1 else "are"} {n} post{"" if n == 1 else "s"}.'
    body = template("archive").format(count=count, items=items)
    render(OUT / "archive.html", "", body, f"Archive - {NAME}",
           "All posts by Chanyut Lisawat.", "archive")


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
    build_home(posts)
    build_archive(posts)
    build_pages()
    print(f"built {len(posts)} post(s) into docs/")


if __name__ == "__main__":
    main()
