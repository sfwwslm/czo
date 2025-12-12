# Repository Guidelines

## Project Structure & Module Organization

- Core package lives in `src/czo`; `__init__.py` re-exports `Timer`, `DateTime`, `Rand`, `Net`, `Paths`, `Faker`.
- Utility modules sit under `src/czo/utils/` (`randgen.py`, `datetime.py`, `net.py`, `paths.py`, `faker.py`); keep helpers cohesive and small.
- Reference datasets are in `src/czo/data/` (addresses, housing, shop signs, internal utils). Treat these as read-only assets and avoid in-place mutation.
- Tests use pytest in `tests/` with `test_*.py` names mirroring the module under test. Build artifacts appear in `dist/`; do not hand-edit.

## Build, Test, and Development Commands

- Create environment: `python -m venv .venv && .\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Unix).
- Install dependencies: `pip install -r requirements.txt` (generated via `uv pip compile pyproject.toml -o requirements.txt`).
- Run tests: `python -m pytest` (inherits `-ra -v -s --disable-warnings` from `pyproject.toml`).
- Build distributables: `python -m build` writes wheels/sdist to `dist/`.

## Coding Style & Naming Conventions

- Target Python 3.10+; use 4-space indentation and PEP 8 spacing. Favor explicit type hints.
- Public APIs should be exported via `__all__` in `src/czo/__init__.py` to keep the surface small.
- Functions and variables use `snake_case`; classes use `PascalCase`. Keep docstrings concise and factual.
- For randomness helpers, prefer `secrets` or `random.SystemRandom` as used in `Rand` to stay consistent.

## Testing Guidelines

- Place new tests in `tests/` alongside existing `test_date.py`, `test_help.py`, `test_net.py`, `test_rand.py`; name files `test_<module>.py`.
- Aim for deterministic assertions even when exercising random utilities (seed where needed or assert shapes, not specific values).
- If adding datasets, include a smoke test that loads them and validates expected keys/counts to avoid regressions.

## Commit & Pull Request Guidelines

- Submission guidelines: Use the English prefix "Conventional Commit" (e.g., `feat:`, `fix:`, `chore:`), and use Chinese descriptions after the colon.
- Each PR should include: short summary of changes, linked issue (if any), test evidence (`python -m pytest` output), and notes on public API changes.
- Keep commits focused; prefer small, reviewable diffs and avoid mixing refactors with feature work.
- Do not commit `.venv`, `dist/`, or cache directories; respect `.gitignore`.

## Communication

- Please respond in Chinese by default.
