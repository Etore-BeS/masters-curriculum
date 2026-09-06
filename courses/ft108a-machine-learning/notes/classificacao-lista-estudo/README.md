# Classificação — lista de estudo (Manim)

Notas e animações didáticas (português) para FT108A.  
Não resolve a lista nem a Tarefa 3.

## Setup (venv compartilhado na raiz do repo)

```bash
cd /Users/etorebraga/Code/masters-curriculum
uv sync --group manim
source .venv/bin/activate
```

Fish: same `uv` commands; activate with `source .venv/bin/activate.fish`.

Requisito de sistema: `ffmpeg`.

## Renderizar

```bash
cd courses/ft108a-machine-learning/notes/classificacao-lista-estudo
source ../../../../.venv/bin/activate

manim -ql scenes.py BiasVariance          # draft
manim -qm scenes.py BiasVariance          # medium
./render_all.sh -ql                       # todas → figures/manim/
```

## Cenas

| Classe | Tema |
| --- | --- |
| `BiasVariance` | Viés × variância / underfit–overfit |
| `EntropyGain` | Entropia e ganho de informação |
| `TreePrune` | Poda de árvore |
| `KNNScale` | k-NN sem/com escala |
| `MLPForward` | Forward pass de MLP |
| `OverfitGap` | Gap treino × teste |
| `MajorityVote` | Voto majoritário |
| `NaiveBayesProduct` | Produto de verossimilhanças |

## Arquivos

- `scenes.py` — cenas Manim (sem MathTex; fórmulas em Text)
- `resumo.md` — fórmulas LaTeX no markdown + embeds mp4/png
- `figures/` — PNG matplotlib; `figures/manim/` — renders Manim
- `gerar_plots.py` — fallback estático
- Root `pyproject.toml` dependency group `manim`

Não use `.venv` sob esta pasta — o ambiente compartilhado é o da raiz do repo.

## Ambiente

Use o `.venv` na **raiz** de `masters-curriculum` (`uv sync` / `source .venv/bin/activate`). Não crie `.venv` dentro de `notes/`.
Plots estáticos: `uv run python gerar_plots.py` (ou o venv ativado).
Manim: `uv sync --group manim` no mesmo venv; veja `render_all.sh`.
