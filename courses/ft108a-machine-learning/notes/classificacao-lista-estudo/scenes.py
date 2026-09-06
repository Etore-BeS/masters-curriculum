"""
FT108A — Cenas Manim (estilo 3Blue1Brown) para estudo de classificação.
Rótulos em português. Sem MathTex (evita dependência de pacotes LaTeX).
Não resolve exercícios da lista.
"""

from manim import *
import numpy as np

AZUL = BLUE_C
VERMELHO = RED_C
VERDE = GREEN_C
AMARELO = YELLOW_C
CINZA = GREY_B
LARANJA = ORANGE


class BiasVariance(Scene):
    """Viés vs variância: underfit, bom ajuste, overfit."""

    def construct(self):
        titulo = Text("Viés × Variância", font_size=36).to_edge(UP)
        self.play(Write(titulo))

        axes = Axes(
            x_range=[-0.5, 4.5, 1],
            y_range=[-0.5, 3.5, 1],
            x_length=5.5,
            y_length=3.8,
            tips=False,
        ).shift(DOWN * 0.3)

        rng = np.random.default_rng(7)
        xs = np.array([0.4, 0.9, 1.4, 1.9, 2.4, 2.9, 3.4, 3.9])
        ys = 0.35 * xs ** 2 - 0.9 * xs + 1.8 + rng.normal(0, 0.18, size=len(xs))
        dots = VGroup(*[
            Dot(axes.c2p(float(x), float(y)), color=AZUL, radius=0.07)
            for x, y in zip(xs, ys)
        ])

        self.play(Create(axes), FadeIn(dots))
        self.wait(0.3)

        under = axes.plot(lambda x: 1.4 + 0.08 * x, x_range=[0.2, 4.2], color=VERMELHO)
        lab_u = Text("Subajuste\n(alto viés)", font_size=22, color=VERMELHO).next_to(axes, RIGHT).shift(UP * 1.2)
        self.play(Create(under), FadeIn(lab_u))
        self.wait(0.8)
        self.play(FadeOut(under), FadeOut(lab_u))

        good = axes.plot(lambda x: 0.35 * x ** 2 - 0.9 * x + 1.8, x_range=[0.2, 4.2], color=VERDE)
        lab_g = Text("Bom ajuste\n(equilíbrio)", font_size=22, color=VERDE).next_to(axes, RIGHT).shift(UP * 1.2)
        self.play(Create(good), FadeIn(lab_g))
        self.wait(0.8)
        self.play(FadeOut(good), FadeOut(lab_g))

        over = axes.plot(
            lambda x: 0.35 * x ** 2 - 0.9 * x + 1.8 + 0.35 * np.sin(6 * x),
            x_range=[0.2, 4.2],
            color=LARANJA,
        )
        lab_o = Text("Sobreajuste\n(alta variância)", font_size=22, color=LARANJA).next_to(axes, RIGHT).shift(UP * 1.2)
        self.play(Create(over), FadeIn(lab_o))
        self.wait(1.2)
        self.wait(0.5)  # hold final frame for PNG


