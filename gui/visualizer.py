import pygame
import json
from config import *
from grid import Grid
from player import Player
from sidebar import Sidebar
from menu import Menu  # Import the Menu class

class Visualizer:
    def __init__(self, FILENAME):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Delivery-System-AI')
        self.state = self.load_state(FILENAME)
        self.state_ids = list(self.state.keys())
        self.current_state_index = 0
        self.playing = False
        self.frame_count = 0
        self.clock = pygame.time.Clock()

        # Initialize buttons dictionary
        self.buttons = {
            'previous': pygame.Rect(GRID_WIDTH * GRID_SIZE + 10, GRID_HEIGHT * GRID_SIZE - 3 * BUTTON_HEIGHT - 20, SIDEBAR_WIDTH - 20, BUTTON_HEIGHT),
            'next': pygame.Rect(GRID_WIDTH * GRID_SIZE + 10, GRID_HEIGHT * GRID_SIZE - 2 * BUTTON_HEIGHT - 20, SIDEBAR_WIDTH - 20, BUTTON_HEIGHT),
            'play_stop': pygame.Rect(GRID_WIDTH * GRID_SIZE + 10, GRID_HEIGHT * GRID_SIZE - BUTTON_HEIGHT - 20, SIDEBAR_WIDTH - 20, BUTTON_HEIGHT),
            'playing': False
        }

        # Initialize Menu
        self.menu = Menu()
        self.menu_active = True

        # Initialize Grid, Player, and Sidebar
        self.grid = Grid(self.get_current_grid())
        self.player = Player()
        self.sidebar = Sidebar(self.buttons)

    def changeFile(self, FILENAME):
        self.state = self.load_state(FILENAME)
        self.state_ids = list(self.state.keys())

    def load_state(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def get_current_grid(self):
        return [row.split() for row in self.state[self.state_ids[self.current_state_index]]['map']['grid']]

    def get_players(self):
        return {k: v for k, v in self.state[self.state_ids[self.current_state_index]].items() if k.startswith('player')}

    def handle_events(self):
        if self.menu_active:
            result = self.menu.handle_events()
            if result == 'exit':
                return False
            elif result == 'start':
                self.menu_active = False
                return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.buttons['previous'].collidepoint(mouse_pos):
                        self.current_state_index = max(0, self.current_state_index - 1)
                        self.buttons['playing'] = False
                    elif self.buttons['next'].collidepoint(mouse_pos):
                        self.current_state_index = min(len(self.state_ids) - 1, self.current_state_index + 1)
                        self.buttons['playing'] = False
                    elif self.buttons['play_stop'].collidepoint(mouse_pos):
                        self.buttons['playing'] = not self.buttons['playing']
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Check if Escape key is pressed
                        self.menu_active = True  # Return to menu
        return True

    def update_state(self):
        if self.buttons['playing'] and self.frame_count % STATE_DELAY == 0:
            self.current_state_index = (self.current_state_index + 1) % len(self.state_ids)
            if self.current_state_index == len(self.state_ids) - 1:
                self.buttons['playing'] = False

    def draw(self):
        self.grid.draw(self.screen)
        self.player.draw(self.screen, self.get_players(), self.frame_count)
        self.sidebar.draw(self.screen, self.get_players(), self.state_ids[self.current_state_index])
        pygame.display.flip()

    def run(self):
        while self.handle_events():
            if self.menu_active:
                self.menu.draw(self.screen)
            else:
                self.update_state()
                self.draw()
            self.frame_count += 1
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    FILENAME = '../Assets/Json/state.json'
    visualizer = Visualizer(FILENAME)
    visualizer.run()
