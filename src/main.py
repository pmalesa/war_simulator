from src.models.soldier import Soldier
from src.scenes.scene import Scene


def main():
    print("Welcome to War Simulator!")
    soldiers = [
        Soldier(1, "A", 100, [200, 300], 1),
        Soldier(2, "B", 100, [400, 300], 1),
        Soldier(3, "C", 100, [500, 300], 2),
        Soldier(4, "D", 100, [500, 400], 2),
    ]
    scene: Scene = Scene(1200, 1024, soldiers)
    scene.run()


if __name__ == "__main__":
    main()
