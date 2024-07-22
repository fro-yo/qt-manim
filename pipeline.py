from manim import *

config.background_color = LOGO_WHITE
BLACK = GREY_BROWN

class Pipeline(Scene):
    def construct(self):
        
        source_box = RoundedRectangle(corner_radius=0.5, height=4.0, width=2.0, color=LOGO_RED, fill_color=LOGO_RED, fill_opacity=0.8)
        source_text = Text("Source", font="futura").move_to(source_box.get_center()) # create text
        source_text.scale(0.8)
        source = VGroup(source_box, source_text)
        source.to_edge(LEFT)

        source_to_compute = Arrow(color=BLACK)
        source_to_compute.next_to(source, RIGHT)

        self.play(
            Create(source)
        )
        self.wait(2)

        db_image = ImageMobject(filename_or_array="assets/db.png").scale(0.7)
        rift_image = ImageMobject(filename_or_array="assets/rift.png").next_to(db_image, DOWN)
        sf_image = ImageMobject(filename_or_array="assets/snowflake.png").scale(0.25).next_to(rift_image, DOWN*2)
        mat_text = Text("Materialization", font="futura", color=BLACK).scale(0.7)
        mat_text.next_to(sf_image, DOWN)

        computes = Group(db_image, rift_image, sf_image, mat_text)
        computes.next_to(source_to_compute, RIGHT)

        self.play(
            GrowArrow(source_to_compute),
            FadeIn(computes)
        )
        self.wait(2)

       # New rectangles
        online = RoundedRectangle(height=2, width=2, color=LOGO_BLUE, fill_color=LOGO_BLUE, fill_opacity=0.8)
        online.to_edge(UP).shift(RIGHT * 3)
        
        offline = RoundedRectangle(height=2, width=2, color=LOGO_GREEN, fill_color=LOGO_GREEN, fill_opacity=0.8)
        offline.to_edge(DOWN).shift(RIGHT * 3)

        # New arrows
        upper_arrow = Arrow(start=computes.get_right() + (LEFT/2), end=online.get_left(), color=BLACK)
        lower_arrow = Arrow(start=computes.get_right() + (LEFT/2), end=offline.get_left(), color=BLACK)

        ol = Text("Online", font="futura", color=LOGO_WHITE)
        of = Text("Offline", font="futura", color=LOGO_WHITE)
        store = Text("Store", font="futura", color=LOGO_WHITE)
        store2 = Text("Store", font="futura", color=LOGO_WHITE)

        online_text = VGroup(ol, store).arrange(DOWN).scale(0.5).move_to(online.get_center())
        offline_text = VGroup(of, store2).arrange(DOWN).scale(0.5).move_to(offline.get_center())

        # Add new elements
        self.play(
            Create(online),
            Create(offline),
            Create(online_text),
            Create(offline_text),
            GrowArrow(upper_arrow),
            GrowArrow(lower_arrow)
        )
        self.wait(2)

        on_ret= Text("Online Retrieval", font="futura", color=BLACK)
        off_ret = Text("Offline Retrieval", font="futura", color=BLACK)
        api = Text("HTTP API", font="menlo", color=BLACK)
        client = Text("Py/Java Clients", font="menlo", color=BLACK)
        sdk = Text("Tecton SDK", font="menlo", color=BLACK)
        pf = Text("Publish Features", font="menlo", color=BLACK)

        online_read = VGroup(on_ret, api, client).arrange(DOWN).scale(0.3).next_to(online, RIGHT)
        offline_read = VGroup(off_ret, sdk, pf).arrange(DOWN).scale(0.3).next_to(offline, RIGHT)
        offline_read.shift(UP * 0.2)


        self.play(
            Create(online_read),
            Create(offline_read),
        )


        tree = self.get_tree()

        # Scale the entire tree
        tree.scale(0.7)
        tree.move_to(mat_text)
        tree.to_edge(DOWN)

        tree2 = tree.copy()
        tree2.move_to(offline_read)
        tree2.to_edge(DOWN)

        qt1 = VGroup(mat_text, tree)
        qt2 = VGroup(offline_read, tree2)
        
        # Create the surrounding rectangle
        hl1 = SurroundingRectangle(qt1, color=GREEN, buff=0.1)
        hl2 = SurroundingRectangle(qt2, color=GREEN, buff=0.1)



        self.wait(2)
        self.play(
            Create(tree), 
            Create(tree2), 
            Create(hl1),
            Create(hl2),
            run_time=1.5
        )


    def get_tree(self):
        def create_node(position):
            return Dot(point=position, radius=0.075, color=GREEN)

        # Create nodes
        root = create_node(ORIGIN)
        left_child = create_node(DOWN/2 + LEFT/2)
        right_child = create_node(DOWN/2 + RIGHT/2)
        left_grandchild1 = create_node(DOWN/2 + DOWN/2 + LEFT/2 + LEFT/2)
        left_grandchild2 = create_node(DOWN/2 + DOWN/2 + LEFT/4)
        right_grandchild1 = create_node(DOWN/2 + DOWN/2 + RIGHT/2 + RIGHT/2)
        right_grandchild2 = create_node(DOWN/2 + DOWN/2 + RIGHT/4)

        # Create lines connecting nodes
        line_root_left = Line(root.get_center(), left_child.get_center(), stroke_width=2, color=GREEN)
        line_root_right = Line(root.get_center(), right_child.get_center(), stroke_width=2, color=GREEN)
        line_left_grandchild1 = Line(left_child.get_center(), left_grandchild1.get_center(), stroke_width=2, color=GREEN)
        line_left_grandchild2 = Line(left_child.get_center(), left_grandchild2.get_center(), stroke_width=2, color=GREEN)
        line_right_grandchild1 = Line(right_child.get_center(), right_grandchild1.get_center(), stroke_width=2, color=GREEN)
        line_right_grandchild2 = Line(right_child.get_center(), right_grandchild2.get_center(), stroke_width=2, color=GREEN)

        tree = VGroup(
            root, left_child, right_child, 
            left_grandchild1, left_grandchild2, 
            right_grandchild1, right_grandchild2,
            line_root_left, line_root_right,
            line_left_grandchild1, line_left_grandchild2,
            line_right_grandchild1, line_right_grandchild2
        )
        return tree
