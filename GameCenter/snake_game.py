from tkinter.messagebox import askyesno
import pygame
import random
import os
import tkinter as tk
import sys


def run(player):
    pygame.init()
    pygame.mixer.init()

    width, height = 1005, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(f"Snake: Hello, {player['name']}!")

    block_size = 15

    # Colors
    green = (0, 255, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (250, 0, 0)
    yellow = (220, 220, 0)

    # Load images
    def load_image(path):
        return pygame.image.load(path) if os.path.exists(path) else None

    red_apple_img = load_image("assets/assets_snake/assets/food.png")
    green_apple_img = load_image("assets/assets_snake/assets/apple_boostsize.png")
    yellow_apple_img = load_image("assets/assets_snake/assets/apple_points.png")
    snake_image = load_image("assets/assets_snake/assets/snake.png")

    # Load sounds
    def load_sound(path):
        return pygame.mixer.Sound(path) if os.path.exists(path) else None

    background_music = load_sound("assets/assets_snake/audio/background_music.wav")
    eat_sound = load_sound("assets/assets_snake/audio/food.wav")

    class Snake:

        def __init__(self):
            self.snake_x = random.randrange(0, width, block_size)
            self.snake_y = random.randrange(100, height, block_size)

            self.snake_body = []
            self.snake_length = 5
            self.points = 0
            self.direction = "RIGHT"
            self.init_body()

        def init_body(self):

            for i in range(self.snake_length):
                self.snake_body.append(
                    [self.snake_x - i * block_size, self.snake_y]
                )

        def movement(self):

            if self.direction == "LEFT":
                self.snake_x -= block_size

            elif self.direction == "RIGHT":
                self.snake_x += block_size

            elif self.direction == "UP":
                self.snake_y -= block_size

            elif self.direction == "DOWN":
                self.snake_y += block_size

        def update(self):

            self.snake_body.append([self.snake_x, self.snake_y])

            if len(self.snake_body) > self.snake_length:
                self.snake_body.pop(0)

        def draw(self):

            for x, y in self.snake_body:

                if snake_image and [x, y] == [self.snake_x, self.snake_y]:
                    screen.blit(snake_image, (x, y))

                else:
                    pygame.draw.rect(
                        screen,
                        green,
                        (x, y, block_size, block_size)
                    )

        def is_dead(self):

            if (
                self.snake_x < 0 or
                self.snake_x >= width or
                self.snake_y < 0 or
                self.snake_y >= height
            ):
                return True

            if [self.snake_x, self.snake_y] in self.snake_body[:-1]:
                return True

            return False

        @property
        def head_rect(self):
            return pygame.Rect(
                self.snake_x,
                self.snake_y,
                block_size,
                block_size
            )

    class Food:

        def __init__(self, snake):
            self.snake = snake
            self.apples = 0

            self.spawn()

        def spawn(self):

            while True:

                self.food_x = random.randrange(
                    0,
                    width,
                    block_size
                )

                self.food_y = random.randrange(
                    100,
                    height,
                    block_size
                )

                if [self.food_x, self.food_y] not in self.snake.snake_body:
                    break

            self.apple_type = random.choices(
                ["red", "green", "yellow"],
                weights=[70, 25, 5]
            )[0]

            self.food_rect = pygame.Rect(
                self.food_x,
                self.food_y,
                block_size,
                block_size
            )

        def update(self):

            if self.snake.head_rect.colliderect(self.food_rect):

                if self.apple_type == "red":
                    self.snake.snake_length += 1
                    self.snake.points += 10

                elif self.apple_type == "green":
                    self.snake.snake_length += 2
                    self.snake.points += 20

                elif self.apple_type == "yellow":
                    self.snake.snake_length += 5
                    self.snake.points += 40

                self.apples += 1

                if eat_sound:
                    eat_sound.play()

                self.spawn()

        def draw(self):

            if self.apple_type == "red":

                if red_apple_img:
                    screen.blit(
                        red_apple_img,
                        (self.food_x, self.food_y)
                    )

                else:
                    pygame.draw.rect(
                        screen,
                        red,
                        self.food_rect
                    )

            elif self.apple_type == "green":

                if green_apple_img:
                    screen.blit(
                        green_apple_img,
                        (self.food_x, self.food_y)
                    )

                else:
                    pygame.draw.rect(
                        screen,
                        green,
                        self.food_rect
                    )

            elif self.apple_type == "yellow":

                if yellow_apple_img:
                    screen.blit(
                        yellow_apple_img,
                        (self.food_x, self.food_y)
                    )

                else:
                    pygame.draw.rect(
                        screen,
                        yellow,
                        self.food_rect
                    )

    title_font = pygame.font.SysFont("Comic Sans MS", 42)
    font = pygame.font.SysFont("Comic Sans MS", 24)

    def draw_text(text, color, x, y, custom_font=font):

        img = custom_font.render(text, True, color)
        screen.blit(img, (x, y))

    def difficulty_menu():

        easy_rect = pygame.Rect(180, 300, 180, 70)
        med_rect = pygame.Rect(410, 300, 180, 70)
        hard_rect = pygame.Rect(640, 300, 180, 70)

        while True:

            screen.fill(black)

            draw_text(
                "Избери трудност",
                white,
                width // 2 - 170,
                120,
                title_font
            )

            pygame.draw.rect(screen, (255, 215, 0), easy_rect)
            pygame.draw.rect(screen, (80, 200, 120), med_rect)
            pygame.draw.rect(screen, (60, 60, 60), hard_rect)

            draw_text("Лесно", black, 225, 320)
            draw_text("Средно", black, 450, 320)
            draw_text("Трудно", white, 690, 320)

            pygame.display.update()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    mouse_pos = pygame.mouse.get_pos()

                    if easy_rect.collidepoint(mouse_pos):
                        return 8, 3

                    elif med_rect.collidepoint(mouse_pos):
                        return 12, 2

                    elif hard_rect.collidepoint(mouse_pos):
                        return 18, 1

    def start_screen():

        screen.fill(black)

        # Title
        draw_text(
            "SNAKE",
            green,
            width // 2 - 85,
            60,
            title_font
        )

        # Instructions
        draw_text(
            "Управлявайте змията със стрелките на клавиатурата.",
            white,
            180,
            160
        )

        draw_text(
            "Играта приключва при удар в стената",
            white,
            230,
            200
        )

        draw_text(
            "или докосване на опашката.",
            white,
            310,
            235
        )

        # Apples title
        draw_text(
            "Ябълки:",
            yellow,
            430,
            310
        )

        # Red apple
        if red_apple_img:
            screen.blit(red_apple_img, (230, 355))

        draw_text(
            "Червена — 10 точки, +1 сегмент",
            red,
            270,
            360
        )

        # Green apple
        if green_apple_img:
            screen.blit(green_apple_img, (230, 395))

        draw_text(
            "Зелена — 20 точки, +2 сегмента",
            green,
            270,
            400
        )

        # Yellow apple
        if yellow_apple_img:
            screen.blit(yellow_apple_img, (230, 435))

        draw_text(
            "Златна — 40 точки, +5 сегмента",
            yellow,
            270,
            440
        )

        # Start text
        draw_text(
            "Натиснете SPACE за начало",
            white,
            width // 2 - 170,
            530
        )

        pygame.display.update()

        waiting = True

        while waiting:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    if askyesno(
                        "Exit",
                        "Do you want to quit?"
                    ):
                        pygame.quit()
                        sys.exit()

                if (
                    event.type == pygame.KEYDOWN and
                    event.key == pygame.K_SPACE
                ):
                    waiting = False

    def game_over_screen(score):

        screen.fill(black)

        draw_text(
            "GAME OVER",
            red,
            width // 2 - 120,
            height // 2 - 40,
            title_font
        )

        draw_text(
            f"Score: {score}",
            white,
            width // 2 - 70,
            height // 2 + 20
        )

        draw_text(
            "Press ESCAPE to exit",
            white,
            width // 2 - 110,
            height // 2 + 60
        )

        pygame.display.update()

        waiting = True

        while waiting:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    waiting = False

                if (
                    event.type == pygame.KEYDOWN and
                    event.key == pygame.K_ESCAPE
                ):
                    waiting = False



    snake = Snake()
    food = Food(snake)

    start_screen()
    game_speed, speed_increase = difficulty_menu()
    clock = pygame.time.Clock()

    running = True

    if background_music:
        background_music.play(-1)

    while running:

        speed = min(game_speed + food.apples // speed_increase, 35)
        clock.tick(speed)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if (
                    event.key == pygame.K_LEFT and
                    snake.direction != "RIGHT"
                ):
                    snake.direction = "LEFT"

                elif (
                    event.key == pygame.K_RIGHT and
                    snake.direction != "LEFT"
                ):
                    snake.direction = "RIGHT"

                elif (
                    event.key == pygame.K_UP and
                    snake.direction != "DOWN"
                ):
                    snake.direction = "UP"

                elif (
                    event.key == pygame.K_DOWN and
                    snake.direction != "UP"
                ):
                    snake.direction = "DOWN"

        snake.movement()

        if snake.is_dead():
            game_over_screen(snake.points)
            break

        snake.update()
        food.update()

        screen.fill(white)

        snake.draw()
        food.draw()

        draw_text(
            f"Apples: {food.apples}",
            black,
            10,
            10
        )

        draw_text(
            f"Points: {snake.points}",
            black,
            10,
            40
        )
        draw_text(f"Speed: {speed}", black, 10, 70)
        pygame.display.set_caption(
            f"Snake: {player['name']} | Score: {snake.points}"
        )

        pygame.display.flip()

    pygame.quit()

    return snake.points