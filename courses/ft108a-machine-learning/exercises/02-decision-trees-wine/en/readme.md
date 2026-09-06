# Assignment 1: Decision Trees, Wine

**Prompt:** choose a software tool that offers a decision tree algorithm and apply it to the Wine data set from the UCI repository (178 samples, 3 classes). Split 80% of the samples for training and 20% for testing, at random, with all three classes in the test set. Present the tree and the classification errors on training and test. Repeat with a new split and comment on whether the errors were identical. Discuss how the algorithm in the tool differs from the algorithm covered in class. Deliver a PDF and the tool data file in one ZIP.

## Solution

Tool: scikit-learn in a Jupyter notebook. Algorithm: `DecisionTreeClassifier` with `criterion="entropy"` (binary CART, information gain). No pruning.

The submission report is [code/report.ipynb](../code/report.ipynb). Quarto builds the PDF from that notebook. The data file is [code/wine.csv](../code/wine.csv).

### Splits

Two stratified 80/20 splits, seeds 42 and 7. Stratification keeps classes 1, 2, and 3 in the test set. The classifier uses `random_state=0` in both runs, so the split is the only change.

### Errors

Training and test errors are not the same across the two splits. Induction is greedy: a new training set yields new cuts. The test set has about 36 samples, so the error estimate moves. The lecture asks for repeated splits and a mean score.

### Class versus tool

The lecture computed information gain for ID3 and named CART and C4.5. Wine has only continuous attributes. For those attributes the lecture already describes a binary cut, and scikit-learn CART does the same. Differences: CART does not open one branch per discrete value; scikit-learn defaults to Gini (this report forces entropy); this experiment does not apply C4.5 pruning.

## How to build the PDF

From the repository root, then in `code/`:

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

*Content, experiments, and conclusions are my own; the text's formatting had AI assistance.*
