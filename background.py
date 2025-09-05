# --- Imports --- #

import pygame


# --- Background Class --- #

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        import sprites

        self.animation_int = 1
        self.images = sprites.load(("Outside_Mansion", "Inside_Mansion"))
        self.image = self.images[self.animation_int]
        self.rect = self.image.get_rect()
    
