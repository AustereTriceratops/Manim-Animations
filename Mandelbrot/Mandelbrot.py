'''
TODO: Clean up code
'''

from big_ol_pile_of_manim_imports import *
import numpy as np
import os


class Coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_0 = x
        self.y_0 = y


def iteration_step(coord):
    re = coord.x**2 - coord.y**2
    im = 2*coord.x*coord.y
    new_x = re + coord.x_0
    new_y = im + coord.y_0

    return Coord(new_x, new_y)


def dots_from_domain(domain, scl):
    dots = []
    for a in domain:
        for b in a:
            dots.append(Dot(radius=0.04).shift(b.x * scl * RIGHT + b.y * scl * UP))
    dots = VGroup(*dots)
    return dots


def create_domain(res):
    domain = np.asarray(
        [[Coord(-2 + 4/res * i, -2.0 + 4/res * j) for j in range(res+1)] for i in range(res+1)])  # domain[x][y] returns (x,y)
    return domain


class Iterations(GraphScene):
    CONFIG = {
        'x_min': -2,
        'x_max': 2,
        'x_axis_width': 6,
        'x_axis_label': '$Re(z)$',
        'x_tick_frequency': 4,
        'y_min': -2,
        'y_max': 2,
        'y_axis_height': 6,
        'y_axis_label': '$Im(z)$',
        'y_tick_frequency': 4,
        'graph_origin': 0,
    }
    def construct(self):

        # recurrence relations ==========


        # ========== SETUP AXES/GRAPH ==============
        self.setup_axes()
        xticks = self.x_axis.get_tick_marks()
        yticks = self.y_axis.get_tick_marks()
        xlabels = [TexMobject('-2'), TexMobject('2')]
        ylabels = [TexMobject('-2'), TexMobject('2')]
        for i in range(2):
            xlabels[i].next_to(xticks[i], DOWN)
            ylabels[i].next_to(yticks[i], RIGHT + 0.5*DOWN)

        labels = VGroup(*xlabels, *ylabels)
        everything = VGroup(labels, self.x_axis, self.y_axis).shift(RIGHT*2)

        self.bring_to_front(self.x_axis, self.y_axis)
        self.play(Write(labels))
        # ==========================================

        # ============ SINGLE POINT RUNNERS==========
        c = Coord(0.2, 0.5)
        runners = [c]
        for i in range(1,5):
            runners.append(iteration_step(runners[i-1]))

        runner_labels = VGroup(*[TexMobject('({},{})'.format(round(r.x, 2), round(r.y, 2))).scale(0.6) for r in runners]).shift(2*RIGHT)

        runners = VGroup(*[Dot(color='BLACK').shift(1.5*r.x*RIGHT + 1.5*r.y*UP) for r in runners]).shift(2*RIGHT)

        for i in range(5):
            runner_labels[i].next_to(runners[i], RIGHT + 0.2*UP)

        self.wait()
        self.add(runners[0], runner_labels[0])
        self.wait()
        for i in range(1,5):
            self.remove(runners[i-1], runner_labels[i-1])
            self.add(runners[i], runner_labels[i])
            self.wait(0.3)
        self.play(FadeOut(runners[4]), FadeOut(runner_labels[4]))

        # ============================================

        # ================= WHOLE DOMAIN ORBITS ========
        domain = create_domain(70)
        dots = [dots_from_domain(domain, 1.5)]

        for _ in range(5):
            domain = [[iteration_step(a) for a in b] for b in domain]
            dots.append(dots_from_domain(domain, 1.5))

        dots = VGroup(dots).shift(2*RIGHT)

        self.play(ShowCreation(dots[0]))
        self.wait()
        self.play(Transform(dots[0], dots[1]))
        self.add(dots[1])
        self.remove(dots[0])
        self.wait()
        for i in range(2,6):
            self.remove(dots[i-1])
            self.add(dots[i])
            self.wait(0.7)
        # ===============================================
