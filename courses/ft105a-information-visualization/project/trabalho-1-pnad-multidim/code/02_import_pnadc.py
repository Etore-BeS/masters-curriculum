#!/usr/bin/env python3
"""Import PNADC fixed-width microdata using IBGE SAS/TXT input widths.

Writes selected columns to data/processed/ as parquet (+ CSV head preview).
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

import pandas as pd

COURSE_DATA = Path(__file__).resolve().parents[3] / "data"
RAW = COURSE_DATA / "raw"
PROCESSED = COURSE_DATA / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

MICRO_ZIP = RAW / "PNADC_022026.zip"
MICRO_TXT = RAW / "extracted" / "PNADC_022026.txt"
DICT_ZIP = RAW / "Dicionario_e_input_20221031.zip"
INPUT_TXT = RAW / "input_PNADC_trimestral.txt"

KEEP = [
    "Ano",
    "Trimestre",
    "UF",
    "V2007",  # sexo
    "V2009",  # idade
    "V2010",  # cor/raca
    "V4010",  # ocupacao CBO
    "V40132A",  # secao da atividade
    "V403312",  # rendimento habitual dinheiro (trab. principal)
    "VD3004",  # nivel de instrucao
    "VD4002",  # condicao de ocupacao
    "VD4010",  # grupamento de atividade (trabalho principal)
    "VD4019",  # rendimento habitual todos os trabalhos
    "V1028",  # peso com calibracao
]


def ensure_extracted() -> Path:
    RAW.mkdir(parents=True, exist_ok=True)
    if not INPUT_TXT.exists():
        with zipfile.ZipFile(DICT_ZIP) as zf:
            zf.extractall(RAW)
    MICRO_TXT.parent.mkdir(parents=True, exist_ok=True)
    if not MICRO_TXT.exists() or MICRO_TXT.stat().st_size < 1_000_000_000:
        print(f"Extracting {MICRO_ZIP.name} ...")
        with zipfile.ZipFile(MICRO_ZIP) as zf:
            zf.extractall(MICRO_TXT.parent)
    return MICRO_TXT


def parse_sas_input(path: Path) -> dict[str, tuple[int, int]]:
    """Map variable name -> (start0, end0_exclusive) from SAS @pos specs."""
    text = path.read_text(encoding="latin-1")
    pat = re.compile(
        r"@(?P<pos>\d+)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s+\$?(?P<width>\d+)\."
    )
    out: dict[str, tuple[int, int]] = {}
    for m in pat.finditer(text):
        start1 = int(m.group("pos"))
        width = int(m.group("width"))
        start0 = start1 - 1
        out[m.group("name")] = (start0, start0 + width)
    return out


def main() -> None:
    ensure_extracted()
    specs = parse_sas_input(INPUT_TXT)
    missing = [c for c in KEEP if c not in specs]
    if missing:
        raise SystemExit(f"Variables not found in SAS input: {missing}")

    colspecs = [specs[c] for c in KEEP]
    print(f"Reading FWF: {MICRO_TXT} ({MICRO_TXT.stat().st_size:,} bytes)")
    print(f"Columns: {KEEP}")

    df = pd.read_fwf(
        MICRO_TXT,
        colspecs=colspecs,
        names=KEEP,
        dtype=str,
        encoding="latin-1",
    )
    print(f"Rows: {len(df):,}")

    out_parquet = PROCESSED / "pnadc_2026q2_selected.parquet"
    out_csv_head = PROCESSED / "pnadc_2026q2_selected_head.csv"
    df.to_parquet(out_parquet, index=False)
    df.head(2000).to_csv(out_csv_head, index=False)
    print(f"Wrote {out_parquet} ({out_parquet.stat().st_size:,} bytes)")
    print(f"Wrote {out_csv_head} (preview)")
    print("Next: 03_prepare_sample.py")


if __name__ == "__main__":
    main()
