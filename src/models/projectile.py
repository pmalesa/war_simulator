import pygame
from pygame import Surface

from src.utils.utils import clamp


class Projectile:
    DEFAULT_DAMAGE = 10
    DEFAULT_VELOCITY = 100
    DEFAULT_SIZE = 2
    DEFAULT_COLOR = (255, 255, 255)

    def __init__(self, position: list[int], direction: list[int]):
        self.position: list[int] = position
        self.direction: list[int] = direction
        self.collision: bool = False

    def move(self):
        if not self.collision:
            return
        self.position[0] += clamp(self.direction[0] * Projectile.DEFAULT_VELOCITY)
        self.position[1] += clamp(self.direction[1] * Projectile.DEFAULT_VELOCITY)

    def draw(self, screen: Surface):
        if not isinstance(screen, Surface) or not screen:
            raise RuntimeError(
                f"Invalid type of screen object: {type(screen)} instead of pygame.Surface."
            )
        pygame.draw.circle(screen, Projectile.DEFAULT_COLOR, self.position, Projectile.DEFAULT_SIZE)
