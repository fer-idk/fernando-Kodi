import math
import struct
import wave
from pathlib import Path

import pygame

# Usamos Pygame porque permite generar imágenes PNG y archivos WAV de forma rápida y consistente con el proyecto, sin dependencias extra.

ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / "assets"

PLAYER_SIZE = (64, 64)
ENEMY_SIZE = (64, 64)
PLATFORM_SIZE = (120, 22)

PLAYER_COLOR = (255, 214, 82)
ENEMY_COLOR = (220, 80, 80)
PLATFORM_COLOR = (120, 120, 120)
BACKGROUND = (45, 45, 45)
EYE_COLOR = (24, 24, 24)


def ensure_assets_dir():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def generate_player_sprite(path: Path):
    surface = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
    # cuerpo principal
    pygame.draw.ellipse(surface, PLAYER_COLOR, (8, 12, 48, 36))
    # cabeza
    pygame.draw.circle(surface, PLAYER_COLOR, (32, 24), 18)
    # pico / cuerpo
    pygame.draw.polygon(surface, (255, 140, 0), [(42, 30), (58, 25), (58, 35)])
    # ojos
    pygame.draw.circle(surface, EYE_COLOR, (24, 24), 3)
    pygame.draw.circle(surface, EYE_COLOR, (38, 24), 3)
    # patas
    pygame.draw.line(surface, (90, 60, 0), (24, 48), (18, 58), 3)
    pygame.draw.line(surface, (90, 60, 0), (40, 48), (46, 58), 3)
    pygame.image.save(surface, str(path))


def generate_enemy_sprite(path: Path):
    surface = pygame.Surface(ENEMY_SIZE, pygame.SRCALPHA)
    pygame.draw.rect(surface, ENEMY_COLOR, (12, 12, 40, 36), border_radius=10)
    pygame.draw.circle(surface, (255, 255, 255), (24, 27), 6)
    pygame.draw.circle(surface, EYE_COLOR, (24, 27), 3)
    pygame.draw.circle(surface, (255, 255, 255), (39, 27), 6)
    pygame.draw.circle(surface, EYE_COLOR, (39, 27), 3)
    pygame.draw.line(surface, EYE_COLOR, (20, 40), (44, 40), 3)
    pygame.draw.rect(surface, (80, 0, 0), (18, 46, 28, 8), border_radius=4)
    pygame.image.save(surface, str(path))


def generate_platform_sprite(path: Path):
    surface = pygame.Surface(PLATFORM_SIZE, pygame.SRCALPHA)
    pygame.draw.rect(surface, PLATFORM_COLOR, (0, 0, 120, 22), border_radius=4)
    pygame.draw.rect(surface, (70, 70, 70), (8, 7, 104, 8), border_radius=2)
    pygame.image.save(surface, str(path))


def generate_jump_sound(path: Path, sample_rate: int = 22050, duration: float = 0.14):
    amplitude = 32767
    frames = []
    total_samples = int(sample_rate * duration)
    start_freq = 420.0
    end_freq = 840.0

    for i in range(total_samples):
        t = i / sample_rate
        freq = start_freq + (end_freq - start_freq) * (t / duration)
        value = math.sin(2 * math.pi * freq * t)
        frame = int(value * amplitude * 0.7)
        frames.append(struct.pack("<h", frame))

    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b"".join(frames))


def generate_collision_sound(path: Path, sample_rate: int = 22050, duration: float = 0.18):
    amplitude = 32767
    frames = []
    total_samples = int(sample_rate * duration)
    start_freq = 260.0
    end_freq = 80.0

    for i in range(total_samples):
        t = i / sample_rate
        freq = start_freq + (end_freq - start_freq) * (t / duration)
        noise = math.sin(2 * math.pi * freq * t) * (1.0 - t / duration)
        value = noise * 0.8
        frame = int(value * amplitude)
        frames.append(struct.pack("<h", frame))

    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b"".join(frames))


def generate_assets():
    ensure_assets_dir()
    pygame.init()
    pygame.display.set_mode((1, 1))

    generate_player_sprite(ASSETS_DIR / "jugador.png")
    generate_enemy_sprite(ASSETS_DIR / "enemigo.png")
    generate_platform_sprite(ASSETS_DIR / "plataforma.png")
    generate_jump_sound(ASSETS_DIR / "salto.wav")
    generate_collision_sound(ASSETS_DIR / "colision.wav")

    pygame.quit()
    print("Recursos placeholder creados en:", ASSETS_DIR)
    print("Archivos generados:")
    for name in ["jugador.png", "enemigo.png", "plataforma.png", "salto.wav", "colision.wav"]:
        print(f"- {name}")


if __name__ == "__main__":
    generate_assets()
