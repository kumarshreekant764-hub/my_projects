
import pygame
import random
import sys

pygame.init()

# =========================
# SCREEN
# =========================

WIDTH = 1000
HEIGHT = 450

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Runner")

clock = pygame.time.Clock()
FPS = 60

# =========================
# COLORS
# =========================

WHITE = (247, 247, 247)
BLACK = (40, 40, 40)
GRAY = (120, 120, 120)
GREEN = (70, 140, 70)
DARK_GREEN = (45, 100, 45)
BROWN = (130, 90, 50)

# =========================
# GROUND
# =========================

GROUND_Y = 350

# =========================
# FONTS
# =========================

font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 60)

# =========================
# DINO CLASS
# =========================

class Dino:

    def __init__(self):

        self.x = 100
        self.y = GROUND_Y - 70

        self.width = 55
        self.height = 70

        self.velocity_y = 0

        self.gravity = 1.1
        self.jump_power = -20

        self.ducking = False

        self.animation_timer = 0
        self.frame = 0

    def jump(self):

        if self.y >= GROUND_Y - self.height:

            self.velocity_y = self.jump_power

    def update(self):

        # Gravity
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # Ground collision
        if self.y >= GROUND_Y - self.height:

            self.y = GROUND_Y - self.height
            self.velocity_y = 0

        # Running animation
        self.animation_timer += 1

        if self.animation_timer >= 8:

            self.animation_timer = 0
            self.frame += 1

            if self.frame > 1:
                self.frame = 0

    def get_rect(self):

        if self.ducking:

            return pygame.Rect(
                self.x,
                self.y + 30,
                70,
                40
            )

        return pygame.Rect(
            self.x + 8,
            self.y + 5,
            40,
            60
        )

    def draw(self, surface):

        color = BLACK

        # =====================
        # DINO BODY
        # =====================

        if self.ducking:

            # Body
            pygame.draw.rect(
                surface,
                color,
                (self.x, self.y + 30, 65, 35)
            )

            # Head
            pygame.draw.rect(
                surface,
                color,
                (self.x + 45, self.y + 15, 35, 35)
            )

            # Eye
            pygame.draw.rect(
                surface,
                WHITE,
                (self.x + 65, self.y + 22, 5, 5)
            )

            # Legs
            pygame.draw.rect(
                surface,
                color,
                (self.x + 10, self.y + 55, 10, 20)
            )

            pygame.draw.rect(
                surface,
                color,
                (self.x + 45, self.y + 55, 10, 20)
            )

            # Tail
            pygame.draw.polygon(
                surface,
                color,
                [
                    (self.x + 5, self.y + 35),
                    (self.x - 20, self.y + 20),
                    (self.x + 5, self.y + 50)
                ]
            )

        else:

            # Body
            pygame.draw.rect(
                surface,
                color,
                (self.x + 15, self.y + 25, 35, 40)
            )

            # Head
            pygame.draw.rect(
                surface,
                color,
                (self.x + 30, self.y + 5, 35, 35)
            )

            # Snout
            pygame.draw.rect(
                surface,
                color,
                (self.x + 55, self.y + 18, 20, 20)
            )

            # Eye
            pygame.draw.rect(
                surface,
                WHITE,
                (self.x + 55, self.y + 10, 5, 5)
            )

            # Tail
            pygame.draw.polygon(
                surface,
                color,
                [
                    (self.x + 15, self.y + 35),
                    (self.x - 20, self.y + 15),
                    (self.x + 5, self.y + 45)
                ]
            )

            # Arms
            pygame.draw.rect(
                surface,
                color,
                (self.x + 42, self.y + 38, 20, 8)
            )

            # Legs animation
            if self.frame == 0:

                pygame.draw.rect(
                    surface,
                    color,
                    (self.x + 18, self.y + 60, 10, 25)
                )

                pygame.draw.rect(
                    surface,
                    color,
                    (self.x + 40, self.y + 60, 10, 18)
                )

            else:

                pygame.draw.rect(
                    surface,
                    color,
                    (self.x + 18, self.y + 60, 10, 18)
                )

                pygame.draw.rect(
                    surface,
                    color,
                    (self.x + 40, self.y + 60, 10, 25)
                )


# =========================
# CACTUS CLASS
# =========================

class Cactus:

    def __init__(self):

        self.x = WIDTH + random.randint(0, 200)

        self.height = random.choice(
            [45, 55, 65, 75]
        )

        self.width = random.choice(
            [25, 30, 35]
        )

        self.y = GROUND_Y - self.height

    def update(self, speed):

        self.x -= speed

    def get_rect(self):

        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def draw(self, surface):

        color = DARK_GREEN

        # Main cactus
        pygame.draw.rect(
            surface,
            color,
            (
                self.x,
                self.y,
                self.width,
                self.height
            )
        )

        # Left arm
        if self.height > 40:

            pygame.draw.rect(
                surface,
                color,
                (
                    self.x - 12,
                    self.y + 20,
                    12,
                    10
                )
            )

            pygame.draw.rect(
                surface,
                color,
                (
                    self.x - 12,
                    self.y + 10,
                    10,
                    20
                )
            )

        # Right arm
        if self.height > 70:

            pygame.draw.rect(
                surface,
                color,
                (
                    self.x + self.width,
                    self.y + 30,
                    12,
                    10
                )
            )

            pygame.draw.rect(
                surface,
                color,
                (
                    self.x + self.width + 2,
                    self.y + 20,
                    10,
                    20
                )
            )


