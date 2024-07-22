# sidebar.py
import pygame
from datetime import datetime
from gui.config import GRAY, BLACK, SIDEBAR_WIDTH, WINDOW_SIZE, font, BUTTON_HEIGHT

class Sidebar:
    def __init__(self, buttons, player_images, offset=(0, 0)):
        self.buttons = buttons
        self.player_images = player_images
        self.offset = offset

    def draw(self, screen, players, current_turn_index):
        sidebar_bg_color = GRAY
        sidebar_x = WINDOW_SIZE[0] - SIDEBAR_WIDTH + self.offset[0]
        sidebar_y = self.offset[1]
        sidebar_width = SIDEBAR_WIDTH
        sidebar_height = WINDOW_SIZE[1]

        # Draw sidebar background
        pygame.draw.rect(
            screen,
            sidebar_bg_color,
            (sidebar_x, sidebar_y, sidebar_width, sidebar_height),
        )

        # Draw sidebar border
        pygame.draw.rect(
            screen, BLACK, (sidebar_x, sidebar_y, sidebar_width, sidebar_height), 2
        )

        state_text = font.render(f"Current turn: {current_turn_index}", True, BLACK)
        screen.blit(state_text, (sidebar_x + 10, sidebar_y + 10))

        sidebar_text_color = BLACK
        sidebar_line_height = 80
        sidebar_margin_top = 40
        sidebar_margin_left = sidebar_x + 10

        for idx, (player_name, player_data) in enumerate(players.items()):
            text_y = idx * sidebar_line_height + sidebar_margin_top
            player_title = font.render(
                f"{player_name[:-1] + str(int(player_name[-1]) - 1)}:",
                True,
                sidebar_text_color,
            )
            fuel_text = font.render(
                f"FUEL: {player_data['fuel']}", True, sidebar_text_color
            )
            reach_goal_text = font.render(
                f"Reached Goal: {'True' if player_data['reached'] else 'False'}",
                True,
                sidebar_text_color,
            )

            player_image = pygame.transform.scale(
                self.player_images[player_name]["idle"], (30, 40)
            )
            screen.blit(player_image, (sidebar_margin_left + 100, text_y))
            screen.blit(player_title, (sidebar_margin_left, text_y))
            screen.blit(fuel_text, (sidebar_margin_left, text_y + 20))
            screen.blit(reach_goal_text, (sidebar_margin_left, text_y + 40))

        button_offset_x = sidebar_x
        button_offset_y = sidebar_y + sidebar_height - 3 * BUTTON_HEIGHT - 40

        self.buttons["previous"].topleft = (button_offset_x + 10, button_offset_y)
        self.buttons["next"].topleft = (
            button_offset_x + 10,
            button_offset_y + BUTTON_HEIGHT + 10,
        )
        self.buttons["play_stop"].topleft = (
            button_offset_x + 10,
            button_offset_y + 2 * (BUTTON_HEIGHT + 10),
        )

        pygame.draw.rect(screen, pygame.Color("white"), self.buttons["previous"])
        pygame.draw.rect(screen, pygame.Color("white"), self.buttons["next"])
        pygame.draw.rect(screen, pygame.Color("white"), self.buttons["play_stop"])

        previous_text = font.render("Previous", True, BLACK)
        next_text = font.render("Next", True, BLACK)
        play_stop_text = font.render(
            "Stop" if self.buttons["playing"] else "Play", True, BLACK
        )

        screen.blit(
            previous_text,
            (self.buttons["previous"].x + 10, self.buttons["previous"].y + 10),
        )
        screen.blit(
            next_text, (self.buttons["next"].x + 10, self.buttons["next"].y + 10)
        )
        screen.blit(
            play_stop_text,
            (self.buttons["play_stop"].x + 10, self.buttons["play_stop"].y + 10),
        )
