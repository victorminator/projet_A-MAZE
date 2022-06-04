from random import choice
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
import pygame.math
from settings import *
from gamesprites import StaticSprite
from support import auto_square_resize, check_group_collisions, folder_import


class PlayerConstructor(StaticSprite):
    def __init__(self, img, size, splats_images, pos, identif, transition_length=6, origin_point="topleft"):
        self.size = size
        updated_img = auto_square_resize(img, size - 1)
        super().__init__(updated_img, pos, identif, origin_point)
        self.direction = pygame.math.Vector2(0, 0)
        self.key_lock = False
        self.transition_length = transition_length
        self.smart_speedcut()
        self.initial_position = pos
        self.splat_images = splats_images
        self.splats = pygame.sprite.Group()
        self.wall_vulnerable = False
        self.movement_transition_index = 0
        self.recursion_movement = False
        self.recursion_index = 0
        self.has_moved = False
        self.splosh_sounds = folder_import("sounds/impsplats", object_type="sound")
    
    def reverse_speed(self):
        self.quotient_speed *= -1

    def smart_speedcut(self):
        self.quotient_speed = self.size // self.transition_length
        self.remaining_speed = self.size % self.transition_length

    def fill_move(self, wall_group, n):
        for _ in range(n):
            if self.direction.x < 0:
                self.move(wall_group, -self.remaining_speed, 0)
            elif self.direction.x > 0:
                self.move(wall_group, self.remaining_speed, 0)
            elif self.direction.y > 0:
                self.move(wall_group, 0, self.remaining_speed)
            elif self.direction.y < 0:
                self.move(wall_group, 0, -self.remaining_speed)
    
    def get_input(self, wall_group):
        touches = pygame.key.get_pressed()
        if touches[pygame.K_UP] and not self.key_lock:
            self.direction.y = -self.quotient_speed
        elif touches[pygame.K_DOWN] and not self.key_lock:
            self.direction.y = self.quotient_speed
        elif touches[pygame.K_LEFT] and not self.key_lock:
            self.direction.x = -self.quotient_speed
        elif touches[pygame.K_RIGHT] and not self.key_lock:
            self.direction.x = self.quotient_speed
        elif self.movement_transition_index % self.transition_length == 0:
            if self.recursion_movement:
                fill_quantity = self.movement_transition_index
            elif self.has_moved:
                fill_quantity = 1
            else:
                fill_quantity = 0
            self.fill_move(wall_group, fill_quantity)
            self.direction.x = 0
            self.direction.y = 0
            self.movement_transition_index = 0
            self.recursion_index = 0
        self.key_lock = 1 in touches or self.movement_transition_index != 0
    
    def may_move(self, wall_group, coordinates):
        collision_rect = pygame.Rect(coordinates[0], coordinates[1], self.rect.width, self.rect.height)
        for tile in wall_group.sprites():
            if collision_rect.colliderect(tile.rect):
                if self.wall_vulnerable: self.splash()
                return False
        return True

    def reset_position(self):
        self.direction.x = 0
        self.direction.y = 0
        self.movement_transition_index = 0
        self.recursion_index = 0
        self.rect.topleft = self.initial_position

    def splash(self):
        random_splash = choice(self.splat_images)
        splash_sprite = StaticSprite(random_splash, self.rect.topleft)
        self.splats.add(splash_sprite)
        for player_characters in self.groups()[0]:
            player_characters.reset_position()
        choice(self.splosh_sounds).play()

    def get_sploshed(self, hazard_group):
        return check_group_collisions(self.rect, hazard_group)
    
    def get_recursion_index(self, wall_group):
        if self.direction.x != 0 or self.direction.y != 0:
            safety_coordinates = (self.rect.x + self.direction.x * (self.recursion_index + 1), self.rect.y + self.direction.y * (self.recursion_index + 1))
            if self.may_move(wall_group, safety_coordinates):
                self.recursion_index += 1
                self.transition_length = self.recursion_index
                self.get_recursion_index(wall_group)

    def move(self, wall_group, x, y):
        if self.direction.x != 0 or self.direction.y != 0:
            safety_coordinates = (self.rect.x + x, self.rect.y + y)
            if self.may_move(wall_group, safety_coordinates):
                self.rect.x += x
                self.rect.y += y 
                self.has_moved = True
            else:
                self.has_moved = False       

    def update(self, wall_group, hazard_group):
        self.get_input(wall_group)
        if self.recursion_movement and self.recursion_index == 0:
            self.get_recursion_index(wall_group)
        self.move(wall_group, self.direction.x, self.direction.y)
        if self.get_sploshed(hazard_group) or (self.wall_vulnerable and self.get_sploshed(wall_group)):
            self.splash()
        if self.direction.x != 0 or self.direction.y != 0:
            self.movement_transition_index += 1

class BasicPlayer(PlayerConstructor):
    def __init__(self, size, pos=(0, 0), origin_point="topleft", trans_length=6):
        img = pygame.image.load(BLUE_PLAYER_IMG).convert_alpha()
        splats = folder_import("images/splats_cyan", size)
        super().__init__(img, size, splats, pos, BASIC, trans_length, origin_point)

class DizzyPlayer(PlayerConstructor):
    def __init__(self, size, pos=(0, 0), origin_point="topleft", trans_length=6):
        img = pygame.image.load(GREEN_PLAYER_IMG).convert_alpha()
        splats = folder_import("images/splats_lightgreen", size)
        super().__init__(img, size,splats, pos, DIZZY, trans_length, origin_point)
        self.reverse_speed()

class SadPlayer(PlayerConstructor):
    def __init__(self, size, pos=(0, 0), origin_point="topleft", trans_length=6):
        img = pygame.image.load(ORANGE_PLAYER_IMG).convert_alpha()
        splats_images = folder_import("images/splats_orange", size)
        super().__init__(img, size,splats_images, pos, SAD, trans_length, origin_point)
        self.wall_vulnerable = True

class MadPlayer(PlayerConstructor):
    def __init__(self, size, pos=(0, 0), origin_point="topleft", trans_length=6):
        img = pygame.image.load(RED_PLAYER_IMG).convert_alpha()
        splats_images = folder_import("images/splats_red", size)
        super().__init__(img, size,splats_images, pos, MAD, trans_length, origin_point)
        self.wall_vulnerable = True
        self.reverse_speed()

class FrowningPlayer(PlayerConstructor):
    def __init__(self, size, pos=(0, 0), origin_point="topleft", transition_length=2):
        img = pygame.image.load(BROWN_PLAYER_IMG).convert_alpha()
        splats_images = folder_import("images/splats_brown", size)
        super().__init__(img, size, splats_images, pos, FROWN, transition_length, origin_point)
        self.recursion_movement = True