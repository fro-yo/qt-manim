from manim import *

config.background_color = LOGO_WHITE
BLACK = GREY_BROWN

class TransactionTimeline(Scene):
    def construct(self):
        # Create a number line representing 5 days
        timeline = NumberLine(
            x_range=[0, 6, 1],
            length=10,
            include_numbers=True,
            label_direction=DOWN,
            color=BLACK,
        )
        timeline.numbers.set_color(BLACK)
        
        # Add a title
        title = Text("Offline Aggregations", color=BLACK, font="futura").scale(0.8).to_edge(UP)
        self.add(title)

        # Create transaction events
        events = [
            ("Day 1", "$50", 1),
            ("Day 2", "$80", 2),
            ("Day 2", "$30", 2),
            ("Day 3", "$75", 3),
            ("Day 3", "$40", 3),
            ("Day 3", "$25", 3),
            ("Day 4", "$20", 4),
            ("Day 5", "$5", 5)
        ]

        # Dictionary to keep track of transactions per day
        transactions_per_day = {}
        
        dots = VGroup()
        dot_map = {}

        # Add events to the timeline
        for day, amount, position in events:
            if position not in transactions_per_day:
                transactions_per_day[position] = 0
            
            vertical_offset = transactions_per_day[position] * 0.8
            transactions_per_day[position] += 1

            dot = Dot(point=timeline.n2p(position), color=MAROON)
            dot.shift(UP * vertical_offset)
            dot.shift(RIGHT)
            
            label = Text(f"{amount}", font_size=15, font="futura", color=BLACK).next_to(dot, UP, buff=0.2)
            dots.add(dot)
            dots.add(label)

            if position not in dot_map:
                dot_map[position] = VGroup()
            dot_map[position].add(dot)
            dot_map[position].add(label)

        # Position the timeline
        timeline.shift(DOWN * 0.5)
        self.play(Create(dots))
        # Add the timeline to the scene
        self.play(Create(timeline))
        

        at = Text(f"anchor_time", font_size=24, font="menlo", color=BLACK).next_to(timeline, DOWN)
        at_explained = Text(f"The start of the tile interval. Used to uniquely identify individual tiles.", font_size=24, font="futura", color=BLACK).next_to(at, RIGHT)
        at_group = VGroup(at, at_explained)
        at_group.move_to(ORIGIN)
        at_group.shift(DOWN * 3.5)

        self.wait(1)
        self.play(
            Write(at_group)
        )

        table = Table(
            [["Day 1: 00:00", "Day 2: 00:00", "Day 3: 00:00", "Day 4: 00:00", "Day 5 00:00"],
            ["50", "110", "140", "20", "5"]],
            row_labels=[Text("Anchor Time"), Text("Aggregated Sum")],
            col_labels=[Text("user_1"), Text("user_1"), Text("user_1"), Text("user_1"), Text("user_1")],
            top_left_entry=Star().scale(0.3),
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": BLACK},
            color=BLACK,
        )

        table.next_to(timeline, DOWN/2)
        table.scale(0.3)
        table.set_row_colors(BLACK, BLACK, BLACK)
        table.shift(UP)

        self.wait(2)

        self.play(Create(table))

        self.wait(2)

        for i in range (2, 7):
            hl = SurroundingRectangle(dot_map[i-1], color=MAROON, buff=0.1)
            hl2 = SurroundingRectangle(table.get_entries((3, i)), color=MAROON)

            #table.add_highlighted_cell((2, i), GREEN)
            #table.add_highlighted_cell((3, i), GREEN)

            self.play(Create(hl), Create(hl2), run_time=0.5)
            
            self.play(
                FadeOut(hl),
                FadeOut(hl2),
                run_time = 0.5
            )


        self.wait(1)
        self.play(
            FadeOut(table)
        )


        et = Text(f"effective_time", font_size=20, font="menlo", color=BLACK).next_to(timeline, DOWN)
        et_explained = Text(f"The time when a specific feature value will be available in the Online Store.", font_size=20, font="futura", color=BLACK).next_to(et, RIGHT)
        et_group = VGroup(et, et_explained)
        et_group.move_to(ORIGIN)
        et_group.shift(DOWN * 2)
        self.play(Transform(at_group, et_group))

        schedule = Text(f"Batch Schedule = 1 day", font_size=12, font="menlo", color=BLACK, weight=BOLD).next_to(timeline, UP).shift(LEFT * 5)
        ts_arrow = Arrow(dot_map[1].get_top() + UP * 1.5, dot_map[1].get_top(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)
        ts_text = Text(f"Timestamp", font_size=12, font="menlo", color=RED, weight=BOLD).next_to(ts_arrow, UP)
        self.wait(1)
        self.play(Create(ts_arrow), Write(ts_text), Write(schedule), run_time=0.5)


        et_arrow = Arrow(timeline.number_to_point(2) + UP * 2, timeline.number_to_point(2), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)
        et_text = Text(f"Effective Timestamp", font_size=12, font="menlo", color=GREEN, weight=BOLD).next_to(et_arrow, UP).shift(RIGHT/3)

        self.wait(1)
        self.play(Create(et_arrow))

        self.wait(1)
        self.play(Write(et_text), run_time=0.5)
