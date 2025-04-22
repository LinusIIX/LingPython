import utils.assets.asset_keys as assets


class AnimatedEntity:
    """
    Represents an entity with animation capabilities.
    """

    def __init__(self, updates_per_frame: int, sprite_sheet_id):
        """
        Initializes an AnimatedEntity object.

        Args:
            updates_per_frame (int): Number of updates per animation frame.
            sprite_sheet_id: Identifier for the sprite sheet used for animation.
        """
        self.m_updates_per_frame = updates_per_frame
        self.m_sprite_sheet_id = sprite_sheet_id

        self.m_facing: int = assets.FACING_FRONT
        self.m_anim_frame: int = assets.STILLS[self.m_sprite_sheet_id][0]
        self.m_sprite: int = assets.STILLS[self.m_sprite_sheet_id][self.m_facing]

        self.m_frame_timer: int = self.m_updates_per_frame

    def set_facing(self, direction: tuple[float, float]) -> None:
        """
        Sets the facing direction of the entity based on the given direction vector.

        Args:
            direction (tuple[float, float]): The direction vector.
        """
        if abs(direction[0]) > abs(direction[1]):  # facing left or right
            if direction[0] < 0:
                self.m_facing = assets.FACING_LEFT  # facing right
                return
            self.m_facing = assets.FACING_RIGHT  # facing right
            return
        if direction[1] < 0:  # facing back
            self.m_facing = assets.FACING_BACK
            return
        self.m_facing = assets.FACING_FRONT  # facing the front

    def animate(self) -> None:
        """
        Updates the animation frame based on the frame timer.
        """
        self.m_frame_timer -= 1
        if self.m_frame_timer <= 0:
            self.m_frame_timer = self.m_updates_per_frame
            self.m_anim_frame += 1
            self.m_anim_frame %= len(assets.WALKS[self.m_sprite_sheet_id][self.m_facing])
            self.update_frame()

    def update_frame(self) -> None:
        """
        Updates the currently shown frame with error handling.
        """
        if self.m_facing >= len(assets.FACING):
            print(f"ERROR: {self.m_facing} is not a valid facing direction value")
            return
        if self.m_anim_frame >= len(assets.WALKS[self.m_sprite_sheet_id][self.m_facing]):
            print(
                f"ERROR: Frame {self.m_anim_frame} is out of bounds for size {len(assets.WALKS[self.m_sprite_sheet_id][self.m_facing])}"
            )
            return
        self.m_sprite = assets.WALKS[self.m_sprite_sheet_id][self.m_facing][self.m_anim_frame]
