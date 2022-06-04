

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

BASIC = "b"
DIZZY = "d"
SAD = "s"
MAD = "m"
FROWN = "f"
DOOR = "G"
KEY = "K"

GREEN_BLOCK = "X"
RED_BLOCK = "1"
BLUE_BLOCK = "2"
YELLOW_BLOCK = "3"
PURPLE_BLOCK = "4"
BLACK_BLOCK = "5"
GRAY_BLOCK = "6"
BROWN_BLOCK = "7"

YELLOW_ROUTE = "_"
RED_ROUTE = "+"
GREEN_ROUTE = "-"
BLACK_ROUTE = "*"
GRAY_ROUTE = "%"
PURPLE_ROUTE = "/"
BLUE_ROUTE = "="
BROWN_ROUTE = "."

HORIZONTAL_GHOST = "H"
VERTICAL_GHOST = "V"

BLUE_PLAYER_IMG = "images/player_cublets/Fred.png"
GREEN_PLAYER_IMG = "images/player_cublets/Joshy.png"
ORANGE_PLAYER_IMG = "images/player_cublets/Mr.Max_.png"
BROWN_PLAYER_IMG = "images/player_cublets/Liam.png"
RED_PLAYER_IMG = "images/player_cublets/Evil.Doc_.png"

GREEN_BLOCK_IMG = "images/blocks/Block_Type2_Green.png"
BLACK_BLOCK_IMG = "images/blocks/Block_Type2_Black.png"
BROWN_BLOCK_IMG = "images/blocks/Block_Type2_Brown.png"
BLUE_BLOCK_IMG = "images/blocks/Block_Type2_Blue.png"
GRAY_BLOCK_IMG = "images/blocks/Block_Type2_Gray.png"
PURPLE_BLOCK_IMG = "images/blocks/Block_Type2_Purple.png"
RED_BLOCK_IMG = "images/blocks/Block_Type2_Red.png"
YELLOW_BLOCK_IMG = "images/blocks/Block_Type2_Yellow.png"

YELLOW_ROUTE_IMG = "images/walkable_tiles/Tile_Yellow.png"
GREEN_ROUTE_IMG = "images/walkable_tiles/Tile_Green.png"
RED_ROUTE_IMG = "images/walkable_tiles/Tile_Red.png"
PURPLE_ROUTE_IMG = "images/walkable_tiles/Tile_Purple.png"
GRAY_ROUTE_IMG = "images/walkable_tiles/Tile_Gray.png"
BLACK_ROUT_IMG = "images/walkable_tiles/Tile_Black.png"
BLUE_ROUTE_IMG = "images/walkable_tiles/Tile_Blue.png"
BROWN_ROUTE_IMG = "images/walkable_tiles/Tile_Brown.png"

DOOR_IMG = "images/divers/door.png"
KEY_IMG = "images/key/key0.png"
HORIZONTAL_GHOST_IMG = "images/divers/ghost_horizontal.png"
VERTICAL_GHOST_IMG = "images/divers/ghost_vertical.png"

ID_PAIRS = {BASIC:BLUE_PLAYER_IMG, 
            DIZZY:GREEN_PLAYER_IMG, 
            SAD:ORANGE_PLAYER_IMG,
            MAD:RED_PLAYER_IMG,
            FROWN:BROWN_PLAYER_IMG,
            KEY:KEY_IMG,
            DOOR:DOOR_IMG,
            HORIZONTAL_GHOST:HORIZONTAL_GHOST_IMG,
            VERTICAL_GHOST:VERTICAL_GHOST_IMG,
            YELLOW_BLOCK:YELLOW_BLOCK_IMG,
            RED_BLOCK:RED_BLOCK_IMG,
            BLACK_BLOCK:BLACK_BLOCK_IMG,
            BROWN_BLOCK:BROWN_BLOCK_IMG,
            GREEN_BLOCK:GREEN_BLOCK_IMG,
            BLUE_BLOCK:BLUE_BLOCK_IMG,
            PURPLE_BLOCK:PURPLE_BLOCK_IMG,
            GRAY_BLOCK:GRAY_BLOCK_IMG,
            YELLOW_ROUTE:YELLOW_ROUTE_IMG,
            RED_ROUTE:RED_ROUTE_IMG,
            BLACK_ROUTE:BLACK_ROUT_IMG,
            GRAY_ROUTE:GRAY_ROUTE_IMG,
            PURPLE_ROUTE:PURPLE_ROUTE_IMG,
            BLUE_ROUTE:BLUE_ROUTE_IMG,
            GREEN_ROUTE:GREEN_ROUTE_IMG,
            BROWN_ROUTE:BROWN_ROUTE_IMG
            }

BLOCKS = [GREEN_BLOCK, YELLOW_BLOCK, BLACK_BLOCK, BLUE_BLOCK, PURPLE_BLOCK, GRAY_BLOCK, BROWN_BLOCK, RED_BLOCK]
ROUTES = [GREEN_ROUTE, YELLOW_ROUTE, BLACK_ROUTE, BLUE_ROUTE, PURPLE_ROUTE, GRAY_ROUTE, BROWN_ROUTE, RED_ROUTE]
PLAYER_LETTERS = [BASIC, DIZZY, SAD, MAD, FROWN]
GHOSTS = [HORIZONTAL_GHOST, VERTICAL_GHOST]
MULTIPLE_STYLES = [BLOCKS, ROUTES, PLAYER_LETTERS, GHOSTS]


UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

EDITOR_WIDTH_INITIAL = 1000
EDITOR_HEIGHT_INITIAL = 700

MENU_BAR_HEIGHT = EDITOR_HEIGHT_INITIAL // 7
EDITOR_PADDING = 40
EDITOR_MAX_LEN = 48
EDITOR_MIN_LEN = 8

LEVEL_FILES_EXTENSION = "mznv"

TK_GUI_DIMENSIONS = (400, 150)

LEVEL_BOARD_DIMENSIONS = (EDITOR_WIDTH_INITIAL - EDITOR_PADDING * 2, EDITOR_HEIGHT_INITIAL - MENU_BAR_HEIGHT)

MIN_DEFAULT_SIZE = 0

ALT_SIZE = 64
ECART_X = EDITOR_WIDTH_INITIAL - ALT_SIZE * 1.5
ECART_Y = ALT_SIZE * 2
