import pygame
import os
import random
from gui.config import *
import gui.config as config


class Grid:
    def __init__(self, grid_data, offset=(0, 0)):
        self.grid_data = grid_data
        self.offset = offset
        self.obstacle_images = self.load_images(config.OBSTACLE_FOLDER)
        self.assigned_obstacle_images = self.assign_obstacle_images()
        self.dynamic_font = pygame.font.SysFont(
            "Roboto", max(12, config.GRID_SIZE // 2)
        )
        self.flags = self.load_flags(config.FLAG_FOLDER)
        self.road_image = pygame.image.load(config.ROAD_FOLDER + "/road1.png")
        self.road_image = pygame.transform.scale(
            self.road_image, (config.GRID_SIZE, config.GRID_SIZE)
        )
        self.fuel_image = pygame.image.load(config.FUEL_FOLDER + "/fuel1.png")
        MIN = min(
            config.GRID_SIZE / self.fuel_image.get_height(),
            config.GRID_SIZE / self.fuel_image.get_width(),
        )
        self.fuel_image = pygame.transform.scale(
            self.fuel_image,
            (
                int(self.fuel_image.get_width() * MIN),
                int(self.fuel_image.get_height() * MIN),
            ),
        )

    def load_flags(self, folder):
        flags = {}
        for filename in os.listdir(folder):
            if filename.endswith(".png"):
                filename = os.path.join(folder, filename)
                img = pygame.image.load(filename)
                MAX = 2 * max(
                    img.get_height() / config.GRID_SIZE,
                    img.get_width() / config.GRID_SIZE,
                )
                img = pygame.transform.scale(
                    img, (int(img.get_width() / MAX), int(img.get_height() / MAX))
                )
                for text in ["start", "goal"]:
                    if text in filename:
                        if filename[-5] not in flags:
                            flags[filename[-5]] = {"start": None, "goal": None}
                        flags[filename[-5]][text] = {"img": img, "pos": None}
        for row in range(len(self.grid_data)):
            for col in range(len(self.grid_data[row])):
                cell_value = str(self.grid_data[row][col])
                if cell_value[0] == "S":
                    if len(cell_value) == 1:
                        cell_value += "0"
                    flags[cell_value[1]]["start"]["pos"] = (row, col)
                elif cell_value[0] == "G":
                    if len(cell_value) == 1:
                        cell_value += "0"
                    flags[cell_value[1]]["goal"]["pos"] = (row, col)
        return flags

    def update_grid(self, grid_data):
        self.grid_data = grid_data

    def load_images(self, folder):
        images = []
        for filename in os.listdir(folder):
            if filename.endswith(".png"):
                filename = os.path.join(folder, filename)
                img = pygame.image.load(filename)
                img = pygame.transform.scale(img, (config.GRID_SIZE, config.GRID_SIZE))
                images.append(img)
        return images

    def assign_obstacle_images(self):
        assigned_images = {}
        for row in range(len(self.grid_data)):
            for col in range(len(self.grid_data[row])):
                if str(self.grid_data[row][col]) == "-1":
                    assigned_images[(row, col)] = random.choice(self.obstacle_images)
        return assigned_images

    def draw(self, screen):
        screen.fill(WHITE)
        for row in range(len(self.grid_data)):
            for col in range(len(self.grid_data[row])):
                screen.blit(
                    self.road_image,
                    (
                        col * config.GRID_SIZE + self.offset[0],
                        row * config.GRID_SIZE + self.offset[1],
                    ),
                )
                if isinstance(self.grid_data[row][col], list):
                    if self.grid_data[row][col][0] == "F":
                        screen.blit(
                            self.fuel_image,
                            (
                                col * config.GRID_SIZE
                                + self.offset[0]
                                + (config.GRID_SIZE - self.fuel_image.get_width()) / 2,
                                row * config.GRID_SIZE
                                + self.offset[1]
                                + (config.GRID_SIZE - self.fuel_image.get_height()) / 2,
                            ),
                        )
                        self._draw_text(
                            screen, self.grid_data[row][col][1], row, col, (-2, +2)
                        )
                        continue
                cell_value = str(self.grid_data[row][col])
                color = WHITE
                border_color = LITE_BLACK

                text_value = cell_value
                if cell_value[0] == "S" or cell_value[0] == "G":
                    if len(cell_value) == 1:
                        cell_value += "1"
                    else:
                        cell_value = f"{cell_value[0]}{int(cell_value[1]) + 1}"

                if cell_value[0] == "S" or cell_value[0] == "G":
                    color = PLAYER_COLORS[cell_value[1]]  # Start positions
                    pygame.draw.rect(
                        screen,
                        color,
                        (
                            col * config.GRID_SIZE + self.offset[0],
                            row * config.GRID_SIZE + self.offset[1],
                            config.GRID_SIZE,
                            config.GRID_SIZE,
                        ),
                    )
                # draw obstacles
                elif cell_value == "-1":
                    obstacle_image = self.assigned_obstacle_images.get((row, col), None)
                    if obstacle_image:
                        screen.blit(
                            obstacle_image,
                            (
                                col * config.GRID_SIZE + self.offset[0],
                                row * config.GRID_SIZE + self.offset[1],
                            ),
                        )
                # draw border
                pygame.draw.rect(
                    screen,
                    border_color,
                    (
                        col * config.GRID_SIZE + self.offset[0],
                        row * config.GRID_SIZE + self.offset[1],
                        config.GRID_SIZE,
                        config.GRID_SIZE,
                    ),
                    1,
                )
                # check if text_value is integer
                if text_value.isdigit() and text_value not in ["-1", "0"]:
                    self._draw_text(screen, text_value, row, col)

        self._draw_flags(screen)

    def _draw_flags(self, screen):
        for player in self.flags:
            for text in ["start", "goal"]:
                if self.flags[player][text]["pos"]:
                    screen.blit(
                        self.flags[player][text]["img"],
                        (
                            self.flags[player][text]["pos"][1] * config.GRID_SIZE
                            + self.offset[0],
                            self.flags[player][text]["pos"][0] * config.GRID_SIZE
                            + self.offset[1],
                        ),
                    )

    def _draw_text(self, screen, text_value, row, col, offset=(0, 0)):
        text_value = str(text_value)
        text_color = BLACK
        text_surface = self.dynamic_font.render(text_value, True, text_color)
        text_rect = text_surface.get_rect(
            center=(
                col * config.GRID_SIZE
                + config.GRID_SIZE // 2
                + self.offset[0]
                + offset[0],
                row * config.GRID_SIZE
                + config.GRID_SIZE // 2
                + self.offset[1]
                + offset[1],
            )
        )
        screen.blit(text_surface, text_rect)
