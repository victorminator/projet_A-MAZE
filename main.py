import pygame
import pygame.key
import pygame.event
import pygame.font
import pygame.surface
import pygame.image
import pygame.display
import pygame.time
import pygame.rect
import pygame.sprite
import pygame.mixer
import sys

from settings import *
from game_data import get_levels

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A-Maze")
game_icon = pygame.image.load("images/divers/Fred_ico.ico").convert_alpha()
pygame.display.set_icon(game_icon)
clock = pygame.time.Clock()
playing = True
endgame = False
final_sound_occured = False
game_levels = get_levels("levels", screen)

current_level = 0
bg = pygame.image.load("images/divers/game_bg.png").convert_alpha()

game_music = pygame.mixer.Sound("sounds/Caketown 1.mp3")
game_music.play(-1)

while current_level < len(game_levels):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(bg, (0, 0))
    game_levels[current_level].run()
    if game_levels[current_level].reached_goal():
        current_level += 1
        if current_level < len(game_levels):
            for plyer in game_levels[current_level].player_container.sprites():
                plyer.key_lock = True
    pygame.display.update()
    clock.tick(60)