from gui import visualizer
from search_logic import main as search_logic
from search_logic import level4 as level4


def main():
    # search_logic.run_solutions_on_maps()
    for i in range(1, 4):
        print(f"Running level 4 on map{i}.txt...")
        level4.runner(f"Assets/Maps/lv4/map{i}.txt")
    visualizer.visualize()


if __name__ == "__main__":
    main()
