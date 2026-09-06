# Agent rules

This repository holds study notes, exercises, and course projects for Étore Braga e Santos's master's at UNICAMP PPGT (FT Limeira). Thesis work lives in another repository. Do not add thesis drafts, proposals, or literature reviews here.

Read this file before you change the tree. Follow these rules unless the user overrides them in the current message.

## Scope

- In: courses, notes, exercises, course projects, bibliographic records, local (gitignored) lecture slides and paper PDFs, local admin facts for forms.
- Out: thesis files, enrollment PII in git, lecture PDFs in git, paper PDFs in git.

## Layout

```
README.md
AGENTS.md
.gitignore
pyproject.toml            # uv project: default deps + group manim
uv.lock                   # locked resolutions (commit this)
env/                      # how to use the shared env (README only)
  README.md
.venv/                    # SINGLE shared Python env (gitignored; uv-managed)
admin/                    # bureaucratic kit
  README.md               # tracked
  facts.example.md        # tracked template
  facts.md                # gitignored
  documents/              # gitignored PDFs
references/
  catalog.md              # one record per source
  papers/                 # gitignored PDFs named <key>.pdf
courses/<code>-<slug>/
  README.md
  references.md           # keys used in this course
  data/                   # canonical datasets for THIS course
  entregas/               # local ZIP/PDF deliveries (gitignored)
  notes/                  # study notes — NO local .venv
  exercises/<slug>/
    pt/readme.md
    en/readme.md
    code/                 # optional; load data via ../../../data/
    references.md
  project/
    references.md
  materials/              # gitignored except README.md
```

Current courses: `ft108a-machine-learning` (Python when code exists), `ft105a-information-visualization` (R/Quarto when code exists).


## Python environment, data, and deliveries

Prefer one shared toolchain. Do not multiply virtualenvs or copy the same CSV into every exercise.

### Repo-global (shared)

- Package manager: **uv**. Source of truth: root `pyproject.toml` + `uv.lock`.
- Put the only Python virtualenv at the repository root: `.venv/` (created by `uv sync`).
- Default install: `uv sync` (course stack + `dev` group with Ruff; no Manim).
- Manim (optional, heavy): `uv sync --group manim` into the **same** root `.venv`. Never create a second venv for notes or Manim.
- Activate from the repo root: `source .venv/bin/activate` (or `uv run …`).
- Jupyter kernel name: `masters-curriculum` (see `env/README.md`).
- Do not add `env/requirements.txt`. Edit `pyproject.toml`, run `uv sync`, commit `uv.lock`.

### Per course

- `courses/<code>-<slug>/data/` — canonical datasets for that course (example: `liver.csv` for FT108A).
- `courses/<code>-<slug>/entregas/` — local submission ZIP/PDF artifacts. Gitignore the binaries; keep a short README.
- Exercise code must load data with a relative path to the course `data/` folder (from `exercises/<slug>/code/`: `../../../data/<file>`). Prefer a symlink in `code/` only when a legacy notebook expects a local filename.

### Do not

- Create `.venv` under `courses/`, `exercises/*/code/`, or `notes/`.
- Duplicate datasets across exercises or notes.
- Store delivery ZIPs permanently inside `code/` (move them to that course `entregas/`).
- Commit virtualenvs, generated `partitions/` splits (unless the user asks), or delivery binaries.

### Regenerating plots / Manim

Study notes under `notes/` use the repo-root `.venv`. Document the activate command in the note README. Prefer Manim for didactic animations when the student asks; otherwise matplotlib static figures are fine as a fallback.

When you add or update Manim scenes:

