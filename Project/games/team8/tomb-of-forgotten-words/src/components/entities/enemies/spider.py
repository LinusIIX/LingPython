import pygame
import random
import utils.assets.asset_keys as assets
from utils.assets.asset_manager import AssetManager
from utils.assets.audio_manager import AudioManager
from components.entities.enemies.enemy import Enemy
from components.ui.health_bar import HealthBar
from components.entities.projectiles.cobweb_ball import CobwebBall


class Spider(Enemy):
    """
    Represents a Spider enemy entity with the ability to shoot webs.
    """

    def __init__(
        self,
        hp: int,
        speed: float,
        bounds: pygame.Rect,
        stage,
        knockback: int,
        acceleration: float = 0.05,
        damage: int = 0,
        shooting_range: int = 0,
    ):
        """
        Initializes a Spider object.

        Args:
            hp (int): Health points of the spider.
            speed (float): Movement speed of the spider.
            bounds (pygame.Rect): Position and collision box and size of the sprite.
            stage (Stage): The stage in which the spider exists.
            knockback (int): The knockback force applied to the player when hit by the spider.
            acceleration (float, optional): Movement acceleration to smooth out movement. Defaults to 0.05.
            damage (int, optional): The damage dealt to the player when hit by the spider. Defaults to 0.
            shooting_range (int, optional): The range within which the spider can shoot a web. Defaults to 0.
        """
        super().__init__(
            hp, speed, bounds, damage, knockback, pygame.Rect(0, 0, 100, 15), -100, stage
        )
        self.m_sprite = self.m_assets.get_image_scaled(
            assets.SPRITE_SPIDER, (bounds.width, bounds.height)
        )
        self.m_shooting: bool = False
        self.m_shooting_range: int = shooting_range  # set to zero to disable shooting
        self.m_shot_charge_time: int = 15
        self.m_shot_recover_time: int = 30
        self.m_charge_timer: int = 0
        self.m_recover_timer: int = self.m_shot_recover_time
        self.m_shot_recharge_time: int = 120
        self.m_recharge_timer: int = self.m_shot_charge_time
        self.m_aim_direction: tuple[float, float] = (0, 0)

    def take_damage(self, dmg: int) -> None:
        """
        Reduces the spider's health and stops it from shooting if it takes damage.

        Args:
            dmg (int): The damage amount.
        """
        super().take_damage(dmg)
        self.m_shooting = False
        self.m_charge_timer = 0

    def update(self) -> None:
        """
        Updates the state of the spider, including movement, shooting, and collision handling.
        """
        if self.m_recharge_timer > 0:
            self.m_recharge_timer -= 1

        # shoot web
        if self.m_shooting:
            self.m_health_bar.update()
            # do some stuff
            if self.m_charge_timer < self.m_shot_charge_time:
                self.m_charge_timer += 1
                return
            self.shoot_web()
            self.m_charge_timer = 0
            self.m_recover_timer = self.m_shot_recover_time
            self.m_shooting = False
            self.m_x_speed = 0
            self.m_y_speed = 0
            return

        if self.m_recover_timer > 0:  # disable movement whilst recovering from shooting
            self.m_recover_timer -= 1
            self.m_health_bar.update()
            return

        if self.m_recharge_timer <= 0:
            distance_to_player = self.distance_to(self.m_stage.player_center)
            if distance_to_player < self.m_shooting_range:
                rand = random.randint(
                    0, 250
                )  # the chance to shoot is very low as there is a new chance every frame, and there will be multiple spiders on screen at the same time
                if rand == 13:  # random number, chance is 1/1001
                    self.m_shooting = True
                    self.m_aim_direction = self.get_diagonal_ratio(
                        self.get_angle_to(self.m_stage.player_center)
                    )
                    return

        self.m_last_pos = self.m_bounds.topleft
        self.move_toward(self.m_stage.player_center)
        self.handle_collisions()
        self.m_health_bar.update()  # update healthbar position

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the spider on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        if self.m_sprite:
            window.blit(self.m_sprite, self.m_bounds.topleft)
        else:
            pygame.draw.rect(window, (220, 50, 50), self.m_bounds)

        self.m_health_bar.render(window)

    def shoot_web(self) -> None:
        """
        Shoots a cobweb ball projectile in the aim direction.
        """
        shot_speed = 10.0
        diagonals = self.m_aim_direction
        start_pos = (
            self.m_bounds.centerx + (0.5 * self.m_bounds.height * diagonals[0]),
            self.m_bounds.centery + (0.5 * self.m_bounds.height * diagonals[1]),
        )
        self.m_stage.spawn_projectile(
            CobwebBall(
                shot_speed,
                start_pos,
                diagonals,
                10,
                self.m_damage,
                self.m_shooting_range / shot_speed,
                100,
                100,
                210,
                self.m_stage,
            )
        )

    def handle_collisions(self) -> None:
        """
        Handles collisions with nearby objects.
        """
        objects = self.m_stage.get_nearby_objects(self)
        for o in objects:
            obj_type = self.m_stage.get_object_type(o)
            if obj_type == self.m_stage.WALL:
                if self.collides_with(o):
                    self.handle_wall_collision(o)
