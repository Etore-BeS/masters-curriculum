# Trabalho 1 — status (EN)

## Scaffold status

- `PNADC_022026.zip` (2026 Q2) downloaded — no quarter fallback needed.
- Dictionary zip present; SAS input used for fixed-width positions.
- Python pipeline: download → FWF import → sample → 3 exploratory Plotly HTML files.
- Group draft DOCX at `docs/rascunho-grivapp.docx`.
- Draft techniques: parallel coordinates, treemap, pixel matrix.

## Notebooks

- `code/pnad_dataviz.ipynb` — six techniques over the 50k sample (sections 1-6).
- `code/pnad_analise_ponderada.ipynb` — three techniques over the full quarter with the sampling weight (sections 7-9): bubble scatter, small-multiples heatmap and Sankey.

The second one needs the 63-column extract, which is not in the repository. Generate it first with `code/05_prepare_extrato.py`. Every rate, mean and median there is weighted by `V1028` and matches the IBGE release for 2026Q2: unemployment 5.4%, informality 37.4%, mean usual income R$ 3,738.

## Enunciado checklist

- [x] Microdata + dictionary obtained
- [x] Python preprocessing pipeline
- [x] Three exploratory visualizations (distinct techniques, >3 variables each)
- [x] Three weighted visualizations proposed for the submission
- [ ] Write the **3 insights** with justification (text + figures)
- [ ] Final report in **GRIVAPP 2027** format (PDF)
- [ ] Deliver by **2026-09-24**

## How to run

See `../README.md`. Activate the repo-root `.venv` and run `code/01`…`04`, plus `code/05_prepare_extrato.py` for the weighted notebook.

## Still for the group

1. Move the three findings from `pnad_analise_ponderada.ipynb` into the report, with the figures.
2. Refine interactive visualizations for submission.
3. Build the GRIVAPP PDF and place it under `entregas/`.

Content, experiments, and conclusions are my own; the text's formatting had AI assistance.
