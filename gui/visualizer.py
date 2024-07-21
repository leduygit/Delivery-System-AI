# visualizer.py
import pygame
import json
import config
from config import *
from grid import Grid
from player import Player
from sidebar import Sidebar

class Visualizer:
    def __init__(self, FILENAME):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Multi-player Grid Visualization')
        self.state = self.load_state(FILENAME)
        self.current_turn_index = 0
        self.playing = False
        self.frame_count = 0
        self.clock = pygame.time.Clock()
        self.update_grid_size()
        self.offset = ((WINDOW_WIDTH - config.GRID_SIZE * len(self.state["moves"][0]["map"][0])) / 2, (WINDOW_HEIGHT - config.GRID_SIZE * len(self.state["moves"][0]["map"])) / 2)
        print(self.offset)
        self.buttons = {
            'previous': pygame.Rect(0, 0, SIDEBAR_WIDTH - 20, BUTTON_HEIGHT),
            'next': pygame.Rect(0, 0, SIDEBAR_WIDTH - 20, BUTTON_HEIGHT),
            'play_stop': pygame.Rect(0, 0, SIDEBAR_WIDTH - 20, BUTTON_HEIGHT),
            'playing': False
        }
        self.grid = Grid(self.get_current_map(), offset=self.offset)
        self.player = Player(offset=self.offset)
        self.sidebar = Sidebar(self.buttons, self.player.player_images)

    def update_grid_size(self):
        print("update_grid_size")
        row = len(self.state["moves"][0]["map"])
        col = len(self.state["moves"][0]["map"][0])
        new_grid_size = min((WINDOW_HEIGHT) // row, (WINDOW_WIDTH) // col)
        self.offset = ((WINDOW_WIDTH - new_grid_size * col) / 2, (WINDOW_HEIGHT - new_grid_size * row) / 2)
        ratio = new_grid_size / config.GRID_SIZE
        config.GRID_SIZE = new_grid_size
        config.PLAYER_IMAGE_SIZE = (config.PLAYER_IMAGE_SIZE[0] * ratio, config.PLAYER_IMAGE_SIZE[1] * ratio)

    def load_state(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def get_current_turn(self):
        return self.state['moves'][self.current_turn_index][f'turn {self.current_turn_index}']

    def get_current_map(self):
        return self.state['moves'][self.current_turn_index]['map']

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.buttons['previous'].collidepoint(mouse_pos):
                    self.current_turn_index = max(0, self.current_turn_index - 1)
                    self.buttons['playing'] = False
                elif self.buttons['next'].collidepoint(mouse_pos):
                    self.current_turn_index = min(len(self.state['moves']) - 1, self.current_turn_index + 1)
                    self.buttons['playing'] = False
                elif self.buttons['play_stop'].collidepoint(mouse_pos):
                    self.buttons['playing'] = not self.buttons['playing']
        return True

    def update_state(self):
        if self.buttons['playing'] and self.frame_count % STATE_DELAY == 0:
            self.current_turn_index = (self.current_turn_index + 1) % len(self.state['moves'])
            if self.current_turn_index == len(self.state['moves']) - 1:
                self.buttons['playing'] = False

    def draw(self):
        self.grid = Grid(self.get_current_map(), offset=self.offset)
        self.grid.draw(self.screen)
        self.player.draw(self.screen, self.get_current_turn(), self.frame_count)
        self.sidebar.draw(self.screen, self.get_current_turn(), self.current_turn_index)
        pygame.display.flip()

    def run(self):
        while self.handle_events():
            self.update_state()
            self.draw()
            self.frame_count += 1
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    FILENAME = "../Assets/Json/output.json"
    visualizer = Visualizer(FILENAME)
    visualizer.run()
