
from src import mixins

class GameBuilding(mixins.DrawableMixin , mixins.CollidableMixin):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        texture_id: str,
        frame_index: int,
        collidable: bool,
        solid : bool = False,
        #on_collide: Optional[Callable[[TypeVar("GameItem"), Any], Any]] = None,
        #on_consume: Optional[Callable[[TypeVar("GameItem"), Any], Any]] = None,
        
        ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture_id = texture_id
        self.frame_index = frame_index
        self.flipped = False
        self.collidable = collidable
        #self._on_collide = on_collide
        #self._on_consume = on_consume
        self.active = True
        self.solid = solid
    pass
pass 