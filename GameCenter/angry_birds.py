import math
import pygame
import os
import random
import tkinter as tk
from tkinter import messagebox


def run(player):
    pygame.init()
    pygame.mixer.init()
    width = 1000
    height = 600
    points = 0
    dir = "assets/assets_angry_birds"

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Angry Birds: " + f"Hello, {player['name']}! Your score is {player['score_angry_birds']}")
    icon = pygame.image.load(f"{dir}/angry-birds.png")
    pygame.display.set_icon(icon)

    background_surface = pygame.image.load(f'{dir}/background.png').convert()

    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    black = (0, 0, 0)

    font = pygame.font.SysFont(None, 32)

    if os.path.exists(f"{dir}/hit.wav"):
        hit_sound = pygame.mixer.Sound(f"{dir}/hit.wav")
    else:
        hit_sound = None

    # ──────────────────────────────────────────────
    # LEVEL DEFINITIONS
    # Each level: (pig_count, pig_health, pig_size, points_per_kill, label)
    # ──────────────────────────────────────────────
    # Формат: (брой прасета, [здраве за всяко], [размер за всяко], точки на убийство, надпис)
    # Здравето расте и с нивото, и с трудността
    LEVEL_TEMPLATES = {
        "easy": [
            (1, [1],          [(80, 80)],                                        20, "Ниво 1"),
            (2, [1, 2],       [(80, 80), (65, 65)],                              20, "Ниво 2"),
            (3, [1, 2, 2],    [(80, 80), (65, 65), (60, 60)],                    20, "Ниво 3"),
            (4, [1, 2, 2, 2], [(75, 75), (65, 65), (60, 60), (55, 55)],          20, "Ниво 4"),
            (4, [2, 2, 2, 2], [(75, 75), (65, 65), (60, 60), (55, 55)],          25, "Ниво 5"),
        ],
        "medium": [
            (2, [2, 2],              [(70, 70), (60, 60)],                                       25, "Ниво 1"),
            (3, [2, 2, 3],           [(70, 70), (60, 60), (55, 55)],                             25, "Ниво 2"),
            (4, [2, 2, 3, 3],        [(65, 65), (60, 60), (55, 55), (50, 50)],                   25, "Ниво 3"),
            (5, [2, 2, 3, 3, 3],     [(65, 65), (60, 60), (55, 55), (50, 50), (45, 45)],         25, "Ниво 4"),
            (5, [3, 3, 3, 3, 3],     [(70, 70), (65, 65), (60, 60), (55, 55), (50, 50)],         30, "Ниво 5"),
        ],
        "hard": [
            (3, [3, 3, 3],           [(65, 65), (55, 55), (45, 45)],                                       25, "Ниво 1"),
            (4, [3, 3, 3, 4],        [(65, 65), (60, 60), (50, 50), (45, 45)],                             25, "Ниво 2"),
            (5, [3, 3, 3, 4, 4],     [(65, 65), (60, 60), (55, 55), (50, 50), (42, 42)],                   25, "Ниво 3"),
            (6, [3, 3, 3, 4, 4, 4],  [(65, 65), (60, 60), (55, 55), (50, 50), (45, 45), (40, 40)],         30, "Ниво 4"),
            (6, [4, 4, 4, 4, 4, 4],  [(70, 70), (65, 65), (60, 60), (55, 55), (50, 50), (45, 45)],         35, "Ниво 5"),
        ],
    }

    # ──────────────────────────────────────────────
    # CLASSES
    # ──────────────────────────────────────────────
    class Bird:
        def __init__(self, slingshot_pos):
            self.slingshot_x = slingshot_pos[0]
            self.slingshot_y = slingshot_pos[1]
            self.bird_pos = slingshot_pos.copy()
            self.bird_velocity = [0, 0]
            self.bird_radius = 32
            self.gravity = 0.5
            self.load_random_image()
            self.launched = False
            self.dragging = False
            self.launcher_timer = 0
            self.rect = None

        def load_random_image(self):
            files = [
                f"{dir}/angry-birds.png", f"{dir}/angry-birds-1.png",
                f"{dir}/angry-birds-2.png", f"{dir}/angry-birds-3.png",
                f"{dir}/angry-birds-4.png"
            ]
            filesname = random.choice(files)
            self.image = pygame.image.load(filesname)
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.rect = self.image.get_rect()

        def draw(self):
            if self.image:
                screen.blit(self.image, (
                    self.bird_pos[0] - self.bird_radius,
                    self.bird_pos[1] - self.bird_radius
                ))
            else:
                pygame.draw.circle(screen, red, self.bird_pos, self.bird_radius)

        def reset(self):
            self.bird_pos = [self.slingshot_x, self.slingshot_y]
            self.bird_velocity = [0, 0]
            self.launched = False
            self.dragging = False
            self.launcher_timer = 0
            self.load_random_image()

    class Target:
        def __init__(self, x, y, w=40, h=40, health=3):
            self.rect = pygame.Rect(x, y, w, h)
            self.max_health = health
            self.health = health
            self.alive = True
            self.w = w
            self.h = h
            self._load_image()

        def _load_image(self):
            # Избира изображение спрямо % здраве (работи за здраве 1-4)
            ratio = self.health / self.max_health if self.max_health > 0 else 0
            if ratio > 0.66:
                path = f"{dir}/piggy.png"
            elif ratio > 0.33:
                path = f"{dir}/pig2.png"
            else:
                path = f"{dir}/pig3.png"
            img = pygame.image.load(path)
            self.img = pygame.transform.scale(img, (self.w, self.h))

        def hit(self):
            self.health -= 1
            if self.health <= 0:
                self.alive = False
            else:
                self._load_image()
            if hit_sound:
                hit_sound.play()

        def draw(self, screen):
            if not self.alive:
                return
            screen.blit(self.img, (self.rect.x, self.rect.y))

    # ──────────────────────────────────────────────
    # HELPER: spawn a group of non-overlapping targets
    # ──────────────────────────────────────────────
    def spawn_targets(count, healths, sizes):
        targets = []
        attempts = 0
        while len(targets) < count and attempts < 500:
            attempts += 1
            idx = len(targets)
            w, h = sizes[idx] if idx < len(sizes) else sizes[-1]
            hp = healths[idx] if idx < len(healths) else healths[-1]
            x = random.randint(400, width - w - 10)
            y = random.randint(50, height - h - 10)
            new_rect = pygame.Rect(x, y, w, h)
            overlap = any(new_rect.colliderect(t.rect.inflate(10, 10)) for t in targets)
            if not overlap:
                targets.append(Target(x, y, w, h, hp))
        return targets


    # ──────────────────────────────────────────────
    # SCREENS
    # ──────────────────────────────────────────────
    def difficulty_menu():
        easy_rect = pygame.Rect(200, 300, 180, 70)
        med_rect = pygame.Rect(410, 300, 180, 70)
        hard_rect = pygame.Rect(620, 300, 180, 70)

        while True:
            screen.fill((30, 30, 30))
            title = font.render("Choose Difficulty", True, white)
            screen.blit(title, (width // 2 - 120, 150))

            pygame.draw.rect(screen, (255, 215, 0), easy_rect)
            pygame.draw.rect(screen, (80, 200, 120), med_rect)
            pygame.draw.rect(screen, (60, 60, 60), hard_rect)

            screen.blit(font.render("EASY", True, black), (easy_rect.x + 50, easy_rect.y + 20))
            screen.blit(font.render("MEDIUM", True, black), (med_rect.x + 35, med_rect.y + 20))
            screen.blit(font.render("HARD", True, white), (hard_rect.x + 45, hard_rect.y + 20))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "easy"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if easy_rect.collidepoint(mx, my):
                        return "easy"
                    elif med_rect.collidepoint(mx, my):
                        return "medium"
                    elif hard_rect.collidepoint(mx, my):
                        return "hard"

    def start_screen():
        title_font = pygame.font.SysFont(None, 50)
        small_font = pygame.font.SysFont(None, 30)
        waiting = True
        while waiting:
            screen.fill(black)
            screen.blit(title_font.render("ANGRY BIRDS", True, red), (width // 2 - 120, 60))
            lines = [
                "Използвайте мишката, за да опънете прашката.",
                "Освободете бутона, за да изстреляте птицата.",
                "Целта е да уцелите прасетата с възможно най-малко изстрели.",
                "Убийте всички прасета, за да минете на следващото ниво.",
            ]
            for i, line in enumerate(lines):
                screen.blit(small_font.render(line, True, white), (80, 180 + i * 40))
            screen.blit(small_font.render("Натисни SPACE за старт", True, green), (width // 2 - 130, 420))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False

    def level_intro_screen(label, level_num, total_levels):
        overlay_font = pygame.font.SysFont(None, 56)
        sub_font = pygame.font.SysFont(None, 32)
        for alpha in range(0, 256, 8):
            screen.blit(background_surface, (0, 0))
            surf = pygame.Surface((width, height), pygame.SRCALPHA)
            surf.fill((0, 0, 0, min(alpha, 160)))
            screen.blit(surf, (0, 0))
            t1 = overlay_font.render(label, True, (255, 220, 50))
            t2 = sub_font.render(f"Ниво {level_num} от {total_levels}", True, white)
            t3 = sub_font.render("Натисни SPACE за старт", True, (150, 255, 150))
            screen.blit(t1, (width // 2 - t1.get_width() // 2, height // 2 - 60))
            screen.blit(t2, (width // 2 - t2.get_width() // 2, height // 2))
            screen.blit(t3, (width // 2 - t3.get_width() // 2, height // 2 + 50))
            pygame.display.update()
            pygame.time.delay(15)

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False

    def game_over_screen(score, won=False):
        title_font = pygame.font.SysFont(None, 60)
        sub_font = pygame.font.SysFont(None, 32)
        screen.fill(black)
        if won:
            msg = "ПОБЕДА!"
            color = (255, 220, 50)
        else:
            msg = "GAME OVER"
            color = red
        screen.blit(title_font.render(msg, True, color), (width // 2 - 120, height // 2 - 60))
        screen.blit(sub_font.render(f"Точки: {score}", True, white), (width // 2 - 70, height // 2 + 10))
        screen.blit(sub_font.render("Натисни ESCAPE за изход", True, white), (width // 2 - 130, height // 2 + 55))
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    waiting = False

    # ──────────────────────────────────────────────
    # MAIN FLOW
    # ──────────────────────────────────────────────
    start_screen()
    difficulty = difficulty_menu()
    levels = LEVEL_TEMPLATES[difficulty]
    total_levels = len(levels)

    shots_fired = 0
    hits = 0
    clock = pygame.time.Clock()

    slingshot_pos = [150, height - 150]

    for level_index, (pig_count, pig_healths, pig_sizes, pts_per_kill, label) in enumerate(levels):
        level_intro_screen(label, level_index + 1, total_levels)

        targets = spawn_targets(pig_count, pig_healths, pig_sizes)
        bird = Bird(slingshot_pos)

        running = True
        while running:
            dt = clock.tick(60)
            screen.blit(background_surface, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    answer = messagebox.askyesno("Изход", "Искаш ли да излезеш?")
                    if answer:
                        pygame.quit()
                        return points

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not bird.launched:
                        mx, my = pygame.mouse.get_pos()
                        dist = math.hypot(mx - bird.bird_pos[0], my - bird.bird_pos[1])
                        if dist <= bird.bird_radius:
                            bird.dragging = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    if bird.dragging:
                        bird.dragging = False
                        bird.launched = True
                        shots_fired += 1
                        mx, my = pygame.mouse.get_pos()
                        dx = bird.slingshot_x - mx
                        dy = bird.slingshot_y - my
                        bird.bird_velocity = [dx * 0.2, dy * 0.2]

            # Bird physics
            if bird.dragging:
                mx, my = pygame.mouse.get_pos()
                bird.bird_pos[0] = mx
                bird.bird_pos[1] = my
            elif bird.launched:
                bird.bird_velocity[1] += bird.gravity
                bird.bird_pos[0] += bird.bird_velocity[0]
                bird.bird_pos[1] += bird.bird_velocity[1]
                bird.launcher_timer += dt
                if bird.bird_pos[0] > width or bird.bird_pos[1] > height:
                    bird.reset()

            # Collision with targets
            if bird.launched:
                bird.rect = pygame.Rect(
                    bird.bird_pos[0] - bird.bird_radius,
                    bird.bird_pos[1] - bird.bird_radius,
                    bird.bird_radius * 2,
                    bird.bird_radius * 2
                )
                for t in targets:
                    if t.alive and bird.rect.colliderect(t.rect):
                        t.hit()
                        hits += 1
                        if not t.alive:
                            points += pts_per_kill
                        bird.reset()
                        break

            # Draw
            for t in targets:
                t.draw(screen)
            bird.draw()
            pygame.draw.line(screen, black, (bird.slingshot_x, bird.slingshot_y),
                             (int(bird.bird_pos[0]), int(bird.bird_pos[1])), 2)
            pygame.draw.circle(screen, black, (bird.slingshot_x, bird.slingshot_y), 5)

            # HUD
            screen.blit(font.render(f"Изстрели: {shots_fired}", True, black), (10, 10))
            screen.blit(font.render(f"Удари: {hits}", True, black), (10, 40))
            screen.blit(font.render(f"Точки: {points}", True, black), (10, 70))
            alive_count = sum(1 for t in targets if t.alive)
            screen.blit(font.render(f"Прасета: {alive_count}", True, black), (10, 100))
            screen.blit(font.render(f"Ниво: {level_index + 1}/{total_levels}", True, black), (10, 130))

            pygame.display.set_caption(f"Angry Birds — {player['name']} | Точки: {points}")
            pygame.display.update()

            # Check level complete
            if all(not t.alive for t in targets):
                running = False  # advance to next level

    game_over_screen(points, won=True)
    pygame.quit()
    return points