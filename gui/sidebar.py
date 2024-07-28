import pygame
import os
from gui.config import (
    GRAY,
    BLACK,
    SIDEBAR_WIDTH,
    WINDOW_SIZE,
    font,
    BUTTON_HEIGHT,
    CONTROLBUTTON_FOLDER,
)


class Sidebar:
    def __init__(self, buttons, player_images, offset=(0, 0)):
        self.buttons = buttons
        self.player_images = player_images
        self.offset = offset
        self.load_button_images()

    def load_button_images(self):
        self.button_images = {
            "previous": pygame.image.load(
                os.path.join(CONTROLBUTTON_FOLDER, "prev.png")
            ),
            "next": pygame.image.load(os.path.join(CONTROLBUTTON_FOLDER, "next.png")),
            "play": pygame.image.load(os.path.join(CONTROLBUTTON_FOLDER, "play.png")),
            "pause": pygame.image.load(os.path.join(CONTROLBUTTON_FOLDER, "pause.png")),
        }
        for key in self.button_images:
            self.button_images[key] = pygame.transform.scale(
                self.button_images[key], (50, 50)
            )

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

        # Render and draw the current turn text
        total_players = len(players.items())
        state_text = font.render(f"Current time: {int((current_turn_index + total_players - 1) / total_players)}", True, BLACK)
        screen.blit(state_text, (sidebar_x + 10, sidebar_y + 10))

        sidebar_text_color = BLACK
        sidebar_line_height = 70
        sidebar_margin_top = 40
        sidebar_margin_left = sidebar_x + 10

        for idx, (player_name, player_data) in enumerate(players.items()):
            text_y = idx * sidebar_line_height + sidebar_margin_top
            player_title = font.render(
                f"{player_name[:-1] + str(int(player_name[-1]) - 1)}:",
                True,
                sidebar_text_color,
            )
            if player_data["fuel"] is not None:
                fuel_color = sidebar_text_color if player_data["fuel"] > 0 else (255, 0, 0)
            else:
                fuel_color = sidebar_text_color
            fuel_text = font.render(
                f"FUEL: {player_data['fuel']}", True, fuel_color
            )
            if player_data["time"] is not None:
                time_color = sidebar_text_color if player_data["time"] > 0 else (255, 0, 0)
            else:
                time_color = sidebar_text_color
            time_text = font.render(
                f"TIME: {player_data['time']}", True, time_color
            )

            player_image = pygame.transform.scale(
                self.player_images[player_name]["idle"], (30, 40)
            )
            screen.blit(player_image, (sidebar_margin_left + 100, text_y))
            screen.blit(player_title, (sidebar_margin_left, text_y))
            screen.blit(fuel_text, (sidebar_margin_left, text_y + 20))
            screen.blit(time_text, (sidebar_margin_left, text_y + 40))

        button_offset_x = sidebar_x + 10
        button_offset_y = sidebar_y + sidebar_height - BUTTON_HEIGHT - 20

        self.buttons["previous"].topleft = (button_offset_x, button_offset_y)
        self.buttons["play_stop"].topleft = (button_offset_x + 60, button_offset_y)
        self.buttons["next"].topleft = (button_offset_x + 120, button_offset_y)

        screen.blit(self.button_images["previous"], self.buttons["previous"].topleft)
        play_stop_image = (
            self.button_images["pause"]
            if self.buttons["playing"]
            else self.button_images["play"]
        )
        screen.blit(play_stop_image, self.buttons["play_stop"].topleft)
        screen.blit(self.button_images["next"], self.buttons["next"].topleft)
