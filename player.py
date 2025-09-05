# --- Imports --- #

import sprites
import pygame


# --- Weapon Class --- #

class Weapon:
    _weapon_dict = {0:"Handgun", 1:"Shotgun", 2:"Sniper", 3:"Machine Gun", 4:"Submachine Gun", 5:"Assault Rifle"}
    _weapon_damage_dict = {"Handgun":35, "Shotgun":90, "Sniper":100, "Machine Gun":55, "Submachine Gun":45, "Assault Rifle":60}
        
    def __init__(self):
        self.weapon = "Handgun"
        self.weapon_int = 0

    @property
    def damage(self) -> int:
        self._weapon_damage_dict.get(self.weapon)

    def get(self):
        self.weapon_int += 1
        if self.weapon_int > 5:
            self.weapon_int = 0
        self.weapon = self._weapon_dict.get(self.weapon_int)

        return self.weapon


# --- Bullet Class --- #

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Images/Bullet.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.speed = 30
        self.direction = "Right"
        self.dead = False
        self.shot_counter = 0
        self.counter = 0

    def shot(self, shooting: bool, aiming: bool, direction: int):
        self.shot_counter += 1
        
        if shooting and aiming:
            if self.counter == 0:
##                self.bullets_list.append(self.rect.topleft)
                self.rect.x = self.rect.x
                self.rect.y = self.rect.y + 50
                self.direction = direction
                self.counter += 1
                self.dead = False
                
        if self.direction == "Left" and not self.dead:
            self.rect.x -= self.speed
        elif self.direction == "Right" and not self.dead:
            self.rect.x += self.speed

        if self.counter >= 1:
            if self.rect.x <= 0 or self.rect.x >= 1280:
                self.counter = 0
                self.shot_counter = 0
                del self.bullets_list[:]


# --- Player Class --- #

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        import random
        
        character = ""
        match random.randrange(0,4):
            case 0: character = "Nerd"
            case 1: character = "Athlete"
            case 2: character = "ValleyGirl"
            case 3: character = "Rapp"

        self.__Player_Walking_List,\
        self.__Player_Shooting_Melee_List,\
        self.__Player_Shooting_HG_List,\
        self.__Player_Shooting_SG_List,\
        self.__Player_Shooting_SR_List,\
        self.__Player_Shooting_MG_List,\
        self.__Player_Shooting_SMG_List,\
        self.__Player_Shooting_AR_List = sprites.load_all(character)
        
        self.animation_int = 0
        self.images = self.__Player_Walking_List
        self.image = self.images[self.animation_int]
        self.rect = self.image.get_rect()

        self.rect.x = 640
        self.rect.y = 530
        
        self.counter = 0
        self.ground = 530
        self.direction = "Right"
        self.speed = 10
        self.jump_height = 150
        self.gravity_speed = 5
        self.health = 100
        self.max_health = 100
        self.damaged_counter = 0
        self.bullets_list = []

        self.dead = False
        self.moving = False
        self.aiming = False
        self.shooting = False

    @property
    def damaged(self) -> bool:
        return self.health < self.max_heath

    def animation(self): #Edit to include checks for gun type and walk whilst aiming, etc.
        self.counter += 1

        if self.counter == 5:
            if self.moving_right or self.moving_left:
                self.animation_int = 0 if self.animation_int == 1 else 1
            else:
                self.animation_int = 0
                
            self.counter = 0
            
    def jump(self):
        if self.rect.y <= self.ground:
            return
        self.rect.y -= self.jump_height
                
    def gravity(self):
        if self.rect.y >= self.ground:
            return
        self.rect.y += self.gravity_speed

    def regen(self):
        if self.dead:
            return
        if self.health >= self.max_health:
            return
        self.health += 0.5
                    
    def change_weapon(self):
        self.weapon = self.weapon.get()

        if not self.aiming:
            self.images = self.__Player_Walking_List
            return

        match self.weapon:
            case "Handgun": self.images = self.__Player_Shooting_HG_List
            case "Shotgun": self.images = self.__Player_Shooting_SG_List
            case "Sniper": self.images = self.__Player_Shooting_SR_List
            case "Machine Gun": self.images = self.__Player_Shooting_MG_List
            case "Submachine Gun": self.images = self.__Player_Shooting_SMG_List
            case "Assault Rifle": self.images = self.__Player_Shooting_AR_List
            case _: self.images = self.__Player_Walking_List

    def events(self, event: pygame.event.Event):
        if self.dead:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.jump()
            if event.key == pygame.K_RIGHT:
                if self.rect.x < 1280:
                    self.direction = "Right"
                    self.rect.x += self.speed
            if event.key == pygame.K_LEFT:
                if self.rect.x > 0:
                    self.direction = "Left"
                    self.rect.x -= self.speed
            if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                self.aiming = True
            if event.key == pygame.K_SPACE:
                self.shooting = True
            if event.key == pygame.K_DOWN:
                self.change_weapon()
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                self.aiming = False
            if event.key == pygame.K_SPACE:
                self.shooting = False

        self.gravity()
        
        if not self.damaged:
            return
        
        self.regen()
                
    def __main__(self):

        self.animation()
        self.bullet.shot(self.shooting, self.aiming, self.direction)
##        self.movement()
##        self.jump()
##        self.gravity()
