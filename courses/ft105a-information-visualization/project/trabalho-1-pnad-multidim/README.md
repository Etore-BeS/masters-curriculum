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
- [x] Propose **3 interactive** multidimensional visualizations, **3 distinct techniques**, each with **>3 variables** — bubble scatter, small-multiples heatmap and Sankey, in `code/pnad_analise_ponderada.ipynb`
- [ ] For each insight: justification with viz image(s) + text (**student writes the 3 informações**)
- [ ] Report in **GRIVAPP 2027** format (Word/LaTeX template later): Intro, PNAD, Techniques, Tools, Preprocessing, Findings, Conclusion
- [ ] Deliver by **24/09/2026**

Draft techniques (from group DOCX): **Parallel Coordinates**, **Treemap**, **Pixel matrix**.

## Notebooks

| Notebook | Scope |
| --- | --- |
| `code/pnad_dataviz.ipynb` | Six techniques over a 50k sample (sections 1-6) |
| `code/pnad_analise_ponderada.ipynb` | Three techniques over the full quarter with the sampling weight (sections 7-9) |

The second notebook needs the wide extract, which is not in the repository. Generate it with `code/05_prepare_extrato.py` before running it. All rates, means and medians there are weighted by `V1028`; totals match the IBGE release for 2026Q2 (unemployment 5.4%, informality 37.4%, mean usual income R$ 3,738).

## Paths

| Path | Role |
| --- | --- |
| `../../../data/raw/` | Zips + extracted fixed-width TXT (gitignored) |
| `../../../data/processed/` | Selected parquet + sample CSV/parquet + codebook (gitignored) |
| `code/` | Download → import → sample → exploratory viz → wide extract |
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
python 05_prepare_extrato.py   # ~few minutes; 63-column extract for the weighted notebook
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

1. Move the three findings from `code/pnad_analise_ponderada.ipynb` into the report, with the figures.
2. Polish interactivity and visual encodings for submission-quality Plotly (or equivalent Python) HTML.
3. Produce the **GRIVAPP 2027** camera-ready PDF (English) from the Word/LaTeX template; Quarto/Jupyter here is only a content outline.
4. Package delivery into `entregas/` by the due date.

## Attribution note

Scaffold/pipeline setup had AI assistance. Content, analysis, and conclusions for the graded report are the group's responsibility.
