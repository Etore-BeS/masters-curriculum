#!/usr/bin/env python3
"""Gera figuras ilustrativas para o guia de estudo FT108A (classificação).
Apenas material didático — exemplos inventados, sem dados da lista de exercícios.
Requer: numpy, matplotlib.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# Estilo limpo, legível em anotações
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.grid": True,
    "grid.alpha": 0.25,
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
})


def save(fig, name: str) -> None:
    path = OUT / name
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {path}")


def fig_bias_variance():
    """Curvas clássicas de erro treino/teste vs complexidade (under/overfitting)."""
    complexity = np.linspace(1, 10, 200)
    # Erro de treino cai com complexidade; erro de teste em U
    train_err = 0.45 * np.exp(-0.35 * complexity) + 0.05
    test_err = (
        0.55 * np.exp(-0.45 * complexity)
        + 0.018 * (complexity - 4.2) ** 2
        + 0.12
    )
    # Bias^2 e variance (esquemáticos, somando aproximadamente o erro de teste)
    bias2 = 0.50 * np.exp(-0.40 * complexity) + 0.05
    variance = 0.01 * (complexity - 1) ** 1.6 + 0.02
    irreducible = 0.08

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))

    ax = axes[0]
    ax.plot(complexity, train_err, "C0-", lw=2.2, label="Erro treino (Train)")
    ax.plot(complexity, test_err, "C3-", lw=2.2, label="Erro teste (Test)")
    # Marcas under / sweet spot / over
    x_u, x_o = 2.0, 8.0
    x_opt = complexity[np.argmin(test_err)]
    for x, lab, c in [
        (x_u, "Underfitting\n(alto bias)", "C1"),
        (x_opt, "Bom equilíbrio", "C2"),
        (x_o, "Overfitting\n(alta variance)", "C3"),
    ]:
        ax.axvline(x, color=c, ls="--", alpha=0.7)
        ax.text(x, ax.get_ylim()[1] if False else 0.02, lab, ha="center",
                va="bottom", fontsize=8, color=c,
                transform=ax.get_xaxis_transform())
    ax.set_xlabel("Complexidade do modelo →")
    ax.set_ylabel("Erro (esquemático)")
    ax.set_title("Bias–Variance: underfitting vs overfitting")
    ax.legend(loc="upper right")
    ax.set_ylim(0, 0.72)

    ax = axes[1]
    ax.plot(complexity, bias2, "C0-", lw=2, label=r"Bias$^2$")
    ax.plot(complexity, variance, "C1-", lw=2, label="Variance")
    ax.plot(complexity, bias2 + variance + irreducible, "C3--", lw=2,
            label=r"Erro ≈ Bias$^2$ + Var + ruído")
    ax.set_xlabel("Complexidade do modelo →")
    ax.set_ylabel("Contribuição ao erro")
    ax.set_title("Decomposição esquemática do erro")
    ax.legend(loc="upper right")

    save(fig, "01_bias_variance.png")


def fig_naive_bayes():
    """Diagrama conceitual: prior × likelihood → posterior (independência)."""
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("Naïve Bayes — ideia (independência condicional)", pad=12)

    def box(x, y, w, h, text, fc="#E8F4FC", ec="#1F4E79"):
        from matplotlib.patches import FancyBboxPatch
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.15",
                           facecolor=fc, edgecolor=ec, lw=1.8)
        ax.add_patch(p)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=10, wrap=True)

    box(0.3, 3.8, 2.4, 1.4, "Features\n$x_1, x_2, \\ldots, x_d$", "#FFF4E5", "#B86E00")
    box(3.5, 4.2, 2.8, 1.0, "Hipótese ingenua:\n$P(x_i|y)$ independentes", "#FDEDEC", "#922B21")
    box(7.0, 3.8, 2.6, 1.4, "Likelihood\n$\\prod_i P(x_i\\mid y)$", "#E8F8F5", "#117A65")

    box(0.3, 0.6, 2.4, 1.4, "Prior\n$P(y)$", "#EBF5FB", "#1A5276")
    box(3.5, 0.8, 2.8, 1.2, "Bayes\n$\\propto$ prior $\\times$ lik.", "#F5EEF8", "#6C3483")
    box(7.0, 0.6, 2.6, 1.4, "Posterior\n$\\hat{y}=\\arg\\max_y$", "#E8F8F5", "#117A65")

    # Setas
    for (x0, y0, x1, y1) in [
        (2.7, 4.5, 3.5, 4.7),
        (6.3, 4.7, 7.0, 4.5),
        (2.7, 1.3, 3.5, 1.4),
        (6.3, 1.4, 7.0, 1.3),
        (4.9, 4.2, 4.9, 2.0),
        (1.5, 3.8, 1.5, 2.0),
    ]:
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color="#555", lw=1.5))

    ax.text(5, 3.2,
            r"$P(y\mid\mathbf{x}) \propto P(y)\prod_{i=1}^{d} P(x_i\mid y)$",
            ha="center", va="center", fontsize=13,
            bbox=dict(boxstyle="round", facecolor="white", edgecolor="#888"))
    ax.text(5, 0.15,
            "Classifica a classe com maior posterior (MAP). / Predict class with largest posterior.",
            ha="center", fontsize=9, color="#444")
    save(fig, "02_naive_bayes.png")


def fig_entropy_ig():
    """Entropia binária + exemplo inventado de information gain."""
    # Curva de entropia H(p)
    p = np.linspace(1e-4, 1 - 1e-4, 400)
    H = -p * np.log2(p) - (1 - p) * np.log2(1 - p)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.3))
    ax = axes[0]
    ax.plot(p, H, "C0-", lw=2.2)
    ax.axhline(1.0, color="gray", ls=":", alpha=0.6)
    ax.set_xlabel(r"$p = P(Y=1)$")
    ax.set_ylabel(r"Entropia $H(Y)$ [bits]")
    ax.set_title(r"Entropia binária $H(p)=-p\log_2 p-(1-p)\log_2(1-p)$")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.annotate("máx. incerteza\nem $p=0.5$", xy=(0.5, 1.0), xytext=(0.65, 0.7),
                arrowprops=dict(arrowstyle="->", color="C3"), color="C3", fontsize=9)

    # Exemplo inventado: 8 amostras, split por atributo A
    # Parent: 5 pos / 3 neg → H_parent
    # Left: 4 pos / 1 neg; Right: 1 pos / 2 neg
    def entropy_counts(pos, neg):
        n = pos + neg
        if n == 0:
            return 0.0
        probs = [c / n for c in (pos, neg) if c > 0]
        return float(-sum(q * np.log2(q) for q in probs))

    Hp = entropy_counts(5, 3)
    Hl = entropy_counts(4, 1)
    Hr = entropy_counts(1, 2)
    # pesos
    wl, wr = 5 / 8, 3 / 8
    H_after = wl * Hl + wr * Hr
    IG = Hp - H_after

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("Exemplo inventado (NÃO é Tabela 1 da lista)")

    lines = [
        "Conjunto pai (toy): 8 exemplos → 5 ⊕ / 3 ⊖",
        f"H(pai) = {Hp:.3f} bits",
        "",
        "Split pelo atributo A (inventado):",
        f"  A=sim (5): 4 ⊕ / 1 ⊖ → H = {Hl:.3f}",
        f"  A=não (3): 1 ⊕ / 2 ⊖ → H = {Hr:.3f}",
        "",
        f"H após split = (5/8)·{Hl:.3f} + (3/8)·{Hr:.3f} = {H_after:.3f}",
        f"IG(A) = H(pai) − H após = {Hp:.3f} − {H_after:.3f} = {IG:.3f}",
        "",
        "Escolhe-se o atributo com maior IG.",
    ]
    ax.text(0.3, 9.2, "\n".join(lines), va="top", family="monospace", fontsize=9.5,
            bbox=dict(boxstyle="round", facecolor="#F8F9F9", edgecolor="#AAA"))
    save(fig, "03_entropy_information_gain.png")


def fig_decision_tree_pruning():
    """Árvore conceitual + efeito do pruning no erro."""
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.5))

    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("Árvore de decisão (esquema) + poda")

    # Nós
    nodes = {
        "r": (5, 9, "x₁ < 0.4?"),
        "l": (2.5, 6.5, "x₂ < 1?"),
        "rr": (7.5, 6.5, "folha: ⊕"),
        "ll": (1.2, 4, "folha: ⊖"),
        "lr": (3.8, 4, "folha: ⊕"),
        "prune": (7.5, 4.2, "nó podado\n→ folha ⊕"),
    }
    for k, (x, y, t) in nodes.items():
        fc = "#FADBD8" if k == "prune" else ("#D5F5E3" if "folha" in t else "#D6EAF8")
        ax.text(x, y, t, ha="center", va="center", fontsize=9,
                bbox=dict(boxstyle="round", facecolor=fc, edgecolor="#555"))
    # Arestas
    for (a, b, lab) in [
        ("r", "l", "sim"),
        ("r", "rr", "não"),
        ("l", "ll", "sim"),
        ("l", "lr", "não"),
    ]:
        x0, y0, _ = nodes[a]
        x1, y1, _ = nodes[b]
        ax.annotate("", xy=(x1, y1 + 0.45), xytext=(x0, y0 - 0.45),
                    arrowprops=dict(arrowstyle="->", color="#333"))
        ax.text((x0 + x1) / 2 - 0.15, (y0 + y1) / 2, lab, fontsize=8, color="#666")

    ax.text(5, 1.2,
            "Poda (pruning): remove ramos que\n"
            "só memorizam ruído → menor variance,\n"
            "melhor generalização no teste.",
            ha="center", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="#FEF9E7", edgecolor="#B7950B"))

    ax = axes[1]
    depth = np.arange(1, 12)
    train = 0.40 * np.exp(-0.35 * depth) + 0.02
    test = 0.42 * np.exp(-0.32 * depth) + 0.012 * (depth - 4) ** 2 + 0.08
    ax.plot(depth, train, "C0-o", label="Erro treino")
    ax.plot(depth, test, "C3-s", label="Erro validação/teste")
    best = depth[np.argmin(test)]
    ax.axvline(best, color="C2", ls="--", label=f"Profundidade útil ≈ {best}")
    ax.set_xlabel("Profundidade / nº de folhas →")
    ax.set_ylabel("Erro")
    ax.set_title("Por que podar? Erro de teste sobe após certo ponto")
    ax.legend(loc="upper left")
    ax.set_ylim(0, 0.55)
    save(fig, "04_decision_tree_pruning.png")


def fig_confusion_matrix():
    """Matriz de confusão + métricas com exemplo inventado pequeno."""
    # Inventado: 100 exemplos — TP=40, FN=10, FP=15, TN=35
    TP, FN, FP, TN = 40, 10, 15, 35
    cm = np.array([[TP, FN], [FP, TN]], dtype=float)
    acc = (TP + TN) / (TP + TN + FP + FN)

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.4))
    ax = axes[0]
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Pred ⊕", "Pred ⊖"])
    ax.set_yticklabels(["Real ⊕", "Real ⊖"])
    ax.set_title("Matriz de confusão (exemplo inventado)")
    for i in range(2):
        for j in range(2):
            labels = [["TP", "FN"], ["FP", "TN"]]
            ax.text(j, i, f"{labels[i][j]}\n{int(cm[i, j])}", ha="center", va="center",
                    color="white" if cm[i, j] > cm.max() / 2 else "black", fontsize=12, fontweight="bold")
    fig.colorbar(im, ax=ax, fraction=0.046)

    ax = axes[1]
    ax.axis("off")
    text = (
        "Definições (classe positiva ⊕):\n"
        "  TP = verdadeiros positivos\n"
        "  TN = verdadeiros negativos\n"
        "  FP = falsos positivos\n"
        "  FN = falsos negativos\n\n"
        r"Accuracy = (TP+TN) / (TP+TN+FP+FN)" "\n"
        f"         = ({TP}+{TN}) / 100 = {acc:.2f}\n\n"
        "Lembrete: accuracy pode enganar em\n"
        "classes desbalanceadas — olhar também\n"
        "precisão, recall, F1 (conceitos próximos)."
    )
    ax.text(0.05, 0.95, text, va="top", family="monospace", fontsize=10,
            transform=ax.transAxes,
            bbox=dict(boxstyle="round", facecolor="#F4F6F7", edgecolor="#888"))
    ax.set_title("Fórmulas + toy numérico (não é da lista)")
    save(fig, "05_confusion_matrix.png")


def fig_knn_normalization():
    """k-NN: feature com escala grande domina a distância euclidiana."""
    rng = np.random.default_rng(7)
    n = 40
    # Classe 0 e 1
    c0 = np.column_stack([rng.normal(2, 0.6, n), rng.normal(50, 8, n)])
    c1 = np.column_stack([rng.normal(4, 0.6, n), rng.normal(70, 8, n)])
    query = np.array([3.0, 55.0])

    def knn_idx(X, q, k=5):
        d = np.linalg.norm(X - q, axis=1)
        return np.argsort(d)[:k], d

    X = np.vstack([c0, c1])
    y = np.array([0] * n + [1] * n)

    # Sem normalização
    idx_raw, _ = knn_idx(X, query, 5)
    # Com z-score
    mu, sd = X.mean(0), X.std(0)
    Xn = (X - mu) / sd
    qn = (query - mu) / sd
    idx_n, _ = knn_idx(Xn, qn, 5)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.5))

    ax = axes[0]
    ax.scatter(c0[:, 0], c0[:, 1], c="C0", label="Classe 0", alpha=0.75)
    ax.scatter(c1[:, 0], c1[:, 1], c="C3", label="Classe 1", alpha=0.75)
    ax.scatter(*query, c="black", marker="*", s=220, zorder=5, label="Query")
    ax.scatter(X[idx_raw, 0], X[idx_raw, 1], facecolors="none", edgecolors="gold",
               s=180, lw=2, label="5-NN (raw)")
    ax.set_xlabel("feat A (pequena escala, ~unidades)")
    ax.set_ylabel("feat B (grande escala, ~dezenas)")
    ax.set_title("Sem normalização: B domina a distância")
    ax.legend(loc="best", fontsize=8)

    ax = axes[1]
    ax.scatter(Xn[y == 0, 0], Xn[y == 0, 1], c="C0", label="Classe 0", alpha=0.75)
    ax.scatter(Xn[y == 1, 0], Xn[y == 1, 1], c="C3", label="Classe 1", alpha=0.75)
    ax.scatter(*qn, c="black", marker="*", s=220, zorder=5, label="Query")
    ax.scatter(Xn[idx_n, 0], Xn[idx_n, 1], facecolors="none", edgecolors="gold",
               s=180, lw=2, label="5-NN (z-score)")
    ax.set_xlabel("feat A (z-score)")
    ax.set_ylabel("feat B (z-score)")
    ax.set_title("Com normalização: ambas features contam")
    ax.legend(loc="best", fontsize=8)
    ax.set_aspect("equal", adjustable="datalim")

    fig.suptitle("k-NN e escala das features (exemplo inventado)", y=1.02)
    save(fig, "06_knn_normalization.png")


def fig_mlp_overview():
    """MLP: arquitetura, contagem de pesos, overfitting, preprocessing."""
    fig = plt.figure(figsize=(11, 7.2))
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.28)

    # (0,0) diagrama de rede
    ax = fig.add_subplot(gs[0, 0])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_title("MLP — unidades, bias e pesos")

    layers = {
        "in": [(1.5, y) for y in (6.5, 5, 3.5, 2)],
        "h": [(5, y) for y in (7, 5.5, 4, 2.5, 1)],
        "out": [(8.5, y) for y in (5.5, 3.5)],
    }
    labels_in = [r"$x_1$", r"$x_2$", r"$x_3$", "bias\n(+1)"]
    for (x, y), lab in zip(layers["in"], labels_in):
        ax.plot(x, y, "o", ms=18, color="#5DADE2" if "bias" not in lab else "#F5B041")
        ax.text(x - 0.7, y, lab, ha="right", va="center", fontsize=9)
    for i, (x, y) in enumerate(layers["h"]):
        lab = "bias" if i == 4 else f"$h_{i+1}$"
        ax.plot(x, y, "o", ms=18, color="#58D68D" if i < 4 else "#F5B041")
        ax.text(x, y - 0.55, lab, ha="center", fontsize=8)
    for i, (x, y) in enumerate(layers["out"]):
        ax.plot(x, y, "o", ms=18, color="#EC7063")
        ax.text(x + 0.55, y, f"$y_{i+1}$", ha="left", va="center", fontsize=9)
    # Algumas conexões
    for xi, yi in layers["in"][:3]:
        for xh, yh in layers["h"][:4]:
            ax.plot([xi, xh], [yi, yh], color="#BBB", lw=0.5, zorder=0)
    for xh, yh in layers["h"][:4]:
        for xo, yo in layers["out"]:
            ax.plot([xh, xo], [yh, yo], color="#BBB", lw=0.5, zorder=0)
    # Bias connections
    for xh, yh in layers["h"][:4]:
        ax.plot([layers["in"][3][0], xh], [layers["in"][3][1], yh],
                color="#F5B041", lw=0.8, zorder=0, alpha=0.7)
    ax.text(5, 0.2,
            r"Pesos ≈ $n_{\mathrm{in}}\!\cdot\!n_h + n_h\!\cdot\!n_{\mathrm{out}}$"
            "\n(+ bias em cada unidade oculta/saída)",
            ha="center", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="#FCF3CF", edgecolor="#B7950B"))

    # (0,1) fórmula de contagem
    ax = fig.add_subplot(gs[0, 1])
    ax.axis("off")
    ax.set_title("Contagem de pesos (uma camada oculta)")
    formula = (
        "Entradas: $n_{in}$  |  Ocultas: $n_h$  |  Saídas: $n_{out}$\n\n"
        "Com bias em cada neurônio (oculto e saída):\n\n"
        r"$W = (n_{in}+1)\,n_h + (n_h+1)\,n_{out}$" "\n\n"
        "Exemplo inventado: $n_{in}=4$, $n_h=5$, $n_{out}=2$\n"
        r"$\Rightarrow W = 5\cdot5 + 6\cdot2 = 25+12 = 37$" "\n\n"
        "(Não use números da lista/MLP Liver aqui.)"
    )
    ax.text(0.05, 0.9, formula, va="top", fontsize=11, transform=ax.transAxes,
            bbox=dict(boxstyle="round", facecolor="#EBF5FB", edgecolor="#2980B9"))

    # (1,0) overfitting train vs test
    ax = fig.add_subplot(gs[1, 0])
    epochs = np.arange(1, 81)
    train_loss = 1.2 * np.exp(-0.06 * epochs) + 0.05
    val_loss = 1.15 * np.exp(-0.05 * epochs) + 0.0025 * np.maximum(0, epochs - 35) ** 1.3 + 0.12
    ax.plot(epochs, train_loss, "C0-", lw=2, label="Loss treino")
    ax.plot(epochs, val_loss, "C3-", lw=2, label="Loss validação/teste")
    ax.axvline(35, color="C2", ls="--", label="Início do overfitting")
    ax.set_xlabel("Épocas →")
    ax.set_ylabel("Loss")
    ax.set_title("MLP: treino continua caindo, teste sobe")
    ax.legend(fontsize=8)

    # (1,1) preprocessing
    ax = fig.add_subplot(gs[1, 1])
    ax.axis("off")
    ax.set_title("Pré-processamento típico (MLP)")
    prep = (
        "1. Variáveis categóricas → encoding\n"
        "   (one-hot / dummy; evitar rótulos ordinais\n"
        "   se não houver ordem real)\n\n"
        "2. Variáveis contínuas → escala\n"
        "   (StandardScaler / MinMax) — ajuda o\n"
        "   gradiente e evita features dominantes\n\n"
        "3. Separar treino / validação / teste\n"
        "   antes de ajustar scalers (fit só no treino)\n\n"
        "4. Regularização / early stopping / dropout\n"
        "   para controlar overfitting"
    )
    ax.text(0.05, 0.92, prep, va="top", fontsize=10, transform=ax.transAxes,
            family="sans-serif",
            bbox=dict(boxstyle="round", facecolor="#EAFAF1", edgecolor="#1E8449"))

    save(fig, "07_mlp_overview.png")


def fig_ensemble_majority():
    """Majority-vote ensemble — diagrama conceitual (não Tabela 2)."""
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6))

    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_title("Ensemble por voto majoritário (ideia)")

    # Base learners
    preds = ["⊕", "⊕", "⊖", "⊕", "⊖"]
    for i, p in enumerate(preds):
        x = 1.2 + i * 1.5
        ax.text(x, 6.2, f"Modelo {i+1}", ha="center", fontsize=8, color="#555")
        ax.text(x, 5.2, p, ha="center", va="center", fontsize=16, fontweight="bold",
                bbox=dict(boxstyle="circle", facecolor="#D6EAF8" if p == "⊕" else "#FADBD8",
                          edgecolor="#555"))
        ax.annotate("", xy=(5, 2.8), xytext=(x, 4.6),
                    arrowprops=dict(arrowstyle="->", color="#888", lw=1.2))

    ax.text(5, 2.0, "Voto majoritário\n(⊕: 3  |  ⊖: 2)  →  ⊕",
            ha="center", va="center", fontsize=12, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#D5F5E3", edgecolor="#1E8449", lw=2))
    ax.text(5, 0.5,
            "Cada modelo erra de forma diferente → média/voto reduz variance.",
            ha="center", fontsize=9, color="#333")

    ax = axes[1]
    # Simulação esquemática: acurácia individual vs ensemble
    rng = np.random.default_rng(0)
    n_models = np.arange(1, 16)
    # Accuracy sobe e estabiliza (conceitual)
    single = 0.72 + rng.normal(0, 0.01, size=n_models.size)
    ens = 0.72 + 0.12 * (1 - np.exp(-0.35 * (n_models - 1))) + rng.normal(0, 0.005, size=n_models.size)
    ax.plot(n_models, single, "C0--", marker="o", label="Modelo único (média ~)")
    ax.plot(n_models, ens, "C2-", marker="s", label="Ensemble (voto)")
    ax.set_xlabel("Nº de classificadores no ensemble →")
    ax.set_ylabel("Acurácia (esquemática)")
    ax.set_title("Efeito típico do voto (exemplo inventado)")
    ax.set_ylim(0.65, 0.90)
    ax.legend(loc="lower right")
    ax.text(0.5, 0.05,
            "Diagrama conceitual — NÃO calcula Tabela 2 da lista.",
            transform=ax.transAxes, fontsize=8, color="#922B21",
            ha="left", va="bottom")

    save(fig, "08_ensemble_majority.png")


def main():
    fig_bias_variance()
    fig_naive_bayes()
    fig_entropy_ig()
    fig_decision_tree_pruning()
    fig_confusion_matrix()
    fig_knn_normalization()
    fig_mlp_overview()
    fig_ensemble_majority()
    print("Done. Figures in:", OUT)


if __name__ == "__main__":
    main()
