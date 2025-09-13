# --- Imports --- #

import pygame
from dataclasses import dataclass

__all__ = ("Palette",)


# --- Palette Class --- #

@dataclass(slots=True)
class Palette:
    bg_color: pygame.Color
    fg_color: pygame.Color
    active_color: pygame.Color

    @staticmethod
    def to_color(color: tuple[int,int,int]) -> pygame.Color:
        return pygame.Color(*color)
