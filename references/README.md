# References

Canonical library for papers, books, and other sources used in this repo. Each work has one catalog entry and a stable key. Courses, exercises, and projects point at those keys. They do not copy the full citation.

## Layout

```
references/
  README.md         # this file
  catalog.md        # one section per work, headed by the key
  papers/           # local PDFs named <key>.pdf (gitignored)
  papers/README.md
```

## Keys

Use `lastnameYYYY` (or `lastnameYYYY-shortword` if two works collide). Examples: `han2006`, `wickham2023-r4ds`.

## Add a source

1. Add a section to `catalog.md` with the key, citation, DOI or URL, and a short note.
2. Drop the PDF in `papers/` as `<key>.pdf` when you have a local file.
3. List the key in the course `references.md` and in the exercise or project `references.md` that uses it. Add one line that states why you used it.

## Pointers

| Location | What it lists |
| --- | --- |
| [catalog.md](catalog.md) | Every source, once |
| `courses/<course>/references.md` | Keys used in that course |
| `exercises/<slug>/references.md` | Keys used in that exercise |
| `project/references.md` | Keys used in the course project |

Do not commit PDFs. Git ignores `references/papers/` except `README.md`.
