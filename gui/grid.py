import pygame
from config import WHITE, GRAY, BLACK, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, font

class Grid:
    def __init__(self, grid_data):
        self.grid_data = grid_data

    def draw(self, screen):
        screen.fill(WHITE)
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                cell_value = self.grid_data[row][col]
                color = WHITE
                text_color = BLACK
                border_color = BLACK

                if cell_value[0] == 'S':
                    color = GRAY  # Start position
                elif cell_value[0] == 'G':
                    border_color = GRAY  # Goals
                elif cell_value == 'F':
                    color = GRAY  # Fuel stations
                elif cell_value == '-1':
                    color = BLACK  # Obstacle
                elif cell_value != '0':
                    border_color = BLACK  

                pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, border_color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

                if cell_value not in ['-1', '0']:
                    text_surface = font.render(cell_value, True, text_color)
                    text_rect = text_surface.get_rect(center=(col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))
                    screen.blit(text_surface, text_rect)
