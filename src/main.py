from src.scenes.scene import Scene


def main():
    print("Welcome to War Simulator!")
    scene: Scene = Scene(1600, 1200)
    scene.run()


if __name__ == "__main__":
    main()
