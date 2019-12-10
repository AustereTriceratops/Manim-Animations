from manimlib.imports import *


def equality(lhs, rhs):
    lhs_ = TexMobject(lhs)
    rhs_ = TexMobject(rhs)
    eq_ = TexMobject('=')

    lhs_.next_to(eq_, direction=LEFT)
    rhs_.next_to(eq_, direction=RIGHT)

    return VGroup(lhs_, eq_, rhs_)


def function_curve(func, interval=(1,7), resolution=20):
    width = interval[1] - interval[0]
    step = width/resolution
    x = [interval[0]]
    y = [func(interval[0])]
    curve_ = VGroup()

    for i in range(1, resolution+1):
        x.append(x[i-1] + step)
        y.append(func(x[i]))
        curve_.add(
            Line(start=x[i-1]*RIGHT + y[i-1]*UP, end=x[i]*RIGHT + y[i]*UP)
        )

    return curve_


class Main(Scene):
    def construct(self):
        eq1 = equality(r'\displaystyle\sum_1^{\infty}', r'1 + \frac{1}{2} + \frac{1}{3}+\frac{1}{4}+\cdots')
        eq1.center()

        pluses = VGroup(*[TexMobject('+') for _ in range(1, 6)])
        bars = VGroup(*[Rectangle(height=2/n, width=1, color=BLACK) for n in range(1,7)])
        #curve = function_curve(lambda x: 1/x).stretch(2, 1)
        curve = ParametricFunction(function=lambda x: [x, 1/x, 0], t_min=1, t_max=7, step_size=0.2).stretch(2,1)

        bars_aligned = bars.copy()
        for i in range(0,6):
            if i > 0:
                bars_aligned[i].next_to(bars_aligned[i-1], buff=0)

                pluses[i-1].next_to(bars[i-1], buff=SMALL_BUFF)
                bars[i].next_to(pluses[i-1], buff=SMALL_BUFF)

            bars_aligned[i].next_to(bars_aligned[i].get_x()*RIGHT, direction=UP, buff=0)

        curve.next_to(eq1[1])
        bars_aligned.next_to(eq1[1])
        rhs_bars = VGroup(bars, pluses).next_to(eq1[1])
        curve.shift(UP/6)

        eq2 = VGroup(eq1[0].copy(), eq1[1].copy(), rhs_bars).center()
        eq3 = VGroup(eq1[0].copy(), eq1[1].copy(), bars_aligned, curve).center()

        # it would be useful to have VGroups in which not all objects are rendered during transformations
        # i.e. VGroups which serve only as containers for aligning/organizing mobjects
        # this may be their intended use and I need to figure out how to properly use Transformations

        self.add(eq1)
        self.wait()
        self.play(Transform(eq1, eq2))
        self.wait()
        self.play(Transform(eq1, eq3[0:3]))
        self.wait()
        self.play(Write(curve))
        self.wait()
