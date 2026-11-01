import random
from dataclasses import dataclass

import pygame

# -----------------------------
# Configuración del juego
# -----------------------------
WIDTH, HEIGHT = 960, 640
FPS = 60
ROAD_TOP = 90
ROAD_BOTTOM = HEIGHT - 90
GOAL_Y = 30
PLAYER_SIZE = 34
PLAYER_START = (60, HEIGHT - 120)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (76, 175, 80)
GRASS = (34, 139, 34)
ROAD = (50, 50, 50)
LINE = (255, 255, 255)
GOAL = (255, 230, 120)
YELLOW = (255, 220, 80)
LIMON = (224, 255, 116)
RED = (220, 60, 60)
BLUE = (75, 130, 255)


@dataclass
class Level:
    name: str
    lane_y: list[int]
    car_count: int
    min_speed: float
    max_speed: float


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.x = self.x
        self.rect.y = self.y

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        pygame.draw.ellipse(screen, YELLOW, self.rect)
        pygame.draw.rect(screen, BLACK, (self.x + 8, self.y + 10, 18, 8), 0)
        pygame.draw.circle(screen, BLACK, (self.x + 10, self.y + 10), 3)
        pygame.draw.circle(screen, BLACK, (self.x + 24, self.y + 10), 3)
        pygame.draw.line(screen, BLACK, (self.x + 18, self.y + 7), (self.x + 30, self.y + 2), 2)


class Car:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        self.x += self.speed
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        pygame.draw.rect(screen, BLUE, (self.x + 10, self.y + 5, self.width - 20, self.height - 10))

    def recycle(self, direction):
        if direction > 0 and self.x > WIDTH + 200:
            self.x = -self.width - random.randint(40, 180)
            self.rect.x = self.x
        elif direction < 0 and self.x < -self.width - 200:
            self.x = WIDTH + random.randint(40, 180)
            self.rect.x = self.x


def build_levels():
    return [
        Level("Nivel 1: Primer intento", [150, 220, 290], 5, 2.2, 4.0),
        Level("Nivel 2: Calle más exigente", [130, 200, 270, 340], 7, 3.3, 5.5),
    ]


def create_cars_for_level(level):
    cars = []
    used_positions = {lane: [] for lane in level.lane_y}

    for index in range(level.car_count):
        lane_index = index % len(level.lane_y)
        lane_y = level.lane_y[lane_index]
        direction = 1 if lane_index % 2 == 0 else -1
        width = 80 if index % 2 == 0 else 68
        height = 28
        speed = random.uniform(level.min_speed, level.max_speed) * direction

        if direction > 0:
            x = -random.randint(80, 240) - index * 25
        else:
            x = WIDTH + random.randint(80, 240) + index * 26

        car = Car(x, lane_y, width, height, speed)
        cars.append(car)
        used_positions[lane_y].append(car)

    return cars


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("La gallina cruzando la calle")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.levels = build_levels()
        self.current_level_index = 0
        self.player = Player(*PLAYER_START)
        self.cars = []
        self.running = True
        self.game_state = "playing"
        self.load_level(self.current_level_index)

    def load_level(self, level_index):
        level = self.levels[level_index]
        self.current_level_index = level_index
        self.cars = create_cars_for_level(level)
        self.player.reset(*PLAYER_START)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_state = "quit"

    def handle_player_movement(self):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.player.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.player.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.player.speed

        self.player.move(dx, dy)
        self.player.x = max(0, min(self.player.x, WIDTH - self.player.width))
        self.player.y = max(ROAD_TOP, min(self.player.y, HEIGHT - self.player.height - ROAD_TOP))

    def update_cars(self):
        for car in self.cars:
            car.update()
            car.recycle(car.speed)

    def check_collisions(self):
        for car in self.cars:
            if self.player.rect.colliderect(car.rect):
                self.player.reset(*PLAYER_START)
                break

    def check_win_condition(self):
        if self.player.y < GOAL_Y + 20:
            if self.current_level_index < len(self.levels) - 1:
                self.current_level_index += 1
                self.load_level(self.current_level_index)
            else:
                self.game_state = "won"
                self.running = False

    def draw_background(self):
        self.screen.fill(BLACK)

        # Suelo
        pygame.draw.rect(self.screen, GRASS, (0, 0, WIDTH, ROAD_TOP))
        pygame.draw.rect(self.screen, GRASS, (0, ROAD_BOTTOM, WIDTH, ROAD_TOP))
        pygame.draw.rect(self.screen, ROAD, (0, ROAD_TOP, WIDTH, ROAD_BOTTOM - ROAD_TOP))

        # Línea de meta
        pygame.draw.rect(self.screen, GOAL, (0, GOAL_Y, WIDTH, 18))

        # Líneas separadoras del carril
        for y in range(ROAD_TOP, ROAD_BOTTOM, 60):
            pygame.draw.rect(self.screen, LINE, (0, y + 28, WIDTH, 4))

        # Bordes de carretera
        pygame.draw.rect(self.screen, WHITE, (0, ROAD_TOP, WIDTH, 3))
        pygame.draw.rect(self.screen, WHITE, (0, ROAD_BOTTOM - 3, WIDTH, 3))

    def draw_ui(self):
        level_name = self.levels[self.current_level_index].name
        font = pygame.font.SysFont("arial", 24)
        label = font.render(level_name, True, WHITE)
        self.screen.blit(label, (20, 18))

    def draw(self):
        self.draw_background()
        for car in self.cars:
            car.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_ui()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()

            if self.game_state == "playing":
                self.handle_player_movement()
                self.update_cars()
                self.check_collisions()
                self.check_win_condition()
                self.draw()

        self.show_end_screen()
        pygame.quit()

    def show_end_screen(self):
        self.screen.fill(BLACK)
        font_large = pygame.font.SysFont("arial", 44)
        font_small = pygame.font.SysFont("arial", 26)

        if self.game_state == "won":
            text = font_large.render("¡Ganaste!", True, LIMON)
            subtitle = font_small.render("La gallina cruzó la calle con éxito.", True, WHITE)
        else:
            text = font_large.render("Juego cerrado", True, WHITE)
            subtitle = font_small.render("Gracias por jugar.", True, WHITE)

        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 40))
        self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.flip()
        pygame.time.delay(2000)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
