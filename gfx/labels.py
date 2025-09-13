# --- Imports --- #

import pygame
from typing import Self
from enum import IntEnum, auto
from .fonts import Text, TextSize

__all__ = ("Align", "Label")


# --- Align Enum --- #

class Align(IntEnum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


# --- Label Class --- #

class Label(pygame.sprite.Sprite):
    def __init__(self, text: str, color: pygame.Color, text_size: TextSize, /, align: Align = Align.LEFT, pos: tuple[int,int] = (0,0)) -> Self: #pos: tuple[int,int], 
        super().__init__()
        
        self._text = text
        self.color = color
        self.text_size = text_size
        self.align = align
        self.pos = pos
        
        self.image, self.rect  = Text(self._text, self.color, self.text_size)

        match self.align:
            case Align.LEFT: self.rect.topleft = self.pos
            case Align.CENTER: self.rect.midtop = self.pos
            case Align.RIGHT: self.rect.topright = self.pos

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> str:
        self._text = text
        self.image, self.rect  = Text(self._text, self.color, self.text_size)

        match self.align:
            case Align.LEFT: self.rect.topleft = self.pos
            case Align.CENTER: self.rect.midtop = self.pos
            case Align.RIGHT: self.rect.topright = self.pos

    def collide(self, pos) -> None: pass
    def update(self) -> None: pass
