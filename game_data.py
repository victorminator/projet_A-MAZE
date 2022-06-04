"""
X = wall
_ = route
G = door
K = key
H = horizontal ghost
V = vertical ghost
b = personnage basique (aucune caractéristique spéciale)
s = personnage triste (vulnérable aux murs)
d = personnage confus (déplacement inversé)
m = personnage diabolique (déplacement inversé + vulnérable aux murs)
f = personnage fonceur (déplacement récursif)
"""

import os
from level import Level

def read_data(filepath):
    with open(filepath) as fic:
        lv_data = [[]]
        for char in fic.read():
            if char == "\n":
                lv_data.append([])
            else:
                lv_data[-1].append(char)
    return lv_data

def get_levels(folderpath, display_surface):
    files = os.listdir(folderpath)
    levels = []
    for filename in files:
        level_content = read_data(folderpath + "/" + filename)
        levels.append(Level(display_surface, level_content))
    return levels