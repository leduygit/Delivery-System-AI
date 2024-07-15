import pygame
from config import GRAY, BLACK, SIDEBAR_WIDTH, GRID_WIDTH, GRID_HEIGHT, font, GRID_SIZE

class Sidebar:
    def __init__(self, buttons):
        self.buttons = buttons

    def draw(self, screen, players, currentstate):
        sidebar_bg_color = GRAY
        pygame.draw.rect(screen, sidebar_bg_color, (GRID_WIDTH * GRID_SIZE, 0, SIDEBAR_WIDTH, GRID_HEIGHT * GRID_SIZE))

        state_text = font.render(f"Current state: {currentstate}", True, BLACK)
        screen.blit(state_text, (GRID_WIDTH * GRID_SIZE + 10, 10))

        sidebar_text_color = BLACK
        sidebar_line_height = 80
        sidebar_margin_top = 40
        sidebar_margin_left = GRID_WIDTH * GRID_SIZE + 10

        for idx, (player_name, player_data) in enumerate(players.items()):
            text_y = idx * sidebar_line_height + sidebar_margin_top
            player_title = font.render(f"Player {idx}:", True, sidebar_text_color)
            fuel_text = font.render(f"FUEL: {player_data['fuel']}", True, sidebar_text_color)
            reach_goal_text = font.render(f"Reached Goal: {'True' if player_data['isReachGoal'] else 'False'}", True, sidebar_text_color)

            screen.blit(player_title, (sidebar_margin_left, text_y))
            screen.blit(fuel_text, (sidebar_margin_left, text_y + 20))
            screen.blit(reach_goal_text, (sidebar_margin_left, text_y + 40))

        pygame.draw.rect(screen, pygame.Color('white'), self.buttons['previous'])
        pygame.draw.rect(screen, pygame.Color('white'), self.buttons['next'])
        pygame.draw.rect(screen, pygame.Color('white'), self.buttons['play_stop'])

        previous_text = font.render('Previous', True, BLACK)
        next_text = font.render('Next', True, BLACK)
        play_stop_text = font.render('Stop' if self.buttons['playing'] else 'Play', True, BLACK)

        screen.blit(previous_text, (self.buttons['previous'].x + 10, self.buttons['previous'].y + 10))
        screen.blit(next_text, (self.buttons['next'].x + 10, self.buttons['next'].y + 10))
        screen.blit(play_stop_text, (self.buttons['play_stop'].x + 10, self.buttons['play_stop'].y + 10))
