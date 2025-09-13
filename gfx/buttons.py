# --- Imports --- #

import pygame
from typing import Self, Callable
from .palette import Palette
from .colors import BLACK, WHITE, RED
from .fonts import font, Text, TextSize

__all__ = ("Button",)


# --- Button Class --- #

class Button(pygame.sprite.Sprite):
    """A button widget"""

    _palette: Palette = Palette(BLACK, WHITE, RED)
    
    def __init__(self, size: tuple[int,int], text: str = "", *, onclick: Callable = None) -> Self:
        super().__init__()

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()

        self._active = False
        self._text = text
        self.onclick = onclick

        self.update()
        
    @property
    def active(self) -> bool:
        return self._active
        
    @property
    def text(self) -> str:
        return self._text
        
    @text.setter
    def text(self, text) -> None:
        self._text = text

    @property
    def color(self) -> pygame.Color:
        return Button._palette.active_color if self.active else Button._palette.bg_color

    def collide(self, pos):
        self._active = self.rect.collidepoint(pos)
        self.update()
        return self._active

    def update(self) -> None:
        self.image.fill(self.color)
        pygame.draw.rect(self.image, Button._palette.fg_color, ((0,0),self.rect.size), width = 1)

        font.size = 30
        textSurf, textRect  = Text(self.text, Button._palette.fg_color, TextSize.SMALL)
        textRect.center = pygame.Vector2(self.rect.size)//2
        self.image.blit(textSurf, textRect)

