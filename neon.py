import math as m
import random as r
import turtle as t

s = t.Screen()
s.setup(800, 800)
s.bgcolor("#03030b")
s.title("Neon Butterfly")
s.tracer(0)

cv = s.getcanvas()
OY = -30
rng = r.Random(12)


def butterfly(a, scale):
    radius = (
        m.exp(m.cos(a))
        - 2 * m.cos(4 * a)
        + m.sin(a / 12) ** 5
    ) * scale

    return radius * m.sin(a), radius * m.cos(a) + OY


def hx(color):
    return "#%02x%02x%02x" % tuple(
        int(max(0, min(1, value)) * 255)
        for value in color
    )


def mix(first, second, amount):
    return tuple(
        a + (b - a) * amount
        for a, b in zip(first, second)
    )


def segment(x1, y1, x2, y2, color, width):
    cv.create_line(
        x1, -y1, x2, -y2,
        fill=hx(color),
        width=width,
        capstyle="round",
    )


def artwork():
    points = sorted(
        (
            (rng.uniform(0, 2 * m.pi), rng.uniform(3, 92))
            for _ in range(5600)
        ),
        key=lambda point: point[1],
    )

    for a, scale in points:
        x, y = butterfly(a, scale)

        angle = (
            m.atan2(y - OY, x)
            + rng.uniform(-0.18, 0.18)
        )
        length = rng.uniform(3, 8)

        if scale < 41:
            color = mix(
                (0.32, 0.95, 1.0),   
                (0.22, 0.42, 1.0),   
                scale / 41,
            )

        elif scale < 74:
            color = mix(
                (0.22, 0.42, 1.0),   
                (0.88, 0.20, 1.0),   
                (scale - 41) / 33,
            )

        else:
            amount = (scale - 74) / 18
            amount = amount * amount * (3 - 2 * amount)

            color = mix(
                (0.88, 0.20, 1.0),   
                (0.24, 0.025, 0.42), 
                amount,
            )

        yield (
            x, y,
            x + length * m.cos(angle),
            y + length * m.sin(angle),
            color,
            rng.uniform(0.7, 1.3),
        )

strokes = iter(artwork())


def draw_next():
    try:
        segment(*next(strokes))
        s.update()
        s.ontimer(draw_next, 0)

    except StopIteration:
        s.update()

    except (t.Terminator, t.TclError):
        return


s.ontimer(draw_next, 0)
t.done()