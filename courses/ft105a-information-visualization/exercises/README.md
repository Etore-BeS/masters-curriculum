# Exercises

Bilingual exercise writeups for FT105A. Each exercise gets its own folder.

## Layout

```
exercises/
  <exercise-slug>/
    pt/
      readme.md    # problem statement and solution notes (Portuguese)
    en/
      readme.md    # problem statement and solution notes (English)
    code/          # shared R scripts and Quarto files (optional, add when needed)
    references.md  # catalog keys used in this exercise
```

## Rules

- Write the problem statement and your solution notes in both `pt/` and `en/`.
- Put R scripts and Quarto files once in `code/` when an exercise needs them. Do not duplicate scripts across language folders.
- Use dash-case folder names (e.g., `01-ggplot2-basics/`).
- Number exercises when order matters: `01-slug/`, `02-slug/`.
- List catalog keys in `references.md`. Add the full record once in [catalog.md](../../../references/catalog.md). Also add the key to the [course references](../references.md).

## Source material

Lecture slides and lab handouts live in [materials/](../materials/). Distance activities between synchronous sessions also go here as you complete them.

No exercises are scaffolded yet. Add folders as you work through the semester.
