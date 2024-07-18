from manim import *

config.background_color = LOGO_WHITE

class TectonQueryTreeIntro(Scene):
    def construct(self):
        # Create a single MarkupText object with styling
        title = Text("The Tecton Query Tree", font="futura", color=BLACK)
        title.scale(1)
        title.to_edge(UP)
        ul = Underline(title, color=BLACK)
        self.play(FadeIn(title, ul))

        full_text = MarkupText(
            'The <span foreground="orange">Tecton Query Tree</span> is an internal <span foreground="green"><i>logical representation</i></span> of a SQL or Pyspark Query where the individual parts that it is built from (nodes) are stored and evaluated independently.',
            line_spacing=1.5,
            font_size=60,
            font="futura",
            color=BLACK
        )

        full_text.scale_to_fit_width(config.frame_width * 0.8)
        full_text.move_to(ORIGIN)

        # Animate the text
        self.play(Write(full_text))

        # Wait for a moment at the end
        self.wait(2)
