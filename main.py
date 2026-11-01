import random
from dataclasses import dataclass
from pathlib import Path

import pygame

# -----------------------------
# Configuración del juego
# -----------------------------
WIDTH, HEIGHT = 960, 640
FPS = 60
ROAD_TOP = 90
ROAD_BOTTOM = HEIGHT - 90
GOAL_Y = 30
PLAYER_SIZE = (36, 36)
PLAYER_START = (60, HEIGHT - 120)
ASSETS_DIR = Path(__file__).resolve().parent / "assets"

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


def load_image(path: Path, size):
    if path.exists():
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(image, size)

    surface = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.ellipse(surface, YELLOW, (8, 8, size[0] - 16, size[1] - 12))
    pygame.draw.circle(surface, BLACK, (size[0] // 3, size[1] // 2 - 2), 4)
    pygame.draw.circle(surface, BLACK, (size[0] * 2 // 3, size[1] // 2 - 2), 4)
    pygame.draw.line(surface, BLACK, (size[0] // 2, size[1] // 2 - 6), (size[0] - 8, size[1] // 3), 2)
    return surface


def load_sound(path: Path):
    if not path.exists():
        return None
    try:
        return pygame.mixer.Sound(str(path))
    except pygame.error:
        return None


class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.jump_cooldown = 0
        self.invulnerable = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def jump(self):
        if self.jump_cooldown <= 0:
            self.rect.y -= 26
            self.jump_cooldown = 18

    def update(self):
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        if self.invulnerable > 0:
            self.invulnerable -= 1

    def draw(self, screen):
        if self.invulnerable > 0 and (pygame.time.get_ticks() // 90) % 2 == 0:
            return
        screen.blit(self.image, self.rect)


class Car:
    def __init__(self, x, y, image, speed):
        self.image = image
        self.speed = speed
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def recycle(self):
        if self.speed > 0 and self.rect.x > WIDTH + 120:
            self.rect.x = -self.rect.width - random.randint(40, 180)
        elif self.speed < 0 and self.rect.x < -self.rect.width - 120:
            self.rect.x = WIDTH + random.randint(40, 180)


def build_levels():
    return [
        Level("Nivel 1: Primer intento", [150, 220, 290], 5, 2.2, 4.0),
        Level("Nivel 2: Calle más exigente", [130, 200, 270, 340], 7, 3.3, 5.5),
        Level("Nivel 3: Cruce extremo", [120, 180, 240, 300, 360], 9, 4.2, 6.8),
    ]


def create_cars_for_level(level, enemy_image):
    cars = []
    for index in range(level.car_count):
        lane_index = index % len(level.lane_y)
        y = level.lane_y[lane_index]
        direction = 1 if lane_index % 2 == 0 else -1
        size = (88, 32)
        image = pygame.transform.smoothscale(enemy_image, size)
        speed = random.uniform(level.min_speed, level.max_speed) * direction

        if direction > 0:
            x = -random.randint(80, 240) - index * 25
        else:
            x = WIDTH + random.randint(80, 240) + index * 26

        cars.append(Car(x, y, image, speed))
    return cars


class Game:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pygame.mixer = None

        pygame.display.set_caption("La gallina cruzando la calle")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.player_image = load_image(ASSETS_DIR / "jugador.png", PLAYER_SIZE)
        self.enemy_image = load_image(ASSETS_DIR / "enemigo.png", (88, 32))
        self.jump_sound = load_sound(ASSETS_DIR / "salto.wav")
        self.collision_sound = load_sound(ASSETS_DIR / "colision.wav")

        self.levels = build_levels()
        self.current_level_index = 0
        self.player = Player(60, HEIGHT - 120, self.player_image)
        self.cars = []
        self.running = True
        self.state = "menu"
        self.lives = 3
        self.score = 0
        self.load_level(self.current_level_index)

    def load_level(self, level_index):
        self.current_level_index = level_index
        level = self.levels[level_index]
        self.cars = create_cars_for_level(level, self.enemy_image)
        self.player.reset(60, HEIGHT - 120)
        self.player.invulnerable = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.state = "quit"

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

        if keys[pygame.K_SPACE]:
            self.player.jump()
            if self.jump_sound is not None:
                self.jump_sound.play()

        self.player.move(dx, dy)
        self.player.rect.x = max(0, min(self.player.rect.x, WIDTH - self.player.rect.width))
        self.player.rect.y = max(0, min(self.player.rect.y, HEIGHT - self.player.rect.height))

        self.player.update()

    def update_cars(self):
        for car in self.cars:
            car.update()
            car.recycle()

    def check_collisions(self):
        for car in self.cars:
            if self.player.rect.colliderect(car.rect):
                if self.player.invulnerable > 0:
                    continue
                self.player.invulnerable = 90
                self.lives -= 1
                self.score = max(0, self.score - 25)
                if self.collision_sound is not None:
                    self.collision_sound.play()
                self.player.reset(60, HEIGHT - 120)

                if self.lives <= 0:
                    self.state = "game_over"
                    self.running = False
                break

    def check_win_condition(self):
        if self.player.rect.y < GOAL_Y + 20:
            self.score += 100 * (self.current_level_index + 1)
            if self.current_level_index < len(self.levels) - 1:
                self.current_level_index += 1
                self.load_level(self.current_level_index)
            else:
                self.state = "won"
                self.running = False

    def draw_background(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, GRASS, (0, 0, WIDTH, ROAD_TOP))
        pygame.draw.rect(self.screen, GRASS, (0, ROAD_BOTTOM, WIDTH, ROAD_TOP))
        pygame.draw.rect(self.screen, ROAD, (0, ROAD_TOP, WIDTH, ROAD_BOTTOM - ROAD_TOP))
        pygame.draw.rect(self.screen, GOAL, (0, GOAL_Y, WIDTH, 18))

        for y in range(ROAD_TOP, ROAD_BOTTOM, 60):
            pygame.draw.rect(self.screen, LINE, (0, y + 28, WIDTH, 4))

        pygame.draw.rect(self.screen, WHITE, (0, ROAD_TOP, WIDTH, 3))
        pygame.draw.rect(self.screen, WHITE, (0, ROAD_BOTTOM - 3, WIDTH, 3))

    def draw_ui(self):
        level_name = self.levels[self.current_level_index].name
        font = pygame.font.SysFont("arial", 24)
        text = font.render(f"{level_name} | Vidas: {self.lives} | Puntuación: {self.score}", True, WHITE)
        self.screen.blit(text, (20, 18))

    def draw(self):
        self.draw_background()
        for car in self.cars:
            car.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_ui()
        pygame.display.flip()

    def show_start_screen(self):
        self.screen.fill(BLACK)
        title_font = pygame.font.SysFont("arial", 52)
        text_font = pygame.font.SysFont("arial", 28)

        title = title_font.render("La gallina cruzando", True, LIMON)
        subtitle = text_font.render("Pulsa ENTER para comenzar", True, WHITE)
        controls = text_font.render("Mover: flechas o WASD | Saltar: ESPACIO", True, WHITE)

        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
        self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 220))
        self.screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, 270))
        pygame.display.flip()

        while self.state == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = "quit"
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.state = "playing"
                    return
            pygame.time.delay(20)

    def show_end_screen(self):
        self.screen.fill(BLACK)
        large = pygame.font.SysFont("arial", 48)
        small = pygame.font.SysFont("arial", 28)

        if self.state == "won":
            text = large.render("¡Has ganado!", True, LIMON)
            detail = small.render(f"Puntuación final: {self.score}", True, WHITE)
        else:
            text = large.render("Juego terminado", True, RED)
            detail = small.render(f"Puntuación final: {self.score}", True, WHITE)

        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
        self.screen.blit(detail, (WIDTH // 2 - detail.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.flip()
        pygame.time.delay(2100)

    def run(self):
        self.show_start_screen()
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()

            if self.state == "playing":
                self.handle_player_movement()
                self.update_cars()
                self.check_collisions()
                self.check_win_condition()
                self.draw()

        self.show_end_screen()
        pygame.quit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
