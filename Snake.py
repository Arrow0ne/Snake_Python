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

food_x = random.randint(0, (1200 // TILE) - 1) * TILE
food_y = random.randint(0, (720 // TILE) - 1) * TILE
body = [pygame.Vector2(600, 350), pygame.Vector2(550, 350), pygame.Vector2(500, 350)]
font = pygame.font.Font(None, 36)

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if state == "menu":
                if event.key == pygame.K_RETURN:
                    state = "playing"
                if event.key == pygame.K_x:  # close game
                    running = False
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
            elif state == "gameover":
                if event.key == pygame.K_RETURN:
                    # reset everything
                    score = 0
                    tick = 2.5
                    direction = "right"
                    next_direction = "right"
                    body = [pygame.Vector2(600, 350), pygame.Vector2(550, 350), pygame.Vector2(500, 350)]
                    food_x = random.randint(0, (1200 // TILE) - 1) * TILE
                    food_y = random.randint(0, (720 // TILE) - 1) * TILE
                    state = "playing"
                if event.key == pygame.K_ESCAPE:
                    # reset everything and go to menu
                    score = 0
                    tick = 2.5
                    direction = "right"
                    next_direction = "right"
                    body = [pygame.Vector2(600, 350), pygame.Vector2(550, 350), pygame.Vector2(500, 350)]
                    food_x = random.randint(0, (1200 // TILE) - 1) * TILE
                    food_y = random.randint(0, (720 // TILE) - 1) * TILE
                    state = "menu"
                if event.key == pygame.K_x:  # close game
                    running = False

    if state == "menu":
        screen.fill("black")
        title = font.render("SNAKE", True, "green")
        creator = font.render("By Awack", True, "white")
        start = font.render("ENTER = play", True, "white")
        hi = font.render(f"High Score: {highscore}", True, "yellow")
        quit_text = font.render("X = Quit Game", True, "grey")
        screen.blit(title, (550, 300))
        screen.blit(creator, (525, 650))
        screen.blit(start, (510, 400))
        screen.blit(hi, (510, 450))
        screen.blit(quit_text, (500, 500))

    elif state == "playing":
        # KeyHandling
        direction = next_direction

        new_head = pygame.Vector2(body[0])
        if direction == "up":
            new_head.y -= TILE
        if direction == "down":
            new_head.y += TILE
        if direction == "left":
            new_head.x -= TILE
        if direction == "right":
            new_head.x += TILE

        body.insert(0, new_head)

        # wall collision
        if new_head.x < 0 or new_head.x >= 1200 or new_head.y < 0 or new_head.y >= 720:
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
            # new apple
            food_x = random.randint(0, (1200 // TILE) - 1) * TILE
            food_y = random.randint(0, (720 // TILE) - 1) * TILE
        else:
            body.pop()  # normal movement

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("green")

        # grid lines
        for x in range(0, 1200, 50):
            pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, 720))
        for y in range(0, 720, 50):
            pygame.draw.line(screen, (30, 30, 30), (0, y), (1200, y))

        pygame.draw.rect(screen, "red", (food_x, food_y, TILE, TILE))

        # rendering gamefield
        for segment in body:
            pygame.draw.rect(screen, "blue", (segment.x, segment.y, TILE, TILE))

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
        screen.blit(over, (520, 280))
        screen.blit(sc, (540, 340))
        screen.blit(hi, (510, 390))
        screen.blit(restart, (380, 450))
        screen.blit(quit_text, (500, 500))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(tick)

pygame.quit()