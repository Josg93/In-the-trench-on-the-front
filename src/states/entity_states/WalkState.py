from gale.state import BaseState

class WalkState(BaseState):
    def enter(self, direction: str = "right", **kwargs) -> None:
        self.entity = self.state_machine.entity
        self.direction = direction
        self.entity.change_animation(f"walk_{direction}")

    def update(self, dt: float) -> None:
        speed = getattr(self.entity, "speed", 100.0)
        if self.direction == "left":
            self.entity.x -= speed * dt
        elif self.direction == "right":
            self.entity.x += speed * dt
        elif self.direction == "up":
            self.entity.y -= speed * dt
        elif self.direction == "down":
            self.entity.y += speed * dt
