import pygame, math
from pygame import Surface, Rect
from components.entities.entity import Entity
from components.entities.animated_entity import AnimatedEntity
from components.entities.enemies.enemy import Enemy
from components.obstacles.cobweb import Cobweb
from components.ui.health_bar import HealthBar
from components.entities.player.gun import Gun
from components.entities.projectiles.grenade import Grenade
from components.ui.hud import HUD
from components.ui.stamina_bar import StaminaBar
from utils.input.input_manager import InputManager
import utils.assets.asset_keys as assets
from utils.input.keymap import *
from utils.assets.asset_manager import AssetManager
from utils.assets.audio_manager import AudioManager
from utils.assets.sprite_sheet import SpriteSheet


class Player(Entity, AnimatedEntity):
    """
    Represents the player entity in the game with movement, shooting, and collision handling capabilities.
    """

    @property
    def max_stamina(self) -> int:
        """
        Gets the maximum stamina of the player.

        Returns:
            int: The maximum stamina.
        """
        return self.m_max_stamina

    @property
    def stamina(self) -> int:
        """
        Gets the current stamina of the player.

        Returns:
            int: The current stamina.
        """
        return self.m_stamina

    def __init__(
        self,
        hp: int,
        speed: float,
        bounds: Rect,
        sprint_speed: float,
        slow_speed: float,
        stamina: int,
        stage,
    ):
        """
        Initializes the Player object.

        Args:
            hp (int): The maximum and starting health points of the player.
            speed (float): The normal movement speed of the player.
            bounds (Rect): The rectangular bounds of the player entity.
            sprint_speed (float): The speed of the player while sprinting.
            slow_speed (float): The speed of the player when stamina is depleted.
            stamina (int): The maximum stamina of the player.
            stage (Stage): The stage in which the player exists.
        """
        Entity.__init__(self, hp, speed, bounds, stage=stage)
        AnimatedEntity.__init__(self, 15, assets.PLAYER)
        self.m_input = InputManager()
        self.m_directions = [(0.0, -1.0), (-1.0, 0.0), (0.0, 1.0), (1.0, 0.0)]
        self.m_direction_keys: [int] = [KEY_MOVE_UP, KEY_MOVE_LEFT, KEY_MOVE_DOWN, KEY_MOVE_RIGHT]

        self.m_spritesheet = SpriteSheet(self.m_assets.get_image(assets.SPRITESHEET_PLAYER), 32, 32)

        self.m_max_stamina: int = stamina
        self.m_stamina: int = stamina
        self.m_stamina_refilling: bool = False
        self.m_sprint_speed: float = sprint_speed
        self.m_slow_speed: float = slow_speed

        self.m_guns: list[Gun] = [
            Gun(50, 50, 50, assets.WEAPON_REVOLVER, 2, 13, 5, 15, 120, 5, 15, self.m_stage),
            Gun(50, 50, 50, assets.WEAPON_SHOTGUN, 5, 10, 6, 10, 60, 15, 25, self.m_stage),
            Gun(
                50,
                50,
                50,
                assets.WEAPON_MACHINE_GUN,
                1,
                25,
                3,
                15,
                180,
                1,
                8,
                self.m_stage,
                automatic=True,
            ),
        ]
        self.m_gun: int = 0
        self.m_guns[self.m_gun].set_active()
        self.m_walk_through_cobweb = False

        self.m_input.assign_function_to_scroll(self.scroll_through_weapons)
        self.m_input.assign_function_to_mouse_button(pygame.BUTTON_RIGHT, self.throw_grenade)
        self.m_grenade_charge_time = 480    
        self.m_grenade_timer = self.m_grenade_charge_time   # start of waiting for the grenade to charge

        self.m_hud = HUD()
        self.m_health_bar = HealthBar(self, pygame.Rect(0, 0, 120, 20), -120)
        self.m_stamina_bar = StaminaBar(pygame.Rect(0, 0, 80, 4), self, -104)

    def update(self) -> None:
        """
        Updates the state of the player, including movement, shooting, and collision handling.
        """
        moved: bool = False
        self.m_walk_through_cobweb = False
        self.handle_collisions()
        movement = [0.0, 0.0]
        for i in range(len(self.m_direction_keys)):
            if self.m_input.is_key_pressed(self.m_direction_keys[i]):
                dir = self.m_directions[i % len(self.m_directions)]
                movement[0] += dir[0]
                movement[1] += dir[1]

        if movement[0] != 0 and movement[1] != 0:
            movement[0] *= 0.8
            movement[1] *= 0.8

        moved = not (abs(movement[0]) + abs(movement[1]) == 0)

        if not moved:
            self.m_sprite = assets.PLAYER_STILL[self.m_facing]
        else:
            self.set_facing(movement)
            self.update_frame()
            self.animate()

        speed = self.m_speed
        if self.m_stamina_refilling:
            speed = self.m_slow_speed
        elif self.m_input.is_key_pressed(KEY_SPRINT) and moved:
            speed = self.m_sprint_speed
            self.m_stamina -= 2  # subtract two because one stamina is added every frame
            if self.m_stamina <= 0:
                self.m_stamina_refilling = True

        self.m_stamina = min(self.m_max_stamina, self.m_stamina + 1)
        if self.m_stamina == self.m_max_stamina:
            self.m_stamina_refilling = False

        if self.m_walk_through_cobweb:
            speed *= 0.3

        self.bounds.move_ip(movement[0] * speed, movement[1] * speed)
        self.m_health_bar.update()  # update the healthbar after moving to align the position
        self.m_stamina_bar.update()

        self.m_guns[self.m_gun].update(self.m_bounds.center, self.get_mouse_angle())

        if self.m_grenade_timer > 0:
            self.m_grenade_timer -= 1
            self.m_hud.update_grenade_recharge(
                (self.m_grenade_charge_time - self.m_grenade_timer) / self.m_grenade_charge_time
            )

    def scroll_through_weapons(self, dir: int) -> None:
        """
        Scrolls through the available weapons.

        Args:
            dir (int): The direction to scroll.
        """
        self.m_gun -= dir
        if self.m_gun < 0:
            self.m_gun = len(self.m_guns) - 1
        elif self.m_gun >= len(self.m_guns):
            self.m_gun = 0

        self.m_guns[self.m_gun].set_active()
        self.m_hud.update_inventory_selection(self.m_gun)

    def get_mouse_angle(self) -> float:
        """
        Gets the angle between the player and the mouse position.

        Returns:
            float: The angle in radians.
        """
        return self.get_angle_to(self.m_input.get_mouse_world_pos())

    def get_diagonal_speeds(self) -> tuple[float, float]:
        """
        Calculates the x and y speed for diagonal movements following the mouse from the player location.

        Returns:
            tuple[float, float]: The x and y speeds for diagonal movements.
        """
        angle: float = self.get_angle_to(self.m_input.get_mouse_world_pos())
        return self.get_diagonal_ratio(angle)

    def render(self, window: Surface) -> None:
        """
        Renders the player on the given window surface.

        Args:
            window (Surface): The window surface to render on.
        """
        window.blit(
            self.m_spritesheet.get_sprite_sized(
                self.m_sprite, self.m_bounds.width, self.m_bounds.height
            ),
            (self.m_bounds.x, self.m_bounds.y),
        )
        self.m_health_bar.render(window)
        self.m_stamina_bar.render(window)
        self.m_guns[self.m_gun].render(window)

    def recoil(self, direction: tuple[float, float], strength: int) -> None:
        """
        Applies recoil to the player in the given direction with the specified strength.

        Args:
            direction (tuple[float, float]): The direction of the recoil.
            strength (int): The strength of the recoil.
        """
        self.take_knockback_old((direction[0] * strength, direction[1] * strength))

    def handle_collisions(self) -> None:
        """
        Handles collisions with nearby objects.
        """
        objects = self.m_stage.get_nearby_objects(self)
        for o in objects:
            obj_type = self.m_stage.get_object_type(o)
            if obj_type != self.m_stage.PLAYER and obj_type != self.m_stage.BULLET:
                if self.collides_with(o):
                    match (obj_type):
                        case self.m_stage.WALL:
                            self.handle_wall_collision(o)

                        case self.m_stage.ENEMY:
                            self.hit_by_enemy(o)

                        case self.m_stage.PROJECTILE:
                            o.collide(self, type_id=self.m_stage.PLAYER)
                            self.take_damage(o.damage)

                        case self.m_stage.COBWEB:
                            self.walk_through_obstacle(o)

    def hit_by_enemy(self, enemy: Enemy) -> None:
        """
        Handles the player being hit by an enemy.

        Args:
            enemy (Enemy): The enemy that hit the player.
        """
        self.take_damage(enemy.damage)
        enemy_dir = enemy.get_direction()
        player_dir = self.get_direction()
        self.take_knockback(enemy, knockback=enemy.knockback)
        enemy.take_knockback(self, knockback=enemy.knockback)

    def walk_through_obstacle(self, cobweb: Cobweb) -> None:
        """
        Handles the player walking through a cobweb.

        Args:
            cobweb (Cobweb): The cobweb obstacle.
        """
        if cobweb.active:
            self.m_walk_through_cobweb = True

    def throw_grenade(self) -> None:
        """
        Throws a grenade if the grenade timer is not active.
        """
        if self.m_grenade_timer <= 0:
            self.m_grenade_timer = self.m_grenade_charge_time
            self.m_stage.spawn_projectile(
                Grenade(
                    10,
                    20,
                    125,
                    pygame.Rect(self.m_bounds.x, self.m_bounds.y, 32, 32),
                    self.m_input.get_mouse_world_pos(),
                    self.m_stage,
                )
            )
