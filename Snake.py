import pygame
import random
import json
import os

pygame.init()

# get fullscreen resolution automatically
info = pygame.display.Info()
SCREEN_W = info.current_w
SCREEN_H = info.current_h

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

# movement timing
move_delay = 175
last_move = 0

running = True

# snake movement
direction = "right"
input_queue = []

# board settings
TILE = 50
score = 0

COLS = 12
ROWS = 12

# keeps board centered on every resolution
OFFSET_X = (SCREEN_W - COLS * TILE) // 2
OFFSET_Y = (SCREEN_H - ROWS * TILE) // 2

state = "menu"
current_size = "12x12"


# ---------------- SPRITES / SOUNDS ---------------- #


def load_sprite(path):
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (TILE, TILE))
    return None


def load_sound(path):
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    return None


pygame.mixer.init()

snd_eat = load_sound("assets/sounds/Apple_Eat_Sound.wav")
snd_death = load_sound("assets/sounds/Snake_Died_Sound.wav")
snd_menu_select = load_sound("assets/sounds/Menu_Select_Sound.wav")
snd_movement = load_sound("assets/sounds/Movement_sound (2).wav")

# sound balancing
if snd_eat:
    snd_eat.set_volume(0.3)

if snd_death:
    snd_death.set_volume(0.3)

if snd_menu_select:
    snd_menu_select.set_volume(1.0)

if snd_movement:
    snd_movement.set_volume(1.0)

img_apple = load_sprite("assets/Snake_Apple.png")
img_body = load_sprite("assets/Snake_Body.png")
img_grass = load_sprite("assets/Snake_Grass.png")
img_head = load_sprite("assets/Snake_Head.png")
img_turn = load_sprite("assets/Snake_Turn.png")
img_tail = load_sprite("assets/Snake_Tail.png")


# pre-rotated sprites so pygame doesnt rotate every frame
if img_head:
    head_sprites = {
        "up": img_head,
        "down": pygame.transform.rotate(img_head, 180),
        "left": pygame.transform.rotate(img_head, 90),
        "right": pygame.transform.rotate(img_head, 270),
    }
else:
    head_sprites = None

if img_body:
    body_h = img_body
    body_v = pygame.transform.rotate(img_body, 90)
else:
    body_h = body_v = None

if img_turn:
    turn_sprites = {
        -90: pygame.transform.rotate(img_turn, -90),
        0: img_turn,
        90: pygame.transform.rotate(img_turn, 90),
        180: pygame.transform.rotate(img_turn, 180),
    }
else:
    turn_sprites = None

if img_tail:
    tail_sprites = {
        "down": img_tail,
        "up": pygame.transform.rotate(img_tail, 180),
        "right": pygame.transform.rotate(img_tail, 90),
        "left": pygame.transform.rotate(img_tail, 270),
    }
else:
    tail_sprites = None


# ---------------- HIGHSCORES ---------------- #


def load_highscores():
    if os.path.exists("highscore.json"):
        with open("highscore.json") as f:
            return json.load(f)

    return {"6x6": 0, "9x9": 0, "12x12": 0}


def save_highscores(highscores):
    with open("highscore.json", "w") as f:
        json.dump(highscores, f)


highscores = load_highscores()


# ---------------- FOOD ---------------- #


# prevents food from spawning inside the snake
def spawn_food(body, COLS, ROWS):

    free_tiles = []

    for x in range(COLS):
        for y in range(ROWS):
            pos = pygame.Vector2(x, y)

            if pos not in body:
                free_tiles.append(pos)

    # if no free tiles exist -> player filled map
    if len(free_tiles) == 0:
        return None, None

    food = random.choice(free_tiles)

    return int(food.x), int(food.y)


# ---------------- GAME START ---------------- #

