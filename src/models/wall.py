import pygame
from pygame import Rect, Surface


class Wall:
    MAX_HEALTH = 1000
    COLOR = (150, 150, 150)

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> None:
        self.rect = Rect(x, y, width, height)

    def draw(self, screen: Surface) -> None:
        pygame.draw.rect(screen, Wall.COLOR, self.rect)
