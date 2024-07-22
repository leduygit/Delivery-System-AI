import pygame
from gui.config import *
import gui.config as config

class Grid:
    def __init__(self, grid_data, offset=(0, 0)):
        self.grid_data = grid_data
        self.offset = offset

    def draw(self, screen):
        screen.fill(WHITE)
        for row in range(len(self.grid_data)):
            for col in range(len(self.grid_data[row])):
                cell_value = str(self.grid_data[row][col])
                color = WHITE
                text_color = BLACK
                border_color = BLACK

                text_value = cell_value
                if cell_value[0] == 'S' or cell_value[0] == 'G':
                    if len(cell_value) == 1:
                        cell_value += '1'
                    else:
                        cell_value = f'{cell_value[0]}{int(cell_value[1]) + 1}'

                if cell_value[0] == 'S':
                    color = PLAYER_COLORS[cell_value[1]]  # Start positions
                elif cell_value[0] == 'G':
                    color = PLAYER_COLORS[cell_value[1]]  # Goals
                elif cell_value == 'F':
                    color = GRAY  # Fuel stations
                elif cell_value == '-1':
                    color = BLACK  # Obstacles

                pygame.draw.rect(screen, color, (col * config.GRID_SIZE + self.offset[0], row * config.GRID_SIZE + self.offset[1], config.GRID_SIZE, config.GRID_SIZE))
                pygame.draw.rect(screen, border_color, (col * config.GRID_SIZE + self.offset[0], row * config.GRID_SIZE + self.offset[1], config.GRID_SIZE, config.GRID_SIZE), 2)

                if text_value not in ['-1', '0']:
                    text_surface = font.render(text_value, True, text_color)
                    text_rect = text_surface.get_rect(center=(col * config.GRID_SIZE + config.GRID_SIZE // 2 + self.offset[0], row * config.GRID_SIZE + config.GRID_SIZE // 2 + self.offset[1]))
                    screen.blit(text_surface, text_rect)
