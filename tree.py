import turtle
import math
import random
import colorsys
import time

# ---------- Screen setup ----------
screen = turtle.Screen()
screen.setup(width=1000, height=850)
screen.bgcolor("#03020c")
screen.title("Cosmic Tree")
screen.colormode(1.0)
screen.tracer(0)  # we'll manually call screen.update() for speed control

t = turtle.Turtle()
t.hideturtle()
t.speed(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)


def refresh(step, interval, delay):
    """Update the screen every `interval` steps, pausing `delay` seconds."""
    if step % interval == 0:
        screen.update()
        time.sleep(delay)


def get_hsv(h, s=0.85, v=1.0):
    """Convert an HSV color to an RGB tuple turtle can use."""
    return colorsys.hsv_to_rgb(h % 1.0, s, v)


# ---------- Starfield ----------
num_stars = 200
star_hues = [0.55, 0.65, 0.75, 0.85]  # blues/purples/pinks


def draw_stars(delay):
    pen.penup()
    for i in range(num_stars):
        x = random.randint(-480, 480)
        y = random.randint(-400, 400)
        size = random.uniform(1, 3)
        hue = random.choice(star_hues)
        color = get_hsv(hue, s=random.uniform(0.1, 0.4), v=random.uniform(0.7, 1.0))
        pen.goto(x, y)
        pen.dot(size, color)
        refresh(i, interval=1, delay=delay)


# ---------- Recursive cosmic tree ----------
def draw_branch(t, length, depth, base_hue, delay, count_only=False):
    """If count_only=True, no drawing happens -- just returns how many
    branch segments *would* be drawn, so we can pace the real drawing."""
    if depth == 0 or length < 4:
        return 0

    steps = 1
    if not count_only:
        hue = (base_hue + depth * 0.02) % 1.0
        color = get_hsv(hue, s=0.8, v=1.0)
        t.pencolor(color)
        t.pensize(max(1, depth * 0.6))
        t.forward(length)
        refresh(depth, interval=1, delay=delay)
    else:
        t.forward(length)  # keep turtle position in sync without drawing time

    new_length = length * random.uniform(0.68, 0.78)
    angle = random.uniform(18, 32)

    t.left(angle)
    steps += draw_branch(t, new_length, depth - 1, base_hue, delay, count_only)
    t.right(angle * 2)
    steps += draw_branch(t, new_length, depth - 1, base_hue, delay, count_only)
    t.left(angle)

    if random.random() < 0.25 and depth > 2:
        t.left(random.uniform(-15, 15))
        steps += draw_branch(t, new_length * 0.8, depth - 2, base_hue, delay, count_only)
        t.right(random.uniform(-15, 15))

    t.backward(length)
    return steps


def draw_tree(delay):
    """Starts branching immediately from the base -- no straight root/trunk."""
    t.penup()
    t.goto(0, -380)
    t.setheading(90)
    t.pendown()

    length = 160
    new_length = length * random.uniform(0.68, 0.78)
    angle = random.uniform(18, 32)

    t.left(angle)
    draw_branch(t, new_length, 10, 0.55, delay)
    t.right(angle * 2)
    draw_branch(t, new_length, 10, 0.55, delay)
    t.left(angle)


def count_tree_steps():
    """Dry run (no drawing) to count how many segments the tree will use,
    so the real run can be paced to take a fixed total duration."""
    t.penup()
    t.goto(0, -380)
    t.setheading(90)

    length = 160
    new_length = length * random.uniform(0.68, 0.78)
    angle = random.uniform(18, 32)

    t.left(angle)
    steps = draw_branch(t, new_length, 10, 0.55, 0, count_only=True)
    t.right(angle * 2)
    steps += draw_branch(t, new_length, 10, 0.55, 0, count_only=True)
    t.left(angle)
    return steps


# ---------- Timing setup ----------
TOTAL_DURATION = 20  # seconds, minimum time for the whole drawing to complete
STAR_SHARE = 0.25     # ~25% of the time on stars, ~75% on the tree

random.seed(42)
tree_steps = count_tree_steps()   # dry run consumes the random sequence

random.seed(42)  # reset so the REAL drawing reproduces the same tree

star_time = TOTAL_DURATION * STAR_SHARE
tree_time = TOTAL_DURATION * (1 - STAR_SHARE)

star_delay = star_time / num_stars
tree_delay = tree_time / max(tree_steps, 1)

# ---------- Run ----------
start = time.time()

draw_stars(star_delay)
draw_tree(tree_delay)

elapsed = time.time() - start
if elapsed < TOTAL_DURATION:
    time.sleep(TOTAL_DURATION - elapsed)

screen.update()
screen.exitonclick()