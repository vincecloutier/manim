from manim import *

class CombinedScene(Scene):

    def construct(self):
        self.construct_main_circle()

        self.display_explanation("Micro Dominance (Threshold Effects, Non-linear Diffusion)", True)
        self.play(
            Rotating(self.circle, radians=-TAU, about_point=ORIGIN, rate_func=smooth),
            Rotating(self.arrows, radians=-TAU, about_point=ORIGIN, rate_func=smooth),
            UpdateFromFunc(self.arrows, self.adjust_arrows_size),
            run_time=10
        )

        self.display_explanation("Macro Dominance (COVID, Fukushima, Subprime Crisis)", False)
        self.play(
            Rotating(self.circle, radians=-TAU, about_point=ORIGIN, rate_func=smooth),
            Rotating(self.arrows, radians=-TAU, about_point=ORIGIN, rate_func=smooth),
            UpdateFromFunc(self.arrows, lambda mobject: self.adjust_arrows_size(False)),
            run_time=10
        )

        self.wait(5)


    # TODO bubble scene with threshold effects
    # TODO split up the scenes
    
    def construct_main_circle(self):
        intro_text = Tex("Redefining Micro / Macro Linkages").to_edge(UP)
        self.explanation_text = Tex("Circularity and Continuity").to_edge(DOWN)
        self.circle = Circle(radius=2.5, fill_opacity=0.0, stroke_opacity=0.0)
        self.arrows = VGroup(*[self.create_arrow_on_circle(angle) for angle in np.arange(0, TAU, TAU / 12)])
        left_group, right_group = self.get_labels_with_background()

        self.play(
            Write(intro_text),
            Create(self.circle),
            Create(self.arrows),
            Write(left_group),
            Write(right_group),
            Write(self.explanation_text)
        )

        self.play(
            Rotating(self.circle, radians=-TAU, about_point=ORIGIN, rate_func=smooth),
            Rotating(self.arrows, radians=-TAU, about_point=ORIGIN, rate_func=smooth),
            run_time=10
        )


    def get_labels_with_background(self):
        left_label, right_label = Tex("Micro"), Tex("Macro")
        left_label.move_to(self.circle.point_at_angle(PI))
        right_label.move_to(self.circle.point_at_angle(0))

        left_background = BackgroundRectangle(left_label, fill_opacity=1, buff=0.5)
        right_background = BackgroundRectangle(right_label, fill_opacity=1, buff=0.5)

        return VGroup(left_background, left_label), VGroup(right_background, right_label)

    def create_arrow_on_circle(self, angle, l, c):
        start_point = self.circle.point_at_angle(angle + l)
        end_point = self.circle.point_at_angle(angle)
        return Arrow(start=start_point, color = c, end=end_point, buff=0, max_tip_length_to_length_ratio=0.5)

    def display_explanation(self, text_content, top_bigger):
        new_explanation_text = Tex(text_content).to_edge(DOWN)
        self.play(ReplacementTransform(self.explanation_text, new_explanation_text))
        self.explanation_text = new_explanation_text
        self.adjust_arrows_size(top_bigger, animate=True)

    def adjust_arrows_size(self, top_bigger=True, animate=False):
        adjusted_arrows = [self.get_adjusted_arrow(arrow, top_bigger) for arrow in self.arrows]
        if animate:
            animations = [Transform(arrow, adjusted_arrow) for arrow, adjusted_arrow in zip(self.arrows, adjusted_arrows)]
            self.play(*animations, run_time=2)
        else:
            for arrow, adjusted_arrow in zip(self.arrows, adjusted_arrows):
                arrow.become(adjusted_arrow)

    def get_adjusted_arrow(self, arrow, top_bigger):
        # make the arrows 0.25 to start and then 0.1 when they are small
        angle = np.arctan2(arrow.get_end()[1], arrow.get_end()[0]) % TAU
        is_big = (angle < PI and top_bigger) or (angle > PI and not top_bigger)
        is_small = (angle < PI and not top_bigger) or (angle > PI and top_bigger)        
        return self.create_arrow_on_circle(angle, is_big, is_small)
