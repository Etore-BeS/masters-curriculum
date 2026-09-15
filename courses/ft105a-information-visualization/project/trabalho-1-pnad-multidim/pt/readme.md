# Trabalho 1 — status (PT)

## Estado do scaffold

- Dados `PNADC_022026.zip` (2º trim. 2026) baixados — **não** foi necessário fallback de trimestre.
- Dicionário `Dicionario_e_input_20221031.zip` baixado e input SAS disponível.
- Pipeline Python: download → import FWF → amostra → 3 HTML exploratórios (Plotly).
- Rascunho DOCX do grupo em `docs/rascunho-grivapp.docx`.
- Técnicas do rascunho: coordenadas paralelas, treemap, matriz de pixels.

## Notebooks

- `code/pnad_dataviz.ipynb` — seis técnicas sobre a amostra de 50 mil registros (seções 1 a 6).
- `code/pnad_analise_ponderada.ipynb` — três técnicas sobre o trimestre inteiro com peso amostral (seções 7 a 9): dispersão com bolhas, mapa de calor em pequenos múltiplos e Sankey.

O segundo precisa do extrato de 63 colunas, que não vai para o repositório. Gere antes com `code/05_prepare_extrato.py`. Tudo que é taxa, média ou mediana ali é ponderado por `V1028` e fecha com o release do IBGE do 2º tri/2026: desocupação 5,4%, informalidade 37,4%, rendimento médio habitual R$ 3.738.

## Checklist do enunciado

- [x] Microdados + dicionário obtidos
- [x] Pipeline de pré-processamento Python
- [x] Três visualizações exploratórias (técnicas distintas, >3 variáveis)
- [x] Três visualizações propostas para a entrega, com peso amostral
- [ ] Redigir as **3 informações** com justificativa (texto + figuras)
- [ ] Relatório final no formato **GRIVAPP 2027** (PDF)
- [ ] Entrega em **24/09/2026**

## Como rodar

Ver `../README.md` (inglês STE). Ativar `.venv` na raiz do repositório e executar `code/01`…`04`, mais `code/05_prepare_extrato.py` para o notebook ponderado.

## Ainda falta (grupo)

1. Levar as 3 informações do `pnad_analise_ponderada.ipynb` para o relatório, com as figuras.
2. Refinar visualizações interativas para a entrega.
3. Montar PDF GRIVAPP e colocar em `entregas/`.

Conteúdo, experimentos e conclusões são meus; a formatação do texto teve assistência de IA.
