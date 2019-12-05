from manimlib.imports import *
import numpy as np


def generate_coprimes(q):  # returns all tuples (p/q, 1/q) with p < q and GCD(p,q) = 1
    pairs = []
    for i in range(1, q+1):
        gcd = np.gcd(i,q)
        if gcd == 1:
            y = 1.0/q
            x = i*y
            pairs.append((x,y))

    return pairs


def thomae(limit):  $ Thomae's function
    points = []
    for i in range(2, limit+1):
        points.extend(generate_coprimes(i))
    return points


def farey_approximator(target, limit):
    # numerator, demonimator
    a, b = 0, 1
    c, d = 1, 1
    sequence = []

    while b <= limit and d <= limit:
        p, q = a + c, b + d
        approx = p/q

        # a/b always < target, c/d always > target
        if approx < target:
            a, b = p, q
            if q <= limit:
                sequence.append((a/b, 1.0/b))
                print(a,b)
        else:
            c, d = p, q
            if q <= limit:
                sequence.append((c/d, 1.0/d))
                print(c,d)

    return sequence


class Main(Scene):
    def construct(self):
        x_scl = 12
        y_scl = 14
        limit = 79
        target = (2 + np.sqrt(7))/8

        points = thomae(limit)
        thomae_graph = VGroup(*[Dot(point=x_scl*p[0]*RIGHT + y_scl*p[1]*UP, radius=0.03, color=BLACK) for p in points])

        approximations = farey_approximator(target, limit)
        approximations_ = VGroup(
            *[Dot(point=x_scl*p[0]*RIGHT + y_scl*p[1]*UP, radius=0.06, color=RED) for p in approximations])

        everything = VGroup(thomae_graph, approximations_).center()

        self.add(thomae_graph)
        self.wait()
        self.play(ShowCreation(approximations_, run_time=3))
