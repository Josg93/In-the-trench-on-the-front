from typing import Any
from pygame import Surface
from src.GameEntity import GameEntity 
import pygame
import settings

import random

class Soldier(GameEntity):
    """
    Representa una unidad de combate (soldado amigo o enemigo) capaz de detectar
    objetivos enemigos dentro de su rango de ataque, disparar/atacar y gestionar su salud (HP).
    """
    def __init__(self,
                 x: float,
                 y: float, 
                 width: float, 
                 height: float, 
                 texture_id: str, 
                 animations: dict, 
                 speed: float = 60, 
                 battlefield: Any = None, 
                 entity_type: str = "Soldier",
                 waypoints : list = [],
                 target_position: tuple = None,  
                 is_enemy: bool = False,
                 hp: int = 100,
                 attack_power: int = 15,
                 attack_range: float = 1000,
                 attack_cooldown: float = 1.0) -> None:
        super().__init__(x, y, width, height, texture_id, animations, speed, battlefield, entity_type, waypoints, target_position)
        self.is_enemy = is_enemy
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power
        self.attack_range = attack_range
        self.attack_cooldown = attack_cooldown
        self.attack_timer = 0.0
        self.current_target = None
        self.previous_waypoints = []
        self.previous_target_position = None
        self.trench_state = None
        self.pending_slot = None
        self.exit_destination = None
        self.is_working = False


    def update(self, dt: float) -> None:
        
        # Manejo de estados de trinchera (entrada, interior y salida)
        if self.trench_state == "moving_to_door":
            if not self.waypoints:
                self.trench_state = "entering"
                if self.pending_slot:
                    slot_pos = self.pending_slot["pos"]
                    from gale.timer import Tween
                    Tween(0.6, [(self, {"x": slot_pos[0], "y": slot_pos[1]})], on_complete=self._finish_entering_trench)
            else:
                super().update(dt)
            return
        elif self.trench_state == "entering" or self.trench_state == "exiting":
            return
        elif self.trench_state == "in_trench":
            if self.attack_timer > 0:
                self.attack_timer -= dt
            if self.battlefield and hasattr(self.battlefield, "entitys"):
                if self.current_target is not None:
                    if self._is_alive_and_in_range(self.current_target):
                        self.shoot(self.current_target)
                    else:
                        self.current_target = None
                else:
                    closest_enemy = None
                    min_dist = self.attack_range
                    for entity in self.battlefield.entitys:
                        if entity != self and getattr(entity, "is_enemy", False) != self.is_enemy:
                            dist = ((entity.x - self.x) ** 2 + (entity.y - self.y) ** 2) ** 0.5
                            if dist < min_dist:
                                min_dist = dist
                                closest_enemy = entity
                    if closest_enemy is not None:
                        self.current_target = closest_enemy
                        self.shoot(closest_enemy)
            super().update(dt)
            return
        
        self.looking_enemies(dt)
        super().update(dt)
        
        

    def _is_alive_and_in_range(self, entity: 'GameEntity') -> bool:
        """Verifica si el objetivo sigue vivo y dentro del rango de ataque."""
        if not hasattr(entity, "x") or not hasattr(entity, "y"):
            return False
        if entity.hp <= 0:
            return False
        dist = ((entity.x - self.x) ** 2 + (entity.y - self.y) ** 2) ** 0.5
        return dist <= self.attack_range

    def _save_previous_state(self) -> None:
        """Guarda la ruta y posición objetivo actual antes de iniciar el combate."""
        self.previous_waypoints = list(self.waypoints)
        self.previous_target_position = self.target_position

    def _restore_previous_state(self) -> None:
        """Restaura la ruta y posición objetivo previa cuando el combate finaliza."""
        self.waypoints = list(self.previous_waypoints)
        self.target_position = self.previous_target_position
        self.previous_waypoints = []
        self.previous_target_position = None
        self.trench_state = None
        self.pending_slot = None
        self.exit_destination = None

    def shoot(self, closest_enemy : GameEntity):
        """Detiene el movimiento y ejecuta el ataque/disparo contra el objetivo actual."""
        self.waypoints = []
        self.state_machine.change("shoot")
                
        if self.attack_timer <= 0:
            # Infligir daño al enemigo y reiniciar el cooldown
            canal = pygame.mixer.find_channel(True)
            shoot = random.randint(0,1)
            if shoot == 0:
                canal.play(settings.SOUNDS["shoot1"])
            else:
                canal.play(settings.SOUNDS["shoot2"])
                
            error = random.randint(0,10)    
            closest_enemy.hp -= self.attack_power + error
            self.attack_timer = self.attack_cooldown
    
    def looking_enemies(self , dt :float):
        # Reducir el temporizador de ataque en cada frame
        if self.attack_timer > 0:
            self.attack_timer -= dt

        # Lógica de combate: mantener objetivo seleccionado hasta que muera o se aleje
        if self.battlefield and hasattr(self.battlefield, "entitys"):
            # Si hay un objetivo actual y aún está vivo y en rango, continuar atacándolo
            if self.current_target is not None:
                if self._is_alive_and_in_range(self.current_target):
                    self.shoot(self.current_target)
                    super().update(dt)
                    return
                else:
                    # El objetivo actual ha muerto o salió del rango:
                    # Liberar el objetivo y restaurar el estado/ruta previa
                    self.current_target = None
                    self._restore_previous_state()
                    
                    # Si es una unidad enemiga y tras eliminar su objetivo no le quedan waypoints,
                    # reasignar tarea original: continuar avanzando hacia el objetivo final (borde izquierdo x = 0).
                    if self.is_enemy and not self.waypoints and self.battlefield and hasattr(self.battlefield, "find_path"):
                        target_edge = (0, self.y)
                        waypoints = self.battlefield.find_path((self.x, self.y), target_edge)
                        if waypoints:
                            self.waypoints = waypoints
                            self.target_position = target_edge

            # Buscar un nuevo objetivo solo si la unidad no tiene un objetivo actual
            closest_enemy = None
            min_dist = self.attack_range

            for entity in self.battlefield.entitys:
                # Una entidad es enemiga si su bando (is_enemy) difiere del nuestro
                if entity != self and getattr(entity, "is_enemy", False) != self.is_enemy:
                    dist = ((entity.x - self.x) ** 2 + (entity.y - self.y) ** 2) ** 0.5
                    if dist < min_dist:
                        min_dist = dist
                        closest_enemy = entity

            for building in self.battlefield.buildings:
                if building != self and getattr(building, "is_enemy", False) != self.is_enemy:
                    dist = ((building.x - self.x) ** 2 + (building.y - self.y) ** 2) ** 0.5
                    if dist < min_dist:
                        min_dist = dist
                        closest_enemy = building

            if closest_enemy is not None:
                self.current_target = closest_enemy
                self._save_previous_state()

            if self.current_target is not None:
                self.shoot(self.current_target)
            else:
                super().update(dt)
            return
    
    def work(self):
        self.trench()
        
    def trench(self):
        if self.assigned_slot:
            slot_pos = self.assigned_slot["pos"]
            self.x = slot_pos[0]
            self.y = slot_pos[1]
            self.is_working = True
            self.state_machine.change("idle")

    def stop_working(self):
        if self.is_working:
            self.is_working = False
            if self.assigned_building and hasattr(self.assigned_building, "free_slot"):
                self.assigned_building.free_slot(self)
            self.assigned_building = None
            self.assigned_slot = None
            self.state_machine.change("idle")
    
    def render(self, surface: Surface, camera: Any) -> None:
        super().render(surface, camera)
