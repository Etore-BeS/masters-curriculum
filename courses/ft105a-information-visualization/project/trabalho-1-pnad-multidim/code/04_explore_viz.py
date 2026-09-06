#!/usr/bin/env python3
"""EXPLORATORY interactive Plotly HTML visualizations — scaffold only.

Techniques (group draft): parallel coordinates, treemap, pixel matrix.
Do NOT treat patterns as final graded findings.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COURSE_DATA = Path(__file__).resolve().parents[3] / "data"
PROCESSED = COURSE_DATA / "processed"
OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(parents=True, exist_ok=True)

SAMPLE = PROCESSED / "pnadc_2026q2_sample.parquet"
TITLE_PREFIX = "EXPLORATORY — scaffold (not final submission)"

INSTR_ORDER = [
    "Sem instrucao",
    "Fund. incompleto ou equiv.",
    "Fund. completo ou equiv.",
    "Medio incompleto ou equiv.",
    "Medio completo ou equiv.",
    "Superior incompleto ou equiv.",
    "Superior completo",
]
COR_ORDER = ["Branca", "Preta", "Parda", "Amarela", "Indigena"]


def load() -> pd.DataFrame:
    if not SAMPLE.exists():
        raise SystemExit(f"Missing {SAMPLE}. Run 03_prepare_sample.py first.")
    return pd.read_parquet(SAMPLE)


def parallel_coords(df: pd.DataFrame) -> Path:
    """Parallel coordinates with >=4 variables; color by sexo (colorblind palette)."""
    d = df.loc[
        (df["cond_ocupacao"] == "Ocupado")
        & df["rend_todos"].notna()
        & (df["rend_todos"] > 0)
        & df["idade"].notna()
    ].copy()
    cap = d["rend_todos"].quantile(0.99)
    d = d.loc[d["rend_todos"] <= cap]
    if len(d) > 8000:
        d = d.sample(n=8000, random_state=0)

    d["instr_ord"] = pd.Categorical(d["instrucao"], categories=INSTR_ORDER, ordered=True)
    d = d.dropna(subset=["instr_ord", "sexo"])
    d["instr_num"] = d["instr_ord"].cat.codes.astype(float)
    d["sexo_num"] = (d["sexo"] == "Mulher").astype(float)
    d["uf_num"] = pd.to_numeric(d["uf_cod"], errors="coerce")

    fig = go.Figure(
        data=go.Parcoords(
            line=dict(
                color=d["sexo_num"],
                colorscale=[[0, "#0072B2"], [1, "#D55E00"]],
                showscale=True,
                colorbar=dict(
                    title="Sexo",
                    tickvals=[0, 1],
                    ticktext=["Homem", "Mulher"],
                ),
            ),
            dimensions=[
                dict(label="Idade", values=d["idade"], range=[14, float(d["idade"].max())]),
                dict(
                    label="Instrucao (ord)",
                    values=d["instr_num"],
                    tickvals=list(range(len(INSTR_ORDER))),
                    ticktext=INSTR_ORDER,
                ),
                dict(label="Rend. todos (R$)", values=d["rend_todos"]),
                dict(label="UF cod.", values=d["uf_num"]),
                dict(
                    label="Sexo (0/1)",
                    values=d["sexo_num"],
                    tickvals=[0, 1],
                    ticktext=["H", "M"],
                ),
            ],
            labelangle=-15,
        )
    )
    fig.update_layout(
        title=(
            f"{TITLE_PREFIX}<br>Parallel coordinates — "
            f"idade, instrucao, rendimento, UF, sexo (n={len(d):,})"
        ),
        font=dict(size=12),
        margin=dict(l=80, r=40, t=100, b=40),
        height=560,
    )
    path = OUT / "01_parallel_coordinates.html"
    fig.write_html(path, include_plotlyjs="cdn")
    return path


def treemap(df: pd.DataFrame) -> Path:
    """Treemap UF -> setor; size=count; color=mean income (Cividis)."""
    d = df.loc[
        (df["cond_ocupacao"] == "Ocupado")
        & df["setor"].notna()
        & (df["setor"] != "Nao classificado / NA")
        & df["rend_todos"].notna()
        & (df["rend_todos"] > 0)
    ].copy()
    g = (
        d.groupby(["uf", "setor"], as_index=False)
        .agg(n=("rend_todos", "size"), rend_medio=("rend_todos", "mean"))
    )
    fig = px.treemap(
        g,
        path=["uf", "setor"],
        values="n",
        color="rend_medio",
        color_continuous_scale="Cividis",
        title=(
            f"{TITLE_PREFIX}<br>Treemap — UF → setor "
            f"(tamanho=contagem; cor=renda media) n_obs={len(d):,}"
        ),
    )
    fig.update_traces(
        textinfo="label+value+percent root",
        hovertemplate=(
            "<b>%{label}</b><br>n=%{value}<br>renda media=%{color:.0f}<extra></extra>"
        ),
    )
    fig.update_layout(margin=dict(t=90, l=10, r=10, b=10), height=650)
    path = OUT / "02_treemap.html"
    fig.write_html(path, include_plotlyjs="cdn")
    return path


def pixel_matrix(df: pd.DataFrame) -> Path:
    """Dense heatmap: mean of scaled idade / log-renda / ocupacao by instrucao x cor."""
    d = df.loc[df["instrucao"].notna() & df["cor_raca"].notna()].copy()
    d["log_rend"] = np.log1p(d["rend_todos"].clip(lower=0))
    d["ocupado"] = (d["cond_ocupacao"] == "Ocupado").astype(float)
    d = d.loc[d["instrucao"].isin(INSTR_ORDER) & d["cor_raca"].isin(COR_ORDER)]

    for col in ["idade", "log_rend", "ocupado"]:
        v = d[col]
        d[f"z_{col}"] = (v - v.min()) / (v.max() - v.min() + 1e-9)
    d["score"] = d[["z_idade", "z_log_rend", "z_ocupado"]].mean(axis=1)

    pivot = (
        d.pivot_table(index="instrucao", columns="cor_raca", values="score", aggfunc="mean")
        .reindex(index=INSTR_ORDER, columns=COR_ORDER)
    )
    counts = (
        d.pivot_table(index="instrucao", columns="cor_raca", values="score", aggfunc="size")
        .reindex(index=INSTR_ORDER, columns=COR_ORDER)
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=list(pivot.columns),
            y=list(pivot.index),
            colorscale="Viridis",
            colorbar=dict(title="Media<br>escalas 0-1"),
            hovertemplate=(
                "Instrucao: %{y}<br>Cor/raca: %{x}<br>"
                "score=%{z:.3f}<br>n=%{customdata}<extra></extra>"
            ),
            customdata=counts.fillna(0).values,
        )
    )
    fig.update_layout(
        title=(
            f"{TITLE_PREFIX}<br>"
            "Pixel matrix — score medio (idade, log-renda, ocupacao) "
            f"por instrucao × cor/raca (n={len(d):,})"
        ),
        xaxis_title="Cor ou raca",
        yaxis_title="Nivel de instrucao",
        yaxis=dict(autorange="reversed"),
        height=520,
        margin=dict(t=100, l=200, r=40, b=60),
    )
    path = OUT / "03_pixel_matrix.html"
    fig.write_html(path, include_plotlyjs="cdn")
    return path


def main() -> None:
    df = load()
    paths = [parallel_coords(df), treemap(df), pixel_matrix(df)]
    print("Wrote exploratory HTML:")
    for p in paths:
        print(f"  {p} ({p.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
