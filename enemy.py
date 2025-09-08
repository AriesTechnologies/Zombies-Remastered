# --- Imports --- #

import sprites
import random
import pygame

# --- Enemy Class --- #

class Enemy(pygame.sprite.Sprite):
    def __init__(self, inverse_speed: bool):
        super().__init__()

        self.animation_int = 0
        self.images = sprites.load(("Zombie1", "Zombie1_Running"))
        self.image = self.images[self.animation_int]
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(0,1280)
        self.rect.y = 530

        self.health = 100
        self.counter = 0
        self.wait_counter = 0
        self.damage = 30
        self.speed = 0
        if inverse_speed:
            self.image = pygame.transform.flip(self.image, True, False)

        self.moving = True
##        self.dead = False
        self.attack = False

    @property
    def dead(self) -> bool:
        return self.health <= 0

    def movement(self, player_x: int):
        if self.attack or not self.moving or self.dead:
            return
        
        if player_x < self.rect.x:
            self.speed = -5
        elif player_x > self.rect.x:
            self.speed = 5
        self.rect.x += self.speed

    def animation(self):
        self.counter += 1

        if self.counter != 12:
            return
        if not self.moving:
            return

        self.counter = 0
        self.animation_int = 0 if self.animation_int == 1 else 1
        self.image = self.images[self.animation_int]
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, player_x: int):
        self.movement(player_x)
        self.animation()
