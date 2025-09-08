# --- Imports --- #

import pygame
from typing import Self
from palette import Palette, BLACK, WHITE, RED
from fonts import font, text_obj


# --- Button Class --- #

class Button(pygame.sprite.Sprite):
    """A button widget"""

    _palette: Palette = Palette(BLACK, WHITE, RED)
    
    def __init__(self, size: tuple[int,int], text: str = "") -> Self:
        super().__init__()

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()

        self._active = False
        self._text = text

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
        textSurf, textRect  = text_obj(self.text, Button._palette.fg_color, "small")
        textRect.center = pygame.Vector2(self.rect.size)//2 #self.rect.w//2, self.rect.h//2
        self.image.blit(textSurf, textRect)

