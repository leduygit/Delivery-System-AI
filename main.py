from gui import visualizer
from search_logic import main as search_logic

def main():
    search_logic.run_solutions_on_maps()
    visualizer.visualize()

if __name__ == '__main__':
    main()