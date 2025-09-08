# --- Imports --- #

import sprites
import pygame


# --- Player Class --- #

class Player(pygame.sprite.GroupSingle):
    def __init__(self):
        super().__init__()

        import random
        from weapons import Weapon
        
        character = ""
        match random.randrange(0,4):
            case 0: character = "Nerd"
            case 1: character = "Athlete"
            case 2: character = "ValleyGirl"
            case 3: character = "Rapp"

        self.__walking_list,\
        self.__shooting_list,\
        self.__shooting_HG_list,\
        self.__shooting_SG_list,\
        self.__shooting_SR_list,\
        self.__shooting_MG_list,\
        self.__shooting_SMG_list,\
        self.__shooting_AR_list = sprites.load_all(character)
        
        self.animation_int = 0

        self.sprite = pygame.sprite.Sprite()
        self.images = self.__walking_list
        self.sprite.image = self.images[self.animation_int]
        self.sprite.rect = self.sprite.image.get_rect()

        self.ground = 530
        self.sprite.rect.x = 640
        self.sprite.rect.y = self.ground
        
        self.counter = 0
        self.speed = 0 #10
        self.jump_height = 150
        self.gravity_speed = 5
        self.health = 100
        self.max_health = 100
##        self.damaged_counter = 0
        self.weapon = Weapon()

##        self.moving = False
        self.aiming = False
        self.shooting = False
        self.direction = "Right"

    @property
    def dead(self) -> bool:
        return self.health <= 0

    @property
    def damaged(self) -> bool:
        return self.health < self.max_health

    def die(self):
        self.animation_int = 0
        self.images = self.__walking_list
        self.sprite.image = self.images[self.animation_int]

    def animation(self): #Edit to include checks for gun type and walk whilst aiming, etc.
        self.counter += 1
        if self.counter != 12:
            return
        self.counter = 0
        self.animation_int = 0 if (self.animation_int == 1) or (self.speed == 0) else 1
        self.sprite.image = self.images[self.animation_int]
        if self.direction != "Left":
            return
        self.sprite.image = pygame.transform.flip(self.images[self.animation_int], True, False)
            
    def jump(self):
        if self.sprite.rect.y < self.ground:
            return
        self.sprite.rect.y -= self.jump_height
                
    def gravity(self):
        if self.sprite.rect.y >= self.ground:
            return
        self.sprite.rect.y += self.gravity_speed

    def regen(self):
        if self.dead or not self.damaged:
            return
        self.health += 5
                    
    def change_weapon(self):
        if not self.aiming:
            self.images = self.__walking_list
            return

        match self.weapon.name:
            case "Handgun": self.images = self.__shooting_HG_list
            case "Shotgun": self.images = self.__shooting_SG_list
            case "Sniper": self.images = self.__shooting_SR_list
            case "Machine Gun": self.images = self.__shooting_MG_list
            case "Submachine Gun": self.images = self.__shooting_SMG_list
            case "Assault Rifle": self.images = self.__shooting_AR_list
            case _: self.images = self.__shooting_list

    def events(self, event: pygame.event.Event):
        if self.dead:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.jump()
            if event.key == pygame.K_RIGHT:
                self.direction = "Right"
                if self.sprite.rect.x < 1280:
                    self.speed = 10
                    self.sprite.rect.x += self.speed
            if event.key == pygame.K_LEFT:
                self.direction = "Left"
                if self.sprite.rect.x > 0:
                    self.speed = -10
                    self.sprite.rect.x += self.speed
            if event.key in {pygame.K_RSHIFT, pygame.K_LSHIFT}\
            or (event.mod in {pygame.KMOD_RSHIFT, pygame.KMOD_LSHIFT}):
                self.aiming = True
            if self.aiming and (event.key == pygame.K_SPACE):
                self.shooting = self.aiming
            if event.key == pygame.K_DOWN:
                self.weapon.get()
                
        elif event.type == pygame.KEYUP:
            if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                self.speed = 0
            if event.key in {pygame.K_RSHIFT, pygame.K_LSHIFT}:
                self.aiming = False
            if event.key == pygame.K_SPACE:
                self.shooting = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.shooting = self.aiming
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.shooting = False
                
        self.gravity()
        self.change_weapon()
        self.animation()
        
        if not self.damaged:
            return
        
        self.regen()

    def update(self):
        pass
