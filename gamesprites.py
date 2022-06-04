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
from support import folder_import, check_group_collisions

class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, img, pos, identif="", origin_point="topleft"):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)
        self.rect_config(pos, origin_point)
        self.id = identif

    def update_rect(self):
        self.rect = self.image.get_rect(center=self.rect.center)

    def rect_config(self, pos, origin_point):
        if origin_point == "topright":
            self.rect = self.image.get_rect(topright=pos)
        elif origin_point == "center":
            self.rect = self.image.get_rect(center=pos)
        elif origin_point == "bottomleft":
            self.rect = self.image.get_rect(bottomleft=pos)
        elif origin_point == "bottomright":
            self.rect = self.image.get_rect(bottomright=pos)

class AnimatedSprite(StaticSprite):
    def __init__(self, img_list, pos, identif="", animation_speed=0.2, origin_point="topleft"):
        self.sprites = img_list
        super().__init__(img_list[0], pos, origin_point=origin_point)
        self.animation_index = 0
        self.animation_speed = animation_speed
        self.id = identif
    
    def animate(self):
        self.animation_index += self.animation_speed
        self.image = self.sprites[int(self.animation_index) % len(self.sprites)]
        self.update_rect()
    
    def update(self):
        self.animate()

class LockAnimation(AnimatedSprite):
    def __init__(self, img_list, pos, animation_speed=0.2, origin_point="topleft"):
        super().__init__(img_list, pos, animation_speed=animation_speed, origin_point=origin_point)
    
    def update(self, opening_condition):
        if opening_condition:
            self.animate()
            if self.animation_index >= len(self.sprites):
                self.kill()


class Ghost(AnimatedSprite):
    def __init__(self, pos, size, moving_pattern, speed, animation_speed=0.2, origin_point="topleft"):
        img_list = folder_import("images/ghost", size)
        identif = HORIZONTAL_GHOST if (UP not in moving_pattern and DOWN not in moving_pattern) else VERTICAL_GHOST
        super().__init__(img_list, pos, identif, animation_speed, origin_point)
        self.move_timer = 0
        self.timer_speed = 0.1
        self.direction = pygame.math.Vector2(0, 0)
        self.timer_limit = 5
        self.all_headings = moving_pattern
        self.heading_index = 0
        self.heading = UP
        self.speed = speed

    def update(self, wall_group):
        self.animate()
        self.move_timer += self.timer_speed
        if self.move_timer > self.timer_limit:
            self.move_timer = 0
            self.get_heading(wall_group)
            self.move()
        else:
            self.direction.x = 0
            self.direction.y = 0
    
    def get_vector(self):
        if self.heading == UP:
            self.direction.y = -self.speed
        elif self.heading == DOWN:
            self.direction.y = self.speed
        elif self.heading == LEFT:
            self.direction.x = -self.speed
        elif self.heading == RIGHT:
            self.direction.x = self.speed
    
    def move(self):
        self.rect.topleft += self.direction

    def get_heading(self, wall_group):
        collision_rect = pygame.Rect(self.rect.left + 2, self.rect.top + 2, self.rect.width - 4, self.rect.height -4)
        self.heading = self.all_headings[self.heading_index % len(self.all_headings)]
        self.get_vector()
        collision_rect.topleft += self.direction
        if check_group_collisions(collision_rect, wall_group):
            self.heading_index += 1
            self.get_heading(wall_group)

class CursorSprite(StaticSprite):
    def __init__(self, img, pos, origin_point="topleft"):
        super().__init__(img, pos, origin_point)
    
    def update(self, pos):
        self.rect.center = pos


        