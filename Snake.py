import pygame
import random
import json
import os

pygame.init()
screen = pygame.display.set_mode((1200, 720))
clock = pygame.time.Clock()
running = True
direction = "right"  # where it moves to right now
next_direction = "right"  # Key buffer so you dont overwrite it instantly when spamming inputs in one frame(where it wants to move)
TILE = 50
score = 0
tick = 2.5
COLS = 12
ROWS = 12
OFFSET_X = (1200 - COLS * TILE) // 2
OFFSET_Y = (720 - ROWS * TILE) // 2
state = "menu"


# load highscore from file
def load_highscore():
    if os.path.exists("highscore.json"):
        with open("highscore.json") as f:
            return json.load(f)["highscore"]
    return 0


# save highscore to file
def save_highscore(score):
    with open("highscore.json", "w") as f:
        json.dump({"highscore": score}, f)


highscore = load_highscore()


# spawn food but not in the snake
def spawn_food(body, COLS, ROWS):
    while True:
        food_x = random.randint(0, COLS - 1)
        food_y = random.randint(0, ROWS - 1)
        if pygame.Vector2(food_x, food_y) not in body:  # not in the snake
            return food_x, food_y


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
                    OFFSET_X = (1200 - COLS * TILE) // 2
                    OFFSET_Y = (720 - ROWS * TILE) // 2
                    body = [pygame.Vector2(COLS // 2, ROWS // 2), pygame.Vector2(COLS // 2 - 1, ROWS // 2), pygame.Vector2(COLS // 2 - 2, ROWS // 2)]
                    food_x, food_y = spawn_food(body, COLS, ROWS)
                    state = "playing"
                if event.key == pygame.K_2:
                    COLS, ROWS = 9, 9
                    OFFSET_X = (1200 - COLS * TILE) // 2
                    OFFSET_Y = (720 - ROWS * TILE) // 2
                    body = [pygame.Vector2(COLS // 2, ROWS // 2), pygame.Vector2(COLS // 2 - 1, ROWS // 2), pygame.Vector2(COLS // 2 - 2, ROWS // 2)]
                    food_x, food_y = spawn_food(body, COLS, ROWS)
                    state = "playing"
                if event.key == pygame.K_3:
                    COLS, ROWS = 12, 12
                    OFFSET_X = (1200 - COLS * TILE) // 2
                    OFFSET_Y = (720 - ROWS * TILE) // 2
                    body = [pygame.Vector2(COLS // 2, ROWS // 2), pygame.Vector2(COLS // 2 - 1, ROWS // 2), pygame.Vector2(COLS // 2 - 2, ROWS // 2)]
                    food_x, food_y = spawn_food(body, COLS, ROWS)
                    state = "playing"

            # playing state
            elif state == "playing":
                # KeyDetecting
                if event.key == pygame.K_w and direction != "down":
                    next_direction = "up"
                if event.key == pygame.K_a and direction != "right":
                    next_direction = "left"
                if event.key == pygame.K_s and direction != "up":
                    next_direction = "down"
                if event.key == pygame.K_d and direction != "left":
                    next_direction = "right"

            # game over (dead, wall collision or snake collision)
            elif state == "gameover":
                if event.key == pygame.K_RETURN:
                    # reset everything
                    score = 0
                    tick = 2.5
                    direction = "right"
                    next_direction = "right"
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
                    tick = 2.5
                    direction = "right"
                    next_direction = "right"
                    body = [
                        pygame.Vector2(COLS // 2, ROWS // 2),
                        pygame.Vector2(COLS // 2 - 1, ROWS // 2),
                        pygame.Vector2(COLS // 2 - 2, ROWS // 2),
                    ]
                    food_x, food_y = spawn_food(body, COLS, ROWS)
                    state = "menu"
                if event.key == pygame.K_x:  # close game
                    running = False
    
    #drawing every state
    if state == "menu":
        screen.fill("black")
        title = font.render("SNAKE", True, "green")
        creator = font.render("By Awack", True, "white")
        start = font.render("ENTER = play", True, "white")
        hi = font.render(f"High Score: {highscore}", True, "yellow")
        quit_text = font.render("X = Quit Game", True, "grey")
       # zentriert mit get_rect(center=...)
        screen.blit(title, title.get_rect(center = (600, 250)))
        screen.blit(start, start.get_rect(center = (600, 350)))
        screen.blit(hi, hi.get_rect(center = (600, 400)))
        screen.blit(quit_text, quit_text.get_rect(center = (600, 450)))
        screen.blit(creator, creator.get_rect(center = (600, 680)))

    elif state == "sizeselect":
        screen.fill("black")
        title = font.render("SELECT SIZE:", True, "green")
        op1 = font.render("1 - Small (6x6)", True, "white")
        op2 = font.render("2 - Medium (9x9)", True, "white")
        op3 = font.render("3 - Large (12x12)", True, "white")
        screen.blit(title, title.get_rect(center = (600, 250)))
        screen.blit(op1, op1.get_rect(center = (600, 340)))
        screen.blit(op2, op2.get_rect(center = (600, 390)))
        screen.blit(op3, op3.get_rect(center = (600, 440)))

    elif state == "playing":
        # KeyHandling
        direction = next_direction

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
            if score > highscore:
                highscore = score
                save_highscore(score)
            state = "gameover"

        # self collision
        if new_head in body[1:]:
            if score > highscore:
                highscore = score
                save_highscore(score)
            state = "gameover"

        # apple eaten
        if new_head.x == food_x and new_head.y == food_y:  # dont pop -> snake grows
            # score + 1
            score += 1
            # speed increases every Xth apple
            if score % 2 == 0:
                tick = min(tick + 0.5, 10)
            # new apple — use spawn_food so it doesnt spawn in the snake
            food_x, food_y = spawn_food(body, COLS, ROWS)
        else:
            body.pop()  # normal movement

        # fill screen black outside, green only play area
        screen.fill("black")
        pygame.draw.rect(screen, "lightgreen", (OFFSET_X, OFFSET_Y, COLS * TILE, ROWS * TILE))

        # grid lines — only inside play area
        for x in range(OFFSET_X, OFFSET_X + COLS * TILE + 1, TILE):
            pygame.draw.line(screen, (30, 30, 30), (x, OFFSET_Y), (x, OFFSET_Y + ROWS * TILE))
        for y in range(OFFSET_Y, OFFSET_Y + ROWS * TILE + 1, TILE):
            pygame.draw.line(screen, (30, 30, 30), (OFFSET_X, y), (OFFSET_X + COLS * TILE, y))

        # border around play area
        pygame.draw.rect(screen, "green", (OFFSET_X, OFFSET_Y, COLS * TILE, ROWS * TILE), 3)

        # draw food
        pygame.draw.rect(screen, "red", (OFFSET_X + food_x * TILE, OFFSET_Y + food_y * TILE, TILE, TILE))

        # rendering snake
        for segment in body:
            if(segment == body[0]):
                pygame.draw.rect(screen, "blue", (OFFSET_X + segment.x * TILE, OFFSET_Y + segment.y * TILE, TILE, TILE))
            else:
                pygame.draw.rect(screen, "purple", (OFFSET_X + segment.x * TILE, OFFSET_Y + segment.y * TILE, TILE, TILE))

        # showing score
        text = font.render(f"Score: {score}", True, "white")
        screen.blit(text, (550, 10))

    elif state == "gameover":
        screen.fill("black")
        over = font.render("GAME OVER", True, "red")
        sc = font.render(f"Score: {score}", True, "white")
        hi = font.render(f"High Score: {highscore}", True, "yellow")
        restart = font.render("ENTER = play again    ESC = menu", True, "white")
        quit_text = font.render("X = Quit Game", True, "grey")
        screen.blit(over, over.get_rect(center = (600, 280)))
        screen.blit(sc, sc.get_rect(center = (600, 340)))
        screen.blit(hi, hi.get_rect(center = (600, 390)))
        screen.blit(restart, restart.get_rect(center = (600, 450)))
        screen.blit(quit_text, quit_text.get_rect(center = (600, 500)))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(tick)

pygame.quit()