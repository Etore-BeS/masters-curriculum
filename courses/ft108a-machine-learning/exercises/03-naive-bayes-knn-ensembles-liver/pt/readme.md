# Tarefa 2: Naïve Bayes, k-NN e Ensembles, Liver Disorder

**Enunciado:** escolher um pacote com árvores de decisão, Naïve Bayes e k-NN; aplicá-los ao conjunto Liver Disorder (UCI). Usar subamostragem aleatória com 5 repetições, divisão 70/30, mesmos dados por repetição para todos os algoritmos; reportar erro médio de classificação no teste. Em cada repetição, montar ensemble por voto majoritário sobre os classificadores já treinados e reportar desempenho médio. Documentar parâmetros e a definição do atributo alvo. Entregar PDF e arquivo de dados em um ZIP.

## Solução

Ferramenta: scikit-learn em notebook Jupyter. Algoritmos: `DecisionTreeClassifier` (`criterion="entropy"`, `random_state=0`), `GaussianNB()` (defaults), `KNeighborsClassifier(n_neighbors=5)`.

O relatório de entrega está em [code/report.ipynb](../code/report.ipynb). O Quarto gera o PDF a partir desse notebook. Os dados estão em [code/liver.csv](../code/liver.csv).

### Alvo

O campo `selector` não é rótulo de doença (UCI). Seguindo Turney (1995), o alvo binário `heavy_drinker` vale 1 quando `drinks ≥ 3` e 0 caso contrário. Features: cinco exames sanguíneos.

### Erros médios no teste (5 repetições)

| Modelo | Erro médio |
| --- | --- |
| Árvore de decisão | 0,4327 |
| Naïve Bayes | 0,4346 |
| k-NN | 0,4423 |
| Ensemble (voto majoritário) | 0,4365 |

### Ensemble

Em cada repetição, as três predições no teste são combinadas por moda. O ensemble não supera o melhor modelo isolado neste protocolo, mas reduz picos de erro em algumas sementes.

## Como gerar o PDF

Na raiz do repositório e depois em `code/`:

```bash
uv sync
source .venv/bin/activate
cd courses/ft108a-machine-learning/exercises/03-naive-bayes-knn-ensembles-liver/code
./render_pdf.sh
```

Fish:

```fish
uv sync
source .venv/bin/activate.fish
cd courses/ft108a-machine-learning/exercises/03-naive-bayes-knn-ensembles-liver/code
bash render_pdf.sh
```

O script executa o notebook antes de gerar o PDF, para a saída dos experimentos aparecer no relatório. Se Quarto estiver instalado, ele é usado; caso contrário, o fallback usa pandoc.

## Como montar o ZIP de entrega

No diretório `code/`, após gerar o PDF:

```bash
zip -j entrega-tarefa2-liver.zip report.pdf liver.csv
```

Fish:

```fish
zip -j entrega-tarefa2-liver.zip report.pdf liver.csv
```

*Conteúdo, experimentos e conclusões são meus; a formatação do texto teve assistência de IA.*
