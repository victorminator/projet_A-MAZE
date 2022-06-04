import os
import pygame.transform
import pygame.image
import pygame.surface
import pygame.mixer
from settings import ID_PAIRS

def list_folders(path):
    content = os.listdir(path)
    return [folder for folder in content if os.path.isdir(path + "/" + folder)]

def folder_import(path, dimensions=0, object_type="image"):
    objets = []
    for nom_fichier in os.listdir(path):
        if object_type == "image":    
            new_object = auto_square_resize(pygame.image.load(path + "/" + nom_fichier), dimensions).convert_alpha() if dimensions > 0 else pygame.image.load(path + "/" + nom_fichier).convert_alpha()
        else:
            new_object = pygame.mixer.Sound(path + "/" + nom_fichier)
        objets.append(new_object)
    return objets

def difference(a, b):
    return abs(a - b)

def nb_plus_proche(n_origine, *args):
    plus_proche = None
    diff_plus_courte = None
    for n in args:
        if plus_proche != None:
            diff = difference(n_origine, n)
            if diff < diff_plus_courte:
                diff_plus_courte = diff
                plus_proche = n
        else:
            plus_proche = n 
            diff_plus_courte = difference(n_origine, n)
    return plus_proche

def mutliple_plus_proche(n: int, source_multiple: int) -> int:
    if n % source_multiple == 0: return n
    premier_mutltiple = source_multiple * int(n/source_multiple)
    second_mulitple = premier_mutltiple + source_multiple
    return nb_plus_proche(n, premier_mutltiple, second_mulitple)


def simple_sprites_collision(sprite_1, sprite_2, kill_1=False, kill_2=False):
    if sprite_1.rect.colliderect(sprite_2.rect):
        if kill_1: sprite_1.kill()
        if kill_2: sprite_2.kill()
        return True
    return False

def check_group_collisions(rect_object, group):
    for sprite in group.sprites():
        if sprite.rect.colliderect(rect_object): return True
    return False

def ajuste_n(n, x_min, x_max):
    if n > x_max:
        return x_max
    if n < x_min:
        return x_min
    return n

def list2d(row_quantity: int, column_quantity: int, fillchar="_") -> list:
    bidimensional_list = []
    for _ in range(row_quantity):
        row = [fillchar for _ in range(column_quantity)]
        bidimensional_list.append(row)
    return bidimensional_list

def auto_square_resize(img_obj, dimensions):
    return pygame.transform.scale(img_obj, (dimensions, dimensions)).convert_alpha()
    

def get_dimensions(display_width, display_height, len_x, len_y):
    if len_x > len_y:
        width = mutliple_plus_proche(display_width, len_x)
        sprite_size = int(width / len_x)
        height = sprite_size * len_y
    else:
        height = mutliple_plus_proche(display_height, len_y)
        sprite_size = int(height / len_y)
        width = len_x * sprite_size
    return width, height, sprite_size

def get_image(sprite_identifier):
    return pygame.image.load(ID_PAIRS[sprite_identifier]).convert_alpha()

def has_common_elements(big_ls, small_ls, elements_number):
    found = 0
    excluded = []
    for ls in big_ls:
        for elt in small_ls:
            if elt in ls and elt not in excluded:
                found += 1
                excluded.append(elt)
                if found == elements_number:
                    return excluded
    return []

if __name__ == "__main__":
    with open("test.mznv") as fic:
        print(fic.read())
