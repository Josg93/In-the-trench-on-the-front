from gale.state import BaseState

class WorkState(BaseState):
    def enter(self, **kwargs) -> None:
        self.entity = self.state_machine.entity
        self.entity.change_animation("work")

    def update(self, dt: float) -> None:
        pass
