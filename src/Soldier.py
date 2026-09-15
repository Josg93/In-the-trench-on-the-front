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
                        
            for building in self.battlefield.buildings:
                if building != self and getattr(building, "is_enemy", False) != self.is_enemy:
                    dist = ((building.x - self.x) ** 2 + (building.y - self.y) ** 2) ** 0.5
                    if dist < min_dist:
                        min_dist = dist
                        closest_enemy = building
            # Si hay un enemigo en rango, detener el movimiento para enfocar el combate
          
          
            if closest_enemy is not None:
                self.shoot(closest_enemy)
            
        super().update(dt)
    
    def shoot(self, closest_enemy : GameEntity):
        self.waypoints = []
        self.state_machine.change("shoot")
                
        if self.attack_timer <= 0:
            # Infligir daño al enemigo y reiniciar el cooldown
            canal = pygame.mixer.find_channel()
            if self.is_enemy is False:
                canal.play(settings.SOUNDS["shoot1"])
                               
            else:
                canal.play(settings.SOUNDS["shoot2"])
                
            error = random.randint(0,10)    
            closest_enemy.hp -= self.attack_power + error
            self.attack_timer = self.attack_cooldown
        
          

        
    
    def trench(self):
        # Lógica para interactuar con trincheras
        pass
    
    def render(self, surface: Surface, camera: Any) -> None:
        super().render(surface, camera)
