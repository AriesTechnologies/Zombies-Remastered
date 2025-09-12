# --- Imports --- #

import pygame
from dataclasses import dataclass


# --- Weapon Class --- #

@dataclass(slots=True, frozen=True)
class Weapon:
        name: str
        damage: int
        max_bullets: int #Magazine Amount


_handgun = Weapon("Handgun", 15, max_bullets=3)
_shotgun = Weapon("Shotgun", 50, max_bullets=2)
_sniper = Weapon("Sniper", 100, max_bullets=1)
_mg = Weapon("Machine Gun", 30, max_bullets=5)
_smg = Weapon("Submachine Gun", 10, max_bullets=8)
_assault_rifle = Weapon("Assault Rifle", 25, max_bullets=6)
weapons = [_handgun, _shotgun, _sniper, _mg, _smg, _assault_rifle]


# --- Bullet Class --- #

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int,int], inverse_speed: bool): #pygame.typing.IntPoint
        super().__init__()

        self.image = pygame.image.load("Images/Bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.speed = 30
        if inverse_speed:
            self.speed = -self.speed
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 1280 or self.rect.x < 0:
            self.kill()
