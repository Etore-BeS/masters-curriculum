# Trabalho 1 — status (EN)

## Official graded trio (locked)

Three distinct techniques for the graded delivery (static GRIVAPP PDF):

1. **Bubble scatter** — informality × income by UF
2. **Heatmap small-multiples** — unemployment by age, sex and colour/race
3. **Sankey** — labour-force participation ages 25–49, with a clear default/static frame

Weighted analysis source: `code/pnad_analise_ponderada.ipynb` (**author: Raphael Pizzi**).

Final academic report notebook (GRIVAPP content outline): `code/pnad_trabalho1_relatorio.ipynb` (**Étore, Raphael, Saulo**).

Draft DOCX techniques (parallel coordinates, treemap, pixel matrix) and other plots in `pnad_dataviz.ipynb` / `code/output/` HTML are **exploration / appendix only** — not the official graded set.

Delivery is **static** (PDF): main figures must read well in a fixed frame; do not rely on interactive filters for the main narrative.

## Scaffold status

- `PNADC_022026.zip` (2026 Q2) downloaded — no quarter fallback needed.
- Dictionary zip present; SAS input used for fixed-width positions.
- Python pipeline: download → FWF import → sample → exploratory Plotly HTML → weighted extract.
- Group draft DOCX at `docs/rascunho-grivapp.docx`.

## Notebooks

- `code/pnad_dataviz.ipynb` — six techniques over the 50k sample (exploration / appendix).
- `code/pnad_analise_ponderada.ipynb` — official trio over the full quarter with sampling weight (**Raphael Pizzi**).
- `code/pnad_trabalho1_relatorio.ipynb` — academic InfoVis report (trio + appendix; all three authors).

The weighted notebook and the report need the 63-column extract (`code/05_prepare_extrato.py`). Rates/means/medians weighted by `V1028`; totals match IBGE 2026Q2: unemployment 5.4%, informality 37.4%, mean usual income R$ 3,738.

## Enunciado checklist

- [x] Microdata + dictionary obtained
- [x] Python preprocessing pipeline
- [x] Exploration (parallel / treemap / pixels etc.)
- [x] Official weighted trio defined
- [ ] Write the **3 insights** with justification in the report / PDF (text + static figures)
- [ ] Final report in **GRIVAPP 2027** format (static PDF)
- [ ] Deliver by **2026-09-24**

## How to run

See `../README.md`. Activate the repo-root `.venv` and run `code/01`…`05`.

## Still for the group

1. Run the final report notebook after generating the extrato; export static PNGs of the official trio.
2. Build the GRIVAPP PDF from the report notebook and place it under `entregas/`.
