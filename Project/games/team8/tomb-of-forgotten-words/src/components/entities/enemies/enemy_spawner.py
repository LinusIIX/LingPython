import random

import pygame
from components.entities.enemies.enemy import Enemy
from components.entities.enemies.golem import Golem
from components.entities.enemies.mummy import Mummy
from components.entities.enemies.spider import Spider
from utils.assets import asset_keys
from utils.assets.asset_manager import AssetManager
from enum import Enum

TARGET_MARKER_MAX_DELAY = 45
"""
The maximum number of ticks until enemy spawn that the target marker will be
revealed at. This makes the target marker show up only very shortly before the
enemy spawns, which makes the game more fast-paced.
"""
TARGET_MARKER_INITIAL_SCALE = 2
"""
The initial scale of the target marker (relative to the spawned object's size). The
target marker will shrink every frame to simulate a "convergence" effect.
"""

ENEMY_SPAWN_MAX_RANGE = 200
"""
The maximum distance from the player at which enemies should spawn.
"""
ENEMY_SPAWN_MIN_RANGE = 100
"""
The minimum distance from the player
"""


class Direction(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3


def get_random_enemy_pos(player_pos: (float, float), direction: Direction, stage_bounds: (float, float)) -> (float, float):
    """
    Helper function to place enemies in a random range around the player.

    Args:
        player_pos: Current player position
        direction: Direction from player the enemies should be placed in
        stage_bounds: Boundaries of the stage.
    """
    offset1 = random.randint(0, ENEMY_SPAWN_MAX_RANGE - ENEMY_SPAWN_MIN_RANGE)
    offset2 = random.randint(-(ENEMY_SPAWN_MAX_RANGE - ENEMY_SPAWN_MIN_RANGE),
                             ENEMY_SPAWN_MAX_RANGE - ENEMY_SPAWN_MIN_RANGE)

    if offset2 < 0:
        offset2 -= ENEMY_SPAWN_MIN_RANGE
    else:
        offset2 += ENEMY_SPAWN_MIN_RANGE
    offset1 += ENEMY_SPAWN_MIN_RANGE

    if direction == Direction.NORTH:
        if player_pos[1] - offset1 < 0:
            offset1 = -offset1
        if player_pos[0] + offset2 < 0 or player_pos[0] + offset2 >= stage_bounds[0]:
            offset2 = -offset2
        enemy_pos = (player_pos[0] + offset2, player_pos[1] - offset1)
    elif direction == Direction.WEST:
        if player_pos[0] - offset1 < 0:
            offset1 = -offset1
        if player_pos[1] + offset2 < 0 or player_pos[1] + offset2 >= stage_bounds[1]:
            offset2 = -offset2
        enemy_pos = (player_pos[0] - offset1, player_pos[1] + offset2)
    elif direction == Direction.SOUTH:
        if player_pos[1] + offset1 >= stage_bounds[1]:
            offset1 = -offset1
        if player_pos[0] + offset2 < 0 or player_pos[0] + offset2 >= stage_bounds[0]:
            offset2 = -offset2
        enemy_pos = (player_pos[0] + offset2, player_pos[1] + offset1)
    elif direction == Direction.EAST:
        if player_pos[0] + offset1 >= stage_bounds[0]:
            offset1 = -offset1
        if player_pos[1] + offset2 < 0 or player_pos[1] + offset2 >= stage_bounds[1]:
            offset2 = -offset2
        enemy_pos = (player_pos[0] + offset1, player_pos[1] + offset2)
    return enemy_pos


class EnemySpawner:
    """
    Class for spawning enemies. Manages rendering of target icons in places where enemies are about to spawn,
    as well as spawning them with appropriate delays.
    """

    class SpawnQueueEntry:
        """
        Utility class for keeping track of an entry in the queue of entities to spawn, and when to spawn it.
        """

        def __init__(self, delay: int, entity: Enemy):
            self.m_remaining_delay = delay
            self.m_entity = entity

    @property
    def queue_len(self) -> int:
        return len(self.m_spawn_queue)

    @property
    def has_next_wave(self) -> bool:
        return self.m_wave_index < len(self.m_waves)

    @property
    def wave_index(self):
        return self.m_wave_index

    @property
    def num_waves(self):
        return len(self.m_waves)

    def __init__(self, asset_manager: AssetManager):
        """
        Initializes the enemy spawner.

        Args:
            asset_manager: The asset manager to use for loading the targeting sprite.
        """
        self.m_spawn_queue: list[EnemySpawner.SpawnQueueEntry] = []
        self.m_asset_manager = asset_manager
        self.m_wave_index = 0

        self.m_enemy_base_sizes = {
            Golem: 256,
            Mummy: 64,
            Spider: 100,
        }
        self.m_waves = [
            {
                Golem: 1,
                Mummy: 2,
                Spider: 1,
            },
            {
                Golem: 0,
                Mummy: 2,
                Spider: 3,
            },
            {
                Golem: 2,
                Mummy: 4,
                Spider: 2,
            },
            {
                Golem: 0,
                Mummy: 4,
                Spider: 4,
            },
            {
                Golem: 12,
                Mummy: 6,
                Spider: 3,
            }
        ]

    def reset(self) -> None:
        """
        Resets the wave progress back to wave 0.
        """
        self.m_wave_index = 0

    def new_wave(self, stage) -> None:
        """
        Starts a new wave, adding new enemies to the spawn queue.

        Args:
            player_pos: The current position of the player.
            stage_bounds: The extent of the stage, to bound enemy spawns to inside the stage.
        """
        # Choose a direction (north, east, south, west) relative to the player to spawn enemies in.
        # Only spawn enemies in a random range in this direction - if we spawn enemies in all directions,
        # they surround the player, which would make escaping unharmed very difficult.
        direction = Direction(random.randint(0, 3))

        player_pos = stage.player_center
        stage_bounds = (stage.width, stage.height)

        enemies = self.m_waves[self.m_wave_index]

        enemy_delay = 80

        for i in range(enemies[Golem]):
            position = get_random_enemy_pos(player_pos, direction, stage_bounds)
            self.spawn_enemy(enemy_delay, Golem(
                30,
                2,
                pygame.Rect(position[0], position[1], 256, 256),
                stage,
                20,
                acceleration=0.05,
                damage=30,
                shooting_range=512,
                player_distance=384,
                lives=3,
            ))
            enemy_delay += 30
        for i in range(enemies[Mummy]):
            position = get_random_enemy_pos(player_pos, direction, stage_bounds)
            self.spawn_enemy(enemy_delay, Mummy(15, 5, pygame.Rect(position[0], position[1], 64, 64), stage, 15, damage=15))
            enemy_delay += 30
        for i in range(enemies[Spider]):
            position = get_random_enemy_pos(player_pos, direction, stage_bounds)
            self.spawn_enemy(enemy_delay, Spider(
                10,
                5,
                pygame.Rect(position[0], position[1], 100, 100),
                stage,
                15,
                damage=3,
                shooting_range=600,
            ))
            enemy_delay += 30

        self.m_wave_index = self.m_wave_index + 1

    def spawn_enemy(self, delay: int, enemy: Enemy) -> None:
        """
        Adds an enemy to the spawn queue.

        Args:
            delay: The number of ticks to wait until actually spawning the enemy.
            enemy: The Enemy entity to spawn.
        """
        self.m_spawn_queue.append(EnemySpawner.SpawnQueueEntry(delay, enemy))

    def update(self) -> list[Enemy]:
        """
        Updates the spawn queue and pops off enemies that should be spawned in this tick.

        Return: A list of enemies to be spawned this tick.
        """
        enemies_to_spawn: list[Enemy] = []
        for i in range(
                len(self.m_spawn_queue) - 1, -1, -1
        ):  # iterate backwards to avoid problems when removing an object during iteration
            self.m_spawn_queue[i].m_remaining_delay -= 1
            if self.m_spawn_queue[i].m_remaining_delay <= 0:
                (enemies_to_spawn.append(self.m_spawn_queue[i].m_entity))
                self.m_spawn_queue.pop(i)
        return enemies_to_spawn

    def render(self, window: pygame.Surface) -> None:
        """
        Renders targeting icons for enemies currently in the spawn queue.

        Args:
            window: The window to draw the targeting icons into.
        """
        # Draw a target marker indicating the imminent enemy spawn during the countdown until
        # the enemy actually spawns.
        for entry in self.m_spawn_queue:
            # Only reveal the enemy's spawning position TARGET_MARKER_MAX_DELAY ticks before the
            # enemy spawns.
            if entry.m_remaining_delay > TARGET_MARKER_MAX_DELAY:
                continue
            bounds = entry.m_entity.m_bounds
            remaining_delay_scale = entry.m_remaining_delay / float(TARGET_MARKER_MAX_DELAY)

            # The target marker should gradually shrink in size to model the targeting icon "converging"
            # on the area where
            width = bounds.width * TARGET_MARKER_INITIAL_SCALE * remaining_delay_scale
            height = bounds.height * TARGET_MARKER_INITIAL_SCALE * remaining_delay_scale
            sprite = self.m_asset_manager.get_image_scaled(asset_keys.SPRITE_SPAWN_MARKER, (width, height))

            topleft_x = bounds.center[0] - width / 2
            topleft_y = bounds.center[1] - height / 2

            window.blit(sprite, (topleft_x, topleft_y))
