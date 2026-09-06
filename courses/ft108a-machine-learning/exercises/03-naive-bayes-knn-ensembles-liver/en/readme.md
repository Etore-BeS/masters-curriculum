# Assignment 2: Naïve Bayes, k-NN, and Ensembles, Liver Disorder

**Prompt:** choose a package with decision trees, Naïve Bayes, and k-NN; apply them to the UCI Liver Disorder data set. Use random subsampling with 5 repetitions, a 70/30 train/test split, and the same data per repetition for all algorithms; report mean test classification error. In each repetition, build a majority-vote ensemble from the already trained classifiers and report mean performance. Document parameters and the target definition. Deliver a PDF and the tool data file in one ZIP.

## Solution

Tool: scikit-learn in a Jupyter notebook. Algorithms: `DecisionTreeClassifier` (`criterion="entropy"`, `random_state=0`), `GaussianNB()` (defaults), `KNeighborsClassifier(n_neighbors=5)`.

The submission report is [code/report.ipynb](../code/report.ipynb). Quarto builds the PDF from that notebook. The data file is [code/liver.csv](../code/liver.csv).

### Target

The `selector` field is not a disease label (UCI). Following Turney (1995), the binary target `heavy_drinker` is 1 when `drinks ≥ 3` and 0 otherwise. Features: five blood tests.

### Mean test errors (5 repetitions)

| Model | Mean error |
| --- | --- |
| Decision tree | 0.4327 |
| Naïve Bayes | 0.4346 |
| k-NN | 0.4423 |
| Ensemble (majority vote) | 0.4365 |

### Ensemble

Each repetition combines the three test predictions by mode. The ensemble does not beat the best single model in this protocol, but it dampens error spikes on some seeds.

## How to build the PDF

From the repository root, then in `code/`:

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

The script executes the notebook before building the PDF so experiment output appears in the report. Quarto is used when installed; otherwise pandoc is the fallback.

## How to build the submission ZIP

In the `code/` directory, after generating the PDF:

```bash
zip -j entrega-tarefa2-liver.zip report.pdf liver.csv
```

Fish:

```fish
zip -j entrega-tarefa2-liver.zip report.pdf liver.csv
```

*Content, experiments, and conclusions are my own; the text's formatting had AI assistance.*
