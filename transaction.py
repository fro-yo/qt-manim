from manim import *

config.background_color = LOGO_WHITE

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






