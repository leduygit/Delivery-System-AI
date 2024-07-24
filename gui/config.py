import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LITE_BLACK = (0, 0, 0, 30)
GRAY = (200, 200, 200)

PLAYER_COLORS = {
    "0": (0, 255, 255),  # CYAN
    "1": (255, 0, 0),  # RED
    "2": (0, 255, 0),  # GREEN
    "3": (0, 0, 255),  # BLUE
    "4": (255, 192, 203),  # PINK
    "5": (255, 165, 0),  # ORANGE
    "6": (128, 128, 128),  # GREY
    "7": (255, 255, 255),  # WHITE
    "8": (255, 255, 0),  # YELLOW
    "9": (165, 42, 42),  # BROWN
}

# Folders
IMAGE_FOLDER = "Assets/Images"
OBSTACLE_FOLDER = "Assets/Images/Obstacles"
ROAD_FOLDER = "Assets/Images/Roads"
FLAG_FOLDER = "Assets/Images/Flags"

# Constants
MAX_WIDTH = 40
MAX_HEIGHT = 28  # 30
GRID_SIZE = 30
WINDOW_WIDTH = MAX_WIDTH * 30
WINDOW_HEIGHT = MAX_HEIGHT * 30
SIDEBAR_WIDTH = 200
WINDOW_SIZE = (WINDOW_WIDTH + SIDEBAR_WIDTH, WINDOW_HEIGHT)
BUTTON_HEIGHT = 40
PLAYER_IMAGE_SIZE = (22.5, 30)
FRAME_DELAY = 5
STATE_DELAY = 30

# Initialize Pygame
pygame.init()
font = pygame.font.SysFont("Roboto", 19)
