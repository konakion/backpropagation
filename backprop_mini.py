from manim import *

BG = WHITE
FG = BLACK

def apply_light_theme(mobj: Mobject) -> Mobject:
    """
    Setzt für (fast) alles einen schwarzen 'Look':
    - Stroke/Lines: schwarz
    - Text/MathTex: schwarz
    - Fills: transparent (damit es wie Line-Art wirkt)
    """
    # Text / Tex / MathTex
    if isinstance(mobj, (Text, MarkupText, Tex, MathTex)):
        mobj.set_color(FG)
        return mobj

    # Vektorobjekte (Circle, Arrow, Line, Rectangle, etc.)
    if isinstance(mobj, VMobject):
        mobj.set_stroke(color=FG)
        # Oft willst du Fill aus, damit es clean bleibt:
        if mobj.get_fill_opacity() > 0:
            mobj.set_fill(color=FG, opacity=0)  # nur Stroke sichtbar
        return mobj

    return mobj

class LightScene(Scene):
    def setup(self):
        self.camera.background_color = BG

    def add_light(self, *mobjects):
        for m in mobjects:
            m.apply_to_family(apply_light_theme)
        self.add(*mobjects)


from manim import *

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

class BackpropMini(Scene):
    def construct(self):
        title = Text("Backpropagation = Forward + Backward + Update", font_size=36)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))

        # --- Nodes ---
        x = Circle(radius=0.45).shift(LEFT*5)
        x_t = MathTex("x").move_to(x)
        
        w = Circle(radius=0.45).shift(LEFT*2.8 + UP*1.2)
        w_t = MathTex("w").move_to(w)

        b = Circle(radius=0.45).shift(LEFT*2.8 + DOWN*1.2)
        b_t = MathTex("b").move_to(b)

        z = Circle(radius=0.55).shift(LEFT*1.0)
        z_t = MathTex("z = wx + b").move_to(z)

        yhat = Circle(radius=0.55).shift(RIGHT*1.4)
        yhat_t = MathTex(r"\hat{y}=\sigma(z)").move_to(yhat)

        y = Circle(radius=0.45).shift(RIGHT*3.8 + UP*1.2)
        y_t = MathTex("y").move_to(y)

        L = RoundedRectangle(corner_radius=0.2, height=1.2, width=2.4).shift(RIGHT*4.2 + DOWN*1.2)
        L_t = MathTex(r"L(\hat{y},y)").move_to(L)

        nodes = VGroup(x, w, b, z, yhat, y, L)
        labels = VGroup(x_t, w_t, b_t, z_t, yhat_t, y_t, L_t)

        self.play(FadeIn(nodes), Write(labels))
        self.wait(0.5)

        # --- Forward arrows ---
        a_xz = Arrow(x.get_right(), z.get_left(), buff=0.1)
        a_wz = Arrow(w.get_right(), z.get_left(), buff=0.1)
        a_bz = Arrow(b.get_right(), z.get_left(), buff=0.1)
        a_zy = Arrow(z.get_right(), yhat.get_left(), buff=0.1)
        a_yL = Arrow(y.get_bottom(), L.get_top(), buff=0.1)
        a_yhatL = Arrow(yhat.get_right(), L.get_left(), buff=0.1)

        forward = VGroup(a_xz, a_wz, a_bz, a_zy, a_yL, a_yhatL)

        forward_txt = Text("Forward pass", font_size=28).next_to(title, DOWN)
        self.play(Write(forward_txt))
        self.play(Create(forward))
        self.wait(0.6)

        # --- Loss highlight ---
        self.play(Indicate(L, scale_factor=1.05))
        self.wait(0.4)

        # --- Backward arrows (gradients flowing back) ---
        back_txt = Text("Backward pass: gradients", font_size=28).next_to(title, DOWN)
        self.play(Transform(forward_txt, back_txt))

        # Backward arrows (reverse direction)
        g_yhat = Arrow(L.get_left(), yhat.get_right(), buff=0.1)
        g_z = Arrow(yhat.get_left(), z.get_right(), buff=0.1)
        g_w = Arrow(z.get_left(), w.get_right(), buff=0.1)
        g_b = Arrow(z.get_left(), b.get_right(), buff=0.1)

        grads = VGroup(g_yhat, g_z, g_w, g_b)

        # Gradient labels
        t1 = MathTex(r"\frac{\partial L}{\partial \hat{y}}").scale(0.6).next_to(g_yhat, UP, buff=0.1)
        t2 = MathTex(r"\frac{\partial L}{\partial z}").scale(0.6).next_to(g_z, UP, buff=0.1)
        t3 = MathTex(r"\frac{\partial L}{\partial w}").scale(0.6).next_to(g_w, UP, buff=0.1)
        t4 = MathTex(r"\frac{\partial L}{\partial b}").scale(0.6).next_to(g_b, DOWN, buff=0.1)

        self.play(Create(grads))
        self.play(Write(VGroup(t1, t2, t3, t4)))
        self.wait(0.8)

        # --- Update rule ---
        upd_txt = Text("Update step", font_size=28).next_to(title, DOWN)
        self.play(Transform(forward_txt, upd_txt))

        update = MathTex(
            r"w \leftarrow w - \eta \frac{\partial L}{\partial w}",
            r"\quad",
            r"b \leftarrow b - \eta \frac{\partial L}{\partial b}"
        ).scale(0.8).to_edge(DOWN)

        self.play(Write(update))
        self.wait(1.2)

        # wrap
        self.play(FadeOut(VGroup(forward_txt, update, grads, t1, t2, t3, t4)))
        self.wait(0.2)