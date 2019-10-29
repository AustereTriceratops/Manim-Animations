from big_ol_pile_of_manim_imports import *


def recaman(n):
    sequence = [0]

    for i in range(1, n):
        r = sequence[i-1] - i
        if (r > 0) and (r not in sequence):
            sequence.append(r)
        else:
            r += 2*i
            sequence.append(r)

    return sequence


class RecamanCircles(Scene):
    CONFIG = {
        'camera_config': {
            'background_color': "#FFFBE3",
        },
    }

    def construct(self):
        max_circles = 2200
        recaman_sequence = recaman(max_circles)
        arcs = []
        scl = 450.0
        for i in range(1,max_circles):
            dist = (recaman_sequence[i] - recaman_sequence[i-1])/scl
            center = RIGHT*(recaman_sequence[i] + recaman_sequence[i-1])/scl
            arc = Arc(radius=dist, arc_center=center, start_angle=0, angle=PI, stroke_width=2.3)
            arcs.append(arc)

        arcs = VGroup(*arcs).shift(5*LEFT)

        self.play(ShowCreation(arcs), run_time=8, rate_func=linear)
        self.wait()
