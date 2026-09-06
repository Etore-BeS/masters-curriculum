# FT108A canonical datasets

Keep datasets here. Do not duplicate CSV files into exercise `code/` folders.

## liver.csv

BUPA Liver Disorders (UCI). Canonical copy for FT108A exercises that use this data set.

From an exercise `code/` directory, load with a relative path:

```python
df = pd.read_csv("../../../data/liver.csv")
```

Exercise 03 keeps a symlink at `exercises/03-naive-bayes-knn-ensembles-liver/code/liver.csv` → `../../../data/liver.csv` so older notebooks that open `liver.csv` in the same directory still work.

Do not copy `liver.csv` into new exercises; use the relative path (or a symlink if a local filename is required).
