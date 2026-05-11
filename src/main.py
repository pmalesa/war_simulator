import random
import sys

import pygame

from src.models.soldier import Soldier

WIDTH = 800
HEIGHT = 600


def clamp(x: int, max_val: int):
    return min(max(0, x), max_val)


def move_randomly(soldier: Soldier):
    val_x: int = random.randint(-1, 1)
    val_y: int = random.randint(-1, 1)
    new_x: int = soldier.position[0] + val_x
    new_y: int = soldier.position[1] + val_y
    soldier.position = (clamp(new_x, WIDTH), clamp(new_y, HEIGHT))


def main():
    print("Welcome to War Simulator!")

    pygame.init()

    # Create window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("War Simulator")

    soldiers = [
        Soldier("A", 100, (200, 300), (255, 0, 0)),
        Soldier("B", 100, (400, 300), (0, 255, 0)),
        Soldier("C", 100, (500, 300), (0, 0, 255)),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Background color
        screen.fill((30, 30, 30))

        # Draw soldiers
        for soldier in soldiers:
            move_randomly(soldier)
            pygame.draw.circle(screen, soldier.color, soldier.position, 10)

        # Update display
        pygame.display.flip()

    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
