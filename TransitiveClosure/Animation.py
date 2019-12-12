from manimlib.imports import *


class Main(Scene):
    def construct(self):
        nodes = [(0,0), (-1.3,0.1), (-0.1,1.3), (1,-1), (0.6,-1.8)]
        nodes_ = VGroup(
            *[Dot(point=i[0]*RIGHT + i[1]*UP, radius=0.1, color='#cf53a7') for i in nodes]
        )

        edges = [(1,0), (2,0), (0,3), (2,3), (0,4)]
        edges_ = VGroup(
            *[
                Arrow(start=nodes[i[0]][0]*RIGHT + nodes[i[0]][1]*UP,
                      end=nodes[i[1]][0]*RIGHT + nodes[i[1]][1]*UP,
                      stroke_width=6,
                      buff=SMALL_BUFF,
                      tip_length=0.1) for i in edges
            ]
        )

        closed_edges = [(1, 3), (1,4), (2,4)]
        closed_edges_ = VGroup(
            *[
                Arrow(start=nodes[i[0]][0] * RIGHT + nodes[i[0]][1] * UP,
                      end=nodes[i[1]][0] * RIGHT + nodes[i[1]][1] * UP,
                      stroke_width=8,
                      buff=SMALL_BUFF,
                      color='#96ed7b',
                      tip_length=0.1) for i in closed_edges
            ]
        )

        graph = VGroup(closed_edges_, nodes_, edges_).rotate(0.7).scale(1.8) # not rendered

        edge_grp1 = VGroup(edges_[0], edges_[2]).copy()
        edge_grp2 = VGroup(edges_[0], edges_[4]).copy()
        edge_grp3 = VGroup(edges_[1], edges_[4]).copy()

        transforms_ = Succession(
            Transform(edge_grp1, closed_edges_[0]),
            Transform(edge_grp2, closed_edges_[1]),
            Transform(edge_grp3, closed_edges_[2])
        )

        self.add(nodes_, edges_)
        self.wait()
        self.play(transforms_)
        self.wait(0.5)
