# Pré-processamento Assignment — FT108A, Topic 2

**Prompt:** based on Pedro Domingos's article, *A Few Useful Things to Know about Machine Learning* [domingos2012], (1) identify which of the twelve recommendations relate to preprocessing; (2) formulate a real machine learning problem, defining the target variable, the preprocessing needed, potential algorithms, the moment the prediction would be made in a real application, and the attributes actually available at that moment; (3) identify an attribute or procedure that could cause data leakage and explain why it produces an artificially optimistic estimate.

## 1. Recommendations related to preprocessing

Of the twelve lessons in the article, three connect directly to preprocessing:

**"It's generalization that counts"** (section 3). This is the lesson that underlies the very idea of separating training, test, and validation sets — a decision made during preprocessing, not in the choice of algorithm. It's also the conceptual root of data leakage: if that separation isn't done carefully (for instance, computing statistics over the whole dataset before splitting), the evaluation step stops meaning what it's supposed to mean.

**"Intuition fails in high dimensions"** (section 6). This is about how human cognition can't intuit the behavior of high-dimensional data, and how inference over that data tends to get more complex (the "curse of dimensionality" makes generalization exponentially harder as the number of attributes grows). Preprocessing connects here through dimensionality reduction — selecting or combining attributes to simplify what the model has to learn.

**"Feature engineering is the key"** (section 8). Figuring out which attributes actually matter to the model, and how to represent raw data so learning works, is preprocessing work — and Domingos calls it the single biggest factor in whether an ML project succeeds or fails.

Worth noting why section 2 ("Learning = Representation + Evaluation + Optimization") **does not** make this list, even though it also talks about "representation": there, Domingos is talking about the *classifier's* representation (the hypothesis space — trees, hyperplanes, rules...), not the representation of the *input data*. The two look similar at first glance but solve different problems, and it's worth keeping that distinction explicit.

## 2. Problem formulation

**Domain:** jurimetrics — predicting whether civil appeals are granted at TJSP (São Paulo state court).

**Data source:** CNJ's public DataJud API [cnj2026-datajud]. The schema below is confirmed from official documentation, not guessed: each case carries `numeroProcesso`, `dataAjuizamento`, `classe` (code + name), `assuntos` (a list of code + name), `orgaoJulgador`, and a `movimentos` array, each entry with `codigo`, `nome`, `dataHora`, and `complemento`. Movement names follow CNJ's Tabela Processual Unificada, a public, nationally standardized table.

### Target variable

Binary: the appeal is **granted** or **denied**. This isn't a ready-made field — it has to be derived from the **julgamento** movement (the session where the appellate panel votes and decides), which is itself a preprocessing step requiring manual validation on a sample before labeling the whole dataset.

### Preprocessing needed

- Parsing and flattening the nested `movimentos` list, sorting chronologically and filtering to relevant events.
- Encoding high-cardinality categorical attributes: `classe.codigo`, `assuntos[].codigo`, `orgaoJulgador`.
- Temporal feature engineering: time between `dataAjuizamento` and each intermediate movement, count of movements logged up to that point.
- Handling missing/inconsistent data (claim value isn't always filled in; subject codes are sometimes generic).
- Deduplicating re-filed cases or cases with legacy numbering.

### Potential algorithms

A simple baseline (logistic regression or a decision tree) can already run on the structured attributes available once the appeal is distributed. But what makes this problem interesting is that it doesn't need to be a single fixed prediction point: a model could update itself with each new pre-judgment movement — the more intermediate movements happen, the more information the model has, and accuracy should improve as the appeal approaches judgment. It's the same logic as election forecasting models, which get more accurate as election day approaches and more polls come in — without ever being allowed to use the actual vote count before it's official, of course.

### Moment of prediction

Anywhere between the appeal's distribution and **julgamento** (not the acórdão — julgamento is when the outcome is decided; the acórdão only formalizes in writing what was already voted on). That's the boundary: anything from julgamento onward, including julgamento itself, already contains the outcome.

### Attributes actually available at that moment

`classe`, `assuntos`, `orgaoJulgador`, `dataAjuizamento`, the first-instance outcome, and the intermediate procedural movements (distribution, referral to the rapporteur, filings, motions to review, etc.). **Not** available: julgamento, acórdão, publication, final res judicata, or anything logged after those.

## 3. Attribute with data leakage risk

Data leakage is "future" information leaking into today's model: data the model wouldn't actually have at inference time in production, but that it has access to during training and validation. Unlike classic overfitting (the model memorizing quirks of the training set and failing on new data), the problem here isn't the model — it's the **evaluation setup itself** being contaminated. The model learns exactly what it was given to learn; the one being fooled is whoever is validating it, because training and test scores "agree" only because the same leaked information sits on both sides, not because real generalization happened.

Concrete example for this case: computing the **average case duration over the entire dataset before splitting into train, test, and validation**, and using that as an attribute. This leaks because that average is computed over cases that have already concluded — including ones sitting in the test set — so it carries, in disguised form, information about the outcome of cases that, at the real moment of prediction, don't have an outcome yet. It's as if the test itself came with a cheat sheet taped to it: information that only exists because someone already knew the answer before you "took the test."

The same reasoning applies to the target variable itself: a sentence-outcome predictor trained on a historical grant-rate average computed over the same set of cases that includes the case being predicted has the same problem — the average already contains the answer key, indirectly.

The result is an artificially optimistic estimate because measured test accuracy is inflated: the model looks like it generalizes well because the cheat sheet was present in both training and test, not because it learned the actual legal pattern. Once deployed at the real prediction moment (without the future average available, because the case hasn't concluded yet), performance drops — just like the student who scored a 10 because they had the cheat sheet, not because they knew how to solve the problem.

## Execution notes

This is a conceptually formulated study — actually pulling data via the DataJud API and implementing the pipeline are left as a next step, outside the scope of this assignment.

*Content, examples, and conclusions are my own; the text's formatting had AI assistance.*
