# --- Imports --- #

import pygame
from dataclasses import dataclass


# --- Variables --- #

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255,255,255)
RED = pygame.Color(200,0,0)
GREEN = pygame.Color(50,165,0)
DARK_GREEN = pygame.Color(50,135,0)


# --- Palette Class --- #

@dataclass
class Palette:
    bg_color: pygame.Color
    fg_color: pygame.Color
    active_color: pygame.Color

    @staticmethod
    def to_color(color: tuple[int,int,int]) -> pygame.Color:
        return pygame.Color(*color)
