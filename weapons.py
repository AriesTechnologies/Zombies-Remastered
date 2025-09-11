# --- Imports --- #

import pygame


# --- Weapon Class --- #

class Weapon:
    _gun_dict = {0: "Handgun",
                 1: "Shotgun",
                 2: "Sniper",
                 3: "Machine Gun",
                 4: "Submachine Gun",
                 5: "Assault Rifle"}
    _damage_dict = {"Handgun": 15,
                    "Shotgun": 50,
                    "Sniper": 100,
                    "Machine Gun": 30,
                    "Submachine Gun": 15,
                    "Assault Rifle": 25}
    _bullet_dict = {"Handgun": 3,
                    "Shotgun": 2,
                    "Sniper": 1,
                    "Machine Gun": 5,
                    "Submachine Gun": 8,
                    "Assault Rifle": 6}
        
    def __init__(self):
        self.weapon_int = 0

    @property
    def name(self) -> str:
        return Weapon._gun_dict.get(self.weapon_int)

    @property
    def damage(self) -> int:
        return Weapon._damage_dict.get(self.name,0)

    @property
    def max_bullets(self) -> int:
        return Weapon._bullet_dict.get(self.name,3)

    def get(self):
        self.weapon_int += 1
        if self.weapon_int > 5:
            self.weapon_int = 0


# --- Bullet Class --- #

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, inverse_speed: bool):
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
