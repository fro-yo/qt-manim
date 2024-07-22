from manim import *

config.background_color = LOGO_WHITE
BLACK = GREY_BROWN

class GfirNodes(Scene):
    def construct(self):
        all_objs = VGroup()
        # Create a number line representing 5 days
        timeline = NumberLine(
            x_range=[0, 6, 1],
            length=10,
            include_numbers=True,
            label_direction=DOWN,
            color=BLACK,
        )
        timeline.numbers.set_color(BLACK)
        all_objs.add(timeline)
        
        # Add a title
        title = Text("Explode Anchor Time Node", color=BLACK, font="futura").scale(0.8).to_edge(UP)
        self.play(
            Write(title),
            run_time = 0.5
        )

        # Create transaction events
        events = [
            ("Day 1", "$50", 1),
            ("Day 3", "$75", 3),
            ("Day 3", "$40", 3),
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
            if position == 1:
                out_of_window_val = label

            dots.add(dot)
            dots.add(label)

            if position not in dot_map:
                dot_map[position] = VGroup()
            dot_map[position].add(dot)
            dot_map[position].add(label)
            all_objs.add(label)
            all_objs.add(dot)

        # Position the timeline
        timeline.shift(DOWN * 0.5)
        self.play(Create(dots))
        # Add the timeline to the scene
        self.play(Create(timeline))
        

        table = Table(
            [
                ["user_1", "Day 1: 00:00", "50"],
                ["user_1", "Day 3: 00:00", "115"],
                ["user_1", "Day 5 00:00", "5"],
            ],
            col_labels=[Text("user_id"), Text("anchor_time"), Text("aggregated_sum")],
            top_left_entry=Star().scale(0.3),
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": BLACK},
            color=BLACK,
        )

        table.next_to(timeline, DOWN/2)
        table.scale(0.3)
        table.set_row_colors(BLACK, BLACK, BLACK, BLACK)
        table.shift(UP * 1.5)

        self.wait(2)

        self.play(Create(table))
        
        table2 = Table(
            [
                ["user_1", "Day 1: 00:00"],
                ["user_1", "Day 3: 00:00"],
                ["user_1", "Day 5 00:00"],
            ],
            col_labels=[Text("user_id"), Text("anchor_time")],
            top_left_entry=Star().scale(0.3),
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": BLACK},
            color=BLACK,
        )
        table2.next_to(timeline, DOWN/2)
        table2.scale(0.3)
        table2.set_row_colors(BLACK, BLACK, BLACK, BLACK)
        table2.shift(UP * 1.5)

        self.wait(2)
        self.play(
            Transform(table, table2)
        )


        unit = timeline.n2p(3)[0] - timeline.n2p(2)[0]
        highlight = Rectangle(
            width=timeline.number_to_point(3)[0] - timeline.number_to_point(0)[0],
            height=0.5,
            fill_color=BLUE,
            fill_opacity=0.3,
            stroke_width=0
        )
        highlight.move_to(timeline.number_to_point(0.5))
        agg_value = Text(f"aggregated_value = 50", font_size=15, font="menlo", color=BLACK).next_to(highlight, DOWN, buff=0.2).shift(DOWN * 0.25)
        all_objs.add(highlight)
        all_objs.add(agg_value)

        self.wait(2)
        self.play(FadeIn(highlight), Write(agg_value), run_time=0.5)

        self.wait(1)
        self.play(
            highlight.animate.shift(RIGHT*unit),
            agg_value.animate.shift(RIGHT*unit),
        )

        self.wait(1)

        self.play(
            highlight.animate.shift(RIGHT*unit),
            agg_value.animate.shift(RIGHT*unit),
        )

        agg_2 = Text(f"aggregated_value = 165", font_size=15, font="menlo", color=BLACK).move_to(agg_value.get_center())
        self.play(
            Transform(agg_value, agg_2),
            run_time=0.5,
        )

        self.wait(1)
        self.play(
            highlight.animate.shift(RIGHT*unit),
            agg_value.animate.shift(RIGHT*unit),
        )
        agg_3 = Text(f"aggregated_value = 115", font_size=15, font="menlo", color=BLACK).move_to(agg_value.get_center())
        self.play(
            Transform(agg_value, agg_3),
            run_time=0.5,
        )


        self.wait(2)
        ntp_arrow = Arrow(out_of_window_val.get_top() + UP * 1.5, out_of_window_val.get_top(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)
        out_of = Text(f"Out of Window", font_size=15, font="futura", color=RED).move_to(ntp_arrow.get_top() + UP*0.2)
        all_objs.add(ntp_arrow, out_of)
        self.play(
            Create(ntp_arrow),
            Write(out_of)
        )

        table3 = Table(
            [
                ["user_1", "Day 1: 00:00"],
                ["user_1", "Day 3: 00:00"],
                ["user_1", "Day 4: 00:00"],
                ["user_1", "Day 5 00:00"],
                ["user_1", "Day 6: 00:00"],
                ["user_1", "Day 8: 00:00"],
            ],
            col_labels=[Text("user_id"), Text("anchor_time")],
            top_left_entry=Star().scale(0.3),
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": BLACK},
            color=BLACK,
        )
        table3.add_highlighted_cell((4, 1), color=GREEN)
        table3.add_highlighted_cell((6, 1), color=GREEN)
        table3.add_highlighted_cell((7, 1), color=GREEN)
        table3.add_highlighted_cell((4, 2), color=GREEN)
        table3.add_highlighted_cell((6, 2), color=GREEN)
        table3.add_highlighted_cell((7, 2), color=GREEN)
        table3.next_to(timeline, DOWN/2)
        table3.scale(0.3)
        table3.set_row_colors(*([BLACK]*7))
        table3.shift(UP * 4)
        table3.shift(RIGHT * 2)

        self.wait(1)
        self.play(
            all_objs.animate.scale(0.9).shift(UP * 0.9),
            table.animate.shift(LEFT * 2),
        )

        table_arrow = Arrow(table.get_right(), table.get_right() + RIGHT * 1.5, buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)

        self.play(
            Create(table3),
            Create(table_arrow)
        )


        self.wait(3)
        self.play(
            all_objs.animate.scale(0.5).to_edge(RIGHT).shift(UP),
            FadeOut(table, table_arrow),
            table3.animate.to_edge(LEFT).shift(UP*1.5 + RIGHT * 2),
            title.animate.to_edge(LEFT)
        )
        self.play(
            FadeOut(highlight, ntp_arrow, out_of, agg_value)
        )
        

        table4 = Table(
            [
                ["user_1", "Day 1: 00:00", "50"],
                ["user_1", "Day 3: 00:00", "165"],
                ["user_1", "Day 4: 00:00", "115",],
                ["user_1", "Day 5 00:00", "120",],
                ["user_1", "Day 6: 00:00", "5"],
                ["user_1", "Day 8: 00:00", "0"],
            ],
            col_labels=[Text("user_id"), Text("anchor_time"), Text("sum_3d")],
            top_left_entry=Star().scale(0.3),
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": BLACK},
            color=BLACK,
        )
        table_arrow = Arrow(table3.get_right() + RIGHT/2, table3.get_right() + RIGHT * 3, buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)
        asof = Text("AsOf Join Full Agg Node", color=BLACK, font="futura").scale(0.8).move_to(title.get_center())
        table4.next_to(table3.get_right(), RIGHT)
        table4.set_row_colors(*([BLACK]*7))
        table4.scale(0.3).shift(LEFT)

        self.play(
            Create(table4),
            Create(table_arrow),
            Transform(title, asof),
        )


        self.wait(3)

        derive = Text("Derive Validity Period Node", color=BLACK, font="futura").scale(0.8).move_to(title.get_center())
        self.play(
            table4.animate.move_to(table3.get_center()),
            FadeOut(table3),
            Transform(title, derive),
        )


        table5 = Table(
            [
                ["user_1", "Day 1: 00:00", "Day 3: 00:00", "50"],
                ["user_1", "Day 3: 00:00", "Day 4: 00:00", "165"],
                ["user_1", "Day 4: 00:00", "Day 5: 00:00", "115",],
                ["user_1", "Day 5 00:00", "Day 6: 00:00", "120",],
                ["user_1", "Day 6: 00:00", "Day 8: 00:00", "5"],
            ],
            col_labels=[Text("user_id"), Text("_valid_from"), Text("_valid_to"), Text("sum_3d")],
            top_left_entry=Star().scale(0.3),
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": BLACK},
            color=BLACK,
        )
        table5.next_to(table4.get_right(), RIGHT)
        table5.set_row_colors(*([BLACK]*7))
        table5.scale(0.3).shift(LEFT * 3)

        self.play(
            Create(table5),
            Transform(title, derive),
        )

        self.wait(2)

        dup = Text("- Removes Duplicates", color=BLACK, font="futura").scale(0.4)
        ttl = Text("- Accounts for TTL", color=BLACK, font="futura").scale(0.4)
        default = Text("- Removes 'Default' Values", color=BLACK, font="futura").scale(0.4)
        texts = VGroup(dup, ttl, default).arrange(DOWN, aligned_edge=LEFT).next_to(table5, DOWN)

        self.play(
            Write(texts),
            run_time=0.5,
        )

        self.wait(1)


