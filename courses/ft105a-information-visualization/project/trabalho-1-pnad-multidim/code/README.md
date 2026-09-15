# Code — Trabalho 1 PNAD

## Official graded trio

1. Bubble scatter (UF informality × income)
2. Heatmap small-multiples (unemployment)
3. Sankey (labour force 25–49) — design for a clear static/default frame

Delivery is a **static** GRIVAPP PDF; interactive menus are optional polish, not the narrative dependency.

## Notebooks (source of truth)

| Notebook | Authors | Role |
| --- | --- | --- |
| `pnad_analise_ponderada.ipynb` | Raphael Pizzi | Official weighted trio |
| `pnad_trabalho1_relatorio.ipynb` | Étore Braga e Santos, Raphael Pizzi, Saulo Celson Bergantini Dias | Final academic report (trio + Appendix) |
| `pnad_dataviz.ipynb` | (exploratory) | Parallel / treemap / pixels / SPLOM / parallel sets / RadViz — **appendix / exploration only** |

Weighted + report notebooks need the extract from `05_prepare_extrato.py` (`../../../data/processed/pnadc_2026q2_extrato.parquet`, gitignored).

Scripts 01–05: reprocess microdata only. HTML under `output/` is optional exploration and does not replace the notebooks.
