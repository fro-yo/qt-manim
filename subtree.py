from manim import *
import random

BLACK = GREY_BROWN
l_config = {"stroke_width": 1,"color": BLACK}

class GFIR(Scene):

    config.background_color = LOGO_WHITE
    all_nodes_and_labels = VGroup()
    all_labels = VGroup()
    all_arrows = VGroup()
    spine_objs = VGroup()
    name_to_node = {}


    def construct(self):
        title = Text("Debugging Queries", font="futura", color=BLACK)
        title.scale(0.9)
        title.to_edge(LEFT).to_edge(UP)
        ul = Underline(title, color=BLACK)
        self.play(FadeIn(title, ul))
        self.wait(2)


        self.create_gffe_graph()
        for node in self.name_to_node.values():
            node.set_color(MAROON)
        all_nodes = VGroup(*self.name_to_node.values())
        all_nodes.scale(0.5).rotate(PI/2)
        self.all_arrows.scale(0.5).rotate(PI/2)
        tree = VGroup(*all_nodes, *self.all_arrows)

        self.play(
            Create(tree)
        )


        nums = VGroup()
        subtree = VGroup()
        sub_map = {}
        for i, dot in enumerate(all_nodes):
            number = Text(str(i+1), font_size=24)  
            number.move_to(dot.get_center())  
            nums.add(number)  # Add the number to the scene
            if i >= 0 and i < 3:
                subtree_node = dot.copy().shift(LEFT * 2).scale(0.8)
                num_c = number.copy().shift(LEFT*2).scale(0.8)
                subtree.add(subtree_node, num_c)
                sub_map[i+1] = subtree_node

        
        self.wait(2)
        self.play(
            Write(nums)
        )


        tree.add(*nums)
        subtree = subtree.copy()

        self.wait(2)
        self.play(
            tree.animate.shift(LEFT * 2).scale(0.8),
        )


        arrow1 = Arrow(sub_map[1].get_top(), sub_map[2].get_bottom(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)
        arrow2 = Arrow(sub_map[2].get_top(), sub_map[3].get_bottom(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)
        subtree.add(arrow1, arrow2)

        call_arrow = Arrow(tree.get_right() + RIGHT, tree.get_right() + RIGHT * 3, buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)
        subtree_call = Text("df.subtree(3)", font="menlo", font_size=20, color=BLACK).next_to(call_arrow, UP)

        self.wait(2)
        self.play(
            Create(call_arrow),
            Write(subtree_call),
        )

        self.wait(2)
        self.play(
            subtree.animate.shift(RIGHT*4 + UP * 2),
        )

        
        

    def create_gffe_graph(self):
        # Create the central node
        node = Dot(radius=0.4, color=MAROON).move_to(ORIGIN)
        node.to_edge(LEFT)


        ################# FIRST NODE ###################
        node_label = Text("DataSourceScan", font='menlo', font_size=12, color=BLACK).next_to(node, DOWN, buff=0.4)
        node_label.shift(RIGHT*0.1)
        self.name_to_node["DataSourceScan"] = node
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


        ################# PARTIAL AGG ANIM ###################
        partial_agg = prev_node.copy()
        partial_agg.set_color(BLUE)
        partial_label = Text("Partial Aggs", font='menlo', font_size=12, color=BLACK).next_to(partial_agg, DOWN, buff=0.4)

        anchor_node = prev_node.shift(RIGHT*2.2)
        anchor_label = label.shift(RIGHT*2.2)

        self.all_labels.add(partial_label)

        self.all_nodes_and_labels.add(partial_agg, partial_label)
        self.name_to_node["Partial Aggs"] = partial_agg

        hl2 = SurroundingRectangle(self.all_nodes_and_labels, color=MAROON, buff=0.1)
        ntp_arrow = Arrow(partial_agg.get_right(), anchor_node.get_left(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15)
        self.all_arrows.add(ntp_arrow)

        ##################### SPINE ##################################################


        self.all_nodes_and_labels.shift(DOWN).scale(0.9)
        self.all_arrows.shift(DOWN).scale(0.9)

        user_data_node = self.name_to_node["FeatureTimeFilter"].copy()
        user_data_node.shift(UP*2)
        user_data_label = Text("User Data", font='menlo', font_size=12, color=BLACK).next_to(user_data_node, DOWN, buff=0.4)
        self.all_nodes_and_labels.add(user_data_node, user_data_label)
        self.name_to_node["User Data"] = user_data_node
        self.all_labels.add(user_data_label)
        self.spine_objs.add(user_data_node, user_data_label) 

        new_nodes = ["ConvertToUTC", "AddRetrievalAnchorTime"]
        prev_node = user_data_node
        for node_name in new_nodes:
            new_node, label, arrow = self.create_node(node_name, prev_node, 0.9)
            prev_node = new_node
            self.spine_objs.add(new_node, label, arrow) 
        



        ##################### FULL AGG  + Feature Time Filter Node ##################################################

        full_agg = prev_node.copy()
        full_agg.set_color(BLUE)
        full_agg.shift(DR + RIGHT)
        label = Text("AsOfJoinFullAgg", font='menlo', weight=BOLD, font_size=12, color=BLACK).next_to(full_agg, DOWN, buff=0.4).scale(0.9)
        arrow1 = Arrow(prev_node.get_right(), full_agg.get_left(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15).scale(0.9)
        arrow2 = Arrow(self.name_to_node["AddAnchorTime"].get_right(), full_agg.get_left(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15).scale(0.9)

        self.all_nodes_and_labels.add(full_agg)
        self.all_nodes_and_labels.add(label)
        self.all_labels.add(label)
        self.name_to_node["AsOfJoinFullAgg"] = full_agg
        self.all_arrows.add(arrow1, arrow2)
        self.spine_objs.add(arrow1)


        feature_time_filter_node, label, arrow = self.create_node("FeatureStartTime", full_agg, 0.9)
        self.fst_label = label

    def create_node(self, name: str, prev_node, scale_factor: int, color = MAROON, play_node = False):
        new_node = prev_node.copy()
        new_node.next_to(prev_node, RIGHT)
        new_node.shift(RIGHT)
        new_node.set_color(color)
        label = Text(name, font='menlo', font_size=12, color=BLACK).next_to(new_node, DOWN, buff=0.4).scale(scale_factor)
        arrow = Arrow(prev_node.get_right(), new_node.get_left(), buff=0.1, color=BLACK, stroke_width=2, tip_length=0.15).scale(scale_factor)

        if play_node:
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


