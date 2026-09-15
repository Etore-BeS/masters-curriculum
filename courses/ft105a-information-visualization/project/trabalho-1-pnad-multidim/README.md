# Trabalho 1 — PNAD Contínua multidimensional visualization

| Field | Value |
| --- | --- |
| Course | FT105A InfoVis |
| Due | 2026-09-24 |
| Authors | Étore Braga e Santos, Raphael Pizzi, Saulo Celson Bergantini Dias |
| Stack | Python (repo-root `.venv`) + Plotly (figures designed for **static** PDF/GRIVAPP) |
| Data | PNAD Contínua microdados 2º trimestre 2026 (`PNADC_022026.zip`) |
| Delivery | **Static** camera-ready PDF (GRIVAPP 2027); interactive filters are not required for the main narrative |

## Official graded trio (locked)

Three distinct techniques, each with >3 mapped variables, for the graded delivery:

1. **Bubble scatter** — UF informality × income (area = employed; colour = region)
2. **Heatmap small-multiples** — unemployment by age × sex × colour/race (panels: Brasil + regions)
3. **Sankey** — labour-force participation ages 25–49 (sex → young child at home → labour status); use a **clear default/static frame** (all schooling levels)

Source of the graded analysis: `code/pnad_analise_ponderada.ipynb` (author: **Raphael Pizzi**).

Final academic report notebook (content outline for the GRIVAPP PDF): `code/pnad_trabalho1_relatorio.ipynb` (authors: all three group members) — created on `main` after merge.

## Assignment checklist (from enunciado)

- [x] Access PNAD Contínua site / microdata downloads (URLs in `code/01_download.py`)
- [x] Obtain `PNADC_022026.zip` (2T/2026) — confirmed on IBGE FTP
- [x] Obtain `Dicionario_e_input_20221031.zip` (Documentação)
- [x] Propose **3** multidimensional visualizations, **3 distinct techniques**, each with **>3 variables** — official trio above
- [ ] For each insight: justification with viz image(s) + text (in the final report notebook / GRIVAPP PDF)
- [ ] Report in **GRIVAPP 2027** format (static PDF): Intro, PNAD, Techniques, Tools, Preprocessing, Findings, Conclusion + Appendix
- [ ] Deliver by **24/09/2026**

## Exploration only (not the graded trio)

Draft techniques from the group DOCX — **parallel coordinates**, **treemap**, **pixel matrix** — plus SPLOM / parallel sets / RadViz in `code/pnad_dataviz.ipynb` and HTML under `code/output/`. These stay as **exploratory / appendix** material only; they are not the official graded set.

## Notebooks

| Notebook | Authors (of that file) | Scope |
| --- | --- | --- |
| `code/pnad_dataviz.ipynb` | (exploratory support) | Six techniques over a 50k sample |
| `code/pnad_analise_ponderada.ipynb` | **Raphael Pizzi** | Official trio over the full quarter, weighted by `V1028` |
| `code/pnad_trabalho1_relatorio.ipynb` | Étore, Raphael, Saulo | Final academic InfoVis report outline (main trio + Appendix) |

The weighted notebook needs the wide extract, which is not in the repository. Generate it with `code/05_prepare_extrato.py` before running it. All rates, means and medians there are weighted by `V1028`; totals match the IBGE release for 2026Q2 (unemployment 5.4%, informality 37.4%, mean usual income R$ 3,738).

## Paths

| Path | Role |
| --- | --- |
| `../../../data/raw/` | Zips + extracted fixed-width TXT (gitignored) |
| `../../../data/processed/` | Selected parquet + sample + extrato (gitignored) |
| `code/` | Download → import → sample → exploratory viz → wide extract → notebooks |
| `code/output/` | Exploratory Plotly HTML (scaffold; not graded) |
| `entregas/figures/` or `code/output/figures/` | Static PNG exports for the PDF |
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
python 04_explore_viz.py       # writes HTML under output/ (exploration)
python 05_prepare_extrato.py   # ~few minutes; 63-column extract for weighted / report notebooks
```

Or with `uv` from repo root:

```bash
uv run python courses/ft105a-information-visualization/project/trabalho-1-pnad-multidim/code/02_import_pnadc.py
```

Dependencies: `pandas`, `pyarrow`, `plotly`, `numpy` (plus `kaleido` for static PNG export if available; `openpyxl`/`xlrd` if you open the XLS dictionary).

## Still for the group

1. Run the final report notebook after generating the extrato; export static PNGs of the official trio.
2. Produce the **GRIVAPP 2027** camera-ready PDF (English) from the Word/LaTeX template using that notebook as content source.
3. Package delivery into `entregas/` by the due date.

## Attribution note

Scaffold/pipeline setup had AI assistance. Graded analysis in `pnad_analise_ponderada.ipynb` is authored by Raphael Pizzi. Content, analysis, and conclusions for the graded report are the group's responsibility.
