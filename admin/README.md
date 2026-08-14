# Admin

Local bureaucratic kit for DAC, PPGT, and SIGA forms. **Do not commit personal data.**

## What belongs here

| Path | Tracked by git | Purpose |
| --- | --- | --- |
| `facts.example.md` | Yes | Field template with empty placeholders |
| `facts.md` | No | Your filled values for copy-paste into forms |
| `documents/` | No | Enrollment PDFs (ficha, edital, approval list, etc.) |

## Setup

1. Copy `facts.example.md` to `facts.md` if it does not exist yet.
2. Fill `facts.md` from your enrollment ficha.
3. Drop PDFs into `documents/` (see list below).

## Expected documents

Place these files in `documents/`:

- `ficha_inscricao.pdf` — enrollment form
- `Edital_ProcessoSeletivo_2s2026.pdf` — selection process notice
- `Candidatos_Aprovados_Mestrado_2_semestre2026.pdf` — approved candidates list

Add other bureaucratic PDFs (diplomas, transcripts, RG scans) as you need them.

## Safety

Git ignores `facts.md` and `documents/`. Before you push, run `git status` and confirm no personal files appear in the staging area.