class EntropyGain(Scene):
    """Entropia e ganho de informação: pureza do split."""

    def construct(self):
        titulo = Text("Entropia e ganho de informação", font_size=32).to_edge(UP)
        self.play(Write(titulo))

        formula = Text("H = - Σ pk log2(pk)", font_size=30).next_to(titulo, DOWN, buff=0.35)
        self.play(Write(formula))

        parent = RoundedRectangle(width=3.2, height=1.2, corner_radius=0.15, color=CINZA)
        parent_dots = VGroup(
            *[Dot(color=AZUL, radius=0.08) for _ in range(4)],
            *[Dot(color=VERMELHO, radius=0.08) for _ in range(4)],
        ).arrange_in_grid(rows=2, cols=4, buff=0.15)
        parent_group = VGroup(parent, parent_dots).move_to(ORIGIN + UP * 0.3)
        parent_dots.move_to(parent.get_center())
        h_pai = Text("H alto (impuro)", font_size=20, color=AMARELO).next_to(parent_group, LEFT)

        self.play(FadeIn(parent_group), FadeIn(h_pai))
        self.wait(0.5)

        left = RoundedRectangle(width=2.4, height=1.0, corner_radius=0.12, color=AZUL)
        left_dots = VGroup(*[Dot(color=AZUL, radius=0.08) for _ in range(4)]).arrange(RIGHT, buff=0.12)
        left_g = VGroup(left, left_dots).move_to(LEFT * 2.8 + DOWN * 1.8)
        left_dots.move_to(left.get_center())

        right = RoundedRectangle(width=2.4, height=1.0, corner_radius=0.12, color=VERMELHO)
        right_dots = VGroup(*[Dot(color=VERMELHO, radius=0.08) for _ in range(4)]).arrange(RIGHT, buff=0.12)
        right_g = VGroup(right, right_dots).move_to(RIGHT * 2.8 + DOWN * 1.8)
        right_dots.move_to(right.get_center())

        line_l = Line(parent.get_bottom(), left.get_top(), color=CINZA)
        line_r = Line(parent.get_bottom(), right.get_top(), color=CINZA)

        self.play(Create(line_l), Create(line_r), FadeIn(left_g), FadeIn(right_g))
        h_folhas = Text("H ≈ 0 (puros) → ganho alto", font_size=22, color=VERDE).to_edge(DOWN)
        self.play(FadeIn(h_folhas))
        self.wait(1.2)
        self.wait(0.5)  # hold final frame for PNG


class TreePrune(Scene):
    """Poda de árvore: antes (complexa) e depois (simplificada)."""

    def construct(self):
        titulo = Text("Poda de árvore de decisão", font_size=34).to_edge(UP)
        self.play(Write(titulo))

        def node(label, color=AZUL, pos=ORIGIN):
            c = Circle(radius=0.28, color=color, fill_opacity=0.25)
            t = Text(label, font_size=16)
            return VGroup(c, t).move_to(pos)

        root = node("A?", AZUL, UP * 1.5)
        n1 = node("B?", VERDE, LEFT * 2.2 + UP * 0.4)
        n2 = node("C?", VERDE, RIGHT * 2.2 + UP * 0.4)
        l1 = node("sim", VERMELHO, LEFT * 3.2 + DOWN * 0.8)
        l2 = node("nao", VERMELHO, LEFT * 1.2 + DOWN * 0.8)
        l3 = node("D?", LARANJA, RIGHT * 1.2 + DOWN * 0.8)
        l4 = node("sim", VERMELHO, RIGHT * 3.2 + DOWN * 0.8)
        l5 = node("sim", CINZA, RIGHT * 0.4 + DOWN * 2.0)
        l6 = node("nao", CINZA, RIGHT * 2.0 + DOWN * 2.0)

        edges = VGroup(
            Line(root.get_bottom(), n1.get_top(), color=CINZA),
            Line(root.get_bottom(), n2.get_top(), color=CINZA),
            Line(n1.get_bottom(), l1.get_top(), color=CINZA),
            Line(n1.get_bottom(), l2.get_top(), color=CINZA),
            Line(n2.get_bottom(), l3.get_top(), color=CINZA),
            Line(n2.get_bottom(), l4.get_top(), color=CINZA),
            Line(l3.get_bottom(), l5.get_top(), color=CINZA),
            Line(l3.get_bottom(), l6.get_top(), color=CINZA),
        )
        tree_before = VGroup(edges, root, n1, n2, l1, l2, l3, l4, l5, l6)
        lab_antes = Text("Antes (complexa)", font_size=22, color=LARANJA).next_to(tree_before, DOWN)

        self.play(FadeIn(tree_before), FadeIn(lab_antes))
        self.wait(0.9)

        prune_box = SurroundingRectangle(VGroup(l3, l5, l6), color=VERMELHO, buff=0.15)
        lab_poda = Text("ramos ruidosos", font_size=18, color=VERMELHO).next_to(prune_box, RIGHT)
        self.play(Create(prune_box), FadeIn(lab_poda))
        self.wait(0.6)

        leaf = node("sim", VERDE, RIGHT * 2.2 + DOWN * 0.8)
        after_edges = VGroup(
            Line(root.get_bottom(), n1.get_top(), color=CINZA),
            Line(root.get_bottom(), n2.get_top(), color=CINZA),
            Line(n1.get_bottom(), l1.get_top(), color=CINZA),
            Line(n1.get_bottom(), l2.get_top(), color=CINZA),
            Line(n2.get_bottom(), leaf.get_top(), color=CINZA),
            Line(n2.get_bottom(), l4.get_top(), color=CINZA),
        )
        lab_depois = Text("Depois (podada)", font_size=22, color=VERDE).next_to(
            VGroup(after_edges, root, n1, n2, l1, l2, leaf, l4), DOWN
        )

        self.play(
            FadeOut(prune_box), FadeOut(lab_poda), FadeOut(lab_antes),
            FadeOut(VGroup(l3, l5, l6)),
            ReplacementTransform(edges, after_edges),
            FadeIn(leaf),
            FadeIn(lab_depois),
        )
        nota = Text("menos complexidade → menos overfitting", font_size=20).to_edge(DOWN)
        self.play(FadeIn(nota))
        self.wait(1.2)
        self.wait(0.5)  # hold final frame for PNG


