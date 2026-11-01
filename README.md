# my_website

## The one rule
**Edit only inside `src/`. Never edit anything in `docs/`.**
`docs/` is the finished website, rebuilt from `src/` every time you run:

```
python3 build.py
```

## What to edit
| I want to change...            | Edit this file                         |
|--------------------------------|----------------------------------------|
| the About page                 | `src/pages/about.html`                 |
| the Contact page               | `src/pages/contact.html`               |
| a blog post                    | `src/posts/YYYY-MM-DD-slug.md`         |
| the menu / header / footer     | `src/templates/base.html`              |
| the home page layout           | `src/templates/home.html`              |
| the archive page layout        | `src/templates/archive.html`           |
| colors, fonts, spacing         | `src/static/style.css`                 |
| images                         | put them in `src/static/images/`       |

Then: `python3 build.py`, open `docs/index.html` (Live Server) to preview,
`git add . && git commit -m "..." && git push` to publish.
Every file in `docs/` starts with a "GENERATED ... do not edit" comment.

## Add a blog post
Create `src/posts/YYYY-MM-DD-slug.md`:
```
---
title: My title
date: YYYY-MM-DD
tags: optional, comma-separated
---
Markdown body here.
```
URL is `/blog/YYYY/MM/DD/slug/`, so several posts can share a date. Images are referenced
from a post as `../../../../../images/name.png`.

## Resume
`src/static/resume.pdf` is git-ignored because it contains a phone number.
Remove the two lines in `.gitignore` to publish it.
