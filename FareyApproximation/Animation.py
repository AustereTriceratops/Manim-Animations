from manimlib.imports import *
import numpy as np


def generate_coprimes(q):  # returns all fractions p/q with p < q and GCD(p,q) = 1
    pairs = []
    y = 1.0 / q

    for i in range(1, q+1):
        gcd = np.gcd(i,q)
        if gcd == 1:
            x = i*y
            pairs.append((x,y))

    return pairs


def thomae(limit):
    points = []
    for i in range(2, limit+1):
        points.extend(generate_coprimes(i))
    return points


def farey_approximator(target, limit):
    # numerator, denominator
    a, b = 0, 1
    c, d = 1, 1
    sequence = []

    while b <= limit and d <= limit:
        p, q = a + c, b + d
        denom = 1.0/q
        approx = p*denom

        # a/b always < target, c/d always > target
        if approx < target:
            a, b = p, q
            if q <= limit:
                sequence.append((approx, denom))
        else:
            c, d = p, q
            if q <= limit:
                sequence.append((approx, denom))

    return sequence


class Main(Scene):
    CONFIG = {
        'camera_config': {
            'background_color': "#FFFDE6",
        },
    }

    def construct(self):
        x_scl = 11
        y_scl = 6
        limit = 136
        target = (2 + np.sqrt(7))/6

        target_line = Line(start=y_scl * target * UP, end=(0.1 + x_scl)*RIGHT + y_scl * target * UP, stroke_width=1.5)
        top_line = Line(start=y_scl * UP, end=x_scl * RIGHT + y_scl * UP, stroke_width=3)
        bottom_line = Line(start=0*UP, end=x_scl * RIGHT, stroke_width=3)
        x_label = TexMobject(r'\text{increasing denominator} \rightarrow').next_to(bottom_line, direction=DOWN)

        target_label = TexMobject(r'\frac{2 + \sqrt{7}}{8}')
        target_label.scale(0.8).next_to(target_line, aligned_edge=LEFT).shift(x_scl*RIGHT/2)
        top_label = TexMobject(r'1').next_to(top_line, aligned_edge=LEFT).shift((2 + x_scl)*LEFT/2)
        bottom_label = TexMobject(r'0').next_to(bottom_line, aligned_edge=LEFT).shift((2 + x_scl)*LEFT/2)

        top_line.add(top_label)
        bottom_line.add(bottom_label)

        points = thomae(limit)
        points = [(p[0], 1.0/(limit*p[1])) for p in points]
        thomae_graph = VGroup(
            *[Dot(point=x_scl*p[1]*RIGHT + y_scl*p[0]*UP, radius=0.03, color='#0C9463') for p in points])

        approximations = farey_approximator(target, limit)
        approximations = [(p[0], 1.0 / (limit * p[1])) for p in approximations]
        approximations_ = VGroup(
            *[Dot(point=x_scl*p[1]*RIGHT + y_scl*p[0]*UP, radius=0.04, color=RED) for p in approximations])
        connecting_lines = VGroup()
        for i in range(1, len(approximations)):
            sp = approximations[i-1]
            ep = approximations[i]
            c = Line(start=x_scl*sp[1]*RIGHT + y_scl*sp[0]*UP, end=x_scl*ep[1]*RIGHT + y_scl*ep[0]*UP, color=RED)
            connecting_lines.add(c)

        approximation_labels = VGroup()
        for a in approximations:
            q = round(a[1]*limit)
            p = round(a[0]*q)

            approximate_line = Line(start=x_scl*a[1]*RIGHT + 1.05*y_scl*UP, end=x_scl*a[1]*RIGHT + y_scl*a[0]*UP)
            approximate_label = TexMobject(r'%d/%d' % (p, q))
            approximate_label.scale(0.7).next_to(approximate_line, direction=UP)

            approximate_label.add(approximate_line)
            approximation_labels.add(approximate_label)

        everything = VGroup(top_line, bottom_line, approximation_labels, connecting_lines,
                            target_line, thomae_graph, approximations_, target_label, x_label
                            ).center().scale(0.9).shift(0.3*DOWN)

        self.add(top_line, bottom_line, x_label)
        self.play(ShowCreation(thomae_graph))
        self.play(Write(target_line), Write(target_label))
        self.wait()
        for i in range(len(approximations_)):
            self.add(approximations_[i])
            if i == 0:
                self.add(approximation_labels[0])
            else:
                self.play(Transform(approximation_labels[0], approximation_labels[i]),
                          Write(connecting_lines[i-1]))

            self.wait(0.2)

