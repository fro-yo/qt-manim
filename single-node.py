from manim import *
import random

BLACK = GREY_BROWN
l_config = {"stroke_width": 1,"color": BLACK}

class NodeWithTables(Scene):

    config.background_color = LOGO_WHITE

    def construct(self):
        title = Text("Query Tree Node", font="futura", color=BLACK)
        title.scale(1)
        title.to_edge(UP)
        ul = Underline(title, color=BLACK)
        self.play(FadeIn(title, ul))
        self.wait(2)


        # Create the central node
        node = Dot(radius=0.4, color=MAROON).move_to(ORIGIN)
        node_label = Text("Node", font='futura', font_size=24, color=BLACK).next_to(node, DOWN, buff=0.4)
        node_group = VGroup(node, node_label)

        self.play(FadeOut(title, ul), Create(node_group))
        self.wait(2)

        # Create the left table (4x4)
        left_table = Table(
            [
                ["2024-07-01 1:00", "user_1", "50"],
                ["2024-07-04 3:00", "user_1", "190"],
                ["2024-07-08 4:00", "user_1", "20"],
                ["2024-07-11 1:00", "user_1", "800"],
            ],
            include_outer_lines=True,
            color=BLACK,
            line_config=l_config,
            col_labels=[Text("timestamp"), Text("user_id"), Text("amount")],
        ).scale(0.4).next_to(node, LEFT, buff=1.5)

        left_table.set_row_colors(BLACK, BLACK, BLACK, BLACK, BLACK)

        # Create the right tables (3 small tables)
        anchor_time = Table(
            [
                ["2024-07-01 1:00", "2024-07-01 1:00", "user_1", "50"],
                ["2024-07-04 3:00", "2024-07-04 3:00", "user_1", "190"],
                ["2024-07-08 4:00", "2024-07-08 4:00", "user_1", "20"],
                ["2024-07-11 1:00", "2024-07-11 1:00", "user_1", "800"],
            ],
            include_outer_lines=True, 
            color=BLACK,
            line_config=l_config,
            col_labels=[Text("timestamp"), Text("anchor_time"), Text("user_id"), Text("amount")],
        ).scale(0.2)
        filter_table = Table(
            [
                ["2024-07-04 3:00", "user_1", "190"],
                ["2024-07-08 4:00", "user_1", "20"],
            ],
            include_outer_lines=True, 
            color=BLACK,
            line_config=l_config,
            col_labels=[Text("timestamp"), Text("user_id"), Text("amount")],
        ).scale(0.3)
        rename_col_table = Table(
            [
                ["2024-07-01 1:00", "user_1", "50"],
                ["2024-07-04 3:00", "user_1", "190"],
                ["2024-07-08 4:00", "user_1", "20"],
                ["2024-07-11 1:00", "user_1", "800"],
            ],
            include_outer_lines=True, 
            color=BLACK,
            line_config=l_config,
            col_labels=[Text("baz"), Text("bar"), Text("foo")],
        ).scale(0.3)

        right_tables = VGroup(anchor_time, filter_table, rename_col_table).arrange(DOWN, buff=0.5).next_to(node, RIGHT*1.5, buff=1.5)


        for table in right_tables:
            table.set_row_colors(BLACK, BLACK, BLACK, BLACK, BLACK)

        # Create arrows
        left_arrow = Arrow(left_table.get_right(), node.get_left(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)
        right_arrows = VGroup(*[
            Arrow(node.get_right(), table.get_left(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)
            for table in right_tables
        ])

        self.play(
            Create(left_table),
            Create(left_arrow),
        )


        filter_arrow = Text("AddAnchorTimeNode", font='futura', font_size=16, color=BLACK).next_to(right_arrows[0], UP, buff=0.1)
        add_arrow = Text("FilterNode", font_size=16, color=BLACK, font='futura').next_to(right_arrows[1], UP, buff=0)
        rename_arrow = Text("RenameNode", font_size=16, color=BLACK, font='futura').next_to(right_arrows[2], DOWN, buff=0.1)
        arrow_labels = [filter_arrow, add_arrow, rename_arrow]

        for i in range(3):
            self.play(
                Create(right_tables[i]),
                Create(right_arrows[i]),
                Create(arrow_labels[i])
            )
            self.wait(2)

        self.wait(1)

        self.play(
            FadeOut(left_table),
            FadeOut(right_tables),
            FadeOut(right_arrows),
            FadeOut(left_arrow),
            FadeOut(*arrow_labels),
            FadeOut(node_label),
        )
        
        ## --------------------------------------------------------------------------------

