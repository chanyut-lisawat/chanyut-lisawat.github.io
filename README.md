# my_website

## Add a blog post
1. Create `posts/YYYY-MM-DD-slug.md`:
   ```
   ---
   title: My title
   date: YYYY-MM-DD
   tags: optional, comma-separated
   ---
   Markdown body here.
   ```
2. Run `.venv/bin/python build.py` (first time: `python3 -m venv .venv && .venv/bin/pip install markdown`).
3. Open `blog.html`. Don't hand-edit `blog.html` or `blog/` — they are generated.

One post per date (URL is `/blog/YYYY/MM/DD/`).
