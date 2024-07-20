# grid.py
import pygame
from config import WHITE, GRAY, BLACK, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, font

class Grid:
    def __init__(self, grid_data, offset=(0, 0)):
        self.grid_data = grid_data
        self.offset = offset

    def draw(self, screen):
        screen.fill(WHITE)
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                try:
                    cell_value = str(self.grid_data[row][col])
                except:
                    cell_value = '0'
                color = WHITE
                text_color = BLACK
                border_color = BLACK

                if cell_value[0] == 'S':
                    color = GRAY  # Start positions
                elif cell_value[0] == 'G':
                    border_color = GRAY  # Goals
                elif cell_value == 'F':
                    color = GRAY  # Fuel stations
                elif cell_value == '-1':
                    color = BLACK  # Obstacles
                elif cell_value != '0':
                    border_color = BLACK

                pygame.draw.rect(screen, color, (col * GRID_SIZE + self.offset[0], row * GRID_SIZE + self.offset[1], GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, border_color, (col * GRID_SIZE + self.offset[0], row * GRID_SIZE + self.offset[1], GRID_SIZE, GRID_SIZE), 1)

                if cell_value not in ['-1', '0']:
                    text_surface = font.render(cell_value, True, text_color)
                    text_rect = text_surface.get_rect(center=(col * GRID_SIZE + GRID_SIZE // 2 + self.offset[0], row * GRID_SIZE + GRID_SIZE // 2 + self.offset[1]))
                    screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, BLACK, (self.offset[0], self.offset[1], GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE), 3)
