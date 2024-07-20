# sidebar.py
import pygame
from datetime import datetime
from config import GRAY, BLACK, SIDEBAR_WIDTH, GRID_WIDTH, GRID_HEIGHT, font, GRID_SIZE

class Sidebar:
    def __init__(self, buttons, player_images, offset=(0, 0)):
        self.buttons = buttons
        self.player_images = player_images
        self.offset = offset

    def draw(self, screen, players, currentstate):
        sidebar_bg_color = GRAY
        pygame.draw.rect(screen, sidebar_bg_color, (GRID_WIDTH * GRID_SIZE + self.offset[0], self.offset[1], SIDEBAR_WIDTH, GRID_HEIGHT * GRID_SIZE))
        pygame.draw.rect(screen, BLACK, (GRID_WIDTH * GRID_SIZE + self.offset[0], self.offset[1], SIDEBAR_WIDTH, GRID_HEIGHT * GRID_SIZE), 3)

        state_text = font.render(f"Current state: {currentstate}", True, BLACK)
        screen.blit(state_text, (GRID_WIDTH * GRID_SIZE + 10 + self.offset[0], 10 + self.offset[1]))

        sidebar_text_color = BLACK
        sidebar_line_height = 80
        sidebar_margin_top = 40
        sidebar_margin_left = GRID_WIDTH * GRID_SIZE + 10

        for idx, (player_name, player_data) in enumerate(players.items()):
            text_y = idx * sidebar_line_height + sidebar_margin_top
            player_title = font.render(f"Player {idx}:", True, sidebar_text_color)
            fuel_text = font.render(f"FUEL: {player_data['fuel']}", True, sidebar_text_color)
            reach_goal_text = font.render(f"Reached Goal: {'True' if player_data['isReachGoal'] else 'False'}", True, sidebar_text_color)

            player_image = pygame.transform.scale(self.player_images[player_name]['idle'], (30, 40))
            screen.blit(player_image, (sidebar_margin_left + 100 + self.offset[0], text_y + self.offset[1]))
            screen.blit(player_title, (sidebar_margin_left + self.offset[0], text_y + self.offset[1]))
            screen.blit(fuel_text, (sidebar_margin_left + self.offset[0], text_y + 20 + self.offset[1]))
            screen.blit(reach_goal_text, (sidebar_margin_left + self.offset[0], text_y + 40 + self.offset[1]))

        # Draw buttons with offset
        # add borders for buttons
        pygame.draw.rect(screen, pygame.Color('white'), self.buttons['previous'].move(self.offset[0], self.offset[1]))
        pygame.draw.rect(screen, pygame.Color('white'), self.buttons['next'].move(self.offset[0], self.offset[1]))
        pygame.draw.rect(screen, pygame.Color('white'), self.buttons['play_stop'].move(self.offset[0], self.offset[1]))

        previous_text = font.render('Previous', True, BLACK)
        next_text = font.render('Next', True, BLACK)
        play_stop_text = font.render('Stop' if self.buttons['playing'] else 'Play', True, BLACK)

        screen.blit(previous_text, (self.buttons['previous'].x + 10 + self.offset[0], self.buttons['previous'].y + 10 + self.offset[1]))
        screen.blit(next_text, (self.buttons['next'].x + 10 + self.offset[0], self.buttons['next'].y + 10 + self.offset[1]))
        screen.blit(play_stop_text, (self.buttons['play_stop'].x + 10 + self.offset[0], self.buttons['play_stop'].y + 10 + self.offset[1]))
