# --- Imports --- #

import pygame
pygame.init()
pygame.freetype.init()

__all__ = ("font", "text_obj")


# --- Variables --- #

font_path = "fonts/Eight-Bit-Madness.ttf"
font = pygame.freetype.Font(font_path, 15)


#Part of Message_To_Screen
def text_obj(text: str, color: pygame.Color, size: str):
    match size:
        case "xsmall": font.size = 15
        case "small": font.size = 30
        case "medium": font.size = 50
        case "large": font.size = 95
        case "xlarge": font.size = 105
    return font.render(text, color)
