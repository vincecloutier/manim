from manim import *

class ConsumptionGraph(Scene):
    def construct(self):
        # Create graph
        axes = Axes(x_range=[0, 10], y_range=[0, 10], tips=False, axis_config={"color": BLUE}).shift(DOWN * 0.5)
        labels = axes.get_axis_labels(x_label="Y-T", y_label="C")

        def pre_consumption_func(x):
            return min(x, 10)
        
        def during_consumption_func(x):
            return min(x, 5) # Cap at C = 5
                
        consumption_line = axes.plot(pre_consumption_func, color=WHITE)
        limit_line = axes.plot(lambda x: 5, color=RED)

        title = Tex("Consumption before COVID").to_edge(UP)

        # First scene
        self.play(Create(axes), Create(labels), Write(title), Create(consumption_line), run_time=2)
        self.wait(2)

        # Second scene
        self.play(Transform(title, Tex("Consumption during COVID").to_edge(UP)), run_time=1)
        self.wait(0.5)
        self.play(Create(limit_line), Transform(consumption_line, axes.plot(during_consumption_func, color=YELLOW)), run_time=2)
        self.wait(2)

        # Third scene
        self.play(Transform(title, Tex("Consumption after COVID").to_edge(UP)), FadeOut(limit_line), run_time=1)
        self.wait(0.5)
        self.play(Transform(consumption_line, Line(axes.c2p(0,1), axes.c2p(4.5,10), color=GREEN)), run_time=2)
        self.wait(2)
                
        # Cleanup
        self.play(FadeOut(consumption_line), FadeOut(title), FadeOut(labels), FadeOut(axes), run_time=1.5)
