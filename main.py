from gui import visualizer
from search_logic import main as search_logic
from search_logic import level4 as level4


def main():
    search_logic.run_solutions_on_maps()
    level4.runner()
    visualizer.visualize()


if __name__ == "__main__":
    main()