class KNNScale(Scene):
    """k-NN: distância distorcida sem normalização."""

    def construct(self):
        titulo = Text("k-NN e escala das features", font_size=32).to_edge(UP)
        self.play(Write(titulo))

        ax1 = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 100, 20],
            x_length=4.2,
            y_length=3.2,
            tips=False,
            axis_config={"include_numbers": False},
        ).shift(LEFT * 3.3 + DOWN * 0.2)
        lab1 = Text("Sem escala", font_size=22, color=VERMELHO).next_to(ax1, UP, buff=0.15)
        xl1 = Text("idade", font_size=14).next_to(ax1.x_axis, DOWN, buff=0.1)
        yl1 = Text("renda", font_size=14).next_to(ax1.y_axis, LEFT, buff=0.1).rotate(PI / 2)

        q1 = Dot(ax1.c2p(5, 50), color=AMARELO, radius=0.1)
        a1 = Dot(ax1.c2p(5.2, 55), color=AZUL, radius=0.08)
        b1 = Dot(ax1.c2p(8.5, 52), color=VERDE, radius=0.08)
        circ1 = Circle(radius=0.55, color=LARANJA).move_to(q1.get_center())

        self.play(Create(ax1), FadeIn(lab1), FadeIn(xl1), FadeIn(yl1))
        self.play(FadeIn(q1), FadeIn(a1), FadeIn(b1), Create(circ1))
        warn = Text("eixo Y domina a distância", font_size=18, color=VERMELHO).next_to(ax1, DOWN)
        self.play(FadeIn(warn))

        ax2 = Axes(
            x_range=[0, 1.2, 0.2],
            y_range=[0, 1.2, 0.2],
            x_length=4.2,
            y_length=3.2,
            tips=False,
            axis_config={"include_numbers": False},
        ).shift(RIGHT * 3.3 + DOWN * 0.2)
        lab2 = Text("Com escala (0–1)", font_size=22, color=VERDE).next_to(ax2, UP, buff=0.15)

        q2 = Dot(ax2.c2p(0.5, 0.5), color=AMARELO, radius=0.1)
        a2 = Dot(ax2.c2p(0.52, 0.55), color=AZUL, radius=0.08)
        b2 = Dot(ax2.c2p(0.85, 0.52), color=VERDE, radius=0.08)
        circ2 = Circle(radius=0.45, color=VERDE).move_to(q2.get_center())

        self.play(Create(ax2), FadeIn(lab2))
        self.play(FadeIn(q2), FadeIn(a2), FadeIn(b2), Create(circ2))
        ok = Text("vizinhos refletem similaridade real", font_size=18, color=VERDE).next_to(ax2, DOWN)
        self.play(FadeIn(ok))
        self.wait(1.2)
        self.wait(0.5)  # hold final frame for PNG


