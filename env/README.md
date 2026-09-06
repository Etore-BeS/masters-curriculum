# Shared Python environment (masters-curriculum)

One virtual environment at the **repository root** serves all courses (FT108A, FT105A, …). Do not create per-course or per-exercise `.venv` folders.

Package manager: **uv**. Dependency source: root `pyproject.toml` + lockfile `uv.lock`.

## Create / refresh the environment

From the repository root:

```bash
uv sync
```

Fish: same command (`uv sync`).

This creates or updates `.venv/` and installs the default dependency set plus the `dev` group (Ruff). Manim is not included.

## Activate

```bash
source .venv/bin/activate
```

Fish:

```fish
source .venv/bin/activate.fish
```

Or run tools without activating:

```bash
uv run python …
uv run jupyter …
```

## Jupyter kernel

```bash
uv run python -m ipykernel install --user --name masters-curriculum --display-name "Python (masters-curriculum)"
```

In notebooks, select the kernel named **masters-curriculum**.

## Manim (optional, heavy)

Manim lives in the `manim` dependency group. System requirement: `ffmpeg`.

```bash
uv sync --group manim
```

Never create a second venv for Manim. Use the same repo-root `.venv`.

## Course data and deliveries

- Datasets stay under each course, e.g. `courses/ft108a-machine-learning/data/`.
- Local ZIP/PDF submissions stay under each course `entregas/` (gitignored).
- From an FT108A exercise `code/` directory, load liver with `../../../data/liver.csv`.

## Rules

- Prefer `.venv/` at the repo root only.
- Never create `courses/*/.venv`, `exercises/*/code/.venv`, or `notes/*/.venv`.
- Do not duplicate CSVs into exercise folders.
- Do not add `requirements.txt` under `env/` — edit `pyproject.toml` and run `uv sync` (then commit `uv.lock`).
