import pygame
import pygame.freetype
import os
from gui.config import WINDOW_SIZE


class LevelPage:
    def __init__(self, level):
        self.level = level
        self.files = self.get_files()
        self.selected_file = None
        self.dropdown_active = False
        self.animation_progress = 0
        self.animation_speed = 0.5  # Speed of the dropdown animation
        self.hovered_index = -1  # Index of the hovered item

        # Load background image
        self.background = pygame.image.load("Assets/images/menu/background.png")
        self.background = pygame.transform.scale(self.background, WINDOW_SIZE)

        # Dropdown configuration
        self.font = pygame.freetype.Font("Assets/Images/Menu/amongus.ttf", 30)  # Load custom font
        self.dropdown_rect = pygame.Rect(
            (WINDOW_SIZE[0] // 2 - 150) if level != "lv1" else (WINDOW_SIZE[0] // 2),
            WINDOW_SIZE[1] // 3,
            300,
            50
        )  # Centered for non-lv1 levels, right for lv1
        self.dropdown_height = 0
        self.max_height = 50 * len(self.files)  # Calculate max height based on number of items

        # Additional dropdown for algorithms (for lv1 only)
        self.algorithms = ["bfs", "dfs", "ucs", "gbfs", "astar"]
        self.selected_algorithm = None
        self.algorithm_dropdown_active = False
        self.algorithm_dropdown_height = 0
        self.algorithm_hovered_index = -1
        self.algorithm_rect = pygame.Rect(
            WINDOW_SIZE[0] // 2 - 320,
            WINDOW_SIZE[1] // 3,
            300,
            50
        )  # Algorithm dropdown on the left

    def get_files(self):
        folder = f"Assets/JSON/{self.level}"
        print(f"Getting files from {folder}")
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        files.sort()
        return files

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Common arrow settings
        arrow_color = (0, 0, 0)
        arrow_size = 20

        # Draw dropdown background for algorithm selection (left) if level is "lv1"
        if self.level == "lv1":
            pygame.draw.rect(screen, (255, 255, 255), self.algorithm_rect, 0)
            pygame.draw.rect(screen, (0, 0, 0), self.algorithm_rect, 2)

            # Draw the selected algorithm or placeholder
            if self.selected_algorithm:
                self.font.render_to(screen, (self.algorithm_rect.x + 10, self.algorithm_rect.y + 10), self.selected_algorithm, (0, 0, 0))
            else:
                self.font.render_to(screen, (self.algorithm_rect.x + 10, self.algorithm_rect.y + 10), "Select an algorithm", (0, 0, 0))

            # Draw arrow for algorithm dropdown
            arrow_pos = (self.algorithm_rect.x + self.algorithm_rect.width - 30, self.algorithm_rect.y + 10)

            if self.algorithm_dropdown_active:
                pygame.draw.polygon(screen, arrow_color, [(arrow_pos[0], arrow_pos[1]), (arrow_pos[0] + arrow_size, arrow_pos[1] + arrow_size), (arrow_pos[0] - arrow_size, arrow_pos[1] + arrow_size)])
            else:
                pygame.draw.polygon(screen, arrow_color, [(arrow_pos[0], arrow_pos[1] + arrow_size), (arrow_pos[0] + arrow_size, arrow_pos[1]), (arrow_pos[0] - arrow_size, arrow_pos[1])])

            # Update dropdown height for algorithm selection
            if self.algorithm_dropdown_active:
                self.algorithm_dropdown_height = min(self.algorithm_dropdown_height + self.animation_speed * 5, 50 * len(self.algorithms))
            else:
                self.algorithm_dropdown_height = max(self.algorithm_dropdown_height - self.animation_speed * 5, 0)

            # Draw algorithm dropdown options with animation
            if self.algorithm_dropdown_height > 0:
                num_items_visible = int(self.algorithm_dropdown_height / 50)
                for i in range(min(num_items_visible, len(self.algorithms))):
                    algorithm = self.algorithms[i]

                    offset = 50 * (i + 1)
                    if i == num_items_visible - 1:
                        offset = self.algorithm_dropdown_height
                    if i > num_items_visible - 1:
                        break
                    item_rect = pygame.Rect(self.algorithm_rect.x, self.algorithm_rect.y + offset, self.algorithm_rect.width, 50)

                    # Change color on hover
                    item_color = (200, 200, 200) if i == self.algorithm_hovered_index else (255, 255, 255)
                    pygame.draw.rect(screen, item_color, item_rect, 0)
                    pygame.draw.rect(screen, (0, 0, 0), item_rect, 2)

                    # Render the algorithm name
                    self.font.render_to(screen, (item_rect.x + 10, item_rect.y + 10), algorithm, (0, 0, 0))

        # Draw dropdown background for file selection (right or centered)
        pygame.draw.rect(screen, (255, 255, 255), self.dropdown_rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.dropdown_rect, 2)

        # Draw the selected file or placeholder
        if self.selected_file:
            self.font.render_to(screen, (self.dropdown_rect.x + 10, self.dropdown_rect.y + 10), self.selected_file, (0, 0, 0))
        else:
            placeholder_text = "Select a file" if self.level != "lv1" or self.selected_algorithm else "Select an algorithm first"
            self.font.render_to(screen, (self.dropdown_rect.x + 10, self.dropdown_rect.y + 10), placeholder_text, (0, 0, 0))

        # Draw arrow for file dropdown
        arrow_pos = (self.dropdown_rect.x + self.dropdown_rect.width - 30, self.dropdown_rect.y + 10)

        if self.dropdown_active:
            pygame.draw.polygon(screen, arrow_color, [(arrow_pos[0], arrow_pos[1]), (arrow_pos[0] + arrow_size, arrow_pos[1] + arrow_size), (arrow_pos[0] - arrow_size, arrow_pos[1] + arrow_size)])
        else:
            pygame.draw.polygon(screen, arrow_color, [(arrow_pos[0], arrow_pos[1] + arrow_size), (arrow_pos[0] + arrow_size, arrow_pos[1]), (arrow_pos[0] - arrow_size, arrow_pos[1])])

        # Update dropdown height for file selection
        if self.dropdown_active:
            self.dropdown_height = min(self.dropdown_height + self.animation_speed * 5, self.max_height)
        else:
            self.dropdown_height = max(self.dropdown_height - self.animation_speed * 5, 0)

        # Draw file dropdown options with animation
        if self.dropdown_height > 0 and (self.level != "lv1" or self.selected_algorithm):
            num_items_visible = int(self.dropdown_height / 50)
            for i in range(min(num_items_visible, len(self.files))):
                file = self.files[i]

                offset = 50 * (i + 1)
                if i == num_items_visible - 1:
                    offset = self.dropdown_height
                if i > num_items_visible - 1:
                    break
                item_rect = pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y + offset, self.dropdown_rect.width, 50)

                # Change color on hover
                item_color = (200, 200, 200) if i == self.hovered_index else (255, 255, 255)
                pygame.draw.rect(screen, item_color, item_rect, 0)
                pygame.draw.rect(screen, (0, 0, 0), item_rect, 2)

                # Render the file name
                self.font.render_to(screen, (item_rect.x + 10, item_rect.y + 10), file, (0, 0, 0))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.level == "lv1":
                    if self.algorithm_rect.collidepoint(mouse_pos):
                        self.algorithm_dropdown_active = not self.algorithm_dropdown_active
                    elif self.algorithm_dropdown_active:
                        for i, algorithm in enumerate(self.algorithms):
                            rect = pygame.Rect(self.algorithm_rect.x, self.algorithm_rect.y + 50 * (i + 1), self.algorithm_rect.width, 50)
                            if rect.collidepoint(mouse_pos):
                                self.selected_algorithm = algorithm
                                self.algorithm_dropdown_active = False
                                self.dropdown_active = False  # Reset file dropdown state
                                return None
                if (self.level != "lv1" or self.selected_algorithm) and self.dropdown_rect.collidepoint(mouse_pos):
                    self.dropdown_active = not self.dropdown_active
                elif self.dropdown_active:
                    for i, file in enumerate(self.files):
                        rect = pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y + 50 * (i + 1), self.dropdown_rect.width, 50)
                        if rect.collidepoint(mouse_pos):
                            self.selected_file = file
                            self.dropdown_active = False
                            if self.level == "lv1":
                                return f"{self.level}/{self.selected_algorithm}/{file}"
                            else:
                                return f"{self.level}/{file}"

        return None

    def handle_mouse_motion(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.dropdown_active:
            for i in range(len(self.files)):
                rect = pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y + 50 * (i + 1), self.dropdown_rect.width, 50)
                if rect.collidepoint(mouse_pos):
                    self.hovered_index = i
                    break
            else:
                self.hovered_index = -1

        if self.level == "lv1" and self.algorithm_dropdown_active:
            for i in range(len(self.algorithms)):
                rect = pygame.Rect(self.algorithm_rect.x, self.algorithm_rect.y + 50 * (i + 1), self.algorithm_rect.width, 50)
                if rect.collidepoint(mouse_pos):
                    self.algorithm_hovered_index = i
                    break
            else:
                self.algorithm_hovered_index = -1
