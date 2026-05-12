class Soldier:
    MAX_HEALTH: int = 100
    DEFAULT_STEP: int = 1
    DEFAULT_SIZE: int = 10

    def __init__(
        self,
        name: str,
        health: int = MAX_HEALTH,
        position: tuple[int, int] = (0, 0),
        team: int = 1,
        size: int = DEFAULT_SIZE,
    ):
        self.name = name
        self.health = health
        self.position = position
        self.color = None
        self.team = team
        self.size = size

        if self.team == 1:
            self.color: tuple[int, int, int] = (255, 0, 0)
        else:
            self.color: tuple[int, int, int] = (0, 255, 0)

    def take_damage(self, damage: int) -> None:
        self.health = max(0, self.health - damage)

    def is_alive(self) -> bool:
        return self.health > 0

    def move(self, direction: tuple[int, int] = (0, 0)):
        if not direction:
            return
        self.position[0] += direction[0]
        self.position[1] += direction[1]

    def draw(self):
        pass
