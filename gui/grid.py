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
                # img = pygame.transform.scale(img, (config.GRID_SIZE/2, config.GRID_SIZE/2))
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
                cell_value = str(self.grid_data[row][col])
                color = WHITE
                text_color = BLACK
                border_color = LITE_BLACK

                text_value = cell_value
                isObstacle = False
                if cell_value[0] == "S" or cell_value[0] == "G":
                    if len(cell_value) == 1:
                        cell_value += "1"
                    else:
                        cell_value = f"{cell_value[0]}{int(cell_value[1]) + 1}"

                if cell_value[0] == "S":
                    color = PLAYER_COLORS[cell_value[1]]  # Start positions
                elif cell_value[0] == "G":
                    color = PLAYER_COLORS[cell_value[1]]  # Goals
                elif cell_value[0] == "F":
                    color = GRAY  # Fuel stations
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
                    isObstacle = True

                if not isObstacle:
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
                    text_surface = self.dynamic_font.render(
                        text_value, True, text_color
                    )
                    text_rect = text_surface.get_rect(
                        center=(
                            col * config.GRID_SIZE
                            + config.GRID_SIZE // 2
                            + self.offset[0],
                            row * config.GRID_SIZE
                            + config.GRID_SIZE // 2
                            + self.offset[1],
                        )
                    )
                    screen.blit(text_surface, text_rect)

        for player in self.flags:
            if self.flags[player]["start"]["pos"]:
                screen.blit(
                    self.flags[player]["start"]["img"],
                    (
                        self.flags[player]["start"]["pos"][1] * config.GRID_SIZE
                        + self.offset[0],
                        self.flags[player]["start"]["pos"][0] * config.GRID_SIZE
                        + self.offset[1],
                    ),
                )
            if self.flags[player]["goal"]["pos"]:
                screen.blit(
                    self.flags[player]["goal"]["img"],
                    (
                        self.flags[player]["goal"]["pos"][1] * config.GRID_SIZE
                        + self.offset[0],
                        self.flags[player]["goal"]["pos"][0] * config.GRID_SIZE
                        + self.offset[1],
                    ),
                )
