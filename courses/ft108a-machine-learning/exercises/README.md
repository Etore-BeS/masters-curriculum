# Exercises

Bilingual exercise writeups for FT108A. Each exercise gets its own folder.

## Layout

```
exercises/
  <exercise-slug>/
    pt/
      readme.md    # problem statement and solution notes (Portuguese)
    en/
      readme.md    # problem statement and solution notes (English)
    code/          # shared implementation (optional, add when needed)
    references.md  # catalog keys used in this exercise
```

## Rules

- Write the problem statement and your solution notes in both `pt/` and `en/`.
- Put code once in `code/` when an exercise needs it. Do not duplicate scripts across language folders.
- Use dash-case folder names (e.g., `01-preprocessing-basics/`).
- Number exercises when order matters: `01-slug/`, `02-slug/`.
- List catalog keys in `references.md`. Add the full record once in [catalog.md](../../../references/catalog.md). Also add the key to the [course references](../references.md).

## Source material

The exercise list PDF lives in [materials/](../materials/). See `lista_de_exercicios_-_v2015-11-16_-_com_algumas_respostas_2015-11-26.pdf`.

- [01-preprocessing-jurimetria-tjsp](01-preprocessing-jurimetria-tjsp/) — Topic 2 assignment on Domingos's "A Few Useful Things to Know about Machine Learning" and a jurimetrics case study (TJSP appeal outcome prediction via CNJ's DataJud API).
- [02-decision-trees-wine](02-decision-trees-wine/) — Assignment 1: CART decision tree on the UCI Wine data set (two 80/20 splits, train/test errors, comparison with ID3 from class).
- [03-naive-bayes-knn-ensembles-liver](03-naive-bayes-knn-ensembles-liver/) — Assignment 2: decision tree, Naïve Bayes, k-NN, and majority-vote ensemble on the UCI BUPA Liver Disorders data set (five 70/30 splits, mean test error).

- [04-mlp-liver](04-mlp-liver/) — Assignment 3: from-scratch MLP (+ library comparison) on BUPA Liver Disorders (five 70/30 splits).
