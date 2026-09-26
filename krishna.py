import pygame
import random
import math

pygame.init()


# =========================
# WINDOW SETTINGS
# =========================

WIDTH = 510
HEIGHT = 830
FPS = 60

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Krishna Particle Animation"
)

clock = pygame.time.Clock()


# =========================
# LOAD KRISHNA IMAGE
# =========================

image = pygame.image.load(
    "krishna.png"
).convert_alpha()


max_width = 400
max_height = 650

img_w, img_h = image.get_size()


scale = min(
    max_width / img_w,
    max_height / img_h
)


new_w = int(img_w * scale)
new_h = int(img_h * scale)


image = pygame.transform.smoothscale(
    image,
    (new_w, new_h)
)


offset_x = (
    WIDTH - new_w
) // 2


offset_y = (
    HEIGHT - new_h
) // 2


# =========================
# CREATE IMAGE PARTICLES
# =========================

particles = []

particle_gap = 5


for y in range(
    0,
    new_h,
    particle_gap
):

    for x in range(
        0,
        new_w,
        particle_gap
    ):

        color = image.get_at(
            (x, y)
        )


        # Only transparent image area
        if color.a > 40 and (
            color.r > 30
            or color.g > 30
            or color.b > 30
        ):

            target_x = (
                offset_x + x
            )

            target_y = (
                offset_y + y
            )


            # Random starting position

            start_x = (
                WIDTH // 2
                +
                random.randint(
                    -250,
                    250
                )
            )


            start_y = (
                HEIGHT // 2
                +
                random.randint(
                    -350,
                    350
                )
            )


            particles.append({

                "x": float(start_x),

                "y": float(start_y),

                "target_x": target_x,

                "target_y": target_y,

                "r": color.r,

                "g": color.g,

                "b": color.b,


                # =====================
                # FASTER DELAY
                # =====================

                "delay": random.uniform(
                    0,
                    30
                ),


                "size": random.randint(
                    1,
                    3
                ),


                # =====================
                # FASTER MOVEMENT
                # =====================

                "speed": random.uniform(
                    0.004,
                    0.009
                ),


                "angle": random.uniform(
                    0,
                    math.pi * 2
                )

            })


# =========================
# ANIMATION VARIABLES
# =========================

time_passed = 0.0

running = True

glow_particles = []


# =========================
# MAIN LOOP
# =========================

while running:

    dt = (
        clock.tick(FPS)
        /
        1000.0
    )


    time_passed += dt


    # =========================
    # BACKGROUND
    # =========================

    screen.fill(
        (5, 5, 12)
    )


    # =========================
    # IMAGE PARTICLES
    # =========================

    for p in particles:


        # -------------------------
        # PARTICLE DELAY
        # -------------------------

        if time_passed < p["delay"]:
            continue


        # -------------------------
        # TARGET DIRECTION
        # -------------------------

        dx = (
            p["target_x"]
            -
            p["x"]
        )

        dy = (
            p["target_y"]
            -
            p["y"]
        )


        # -------------------------
        # MOVE PARTICLE
        # -------------------------

        p["x"] += (
            dx * p["speed"]
        )

        p["y"] += (
            dy * p["speed"]
        )


        # -------------------------
        # FLOATING MOVEMENT
        # -------------------------

        wave_x = math.sin(
            time_passed * 3
            +
            p["angle"]
        ) * 0.8


        wave_y = math.cos(
            time_passed * 3
            +
            p["angle"]
        ) * 0.8


        draw_x = int(
            p["x"] + wave_x
        )


        draw_y = int(
            p["y"] + wave_y
        )


        # -------------------------
        # DISTANCE
        # -------------------------

        distance = math.sqrt(
            dx * dx
            +
            dy * dy
        )


        # =========================
        # PARTICLE GLOW
        # =========================

        if distance < 30:

            glow_size = (
                p["size"] * 5
            )


            glow_surface = pygame.Surface(
                (
                    glow_size * 2,
                    glow_size * 2
                ),
                pygame.SRCALPHA
            )


            pygame.draw.circle(

                glow_surface,

                (
                    p["r"],
                    p["g"],
                    p["b"],
                    40
                ),

                (
                    glow_size,
                    glow_size
                ),

                glow_size
            )


            screen.blit(

                glow_surface,

                (
                    draw_x - glow_size,
                    draw_y - glow_size
                )
            )


        # =========================
        # MAIN PARTICLE
        # =========================

        pygame.draw.circle(

            screen,

            (
                p["r"],
                p["g"],
                p["b"]
            ),

            (
                draw_x,
                draw_y
            ),

            p["size"]
        )


    # =========================
    # EXTRA SPARKLES
    # =========================

    if time_passed > 5:

        if random.random() < 0.15:

            glow_particles.append({

                "x": random.randint(
                    offset_x,
                    offset_x + new_w
                ),

                "y": random.randint(
                    offset_y,
                    offset_y + new_h
                ),

                "life": random.uniform(
                    0.5,
                    1.5
                ),

                "max_life": 1.5,

                "size": random.randint(
                    1,
                    3
                )

            })


    # =========================
    # DRAW SPARKLES
    # =========================

    for g in glow_particles[:]:

        g["life"] -= dt


        if g["life"] <= 0:

            glow_particles.remove(
                g
            )

            continue


        alpha = int(

            255
            *
            (
                g["life"]
                /
                g["max_life"]
            )

        )


        glow = pygame.Surface(
            (20, 20),
            pygame.SRCALPHA
        )


        pygame.draw.circle(

            glow,

            (
                255,
                255,
                255
            ),

            (
                10,
                10
            ),

            g["size"]
        )


        glow.set_alpha(
            alpha
        )


        screen.blit(

            glow,

            (
                g["x"] - 10,
                g["y"] - 10
            )
        )


    # =========================
    # FINAL IMAGE REVEAL
    # AFTER 30 SECONDS
    # =========================

    if time_passed > 30:

        alpha = min(

            255,

            int(
                (
                    time_passed - 30
                )
                *
                51
            )

        )


        final_image = image.copy()


        final_image.set_alpha(
            alpha
        )


        screen.blit(

            final_image,

            (
                offset_x,
                offset_y
            )
        )


    # =========================
    # EVENTS
    # =========================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


    # =========================
    # UPDATE SCREEN
    # =========================

    pygame.display.flip()


# =========================
# EXIT
# =========================

pygame.quit()