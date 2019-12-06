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
        limit = 150
        target = (2 + np.sqrt(7))/8

        target_line = Line(start=y_scl * target * UP, end=x_scl * RIGHT + y_scl * target * UP, stroke_width=1.5)
        target_label = TexMobject(r'\frac{2 + \sqrt{7}}{8}')
        target_label.next_to(target_line, aligned_edge=LEFT).shift(x_scl*RIGHT/2).scale(0.5)

        points = thomae(limit)
        points = [(p[0], 1.0/(limit*p[1])) for p in points]

        thomae_graph = VGroup(
            *[Dot(point=x_scl*p[1]*RIGHT + y_scl*p[0]*UP, radius=0.03, color='#0C9463') for p in points])

        approximations = farey_approximator(target, limit)
        approximations = [(p[0], 1.0 / (limit * p[1])) for p in approximations]

        approximations_ = VGroup(
            *[Dot(point=x_scl*p[1]*RIGHT + y_scl*p[0]*UP, radius=0.04, color=RED) for p in approximations])

        everything = VGroup(target_line, thomae_graph, approximations_, target_label).center().shift(0.8*DOWN)

        self.add(thomae_graph)
        self.play(Write(target_line), Write(target_label))
        self.wait()
        for i in range(len(approximations_)):
            self.add(approximations_[i])
            self.wait(0.1)
