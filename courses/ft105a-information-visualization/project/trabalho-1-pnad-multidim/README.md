# Trabalho 1 — PNAD Contínua (visualização multidimensional)

| | |
| --- | --- |
| Disciplina | FT105A InfoVis |
| Entrega | **24/09/2026** — PDF estático no formato [GRIVAPP 2027](https://grivapp.scitevents.org/Templates.aspx) |
| Grupo | Étore Braga e Santos, Raphael Pizzi, Saulo Celson Bergantini Dias |
| Stack | Python (`.venv` na raiz do repo) + Plotly |
| Dados | PNAD Contínua, 2º trimestre 2026 (`PNADC_022026.zip`) |

Repo no GitHub: [trabalho-1-pnad-multidim](https://github.com/Etore-BeS/masters-curriculum/tree/main/courses/ft105a-information-visualization/project/trabalho-1-pnad-multidim)

## Trio da entrega

Três técnicas distintas (>3 variáveis cada), pensadas para ler bem em PDF:

1. **Dispersão com bolhas** — informalidade × renda por UF  
2. **Heatmap em small multiples** — desocupação por idade × sexo × cor/raça  
3. **Sankey** — força de trabalho 25–49 (sexo → criança pequena em casa → situação); usar o quadro padrão (todas as escolaridades)

Análise ponderada (`V1028`): [`code/pnad_analise_ponderada.ipynb`](code/pnad_analise_ponderada.ipynb) — **Raphael Pizzi**.  
Notebook do relatório (trio + apêndice): [`code/pnad_trabalho1_relatorio.ipynb`](code/pnad_trabalho1_relatorio.ipynb) — os três autores.

Totais de checagem (IBGE 2026Q2): desocupação 5,4%; informalidade 37,4%; rendimento médio habitual R$ 3.738.

## Onde pegar o quê (montagem do PDF)

| O quê | Onde |
| --- | --- |
| Notebook do relatório + figs | [`code/pnad_trabalho1_relatorio.ipynb`](https://github.com/Etore-BeS/masters-curriculum/blob/main/courses/ft105a-information-visualization/project/trabalho-1-pnad-multidim/code/pnad_trabalho1_relatorio.ipynb) |
| Trio ponderado (detalhe) | [`code/pnad_analise_ponderada.ipynb`](https://github.com/Etore-BeS/masters-curriculum/blob/main/courses/ft105a-information-visualization/project/trabalho-1-pnad-multidim/code/pnad_analise_ponderada.ipynb) |
| PNGs estáticos (se já rodou local) | `entregas/figures/` ou `code/output/figures/` (gitignored) |
| Enunciado | [`docs/enunciado-trabalho-1.pdf`](docs/enunciado-trabalho-1.pdf) |
| Instruções / template GRIVAPP | [`docs/grivapp-2027-authors-instructions.pdf`](docs/grivapp-2027-authors-instructions.pdf) · [Templates GRIVAPP](https://grivapp.scitevents.org/Templates.aspx) |
| Rascunho do grupo | [`docs/rascunho-grivapp.docx`](docs/rascunho-grivapp.docx) |
| Status em PT | [`pt/readme.md`](pt/readme.md) |

Coordenadas paralelas / treemap / pixels (e outras em `pnad_dataviz.ipynb`) ficam no **apêndice** — não são o trio da entrega.

## Checklist

- [x] Microdados + dicionário
- [x] Pipeline Python (`01`…`05`)
- [x] Trio oficial + notebook de relatório
- [ ] Três informações com justificativa (texto + figuras) no PDF
- [ ] PDF GRIVAPP em inglês → `entregas/` até 24/09

## Como rodar

Na raiz do repo (`.venv` compartilhado):

```bash
cd courses/ft105a-information-visualization/project/trabalho-1-pnad-multidim/code
source ../../../../../.venv/bin/activate
python 01_download.py
python 02_import_pnadc.py
python 03_prepare_sample.py
python 04_explore_viz.py       # HTML exploratório opcional
python 05_prepare_extrato.py   # extrato 63 cols (gitignored) p/ ponderado + relatório
```

Dependências: `pandas`, `pyarrow`, `plotly`, `numpy`; `kaleido` ajuda no PNG estático.

## Pastas

| Path | Uso |
| --- | --- |
| `../../../data/raw/` · `processed/` | Zips / parquet (gitignored) |
| `code/` | Scripts + notebooks |
| `docs/` | Enunciado, GRIVAPP, rascunho |
| `../../../entregas/` | PDF/ZIP finais (local) |
