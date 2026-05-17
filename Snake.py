import pygame
import random
import json
import os

pygame.init()
info = pygame.display.Info()
SCREEN_W = info.current_w
SCREEN_H = info.current_h
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
move_delay = 175
last_move = 0
running = True
direction = "right"  # where it moves to right now
input_queue = []     # stores up to 2 queued inputs
TILE = 50
score = 0
COLS = 12
ROWS = 12
OFFSET_X = (SCREEN_W - COLS * TILE) // 2
OFFSET_Y = (SCREEN_H - ROWS * TILE) // 2
state = "menu"
current_size = "12x12"  # tracks which map size is being played

# images
def load_sprite(path):
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (TILE, TILE))
    return None  # fallback to rectangle if file missing

img_apple = load_sprite("assets/Snake_Apple.png")
img_body  = load_sprite("assets/Snake_Body.png")
img_grass = load_sprite("assets/Snake_Grass.png")
img_head  = load_sprite("assets/Snake_Head.png")
img_turn  = load_sprite("assets/Snake_Turn.png")
img_tail  = load_sprite("assets/Snake_Tail.png")

# pre-rotate head in all 4 directions — avoids offset bug
if img_head:
    head_sprites = {
        "up":    img_head,
        "down":  pygame.transform.rotate(img_head, 180),
        "left":  pygame.transform.rotate(img_head, 90),
        "right": pygame.transform.rotate(img_head, 270),
    }
else:
    head_sprites = None

if img_body:
    body_h = img_body                                # horizontal
    body_v = pygame.transform.rotate(img_body, 90)  # vertical
else:
    body_h = body_v = None

# pre-rotate turn pieces
if img_turn:
    turn_sprites = {
        -90: pygame.transform.rotate(img_turn, -90),
        0:   img_turn,
        90:  pygame.transform.rotate(img_turn, 90),
        180: pygame.transform.rotate(img_turn, 180),
    }
else:
    turn_sprites = None

# pre-rotate tail — faces down by default
if img_tail:
    tail_sprites = {
        "down":  img_tail,
        "up":    pygame.transform.rotate(img_tail, 180),
        "right": pygame.transform.rotate(img_tail, 90),
        "left":  pygame.transform.rotate(img_tail, 270),
    }
else:
    tail_sprites = None


# load highscores from file — one per map size
def load_highscores():
    if os.path.exists("highscore.json"):
        with open("highscore.json") as f:
            return json.load(f)
    return {"6x6": 0, "9x9": 0, "12x12": 0}


# save highscores to file
def save_highscores(highscores):
    with open("highscore.json", "w") as f:
        json.dump(highscores, f)


highscores = load_highscores()


# spawn food but not in the snake (free tiles)
def spawn_food(body, COLS, ROWS):
    free_tiles = []
    for x in range(COLS):
        for y in range(ROWS):
            pos = pygame.Vector2(x, y)
            if pos not in body:
                free_tiles.append(pos)
    if len(free_tiles) == 0:
        return None, None
    food = random.choice(free_tiles)
    return int(food.x), int(food.y)


