from src import mixins

class GameBuilding(mixins.DrawableMixin, mixins.CollidableMixin):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        texture_id: str,
        frame_index: int,
        collidable: bool = True,
        solid: bool = False,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture_id = texture_id
        self.frame_index = frame_index
        self.flipped = False
        self.collidable = collidable
        self.active = True
        self.solid = solid
