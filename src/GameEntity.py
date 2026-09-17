from typing import Any
from src import mixins
from src import states
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
        self.collision_radius = max(self.width, self.height) / 3  # Radio de colisión circular proporcional para evitar solapamiento
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
        if self.waypoints:
            # Medir distancias al waypoint actual
            target_x, target_y = self.waypoints[0]
            entity_center_x = self.x + self.width / 2
            entity_center_y = self.y + self.height / 2
            dx = target_x - entity_center_x
            dy = target_y - entity_center_y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            # Umbral de llegada optimizado (10.0 px) para prevenir oscilaciones por imprecisión flotante
            arrival_threshold = 10.0
            if distance < arrival_threshold:
                self.waypoints.pop(0)
                if not self.waypoints:
                    self.target_position = None
                    if self.assigned_building and (
                        getattr(self, "assigned_slot", None) or self.get_collision_rect().colliderect(self.assigned_building.get_collision_rect())):
                        if hasattr(self, "work"):
                            self.work()
                        
                    else:
                        if self.assigned_building and hasattr(self.assigned_building, "free_slot"):
                            self.assigned_building.free_slot(self)
                        self.assigned_building = None
                        self.assigned_slot = None
                        self.state_machine.change("idle")
            
            # Caminata hacia el destino con control anti-convulsión y debouncing de dirección
            else:
                
                current_state = self.state_machine.current
                current_direction = getattr(current_state, "direction", None) if isinstance(current_state, states.entity_states.WalkState) else None

                # Inicializar temporizadores de conteo delta para evitar cambios de dirección convulsivos a 60 FPS
                if not hasattr(self, "direction_timer"):
                    self.direction_timer = 0.0

                self.direction_timer += dt

                # Histéresis mejorada con umbral para prevenir parpadeos en diagonales
                threshold = 8.0
                if current_direction in ["left", "right"]:
                    if abs(dy) > abs(dx) + threshold:
                        candidate_direction = "down" if dy > 0 else "up"
                    else:
                        candidate_direction = "right" if dx > 0 else "left"
                elif current_direction in ["up", "down"]:
                    if abs(dx) > abs(dy) + threshold:
                        candidate_direction = "right" if dx > 0 else "left"
                    else:
                        candidate_direction = "down" if dy > 0 else "up"
                else:
                    if abs(dx) > abs(dy):
                        candidate_direction = "right" if dx > 0 else "left"
                    else:
                        candidate_direction = "down" if dy > 0 else "up"

                # Calcular velocidad de Seek hacia el waypoint
                seek_vx = (dx / distance) * self.speed
                seek_vy = (dy / distance) * self.speed

                # Calcular fuerza de Separation por Steering
                sep_x, sep_y = self._compute_separation_force()

                # Combinar fuerzas (Blended Steering: Seek + Separation con peso 0.6)
                separation_weight = 0.6
                final_vx = seek_vx + sep_x * separation_weight
                final_vy = seek_vy + sep_y * separation_weight

                # Aplicar movimiento fluido con dt
                self.x += final_vx * dt
                self.y += final_vy * dt

                # Debouncing y control de frecuencia: solo actualiza la dirección de la máquina de estados 
                # si la nueva dirección difiere tras un intervalo de tiempo (0.15s), eliminando parpadeos y tirones visuales.
                if candidate_direction != current_direction:
                    if self.direction_timer >= 0.15:
                        self.direction_timer = 0.0
                        self.state_machine.change("walk", direction=candidate_direction)
                else:
                    self.direction_timer = 0.0

    def _compute_separation_force(self) -> tuple[float, float]:
        """
        Calcula una fuerza de separación basada en los rectángulos de colisión (collision_rect).
        Permite que las unidades se organicen de forma ortogonal/cuadrada sin solaparse.
        """
        if not self.battlefield or not hasattr(self.battlefield, "entitys"):
            return 0.0, 0.0

        self_rect = self.get_collision_rect()
        # Inflar el rectángulo de colisión para crear un margen de proximidad (padding)
        padded_rect = self_rect.inflate(16, 16)

        sep_x = 0.0
        sep_y = 0.0
        neighbor_count = 0

        self_center_x = self_rect.centerx
        self_center_y = self_rect.centery

        for other in self.battlefield.entitys:
            if other == self:
                continue
            if not hasattr(other, "get_collision_rect"):
                continue

            other_rect = other.get_collision_rect()
            if padded_rect.colliderect(other_rect):
                other_center_x = other_rect.centerx
                other_center_y = other_rect.centery

                dx = self_center_x - other_center_x
                dy = self_center_y - other_center_y
                distance = (dx ** 2 + dy ** 2) ** 0.5

                if distance > 0:
                    strength = self.speed * 1.2
                    sep_x += (dx / distance) * strength
                    sep_y += (dy / distance) * strength
                    neighbor_count += 1
                else:
                    sep_x += self.speed
                    neighbor_count += 1

        if neighbor_count > 0:
            sep_x /= neighbor_count
            sep_y /= neighbor_count

        return sep_x, sep_y

    def update(self, dt: float) -> None:
        self.movement(dt)
        self.state_machine.update(dt)
        super().update(dt)

    def render(self, surface: pygame.Surface, camera: Any) -> None:
        super().render(surface, camera)
        if self.selected:
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

            #dest = camera.apply(pygame.Rect(self.x, self.y, self.width, self.height))
            #pygame.draw.rect(surface, (0, 255, 0), dest, 2)

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
