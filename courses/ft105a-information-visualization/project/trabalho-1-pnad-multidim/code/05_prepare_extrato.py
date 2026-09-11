#!/usr/bin/env python3
"""Import the wide PNADC extract used by the weighted analysis notebook.

02_import_pnadc.py keeps 14 columns, which is enough for the sample-based
figures but not for the weighted ones: those need the household key
(UPA + V1008 + V1014), the position in employment (VD4009), the CNPJ flag
(V4019) and the hours worked (VD4031). This script reads the same fixed-width
file with a wider column list and writes pnadc_2026q2_extrato.parquet.

Output: data/processed/pnadc_2026q2_extrato.parquet (521730 rows x 63 cols).
Consumed by: pnad_analise_ponderada.ipynb
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

OUT_PARQUET = PROCESSED / "pnadc_2026q2_extrato.parquet"

# Identification and sampling design.
KEEP_ID = [
    "Ano",
    "Trimestre",
    "UF",
    "Capital",
    "RM_RIDE",
    "UPA",  # with V1008 and V1014, identifies the household
    "Estrato",
    "V1008",  # household selection number
    "V1014",  # panel
    "V1016",  # interview number
    "V1022",  # urban / rural
    "V1023",  # area type
    "V1028",  # calibrated weight, required for every rate and mean below
]

# Demographics and education.
KEEP_PESSOA = [
    "V2001",  # people in the household
    "V2003",  # order number
    "V2005",  # relation to the reference person
    "V2007",  # sex
    "V2009",  # age
    "V2010",  # colour or race
    "V3001",  # can read and write
    "V3002",  # attends school
    "V3002A",  # type of school
    "V3003A",  # level attended
    "V3009A",  # highest level completed
    "VD2002",  # household composition
    "VD3004",  # education level
    "VD3005",  # years of schooling
]

# Labour force: status, position, formality, hours and income.
KEEP_TRABALHO = [
    "V4009",  # number of jobs
    "V4010",  # occupation, CBO
    "V4012",  # type of employer in the main job
    "V4013",  # activity of the main job, CNAE
    "V4019",  # employer or own account with CNPJ
    "V4028",  # more than one job
    "V4029",  # signed work card in the main job
    "V4032",  # contributes to social security
    "V403312",  # usual cash income, main job
    "V4039",  # usual hours, main job
    "V4039C",  # usual hours, all jobs
    "V4040",  # time in the main job
    "V4041",  # time in the secondary job
    "V4043",  # signed work card in the secondary job
    "V4056",  # hours in the secondary job
    "V4063A",  # looked for work
    "V4071",  # available to work
    "V4076",  # time out of work
    "VD4001",  # in the labour force
    "VD4002",  # employed or unemployed
    "VD4003",  # potential labour force
    "VD4004A",  # underemployment by hours
    "VD4005",  # discouraged
    "VD4007",  # employee, employer, own account
    "VD4008",  # detailed position
    "VD4009",  # position in employment, used for the informality flag
    "VD4010",  # activity group
    "VD4011",  # occupation group
    "VD4012",  # contributes to social security
    "VD4013",  # usual hours bracket
    "VD4016",  # usual income, main job
    "VD4017",  # actual income, main job
    "VD4019",  # usual income, all jobs
    "VD4020",  # actual income, all jobs
    "VD4031",  # usual hours, all jobs
    "VD4035",  # actual hours, all jobs
]

KEEP = KEEP_ID + KEEP_PESSOA + KEEP_TRABALHO

# Columns kept as text: codes with leading zeros, or keys we concatenate.
AS_TEXT = {
    "Ano",
    "UF",
    "Capital",
    "RM_RIDE",
    "UPA",
    "Estrato",
    "V1008",
    "V1014",
    "V1016",
    "V2003",
    "V4010",
    "V4013",
    "V4041",
}
# Columns kept as float: weights and income, which have decimals.
AS_FLOAT = {"V1028", "V403312", "VD4016", "VD4017", "VD4019", "VD4020"}


def ensure_extracted() -> Path:
    """Unzip the microdata and the SAS input if they are not on disk yet."""
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


def cast(df: pd.DataFrame) -> pd.DataFrame:
    """Text stays text, income and weights become float, codes become Int16."""
    for col in df.columns:
        if col in AS_TEXT:
            df[col] = df[col].astype("string")
        elif col in AS_FLOAT:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int16")
    return df


def main() -> None:
    ensure_extracted()
    specs = parse_sas_input(INPUT_TXT)
    missing = [c for c in KEEP if c not in specs]
    if missing:
        raise SystemExit(f"Variables not found in SAS input: {missing}")

    colspecs = [specs[c] for c in KEEP]
    print(f"Reading FWF: {MICRO_TXT} ({MICRO_TXT.stat().st_size:,} bytes)")
    print(f"Columns: {len(KEEP)}")
    df = pd.read_fwf(
        MICRO_TXT,
        colspecs=colspecs,
        names=KEEP,
        dtype=str,
        encoding="latin-1",
    )
    print(f"Rows: {len(df):,}")

    df = cast(df)
    df.to_parquet(OUT_PARQUET, index=False)
    print(f"Wrote {OUT_PARQUET} ({OUT_PARQUET.stat().st_size:,} bytes)")

    # Quick check against the IBGE release for 2026Q2.
    peso = df["V1028"]
    na_forca = df["VD4001"].eq(1).fillna(False)
    ocupado = df["VD4002"].eq(1).fillna(False)
    desocup = 100 * peso[na_forca & df["VD4002"].eq(2).fillna(False)].sum() / peso[na_forca].sum()
    renda = df.loc[ocupado, "VD4019"]
    peso_oc = peso[ocupado]
    ok = renda.notna()
    media = (renda[ok] * peso_oc[ok]).sum() / peso_oc[ok].sum()
    print(f"Population: {peso.sum() / 1e6:.1f} million")
    print(f"Unemployment: {desocup:.1f}% (IBGE release: 5.4%)")
    print(f"Mean usual income: R$ {media:,.0f} (IBGE release: R$ 3,738)")
    print("Next: open pnad_analise_ponderada.ipynb")


if __name__ == "__main__":
    main()
