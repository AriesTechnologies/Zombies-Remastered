# --- Imports --- #

import pygame
from typing import Self
from enum import IntEnum, auto
from .fonts import Text, TextSize


# --- Alignment Enum --- #

class Alignment(IntEnum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


# --- Label Class --- #

class Label(pygame.sprite.Sprite):
    def __init__(self, text: str, color: pygame.Color, text_size: TextSize, /, align: Alignment = Alignment.LEFT, pos: tuple[int,int] = (0,0)) -> Self: #pos: tuple[int,int], 
        super().__init__()
        
        self.text = text
        self.color = color
        self.text_size = text_size
        self.align = align
        
        self.image, self.rect  = Text(self.text, self.color, self.text_size)

        match self.align:
            case Alignment.LEFT: self.rect.topleft = pos
            case Alignment.CENTER: self.rect.midtop = pos
            case Alignment.RIGHT: self.rect.topright = pos

    def collide(self, pos) -> None: pass
    def update(self) -> None: pass
