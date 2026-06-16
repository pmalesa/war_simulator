import math

import pygame
from pygame import Surface

from src.models.team import Team
from src.utils.utils import clamp


class Projectile:
    DEFAULT_DAMAGE = 10
    DEFAULT_STEP = 100
    DEFAULT_SIZE = 2
    DEFAULT_COLOR = (255, 255, 255)

    def __init__(self, position: list[int], angle: float, team: Team):
        self.position: list[int] = position
        self.angle: float = angle
        self.team: Team = team
        self.collision: bool = False
        self.step = self.DEFAULT_STEP

        angle_rad: float = math.radians(self.angle)
        self.velocity: list[float] = [
            math.cos(angle_rad) * self.step,
            math.sin(angle_rad) * self.step,
        ]

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
