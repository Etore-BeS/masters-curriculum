# Trabalho 1 — PNAD Contínua multidimensional visualization

| Field | Value |
| --- | --- |
| Course | FT105A InfoVis |
| Due | 2026-09-24 |
| Authors (draft) | Étore Braga e Santos, Raphael Pizzi, Saulo Celson Bergantini Dias |
| Stack | Python (repo-root `.venv`) + Plotly interactive HTML |
| Data | PNAD Contínua microdados 2º trimestre 2026 (`PNADC_022026.zip`) |

## Assignment checklist (from enunciado)

- [x] Access PNAD Contínua site / microdata downloads (URLs in `code/01_download.py`)
- [x] Obtain `PNADC_022026.zip` (2T/2026) — confirmed on IBGE FTP
- [x] Obtain `Dicionario_e_input_20221031.zip` (Documentação)
- [ ] Propose **3 interactive** multidimensional visualizations, **3 distinct techniques**, each with **>3 variables**
- [ ] For each insight: justification with viz image(s) + text (**student writes the 3 informações**)
- [ ] Report in **GRIVAPP 2027** format (Word/LaTeX template later): Intro, PNAD, Techniques, Tools, Preprocessing, Findings, Conclusion
- [ ] Deliver by **24/09/2026**

Draft techniques (from group DOCX): **Parallel Coordinates**, **Treemap**, **Pixel matrix**.

## Paths

| Path | Role |
| --- | --- |
| `../../../data/raw/` | Zips + extracted fixed-width TXT (gitignored) |
| `../../../data/processed/` | Selected parquet + sample CSV/parquet + codebook (gitignored) |
| `code/` | Download → import → sample → exploratory viz |
| `code/output/` | Exploratory Plotly HTML (scaffold) |
| `docs/` | Enunciado, GRIVAPP instructions, rascunho DOCX |
| `../../../materials/` | Course materials copies (gitignored binaries) |
| `../../../entregas/` | Final submission ZIP/PDF (local only) |

## How to run

From the repository root (uses shared `.venv`):

```bash
cd courses/ft105a-information-visualization/project/trabalho-1-pnad-multidim/code
source ../../../../../.venv/bin/activate   # or: uv run from repo root
python 01_download.py
python 02_import_pnadc.py      # ~few minutes; reads 1.7G FWF
python 03_prepare_sample.py    # writes ~50k-row sample
python 04_explore_viz.py       # writes HTML under output/
```

Or with `uv` from repo root:

```bash
uv run python courses/ft105a-information-visualization/project/trabalho-1-pnad-multidim/code/02_import_pnadc.py
```

Dependencies: `pandas`, `pyarrow`, `plotly`, `numpy` (plus `openpyxl`/`xlrd` if you open the XLS dictionary).

## Exploratory outputs (not the graded submission)

Open in a browser:

- `code/output/01_parallel_coordinates.html`
- `code/output/02_treemap.html`
- `code/output/03_pixel_matrix.html`

Titles are prefixed **EXPLORATORY — scaffold**. Replace / refine encodings after analysis. Final report needs interactive viz evidence and written insights.

## Still for the student

1. Write the **3 informações** (findings) with convincing justifications — do not invent them in scaffold docs.
2. Polish interactivity and visual encodings for submission-quality Plotly (or equivalent Python) HTML.
3. Produce the **GRIVAPP 2027** camera-ready PDF (English) from the Word/LaTeX template; Quarto/Jupyter here is only a content outline.
4. Package delivery into `entregas/` by the due date.

## Attribution note

Scaffold/pipeline setup had AI assistance. Content, analysis, and conclusions for the graded report are the group's responsibility.