class MLPForward(Scene):
    """MLP: passagem forward esquemática."""

    def construct(self):
        titulo = Text("MLP — forward pass", font_size=34).to_edge(UP)
        self.play(Write(titulo))

        def layer(n, x, color, labels=None):
            nodes = VGroup(*[
                Circle(radius=0.28, color=color, fill_opacity=0.3)
                for _ in range(n)
            ]).arrange(DOWN, buff=0.45).move_to(RIGHT * x)
            if labels:
                for node, lab in zip(nodes, labels):
                    node.add(Text(lab, font_size=16).move_to(node.get_center()))
            return nodes

        inp = layer(3, -4.2, AZUL, ["x1", "x2", "x3"])
        hid = layer(4, 0, VERDE, ["h1", "h2", "h3", "h4"])
        out = layer(2, 4.2, VERMELHO, ["y1", "y2"])

        lab_i = Text("entrada", font_size=18).next_to(inp, DOWN)
        lab_h = Text("oculta", font_size=18).next_to(hid, DOWN)
        lab_o = Text("saída", font_size=18).next_to(out, DOWN)

        edges = VGroup()
        for a in inp:
            for b in hid:
                edges.add(Line(a.get_right(), b.get_left(), stroke_width=1.2, color=CINZA))
        for a in hid:
            for b in out:
                edges.add(Line(a.get_right(), b.get_left(), stroke_width=1.2, color=CINZA))

        self.play(FadeIn(inp), FadeIn(lab_i))
        self.play(LaggedStart(*[Create(e) for e in edges[:12]], lag_ratio=0.03), FadeIn(hid), FadeIn(lab_h))
        self.play(LaggedStart(*[Create(e) for e in edges[12:]], lag_ratio=0.05), FadeIn(out), FadeIn(lab_o))

        formula = Text("h = σ(W1 x + b1)   ŷ = σ(W2 h + b2)", font_size=24).to_edge(DOWN)
        self.play(Write(formula))

        pulse = Dot(inp[1].get_center(), color=AMARELO, radius=0.12)
        self.play(FadeIn(pulse))
        self.play(pulse.animate.move_to(hid[1].get_center()), run_time=0.7)
        self.play(pulse.animate.move_to(out[0].get_center()), run_time=0.7)
        self.wait(0.8)
        self.wait(0.5)  # hold final frame for PNG


class OverfitGap(Scene):
    """Acurácia treino alta × teste baixa: gap de overfitting."""

    def construct(self):
        titulo = Text("Gap de overfitting", font_size=34).to_edge(UP)
        self.play(Write(titulo))

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0.4, 1.05, 0.1],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": False},
        ).shift(DOWN * 0.15)
        xlab = Text("complexidade / épocas", font_size=18).next_to(axes.x_axis, DOWN)
        ylab = Text("acurácia", font_size=18).next_to(axes.y_axis, LEFT).rotate(PI / 2)

        train = axes.plot(lambda x: 0.55 + 0.42 * (1 - np.exp(-0.55 * x)), x_range=[0.2, 9.5], color=AZUL)

        def test_fn(x):
            base = 0.55 + 0.32 * (1 - np.exp(-0.55 * x))
            if x > 3:
                return base - 0.012 * (x - 3) ** 2
            return base

        test = axes.plot(test_fn, x_range=[0.2, 9.5], color=VERMELHO)

        leg = VGroup(
            Text("treino", font_size=20, color=AZUL),
            Text("teste", font_size=20, color=VERMELHO),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR).shift(DOWN * 0.8 + LEFT * 0.3)

        self.play(Create(axes), FadeIn(xlab), FadeIn(ylab))
        self.play(Create(train), FadeIn(leg[0]))
        self.play(Create(test), FadeIn(leg[1]))

        x_gap = 8.0
        p_tr = axes.c2p(x_gap, 0.55 + 0.42 * (1 - np.exp(-0.55 * x_gap)))
        p_te = axes.c2p(x_gap, test_fn(x_gap))
        brace = BraceBetweenPoints(p_tr, p_te, direction=RIGHT, color=AMARELO)
        gap_lab = Text("gap", font_size=22, color=AMARELO).next_to(brace, RIGHT)
        self.play(GrowFromCenter(brace), FadeIn(gap_lab))
        nota = Text("treino ↑  teste ↓  → sobreajuste", font_size=22).to_edge(DOWN)
        self.play(FadeIn(nota))
        self.wait(1.2)
        self.wait(0.5)  # hold final frame for PNG


