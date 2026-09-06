# Masters curriculum

Study notes, exercises, and course projects for the master's program. Thesis work lives in a separate repository.

Agents: follow [AGENTS.md](AGENTS.md) for layout, gitignore, language, and the reference catalog.

## Program

| Field | Value |
| --- | --- |
| Student | Étore Braga e Santos |
| Institution | Universidade Estadual de Campinas (UNICAMP) |
| Unit | Faculdade de Tecnologia (FT), Campus Limeira |
| Program | Programa de Pós-graduação em Tecnologia (PPGT) |
| Degree | Mestrado em Tecnologia (82M) |
| Concentration | Sistemas de Informação e Comunicação |
| Research line | Gestão, processamento e armazenamento da informação |
| Advisor | João Roberto Bertini Júnior |
| Start | 2nd semester / 2026 |

## Thesis

The thesis uses jurimetria and complex networks to estimate the relevance of judicial precedents. Source code, drafts, and literature review are in the thesis repository, not here.

## Current semester (2026-2)

| Code | Course | Schedule | Folder |
| --- | --- | --- | --- |
| FT108A | Introdução ao Aprendizado de Máquina | Tue 08:00–12:00 | [courses/ft108a-machine-learning](courses/ft108a-machine-learning/) |
| FT105A | Tópico Interdisciplinar I (InfoVis + R) | Thu 14:00–18:00 | [courses/ft105a-information-visualization](courses/ft105a-information-visualization/) |

See [courses/README.md](courses/README.md) for the full course index.

## Repository layout

- `courses/` — one folder per course with notes, exercises, project, and local materials
- `references/` — global paper catalog. Courses and exercises point at keys (see [references/README.md](references/README.md))
- `admin/` — gitignored enrollment documents and a local facts file for bureaucratic forms (see [admin/README.md](admin/README.md))

## Conventions

- Course READMEs and notes: English
- Exercises: bilingual writeups in `pt/` and `en/` subfolders; shared code in `code/` when needed
- Lecture PDFs: stored locally under each course `materials/` folder; git ignores them
- Papers: one catalog entry per source. Pointers live in each course, exercise, and project `references.md`. PDFs stay in `references/papers/` and git ignores them.
