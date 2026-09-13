from typing import Any
from pygame import Surface
from src.GameEntity import GameEntity 
import pygame

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
                 is_enemy: bool = False,
                 hp: int = 100,
                 attack_power: int = 15,
                 attack_range: float = 150.0,
                 attack_cooldown: float = 1.0) -> None:
        super().__init__(x, y, width, height, texture_id, animations, speed, battlefield, entity_type)
        self.is_enemy = is_enemy
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power
        self.attack_range = attack_range
        self.attack_cooldown = attack_cooldown
        self.attack_timer = 0.0

    def update(self, dt: float) -> None:
        # Reducir el temporizador de ataque en cada frame
        if self.attack_timer > 0:
            self.attack_timer -= dt

        # Lógica de combate: buscar enemigos en el campo de batalla
        if self.battlefield and hasattr(self.battlefield, "entitys"):
            closest_enemy = None
            min_dist = self.attack_range

            for entity in self.battlefield.entitys:
                # Una entidad es enemiga si su bando (is_enemy) difiere del nuestro
                if entity != self and getattr(entity, "is_enemy", False) != self.is_enemy:
                    dist = ((entity.x - self.x) ** 2 + (entity.y - self.y) ** 2) ** 0.5
                    if dist < min_dist:
                        min_dist = dist
                        closest_enemy = entity

            if closest_enemy is not None:
                # Si hay un enemigo en rango, detener el movimiento para enfocar el combate
                self.waypoints = []
                if self.attack_timer <= 0:
                    # Infligir daño al enemigo y reiniciar el cooldown
                    closest_enemy.hp -= self.attack_power
                    self.attack_timer = self.attack_cooldown

            # Limpiar del campo de batalla a todas las entidades cuya vida (HP) sea <= 0
            self.battlefield.entitys = [e for e in self.battlefield.entitys if getattr(e, "hp", 100) > 0]

        super().update(dt)
    
    def shoot(self):
        # Lógica opcional para animación de disparo
        pass
    
    def trench(self):
        # Lógica para interactuar con trincheras
        pass
    
    def render(self, surface: Surface, camera: Any) -> None:
        super().render(surface, camera)
