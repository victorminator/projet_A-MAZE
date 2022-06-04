import pygame
import pygame.key
import pygame.event
import pygame.font
import pygame.surface
import pygame.image
import pygame.time
import pygame.rect
import pygame.sprite
import pygame.mixer
import pygame.mouse
import pygame.display
import pygame.transform
import sys
import gui_editor
from gamesprites import CursorSprite, StaticSprite, AnimatedSprite
from settings import *
from support import folder_import, list2d, auto_square_resize, get_dimensions, get_image, has_common_elements

def get_foot_index(x_pos, length, item_quantity):
    divisor = length / item_quantity
    return int(x_pos // divisor)

def foot_config():
    for i, identifier in enumerate(buildmenu_display):
        img = get_image(identifier)
        pos_x = i * (EDITOR_WIDTH_INITIAL / len(buildmenu_display)) + EDITOR_PADDING + 3
        pos_y = EDITOR_HEIGHT_INITIAL - MENU_BAR_HEIGHT / 4
        display_sprite = StaticSprite(img, (pos_x, pos_y), origin_point="bottomleft")
        build_sprites.add(display_sprite)

def group_collidepoint(x, y, group: pygame.sprite.Group):
    for sprt in group.sprites():
        if sprt.rect.collidepoint(x, y):
            return True
    return False

def find_sprite(spot: tuple, group: pygame.sprite.Group):
    for spt in group.sprites():
        if spt.rect.topleft == spot:
            return spt

def update_representation(info):
    level_representation[info[0]][info[1]] = info[2]

def place_sprite(sprite_info, save=False):
    img_object, column, row, sprite_identifier = sprite_info
    pos = (tile_dimensions * column + level_board_rect.left, tile_dimensions * row + level_board_rect.top)
    sprite_object = StaticSprite(img_object[0], pos, img_object[1])
    found = find_sprite(pos, level_sprites)
    found.kill()
    if save and sprite_object.id != found.id:   
        moves.append({place_sprite:[(found.image, found.id), column, row, level_representation[row][column]]})
    level_sprites.add(sprite_object)
    update_representation((row, column, sprite_identifier))

def switch_all(source_dest, save=False):
    selected_sprite.image = get_image(source_dest[1])
    buildmenu_display[indice] = source_dest[1]
    for y in range(y_len):
        for x in range(x_len):
            if level_representation[y][x] in source_dest[0]:
                symbol = level_representation[y][x]
                img = auto_square_resize(get_image(source_dest[1]), tile_dimensions)
                place_sprite([(img, source_dest[1]), x, y, source_dest[1]], save=False)
    if save:
        moves.append({switch_all:[source_dest[0], symbol]})

def fill_level():
    for y in range(y_len):
        for x in range(x_len):
            if len(level_content) == 1:    
                img = pygame.image.load("images/divers/wall_block.png").convert_alpha()
                identif = GREEN_BLOCK
            else:
                img = get_image(level_content[y][x])
                identif = level_content[y][x]
                update_representation((y, x, level_content[y][x]))
            resized_img = auto_square_resize(img, tile_dimensions)
            x_pos = level_board_rect.left + x * tile_dimensions
            y_pos = level_board_rect.top + y * tile_dimensions
            level_sprite = StaticSprite(resized_img, (x_pos, y_pos), identif)
            level_sprites.add(level_sprite)

def get_alt_index(x, y):
    return int(int(x > EDITOR_WIDTH_INITIAL // 2) + 2 * (y // ECART_Y))

def display_alternatives(alternatives):
    for i in range(len(alternatives)):
        img = auto_square_resize(get_image(alternatives[i]), ALT_SIZE)
        pos_x = ALT_SIZE * 0.5 if i % 2 == 0 else ECART_X
        pos_y = EDITOR_PADDING + ECART_Y * (i // 2)
        alt_sprite = StaticSprite(img, (pos_x, pos_y))
        alternatives_group.add(alt_sprite)

def data_formatting(data):
    formatted = ""
    for row in data:
        for col in row:
            formatted += col
        formatted += "\n"
    return formatted[:-1]

def save_file(filepath, content):
    with open(filepath, mode="w") as fic:
        fic.write(content)

def find_alternative(indice_alt):
    for id_group in MULTIPLE_STYLES:
        if buildmenu_display[indice_alt] in id_group:
            display_alternatives(id_group)
            return id_group
    return []

def undo():
    if len(moves) > 0:
        last_move = moves.pop(-1)
        process = list(last_move.keys())[0]
        arguments = last_move[process]
        process(arguments)

working_file = gui_editor.configuration_interface()
if working_file == -1:
    sys.exit()

with open(working_file) as level_file:
    level_content = level_file.readlines()
if len(level_content) == 1:
    x_len, y_len = map(int, level_content[0].split(" "))
else:
    x_len = len(level_content[-1])
    y_len = len(level_content)

pygame.init()

buildmenu_display = [GREEN_BLOCK, YELLOW_ROUTE, BASIC, DOOR, KEY, HORIZONTAL_GHOST]
editor_width, editor_height, tile_dimensions = get_dimensions(LEVEL_BOARD_DIMENSIONS[1], LEVEL_BOARD_DIMENSIONS[1], x_len, y_len)

editor_screen = pygame.display.set_mode((EDITOR_WIDTH_INITIAL, EDITOR_HEIGHT_INITIAL))
editor_clock = pygame.time.Clock()

footmenu = pygame.surface.Surface((EDITOR_WIDTH_INITIAL, MENU_BAR_HEIGHT))
footmenu.fill((255, 255, 255))


level_board = pygame.surface.Surface((editor_width, editor_height))
level_board_rect = level_board.get_rect(center=(EDITOR_WIDTH_INITIAL // 2, EDITOR_HEIGHT_INITIAL // 2 - EDITOR_PADDING))
level_board.fill((230, 225, 77))

build_sprites = pygame.sprite.Group()
selection_rectangle = pygame.sprite.GroupSingle()

pointer_img = folder_import("images/Pointer")
pointer_sprite = AnimatedSprite(pointer_img, (0, 0), animation_speed=0.3)
pointer_group = pygame.sprite.GroupSingle(pointer_sprite)

currently_running = True
current_item_key = ""
indice_precedent = -1
selection = False

current_file = ""
level_sprites = pygame.sprite.Group()
#cursor_image = pygame.sprite.GroupSingle()
alternatives_group = pygame.sprite.Group()

level_representation = list2d(y_len, x_len, fillchar="X")
selected_alternatives = []
selected_sprite = None
moves = []
stopped_placing = True
fill_level()

block_type = has_common_elements(level_representation, BLOCKS, 1)
buildmenu_display[0] = block_type[0]
walk_type = has_common_elements(level_representation, ROUTES, 1)
buildmenu_display[1] = walk_type[0]
foot_config()

while currently_running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pressed_keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            a = data_formatting(level_representation)
            save_file(working_file, a)
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_y >= EDITOR_HEIGHT_INITIAL - MENU_BAR_HEIGHT:
                for sprite in build_sprites.sprites():
                    if sprite.rect.collidepoint(mouse_x, mouse_y):
                        alternatives_group.empty()
                        indice = get_foot_index(mouse_x, EDITOR_WIDTH_INITIAL, len(buildmenu_display))
                        selection = indice_precedent != indice or indice_precedent == -1
                        if selection:
                            pointer_sprite.rect.center = (sprite.rect.centerx, sprite.rect.top - 20)
                            indice_precedent = indice
                            selected_alternatives = find_alternative(indice)
                            selected_sprite = sprite
                        else:
                            indice_precedent = -1
                            selected_alternatives.clear()
                            alternatives_group.empty()
            else:
                for alt_sprite in alternatives_group.sprites():
                    if alt_sprite.rect.collidepoint(mouse_x, mouse_y):
                        indice_sprite = get_alt_index(mouse_x, mouse_y)
                        if selected_alternatives == ROUTES and has_common_elements(level_representation, ROUTES, 1):
                            switch_all([ROUTES, selected_alternatives[indice_sprite]], save=True)
                        elif selected_alternatives == BLOCKS and has_common_elements(level_representation, BLOCKS, 1):
                            switch_all([BLOCKS, selected_alternatives[indice_sprite]], save=True)
                        else:
                            selected_sprite.image = get_image(selected_alternatives[indice_sprite])
                            buildmenu_display[indice] = selected_alternatives[indice_sprite]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                a = data_formatting(level_representation)
                save_file(working_file, a)
                pygame.quit()
                sys.exit()
            if pressed_keys[pygame.K_LCTRL]:
                if event.key == pygame.K_z:
                    undo()
    if selection and level_board_rect.collidepoint(mouse_x, mouse_y):
        left_click = pygame.mouse.get_pressed()[0]
        if left_click:
            x_column = (mouse_x - level_board_rect.left) // tile_dimensions
            y_row = (mouse_y - level_board_rect.top) // tile_dimensions
            img_to_place = auto_square_resize(get_image(buildmenu_display[indice]), tile_dimensions) 
            place_sprite([(img_to_place, buildmenu_display[indice]), x_column, y_row, buildmenu_display[indice]], save=True)
    editor_screen.fill((181, 0, 205))
    editor_screen.blit(level_board, level_board_rect)
    level_sprites.draw(editor_screen)
    editor_screen.blit(footmenu, (0, EDITOR_HEIGHT_INITIAL - MENU_BAR_HEIGHT))
    build_sprites.draw(editor_screen)
    alternatives_group.draw(editor_screen)
    if selection:
        pointer_group.draw(editor_screen)
        pointer_group.update()
    pygame.display.update()
    editor_clock.tick(60)