from gale.state import BaseState

class ShootState(BaseState):
    """
    Estado en el que la entidad (soldado) ejecuta su animación de disparo/ataque.
    """
    def enter(self, **kwargs) -> None:
        self.entity = self.state_machine.entity
        self.entity.change_animation("shoot")

    def update(self, dt: float) -> None:
        pass