1. Render and copy every scene the note links (use that note's `render_all.sh` when it exists).
2. Put deliverable `.mp4` / `.png` under the path the markdown embeds (for example `figures/manim/`). Do not leave assets only under gitignored `media/`.
3. Extract PNG thumbnails from a mid-clip frame (about 45% of duration). Do not grab the final frame — Manim fades often end black.
4. Before you call the note done, confirm every embedded path exists on disk (`ls` the target files).

## Markdown notes: math and media

In study notes and other tracked markdown that the student reads in the editor, deliver formulas, images, and videos so the **classic** VS Code markdown preview renders them (`Markdown: Open Preview to the Side` / `Cmd+Shift+V` / `Ctrl+Shift+V`). Cursor's native `Preview | Markdown` panel does not render KaTeX, images, or HTML video yet — do not rely on it.

### Math (KaTeX)

- Inline: `$...$`
- Display: `$$` on its own lines around the formula
- Do **not** use LaTeX delimiters `\(...\)` or `\[...\]` in these notes — the classic preview expects `$` / `$$`

### Images

- Embed: `![short alt text](relative/path.png)`
- Do not use a bare link `[label](path.png)` when the intent is to show the image

### Videos

- Embed with HTML so the classic preview can play the file:

```html
<video src="relative/path.mp4" controls width="720"></video>
```

- Keep a PNG still (Manim thumb or static plot) next to the video when both exist
- Relative paths only, from the markdown file

### Checklist before done

- Every `$` / `$$` formula uses those delimiters
- Every image the reader should see uses `![...](...)`
- Every video uses a `<video>` tag with a path that exists
- Optional one-line note in the file if the student must use classic preview for math/media

## Git and secrets

Never stage:

- `admin/facts.md`
- `admin/documents/`
- `courses/*/materials/` except `README.md`
- `references/papers/` except `README.md`
- `.env`, virtualenvs (including any nested `.venv/`), `__pycache__`, `.RData`
- `courses/*/entregas/` binaries (ZIP/PDF); keep README/`.gitkeep` only

Tracked README files must not contain CPF, RG, address, phones, or personal emails. Program-level facts (name, advisor, course codes) belong in `README.md`.

Before `git add -A` or a commit, run `git status` and confirm ignored paths stay untracked. Do not commit unless the user asks.

## Language

- Course READMEs, notes, catalog, and this file: English.
- Exercise writeups: Portuguese in `pt/` and English in `en/`. Both must exist for each exercise.
- Do not duplicate code across `pt/` and `en/`. Put scripts in `code/`.

## Courses

Folder name: lowercase course code, hyphen, short English slug (`ft108a-machine-learning`).

To add a course:

1. Create the folder tree above.
2. Write a syllabus README (schedule, assessment formula, dated topic checklist, bibliography keys).
3. Add `references.md` with syllabus keys from `references/catalog.md`.
4. Add a row to `courses/README.md` and to the semester table in the root `README.md`.

Lecture slides and planos de ensino go in that course `materials/`. Git ignores those binaries. List expected filenames in `materials/README.md`.

## Exercises

Dash-case numbered folders: `01-preprocessing-basics/`.

Minimum files: `pt/readme.md`, `en/readme.md`, `references.md`. Add `code/` only when the exercise needs scripts.

### Follow the assignment exactly

Before you plan or write a submission, read the full prompt (including every ATTENTION / note). Build a checklist of required deliverables, methods, metrics, format rules, and explicit warnings. Map each item to the report or code. Do not skip an item because it seems minor. Do not invent extra work that the prompt does not ask for. Before you call the task done, re-check the checklist against the final PDF and ZIP.

### Assignment attribution

End every exercise writeup and submission report with an attribution line:

- **Portuguese** (`pt/readme.md`, Portuguese report body): *Conteúdo, experimentos e conclusões são meus; a formatação do texto teve assistência de IA.*
- **English** (`en/readme.md`): *Content, experiments, and conclusions are my own; the text's formatting had AI assistance.*

If the assignment has no experiments (for example, a reading essay), use *conteúdo e conclusões* / *content and conclusions* instead of *experimentos* / *experiments*.

Put the line at the end of the document. In Jupyter or Quarto reports, add it as the last paragraph of the final markdown cell.

### PDF reports with code output

Build submission PDFs from an **executed** notebook so stdout and figures appear in the PDF. Prefer `quarto render report.ipynb --to pdf` (Quarto executes the notebook). If Quarto is unavailable, run the notebook first, then export with `jupyter nbconvert --to markdown` and render with pandoc; do not render from a stale or unexecuted notebook.

### Submission PDF formatting (FT108A)

Unless the prompt states other rules, set the report PDF to:

- Font: Times New Roman or Calibri (body text)
- Font size: 12pt
- Line spacing: 1.15
- Margins: 2cm
- Paper: A4

Apply these in Quarto YAML (`mainfont`, `fontsize`, `linestretch`, `geometry`, `papersize: a4`) or in the pandoc fallback (`-V mainfont=...`, `-V fontsize=12pt`, `-V linestretch=1.15`, `-V geometry:margin=2cm`, `-V papersize=a4`). Monospace for code cells is fine. Before you call the task done, check the final PDF with `pdffonts` (Times/Calibri present) and `pdfinfo` (A4 page size). If the prompt adds more format rules, follow those too.

## References

`references/catalog.md` is the only full citation list. One section per source. Heading is the key.

Key form: `lastnameYYYY`. If two works collide, use `lastnameYYYY-shortword` (`wickham2023-r4ds`).

To add a source used in an exercise or project:

1. Add a catalog section (citation, type, DOI or URL, local file name, used-in).
2. Save the PDF as `references/papers/<key>.pdf` (local only).
3. List the key in the exercise or project `references.md` with one line that states why.
4. List the key in `courses/<course>/references.md`.

Do not copy the full citation into exercise or course pointer files. Do not commit paper PDFs.

## Code

- No `__init__.py`. This project targets Python 3.3+.
- Python (FT108A): format and lint with Ruff. Do not add comments that disable lint rules unless the user agrees.
- R (FT105A): scripts and Quarto in `code/`. Do not add `.Rproj` to git.
- Do not add a monorepo toolchain until the first real exercise needs it.

## Prose

Write READMEs and notes in STE-flavored English: active voice, short sentences, one name per thing. No marketing adjectives.

## Teaching (chat and guided notebooks)

This student is often rusty on NumPy, linear algebra, and ML. Prefer **high scaffolding**. Frustration is a signal to chew more, not to speed up.

When you explain NumPy or ML ideas (chat or exercise notebooks):

- Prefer short **phase / role** analogies: what question each piece answers.
- Use a small table when two ideas look similar (example: forward vs backward).

  | Phase | Question | Tool |
  | --- | --- | --- |
  | Forward | What is this neuron's output? | $\sigma(z)$ |
  | Backward | If I nudge $z$ a little, how much does the output change? | $\sigma'(z)=a(1-a)$ |

- Put one concrete numeric example next to a new formula when it helps.
- Keep the math. The analogy sits beside the formula; it does not replace it.
- Reuse this pattern in later sections of the same notebook (standardize, loss vs error, SGD, train/test) so the student sees the same teaching move again.

### Scaffolding level (default for FT108A notebooks)

- One idea per cell block. Do not stack three new NumPy tricks in one TODO.
- Show a **tiny worked example** (2–3 rows) before the real dataset.
- Give a **recipe** (numbered steps) and a **shape line** (`input → output`).
- In hard sections (forward, loss, backward): leave **empty TODOs** with Portuguese step comments and shapes. Do **not** paste a full working solution unless the student asks or is stuck after a real attempt.
- Prefer fill-in blanks (`z1 = ...  # (n, H)`) over finished functions.
- In chat: if stuck, give the **next line** (or one step), not the whole function. Walk end-to-end only when they ask.
- Optional Manim / visuals never block the graded path. Say that out loud when the student is overloaded.

## Commits

Create a commit only when the user asks. Do not amend unless the user asks and the amend rules in the user profile apply. Do not push unless the user asks. Do not skip hooks. Do not force-push.
