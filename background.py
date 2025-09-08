# --- Imports --- #

import pygame


# --- Background Class --- #

class Background(pygame.sprite.GroupSingle):
    def __init__(self):
        super().__init__()

        import sprites

        self.animation_int = 1
        self.images = sprites.load(("Outside_Mansion", "Inside_Mansion"))
                
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.images[self.animation_int]
        self.sprite.rect = self.sprite.image.get_rect()

    def update(self):
        self.sprite.image = self.images[self.animation_int]
