from manim import *
import math

config.tex_compiler = "xelatex"
config.tex_output_format = ".svg"

BG = WHITE
FG = BLACK


def apply_light_theme(mobj: Mobject) -> Mobject:
    if isinstance(mobj, (Text, MarkupText, Tex, MathTex)):
        mobj.set_color(FG)
        return mobj
    if isinstance(mobj, VMobject):
        mobj.set_stroke(color=FG)
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


class NestedFunctionDemo(LightScene):
    def construct(self):
        title = Text("Nested functions (composition in neural nets)", font_size=34).to_edge(UP)
        self.add_light(title)

        # A fixed "slot" so the formula never jumps / disappears
        formula_anchor = Dot(radius=0.001).next_to(title, DOWN, buff=0.45)
        # start formula
        current = Tex(r"$f(x)=x$").scale(1.05).move_to(formula_anchor)
        current.apply_to_family(apply_light_theme)
        current.set_z_index(10)

        self.play(FadeIn(current, shift=UP*0.1))
        self.wait(0.3)

        def update_formula(new_tex: str, scale: float = 1.05, wait: float = 0.4):
            nonlocal current
            nxt = Tex(new_tex).scale(scale).move_to(formula_anchor)
            nxt.apply_to_family(apply_light_theme)
            nxt.set_z_index(10)
            # crossfade (no blinking)
            self.play(FadeOut(current, shift=UP*0.05), FadeIn(nxt, shift=UP*0.05), run_time=0.7)
            current = nxt
            self.wait(wait)

        # -------------------------
        # small pipeline
        # -------------------------
        y_level = 0.2

        def block(label_tex: str):
            box = RoundedRectangle(corner_radius=0.2, width=3.3, height=1.0)
            lab = Tex(label_tex).scale(0.95)
            grp = VGroup(box, lab)
            grp.apply_to_family(apply_light_theme)
            lab.move_to(box.get_center())
            return grp

        x_in = Tex(r"$x$").scale(1.2).move_to(LEFT*5 + DOWN*y_level)
        x_in.apply_to_family(apply_light_theme)

        self.play(Write(x_in))
        self.wait(0.2)

        # Iteration 1: linear neuron
        lin1 = block(r"$z_1=w_1x+b_1$")
        lin1.move_to(LEFT*1.8 + DOWN*y_level)

        a_in = Arrow(x_in.get_right(), lin1.get_left(), buff=0.2)
        a_in.apply_to_family(apply_light_theme)

        y_out = Tex(r"$f(x)$").scale(1.2).move_to(RIGHT*4.3 + DOWN*y_level)
        y_out.apply_to_family(apply_light_theme)

        a_out = Arrow(lin1.get_right(), y_out.get_left(), buff=0.2)
        a_out.apply_to_family(apply_light_theme)

        self.play(Create(a_in), FadeIn(lin1, shift=DOWN*0.2), Create(a_out), Write(y_out))
        update_formula(r"$f(x)=w_1x+b_1$")

        # Iteration 2: activation
        act1 = block(r"$a_1=\sigma(z_1)$")
        act1.move_to(RIGHT*1.1 + DOWN*y_level)

        # replace lin->out with lin->act->out
        a_lin_act = Arrow(lin1.get_right(), act1.get_left(), buff=0.2)
        a_lin_act.apply_to_family(apply_light_theme)
        a_act_out = Arrow(act1.get_right(), y_out.get_left(), buff=0.2)
        a_act_out.apply_to_family(apply_light_theme)

        self.play(FadeOut(a_out), FadeIn(act1, shift=DOWN*0.2), Create(a_lin_act), Create(a_act_out))
        self.play(Indicate(act1[0], scale_factor=1.05), run_time=0.6)
        update_formula(r"$f(x)=\sigma\!\left(w_1x+b_1\right)$", scale=1.03)

        # Iteration 3: another linear layer (nested)
        lin2 = block(r"$z_2=w_2a_1+b_2$")
        lin2.move_to(RIGHT*3.6 + DOWN*y_level)

        # move output a bit to the right
        self.play(y_out.animate.shift(RIGHT*1.6), run_time=0.6)

        # replace act->out with act->lin2->out
        self.play(FadeOut(a_act_out), FadeIn(lin2, shift=DOWN*0.2))
        a_act_lin2 = Arrow(act1.get_right(), lin2.get_left(), buff=0.2)
        a_act_lin2.apply_to_family(apply_light_theme)
        a_lin2_out = Arrow(lin2.get_right(), y_out.get_left(), buff=0.2)
        a_lin2_out.apply_to_family(apply_light_theme)

        self.play(Create(a_act_lin2), Create(a_lin2_out))
        self.play(Indicate(lin2[0], scale_factor=1.05), run_time=0.6)

        update_formula(
            r"$f(x)=\sigma\!\left(w_2\,\sigma\!\left(w_1x+b_1\right)+b_2\right)$",
            scale=0.98,
            wait=0.6
        )

        outro = Text("Neural nets = nested functions (composition)", font_size=28).set_color(FG).to_edge(DOWN)
        self.play(Write(outro))
        self.wait(1.0)