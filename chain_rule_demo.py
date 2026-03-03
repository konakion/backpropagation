from manim import *
import math

# Use xelatex + svg to avoid dvips/dvisvgm injection issues
config.tex_compiler = "xelatex"
config.tex_output_format = ".svg"

# --- Theme: white background, black strokes/text ---
BG = WHITE
FG = BLACK


def apply_light_theme(mobj: Mobject) -> Mobject:
    if isinstance(mobj, (Text, MarkupText, Tex, MathTex)):
        mobj.set_color(FG)
        return mobj
    if isinstance(mobj, VMobject):
        mobj.set_stroke(color=FG)
        # keep fills off for clean line-art
        if mobj.get_fill_opacity() > 0:
            mobj.set_fill(color=FG, opacity=0)
        return mobj
    return mobj


class LightScene(Scene):
    def setup(self):
        self.camera.background_color = BG

    def add_light(self, *mobjects):
        for m in mobjects:
            m.apply_to_family(apply_light_theme)
        self.add(*mobjects)


# --- Helper math functions (for consistent numeric display) ---
def sigmoid(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-z))


def r(x: float, nd: int = 4) -> str:
    # rounded string
    return f"{x:.{nd}f}"


class ChainRuleBackpropDemo(LightScene):
    def construct(self):
        # =========================
        # 0) Title
        # =========================
        title = Text("Backprop (Chain Rule) on a single neuron", font_size=36).to_edge(UP)
        self.add_light(title)

        # =========================
        # 1) Tiny network diagram
        # =========================
        x_node = Circle(radius=0.22).move_to(LEFT * 5 + DOWN * 0.2)
        n_node = Circle(radius=0.28).move_to(LEFT * 1.5 + DOWN * 0.2)
        y_node = Circle(radius=0.22).move_to(RIGHT * 2.2 + UP * 0.8)
        L_node = RoundedRectangle(corner_radius=0.15, height=0.8, width=1.2).move_to(
            RIGHT * 2.6 + DOWN * 1.2
        )

        x_lab = MathTex("x").next_to(x_node, DOWN, buff=0.12)
        n_lab = MathTex(r"z=wx+b").next_to(n_node, DOWN, buff=0.12)
        yhat_lab = MathTex(r"\hat{y}=\sigma(z)").next_to(n_node, UP, buff=0.18)
        y_lab = MathTex("y").next_to(y_node, RIGHT, buff=0.15)
        L_lab = MathTex(r"L=\frac{1}{2}(\hat{y}-y)^2").scale(0.8).move_to(L_node)

        # Edges
        a1 = Arrow(x_node.get_right(), n_node.get_left(), buff=0.08)
        a2 = Arrow(n_node.get_right(), y_node.get_left(), buff=0.08)
        a3 = Arrow(y_node.get_bottom(), L_node.get_top(), buff=0.08)
        a4 = Arrow(n_node.get_right(), L_node.get_left(), buff=0.08)  # yhat influences L

        net = VGroup(
            x_node,
            n_node,
            y_node,
            L_node,
            a1,
            a2,
            a3,
            a4,
            x_lab,
            n_lab,
            yhat_lab,
            y_lab,
            L_lab,
        )
        net.shift(DOWN * 0.15)
        net.apply_to_family(apply_light_theme)

        self.play(FadeIn(net), run_time=0.8)
        self.wait(0.3)

        # =========================
        # 2) Show model equations
        # =========================
        eqs = VGroup(
            MathTex(r"z = wx + b"),
            MathTex(r"\hat{y}=\sigma(z)=\frac{1}{1+e^{-z}}"),
            MathTex(r"L=\frac{1}{2}(\hat{y}-y)^2"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(UL).shift(DOWN * 0.8)

        eqs.apply_to_family(apply_light_theme)
        self.play(Write(eqs), run_time=1.0)
        self.wait(0.3)

        # =========================
        # 3) Chain rule formula (with factor highlights)
        # =========================
        chain_tex = (
            r"$\frac{\partial L}{\partial w} = "
            r"\frac{\partial L}{\partial \hat y} \cdot "
            r"\frac{\partial \hat y}{\partial z} \cdot "
            r"\frac{\partial z}{\partial w}$"
        )
        chain = Tex(chain_tex).scale(0.95).to_edge(RIGHT).shift(DOWN * 0.2)
        chain.apply_to_family(apply_light_theme)

        subtitle = Text("Chain rule", font_size=26).next_to(chain, UP, buff=0.25)
        subtitle.set_color(FG)

        # Separate factor labels (safer to indicate these than indexing chain submobjects)
        t1 = Tex(r"$\frac{\partial L}{\partial \hat y}$").scale(0.9)
        t2 = Tex(r"$\frac{\partial \hat y}{\partial z}$").scale(0.9)
        t3 = Tex(r"$\frac{\partial z}{\partial w}$").scale(0.9)

        dot1 = Tex(r"$\cdot$").scale(0.9)
        dot2 = Tex(r"$\cdot$").scale(0.9)

        factors_row = VGroup(t1, dot1, t2, dot2, t3).arrange(RIGHT, buff=0.25)
        factors_row.apply_to_family(apply_light_theme)
        factors_row.next_to(chain, DOWN, buff=0.35).align_to(chain, LEFT)

        self.play(Write(subtitle), Write(chain), run_time=1.0)
        self.play(FadeIn(factors_row), run_time=0.5)

        self.play(Indicate(t1, scale_factor=1.1))
        self.play(Indicate(t2, scale_factor=1.1))
        self.play(Indicate(t3, scale_factor=1.1))
        self.wait(0.2)

        # =========================
        # 4) Choose simple numbers
        # =========================
        x = 1.0
        w = 0.5
        b = 0.0
        y = 1.0

        z = w * x + b
        yhat = sigmoid(z)
        L = 0.5 * (yhat - y) ** 2

        vals = VGroup(
            MathTex(rf"x={r(x,1)}\quad w={r(w,1)}\quad b={r(b,1)}\quad y={r(y,1)}")
        ).scale(0.9).next_to(eqs, DOWN, buff=0.35).align_to(eqs, LEFT)

        vals.apply_to_family(apply_light_theme)

        self.play(Write(vals), run_time=0.8)
        self.wait(0.2)

        # =========================
        # 5) Forward pass with numbers
        # =========================
        fwd_title = Text("Forward pass (numbers)", font_size=26).set_color(FG).to_edge(DOWN)
        self.play(Write(fwd_title))

        # Build numeric lines without rf-strings inside TeX to avoid brace issues
        fwd1 = MathTex(
            r"z = wx + b = ("
            + r(w, 1)
            + r")("
            + r(x, 1)
            + r") + ("
            + r(b, 1)
            + r") = "
            + r(z)
        )

        fwd2 = MathTex(r"\hat{y} = \sigma(z) = \sigma(" + r(z) + r") = " + r(yhat))

        fwd3 = MathTex(
            r"L = \frac{1}{2}(\hat{y}-y)^2 = \frac{1}{2}("
            + r(yhat)
            + r"-"
            + r(y, 1)
            + r")^2 = "
            + r(L)
        )

        fwd = VGroup(fwd1, fwd2, fwd3).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        fwd.scale(0.85).next_to(chain, DOWN, buff=0.35).align_to(chain, LEFT)

        fwd.apply_to_family(apply_light_theme)
        self.play(Write(fwd), run_time=1.2)
        self.wait(0.6)

        # =========================
        # 6) Backprop: term-by-term (chain rule factors)
        # =========================
        self.play(FadeOut(fwd_title), run_time=0.2)
        bwd_title = Text("Backward pass (chain rule factors)", font_size=26).set_color(FG).to_edge(
            DOWN
        )
        self.play(Write(bwd_title))

        dL_dyhat = yhat - y
        dyhat_dz = yhat * (1 - yhat)  # sigmoid derivative
        dz_dw = x
        dL_dw = dL_dyhat * dyhat_dz * dz_dw

        factor1 = Tex(
            r"$\frac{\partial L}{\partial \hat y} = (\hat y - y) = "
            + r(yhat)
            + r" - "
            + r(y, 1)
            + r" = "
            + r(dL_dyhat)
            + r"$"
        ).scale(0.85)
        factor1.apply_to_family(apply_light_theme)

        factor2 = Tex(
            r"$\frac{\partial \hat y}{\partial z} = \hat y(1-\hat y) = "
            + r(yhat)
            + r"(1-"
            + r(yhat)
            + r") = "
            + r(dyhat_dz)
            + r"$"
        ).scale(0.85)
        factor2.apply_to_family(apply_light_theme)

        factor3 = Tex(r"$\frac{\partial z}{\partial w} = x = " + r(dz_dw, 1) + r"$").scale(0.85)
        factor3.apply_to_family(apply_light_theme)

        factors = VGroup(factor1, factor2, factor3).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        factors.next_to(chain, DOWN, buff=0.35).align_to(chain, LEFT)

        self.play(Indicate(t1, scale_factor=1.1))
        self.play(Write(factor1), run_time=1.0)
        self.wait(0.3)

        self.play(Indicate(t2, scale_factor=1.1))
        self.play(Write(factor2), run_time=1.0)
        self.wait(0.3)

        self.play(Indicate(t3, scale_factor=1.1))
        self.play(Write(factor3), run_time=0.8)
        self.wait(0.4)

        # =========================
        # 7) Multiply everything → final gradient
        # =========================
        final = Tex(
            r"$\frac{\partial L}{\partial w}"
            + r" = ("
            + r(dL_dyhat)
            + r") \cdot ("
            + r(dyhat_dz)
            + r") \cdot ("
            + r(dz_dw, 1)
            + r") = "
            + r(dL_dw)
            + r"$"
        ).scale(0.95).to_edge(DOWN).shift(UP * 0.2)
        final.apply_to_family(apply_light_theme)

        self.play(Write(final), run_time=1.0)
        self.wait(0.8)

        # =========================
        # 8) Optional: one SGD update step
        # =========================
        eta = 0.5
        w_new = w - eta * dL_dw

        update = Tex(
            r"$w \leftarrow w - \eta \frac{\partial L}{\partial w}"
            + r" = "
            + r(w, 1)
            + r" - "
            + r(eta, 1)
            + r"\cdot "
            + r(dL_dw)
            + r" = "
            + r(w_new)
            + r"$"
        ).scale(0.8).next_to(final, UP, buff=0.25).align_to(final, LEFT)
        update.apply_to_family(apply_light_theme)

        self.play(Write(update), run_time=1.0)
        self.wait(1.2)

        # wrap
        self.play(FadeOut(update), FadeOut(bwd_title))
        self.wait(0.3)