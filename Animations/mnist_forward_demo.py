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

class MNISTForwardDemo(LightScene):
    def construct(self):
        title = Text("MNIST example: Forward pass → prediction", font_size=34).to_edge(UP)
        self.add_light(title)

        # --- MNIST image (left) ---
        img = ImageMobject("assets/mnist_7.png").set_height(3.2).to_edge(LEFT).shift(DOWN*0.2)
        img_label = Text("input (28×28)", font_size=24).next_to(img, DOWN, buff=0.25)
        # ImageMobject hat keine Stroke/Füllung wie Vektoren -> label schwarz setzen, Background ist weiß
        img_label.set_color(FG)

        self.play(FadeIn(img), Write(img_label))
        self.wait(0.3)

        # --- Simple network diagram (right) ---
        # Layer x-positions
        x_in, x_h1, x_out = -1.0, 1.3, 3.6
        # y-positions for neurons
        in_ys  = [1.3, 0.4, -0.5, -1.4]          # placeholder "input features"
        h1_ys  = [1.6, 0.8, 0.0, -0.8, -1.6]     # hidden layer
        out_ys = [2.0, 1.55, 1.1, 0.65, 0.2, -0.25, -0.7, -1.15, -1.6, -2.05]  # 10 outputs

        def neuron(x, y, r=0.16):
            c = Circle(radius=r)
            c.move_to([x, y, 0])
            c.set_fill(opacity=0)  # line-art
            return c

        in_nodes  = VGroup(*[neuron(x_in, y) for y in in_ys])
        h1_nodes  = VGroup(*[neuron(x_h1, y) for y in h1_ys])
        out_nodes = VGroup(*[neuron(x_out, y) for y in out_ys])

        # Connections
        conns = VGroup()
        for a in in_nodes:
            for b in h1_nodes:
                conns.add(Line(a.get_right(), b.get_left(), stroke_width=1, stroke_opacity=0.25))
        for a in h1_nodes:
            for b in out_nodes:
                conns.add(Line(a.get_right(), b.get_left(), stroke_width=1, stroke_opacity=0.25))

        # Output labels 0..9
        out_labels = VGroup()
        for i, n in enumerate(out_nodes):
            t = Text(str(i), font_size=22).next_to(n, RIGHT, buff=0.18)
            t.set_color(FG)
            out_labels.add(t)

        net_group = VGroup(conns, in_nodes, h1_nodes, out_nodes, out_labels).shift(DOWN*0.2)
        net_group.apply_to_family(apply_light_theme)

        self.play(FadeIn(net_group))
        self.wait(0.4)

        # --- Forward pass animation (a few highlighted edges) ---
        forward_txt = Text("forward pass", font_size=26).next_to(title, DOWN, buff=0.25)
        forward_txt.set_color(FG)
        self.play(Write(forward_txt))

        # Choose "predicted class" (e.g., 7)
        pred = 7
        pred_node = out_nodes[pred]

        # Highlight some paths to the predicted node
        highlight = VGroup()
        # pick 2 hidden nodes to connect visually
        chosen_h = [h1_nodes[1], h1_nodes[3]]
        for h in chosen_h:
            highlight.add(Line(h.get_right(), pred_node.get_left(), stroke_width=3))
        # and 2 input nodes to chosen hidden nodes
        highlight.add(Line(in_nodes[1].get_right(), chosen_h[0].get_left(), stroke_width=3))
        highlight.add(Line(in_nodes[2].get_right(), chosen_h[1].get_left(), stroke_width=3))

        highlight.apply_to_family(apply_light_theme)

        self.play(Create(highlight), run_time=0.8)
        self.play(Indicate(pred_node, scale_factor=1.2), run_time=0.6)

        pred_txt = Text(f"prediction: {pred}", font_size=30).to_edge(DOWN)
        pred_txt.set_color(FG)
        self.play(Write(pred_txt))
        self.wait(1.0)

        self.play(FadeOut(highlight), FadeOut(forward_txt))
        self.wait(0.3)