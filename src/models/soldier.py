class Soldier:
    MAX_HEALTH: int = 100

    def __init__(
        self,
        name: str,
        health: int = MAX_HEALTH,
        position: tuple[int, int] = (0, 0),
        color: tuple[int, int, int] = (255, 255, 255),
    ):
        self.name = name
        self.health = health
        self.position = position
        self.color = color

    def take_damage(self, damage: int) -> None:
        self.health = max(0, self.health - damage)

    def is_alive(self) -> bool:
        return self.health > 0
