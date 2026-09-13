from typing import Any
from src import mixins
from gale.state import StateMachine
import pygame

class GameEntity(mixins.AnimatedMixin, mixins.DrawableMixin):
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
        })
        self.state_machine.entity = self
        self.state_machine.change("idle")

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def get_work_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y + 64), self.width, 32)
        
    def movement(self, dt : float):
        if getattr(self, "is_working", False) and self.waypoints:
            if hasattr(self, "stop_working"):
                self.stop_working()

        if getattr(self, "is_working", False) and self.assigned_building:
            if not self.get_collision_rect().colliderect(self.assigned_building.get_collision_rect()):
                if hasattr(self, "stop_working"):
                    self.stop_working()

        if self.waypoints:
            target_x, target_y = self.waypoints[0]
            dx = target_x - self.x
            dy = target_y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            # si la distancia con el punto es menor a cinco, ha llegado eliminar waypoint
            if distance < 5.0:
                self.waypoints.pop(0)
                if not self.waypoints:
                    
                    self.target_position = None
                    if self.assigned_building and self.get_collision_rect().colliderect(self.assigned_building.get_collision_rect()):
                        if hasattr(self, "work"):
                            self.work()
                        else:
                            self.state_machine.change("work")
                    else:
                        self.assigned_building = None
                        self.state_machine.change("idle")
            # si no ha llegado caminar:            
            else:
                if abs(dx) > abs(dy):
                    direction = "right" if dx > 0 else "left"
                else:
                    direction = "down" if dy > 0 else "up"

                move_x = (dx / distance) * self.speed * dt
                move_y = (dy / distance) * self.speed * dt

                # Movimiento en eje X con verificación de colisión
                self.x += move_x
                if self.battlefield:
                    entity_rect = self.get_work_rect()
                    collided = False
                    building_collided = False
                    for building in self.battlefield.buildings:
                        if building.solid and building.collidable:
                            if entity_rect.colliderect(building.get_collision_rect()):
                                collided = True
                                building_collided = True
                                break

                    for entity in self.battlefield.entitys:
                        if entity != self and entity_rect.colliderect(entity.get_work_rect()):
                            collided = True
                            break
                            
                    if not collided and hasattr(self.battlefield, "collision_rects"):
                        for rect in self.battlefield.collision_rects:
                            if entity_rect.colliderect(rect):
                                collided = True
                                building_collided = True
                                break

                    if collided:
                        self.x -= move_x
                        if building_collided:
                            self.waypoints = []
                            self.target_position = None
                            self.state_machine.change("idle")

                # Movimiento en eje Y con verificación de colisión
                self.y += move_y
                if self.battlefield:
                    entity_rect = self.get_work_rect()
                    collided = False
                    building_collided = False
                    for building in self.battlefield.buildings:
                        if building.solid and building.collidable:
                            if entity_rect.colliderect(building.get_collision_rect()):
                                collided = True
                                building_collided = True
                                break

                    for entity in self.battlefield.entitys:
                        if entity != self and entity_rect.colliderect(entity.get_work_rect()):
                            collided = True
                            break
                            
                    if not collided and hasattr(self.battlefield, "collision_rects"):
                        for rect in self.battlefield.collision_rects:
                            if entity_rect.colliderect(rect):
                                collided = True
                                building_collided = True
                                break

                    if collided:
                        self.y -= move_y
                        if building_collided:
                            self.waypoints = []
                            self.target_position = None
                            self.state_machine.change("idle")

                from src import states
                current_state = self.state_machine.current
                if self.waypoints and (not isinstance(current_state, states.entity_states.WalkState) or getattr(current_state, "direction", None) != direction):
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
