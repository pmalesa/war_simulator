import pygame
from pygame import Surface


class Soldier:
    MAX_HEALTH: int = 100
    DEFAULT_STEP: int = 1
    DEFAULT_SIZE: int = 10
    DEFAULT_AWARENESS_RADIUS = 100
    DEFAULT_FIELD_OF_VIEW_ANGLE = 30

    def __init__(
        self,
        name: str,
        health: int = MAX_HEALTH,
        position: list[int] = [0, 0],
        team: int = 1,
        size: int = DEFAULT_SIZE,
        step: int = DEFAULT_STEP,
        awareness_radius: int = DEFAULT_AWARENESS_RADIUS,
        field_of_view_angle: int = DEFAULT_FIELD_OF_VIEW_ANGLE,
    ):
        self.name = name
        self.health = health

        self.position = position
        self.face_direction: list[int] = [0, 0]

        self.color = None
        self.team = team

        self.size = size
        self.step = step

        self.awareness_radius = awareness_radius
        self.field_of_view_angle = field_of_view_angle

        if self.team == 1:
            self.color: tuple[int, int, int] = (255, 0, 0)
        else:
            self.color: tuple[int, int, int] = (0, 255, 0)

    def shoot(self):
        pass

    def take_damage(self, damage: int) -> None:
        self.health = max(0, self.health - damage)

    def is_alive(self) -> bool:
        return self.health > 0

    def move(self, direction: list[int] = [0, 0]):
        if not direction:
            return
        self.position[0] += direction[0]
        self.position[1] += direction[1]

    def draw(self, screen: Surface):
        if not isinstance(screen, Surface) or not screen:
            raise RuntimeError(
                f"Invalid type of screen object: {type(screen)} instead of pygame.Surface."
            )
        pygame.draw.circle(screen, self.color, self.position, self.size)
