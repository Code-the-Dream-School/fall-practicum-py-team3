# Packaging and Linting (decisions)

## Why an editable package?
- Problem: our code lives deep in `services/pipeline/src/`, so imports like `import pipeline` only worked if you manually tweaked `sys.path` or `PYTHONPATH`. That's confusing and breaks easily.
- Fix: make it an **editable package** with `pip install -e .`. Now `import pipeline` works from anywhere - tests, scripts, the dashboard — with no path hacks.
- "Editable" means Python reads your code straight from `src/`, so when you edit a file you don't need to reinstall.
- Set up with `python setup_env.py` (or `pip install -e .` directly from the project root.).

## Where the code lives
- All Python code is under `services/pipeline/src/`.
- Data files (`cities.yaml`, `pollutants.csv`) ship with the package so they're available after install.
- Dependencies stay in `requirements.txt`; `pyproject.toml` reads them from there.

## Linting
- We use **Ruff** for linting, formatting, and sorting imports.
- Run it locally: `ruff check .` and `ruff format .`
- Config is in `pyproject.toml` (line length, ignored rules, etc.).
- Ruff auto-fixes many issues: `ruff check --fix .`

## Git hooks (pre-commit)
- Set up in `.pre-commit-config.yaml` at the repo root.
- On every `git push`, pre-commit runs Ruff automatically. If it finds problems (or reformats files), the push is blocked until you fix and re-push.
- `setup_env.py` installs the hooks for you, so new contributors get them automatically - no manual steps.
- You can run them anytime by hand: `pre-commit run --all-files`
- This catches mistakes locally before they ever reach GitHub.

## CI (GitHub Actions)
- Set up in `.github/workflows/python-quality-gates.yml`.
- On every pull request (and push), GitHub spins up a clean machine and runs:
  1. `ruff check .` and `ruff format --check .` (lint + format)
  2. `python -m compileall services` (syntax check)
  3. `pytest` (all tests)
- If any step fails, the PR shows a red X and can't be merged until it's fixed.
- You can see results under the "Checks" tab on the PR, or in the Actions tab of the repo.
- This is our safety net: even if someone skips the local hooks, CI catches problems before merge.
```
