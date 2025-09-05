# --- Imports --- #

import sprites
import random
import pygame

# --- Enemy Class --- #

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.animation_int = 0
        self.images = sprites.load(("Zombie1", "Zombie1_Running"))
        self.image = self.images[self.animation_int]
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(0,1280)
        self.rect.y = 530

        self.direction = "Right"
        self.damage = 30
        self.speed = 5
        self.health = 100
        self.counter = 0
        self.wait_counter = 0

        self.moving = False
        self.dead = False
        self.attack = False

    def movement(self, player_x: int):
        if self.attack or not self.moving or self.dead:
            return
        
        if Player_X < self.rect.x:
            self.direction = "Left"
            self.rect.x -= self.speed
        elif Player_X > self.rect.x:
            self.direction = "Right"
            self.rect.x += self.speed

    def animation(self):
        self.counter += 1

        if self.counter == 10:
            if self.moving:
                self.animation_int = 0 if self.animation_int == 1 else 1

                if self.dead:
                    self.moving = False
                    self.wait_counter += 1
                    if self.wait_counter == 8:
                        self.x = random.randrange(0,1280)
                        self.health = 100
                        self.dead = False
                        self.moving = False
                        self.wait_counter = 0
            else:
                if self.dead and not self.moving:
                    self.wait_counter += 1
                    if self.wait_counter == 8:
                        self.moving = True
                        self.wait_counter = 0

            self.counter = 0 

    def __main__(self, player_x: int):
        self.animation()
        self.movement(player_x)
