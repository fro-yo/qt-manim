from manim import *
import random

BLACK = GREY_BROWN
l_config = {"stroke_width": 1,"color": BLACK}

class NodeWithTables(Scene):

    config.background_color = LOGO_WHITE

    def construct(self):
        # Create the central node
        node = Dot(radius=0.4, color=MAROON).move_to(ORIGIN)

        self.add(node)
        self.wait(2)

        self.play(
            node.animate().to_edge(LEFT),
        )
        node_label = Text("DataSourceScan", font='menlo', font_size=12, color=BLACK).next_to(node, DOWN, buff=0.4)
        node_label.shift(RIGHT*0.1)
        self.play(
            Create(node_label)
        )

        new_nodes = ["FeaturePipeline", "FeatureTimeFilter", "AddAnchorTime"]
        prev_node = node
        all_nodes_and_labels = VGroup()
        all_nodes_and_labels.add(node)
        all_nodes_and_labels.add(node_label)
        
        for node_name in new_nodes:
            new_node = prev_node.copy()
            new_node.next_to(prev_node, RIGHT)
            new_node.shift(RIGHT*1.5)
            label = Text(node_name, font='menlo', font_size=12, color=BLACK).next_to(new_node, DOWN, buff=0.4)
            ntp_arrow = Arrow(prev_node.get_right(), new_node.get_left(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)


            self.wait(1)
            self.play(
                Create(new_node), 
                Create(label), 
                Create(ntp_arrow),
            )

            all_nodes_and_labels.add(new_node)
            all_nodes_and_labels.add(label)
            prev_node = new_node


        hl = SurroundingRectangle(all_nodes_and_labels, color=MAROON, buff=0.1)
        mat = Text("Materialization Query Tree", font="futura", font_size=24, color=BLACK)
        mat.next_to(hl, UP)
        self.wait(2)
        self.play(
            Create(hl),
            Create(mat)
        )
        
        anchor_node = prev_node
        anchor_lable = label
        partial_agg = prev_node.copy()
        partial_agg.set_color(BLUE)
        partial_label = Text("Partial Aggs", font='menlo', font_size=12, color=BLACK).next_to(partial_agg, DOWN, buff=0.4)
        anchor_node.shift(RIGHT),

        ntp_arrow = Arrow(partial_agg.get_right(), anchor_node.get_left(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)

        all_nodes_and_labels.add(partial_agg, partial_label)

        hl2 = SurroundingRectangle(all_nodes_and_labels, color=MAROON, buff=0.1)

        self.wait(2)
        self.play(
            Create(partial_agg),
            Create(partial_label),
            Create(ntp_arrow),
            Transform(hl, hl2),
        )

        self.wait(2)
        self.play(
            FadeOut(hl2),
            FadeOut(mat)
        )





        