# =========================
# CLOUD CLASS
# =========================

class Cloud:

    def __init__(self):

        self.x = WIDTH + random.randint(0, 500)
        self.y = random.randint(50, 180)

        self.speed = random.uniform(1, 2)

    def update(self):

        self.x -= self.speed

        if self.x < -120:

            self.x = WIDTH + random.randint(100, 400)
            self.y = random.randint(50, 180)

    def draw(self, surface):

        color = (190, 190, 190)

        pygame.draw.circle(
            surface,
            color,
            (int(self.x), int(self.y)),
            20
        )

        pygame.draw.circle(
            surface,
            color,
            (int(self.x + 25), int(self.y - 10)),
            25
        )

        pygame.draw.circle(
            surface,
            color,
            (int(self.x + 50), int(self.y)),
            20
        )

        pygame.draw.rect(
            surface,
            color,
            (
                self.x - 5,
                self.y,
                60,
                20
            )
        )


# =========================
# GAME VARIABLES
# =========================

dino = Dino()

cactuses = []

clouds = [
    Cloud(),
    Cloud(),
    Cloud()
]

score = 0
high_score = 0

speed = 7

spawn_timer = 0

game_over = False

night = False

# =========================
# RESET GAME
# =========================

def reset_game():

    global dino
    global cactuses
    global score
    global speed
    global spawn_timer
    global game_over
    global night

    dino = Dino()

    cactuses = []

    score = 0

    speed = 7

    spawn_timer = 0

    game_over = False

    night = False


# =========================
# MAIN GAME LOOP
# =========================

while True:

    # =====================
    # EVENTS
    # =====================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # Jump
            if event.key in (
                pygame.K_SPACE,
                pygame.K_UP
            ):

                if not game_over:

                    dino.jump()

            # Restart
            if event.key == pygame.K_r:

                if game_over:

                    reset_game()

    # =====================
    # KEYBOARD
    # =====================

    keys = pygame.key.get_pressed()

    if not game_over:

        # Duck
        if keys[pygame.K_DOWN]:

            dino.ducking = True

        else:

            dino.ducking = False

        # =================
        # UPDATE DINO
        # =================

        dino.update()

        # =================
        # CLOUDS
        # =================

        for cloud in clouds:

            cloud.update()

        # =================
        # CACTUS SPAWN
        # =================

        spawn_timer += 1

        if spawn_timer > random.randint(70, 130):

            cactuses.append(Cactus())

            spawn_timer = 0

        # =================
        # CACTUS MOVEMENT
        # =================

        for cactus in cactuses:

            cactus.update(speed)

        # Remove old cactus

        cactuses = [
            cactus
            for cactus in cactuses
            if cactus.x > -100
        ]

        # =================
        # COLLISION
        # =================

        dino_rect = dino.get_rect()

        for cactus in cactuses:

            if dino_rect.colliderect(
                cactus.get_rect()
            ):

                game_over = True

        # =================
        # SCORE
        # =================

        score += 1

        # Increase speed

        if score % 500 == 0:

            speed += 0.5

        # Day/Night cycle

        if score % 1500 == 0:

            night = not night

        # High score

        if score > high_score:

            high_score = score

    # =====================
    # BACKGROUND
    # =====================

    if night:

        screen.fill((30, 30, 40))

        ground_color = (220, 220, 220)

    else:

        screen.fill(WHITE)

        ground_color = BLACK

    # =====================
    # CLOUDS
    # =====================

    if not night:

        for cloud in clouds:

            cloud.draw(screen)

    # =====================
    # GROUND
    # =====================

    pygame.draw.line(
        screen,
        ground_color,
        (0, GROUND_Y),
        (WIDTH, GROUND_Y),
        3
    )

    # Ground small lines

    for x in range(
        0,
        WIDTH,
        40
    ):

        pygame.draw.line(
            screen,
            ground_color,
            (x, GROUND_Y + 10),
            (x + 15, GROUND_Y + 10),
            2
        )

    # =====================
    # DINO
    # =====================

    dino.draw(screen)

    # =====================
    # CACTUSES
    # =====================

    for cactus in cactuses:

        cactus.draw(screen)

    # =====================
    # SCORE
    # =====================

    score_text = font.render(
        f"HI {high_score // 10:05d}  {score // 10:05d}",
        True,
        ground_color
    )

    screen.blit(
        score_text,
        (WIDTH - 230, 25)
    )

    # =====================
    # SPEED
    # =====================

    speed_text = font.render(
        f"Speed: {speed:.1f}",
        True,
        ground_color
    )

    screen.blit(
        speed_text,
        (20, 20)
    )

    # =====================
    # GAME OVER
    # =====================

    if game_over:

        text = big_font.render(
            "GAME OVER",
            True,
            ground_color
        )

        screen.blit(
            text,
            (
                WIDTH // 2 - text.get_width() // 2,
                170
            )
        )

        restart_text = font.render(
            "Press R to Restart",
            True,
            ground_color
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 -
                restart_text.get_width() // 2,
                235
            )
        )

    # =====================
    # UPDATE SCREEN
    # =====================

    pygame.display.update()

    clock.tick(FPS)
