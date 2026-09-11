from gale.state import BaseState

class IdleState(BaseState):
    def enter(self, **kwargs) -> None:
        self.entity = self.state_machine.entity
        self.entity.change_animation("idle")

    def update(self, dt: float) -> None:
        pass
