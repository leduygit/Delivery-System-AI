# player.py
import pygame
from config import GRID_SIZE, PLAYER_IMAGE_SIZE, FRAME_DELAY, IMAGE_FOLDER

class Player:
    def __init__(self):
        self.player_images = {}
        self.previous_positions = {}
        self.previous_move = {}
        self.load_images()

    def load_images(self):
        for player_num in range(1, 5):
            self.player_images[f'player{player_num - 1}'] = {
                'left': [pygame.transform.scale(pygame.image.load(f'{IMAGE_FOLDER}/Players/player{player_num}-left-{i}.png'), PLAYER_IMAGE_SIZE) for i in range(12)],
                'right': [pygame.transform.scale(pygame.image.load(f'{IMAGE_FOLDER}/Players/player{player_num}-right-{i}.png'), PLAYER_IMAGE_SIZE) for i in range(12)],
                'idle': pygame.transform.scale(pygame.image.load(f'{IMAGE_FOLDER}/Players/player{player_num}-idle.png'), PLAYER_IMAGE_SIZE)
            }

    def get_player_image(self, player_name, direction, frame, is_idle):
        if is_idle:
            return self.player_images[player_name]['idle']
        return self.player_images[player_name][direction][frame % 12]

    def determine_direction(self, player_name, current_position):
        if player_name not in self.previous_positions:
            self.previous_positions[player_name] = current_position
            self.previous_move[player_name] = 'left'
            return 'left'  

        previous_position = self.previous_positions[player_name]
        self.previous_positions[player_name] = current_position

        if current_position[1] < previous_position[1]:
            self.previous_move[player_name] = 'right'
            return 'right'
        elif current_position[1] > previous_position[1]:
            self.previous_move[player_name] = 'left'
            return 'left'
        else:
            return self.previous_move[player_name]

    def draw(self, screen, players, frame_count):
        for player_id, (player_name, player_data) in enumerate(players.items()):
            current_position = player_data['position']
            direction = self.determine_direction(player_name, current_position)
            is_idle = current_position == player_data['goal']
            player_image = self.get_player_image(player_name, direction, frame_count // FRAME_DELAY, is_idle)
            screen.blit(player_image, (current_position[1] * GRID_SIZE + 10, current_position[0] * GRID_SIZE - 1))

            goal_position = player_data['goal']
            pygame.draw.rect(screen, pygame.Color('black'), (goal_position[1] * GRID_SIZE, goal_position[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 3)