class MajorityVote(Scene):
    """Ensemble: voto majoritário de 3 classificadores."""

    def construct(self):
        titulo = Text("Ensemble — voto majoritário", font_size=32).to_edge(UP)
        self.play(Write(titulo))

        def clf_box(name, pred, color):
            box = RoundedRectangle(width=2.6, height=1.3, corner_radius=0.15, color=color, fill_opacity=0.15)
            t1 = Text(name, font_size=20)
            t2 = Text(f"pred: {pred}", font_size=22, color=color)
            g = VGroup(t1, t2).arrange(DOWN, buff=0.15)
            return VGroup(box, g)

        c1 = clf_box("Classificador 1", "A", AZUL).move_to(LEFT * 4 + UP * 0.8)
        c1[1].move_to(c1[0].get_center())
        c2 = clf_box("Classificador 2", "A", VERDE).move_to(ORIGIN + UP * 0.8)
        c2[1].move_to(c2[0].get_center())
        c3 = clf_box("Classificador 3", "B", VERMELHO).move_to(RIGHT * 4 + UP * 0.8)
        c3[1].move_to(c3[0].get_center())

        self.play(FadeIn(c1), FadeIn(c2), FadeIn(c3))

        vote_pos = DOWN * 1.5
        arrows = VGroup(
            Arrow(c1.get_bottom(), vote_pos + UP * 0.7, buff=0.15, color=CINZA),
            Arrow(c2.get_bottom(), vote_pos + UP * 0.7, buff=0.15, color=CINZA),
            Arrow(c3.get_bottom(), vote_pos + UP * 0.7, buff=0.15, color=CINZA),
        )
        self.play(*[Create(a) for a in arrows])

        vote = RoundedRectangle(width=3.4, height=1.2, corner_radius=0.15, color=AMARELO, fill_opacity=0.2)
        vote.move_to(vote_pos)
        vote_txt = Text("Voto: A (2×1)", font_size=26, color=AMARELO).move_to(vote.get_center())
        self.play(FadeIn(vote), Write(vote_txt))

        nota = Text("diversidade + agregação → mais robustez", font_size=22).to_edge(DOWN)
        self.play(FadeIn(nota))
        self.wait(1.2)
        self.wait(0.5)  # hold final frame for PNG


class NaiveBayesProduct(Scene):
    """Naïve Bayes: produto de verossimilhanças (opcional)."""

    def construct(self):
        titulo = Text("Naïve Bayes — produto de verossimilhanças", font_size=26).to_edge(UP)
        self.play(Write(titulo))

        formula = Text("P(y|x) ∝ P(y) · Πj P(xj | y)", font_size=30).next_to(titulo, DOWN, buff=0.4)
        self.play(Write(formula))

        prior = Text("P(y)", font_size=28, color=AMARELO).move_to(LEFT * 4.5 + DOWN * 0.3)
        likes = VGroup(
            Text("P(x1|y)", font_size=24, color=AZUL),
            Text("P(x2|y)", font_size=24, color=AZUL),
            Text("P(x3|y)", font_size=24, color=AZUL),
        ).arrange(RIGHT, buff=0.55).move_to(ORIGIN + DOWN * 0.3)

        times = Text("×", font_size=36).next_to(prior, RIGHT, buff=0.35)
        # place × between likelihoods
        times2 = Text("×", font_size=36).move_to(likes[0].get_center() * 0.5 + likes[1].get_center() * 0.5)
        times3 = Text("×", font_size=36).move_to(likes[1].get_center() * 0.5 + likes[2].get_center() * 0.5)

        self.play(FadeIn(prior), FadeIn(times), FadeIn(likes))

        arrow = Arrow(likes.get_bottom() + DOWN * 0.1, DOWN * 2.0, color=VERDE)
        result = Text("ŷ = argmax_y ...", font_size=28, color=VERDE).next_to(arrow, DOWN)
        self.play(Create(arrow), Write(result))

        nota = Text("hipótese: features cond. independentes dado y", font_size=20).to_edge(DOWN)
        self.play(FadeIn(nota))
        self.wait(1.2)
        self.wait(0.5)  # hold final frame for PNG
