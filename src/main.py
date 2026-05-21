from src.models.soldier import Soldier
from src.scenes.scene import Scene


def main():
    print("Welcome to War Simulator!")
    soldiers = [
        Soldier(1, "A", 100, [5, 5], [200, 300], 1),
        Soldier(2, "B", 100, [5, 5], [400, 300], 1),
        Soldier(3, "C", 100, [5, 5], [500, 300], 1),
        Soldier(4, "D", 100, [5, 5], [500, 400], 1),
        Soldier(5, "E", 100, [5, 5], [600, 400], 2),
        Soldier(6, "F", 100, [5, 5], [700, 400], 2),
        Soldier(7, "G", 100, [5, 5], [500, 600], 2),
        Soldier(8, "H", 100, [5, 5], [500, 700], 2),
    ]
    scene: Scene = Scene(1200, 1024, soldiers)
    scene.run()


if __name__ == "__main__":
    main()
