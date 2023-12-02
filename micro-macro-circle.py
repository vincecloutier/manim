from manim import *

class BaseScene(Scene):
    def construct_main_circle(self, bottom_text=None):
        intro_text = Tex("Redefining Micro / Macro Linkages").to_edge(UP)
        self.circle = Circle(radius=2.5, fill_opacity=0.0, stroke_opacity=0.0)
        self.arrows = VGroup(*[self.create_arrow_on_circle(angle, 0.25) for angle in np.arange(0, TAU, TAU / 12)])
        left_group, right_group = self.get_labels_with_background()

        self.play(
            Write(intro_text),
            Create(self.circle),
            Create(self.arrows),
            Write(left_group),
            Write(right_group),
            Write(bottom_text)
        )

    def get_labels_with_background(self):
        left_label, right_label = Tex("Micro"), Tex("Macro")
        left_label.move_to(self.circle.point_at_angle(PI))
        right_label.move_to(self.circle.point_at_angle(0))

        left_background = BackgroundRectangle(left_label, fill_opacity=1, buff=0.5)
        right_background = BackgroundRectangle(right_label, fill_opacity=1, buff=0.5)

        return VGroup(left_background, left_label), VGroup(right_background, right_label)

    def create_arrow_on_circle(self, angle, length, color = WHITE, opacity = 1.0):
        start_point = self.circle.point_at_angle(angle + length)
        end_point = self.circle.point_at_angle(angle)
        return Arrow(start=start_point, end=end_point, color=color, buff=0, max_tip_length_to_length_ratio=0.5, fill_opacity=opacity, stroke_opacity=opacity)

    def adjust_arrows_size(self, top_bigger=True, threshold = 0.0, animate=False):
        adjusted_arrows = [self.get_adjusted_arrow(arrow, top_bigger, threshold) for arrow in self.arrows]
        if animate:
            animations = [Transform(arrow, adjusted_arrow) for arrow, adjusted_arrow in zip(self.arrows, adjusted_arrows)]
            self.play(*animations, run_time=2)
        else:
            for arrow, adjusted_arrow in zip(self.arrows, adjusted_arrows):
                arrow.become(adjusted_arrow)

    def get_adjusted_arrow(self, arrow, top_bigger, threshold):
        angle = np.arctan2(arrow.get_end()[1], arrow.get_end()[0]) % TAU
        is_big = (angle < PI and top_bigger) or (angle > PI and not top_bigger)
        length = 0.25 if is_big else 0.1
        color = RED if is_big else WHITE  # Big arrows are red, small arrows are white
        opacity = 0.0 if is_big and threshold == 1 else 1.0
        return self.create_arrow_on_circle(angle, length, color, opacity)

class MainCircleScene(BaseScene):
    def construct(self):
        b_text = Tex("Circularity and Continuity").to_edge(DOWN) 
        self.construct_main_circle(b_text)
        self.play(
            Rotating(self.circle, radians=-TAU, about_point=ORIGIN, rate_func=smooth),
            Rotating(self.arrows, radians=-TAU, about_point=ORIGIN, rate_func=smooth),
            run_time=10
        )
        self.wait(5)

class MicroDominanceScene(BaseScene):
    def construct(self):
        b_text = Tex("Micro Dominance (Threshold Effects, Non-linear Diffusion)").to_edge(DOWN)
        self.construct_main_circle(b_text)
        self.adjust_arrows_size(top_bigger=True, animate=True)
        self.play(
            Rotating(self.circle, radians=-TAU, about_point=ORIGIN, rate_func=smooth),
            Rotating(self.arrows, radians=-TAU, about_point=ORIGIN, rate_func=smooth),
            UpdateFromFunc(self.arrows, self.adjust_arrows_size),
            run_time=10
        )
        self.wait(5)

class MacroDominanceScene(BaseScene):
    def construct(self):
        b_text = Tex("Macro Dominance (COVID, Fukushima, Subprime Crisis)").to_edge(DOWN)
        self.construct_main_circle(b_text)
        self.adjust_arrows_size(top_bigger=False, animate=True)
        self.play(
            Rotating(self.circle, radians=-TAU, about_point=ORIGIN, rate_func=smooth),
            Rotating(self.arrows, radians=-TAU, about_point=ORIGIN, rate_func=smooth),
            UpdateFromFunc(self.arrows, lambda mobject: self.adjust_arrows_size(False)),
            run_time=10
        )
        self.wait(5)

class ThresholdEffectsScene(BaseScene):
    def construct(self):
        b_text = Tex("Threshold Effects").to_edge(DOWN)
        self.construct_main_circle(b_text)

        # Create and animate the expanding bubble
        bubble = self.create_bubble_around_macro()

        # Adjust arrows with opacity for the first 5 seconds
        self.adjust_arrows_size(top_bigger=False, threshold=1, animate=True)
        self.play(
            Rotating(self.circle, radians=-TAU, about_point=ORIGIN, rate_func=smooth),
            Rotating(self.arrows, radians=-TAU, about_point=ORIGIN, rate_func=smooth),
            UpdateFromFunc(self.arrows, lambda mobject: self.adjust_arrows_size(False, threshold=1)),
            bubble.animate.scale(1.5), 
            run_time=7
        )

        # Change opacity of arrows to visible for the next 3 seconds
        self.adjust_arrows_size(top_bigger=False, threshold=0.5, animate=True)
        self.play(
            UpdateFromFunc(self.arrows, lambda mobject: self.adjust_arrows_size(False, threshold=0.5)),
            run_time=3
        )

        self.wait(2)

    def adjust_arrows_size(self, top_bigger=True, threshold=1.0, animate=False):
        adjusted_arrows = [self.get_adjusted_arrow(arrow, top_bigger, threshold) for arrow in self.arrows]
        if animate:
            animations = [Transform(arrow, adjusted_arrow) for arrow, adjusted_arrow in zip(self.arrows, adjusted_arrows)]
            self.play(*animations, run_time=2)
        else:
            for arrow, adjusted_arrow in zip(self.arrows, adjusted_arrows):
                arrow.become(adjusted_arrow)

    def get_adjusted_arrow(self, arrow, top_bigger, threshold):
        angle = np.arctan2(arrow.get_end()[1], arrow.get_end()[0]) % TAU
        is_big = (angle < PI and top_bigger) or (angle > PI and not top_bigger)
        length = 0.25 if is_big else 0.1
        color = RED if is_big else WHITE  # Big arrows are red, small arrows are white

        opacity = 0.0 if is_big and threshold == 1 else 1.0

        return self.create_arrow_on_circle(angle, length, color, opacity)

    def create_bubble_around_macro(self):
        # Create a bubble around the Macro label
        macro_label_pos = self.circle.point_at_angle(0)
        bubble = Circle(radius=1.25, color=WHITE).move_to(macro_label_pos)
        self.add(bubble)
        return bubble
