# Tarefa 1: Árvores de Decisão, Wine

**Enunciado:** escolher uma ferramenta com um algoritmo de árvore de decisão e aplicá-la ao conjunto Wine do repositório UCI (178 amostras, 3 classes). Separar 80% das amostras para treino e 20% para teste, de forma aleatória, com as três classes no teste. Apresentar a árvore e os erros de classificação em treino e teste. Repetir com uma nova partição e comentar se os erros foram idênticos. Discutir as diferenças entre o algoritmo da ferramenta e o visto em aula. Entregar PDF e o arquivo de dados da ferramenta em um ZIP.

## Solução

Ferramenta: scikit-learn em um notebook Jupyter. Algoritmo: `DecisionTreeClassifier` com `criterion="entropy"` (CART binário, ganho de informação). Sem poda.

O relatório de entrega está em [code/report.ipynb](../code/report.ipynb). O Quarto gera o PDF a partir desse notebook. Os dados estão em [code/wine.csv](../code/wine.csv).

### Partições

Dois splits estratificados 80/20, sementes 42 e 7. A estratificação garante as classes 1, 2 e 3 no teste. O classificador usa `random_state=0` nos dois experimentos, para isolar o efeito da partição.

### Erros

Os erros de treino e teste não são idênticos nas duas partições. A indução é gulosa: outro conjunto de treino muda os cortes. O teste tem cerca de 36 amostras, então a estimativa oscila. A aula recomenda repetir o split e olhar a média.

### Aula versus ferramenta

A aula calculou ganho de informação no ID3 e citou CART e C4.5. O Wine tem só atributos contínuos. Nesse caso a aula já descreve um corte binário, e o CART do scikit-learn faz o mesmo. Diferenças: CART não abre um ramo por valor discreto; a métrica padrão do scikit-learn é Gini (aqui forçada para entropia); não há poda C4.5 neste experimento.

## Como gerar o PDF

Na raiz do repositório e depois em `code/`:

```bash
uv sync
source .venv/bin/activate
cd courses/ft108a-machine-learning/exercises/02-decision-trees-wine/code
quarto render report.ipynb --to pdf
```

Fish:

```fish
uv sync
source .venv/bin/activate.fish
cd courses/ft108a-machine-learning/exercises/02-decision-trees-wine/code
quarto render report.ipynb --to pdf
```

*Conteúdo, experimentos e conclusões são meus; a formatação do texto teve assistência de IA.*
