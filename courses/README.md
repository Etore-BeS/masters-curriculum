# Courses

One folder per course. Folder names use the course code and a short English slug.

## 2026-2

| Code | Official name | Folder |
| --- | --- | --- |
| FT108A | Introdução ao Aprendizado de Máquina | [ft108a-machine-learning](ft108a-machine-learning/) |
| FT105A | Tópico Interdisciplinar I | [ft105a-information-visualization](ft105a-information-visualization/) |

## Folder structure (each course)

```
<courses>/<code>-<slug>/
  README.md       # syllabus, assessment, calendar, topic checklist
  references.md   # keys used in this course (points at references/catalog.md)
  notes/          # lecture and study notes
  exercises/      # bilingual exercise writeups (pt/ + en/)
  project/        # semester project or article
  materials/      # local PDFs and slides (gitignored except README.md)
```

Papers and books live in the global [references catalog](../references/catalog.md). Each course lists the keys it uses. Each exercise and project folder has its own `references.md`.

## Adding a new course

1. Create `courses/<code>-<short-english-name>/` with the subfolders above.
2. Add `references.md` that lists syllabus keys from the [catalog](../references/catalog.md).
3. Add a row to this file.
4. Add a row to the semester table in the root [README.md](../README.md).
