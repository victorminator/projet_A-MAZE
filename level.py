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
from gamesprites import *
from player import BasicPlayer, DizzyPlayer, FrowningPlayer, MadPlayer, SadPlayer
from settings import *
from support import auto_square_resize, folder_import, get_image, simple_sprites_collision, get_dimensions

class Level:
    def __init__(self, display_surface, level_data):
        self.display_surface = display_surface
        self.width, self.height, self.tile_dimensions = get_dimensions(SCREEN_WIDTH - 50, SCREEN_HEIGHT, len(level_data[0]), len(level_data))
        self.set_origin_point()
        self.player_container = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        self.walk_path = pygame.sprite.Group()
        self.goal = pygame.sprite.GroupSingle()
        self.key = pygame.sprite.Group()
        self.lock = pygame.sprite.GroupSingle()
        self.ghosts = pygame.sprite.Group()
        self.keys = {}
        self.key_sf = pygame.mixer.Sound("sounds/pick_key.wav")
        self.simple_map_setup(level_data)
        self.lock_config()

    def set_origin_point(self):
        x = SCREEN_WIDTH // 2 - self.width // 2
        y = SCREEN_HEIGHT // 2 - self.height // 2
        self.origin = (x, y)

    def find_route_color(self, level):
        for row in level:
            for col in row:
                if col in ROUTES:
                    return col
        return "_"

    def simple_map_setup(self, level):
        used_routes = self.find_route_color(level)
        for row_index, row in enumerate(level):
            for col_index, column in enumerate(row):
                tile_pos = (self.origin[0] + self.tile_dimensions * col_index, self.origin[1] + self.tile_dimensions * row_index)
                if column not in BLOCKS:
                    img = auto_square_resize(get_image(used_routes), self.tile_dimensions)
                    path_sprite = StaticSprite(img, tile_pos, YELLOW_ROUTE)
                    self.walk_path.add(path_sprite)
                    if column in PLAYER_LETTERS:
                        if column == PLAYER_LETTERS[0]:     
                            player = BasicPlayer(self.tile_dimensions, (tile_pos[0] + 1, tile_pos[1] + 1))
                        elif column == PLAYER_LETTERS[1]:
                            player = DizzyPlayer(self.tile_dimensions, (tile_pos[0] + 1,tile_pos[1] + 1))
                        elif column == PLAYER_LETTERS[2]:
                            player = SadPlayer(self.tile_dimensions, (tile_pos[0] + 1,tile_pos[1] + 1))
                        elif column == PLAYER_LETTERS[3]:
                            player = MadPlayer(self.tile_dimensions, (tile_pos[0] + 1,tile_pos[1] + 1))
                        else:
                            player = FrowningPlayer(self.tile_dimensions, (tile_pos[0] + 1,tile_pos[1] + 1))
                        self.player_container.add(player)
                    elif column == DOOR:
                        goal_img = auto_square_resize(pygame.image.load(DOOR_IMG).convert_alpha(), self.tile_dimensions)
                        goal = StaticSprite(goal_img, tile_pos, column)
                        self.goal.add(goal)
                    elif column == KEY:
                        key_img = folder_import("images/key", self.tile_dimensions)
                        key_sprite = AnimatedSprite(key_img, tile_pos, column)
                        self.keys[key_sprite] = key_sprite.rect.topleft
                        self.key.add(key_sprite)
                    elif column == "V" or column == "H":
                        movement_definition = [LEFT, RIGHT] if column == "H" else [UP, DOWN]
                        ghost_sprite = Ghost(tile_pos, self.tile_dimensions, movement_definition, self.tile_dimensions)
                        self.ghosts.add(ghost_sprite)
                else:
                    wall_img = auto_square_resize(get_image(column), self.tile_dimensions)
                    wall_sprite = StaticSprite(wall_img, tile_pos, GREEN_BLOCK)
                    self.tiles.add(wall_sprite)

    def reached_goal(self):
        if len(self.lock) == 0:    
            for sprite_character in self.player_container.sprites():
                if simple_sprites_collision(sprite_character, self.goal.sprite, kill_1=True):
                    return True
        return False

    def collected_key(self):
        if len(self.key) > 0:
            for sprite_character in self.player_container.sprites():
                for key_sprt in self.keys:
                    if simple_sprites_collision(sprite_character, key_sprt, kill_2=True):
                        sprite_character.initial_position = self.keys[key_sprt]
                        self.key_sf.play()
        return len(self.key) == 0

    def lock_config(self):
        if len(self.key) > 0:
            lock_img = folder_import("images/lock", self.tile_dimensions)   
            lock_sprite = LockAnimation(lock_img, (self.goal.sprite.rect.x, self.goal.sprite.rect.y))
            self.lock.add(lock_sprite)
    
    def run(self):
        self.tiles.draw(self.display_surface)
        self.walk_path.draw(self.display_surface)
        for cube_character in self.player_container.sprites():
            cube_character.splats.draw(self.display_surface)
        self.goal.draw(self.display_surface)
        self.lock.draw(self.display_surface)
        self.lock.update(self.collected_key())
        self.key.draw(self.display_surface)
        self.key.update()
        self.ghosts.draw(self.display_surface)
        self.ghosts.update(self.tiles)
        self.player_container.draw(self.display_surface)
        self.player_container.update(self.tiles, self.ghosts)


