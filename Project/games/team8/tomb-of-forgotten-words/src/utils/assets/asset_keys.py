"""
This file contains constant key for the sprite images and the audio assets to prevent typos.

The key name are the file names without the corresponding file ending.
    - "*.png" - For the Sprite Images
    - "*.ogg" - For the Audio Files
"""

###############################################################################################################
# Sprites
###############################################################################################################
SPRITE_SPIDER: str = "spider"  # TODO: PLACEHOLDER REPLACE
SPRITE_COBWEB: str = "cobweb"  # TODO: PLACEHOLDER REPLACE
SPRITE_EXPLOSION: str = "explosion"
SPRITE_MAP_BACKGROUND: str = "map"
SPRITE_SPAWN_MARKER: str = "spawn"
SPRITE_SPLASH_SCREEN: str = "splash-screen"


###############################################################################################################
# Sprites sheets
###############################################################################################################
SPRITESHEET_PLAYER: str = "player"
SPRITESHEET_TILES: str = "map-tile"
SPRITESHEET_WEAPONS: str = "weapons"
SPRITESHEET_GOLEM: str = "stone-golem"
SPRITESHEET_MUMMY: str = "mummy"
SPRITESHEET_INVENTORY_SLOT: str = "inventory-tiles"


###############################################################################################################
# Sprites sheet values
###############################################################################################################
FACING_FRONT: int = 0
FACING_BACK: int = 1
FACING_RIGHT: int = 2
FACING_LEFT: int = 3
FACING: list[int] = [FACING_FRONT, FACING_BACK, FACING_RIGHT, FACING_LEFT]

PLAYER_FRONT_STILL: int = 1
PLAYER_BACK_STILL: int = 4
PLAYER_RIGHT_STILL: int = 7
PLAYER_LEFT_STILL: int = 10

PLAYER_WALK_FRONT: list[int] = [0, 1, 2, 1]
PLAYER_WALK_BACK: list[int] = [3, 4, 5, 4]
PLAYER_WALK_RIGHT: list[int] = [6, 7, 8, 7]
PLAYER_WALK_LEFT: list[int] = [9, 10, 11, 10]

PLAYER_STILL: dict[int, int] = {
    FACING_FRONT: PLAYER_FRONT_STILL,
    FACING_BACK: PLAYER_BACK_STILL,
    FACING_RIGHT: PLAYER_RIGHT_STILL,
    FACING_LEFT: PLAYER_LEFT_STILL,
}

PLAYER_WALK: dict[int, list[int]] = {
    FACING_FRONT: PLAYER_WALK_FRONT,
    FACING_BACK: PLAYER_WALK_BACK,
    FACING_RIGHT: PLAYER_WALK_RIGHT,
    FACING_LEFT: PLAYER_WALK_LEFT,
}

GOLEM_STILL_FRONT: int = 1
GOLEM_STILL_BACK: int = 4
GOLEM_STILL_RIGHT: int = 7
GOLEM_STILL_LEFT: int = 10

GOLEM_WALK_FRONT: list[int] = [0, 1, 2, 1]
GOLEM_WALK_BACK: list[int] = [3, 4, 5, 4]
GOLEM_WALK_RIGHT: list[int] = [6, 7, 8, 7]
GOLEM_WALK_LEFT: list[int] = [9, 10, 11, 10]

GOLEM_STILL: dict[int, int] = {
    FACING_FRONT: GOLEM_STILL_FRONT,
    FACING_BACK: GOLEM_STILL_BACK,
    FACING_RIGHT: GOLEM_STILL_RIGHT,
    FACING_LEFT: GOLEM_STILL_LEFT,
}

GOLEM_WALK: dict[int, list[int]] = {
    FACING_FRONT: GOLEM_WALK_FRONT,
    FACING_BACK: GOLEM_WALK_BACK,
    FACING_RIGHT: GOLEM_WALK_RIGHT,
    FACING_LEFT: GOLEM_WALK_LEFT,
}

MUMMY_STILL_FRONT: int = 1
MUMMY_STILL_BACK: int = 4
MUMMY_STILL_RIGHT: int = 7
MUMMY_STILL_LEFT: int = 10

MUMMY_WALK_FRONT: list[int] = [0, 1, 2, 1]
MUMMY_WALK_BACK: list[int] = [3, 4, 5, 4]
MUMMY_WALK_RIGHT: list[int] = [6, 7, 8, 7]
MUMMY_WALK_LEFT: list[int] = [9, 10, 11, 10]

MUMMY_STILL: dict[int, int] = {
    FACING_FRONT: MUMMY_STILL_FRONT,
    FACING_BACK: MUMMY_STILL_BACK,
    FACING_RIGHT: MUMMY_STILL_RIGHT,
    FACING_LEFT: MUMMY_STILL_LEFT,
}

MUMMY_WALK: dict[int, list[int]] = {
    FACING_FRONT: MUMMY_WALK_FRONT,
    FACING_BACK: MUMMY_WALK_BACK,
    FACING_RIGHT: MUMMY_WALK_RIGHT,
    FACING_LEFT: MUMMY_WALK_LEFT,
}

PLAYER: int = 0
GOLEM: int = 1
MUMMY: int = 2
SPIDER: int = 3

STILLS: dict[int, dict[int, int]] = {
    PLAYER: PLAYER_STILL,
    GOLEM: GOLEM_STILL,
    MUMMY: MUMMY_STILL,
    # SPIDER: SPIDER_STILL
}

WALKS: dict[int, dict[int, list[int]]] = {PLAYER: PLAYER_WALK, GOLEM: GOLEM_WALK, MUMMY: MUMMY_WALK}


WEAPON_SHOTGUN: int = 0
WEAPON_REVOLVER: int = 1
WEAPON_MACHINE_GUN: int = 2
WEAPON_GRENADE: int = 3

INVENTORY_SELECTED: int = 1
INVENTORY_UNSELECTED: int = 0

###############################################################################################################
# Sound Effects
###############################################################################################################
SFX_SHOT: str = "shot-fx"
SFX_HIT: str = "hit-fx"
SFX_EXPLOSION: str = "explosion-fx"


###############################################################################################################
# Music
###############################################################################################################
MUSIC_LIST: list[str] = (
    [  # all music pieces are stored in a list to enable music control via one music player
        "test2",
        "tomb-loop",
    ]
)

# Track IDs for individual track control
TRACK_TEST: int = 0
TRACK_TOMB: int = 1
