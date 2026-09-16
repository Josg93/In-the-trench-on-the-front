from typing import Any
from src import mixins
from gale.state import StateMachine
import pygame

class GameEntity(mixins.AnimatedMixin, mixins.DrawableMixin, mixins.CollidableMixin):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        texture_id: str,
        animations: dict,
        speed: float = 60.0,
        battlefield: Any = None,
        entity_type: str = "Man",
        waypoints: list = [],
        target_position: tuple = None   
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture_id = texture_id
        self.speed = speed
        self.battlefield = battlefield
        self.entity_type = entity_type
        self.assigned_building = None
        self.assigned_slot = None
        self.animations = {}
        self.current_animation = None
        self.frame_index = 0
        self.flipped = False
        self.selected = False
        self.target_position = target_position
        self.waypoints = waypoints if waypoints is not None else [] 
        self.hp = 50
        self.max_hp = 50
        self.is_enemy = False
        self.generate_animations(animations)

        from src import states
        self.state_machine = StateMachine({
            "idle": states.entity_states.IdleState,
            "walk": states.entity_states.WalkState,
            "work": states.entity_states.WorkState,
            "shoot": states.entity_states.ShootState,
        })
        self.state_machine.entity = self
        self.state_machine.change("idle")

    def get_collision_rect(self) -> pygame.Rect:
        # Hitbox de colisión ubicado en los pies de la entidad (ancho 64, alto 32)
        # Permite superposición visual de los cuerpos pero evita que las unidades se amontonen.
        return pygame.Rect(round(self.x), round(self.y + 64), self.width, 32)

    def get_selection_rect(self) -> pygame.Rect:
        # Hitbox completo para la selección mediante clics del usuario en el sprite entero
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def get_work_rect(self) -> pygame.Rect:
        return self.get_collision_rect()
        
    def movement(self, dt : float):
        if getattr(self, "is_working", False) and (self.waypoints or self.assigned_building):
            valid_working_position = True
            if self.waypoints:
                valid_working_position = False
            elif self.assigned_building:
                if getattr(self, "assigned_slot", None):
                    sx, sy = self.assigned_slot["pos"]
                    if ((self.x - sx)**2 + (self.y - sy)**2)**0.5 >= 60.0:
                        valid_working_position = False
                elif not self.get_collision_rect().colliderect(self.assigned_building.get_collision_rect()):
                    valid_working_position = False

            if not valid_working_position and hasattr(self, "stop_working"):
                self.stop_working()

        if self.waypoints:
            # MEDIR DISTANCIAS 
            target_x, target_y = self.waypoints[0]
            entity_center_x = self.x + self.width / 2
            entity_center_y = self.y + self.height / 2
            dx = target_x - entity_center_x
            dy = target_y - entity_center_y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            # LLEGADA A DESTINO si la distancia con el punto es menor a cinco, ha llegado eliminar waypoint
            if distance < 5.0:
                self.waypoints.pop(0)
                if not self.waypoints:
                    self.target_position = None
                    if self.assigned_building and (
                        getattr(self, "assigned_slot", None) or 
                        self.get_collision_rect().colliderect(self.assigned_building.get_collision_rect())
                    ):
                        if hasattr(self, "work"):
                            self.work()
                        
                    else:
                        if self.assigned_building and hasattr(self.assigned_building, "free_slot"):
                            self.assigned_building.free_slot(self)
                        self.assigned_building = None
                        self.assigned_slot = None
                        self.state_machine.change("idle")
            
            #CAMINATA A DESTINO si no ha llegado caminar:            
            else:
                from src import states
                current_state = self.state_machine.current
                current_direction = getattr(current_state, "direction", None) if isinstance(current_state, states.entity_states.WalkState) else None

                # Histéresis con umbral para evitar parpadeos y cambios convulsivos de dirección
                threshold = 6.0
                if current_direction in ["left", "right"]:
                    if abs(dy) > abs(dx) + threshold:
                        direction = "down" if dy > 0 else "up"
                    else:
                        direction = "right" if dx > 0 else "left"
                elif current_direction in ["up", "down"]:
                    if abs(dx) > abs(dy) + threshold:
                        direction = "right" if dx > 0 else "left"
                    else:
                        direction = "down" if dy > 0 else "up"
                else:
                    if abs(dx) > abs(dy):
                        direction = "right" if dx > 0 else "left"
                    else:
                        direction = "down" if dy > 0 else "up"

                move_x = (dx / distance) * self.speed * dt
                move_y = (dy / distance) * self.speed * dt

                self.x += move_x
                self.y += move_y

                current_state = self.state_machine.current
                if not isinstance(current_state, states.entity_states.WalkState) or getattr(current_state, "direction", None) != direction:
                    self.state_machine.change("walk", direction=direction)




    def update(self, dt: float) -> None:
        self.movement(dt)
        self.state_machine.update(dt)
        super().update(dt)

    def render(self, surface: pygame.Surface, camera: Any) -> None:
        super().render(surface, camera)
        if self.selected:
            dest = camera.apply(pygame.Rect(self.x, self.y, self.width, self.height))
            pygame.draw.rect(surface, (0, 255, 0), dest, 2)

        # Renderizar barra de vida si la entidad ha perdido HP
        if hasattr(self, "hp") and hasattr(self, "max_hp") and self.hp < self.max_hp:
            bar_width = self.width
            bar_height = 6
            bar_x = self.x
            bar_y = self.y - 10
            dest = camera.apply(pygame.Rect(bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(surface, (200, 0, 0), dest)
            current_width = max(0, int(bar_width * (self.hp / self.max_hp)))
            current_rect = pygame.Rect(dest.x, dest.y, current_width, bar_height)
            pygame.draw.rect(surface, (0, 200, 0), current_rect)
            pygame.draw.rect(surface, (255, 255, 255), dest, 1)
