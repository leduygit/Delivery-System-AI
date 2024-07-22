import pygame
from gui.config import WINDOW_SIZE

class Menu:
    def __init__(self):
        # Load menu images
        self.background = pygame.image.load('Assets/images/menu/background.png')
        self.start_button = pygame.image.load('Assets/images/menu/lv1.png')
        self.lv2_button = pygame.image.load('Assets/images/menu/lv2.png')
        self.lv3_button = pygame.image.load('Assets/images/menu/lv3.png')
        self.lv4_button = pygame.image.load('Assets/images/menu/lv4.png')
        self.exit_button = pygame.image.load('Assets/images/menu/exit.png')

        # Load hover images
        self.start_button_hover = pygame.image.load('Assets/images/menu/lv1-2.png')
        self.lv2_button_hover = pygame.image.load('Assets/images/menu/lv2-2.png')
        self.lv3_button_hover = pygame.image.load('Assets/images/menu/lv3-2.png')
        self.lv4_button_hover = pygame.image.load('Assets/images/menu/lv4-2.png')
        self.exit_button_hover = pygame.image.load('Assets/images/menu/exit-2.png')

        # Scale the menu background to fit the window size
        self.background = pygame.transform.scale(self.background, WINDOW_SIZE)

        # Button rectangles for detecting clicks
        button_y = WINDOW_SIZE[1] // 2 - 100
        self.start_button_rect = self.start_button.get_rect(center=(WINDOW_SIZE[0] // 2, button_y))
        self.lv2_button_rect = self.lv2_button.get_rect(center=(WINDOW_SIZE[0] // 2, button_y + 100))
        self.lv3_button_rect = self.lv3_button.get_rect(center=(WINDOW_SIZE[0] // 2, button_y + 200))
        self.lv4_button_rect = self.lv4_button.get_rect(center=(WINDOW_SIZE[0] // 2, button_y + 300))
        self.exit_button_rect = self.exit_button.get_rect(center=(WINDOW_SIZE[0] // 2, button_y + 400))

        self.hovered_button = None  # Track which button is hovered

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        
        # Draw buttons with hover effect
        if self.hovered_button == 'start':
            screen.blit(self.start_button_hover, self.start_button_rect.topleft)
        else:
            screen.blit(self.start_button, self.start_button_rect.topleft)

        if self.hovered_button == 'lv2':
            screen.blit(self.lv2_button_hover, self.lv2_button_rect.topleft)
        else:
            screen.blit(self.lv2_button, self.lv2_button_rect.topleft)

        if self.hovered_button == 'lv3':
            screen.blit(self.lv3_button_hover, self.lv3_button_rect.topleft)
        else:
            screen.blit(self.lv3_button, self.lv3_button_rect.topleft)

        if self.hovered_button == 'lv4':
            screen.blit(self.lv4_button_hover, self.lv4_button_rect.topleft)
        else:
            screen.blit(self.lv4_button, self.lv4_button_rect.topleft)

        if self.hovered_button == 'exit':
            screen.blit(self.exit_button_hover, self.exit_button_rect.topleft)
        else:
            screen.blit(self.exit_button, self.exit_button_rect.topleft)
        
        pygame.display.flip()

    def handle_events(self):
        mouse_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos

        # Update hovered button based on mouse position
        if mouse_pos:
            if self.start_button_rect.collidepoint(mouse_pos):
                self.hovered_button = 'start'
            elif self.lv2_button_rect.collidepoint(mouse_pos):
                self.hovered_button = 'lv2'
            elif self.lv3_button_rect.collidepoint(mouse_pos):
                self.hovered_button = 'lv3'
            elif self.lv4_button_rect.collidepoint(mouse_pos):
                self.hovered_button = 'lv4'
            elif self.exit_button_rect.collidepoint(mouse_pos):
                self.hovered_button = 'exit'
            else:
                self.hovered_button = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(mouse_pos):
                    return "lv1"
                elif self.lv2_button_rect.collidepoint(mouse_pos):
                    return "lv2"
                elif self.lv3_button_rect.collidepoint(mouse_pos):
                    return "lv3"
                elif self.lv4_button_rect.collidepoint(mouse_pos):
                    return "lv4"
                elif self.exit_button_rect.collidepoint(mouse_pos):
                    return "exit"

        return None
