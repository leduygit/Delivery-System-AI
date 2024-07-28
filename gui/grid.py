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
        self.road_image = self.load_road(config.ROAD_FOLDER + "/road1.png")
        self.fuel_image = self.load_fuel(config.FUEL_FOLDER + "/fuel1.png")
        self.delay_obstacle_position = self.load_delay_obstacle()
        self.fuel_position = self.load_fuel_position()

    def load_delay_obstacle(self):
        delay_obstacle = []
        for row in range(len(self.grid_data)):
            for col in range(len(self.grid_data[row])):
                if self.grid_data[row][col] not in [-1, 0] and isinstance(self.grid_data[row][col], int):
                    delay_obstacle.append((self.grid_data[row][col], row, col))
        return delay_obstacle

    def load_fuel_position(self):
        fuel_position = []
        for row in range(len(self.grid_data)):
            for col in range(len(self.grid_data[row])):
                if "F" in str(self.grid_data[row][col]):
                    fuel_value = f"F{self.grid_data[row][col][1]}"
                    fuel_position.append((fuel_value, row, col))
        return fuel_position

    def draw_fuel(self, screen):
        for fuel in self.fuel_position:
            pos = fuel[1:]
            value = fuel[0]
            if "F" in str(value):
                value = value.split("F")[1]
            screen.blit(
                self.fuel_image,
                (
                    pos[1] * config.GRID_SIZE + self.offset[0],
                    pos[0] * config.GRID_SIZE + self.offset[1],
                ),
            )
            self._draw_text(screen, value, pos[0], pos[1], (-2, +2))

    def draw_delay_obstacle(self, screen):
        for delay_obstacle in self.delay_obstacle_position:
            self._draw_text(screen, delay_obstacle[0], delay_obstacle[1], delay_obstacle[2], (-2, +2))

    def load_fuel(self, file):
        fuel_image = pygame.image.load(file)
        MIN = min(
            config.GRID_SIZE / fuel_image.get_height(),
            config.GRID_SIZE / fuel_image.get_width(),
        )
        fuel_image = pygame.transform.scale(
            fuel_image,
            (
                int(fuel_image.get_width() * MIN),
                int(fuel_image.get_height() * MIN),
            ),
        )
        return fuel_image

    def load_road(self, file):
        road_image = pygame.image.load(file)
        road_image = pygame.transform.scale(
            road_image, (config.GRID_SIZE, config.GRID_SIZE)
        )
        return road_image

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
                if "start" in filename:
                    flags[f"S{int(filename[-5]) + 1}"] = img
                elif "goal" in filename:
                    flags[f"G{int(filename[-5]) + 1}"] = img
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
                cell_value = str(self.grid_data[row][col])
                if "_" in str(cell_value):
                    owner = cell_value.split("_")[0]
                    text_value = (cell_value.split("_")[1])
                else:
                    owner = cell_value
                    text_value = cell_value

                border_color = LITE_BLACK
                
                # shift player index by 1
                if (owner[0]).upper() == "S" or owner[0] == "G":
                    if len(owner) == 1:
                        owner = f"{owner}1"
                    else:
                        owner = f"{owner[0]}{int(owner[1]) + 1}"

                if (owner[0]).upper() == "S" or owner[0] == "G":
                    color = PLAYER_COLORS[owner[1]]  # Start positions
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

                #draw flags
                if text_value[0] == "S" or text_value[0] == "G":
                    if len(text_value) == 1:
                        text_value = f"{text_value}1"
                    else:
                        text_value = f"{text_value[0]}{int(text_value[1]) + 1}"
                    screen.blit(
                        self.flags[text_value],
                        (
                            col * config.GRID_SIZE + self.offset[0],
                            row * config.GRID_SIZE + self.offset[1],
                        ),
                    )
        self.draw_fuel(screen)
        self.draw_delay_obstacle(screen)

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
