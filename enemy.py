# --- Imports --- #

import sprites
import random
import pygame

__all__ = ("Enemy", "ATTACK_EVENT")


# --- Variables --- #

ATTACK_EVENT = pygame.event.custom_type()


# --- Enemy Class --- #

class Enemy(pygame.sprite.Sprite):
    def __init__(self, inverse_speed: bool):
        super().__init__()

        self.__animation_int = 0
        self.__images = sprites.load(("Zombie1", "Zombie1_Running"))
        self.image = self.__images[self.__animation_int]
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(0,1280)
        self.rect.y = 530

        self.health = 100
        self.__counter = 0
        self.damage = 30
        self.speed = 3

        self.moving = True
        self.attack = False

    @property
    def dead(self) -> bool:
        return self.health <= 0

    def __movement(self, player_x: int):
        if self.attack or not self.moving or self.dead:
            return
        
        if player_x < self.rect.x:
            self.rect.x -= self.speed
        elif player_x > self.rect.x:
            self.rect.x += self.speed

        self.image = pygame.transform.flip(self.__images[self.__animation_int], (player_x < self.rect.x), False)

    def __animation(self):
        self.__counter += 1

        if self.__counter != 12:
            return
        self.__counter = 0
        self.__animation_int = 0 if self.__animation_int == 1 else 1

    def update(self, player_x: int):
        self.__movement(player_x)
        self.__animation()