body = [
    pygame.Vector2(COLS // 2, ROWS // 2),
    pygame.Vector2(COLS // 2 - 1, ROWS // 2),
    pygame.Vector2(COLS // 2 - 2, ROWS // 2),
]

food_x, food_y = spawn_food(body, COLS, ROWS)

font = pygame.font.Font(None, 36)


# ---------------- MAIN LOOP ---------------- #

while running:
    # ---------- EVENTS ---------- #

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # ---------- MENU ---------- #

            if state == "menu":
                if event.key == pygame.K_RETURN:
                    if snd_menu_select:
                        snd_menu_select.play()

                    state = "sizeselect"

                if event.key == pygame.K_x:
                    running = False

            # ---------- SIZE SELECT ---------- #

            elif state == "sizeselect":
                if event.key == pygame.K_1:
                    if snd_menu_select:
                        snd_menu_select.play()

                    COLS, ROWS = 6, 6
                    current_size = "6x6"

                    TILE = 70

                if event.key == pygame.K_2:
                    if snd_menu_select:
                        snd_menu_select.play()

                    COLS, ROWS = 9, 9
                    current_size = "9x9"

                    TILE = 55

                if event.key == pygame.K_3:
                    if snd_menu_select:
                        snd_menu_select.play()

                    COLS, ROWS = 12, 12
                    current_size = "12x12"

                    # slightly smaller so full map fits on screen
                    TILE = 42

                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    OFFSET_X = (SCREEN_W - COLS * TILE) // 2
                    OFFSET_Y = (SCREEN_H - ROWS * TILE) // 2

                    body = [
                        pygame.Vector2(COLS // 2, ROWS // 2),
                        pygame.Vector2(COLS // 2 - 1, ROWS // 2),
                        pygame.Vector2(COLS // 2 - 2, ROWS // 2),
                    ]

                    food_x, food_y = spawn_food(body, COLS, ROWS)

                    direction = "right"
                    input_queue = []

                    state = "playing"

            # ---------- PLAYING ---------- #

            elif state == "playing":
                # max 2 buffered inputs
                if len(input_queue) < 2:
                    last_dir = input_queue[-1] if input_queue else direction

                    if event.key == pygame.K_w and last_dir != "down":
                        input_queue.append("up")

                    if event.key == pygame.K_a and last_dir != "right":
                        input_queue.append("left")

                    if event.key == pygame.K_s and last_dir != "up":
                        input_queue.append("down")

                    if event.key == pygame.K_d and last_dir != "left":
                        input_queue.append("right")

            # ---------- GAME OVER ---------- #

            elif state == "gameover":
                if event.key == pygame.K_RETURN:
                    if snd_menu_select:
                        snd_menu_select.play()

                    score = 0
                    move_delay = 175

                    direction = "right"
                    input_queue = []

                    body = [
                        pygame.Vector2(COLS // 2, ROWS // 2),
                        pygame.Vector2(COLS // 2 - 1, ROWS // 2),
                        pygame.Vector2(COLS // 2 - 2, ROWS // 2),
                    ]

                    food_x, food_y = spawn_food(body, COLS, ROWS)

                    state = "playing"

                if event.key == pygame.K_ESCAPE:
                    if snd_menu_select:
                        snd_menu_select.play()

                    score = 0
                    move_delay = 175

                    direction = "right"
                    input_queue = []

                    state = "menu"

                if event.key == pygame.K_x:
                    running = False

    # ---------- MENU DRAW ---------- #

    if state == "menu":
        screen.fill("black")

        title = font.render("SNAKE", True, "green")
        creator = font.render("By Awack", True, "white")
        start = font.render("ENTER = play", True, "white")
        quit_text = font.render("X = Quit Game", True, "grey")

        hi1 = font.render(f"6x6   Best: {highscores['6x6']}", True, "yellow")
        hi2 = font.render(f"9x9   Best: {highscores['9x9']}", True, "yellow")
        hi3 = font.render(f"12x12 Best: {highscores['12x12']}", True, "yellow")

        screen.blit(title, title.get_rect(center=(SCREEN_W // 2, 200)))
        screen.blit(start, start.get_rect(center=(SCREEN_W // 2, 300)))

        screen.blit(hi1, hi1.get_rect(center=(SCREEN_W // 2, 370)))
        screen.blit(hi2, hi2.get_rect(center=(SCREEN_W // 2, 410)))
        screen.blit(hi3, hi3.get_rect(center=(SCREEN_W // 2, 450)))

        screen.blit(quit_text, quit_text.get_rect(center=(SCREEN_W // 2, 520)))
        screen.blit(creator, creator.get_rect(center=(SCREEN_W // 2, SCREEN_H - 40)))

    # ---------- SIZE SELECT DRAW ---------- #

    elif state == "sizeselect":
        screen.fill("black")

        title = font.render("SELECT SIZE:", True, "green")

        op1 = font.render("1 - Small (6x6)", True, "white")
        op2 = font.render("2 - Medium (9x9)", True, "white")
        op3 = font.render("3 - Large (12x12)", True, "white")

        screen.blit(title, title.get_rect(center=(SCREEN_W // 2, 250)))

        screen.blit(op1, op1.get_rect(center=(SCREEN_W // 2, 340)))
        screen.blit(op2, op2.get_rect(center=(SCREEN_W // 2, 390)))
        screen.blit(op3, op3.get_rect(center=(SCREEN_W // 2, 440)))

    # ---------- GAME ---------- #

    elif state == "playing":
        now = pygame.time.get_ticks()

        if now - last_move >= move_delay:
            last_move = now

            # buffered turning system
            if input_queue:
                new_direction = input_queue.pop(0)

                # sound only when direction actually changes
                if new_direction != direction and snd_movement:
                    snd_movement.play()

                direction = new_direction

            new_head = pygame.Vector2(body[0])

            if direction == "up":
                new_head.y -= 1

            if direction == "down":
                new_head.y += 1

            if direction == "left":
                new_head.x -= 1

            if direction == "right":
                new_head.x += 1

            body.insert(0, new_head)

            # ---------- COLLISIONS ---------- #

            if (
                new_head.x < 0
                or new_head.x >= COLS
                or new_head.y < 0
                or new_head.y >= ROWS
            ):
                if snd_death:
                    snd_death.play()

                if score > highscores[current_size]:
                    highscores[current_size] = score
                    save_highscores(highscores)

                state = "gameover"

            if new_head in body[1:]:
                if snd_death:
                    snd_death.play()

                if score > highscores[current_size]:
                    highscores[current_size] = score
                    save_highscores(highscores)

                state = "gameover"

            # ---------- APPLE ---------- #

            if new_head.x == food_x and new_head.y == food_y:
                if snd_eat:
                    snd_eat.play()

                score += 1

                # slowly speeds game up
                if score % 2 == 0:
                    move_delay = max(move_delay - 2, 80)

                food_x, food_y = spawn_food(body, COLS, ROWS)

                # if map is completely filled -> win/gameover
                if food_x is None and food_y is None:
                    if score > highscores[current_size]:
                        highscores[current_size] = score
                        save_highscores(highscores)

                    state = "gameover"

            else:
                body.pop()

        # ---------- DRAW BOARD ---------- #

        screen.fill("black")

        for gx in range(COLS):
            for gy in range(ROWS):
                draw_x = OFFSET_X + gx * TILE
                draw_y = OFFSET_Y + gy * TILE

                if img_grass:
                    grass = pygame.transform.scale(img_grass, (TILE, TILE))
                    screen.blit(grass, (draw_x, draw_y))

                else:
                    pygame.draw.rect(screen, "lightgreen", (draw_x, draw_y, TILE, TILE))

        # grid
        for x in range(OFFSET_X, OFFSET_X + COLS * TILE + 1, TILE):
            pygame.draw.line(
                screen, (30, 30, 30), (x, OFFSET_Y), (x, OFFSET_Y + ROWS * TILE)
            )

        for y in range(OFFSET_Y, OFFSET_Y + ROWS * TILE + 1, TILE):
            pygame.draw.line(
                screen, (30, 30, 30), (OFFSET_X, y), (OFFSET_X + COLS * TILE, y)
            )

        pygame.draw.rect(
            screen, "green", (OFFSET_X, OFFSET_Y, COLS * TILE, ROWS * TILE), 3
        )

        # ---------- FOOD ---------- #

        if food_x is not None and food_y is not None:
            if img_apple:
                apple_scaled = pygame.transform.scale(img_apple, (TILE, TILE))

                screen.blit(
                    apple_scaled, (OFFSET_X + food_x * TILE, OFFSET_Y + food_y * TILE)
                )

            else:
                pygame.draw.rect(
                    screen,
                    "red",
                    (OFFSET_X + food_x * TILE, OFFSET_Y + food_y * TILE, TILE, TILE),
                )

        # ---------- SNAKE ---------- #

        for i, segment in enumerate(body):
            x = OFFSET_X + segment.x * TILE
            y = OFFSET_Y + segment.y * TILE

            # HEAD
            if i == 0:
                if head_sprites:
                    head_scaled = pygame.transform.scale(
                        head_sprites[direction], (TILE, TILE)
                    )

                    screen.blit(head_scaled, (x, y))

                else:
                    pygame.draw.rect(screen, "blue", (x, y, TILE, TILE))

            # TAIL
            elif i == len(body) - 1:
                prev = body[i - 1]

                dx = int(segment.x - prev.x)
                dy = int(segment.y - prev.y)

                tail_dir = {
                    (0, -1): "up",
                    (0, 1): "down",
                    (-1, 0): "left",
                    (1, 0): "right",
                }

                if tail_sprites:
                    tail_scaled = pygame.transform.scale(
                        tail_sprites[tail_dir[(dx, dy)]], (TILE, TILE)
                    )

                    screen.blit(tail_scaled, (x, y))

                else:
                    pygame.draw.rect(screen, "purple", (x, y, TILE, TILE))

            # BODY
            else:
                prev = body[i - 1]
                nxt = body[i + 1]

                dx_in = int(segment.x - prev.x)
                dy_in = int(segment.y - prev.y)

                dx_out = int(nxt.x - segment.x)
                dy_out = int(nxt.y - segment.y)

                is_turn = dx_in != dx_out or dy_in != dy_out

                if is_turn and turn_sprites:
                    if (dx_in == 1 and dy_out == 1) or (dy_in == -1 and dx_out == -1):
                        angle = -90

                    elif (dx_in == -1 and dy_out == 1) or (dy_in == -1 and dx_out == 1):
                        angle = 0

                    elif (dx_in == -1 and dy_out == -1) or (dy_in == 1 and dx_out == 1):
                        angle = 90

                    else:
                        angle = 180

                    turn_scaled = pygame.transform.scale(
                        turn_sprites[angle], (TILE, TILE)
                    )

                    screen.blit(turn_scaled, (x, y))

                else:
                    if body_h and body_v:
                        if dx_in != 0:
                            body_scaled = pygame.transform.scale(body_v, (TILE, TILE))

                            screen.blit(body_scaled, (x, y))

                        else:
                            body_scaled = pygame.transform.scale(body_h, (TILE, TILE))

                            screen.blit(body_scaled, (x, y))

                    else:
                        pygame.draw.rect(screen, "purple", (x, y, TILE, TILE))

        # ---------- SCORE ---------- #

        text = font.render(
            f"Score: {score}    Best: {highscores[current_size]}    Map: {current_size}",
            True,
            "white",
        )

        screen.blit(text, text.get_rect(center=(SCREEN_W // 2, 20)))

    # ---------- GAME OVER ---------- #

    elif state == "gameover":
        screen.fill("black")

        over = font.render("GAME OVER", True, "red")

        sc = font.render(f"Score: {score}", True, "white")

        hi = font.render(
            f"Best on {current_size}: {highscores[current_size]}", True, "yellow"
        )

        restart = font.render("ENTER = play again    ESC = menu", True, "white")

        quit_text = font.render("X = Quit Game", True, "grey")

        screen.blit(over, over.get_rect(center=(SCREEN_W // 2, 280)))
        screen.blit(sc, sc.get_rect(center=(SCREEN_W // 2, 340)))
        screen.blit(hi, hi.get_rect(center=(SCREEN_W // 2, 390)))

        screen.blit(restart, restart.get_rect(center=(SCREEN_W // 2, 450)))

        screen.blit(quit_text, quit_text.get_rect(center=(SCREEN_W // 2, 500)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
