import pygame
import sys

WIDTH = 800
HEIGHT = 600

def main():
    print("Welcome to War Simulator!")

    pygame.init()

    # Create window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("War Simulator")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((30, 30, 30))

        # Update display
        pygame.display.flip()

    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()