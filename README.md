# my_website

Static site: Markdown + HTML sources in, plain HTML out. No database.

```
content/
  posts/   blog posts  YYYY-MM-DD-slug.md   (frontmatter: title, date, tags)
  pages/   about.html, contact.html         (frontmatter: title, description)
templates/ base.html (header/nav/footer), post.html, index.html
static/    style.css, images/, resume.pdf   (copied as-is)
docs/      GENERATED output served by GitHub Pages - never edit by hand
build.py   the generator
```

## Add a blog post
1. Create `content/posts/YYYY-MM-DD-slug.md`:
   ```
   ---
   title: My title
   date: YYYY-MM-DD
   tags: optional, comma-separated
   ---
   Markdown body here.
   ```
2. Build: `.venv/bin/python build.py`
   (first time: `python3 -m venv .venv && .venv/bin/pip install markdown`)
3. Open `docs/index.html` to preview.
4. `git add . && git commit -m "..." && git push`

One post per date (URL is `/blog/YYYY/MM/DD/`). Images go in `static/images/` and are
referenced from a post as `../../../../images/name.png`.

## Resume
`static/resume.pdf` is git-ignored because it contains a phone number.
Remove the two lines in `.gitignore` to publish it.
