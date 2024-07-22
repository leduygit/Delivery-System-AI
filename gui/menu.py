import pygame
from config import WINDOW_SIZE


class Menu:
    def __init__(self):
        # Load menu images
        self.background = pygame.image.load("../assets/images/menu/background.png")
        self.start_button = pygame.image.load("../assets/images/menu/lv1.png")
        self.exit_button = pygame.image.load("../assets/images/menu/exit.png")

        # Scale the menu background to fit the window size
        self.background = pygame.transform.scale(self.background, WINDOW_SIZE)

        # Button rectangles for detecting clicks
        self.start_button_rect = self.start_button.get_rect(
            center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 - 50)
        )
        self.exit_button_rect = self.exit_button.get_rect(
            center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 50)
        )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.start_button, self.start_button_rect.topleft)
        screen.blit(self.exit_button, self.exit_button_rect.topleft)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.start_button_rect.collidepoint(mouse_pos):
                    return "start"
                elif self.exit_button_rect.collidepoint(mouse_pos):
                    return "exit"
        return None
