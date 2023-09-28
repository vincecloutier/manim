from manim import *

class ConsumptionGraph(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 10],
            y_range=[0, 10],
            axis_config={"color": BLUE},
        )

        # Labels
        labels = axes.get_axis_labels(x_label="Y-T", y_label="C")

        def pre_consumption_func(x):
            return x
        
        consumption_line = axes.plot(pre_consumption_func, color=WHITE)

        # Title
        title = Tex("Consumption before COVID").to_edge(UP)

        self.play(
            Create(axes),
            Create(labels),
            Create(consumption_line),
            Write(title)
        )
        self.wait()

        # Limit line and label
        limit_line = axes.plot(lambda x: 5, color=RED)

        self.play(
            Transform(title, Tex("Consumption during COVID").to_edge(UP)),
            Create(limit_line),)
        self.wait()

        def post_consumption_func(x):
            return 1 + 2 * x
        
        self.play(
            Transform(consumption_line, axes.plot(post_consumption_func, color=YELLOW)),
            Transform(title, Tex("Consumption after COVID").to_edge(UP))
        )
        self.wait()
