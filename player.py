# --- Imports --- #

import sprites
import pygame

__all__ = ("Player", "REGEN_EVENT")


# --- Variables --- #

REGEN_EVENT = pygame.event.custom_type()


# --- Player Class --- #

class Player(pygame.sprite.GroupSingle):
    _characters = ("Nerd", "Athlete", "ValleyGirl", "Rapp")
    
    def __init__(self):
        super().__init__()

        import random
        from weapons import Weapon
        
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
        self.weapon = Weapon()
        
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
        self.__animation_int = 0
        self.__images = self.__walking_list
        self.sprite.image = self.__images[self.__animation_int]

    def __animation(self):
        self.__counter += 1
        if self.__counter == 12:
            self.__counter = 0
            self.__animation_int = 0 if (self.__animation_int == 1) or (self.speed == 0) else 1
        self.sprite.image = pygame.transform.flip(self.__images[self.__animation_int],
                                                  (self.direction == "Left"), False)
            
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
            match self.weapon.name:
                case "Handgun": self.__images = self.__shooting_HG_list
                case "Shotgun": self.__images = self.__shooting_SG_list
                case "Sniper": self.__images = self.__shooting_SR_list
                case "Machine Gun": self.__images = self.__shooting_MG_list
                case "Submachine Gun": self.__images = self.__shooting_SMG_list
                case "Assault Rifle": self.__images = self.__shooting_AR_list
                case _: self.__images = self.__shooting_list

        self.__animation_int = 0
        self.sprite.image = pygame.transform.flip(self.__images[self.__animation_int],
                                                  (self.direction == "Left"), False)

    def __move(self, up=False, down=False, left=False, right=False):
        if right:
            self.direction = "Right"
            self.sprite.rect.x += self.speed
        if left:
            self.direction = "Left"
            self.sprite.rect.x -= self.speed
        if down:
            self.sprite.rect.y += self.gravity_speed
        if up:
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
        if keys[pygame.K_UP]:
            self.__move(up=True)
        if keys[pygame.K_LEFT]:
            self.__move(left=True)
        if keys[pygame.K_RIGHT]:
            self.__move(right=True)
                
        if event.type == pygame.KEYDOWN:      
            if event.key in {pygame.K_RSHIFT, pygame.K_LSHIFT}:
                self.aiming = True
                self.__change_weapon()
            if (event.mod in {pygame.KMOD_RSHIFT, pygame.KMOD_LSHIFT})\
            and (event.key == pygame.K_SPACE):
                self.shooting = self.aiming
            if event.key == pygame.K_DOWN:
                self.weapon.get()
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
