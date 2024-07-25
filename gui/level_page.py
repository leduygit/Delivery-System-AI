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
        self.animation_speed = 0.1  # Speed of the dropdown animation
        self.hovered_index = -1  # Index of the hovered item

        # Load background image
        self.background = pygame.image.load("Assets/images/menu/background.png")
        self.background = pygame.image.load("Assets/images/menu/background.png")
        self.background = pygame.transform.scale(self.background, WINDOW_SIZE)

        # Dropdown configuration
        self.font = pygame.freetype.Font(
            "Assets/Images/Menu/amongus.ttf", 30
        )  # Load custom font
        self.dropdown_rect = pygame.Rect(
            WINDOW_SIZE[0] // 2 - 150, WINDOW_SIZE[1] // 3, 300, 50
        )  # Larger dropdown
        self.font = pygame.freetype.Font(
            "Assets/Images/Menu/amongus.ttf", 30
        )  # Load custom font
        self.dropdown_rect = pygame.Rect(
            WINDOW_SIZE[0] // 2 - 150, WINDOW_SIZE[1] // 3, 300, 50
        )  # Larger dropdown
        self.dropdown_height = 0
        self.max_height = 50 * len(
            self.files
        )  # Calculate max height based on number of items
        self.max_height = 50 * len(
            self.files
        )  # Calculate max height based on number of items

    def get_files(self):
        folder = f"Assets/JSON/{self.level}/"
        print(f"Getting files from {folder}")
        files = [
            f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))
        ]
        files.sort()
        return files

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Draw dropdown background
        pygame.draw.rect(screen, (255, 255, 255), self.dropdown_rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.dropdown_rect, 2)

        # Draw the selected file or placeholder
        if self.selected_file:
            self.font.render_to(
                screen,
                (self.dropdown_rect.x + 10, self.dropdown_rect.y + 10),
                self.selected_file,
                (0, 0, 0),
            )
            self.font.render_to(
                screen,
                (self.dropdown_rect.x + 10, self.dropdown_rect.y + 10),
                self.selected_file,
                (0, 0, 0),
            )
        else:
            self.font.render_to(
                screen,
                (self.dropdown_rect.x + 10, self.dropdown_rect.y + 10),
                "Select a file",
                (0, 0, 0),
            )
            self.font.render_to(
                screen,
                (self.dropdown_rect.x + 10, self.dropdown_rect.y + 10),
                "Select a file",
                (0, 0, 0),
            )

        # Draw arrow
        arrow_color = (0, 0, 0)
        arrow_size = 20
        arrow_pos = (
            self.dropdown_rect.x + self.dropdown_rect.width - 30,
            self.dropdown_rect.y + 10,
        )
        arrow_pos = (
            self.dropdown_rect.x + self.dropdown_rect.width - 30,
            self.dropdown_rect.y + 10,
        )

        if self.dropdown_active:
            pygame.draw.polygon(
                screen,
                arrow_color,
                [
                    (arrow_pos[0], arrow_pos[1]),
                    (arrow_pos[0] + arrow_size, arrow_pos[1] + arrow_size),
                    (arrow_pos[0] - arrow_size, arrow_pos[1] + arrow_size),
                ],
            )
            pygame.draw.polygon(
                screen,
                arrow_color,
                [
                    (arrow_pos[0], arrow_pos[1]),
                    (arrow_pos[0] + arrow_size, arrow_pos[1] + arrow_size),
                    (arrow_pos[0] - arrow_size, arrow_pos[1] + arrow_size),
                ],
            )
        if not self.dropdown_active:
            pygame.draw.polygon(
                screen,
                arrow_color,
                [
                    (arrow_pos[0], arrow_pos[1] + arrow_size),
                    (arrow_pos[0] + arrow_size, arrow_pos[1]),
                    (arrow_pos[0] - arrow_size, arrow_pos[1]),
                ],
            )
            pygame.draw.polygon(
                screen,
                arrow_color,
                [
                    (arrow_pos[0], arrow_pos[1] + arrow_size),
                    (arrow_pos[0] + arrow_size, arrow_pos[1]),
                    (arrow_pos[0] - arrow_size, arrow_pos[1]),
                ],
            )

        # Update dropdown height
        if self.dropdown_active:
            self.dropdown_height = min(
                self.dropdown_height + self.animation_speed * 5, self.max_height
            )
            self.dropdown_height = min(
                self.dropdown_height + self.animation_speed * 5, self.max_height
            )
        else:
            self.dropdown_height = max(
                self.dropdown_height - self.animation_speed * 5, 0
            )
            self.dropdown_height = max(
                self.dropdown_height - self.animation_speed * 5, 0
            )

        # Draw dropdown options with animation
        if self.dropdown_height > 0:
            num_items_visible = int(self.dropdown_height / 50)
            for i in range(min(num_items_visible, len(self.files))):
                file = self.files[i]

                offset = 50 * (i + 1)
                if i == num_items_visible - 1:
                    offset = self.dropdown_height
                if i > num_items_visible - 1:
                    break
                item_rect = pygame.Rect(
                    self.dropdown_rect.x,
                    self.dropdown_rect.y + offset,
                    self.dropdown_rect.width,
                    50,
                )

                # Change color on hover
                item_color = (
                    (200, 200, 200) if i == self.hovered_index else (255, 255, 255)
                )
                pygame.draw.rect(screen, item_color, item_rect, 0)
                pygame.draw.rect(screen, (0, 0, 0), item_rect, 2)

                # Render the file name
                self.font.render_to(
                    screen, (item_rect.x + 10, item_rect.y + 10), file, (0, 0, 0)
                )

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
                if self.dropdown_rect.collidepoint(mouse_pos):
                    self.dropdown_active = not self.dropdown_active
                elif self.dropdown_active:
                    for i, file in enumerate(self.files):
                        rect = pygame.Rect(
                            self.dropdown_rect.x,
                            self.dropdown_rect.y + 50 * (i + 1),
                            self.dropdown_rect.width,
                            50,
                        )
                        rect = pygame.Rect(
                            self.dropdown_rect.x,
                            self.dropdown_rect.y + 50 * (i + 1),
                            self.dropdown_rect.width,
                            50,
                        )
                        if rect.collidepoint(mouse_pos):
                            self.selected_file = file
                            self.dropdown_active = False
                            return f"{self.level}/{file}"
        return None

    def handle_mouse_motion(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.dropdown_active:
            for i in range(len(self.files)):
                rect = pygame.Rect(
                    self.dropdown_rect.x,
                    self.dropdown_rect.y + 50 * (i + 1),
                    self.dropdown_rect.width,
                    50,
                )
                rect = pygame.Rect(
                    self.dropdown_rect.x,
                    self.dropdown_rect.y + 50 * (i + 1),
                    self.dropdown_rect.width,
                    50,
                )
                if rect.collidepoint(mouse_pos):
                    self.hovered_index = i
                    break
            else:
                self.hovered_index = -1
