# --- Imports --- #

import pygame
from typing import Self
from .fonts import text_obj


# --- Label Class --- #

class Label(pygame.sprite.Sprite):
    def __init__(self, text: str, color: pygame.Color, text_size: str) -> Self: #pos: tuple[int,int], 
        super().__init__()
        
        self.text = text
        self.color = color
        self.text_size = text_size
        
        self.image, self.rect  = text_obj(self.text, self.color, self.text_size)
##        self.rect.topleft = pos

    def collide(self, pos) -> None: pass
    def update(self) -> None: pass
