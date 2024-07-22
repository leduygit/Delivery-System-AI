from gui import visualizer
from search_logic import main as search_logic

def main():
    search_logic.search_logic()
    visualizer.visualize()

if __name__ == '__main__':
    main()