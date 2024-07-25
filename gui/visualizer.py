import pygame
import json
import gui.config as config
from gui.config import *
from gui.grid import Grid
from gui.player import Player
from gui.sidebar import Sidebar
from gui.menu import Menu  # Import the Menu class
from gui.level_page import LevelPage  # Import the LevelPage class
import warnings
from PIL import Image

warnings.filterwarnings("ignore", category=UserWarning, module="PIL")


class Visualizer:
    def __init__(self, FILENAME):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Multi-player Grid Visualization")
        self.state = self.load_state(FILENAME)
        self.current_turn_index = 0
        self.playing = False
        self.frame_count = 0
        self.clock = pygame.time.Clock()
        self.update_grid_size()

        # Initialize buttons dictionary
        self.buttons = {
            "previous": pygame.Rect(0, 0, 50, 50),
            "next": pygame.Rect(0, 0, 50, 50),
            "play_stop": pygame.Rect(0, 0, 50, 50),
            "playing": False,
        }

        # Initialize Menu
        self.menu = Menu()
        self.menu_active = True

        # Initialize Grid, Player, and Sidebar
        self.grid = Grid(self.get_current_map(), offset=self.offset)
        self.player = Player(offset=self.offset)
        self.sidebar = Sidebar(self.buttons, self.player.player_images)

    def update_grid_size(self):
        current_map = self.get_current_map()
        self.map_rows = len(current_map)
        self.map_cols = len(current_map[0])

        # Calculate new grid size
        new_grid_size = min(
            WINDOW_HEIGHT // self.map_rows, WINDOW_WIDTH // self.map_cols
        )

        # Calculate new offset
        self.offset = (
            (WINDOW_WIDTH - new_grid_size * self.map_cols) / 2,
            (WINDOW_HEIGHT - new_grid_size * self.map_rows) / 2,
        )

        # Calculate ratio for resizing
        ratio = new_grid_size / config.GRID_SIZE

        # Update global grid size
        config.GRID_SIZE = new_grid_size

        # Update player image size proportionally
        config.PLAYER_IMAGE_SIZE = (
            int(config.PLAYER_IMAGE_SIZE[0] * ratio),
            int(config.PLAYER_IMAGE_SIZE[1] * ratio),
        )

    def load_state(self, filename):
        with open(filename, "r") as f:
            return json.load(f)

    def get_current_turn(self):
        return self.state["moves"][self.current_turn_index][
            f"turn {self.current_turn_index}"
        ]

    def get_current_map(self):
        return self.state["moves"][self.current_turn_index]["map"]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.buttons["previous"].collidepoint(mouse_pos):
                    self.current_turn_index = max(0, self.current_turn_index - 1)
                    self.buttons["playing"] = False
                    self.update_grid_size()  # Update grid size when changing turns
                elif self.buttons["next"].collidepoint(mouse_pos):
                    self.current_turn_index = min(
                        len(self.state["moves"]) - 1, self.current_turn_index + 1
                    )
                    self.buttons["playing"] = False
                    self.update_grid_size()  # Update grid size when changing turns
                elif self.buttons["play_stop"].collidepoint(mouse_pos):
                    self.buttons["playing"] = not self.buttons["playing"]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Check if Escape key is pressed
                    return "menu"
        return True

    def update_state(self):
        if self.buttons["playing"] and self.frame_count % STATE_DELAY == 0:
            self.current_turn_index = (self.current_turn_index + 1) % len(
                self.state["moves"]
            )
            if self.current_turn_index == len(self.state["moves"]) - 1:
                self.buttons["playing"] = False
            self.update_grid_size()  # Update grid size when changing state

    def draw(self):
        self.grid.update_grid(self.get_current_map())
        self.grid.draw(self.screen)
        self.player.draw(self.screen, self.get_current_turn(), self.frame_count)
        self.sidebar.draw(self.screen, self.get_current_turn(), self.current_turn_index)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            result = self.handle_events()
            if result == "menu":
                return "menu"
            elif not result:
                running = False
            else:
                self.update_state()
                self.draw()
            self.frame_count += 1
            self.clock.tick(60)
        pygame.quit()


def visualize():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Delivery system")

    # Initialize Menu and other pages
    menu = Menu()
    current_page = menu
    level_page = None
    visualizer = None

    # Main game loop
    running = True
    while running:
        if isinstance(current_page, Menu):
            result = current_page.handle_events()
            if result == "exit":
                running = False
            elif result in ["lv1", "lv2", "lv3", "lv4"]:
                level_page = LevelPage(result)
                current_page = level_page

        elif isinstance(current_page, LevelPage):
            result = current_page.handle_events()
            if result == "exit":
                running = False
            elif result == "menu":
                current_page = menu
            elif result:
                visualizer = Visualizer(f"Assets/JSON/{result}")
                current_page = visualizer

        elif isinstance(current_page, Visualizer):
            result = current_page.run()
            if result == "menu":
                current_page = menu

        if isinstance(current_page, Menu) or isinstance(current_page, LevelPage):
            # current page it's level page handle hover events
            if isinstance(current_page, LevelPage):
                current_page.handle_mouse_motion()
            current_page.draw(screen)

    pygame.quit()
