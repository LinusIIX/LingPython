import pygame
from components.game_object import GameObject
from components.entities.enemies.enemy_spawner import EnemySpawner
from components.entities.projectiles.bullet import Bullet
from components.entities.projectiles.cobweb_ball import CobwebBall
from components.entities.enemies.enemy import Enemy
from components.entities.enemies.golem import Golem
from components.entities.enemies.spider import Spider
from components.entities.enemies.mummy import Mummy
from components.entities.entity import Entity
from components.entities.player.player import Player
from components.obstacles.cobweb import Cobweb
from components.entities.projectiles.stone import Stone
from components.obstacles.wall import Wall

import utils.assets.asset_keys as assets
from utils.assets.asset_manager import AssetManager
from utils.input.input_manager import InputManager
from utils.spatial_grid import SpatialGrid


class Stage:
    """
    Represents the stage on which the gameplay takes place.
    """

    PLAYER: int = 0
    WALL: int = 1
    ENEMY: int = 2
    BULLET: int = 3
    PROJECTILE: int = 4
    COBWEB: int = 5

    @property
    def player_center(self) -> tuple[int, int]:
        """Returns the center coordinates of the player."""
        return self.m_player.bounds.center

    @property
    def width(self) -> int:
        """Returns the width of the stage."""
        return self.m_width

    @property
    def height(self) -> int:
        """Returns the height of the stage."""
        return self.m_height

    @property
    def entity_grid(self) -> SpatialGrid:
        """Returns the spatial grid for managing entity positions."""
        return self.m_grid

    @property
    def game_over(self) -> bool:
        """Returns the game_over boolean for managing game_over and restarts"""
        return self.m_game_over or self.game_won

    @property
    def game_won(self) -> bool:
        """Returns the game_over boolean for managing game_over and restarts"""
        return self.m_game_won

    @property
    def enemy_spawner(self) -> EnemySpawner:
        """Returns the enemy spawner for the current stage"""
        return self.m_enemy_spawner

    def __init__(self, width: int, height: int):
        """
        Initializes the Stage object.

        Args:
            width (int): The width of the stage.
            height (int): The height of the stage.
        """
        self.m_type_ids = {
            Player: self.PLAYER,
            Wall: self.WALL,
            Spider: self.ENEMY,
            Golem: self.ENEMY,
            Mummy: self.ENEMY,
            Bullet: self.BULLET,
            CobwebBall: self.PROJECTILE,
            Cobweb: self.COBWEB,
            Stone: self.PROJECTILE,
        }

        self.m_game_over: bool = False
        self.m_game_won: bool = False

        self.m_width = width
        self.m_height = height

        self.m_assets = AssetManager()
        self.m_input = InputManager()
        self.m_game_objects: list[GameObject] = []
        self.m_stage = pygame.Surface((width, height))
        self.m_background = self.m_assets.get_image_scaled(
            assets.SPRITE_MAP_BACKGROUND, (width, height)
        )

        self.m_player = Player(100, 10.0, pygame.Rect(width//2 - 32, height//2 - 32, 64, 64), 15, 5, 180, self)

        self.m_bullets: list[Bullet] = []
        self.m_enemies: list[Enemy] = []
        self.m_projectiles: list[Entity] = []

        self.m_enemy_spawner = EnemySpawner(self.m_assets)

        self.m_grid = SpatialGrid(150)  # for moving entities

        self.m_game_objects.append(Wall(pygame.Rect(0, 0, self.m_width, 64)))
        self.m_game_objects.append(Wall(pygame.Rect(0, 0, 64, height)))
        self.m_game_objects.append(Wall(pygame.Rect(width - 64, 0, 64, height)))
        self.m_game_objects.append(Wall(pygame.Rect(0, height - 64, width, 64)))

        self.m_game_objects.append(self.m_player)

    def update(self) -> None:
        """
        Updates the state of the stage and its game objects.
        """
        if self.m_player.hp <= 0:
            self.m_game_over = True
            return

        self.check_game_objects_to_delete()

        if len(self.m_enemies) == 0 and self.m_enemy_spawner.queue_len == 0:
            if self.m_enemy_spawner.has_next_wave:
                self.m_enemy_spawner.new_wave(self)
            else:
                self.m_game_won = True

        # move
        self.m_grid.clear()
        for o in self.m_game_objects:
            if self.get_object_type(o) == self.COBWEB:
                o.update()
            self.m_grid.add(o)

        self.check_enemy_hp()
        self.update_projectiles()
        self.update_bullets()
        self.m_player.update()

        new_enemies = self.m_enemy_spawner.update()
        for enemy in new_enemies:
            self.spawn_enemy(enemy)

    def update_bullets(self) -> None:
        """
        Updates the state of all bullets.
        """
        for i in range(len(self.m_bullets) - 1, -1, -1):
            if self.m_bullets[i].to_be_deleted:
                self.m_bullets.pop(i)
                return
            self.m_bullets[i].update()

    def check_enemy_hp(self) -> None:
        """
        Checks the health of all enemies and removes those with zero or less health.
        """
        for i in range(
            len(self.m_enemies) - 1, -1, -1
        ):  # iterate backwards to avoid problems when removing an object during iteration
            if self.m_enemies[i].hp <= 0:
                self.m_enemies[i].delete()
                self.m_enemies.pop(i)
            else:
                self.m_enemies[i].update()
                self.m_grid.add(self.m_enemies[i])

    def check_game_objects_to_delete(self) -> None:
        """
        Checks all game objects and removes those marked for deletion.
        """
        for i in range(
            len(self.m_game_objects) - 1, -1, -1
        ):  # iterate backwards to avoid problems when removing an object during iteration
            if self.m_game_objects[i].to_be_deleted:
                self.m_game_objects.pop(i)  # remove from list

    def update_projectiles(self) -> None:
        """
        Updates the state of all projectiles.
        """
        for i in range(len(self.m_projectiles) - 1, -1, -1):
            if self.m_projectiles[i].hp <= 0:
                self.m_projectiles[i].delete()
                self.m_projectiles.pop(i)
            else:
                self.m_projectiles[i].update()

    def render(self, camera_rect: pygame.Rect) -> pygame.Surface:
        """
        Renders the stage and its game objects.

        Args:
            camera_rect (pygame.Rect): The camera rectangle defining the visible area.

        Returns:
            pygame.Surface: The rendered stage surface.
        """
        self.m_stage.blit(self.m_background, (0, 0))
        for go in self.m_game_objects:
            if camera_rect.colliderect(go.bounds):
                go.render(self.m_stage)
        self.m_enemy_spawner.render(self.m_stage)
        return self.m_stage

    # Functions for spawning objects

    def spawn_bullet(self, bullet: Bullet) -> None:
        """
        Spawns a bullet on the stage.

        Args:
            bullet (Bullet): The bullet to spawn.
        """
        bullet.set_stage(self)
        self.m_bullets.append(bullet)
        self.m_game_objects.append(bullet)

    def spawn_enemy(self, enemy: Enemy) -> None:
        """
        Spawns an enemy on the stage.

        Args:
            enemy (Enemy): The enemy to spawn.
        """
        self.m_enemies.append(enemy)
        self.m_game_objects.append(enemy)

    def spawn_game_object(self, obj: GameObject) -> None:
        """
        Spawns a generic game object on the stage.

        Args:
            obj (GameObject): The game object to spawn.
        """
        self.m_game_objects.append(obj)

    def spawn_projectile(self, projectile: Entity) -> None:
        """
        Spawns a projectile on the stage.

        Args:
            projectile (Entity): The projectile to spawn.
        """
        self.m_projectiles.append(projectile)
        self.m_game_objects.append(projectile)

    def get_object_type(self, game_object: GameObject) -> int:
        """
        Returns the type identifier of a game object.

        Args:
            game_object (GameObject): The game object to identify.

        Returns:
            int: The type identifier of the game object.
        """
        return self.m_type_ids.get(game_object.__class__)

    def get_nearby_objects(self, obj: GameObject) -> list[GameObject]:
        """
        Returns a list of nearby game objects for a given game object.

        Args:
            obj (GameObject): The reference game object.

        Returns:
            list[GameObject]: The list of nearby game objects.
        """
        return self.m_grid.get_nearby(obj)
