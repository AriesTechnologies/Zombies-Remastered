# --- Imports --- #

import sprites
import pygame
from enum import IntEnum, auto
from weapons import Weapon

__all__ = ("Player", "REGEN_EVENT")


# --- Variables --- #

REGEN_EVENT = pygame.event.custom_type()


# --- Direction Enum --- #

class Direction(IntEnum):
    LEFT = auto()
    RIGHT = auto()


# --- Player Class --- #

class Player(pygame.sprite.GroupSingle):
    _characters = ("Nerd", "Athlete", "ValleyGirl", "Rapp")
    
    def __init__(self):
        super().__init__()

        import random
        from weapons import weapons
        
        self.__walking_list,\
        self.__shooting_list,\
        self.__shooting_HG_list,\
        self.__shooting_SG_list,\
        self.__shooting_SR_list,\
        self.__shooting_MG_list,\
        self.__shooting_SMG_list,\
        self.__shooting_AR_list = sprites.load_all(random.choice(Player._characters))
        
        self.__animation_int = 0

        self.sprite = pygame.sprite.Sprite()
        self.__images = self.__walking_list
        self.sprite.image = self.__images[self.__animation_int]
        self.sprite.rect = self.sprite.image.get_rect()

        self.__ground = 530
        self.sprite.rect.x = 640
        self.sprite.rect.y = self.__ground
        
        self.__counter = 0
        self.speed = 5
        self.jump_height = 150
        self.gravity_speed = 5
        self.health = 100
        self.max_health = 100

        self.__weapon_int = 0
        self.weapons = weapons
        
        self.aiming = False
        self.shooting = False
        self.direction = Direction.RIGHT

    @property
    def dead(self) -> bool:
        return self.health <= 0

    @property
    def damaged(self) -> bool:
        return self.health < self.max_health

    @property
    def jumped(self) -> bool:
        return self.sprite.rect.y < self.__ground

    @property
    def weapon(self) -> Weapon:
        return self.weapons[self.__weapon_int]

    @property
    def isInverse(self) -> bool:
        return self.direction == Direction.LEFT

    def die(self):
        self.__animation_int = 0
        self.__images = self.__walking_list
        self.sprite.image = self.__images[self.__animation_int]

    def __animation(self):
        self.__counter += 1
        if self.__counter == 12:
            self.__counter = 0
            self.__animation_int = 0 if (self.__animation_int == 1) or (self.speed == 0) else 1
        self.sprite.image = pygame.transform.flip(self.__images[self.__animation_int], self.isInverse, False)
            
    def __jump(self):        
        if self.sprite.rect.y < self.__ground:
            return
        self.__move(up=True)
                
    def __gravity(self):
        if self.sprite.rect.y >= self.__ground:
            return
        self.sprite.rect.y += self.gravity_speed

    def __regen(self):
        if self.dead or not self.damaged:
            return
        self.health += 5
                    
    def __change_weapon(self):
        if not self.aiming:
            self.__images = self.__walking_list
        else:
            match self.__weapon_int:
                case 0: self.__images = self.__shooting_HG_list
                case 1: self.__images = self.__shooting_SG_list
                case 2: self.__images = self.__shooting_SR_list
                case 3: self.__images = self.__shooting_MG_list
                case 4: self.__images = self.__shooting_SMG_list
                case 5: self.__images = self.__shooting_AR_list
                case _: self.__images = self.__shooting_list

        self.__animation_int = 0
        self.sprite.image = pygame.transform.flip(self.__images[self.__animation_int], self.isInverse, False)

    def __move(self, up=False, down=False, left=False, right=False):
        if right:
            self.direction = Direction.RIGHT
            self.sprite.rect.move_ip(self.speed,0)
        if left:
            self.direction = Direction.LEFT
            self.sprite.rect.move_ip(-self.speed,0)
        if down:
            self.sprite.rect.y += self.gravity_speed
        if up and not self.jumped:
            self.sprite.rect.y -= self.jump_height

        # controls the object such that it cannot leave the screen's viewpoint
        if self.sprite.rect.right > 1280:
            self.sprite.rect.x = 0
        if self.sprite.rect.x < 0:
            self.sprite.rect.right = 1280
        if self.sprite.rect.y >= self.__ground:
            self.sprite.rect.y = self.__ground

        self.__animation()

    def events(self, event: pygame.event.Event):
        if self.dead:
            return
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.__move(up=True)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.__move(left=True)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.__move(right=True)
                
        if event.type == pygame.KEYDOWN:      
            if event.key in {pygame.K_RSHIFT, pygame.K_LSHIFT}:
                self.aiming = True
                self.__change_weapon()
            if (event.mod in {pygame.KMOD_RSHIFT, pygame.KMOD_LSHIFT})\
            and (event.key == pygame.K_SPACE):
                self.shooting = self.aiming
            if event.key in {pygame.K_DOWN, pygame.K_s}:
                self.__weapon_int += 1
                if self.__weapon_int > len(self.weapons)-1:
                    self.__weapon_int = 0
                self.__change_weapon()
                
        elif event.type == pygame.KEYUP:
            if event.key in {pygame.K_RSHIFT, pygame.K_LSHIFT}:
                self.aiming = False
                self.__change_weapon()
            if event.key == pygame.K_SPACE:
                self.shooting = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.shooting = self.aiming
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.shooting = False

        elif event.type == REGEN_EVENT:
            self.__regen()
                
        self.__gravity()

    def update(self):
        pass
