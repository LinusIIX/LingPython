import pygame, random
from components.entities.animated_entity import AnimatedEntity
from components.entities.enemies.enemy import Enemy
from components.entities.projectiles.stone import Stone
import utils.assets.asset_keys as assets
from utils.assets.asset_manager import AssetManager
from utils.assets.sprite_sheet import SpriteSheet


class Golem(Enemy, AnimatedEntity):
    """
    Represents a Golem enemy entity with animation capabilities.
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
        shooting_range: float = 0,
        player_distance: float = 0,
        lives: int = 1,
    ):
        """
        Initializes a Golem object.

        Args:
            hp (int): The health points of the golem.
            speed (float): The speed of the golem.
            bounds (pygame.Rect): The rectangular bounds of the golem.
            stage (Stage): The stage on which the golem exists.
            knockback (int): The knockback force of the golem.
            acceleration (float, optional): The acceleration of the golem. Defaults to 0.05.
            damage (int, optional): The damage dealt by the golem. Defaults to 0.
            shooting_range (float, optional): The range within which the golem can shoot projectiles. Defaults to 0.
            player_distance (float, optional): The distance to the player that the golem tries to maintain. Defaults to 0.
            lives (int, optional): The number of lives the golem has. Defaults to 1.
        """
        Enemy.__init__(
            self, hp, speed, bounds, damage, knockback, pygame.Rect(0, 0, 100, 15), -100, stage
        )
        AnimatedEntity.__init__(self, 15, assets.GOLEM)
        self.m_shooting_range = shooting_range
        self.m_lives = lives
        self.m_player_distance = (
            player_distance  # distance to player that the golem tries to keep up
        )
        self.m_acceleration = acceleration

        asset_manager = AssetManager()
        self.m_spritesheet = SpriteSheet(asset_manager.get_image(assets.SPRITESHEET_GOLEM), 64, 64)

        self.m_min_shoot_delay: int = 120
        self.m_max_shoot_delay: int = 240
        self.m_min_projectile_size: int = 16
        self.m_max_projectile_size: int = 48
        self.m_min_shot_speed: float = 10
        self.m_max_shot_speed: float = 20
        self.m_shoot_delay_counter: int = self.m_max_shoot_delay

    def update(self) -> None:
        """
        Updates the state of the golem, including movement, shooting, and animation.
        """
        if self.m_hp <= 0:
            self.m_to_be_deleted = True

        distance_to_player = self.distance_to(self.m_stage.player_center)
        if distance_to_player < self.m_shooting_range:  # if player is within shooting range
            if distance_to_player < self.m_player_distance:  # if the player is too close move away
                self.move_away_from(self.m_stage.player_center)
                self.set_facing((self.m_x_speed, self.m_y_speed))
                self.reset_shoot_delay_counter()
            else:
                self.m_x_speed = 0
                self.m_y_speed = 0
                self.set_facing(
                    self.get_diagonal_ratio(self.get_angle_to(self.m_stage.player_center))
                )  # always face the player when standing
                self.handle_shooting()
        else:
            self.move_toward(
                self.m_stage.player_center
            )  # if the player is out of shooting range move toward the player
            self.reset_shoot_delay_counter()  # if the golem is moving reset the timer

        if abs(self.m_x_speed) + abs(self.m_y_speed) == 0:
            self.m_sprite = assets.GOLEM_STILL[self.m_facing]
        else:
            self.set_facing((self.m_x_speed, self.m_y_speed))
            self.update_frame()
            self.animate()

        self.m_health_bar.update()

    def reset_shoot_delay_counter(self) -> None:
        """
        Resets the shoot delay counter to a random value between the minimum and maximum shoot delay.
        """
        self.m_shoot_delay_counter = random.randint(self.m_min_shoot_delay, self.m_max_shoot_delay)

    def handle_shooting(self) -> None:
        """
        Handles the shooting logic for the golem.
        """
        if self.m_shoot_delay_counter <= 0:
            self.shoot()
            self.reset_shoot_delay_counter()
            return
        self.m_shoot_delay_counter -= 1

    def shoot(self) -> None:
        """
        Shoots a projectile towards the player.
        """
        shot_speed = random.randrange(self.m_min_shot_speed, self.m_max_shot_speed)
        diagonals = self.get_diagonal_ratio(self.get_angle_to(self.m_stage.player_center))
        start_pos = (
            self.m_bounds.centerx + (0.5 * self.m_bounds.height * diagonals[0]),
            self.m_bounds.centery + (0.5 * self.m_bounds.height * diagonals[1]),
        )
        self.m_stage.spawn_projectile(
            Stone(
                shot_speed,
                start_pos,
                diagonals,
                random.randint(self.m_min_projectile_size, self.m_max_projectile_size) // 2,
                self.m_damage,
                self.m_shooting_range / shot_speed,
                self.m_stage,
            )
        )

    def move_away_from(self, position: tuple[int, int]) -> None:
        """
        Moves the golem away from a given position.

        Args:
            position (tuple[int, int]): The position to move away from.
        """
        angle = self.get_angle_to(position)
        diagonal = self.get_diagonal_ratio(angle)

        pos_away = (
            self.m_bounds.centerx + (-diagonal[0] * 1000),
            self.m_bounds.centery + (-diagonal[1] * 1000),
        )  # the thousand has no meaning, just a big number for a distant target point
        self.move_toward(pos_away)

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the golem on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        window.blit(
            self.m_spritesheet.get_sprite_sized(
                self.m_sprite, self.m_bounds.width, self.m_bounds.height
            ),
            (self.m_bounds.x, self.m_bounds.y),
        )
        self.m_health_bar.render(window)

    def summon_children(self) -> None:
        """
        Summons child golems when the parent golem is destroyed.
        """
        for i in range(2):
            startx: int = self.m_bounds.x + random.randint(-128, 128)
            starty: int = self.m_bounds.y + random.randint(-128, 128)
            self.m_stage.enemy_spawner.spawn_enemy(45,
                Golem(
                    self.m_max_hp // 2,
                    self.m_speed,
                    pygame.Rect(
                        startx, starty, self.m_bounds.width // 2, self.m_bounds.height // 2
                    ),
                    self.m_stage,
                    self.m_knockback,
                    acceleration=self.m_acceleration,
                    damage=self.m_damage,
                    shooting_range=self.m_shooting_range * 0.75,
                    player_distance=self.m_player_distance * 0.75,
                    lives=self.m_lives - 1,
                )
            )

    def delete(self) -> None:
        """
        Deletes the golem and summons child golems if it has remaining lives.
        """
        super().delete()
        if self.m_lives > 1:
            self.summon_children()
