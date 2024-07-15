import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Folders
IMAGE_FOLDER = '../Assets/Images'

# Constants
GRID_SIZE = 60
GRID_WIDTH = 10
GRID_HEIGHT = 10
SIDEBAR_WIDTH = 200
WINDOW_SIZE = (GRID_WIDTH * GRID_SIZE + SIDEBAR_WIDTH, GRID_HEIGHT * GRID_SIZE)
BUTTON_HEIGHT = 40
PLAYER_IMAGE_SIZE = (45, 60)
FRAME_DELAY = 5
STATE_DELAY = 30

# Initialize Pygame
pygame.init()
font = pygame.font.SysFont('Arial', 18)
