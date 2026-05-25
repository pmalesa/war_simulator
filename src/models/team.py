from enum import Enum


class Team(Enum):
    RED = 1
    GREEN = 2


TEAM_COLORS = {Team.RED: (255, 0, 0), Team.GREEN: (0, 255, 0)}
