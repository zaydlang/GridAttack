import os
import pygame
import pygame.font
from pygame.locals import *
import random
import time

pygame.init()

# Constants
board_rows = 15
board_columns = 10
tile_size = 25
buffer_zone = 25
empty_tile_color = (255, 255, 255)
barrier_tile_color = (100, 100, 100)
player_tile_color = (0, 255, 0)
text_color = (255, 255, 255)
button_default_color = (100, 100, 100)
button_hover_color = (50, 50, 50)

barrier_density = 0.15
gen_alpha = 200
menu_columns = 6
button_rows = 2
button_buffer_zone = 10

font = pygame.font.Font("Code New Roman.ttf", tile_size)

# Calculated Constants
game_width = (board_rows + menu_columns) * tile_size + buffer_zone * 3
game_height = board_columns * tile_size + buffer_zone * 3
board_color_dict = {'_': empty_tile_color,
                    'X': barrier_tile_color,
                    'O': player_tile_color}

# Variables
board = [[]]
buttons = []
menu_mode = 0

# Classes
class Button:
    def __init__(self, x, y, width, height, text):
        self.button = pygame.Surface((width, height))
        self.x = x
        self.y = y
        self.hovered = False
        buttons.append(self)
        self.rect = self.button.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text
        self.text_surface = font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center
        
    def draw(self):
        self.check_hovered()
        self.button.fill(self.get_color())
        screen.blit(self.button, (self.x, self.y))
        screen.blit(self.text_surface, self.text_rect)

    def check_hovered(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False
        
    def get_color(self):
        if self.hovered:
            return button_hover_color
        else:
            return button_default_color
        
    
# Generates the game board
def generate_board():
    row_number = 0
    column_number = 0
    total_barriers = 0
    
    while row_number < board_rows:
        board.append([])
        while column_number < board_columns:
            total = row_number * board_rows + column_number
            barrier_ratio = total_barriers / (total) if total != 0 else barrier_density
            
            # This formula's weird. If the barrier ratio is not at the barrier density, I add a value to make
            # the next barrier more or less likely to occur to compensate.
            chance = barrier_density + ((0 if row_number == 0 else 1) * gen_alpha * (barrier_density - barrier_ratio)) / 100
            if chance < 0:
                chance = 0
            if chance > 1:
                chance = 1
                
            if random.uniform(0, 1) > chance:
               board[row_number].append('_')
            else:
               board[row_number].append('X')
               total_barriers = total_barriers + 1
            
            column_number = column_number + 1
            
        row_number = row_number + 1
        column_number = 0
            

# Displays the game board
def draw_board():
    row_number = 0
    column_number = 0

    text_surface = font.render("Board", True, text_color)
    screen.blit(text_surface, (buffer_zone + 6 * tile_size, buffer_zone))
    
    for row in board:
        for tile in row:
            # _ is empty, X is barrier, O is player.
            rectangle = pygame.Surface((tile_size, tile_size))
            rectangle.fill(board_color_dict[tile])
            screen.blit(rectangle, (row_number + buffer_zone, column_number + 2 * buffer_zone))
            
            column_number = column_number + tile_size
            
        row_number = row_number + tile_size
        column_number = 0
            
# Displays the menu
def draw_menu():
    menu = pygame.Surface((tile_size * menu_columns, tile_size * board_columns))
    menu.fill(empty_tile_color)
    screen.blit(menu, (board_rows * tile_size + buffer_zone * 2, buffer_zone * 2))
    buttons.clear()
    
    if menu_mode == 0:
        button_host = Button(board_rows * tile_size + 2 * buffer_zone + button_buffer_zone, buffer_zone * 2 + button_buffer_zone,
                             tile_size * menu_columns - 2 * button_buffer_zone, tile_size * button_rows,
                             "Host")
        button_join = Button(board_rows * tile_size + 2 * buffer_zone + button_buffer_zone, buffer_zone * 2 + button_buffer_zone * 2 + tile_size * button_rows,
                             tile_size * menu_columns - 2 * button_buffer_zone, tile_size * button_rows,
                             "Join")

    elif menu_mode == 1:
        button_host = Button(board_rows * tile_size + 2 * buffer_zone + button_buffer_zone, buffer_zone * 2 + button_buffer_zone,
                             tile_size * menu_columns - 2 * button_buffer_zone, tile_size * button_rows,
                             "Cancel")
                         
                         
'''
    button_join = pygame.Surface((tile_size * menu_columns - 2 * button_buffer_zone, tile_size * button_rows))
    button_join.fill(barrier_tile_color)
    screen.blit(button_join, ((board_rows * tile_size + 2 * buffer_zone + button_buffer_zone, buffer_zone * 2 + button_buffer_zone * 2 + tile_size * button_rows)))

    text_surface = font.render("Join", True, text_color)
    screen.blit(text_surface, (18.9 * tile_size, buffer_zone + 2 * button_buffer_zone + button_rows * tile_size * 1.76))
'''
    
screen = pygame.display.set_mode((game_width, game_height))
game_status = "running"

generate_board()
draw_board()
draw_menu()

while game_status == "running":
    for event in pygame.event.get():
        if pygame.mouse.get_pressed()[0] == 1:
            for button in buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    action = button.text
                    
                    if action == "Host":
                        menu_mode = 1
                    elif action == "Join":
                        menu_mode = 2
                    elif action == "Cancel":
                        menu_mode = 0
                        
                    draw_menu()
                    break

    for button in buttons:
        button.draw()
        
    pygame.display.flip()


