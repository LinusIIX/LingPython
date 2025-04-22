import pygame, math
import utils.assets.asset_keys as assets
from utils.input.input_manager import InputManager
from utils.assets.asset_manager import AssetManager
from utils.assets.audio_manager import AudioManager
from utils.assets.sprite_sheet import SpriteSheet
from components.entities.projectiles.bullet import Bullet


class Gun:
    """
    Represents a gun with shooting capabilities.

    Attributes:
        m_width (int): The width of the gun.
        m_height (int): The height of the gun.
        m_offset (int): The offset of the gun from the player.
        m_assets (AssetManager): The asset manager for loading assets.
        m_damage (int): The damage dealt by the gun.
        m_bullet_speed (float): The speed of the bullets.
        m_bullet_width (int): The width of the bullets.
        m_bullet_length (int): The length of the bullets.
        m_input (InputManager): The input manager for handling input.
        m_base_sprite (pygame.Surface): The base sprite of the gun.
        m_sprite (pygame.Surface): The current sprite of the gun.
        m_sprite_rect (pygame.Rect): The rectangle of the current sprite.
        m_pos (tuple[float, float]): The position of the gun.
        m_bullet_lifespan (int): The lifespan of the bullets.
        m_recoil (float): The recoil of the gun.
        m_shot_delay (int): The delay between shots.
        m_shot_delay_counter (int): The counter for the shot delay.
        m_stage: The stage on which the gun exists.
        m_audio (AudioManager): The audio manager for playing sounds.
        m_x (float): The x-coordinate of the gun's direction.
        m_y (float): The y-coordinate of the gun's direction.
        m_automatic (bool): Indicates if the gun is automatic.
        m_shooting (bool): Indicates if the gun is currently shooting.
    """

    @property
    def position(self) -> tuple[float, float]:
        """
        Gets the position of the gun.

        Returns:
            tuple[float, float]: The position of the gun.
        """
        return self.m_pos

    @property
    def damage(self) -> int:
        """
        Gets the damage dealt by the gun.

        Returns:
            int: The damage dealt by the gun.
        """
        return self.m_damage

    @property
    def bullet_size(self) -> tuple[int, int]:
        """
        Gets the size of the bullets.

        Returns:
            tuple[int, int]: The width and length of the bullets.
        """
        return (self.m_bullet_width, self.m_bullet_length)

    @property
    def bullet_speed(self) -> float:
        """
        Gets the speed of the bullets.

        Returns:
            float: The speed of the bullets.
        """
        return self.m_bullet_speed

    @property
    def bullet_lifespan(self) -> int:
        """
        Gets the lifespan of the bullets.

        Returns:
            int: The lifespan of the bullets.
        """
        return self.m_bullet_lifespan

    @property
    def width(self) -> int:
        """
        Gets the width of the gun.

        Returns:
            int: The width of the gun.
        """
        return self.m_width

    @property
    def height(self) -> int:
        """
        Gets the height of the gun.

        Returns:
            int: The height of the gun.
        """
        return self.m_height

    @property
    def recoil(self) -> float:
        """
        Gets the recoil of the gun.

        Returns:
            float: The recoil of the gun.
        """
        return self.m_recoil

    @property
    def delay_active(self) -> bool:
        """
        Checks if the shot delay is active.

        Returns:
            bool: True if the shot delay is active, False otherwise.
        """
        return self.m_shot_delay_counter > 0

    def __init__(
        self,
        width: int,
        height: int,
        offset: int,
        weapon_sprite: int,
        damage: int,
        bullet_speed: float,
        bullet_width: int,
        bullet_length: int,
        bullet_lifespan: int,
        recoil: float,
        shoot_delay: int,
        stage,
        automatic: bool = False,
    ):
        """
        Initializes a Gun object.

        Args:
            width (int): The width of the gun.
            height (int): The height of the gun.
            offset (int): The offset of the gun from the player.
            weapon_sprite (int): The sprite ID of the weapon.
            damage (int): The damage dealt by the gun.
            bullet_speed (float): The speed of the bullets.
            bullet_width (int): The width of the bullets.
            bullet_length (int): The length of the bullets.
            bullet_lifespan (int): The lifespan of the bullets.
            recoil (float): The recoil of the gun.
            shoot_delay (int): The delay between shots.
            stage: The stage on which the gun exists.
            automatic (bool, optional): Indicates if the gun is automatic. Defaults to False.
        """
        self.m_width = width
        self.m_height = height
        self.m_offset = offset
        self.m_assets = AssetManager()
        self.m_damage = damage
        self.m_bullet_speed = bullet_speed
        self.m_bullet_width = bullet_width
        self.m_bullet_length = bullet_length

        self.m_input = InputManager()

        sprite_sheet = SpriteSheet(self.m_assets.get_image(assets.SPRITESHEET_WEAPONS), 32, 32)
        self.m_base_sprite = sprite_sheet.get_sprite_sized(
            weapon_sprite, self.m_width, self.m_height
        )
        self.m_sprite = self.m_base_sprite
        self.m_sprite_rect = self.m_sprite.get_rect()
        self.m_pos = (0.0, 0.0)
        self.m_bullet_lifespan = bullet_lifespan
        self.m_recoil = recoil
        self.m_shot_delay = shoot_delay
        self.m_shot_delay_counter = 0
        self.m_stage = stage
        self.m_audio = AudioManager()
        self.m_x = 0
        self.m_y = 0

        self.m_automatic = automatic
        self.m_shooting = False

    def update(self, player_pos: tuple[int, int], mouse_angle: float) -> None:
        """
        Updates the state of the gun, including rotation and shooting.

        Args:
            player_pos (tuple[int, int]): The position of the player.
            mouse_angle (float): The angle of the mouse relative to the player.
        """
        if self.m_shot_delay_counter > 0:
            self.m_shot_delay_counter -= 1
        self.rotate_gun(player_pos, mouse_angle)

        if self.m_shooting:
            self.m_shooting = self.m_input.is_button_pressed(pygame.BUTTON_LEFT)
            self.shoot()

    def rotate_gun(self, player_pos: tuple[int, int], mouse_angle: float) -> None:
        """
        Rotates the gun based on the player's position and mouse angle.

        Args:
            player_pos (tuple[int, int]): The position of the player.
            mouse_angle (float): The angle of the mouse relative to the player.
        """
        self.m_x = math.cos(mouse_angle)
        self.m_y = math.sin(mouse_angle)
        gun_x = player_pos[0] - self.m_offset * self.m_x
        gun_y = player_pos[1] - self.m_offset * self.m_y
        self.m_pos = (gun_x, gun_y)

        angle_deg = math.degrees(mouse_angle)
        self.m_sprite = self.m_base_sprite
        if abs(angle_deg) < 90:
            self.m_sprite = pygame.transform.flip(self.m_sprite, False, True)
        self.m_sprite = pygame.transform.rotate(self.m_sprite, -(angle_deg + 180))
        self.m_sprite_rect = self.m_sprite.get_rect(center=(gun_x, gun_y))

    def render(self, window: pygame.Surface) -> None:
        """
        Renders the gun on the given window surface.

        Args:
            window (pygame.Surface): The window surface to render on.
        """
        window.blit(self.m_sprite, self.m_sprite_rect.topleft)

    def set_active(self) -> None:
        """
        Sets the gun as active, assigning a function to the mouse button.
        """
        self.m_input.assign_function_to_mouse_button(pygame.BUTTON_LEFT, self.click)

    def click(self) -> None:
        """
        Handles the click event for the gun.
        """
        if self.m_automatic:
            self.m_shooting = True
        else:
            self.shoot()

    def shoot(self) -> None:
        """
        Shoots a bullet from the gun.
        """
        if self.m_shot_delay_counter > 0:
            return
        self.m_shot_delay_counter = self.m_shot_delay
        self.m_audio.play_sfx(assets.SFX_SHOT)
        x_pos = self.m_pos[0] + int(self.m_x * self.m_width)
        y_pos = self.m_pos[1] + int(self.m_y * self.m_height)
        self.m_stage.spawn_bullet(
            Bullet(
                self.m_bullet_speed,
                (-self.m_x, -self.m_y),
                self.damage,
                pygame.Rect(
                    self.m_pos[0], self.m_pos[1], self.m_bullet_width, self.m_bullet_length
                ),
                self.m_bullet_lifespan,
            )
        )
