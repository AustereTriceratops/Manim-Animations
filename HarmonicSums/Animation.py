from manimlib.imports import *


def equality(lhs, rhs):
    lhs_ = TexMobject(lhs)
    rhs_ = TexMobject(rhs)
    eq_ = TexMobject('=')

    lhs_.next_to(eq_, direction=LEFT)
    rhs_.next_to(eq_, direction=RIGHT)

    return VGroup(lhs_, eq_, rhs_)


class Main(Scene):
    def construct(self):
        eq1 = equality(r'\displaystyle\sum_1^{\infty}', r'1 + \frac{1}{2} + \frac{1}{3}+\frac{1}{4}+\cdots')
        eq1.center()

        pluses = VGroup(*[TexMobject('+') for _ in range(1, 6)])
        bars = VGroup(*[Rectangle(height=2/n, width=1, color=BLACK) for n in range(1,7)])

        bars_aligned = bars.copy()
        for i in range(0,6):
            if i > 0:
                bars_aligned[i].next_to(bars_aligned[i-1], buff=0)

                pluses[i-1].next_to(bars[i-1], buff=SMALL_BUFF)
                bars[i].next_to(pluses[i-1], buff=SMALL_BUFF)

            bars_aligned[i].next_to(bars_aligned[i].get_x()*RIGHT, direction=UP, buff=0)

        bars_aligned.next_to(eq1[1])
        rhs_bars = VGroup(bars, pluses).next_to(eq1[1])

        eq2 = VGroup(eq1[0].copy(), eq1[1].copy(), rhs_bars).center()
        eq3 = VGroup(eq1[0].copy(), eq1[1].copy(), bars_aligned).center()

        self.add(eq1)
        self.wait()
        self.play(Transform(eq1, eq2))
        self.wait()
        self.play(Transform(eq1, eq3))
        self.wait()
