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

        # Consumption function parameters
        a = 2
        b = 0.8

        def consumption_func(x):
            return a + b * x

        consumption_graph = axes.plot(consumption_func, color=WHITE)

        # Title
        title = Tex("Pre-COVID Consumption").to_edge(UP)

        self.play(
            Create(axes),
            Create(labels),
            Create(consumption_graph),
            Write(title)
        )
        self.wait()

        # Updating title
        new_title = Tex("During COVID Consumption").to_edge(UP)
        
        # Limit line and label
        limit_line = axes.plot(lambda x: 5, color=RED, stroke_width=2)
        limit_label = Tex("Limit").next_to(limit_line, UP)

        self.play(
            Transform(title, new_title),
            Create(limit_line),
            Write(limit_label)
        )
        self.wait()

        # New Consumption function parameters
        a_new = 1.5
        b_new = 0.7

        def new_consumption_func(x):
            return a_new + b_new * x

        new_consumption_graph = axes.plot(new_consumption_func, color=YELLOW)

        self.play(
            Transform(consumption_graph, new_consumption_graph),
            Transform(title, Tex("Post-COVID Consumption").to_edge(UP))
        )
        self.wait()
