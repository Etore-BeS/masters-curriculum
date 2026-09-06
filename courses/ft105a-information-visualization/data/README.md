# FT105A data

Canonical datasets for Information Visualization live here (not under `project/*/code/`).

## Layout

| Path | Contents |
| --- | --- |
| `raw/` | IBGE zips + extracted fixed-width TXT + dictionary/input (gitignored) |
| `processed/` | Selected columns parquet, analysis sample CSV/parquet, codebook (gitignored) |

Keep this README tracked. Large binaries stay local.

## Expected raw files (Trabalho 1)

| File | Size (approx.) | Notes |
| --- | --- | --- |
| `raw/PNADC_022026.zip` | ~223 MB | Microdados 2º trimestre 2026 — **confirmed on IBGE FTP** |
| `raw/Dicionario_e_input_20221031.zip` | ~69 KB | Documentação |
| `raw/input_PNADC_trimestral.txt` | ~22 KB | SAS/R-style input (used by Python FWF parser) |
| `raw/dicionario_PNADC_microdados_trimestral.xls` | ~346 KB | Variable dictionary |
| `raw/extracted/PNADC_022026.txt` | ~1.7 GB | Fixed-width microdata |

## Processed outputs (generated)

| File | Role |
| --- | --- |
| `processed/pnadc_2026q2_selected.parquet` | All rows, selected columns |
| `processed/pnadc_2026q2_selected_head.csv` | 2k-row preview |
| `processed/pnadc_2026q2_sample.csv` | ~50k labeled sample for viz |
| `processed/pnadc_2026q2_sample.parquet` | Same sample, parquet |
| `processed/pnadc_2026q2_codebook.csv` | Column → origin variable |

Regenerate with `project/trabalho-1-pnad-multidim/code/01_download.py` … `03_prepare_sample.py`.
