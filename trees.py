from manim import *
import random

BLACK = GREY_BROWN
l_config = {"stroke_width": 1,"color": BLACK}

class NodeWithTables(Scene):

    config.background_color = LOGO_WHITE
    all_nodes_and_labels = VGroup()
    all_labels = VGroup()
    all_arrows = VGroup()
    name_to_node = {}


    def construct(self):
        # Create the central node
        node = Dot(radius=0.4, color=MAROON).move_to(ORIGIN)

        self.add(node)
        self.wait(2)

        self.play(
            node.animate().to_edge(LEFT),
        )


        ################# FIRST NODE ###################
        node_label = Text("DataSourceScan", font='menlo', font_size=12, color=BLACK).next_to(node, DOWN, buff=0.4)
        node_label.shift(RIGHT*0.1)
        self.name_to_node["DataSourceScan"] = node
        self.play(
            Create(node_label)
        )
        self.all_nodes_and_labels.add(node)
        self.all_nodes_and_labels.add(node_label)
        self.all_labels.add(node_label)
        

        ################# MAT PIPELINE NODES ###################
        node_label = Text("DataSourceScan", font='menlo', font_size=12, color=BLACK).next_to(node, DOWN, buff=0.4)
        new_nodes = ["FeaturePipeline", "FeatureTimeFilter", "AddAnchorTime"]
        prev_node = node
        for node_name in new_nodes:
            new_node, label, arrow = self.create_node(node_name, prev_node, 1)
            prev_node = new_node


        ################# MAT PIPELINE LABEL ###################
        hl = SurroundingRectangle(self.all_nodes_and_labels, color=MAROON, buff=0.1)
        mat = Text("Materialization Query Tree", font="futura", font_size=24, color=BLACK)
        mat.next_to(hl, UP)
        self.wait(2)
        self.play(
            Create(hl),
            Create(mat)
        )
        
        anchor_node = prev_node
        anchor_label = label

        ################# PARTIAL AGG ANIM ###################
        partial_agg = prev_node.copy()
        partial_agg.set_color(BLUE)
        partial_label = Text("Partial Aggs", font='menlo', font_size=12, color=BLACK).next_to(partial_agg, DOWN, buff=0.4)
        self.all_labels.add(partial_label)

        self.all_nodes_and_labels.add(partial_agg, partial_label)
        self.name_to_node["Partial Aggs"] = partial_agg

        self.wait(2)
        self.play(
            Create(partial_agg),
            Create(partial_label),
            anchor_node.animate.shift(RIGHT*2.2),
            anchor_label.animate.shift(RIGHT*2.2),
        )

        hl2 = SurroundingRectangle(self.all_nodes_and_labels, color=MAROON, buff=0.1)
        ntp_arrow = Arrow(partial_agg.get_right(), anchor_node.get_left(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)
        self.all_arrows.add(ntp_arrow)
        self.play(
            Transform(hl, hl2),
            Create(ntp_arrow),
        )

        ##################### GPA LABEL ##################################################
        self.wait(1)
        gpa = Text("get_partial_aggregates(start, end)", font="menlo", font_size=24, color=BLACK)
        gpa.move_to(mat.get_center())

        self.play(
            Transform(mat, gpa)
        )

        self.wait(2)
        self.play(
            FadeOut(mat),
            FadeOut(hl),
        )
        ##################### OL ##################################################

        self.from_source = VGroup(*self.all_arrows, *self.all_nodes_and_labels)

        ##################### SPINE ##################################################

        self.wait(1)
        self.play(
            self.all_nodes_and_labels.animate.shift(DOWN).scale(0.9),
            self.all_arrows.animate.shift(DOWN).scale(0.9)
        )


        self.wait(3)
        user_data_node = self.name_to_node["FeatureTimeFilter"].copy()
        user_data_node.shift(UP*2)
        user_data_label = Text("User Data", font='menlo', font_size=12, color=BLACK).next_to(user_data_node, DOWN, buff=0.4)
        self.play(
            Create(user_data_node),
            Create(user_data_label),
        )

        self.all_nodes_and_labels.add(user_data_node, user_data_label)
        self.name_to_node["User Data"] = user_data_node
        self.all_labels.add(user_data_label)


        new_nodes = ["ConvertToUTC", "AddRetrievalAnchorTime"]
        prev_node = user_data_node

        for node_name in new_nodes:
            new_node, label, arrow = self.create_node(node_name, prev_node, 0.9)
            prev_node = new_node


        ##################### FULL AGG  + Feature Time Filter Node ##################################################

        full_agg = prev_node.copy()
        full_agg.set_color(BLUE)
        full_agg.shift(DR + RIGHT)
        label = Text("AsOfJoinFullAgg", font='menlo', weight=BOLD, font_size=12, color=BLACK).next_to(full_agg, DOWN, buff=0.4).scale(0.9)
        arrow1 = Arrow(prev_node.get_right(), full_agg.get_left(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15).scale(0.9)
        arrow2 = Arrow(self.name_to_node["AddAnchorTime"].get_right(), full_agg.get_left(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15).scale(0.9)

        self.wait(1)
        self.play(
            Create(full_agg),
            Create(label),
            Create(arrow1),
            Create(arrow2),
        )

        self.all_nodes_and_labels.add(full_agg)
        self.all_nodes_and_labels.add(label)
        self.all_labels.add(label)
        self.name_to_node["AsOfJoinFullAgg"] = full_agg
        self.all_arrows.add(arrow1, arrow2)


        feature_time_filter_node, label, arrow = self.create_node("FeatureStartTime", full_agg, 0.9)
        ################## Offline Store Scan Label #########################################

        offline_scan = self.name_to_node["AddAnchorTime"].copy()
        label = Text("OfflineStoreScan", font='menlo', font_size=12, color=BLACK).next_to(offline_scan, DOWN, buff=0.4).scale(0.9)

        self.wait(2)
        self.play(
            FadeOut(self.from_source),
            FadeIn(offline_scan),
            FadeIn(label),
        )

        self.wait(3)
        self.play(
            FadeIn(self.from_source),
            FadeOut(offline_scan),
            FadeOut(label),
        )
        
        
        ################## GFFE Label #########################################
        hl = SurroundingRectangle(self.all_nodes_and_labels, color=MAROON, buff=0.1)
        mat = Text("get_features_for_events(events)", font="menlo", font_size=24, color=BLACK)
        mat.next_to(hl, UP)
        self.wait(2)
        self.play(
            Create(hl),
            Create(mat)
        )


        self.wait(2)
        self.play(
            FadeOut(self.all_labels),
            FadeOut(mat),
            FadeOut(hl),
        )

        #################### NEW SCENE ##############################################

        for node in self.name_to_node.values():
            node.set_color(MAROON)

        all_nodes = VGroup(*self.name_to_node.values())

        self.wait(2)
        self.play(
            all_nodes.animate.scale(0.4).rotate(PI/2),
            self.all_arrows.animate.scale(0.4).rotate(PI/2),
        )

        self.wait(1)
        mini_tree = VGroup(*all_nodes, *self.all_arrows)

        self.play(
            mini_tree.animate.shift(LEFT * 4)
        )

        self.wait(2)

        hl = SurroundingRectangle(mini_tree, color=MAROON, buff=0.1)
        mat = Text("TectonDataFrame", font="menlo", font_size=24, color=BLACK)
        mat.next_to(hl, UP)
        self.wait(2)
        self.play(
            Create(hl),
            Create(mat)
        )
        self.wait(2)
        self.play(
            FadeOut(hl),
            FadeOut(mat)
        )

        self.wait(2)
        title = Text("Translation", font="futura", color=BLACK)
        title.scale(1)
        title.to_edge(UP)
        ul = Underline(title, color=BLACK)
        self.play(Write(title), Write(ul))


        translated_tree = mini_tree.copy()
        translated_tree.to_edge(RIGHT)
        translated_tree.shift(LEFT*2.5)

        for obj in translated_tree:
            if isinstance(obj, Dot):
                obj.set_color(ORANGE)

        arrow = Arrow(ORIGIN + LEFT * 2, ORIGIN + RIGHT * 2, buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)

        arrow_label = Text("to_spark()", font="menlo", color=BLACK, font_size=18)
        arrow_label.next_to(arrow, UP)

        self.wait(2)
        self.play(Create(arrow))
        self.wait(1)


        self.play(
            Write(arrow_label),
            Create(translated_tree)
        )


        self.wait(1)

        self.play(
            *[obj.animate.set_color(BLUE) for obj in translated_tree if isinstance(obj, Dot)],
            Transform(arrow_label, Text("to_pandas() (Snowflake)", font="menlo", color=BLACK, font_size=18).next_to(arrow, UP))
        )
        self.wait(1)


        self.play(
            *[obj.animate.set_color(YELLOW) for obj in translated_tree if isinstance(obj, Dot)],
            Transform(arrow_label, Text("to_pandas() (Athena)", font="menlo", color=BLACK, font_size=18).next_to(arrow, UP))
        )
        self.wait(1)


        self.play(
            *[obj.animate.set_color(RED) for obj in translated_tree if isinstance(obj, Dot)],
            Transform(arrow_label, Text("to_pandas() (Rift)", font="menlo", color=BLACK, font_size=18).next_to(arrow, UP))
        )
        self.wait(1)


        


    def create_node(self, name: str, prev_node, scale_factor: int):
        new_node = prev_node.copy()
        new_node.next_to(prev_node, RIGHT)
        new_node.shift(RIGHT)
        label = Text(name, font='menlo', font_size=12, color=BLACK).next_to(new_node, DOWN, buff=0.4).scale(scale_factor)
        arrow = Arrow(prev_node.get_right(), new_node.get_left(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15).scale(scale_factor)

        self.wait(1)
        self.play(
            Create(new_node), 
            Create(label), 
            Create(arrow),
        )

        self.all_nodes_and_labels.add(new_node)
        self.all_nodes_and_labels.add(label)
        self.all_arrows.add(arrow)
        self.name_to_node[name] = new_node
        self.all_labels.add(label)

        return new_node, label, arrow


