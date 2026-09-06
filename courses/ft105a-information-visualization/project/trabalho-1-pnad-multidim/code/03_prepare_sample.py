#!/usr/bin/env python3
"""Decode labels, filter adults, write exploratory viz sample (CSV + parquet).

Scaffold only — variable choices are starting points, not graded findings.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

COURSE_DATA = Path(__file__).resolve().parents[3] / "data"
PROCESSED = COURSE_DATA / "processed"
SRC = PROCESSED / "pnadc_2026q2_selected.parquet"

UF_LABELS = {
    "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP",
    "17": "TO", "21": "MA", "22": "PI", "23": "CE", "24": "RN", "25": "PB",
    "26": "PE", "27": "AL", "28": "SE", "29": "BA", "31": "MG", "32": "ES",
    "33": "RJ", "35": "SP", "41": "PR", "42": "SC", "43": "RS", "50": "MS",
    "51": "MT", "52": "GO", "53": "DF",
}
SEXO = {"1": "Homem", "2": "Mulher"}
COR = {
    "1": "Branca",
    "2": "Preta",
    "3": "Amarela",
    "4": "Parda",
    "5": "Indigena",
    "9": "Ignorado",
}
INSTR = {
    "1": "Sem instrucao",
    "2": "Fund. incompleto ou equiv.",
    "3": "Fund. completo ou equiv.",
    "4": "Medio incompleto ou equiv.",
    "5": "Medio completo ou equiv.",
    "6": "Superior incompleto ou equiv.",
    "7": "Superior completo",
}
COND_OCUP = {"1": "Ocupado", "2": "Desocupado"}
# VD4010 — grupamentos de atividade (dictionary labels, shortened)
SETOR = {
    "01": "Agricultura",
    "02": "Industria geral",
    "03": "Construcao",
    "04": "Comercio e reparacao",
    "05": "Transporte e correio",
    "06": "Alojamento e alimentacao",
    "07": "Info/financ/prof/admin",
    "08": "Admin publica",
    "09": "Educacao/saude/sociais",
    "10": "Outros servicos",
    "11": "Servicos domesticos",
    "12": "Atividades mal definidas",
    "1": "Agricultura",
    "2": "Industria geral",
    "3": "Construcao",
    "4": "Comercio e reparacao",
    "5": "Transporte e correio",
    "6": "Alojamento e alimentacao",
    "7": "Info/financ/prof/admin",
    "8": "Admin publica",
    "9": "Educacao/saude/sociais",
}


def to_num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.strip(), errors="coerce")


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing {SRC}. Run 02_import_pnadc.py first.")

    df = pd.read_parquet(SRC)
    out = pd.DataFrame()
    out["ano"] = df["Ano"].str.strip()
    out["trimestre"] = df["Trimestre"].str.strip()
    out["uf_cod"] = df["UF"].str.strip().str.zfill(2)
    out["uf"] = out["uf_cod"].map(UF_LABELS).fillna(out["uf_cod"])
    out["sexo"] = df["V2007"].str.strip().map(SEXO)
    out["idade"] = to_num(df["V2009"])
    out["cor_raca"] = df["V2010"].str.strip().map(COR)
    out["ocupacao_cbo"] = df["V4010"].str.strip()
    out["setor"] = df["VD4010"].astype(str).str.strip().str.zfill(2).map(SETOR)
    # fallback without zfill for single-digit already mapped
    missing = out["setor"].isna()
    out.loc[missing, "setor"] = df.loc[missing, "VD4010"].astype(str).str.strip().map(SETOR)
    out["setor"] = out["setor"].fillna("Nao classificado / NA")
    out["rend_principal"] = to_num(df["V403312"])
    out["instrucao"] = df["VD3004"].str.strip().map(INSTR)
    out["cond_ocupacao"] = df["VD4002"].str.strip().map(COND_OCUP)
    out["rend_todos"] = to_num(df["VD4019"])
    out["peso"] = to_num(df["V1028"])

    sample = out.loc[
        (out["idade"] >= 14)
        & out["cond_ocupacao"].notna()
        & out["sexo"].notna()
        & out["cor_raca"].notna()
        & (out["cor_raca"] != "Ignorado")
    ].copy()

    n_target = 50_000
    if len(sample) > n_target:
        sample = sample.sample(n=n_target, random_state=42)

    codebook = pd.DataFrame(
        [
            {"coluna": "uf", "origem": "UF", "descricao": "Unidade da Federacao (sigla)"},
            {"coluna": "sexo", "origem": "V2007", "descricao": "Sexo"},
            {"coluna": "idade", "origem": "V2009", "descricao": "Idade na data de referencia"},
            {"coluna": "cor_raca", "origem": "V2010", "descricao": "Cor ou raca"},
            {"coluna": "instrucao", "origem": "VD3004", "descricao": "Nivel de instrucao mais elevado"},
            {"coluna": "cond_ocupacao", "origem": "VD4002", "descricao": "Condicao de ocupacao"},
            {"coluna": "setor", "origem": "VD4010", "descricao": "Grupamento de atividade (trabalho principal)"},
            {
                "coluna": "rend_principal",
                "origem": "V403312",
                "descricao": "Rendimento habitual (dinheiro) trab. principal",
            },
            {
                "coluna": "rend_todos",
                "origem": "VD4019",
                "descricao": "Rendimento habitual todos os trabalhos",
            },
            {"coluna": "peso", "origem": "V1028", "descricao": "Peso com calibracao"},
            {"coluna": "ocupacao_cbo", "origem": "V4010", "descricao": "Codigo ocupacao trab. principal"},
        ]
    )

    csv_path = PROCESSED / "pnadc_2026q2_sample.csv"
    parquet_path = PROCESSED / "pnadc_2026q2_sample.parquet"
    code_path = PROCESSED / "pnadc_2026q2_codebook.csv"
    sample.to_csv(csv_path, index=False)
    sample.to_parquet(parquet_path, index=False)
    codebook.to_csv(code_path, index=False)

    print(f"Sample rows: {len(sample):,}")
    print(f"Wrote {csv_path} ({csv_path.stat().st_size:,} bytes)")
    print(f"Wrote {parquet_path}")
    print(f"Wrote {code_path}")
    print("Next: 04_explore_viz.py")


if __name__ == "__main__":
    main()
