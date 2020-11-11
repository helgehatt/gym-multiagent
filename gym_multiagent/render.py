import sys

import numpy as np

from gym_multiagent.world import World

try:
    import matplotlib.pyplot as plt
except:
    print("matplotlib is required to render in 'human' mode")
    print("change to 'raw' or run 'pip install matplotlib'")
    sys.exit(-1)


def Rectangle(x, y, size=1, **kwargs):
    return plt.Rectangle([x - size / 2, y - size / 2], size, size, **kwargs)


def Circle(x, y, size=1, **kwargs):
    return plt.Circle([x, y], size / 2, **kwargs)


def render(world: World):
    ax = plt.gca()

    for (x, y) in np.ndindex(world.level.shape):
        f = world.fixed[(x, y)]
        s = world.state[(x, y)]

        if f == "+":
            ax.add_patch(Rectangle(y, x, fc="black", ec="black"))
        elif f.isalpha():
            ax.add_patch(Rectangle(y, x, fc="lime" if f.upper() == s else "yellow", ec="black"))
            ax.text(y, x, f, fontsize=16, fontweight="bold", ha="center", va="center")
        else:
            ax.add_patch(Rectangle(y, x, fc="lightgray", ec="black"))

        if s.isalpha():
            ax.add_patch(Rectangle(y, x, size=0.75, fc="blue", ec="blue"))
            ax.text(y, x, s, color="white", fontsize=16, fontweight="bold", ha="center", va="center")
        elif s.isnumeric():
            ax.add_patch(Circle(y, x, size=0.75, fc="blue", ec="blue"))
            ax.text(y, x, s, color="white", fontsize=16, fontweight="bold", ha="center", va="center")

    ax.margins(0)
    ax.set_aspect("equal", "box")
    ax.invert_yaxis()
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    world = World()
    render(world)
