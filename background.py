# --- Imports --- #

import pygame


# --- Background Class --- #

class Background(pygame.sprite.GroupSingle):
    _images = None
    
    def __init__(self):
        super().__init__()
        
        self.__animation_int = 1
                
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Background._images[self.__animation_int]
        self.sprite.rect = self.sprite.image.get_rect()

    def update(self, animation_int: int):
        self.__animation_int = animation_int
        self.sprite.image = Background._images[self.__animation_int]
