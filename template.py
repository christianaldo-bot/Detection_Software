import re
import matplotlib.pyplot as plt

from shapely.geometry import Point, box
from shapely.ops import unary_union

# =====================================================
# template size
# =====================================================

WIDTH = 300
HEIGHT = 180

# Resolusi lingkaran (semakin besar semakin halus)
CIRCLE_RESOLUTION = 128


# =====================================================
# Parser
# =====================================================

def parse_code(code):

    code = code.upper()

    radius = list(map(int, re.findall(r"R(\d+)", code)))

    if len(radius) == 0:
        return []

    circles = []

    # R pertama -> sudut kiri bawah
    circles.append((0, 0, radius[0]))

    # R kedua -> sudut kiri atas
    if len(radius) >= 2:
        circles.append((0, HEIGHT, radius[1]))

    return circles


# =====================================================
# Gambar
# =====================================================

def draw_template(code):

    # Persegi panjang
    rectangle = box(0, 0, WIDTH, HEIGHT)

    # Semua lingkaran
    circles = []

    for cx, cy, r in parse_code(code):

        circle = Point(cx, cy).buffer(
            r,
            resolution=CIRCLE_RESOLUTION
        )

        circles.append(circle)

    # Boolean Difference
    if circles:
        holes = unary_union(circles)
        result = rectangle.difference(holes)
    else:
        result = rectangle

    # ==================================================
    # Plot
    # ==================================================

    fig, ax = plt.subplots(figsize=(8,5))

    if result.geom_type == "Polygon":

        x, y = result.exterior.xy
        ax.fill(
            x,
            y,
            facecolor="white",
            edgecolor="black",
            linewidth=2
        )

    else:

        for poly in result.geoms:

            x, y = poly.exterior.xy
            ax.fill(
                x,
                y,
                facecolor="white",
                edgecolor="black",
                linewidth=2
            )

    ax.set_aspect("equal")

    ax.set_xlim(-120, WIDTH + 30)
    ax.set_ylim(-120, HEIGHT + 30)

    ax.axis("off")

    plt.title(code)

    plt.show()


# =====================================================
# TEST
# =====================================================

examples = [
    "AR50",
    "AR50R30",
    "AR80",
    "AR100R40"
]

for e in examples:
    draw_template(e)
