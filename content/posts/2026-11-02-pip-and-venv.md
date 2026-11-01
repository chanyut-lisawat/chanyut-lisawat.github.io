---
title: pip and venv, and why you have to activate
date: 2026-11-02
tags: python, pip, venv
---

While building this site I wrote a small Python script (`build.py`) that turns
Markdown files into HTML. It depends on a single package, `markdown`, but when I ran
`python3 build.py` I got an error:

```
ModuleNotFoundError: No module named 'markdown'
```

even though I had already installed it. This post is what I learned from that.

### What is pip?

`pip` downloads Python packages from a central repository called
[PyPI](https://pypi.org/) onto your machine.

```bash
pip install markdown
```

This downloads the `markdown` package and stores it in the `site-packages` folder of
the Python that pip is attached to. When a script says `import markdown`, Python looks
for it in that folder.

The key point: **a package is installed for one particular Python, not for the whole
machine.**

### The problem with installing everything globally

If you install everything into the machine's single Python, you run into trouble:

- Project A needs version 1 of a package and project B needs version 2, but one Python
  can only hold one version.
- Old packages you no longer use pile up, and you can't tell which project they belong
  to.
- Some systems (for example Python installed through Homebrew on macOS) refuse
  outright and answer `error: externally-managed-environment`, because they don't want
  you changing packages the system itself depends on.

### What is venv?

`venv` creates a second, separate copy of Python inside your project folder, with its
own place to store packages.

```bash
python3 -m venv .venv
.venv/bin/pip install markdown
```

The first line creates the `.venv/` folder. The second installs `markdown` into the
Python inside `.venv`, not the system one. Each project gets its own set of packages,
so they can't collide.

### Why do you have to activate it?

This was the part that confused me most. The `python3` you type in the terminal is the
machine's Python, and it knows nothing about `.venv/`. So there are three ways to end
up using the Python in `.venv`:

| Command | Python that runs | Finds `markdown`? |
|---|---|---|
| `python3 build.py` | the system's | no |
| `.venv/bin/python build.py` | the one in `.venv` | yes |
| `source .venv/bin/activate`, then `python build.py` | the one in `.venv` | yes |

`activate` isn't magic. It just makes the word `python` in that terminal point to the
Python inside `.venv`, and only for that terminal window. Open a new window and you
have to do it again. `deactivate` undoes it.

### Which should you use?

venv trades a cleaner machine for extra steps when you run things.

- **Several projects, or many packages:** use venv. Version conflicts are real and
  painful to untangle.
- **One project, few packages, on your own machine:** a plain `pip install` into the
  machine's Python is fine, as long as your system doesn't block it.

I chose venv for this site because that's the usual best practice, but it turned out to
be slightly more than I needed, since there is one project and one package.

### If you don't want to type the long command every time

- Use `.venv/bin/python build.py` directly, with no activation.
- Let the script find the venv itself. In this site's `build.py`, if `markdown` is
  missing, the script creates `.venv`, installs it, and re-runs itself with the
  `.venv` Python. The result is that `python3 build.py` works as normal.
- Tools like [uv](https://docs.astral.sh/uv/) manage the venv for you automatically
  (I haven't tried it yet).

### Things to remember

- Always put `.venv/` in `.gitignore`. Don't commit it.
- Keep your package list in a `requirements.txt` (create it with
  `pip freeze > requirements.txt`). Other people, or you in the future, can then install
  everything with `pip install -r requirements.txt`.
- If you get `ModuleNotFoundError` even though you installed the package, suspect first
  that the Python running your script and the Python pip installed into are **two
  different ones**. Check with `which python3` and `python3 -m pip --version`.
