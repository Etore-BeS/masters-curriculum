---
title: "Tarefa 2: Naïve Bayes, k-NN e Ensembles — Liver Disorder"
author: "Étore Braga e Santos"
date: "2026-08-28"
format:
  pdf:
    pdf-engine: xelatex
    documentclass: article
    mainfont: Times New Roman
    fontsize: 12pt
    linestretch: 1.15
    geometry:
      - margin=2cm
    latex-auto-mk: true
    keep-tex: true
jupyter: python3
---

# Tarefa 2: Naïve Bayes, k-NN e Ensembles

**Curso:** FT108A — Introdução ao Aprendizado de Máquina, 2026S2.

Este relatório aplica árvore de decisão, Naïve Bayes e k-NN ao conjunto BUPA Liver Disorders (345 instâncias). Em cada uma de cinco repetições, os três classificadores treinam na mesma partição 70/30; um ensemble por voto majoritário avalia o mesmo teste. O texto é sucinto.


## 1. Ferramenta e algoritmos

A ferramenta é o scikit-learn (PEDREGOSA et al., 2011), executado em um notebook Jupyter.

| Algoritmo | Classe scikit-learn |
| --- | --- |
| Árvore de decisão | `DecisionTreeClassifier` |
| Naïve Bayes | `GaussianNB` |
| k-NN | `KNeighborsClassifier` |

O ensemble combina as predições dos três modelos já treinados em cada repetição, por voto majoritário (HAN; KAMBER, 2006).


## 2. Dados e definição do alvo

O conjunto BUPA Liver Disorders vem do repositório UCI (FORSYTH, 1990). Há cinco exames sanguíneos (`mcv`, `alkphos`, `sgpt`, `sgot`, `gammagt`) e o campo `drinks` (meia-caneca equivalente por dia). O arquivo `liver.csv` está no mesmo diretório deste notebook.

A documentação UCI alerta que o campo `selector` **não** é um rótulo de doença hepática: é um indicador de treino/teste criado pelos pesquisadores BUPA. Para classificação, a literatura recomenda dicotomizar `drinks` (TURNEY, 1995):

- classe `0` (`heavy_drinker = 0`): `drinks < 3`;
- classe `1` (`heavy_drinker = 1`): `drinks ≥ 3`.

As features são só os cinco exames; `drinks` bruto e `selector` não entram no treino.


## 3. Parâmetros dos classificadores

| Modelo | Parâmetros |
| --- | --- |
| Árvore de decisão | `criterion="entropy"`, `random_state=0` |
| Naïve Bayes | `GaussianNB()` — defaults (`var_smoothing=1e-9`); Gaussiano para atributos contínuos |
| k-NN | `n_neighbors=5`, `weights="uniform"`, `metric="minkowski"`, `p=2` (distância Euclidiana) |

O enunciado pede os parâmetros definidos; não houve busca de hiperparâmetros.


## 4. Protocolo experimental

- Cinco repetições com sementes `42`, `7`, `13`, `21` e `99`.
- Partição aleatória estratificada: 70% treino, 30% teste (`test_size=0.3`, `stratify=heavy_drinker`).
- Em cada repetição, a amostragem ocorre **antes** do treino; os três algoritmos usam os mesmos conjuntos.
- Métrica: erro de classificação no teste (1 − acurácia).
- Ensemble: moda das três predições no teste, sem re-treinar.



```python
from experiment import load_data, run_experiments

features, labels = load_data()
results, means = run_experiments(features, labels)

display_cols = ["seed", "tree", "nb", "knn", "ensemble"]
print(results[display_cols].to_string(index=False, float_format=lambda value: f"{value:.4f}"))

```

     seed   tree     nb    knn  ensemble
       42 0.3942 0.3942 0.3654    0.3750
        7 0.4904 0.4038 0.3846    0.4423
       13 0.3942 0.3750 0.4327    0.3942
       21 0.4135 0.4904 0.5288    0.4808
       99 0.4712 0.5096 0.5000    0.4904


## 5. Erros médios no teste

A tabela acima lista cada repetição. A linha de médias resume o desempenho pedido no enunciado.



```python
print("Erro medio:")
print(means.to_string(float_format=lambda value: f"{value:.4f}"))

```

    Erro medio:
    tree       0.4327
    nb         0.4346
    knn        0.4423
    ensemble   0.4365


## 6. Ensemble

O voto majoritário escolhe, para cada instância de teste, a classe mais votada entre árvore, Naïve Bayes e k-NN. Empates 1–1 favorecem a classe de índice menor no `bincount` (ver `experiment.py`).

O erro médio do ensemble situa-se entre os três modelos base. A combinação não supera claramente o melhor classificador isolado neste protocolo, mas estabiliza repetições em que um modelo erra mais.


## Referências

- FORSYTH, R. S. BUPA Liver Disorders. UCI Machine Learning Repository, 1990.
- HAN, J.; KAMBER, M. *Data Mining: Concepts and Techniques*. Elsevier, 2006.
- PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. *JMLR*, 2011.
- TURNEY, P. D. Cost-Sensitive Classification. *JAIR*, 1995.

