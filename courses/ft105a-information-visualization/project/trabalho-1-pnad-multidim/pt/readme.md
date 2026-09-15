# Trabalho 1 — status (PT)

## Decisão do trio oficial (entrega)

Três técnicas distintas para a entrega avaliada (PDF estático GRIVAPP):

1. **Dispersão com bolhas** — informalidade × renda por UF
2. **Mapa de calor em pequenos múltiplos** — desocupação por idade, sexo e cor
3. **Sankey** — participação na força de trabalho (25–49 anos), com quadro estático/padrão legível

Fonte da análise ponderada: `code/pnad_analise_ponderada.ipynb` (**autor: Raphael Pizzi**).

Relatório acadêmico final (esboço de conteúdo GRIVAPP): `code/pnad_trabalho1_relatorio.ipynb` (**Étore, Raphael, Saulo**).

Técnicas do rascunho DOCX (coordenadas paralelas, treemap, matriz de pixels) e demais figuras de `pnad_dataviz.ipynb` / HTML em `code/output/` ficam só como **exploração / apêndice** — não são o trio oficial.

A entrega é **estática** (PDF): as figuras principais devem ler bem em um quadro fixo; não depender de filtros interativos para a narrativa.

## Estado do scaffold

- Dados `PNADC_022026.zip` (2º trim. 2026) baixados — **não** foi necessário fallback de trimestre.
- Dicionário `Dicionario_e_input_20221031.zip` baixado e input SAS disponível.
- Pipeline Python: download → import FWF → amostra → HTML exploratórios (Plotly) → extrato ponderado.
- Rascunho DOCX do grupo em `docs/rascunho-grivapp.docx`.

## Notebooks

- `code/pnad_dataviz.ipynb` — seis técnicas sobre a amostra de 50 mil (exploração / apêndice).
- `code/pnad_analise_ponderada.ipynb` — trio oficial sobre o trimestre inteiro com peso amostral (**Raphael Pizzi**).
- `code/pnad_trabalho1_relatorio.ipynb` — relatório InfoVis acadêmico (trio + apêndice; os três autores).

O notebook ponderado e o relatório precisam do extrato de 63 colunas (`code/05_prepare_extrato.py`). Taxas/médias/medianas ponderadas por `V1028`; totais alinhados ao release IBGE 2º tri/2026: desocupação 5,4%, informalidade 37,4%, rendimento médio habitual R$ 3.738.

## Checklist do enunciado

- [x] Microdados + dicionário obtidos
- [x] Pipeline de pré-processamento Python
- [x] Exploração (paralelas / treemap / pixels etc.)
- [x] Trio oficial com peso amostral definido
- [ ] Redigir as **3 informações** com justificativa no relatório / PDF (texto + figuras estáticas)
- [ ] Relatório final no formato **GRIVAPP 2027** (PDF estático)
- [ ] Entrega em **24/09/2026**

## Como rodar

Ver `../README.md`. Ativar `.venv` na raiz e executar `code/01`…`05`.

## Ainda falta (grupo)

1. Rodar o relatório final após gerar o extrato; exportar PNGs estáticos do trio.
2. Montar PDF GRIVAPP a partir do notebook de relatório e colocar em `entregas/`.
