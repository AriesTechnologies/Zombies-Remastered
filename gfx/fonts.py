# --- Imports --- #

import pygame
from enum import IntEnum

pygame.init()
pygame.freetype.init()

__all__ = ("font", "Text", "TextSize")


# --- Variables --- #

font_path = "fonts/Eight-Bit-Madness.ttf"
font = pygame.freetype.Font(font_path, 15)


# --- TextSize Enum --- #

class TextSize(IntEnum):
    XSMALL = 15
    SMALL = 30
    MEDIUM = 50
    LARGE = 95
    XLARGE = 105


#Part of Message_To_Screen
def Text(text: str, color: pygame.Color, size: TextSize):
    match size:
        case TextSize.XSMALL: font.size = 15
        case TextSize.SMALL: font.size = 30
        case TextSize.MEDIUM: font.size = 50
        case TextSize.LARGE: font.size = 95
        case TextSize.XLARGE: font.size = 105
    return font.render(text, color)