body = [
    pygame.Vector2(COLS // 2, ROWS // 2),
    pygame.Vector2(COLS // 2 - 1, ROWS // 2),
    pygame.Vector2(COLS // 2 - 2, ROWS // 2),
]
food_x, food_y = spawn_food(body, COLS, ROWS)  # initial food spawn
font = pygame.font.Font(None, 36)

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if state == "menu":
                if event.key == pygame.K_RETURN:
                    state = "sizeselect"
                if event.key == pygame.K_x:  # close game
                    running = False
            # sizeselect
            elif state == "sizeselect":
                if event.key == pygame.K_1:
                    COLS, ROWS = 6, 6
                    current_size = "6x6"
                    OFFSET_X = (SCREEN_W - COLS * TILE) // 2
                    OFFSET_Y = (SCREEN_H - ROWS * TILE) // 2
                    body = [pygame.Vector2(COLS // 2, ROWS // 2), pygame.Vector2(COLS // 2 - 1, ROWS // 2), pygame.Vector2(COLS // 2 - 2, ROWS // 2)]
                    food_x, food_y = spawn_food(body, COLS, ROWS)
                    input_queue = []
                    state = "playing"
                if event.key == pygame.K_2:
                    COLS, ROWS = 9, 9
                    current_size = "9x9"
                    OFFSET_X = (SCREEN_W - COLS * TILE) // 2
                    OFFSET_Y = (SCREEN_H - ROWS * TILE) // 2
                    body = [pygame.Vector2(COLS // 2, ROWS // 2), pygame.Vector2(COLS // 2 - 1, ROWS // 2), pygame.Vector2(COLS // 2 - 2, ROWS // 2)]
                    food_x, food_y = spawn_food(body, COLS, ROWS)
                    input_queue = []
                    state = "playing"
                if event.key == pygame.K_3:
                    COLS, ROWS = 12, 12
                    current_size = "12x12"
                    OFFSET_X = (SCREEN_W - COLS * TILE) // 2
                    OFFSET_Y = (SCREEN_H - ROWS * TILE) // 2
                    body = [pygame.Vector2(COLS // 2, ROWS // 2), pygame.Vector2(COLS // 2 - 1, ROWS // 2), pygame.Vector2(COLS // 2 - 2, ROWS // 2)]
                    food_x, food_y = spawn_food(body, COLS, ROWS)
                    input_queue = []
                    state = "playing"
            # playing state
            elif state == "playing":
                if len(input_queue) < 2:  # max 2 queued inputs
                    # check against last queued direction to avoid reversing
                    last_dir = input_queue[-1] if input_queue else direction
                    if event.key == pygame.K_w and last_dir != "down":
                        input_queue.append("up")
                    if event.key == pygame.K_a and last_dir != "right":
                        input_queue.append("left")
                    if event.key == pygame.K_s and last_dir != "up":
                        input_queue.append("down")
                    if event.key == pygame.K_d and last_dir != "left":
                        input_queue.append("right")
            # game over (dead, wall collision or snake collision)
            elif state == "gameover":
                if event.key == pygame.K_RETURN:
                    # reset everything
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
                    # reset everything and go to menu
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
                    state = "menu"
                if event.key == pygame.K_x:  # close game
                    running = False

    # drawing every state
    if state == "menu":
        screen.fill("black")
        title     = font.render("SNAKE", True, "green")
        creator   = font.render("By Awack", True, "white")
        start     = font.render("ENTER = play", True, "white")
        quit_text = font.render("X = Quit Game", True, "grey")
        # highscore per map size
        hi1 = font.render(f"6x6   Best: {highscores['6x6']}", True, "yellow")
        hi2 = font.render(f"9x9   Best: {highscores['9x9']}", True, "yellow")
        hi3 = font.render(f"12x12 Best: {highscores['12x12']}", True, "yellow")
        # zentriert mit get_rect(center=...)
        screen.blit(title,     title.get_rect(center=(SCREEN_W // 2, 200)))
        screen.blit(start,     start.get_rect(center=(SCREEN_W // 2, 300)))
        screen.blit(hi1,       hi1.get_rect(center=(SCREEN_W // 2, 370)))
        screen.blit(hi2,       hi2.get_rect(center=(SCREEN_W // 2, 410)))
        screen.blit(hi3,       hi3.get_rect(center=(SCREEN_W // 2, 450)))
        screen.blit(quit_text, quit_text.get_rect(center=(SCREEN_W // 2, 520)))
        screen.blit(creator,   creator.get_rect(center=(SCREEN_W // 2, SCREEN_H - 40)))

    elif state == "sizeselect":
        screen.fill("black")
        title = font.render("SELECT SIZE:", True, "green")
        op1   = font.render("1 - Small (6x6)", True, "white")
        op2   = font.render("2 - Medium (9x9)", True, "white")
        op3   = font.render("3 - Large (12x12)", True, "white")
        screen.blit(title, title.get_rect(center=(SCREEN_W // 2, 250)))
        screen.blit(op1,   op1.get_rect(center=(SCREEN_W // 2, 340)))
        screen.blit(op2,   op2.get_rect(center=(SCREEN_W // 2, 390)))
        screen.blit(op3,   op3.get_rect(center=(SCREEN_W // 2, 440)))

    elif state == "playing":
        now = pygame.time.get_ticks()
        if now - last_move >= move_delay:
            last_move = now

            # apply next queued input
            if input_queue:
                direction = input_queue.pop(0)

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

            # wall collision
            if new_head.x < 0 or new_head.x >= COLS or new_head.y < 0 or new_head.y >= ROWS:
                if score > highscores[current_size]:
                    highscores[current_size] = score
                    save_highscores(highscores)
                state = "gameover"

            # self collision
            if new_head in body[1:]:
                if score > highscores[current_size]:
                    highscores[current_size] = score
                    save_highscores(highscores)
                state = "gameover"

            # apple eaten
            if new_head.x == food_x and new_head.y == food_y:  # dont pop -> snake grows
                # score + 1
                score += 1
                # speed increases every Xth apple
                if score % 2 == 0:
                    move_delay = max(move_delay - 2, 80)
                # new apple — use spawn_food so it doesnt spawn in the snake
                food_x, food_y = spawn_food(body, COLS, ROWS)
            else:
                body.pop()  # normal movement

        # fill screen black outside, grass only play area
        screen.fill("black")
        for gx in range(COLS):
            for gy in range(ROWS):
                if img_grass:
                    screen.blit(img_grass, (OFFSET_X + gx * TILE, OFFSET_Y + gy * TILE))
                else:
                    pygame.draw.rect(screen, "lightgreen", (OFFSET_X + gx * TILE, OFFSET_Y + gy * TILE, TILE, TILE))

        # grid lines — only inside play area
        for x in range(OFFSET_X, OFFSET_X + COLS * TILE + 1, TILE):
            pygame.draw.line(screen, (30, 30, 30), (x, OFFSET_Y), (x, OFFSET_Y + ROWS * TILE))
        for y in range(OFFSET_Y, OFFSET_Y + ROWS * TILE + 1, TILE):
            pygame.draw.line(screen, (30, 30, 30), (OFFSET_X, y), (OFFSET_X + COLS * TILE, y))

        # border around play area
        pygame.draw.rect(screen, "green", (OFFSET_X, OFFSET_Y, COLS * TILE, ROWS * TILE), 3)

        # draw food
        if img_apple:
            screen.blit(img_apple, (OFFSET_X + food_x * TILE, OFFSET_Y + food_y * TILE))
        else:
            pygame.draw.rect(screen, "red", (OFFSET_X + food_x * TILE, OFFSET_Y + food_y * TILE, TILE, TILE))

        # rendering snake — with head rotation, turn pieces and tail
        for i, segment in enumerate(body):
            x = OFFSET_X + segment.x * TILE
            y = OFFSET_Y + segment.y * TILE

            if i == 0:
                # head — use pre-rotated sprite based on direction
                if head_sprites:
                    screen.blit(head_sprites[direction], (x, y))
                else:
                    pygame.draw.rect(screen, "blue", (x, y, TILE, TILE))

            elif i == len(body) - 1:
                # tail — points away from segment in front of it
                prev = body[i - 1]
                dx = int(segment.x - prev.x)
                dy = int(segment.y - prev.y)
                tail_dir = {(0, -1): "up", (0, 1): "down", (-1, 0): "left", (1, 0): "right"}
                if tail_sprites:
                    screen.blit(tail_sprites[tail_dir[(dx, dy)]], (x, y))
                else:
                    pygame.draw.rect(screen, "purple", (x, y, TILE, TILE))

            else:
                prev = body[i - 1]  # segment in front
                nxt  = body[i + 1]  # segment behind

                # direction coming in and going out
                dx_in  = int(segment.x - prev.x)
                dy_in  = int(segment.y - prev.y)
                dx_out = int(nxt.x - segment.x)
                dy_out = int(nxt.y - segment.y)

                is_turn = (dx_in != dx_out or dy_in != dy_out)

                if is_turn and turn_sprites:
                    # figure out rotation of turn piece
                    if (dx_in == 1 and dy_out == 1) or (dy_in == -1 and dx_out == -1):
                        angle = -90
                    elif (dx_in == -1 and dy_out == 1) or (dy_in == -1 and dx_out == 1):
                        angle = 0
                    elif (dx_in == -1 and dy_out == -1) or (dy_in == 1 and dx_out == 1):
                        angle = 90
                    else:
                        angle = 180
                    screen.blit(turn_sprites[angle], (x, y))
                else:
                    # straight body — horizontal or vertical
                    if body_h and body_v:
                        if dx_in != 0:
                            screen.blit(body_v, (x, y))  # horizontal
                        else:
                            screen.blit(body_h, (x, y))  # vertical
                    else:
                        pygame.draw.rect(screen, "purple", (x, y, TILE, TILE))

        # showing score and current map size
        text = font.render(f"Score: {score}    Best: {highscores[current_size]}    Map: {current_size}", True, "white")
        screen.blit(text, text.get_rect(center=(SCREEN_W // 2, 20)))

    elif state == "gameover":
        screen.fill("black")
        over      = font.render("GAME OVER", True, "red")
        sc        = font.render(f"Score: {score}", True, "white")
        hi        = font.render(f"Best on {current_size}: {highscores[current_size]}", True, "yellow")
        restart   = font.render("ENTER = play again    ESC = menu", True, "white")
        quit_text = font.render("X = Quit Game", True, "grey")
        screen.blit(over,      over.get_rect(center=(SCREEN_W // 2, 280)))
        screen.blit(sc,        sc.get_rect(center=(SCREEN_W // 2, 340)))
        screen.blit(hi,        hi.get_rect(center=(SCREEN_W // 2, 390)))
        screen.blit(restart,   restart.get_rect(center=(SCREEN_W // 2, 450)))
        screen.blit(quit_text, quit_text.get_rect(center=(SCREEN_W // 2, 500)))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)

pygame.quit()