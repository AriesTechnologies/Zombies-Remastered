# --- Imports --- #

import pygame
from typing import Iterable


# --- Definition --- #

def load(image_paths: Iterable[str]) -> list[pygame.Surface]:
    return [pygame.image.load(f"images/{image_path}.png").convert_alpha()
                           for image_path in image_paths]

def load_all(character: str) -> list[list[pygame.Surface]]:
    return [load((character, f"{character}_Running")),
            load((f"{character}_Shooting",)),
            load((f"{character}_Shooting_Handgun",f"{character}_Shooting_Handgun_Running")),
            load((f"{character}_Shooting_Shotgun", f"{character}_Shooting_Shotgun_Running")),
            load((f"{character}_Shooting_Sniper", f"{character}_Shooting_Sniper_Running")),
            load((f"{character}_Shooting_Machine_Gun", f"{character}_Shooting_Machine_Gun_Running")),
            load((f"{character}_Shooting_Submachine_Gun", f"{character}_Shooting_Submachine_Gun_Running")),
            load((f"{character}_Shooting_Assault_Rifle", f"{character}_Shooting_Assault_Rifle_Running"))]
