
from src import mixins

class GameEntity(mixins.AnimatedMixin, mixins.DrawableMixin):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        texture_id: str,
        animations: dict,
        initial_animation: str = "idle",
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture_id = texture_id
        self.animations = {}
        self.current_animation = None
        self.frame_index = 0
        self.flipped = False
        self.generate_animations(animations)
        self.change_animation(initial_animation)

    def update(self, dt: float) -> None:
        super().update(dt)
 