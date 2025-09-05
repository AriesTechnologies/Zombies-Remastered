# --- Imports --- #

import sys
import pygame

from background import *
from enemy import *
from player import*
from sprites import *

pygame.init()

# --- Game --- #                                   

global Game
Game = False
global score
score = 0

xsmallfont = pygame.font.SysFont("8-Bit-Madness", 15)
smallfont = pygame.font.SysFont ("8-Bit-Madness", 30)
mediumfont = pygame.font.SysFont ("8-Bit-Madness", 50)
largefont = pygame.font.SysFont ("8-Bit-Madness", 95)
xlargefont = pygame.font.SysFont ("8-Bit-Madness", 105)

black = (0,0,0)
red = (200,0,0)
green = (50,165,0)
dark_green = (50,135,0)
white = (255,255,255)

Display_w = 1280
Display_h = 700
Title = pygame.display.set_caption("Zombies")
display = pygame.display.set_mode((Display_w,Display_h), pygame.RESIZABLE)

clock = pygame.time.Clock()
background = Background()
player = Player()
##enemy = Enemy()
##enemy2 = Enemy()

enemies = pygame.sprite.Group(Enemy(), Enemy())

#Part of Message_To_Screen
def Text_Objects(text: str, color, size: str):
    if size == "xsmall":
        TextSurface = xsmallfont.render (text, True, color)
    elif size == "small":
        TextSurface = smallfont.render (text, True, color)
    elif size == "medium":
        TextSurface = mediumfont.render (text, True, color)
    elif size == "large":
        TextSurface = largefont.render (text, True, color)
    elif size == "xlarge":
        TextSurface = xlargefont.render (text, True, color)
    return TextSurface, TextSurface.get_rect()

#Return a message to be printed to the screen
def message_to_screen(msg, color, x_Pos, x_Displace=0, y_Displace=0, size="small"):
    TextSurf, TextRect = Text_Objects(msg, color, size)
    if x_Pos == 1:
        TextRect.left = (int(Display_w/6)+x_Displace, int(Display_h/2)+y_Displace)
    if x_Pos == 1.5:
        TextRect = (int(Display_w/3)+x_Displace, int(Display_h/2)+y_Displace)
    if x_Pos == 2:
        TextRect.center = (int(Display_w/2)+x_Displace, int(Display_h/2)+y_Displace)
    if x_Pos == 3:
        TextRect.right = (int(Display_w/1.5)+x_Displace, int(Display_h/2)+y_Displace)
    display.blit(TextSurf, TextRect)

#Part of Button
def text_to_button(msg, color, Button_X, Button_Y, Button_w, Button_h, size="small"):
    textSurf, textRect  = Text_Objects(msg, color, size)
    textRect.center = ((Button_X+(Button_w/2)), Button_Y+(Button_h/2))
    display.blit(textSurf, textRect)

#Returns a Button to be printed to screen
def Button(text, x, y, w, h, inactive_color, active_color, action):
    Cursor = pygame.mouse.get_pos()
    if x + w > Cursor[0] > x and y + h > Cursor[1] > y:
        pygame.draw.rect(display, active_color, (x,y,w,h))
    else:
         pygame.draw.rect(display, inactive_color, (x,y,w,h))
    text_to_button(text,white,x,y,w,h)

#Options Screen
def Options():
    background.animation_int = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    break
            
        display.blit(background.image, background.rect.topleft)
        message_to_screen("Instructions:", green, 2, 0, -250, size="xlarge")
        message_to_screen("Right Arrow and Left Arrow Keys: Movement", white, 2, 0, -100, size="medium")
        message_to_screen("Up Arrow Key: Jump", white, 2, 0, -25, size="medium")
        message_to_screen("Down Arrow Key: Change Weapon", white, 2, 0, 50, size="medium")
        message_to_screen("Shift Keys: Aim Weapon", white, 2, 0, 125, size="medium")
        message_to_screen("Spacebar: Shoot Weapon", white, 2, 0, 200, size="medium")
        message_to_screen("©2025 AriesTechnologies", white, 2, 0, 305, size="small")
        pygame.display.flip()

#Updates Screen
def Updates():
    background.animation_int = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    break
            
        display.blit(background.image, background.rect.topleft)
        message_to_screen("Updates:", green, 2, 0, -250, size="xlarge")
##        message_to_screen("Version 1.0.0 Alpha: Fully completed Zombies, bug fixes with weapons", white, 2, 0, -100, size="small")
##        message_to_screen("Version 1.1.0 Alpha: Added in multiple zombies, bug fixes", white, 2, 0, -25, size="small")
##        message_to_screen("Version 1.2.0 Alpha: Added in randomized player type, bug fixes with multiple zombie movements", white, 2, 0, 50, size="small")
##        message_to_screen("Version 1.3.0 Alpha: Added in boundaries on the edges of the screen", white, 2, 0, 125, size="small")
##        message_to_screen("Version 1.3.1 Alpha: Bug fixes with boundaries", white, 2, 0, 200, size="small")
        message_to_screen("©2025 AriesTechnologies", white, 2, 0, 305, size="small")
        pygame.display.flip()

#Title Screen
def __title__():
    background.animation_int = 1
    global Game
    while not Game:
        Cursor = pygame.mouse.get_pos()
        Click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if 536+208 > Cursor[0] > 536 and 371+58 > Cursor[1] > 371:
                if Click[0] == 1:
                    Game = True
                    player.moving = True
                    enemy.moving = True
                    enemy2.moving = True
            elif 540+200 > Cursor[0] > 540 and 440+50 > Cursor[1] > 440:
                if Click[0] == 1:
                    Options()
            elif 540+200 > Cursor[0] > 540 and 505+50 > Cursor[1] > 505:
                if Click[0] == 1:
                    Updates()

        display.blit(background.image, background.rect.topleft)
        message_to_screen("Zombies", green, 2, 0, -250, size="xlarge")
        pygame.draw.rect(display, white, (535,370,210,60))
        pygame.draw.rect(display, white, (535,435,210,60))
        pygame.draw.rect(display, white, (535,500,210,60))
        Button("Play", 536, 371, 208, 58, black, red, action="Play")
        Button("Options", 536, 436, 208, 58, black, red, action="Options")
        Button("Updates", 536, 501, 208, 58, black, red, action="Updates")
        message_to_screen("©2025 AriesTechnologies", white, 2, 0, 305, size="small")
        pygame.display.flip()
        clock.tick(60)

#Pause Screen
def Pause():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    break

        display.fill(black)
        message_to_screen("Paused", red, 2, 0, 0, size="large")
        message_to_screen(f"Score: {score}", white, 2, 0, -75, size="medium")
        pygame.display.flip()
        clock.tick(10)

#Main Game
def __main__():
    background.animation_int = 0
    global Score
    global Game
    Title = pygame.display.set_caption(f"Zombies FPS: {clock.get_fps()}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Pause()

    player.events(event)

##    Runs Player movement, animation, etc.
    player.__main__()
    enemy.__main__(player.rect.x)
    enemy2.__main__(player.rect.x)

    #Checks for Zombie touching Player
    if player.rect.x + 100 >= enemy.rect.x >= player.rect.x and not enemy.dead:
##        player.damaged = True
        enemy.moving = False
        enemy.attack = True
        if player.damaged:
            player.damaged_counter += 1
            if player.damaged_counter >= 8:
                player.health -= enemy.damage
##                player.damaged = False
                player.damaged_counter = 0
                if player.health <= 0:
                    enemy.moving = False
                    player.moving = False
                    Game = False
    else:
##        player.damaged = False
        enemy.moving = True
        enemy.attack = False
##        if player.health < player.max_health:
##            player.regen()

    if player.rect.x + 100 >= enemy2.rect.x >= player.rect.x and not enemy2.dead:
##        player.damaged = True
        enemy2.moving = False
        enemy2.attack = True
        if player.damaged:
            player.damaged_counter += 1
            if player.damaged_counter >= 8:
                player.health -= enemy.damage
##                player.damaged = False
                player.damaged_counter = 0
                if player.health <= 0:
                    enemy2.moving = False
                    player.moving = False
                    Game = False
    else:
##        player.damaged = False
        enemy2.moving = True
        enemy2.attack = False
##        if player.health < player.max_health:
##        player.regen()

    #Checks for bullet touching Enemy
    if enemy.X < player.bullet_X < enemy.X+116 and enemy.Y < player.bullet_Y < enemy.Y+140 and not enemy.dead and not player.bullet_dead:
        if player.shot_counter >= 8:
            enemy.health -= player.weapon_damage
            player.bullet_counter = 0
            player.shot_counter = 0
            del player.bullets_list[:]
            player.bullet_dead = True
            if enemy.health <= 0:
                enemy.dead = True
                enemy.moving = False
                Score += 50

    if enemy2.X < player.bullet_X < enemy2.X+116 and enemy2.Y < player.bullet_Y < enemy2.Y+140 and not enemy2.dead and not player.bullet_dead:
        if player.shot_counter >= 8:
            enemy2.health -= player.weapon_damage
            player.bullet_counter = 0
            player.shot_counter = 0
            del player.bullets_list[:]
            player.bullet_dead = True
            if enemy2.health <= 0:
                enemy2.dead = True
                enemy2.moving = False
                Score += 50

    #Redisplay Background
    display.blit(background.image, background.rect.topleft)

    #Redisplay Player
    if player.direction == "Right":
        display.blit(player.image, player.rect.topleft)
    elif player.direction == "Left":
        display.blit(pygame.transform.flip(player.image, True, False), player.rect.topleft)

    #Redisplay Bullet
    if player.bullet_counter == 1:
        if player.bullet_direction == "Right":
            display.blit(player.bullet[0], (player.bullet_X+110, player.bullet_Y))
        elif player.bullet_direction == "Left":
            display.blit(pygame.transform.flip(player.bullet[0], True, False), (player.bullet_X, player.bullet_Y))

    #Redisplay Zombie
    for enemy in enemies:
        if enemy.dead:
            continue
        if enemy.direction == "Right":
            display.blit(enemy.image, enemy.rect.topleft)
        elif enemy.direction == "Left":
            display.blit(pygame.transform.flip(enemy.image, True, False), enemy.rect.topleft)
            
    message_to_screen(f"Score: {score}", white, 2, -575, -325, size="small")

    pygame.display.flip()
    clock.tick(60)

#After Player Dead
def Death_Screen():
    player.animation_int = 0
##    player.current = sprites.Enemy_Walking_List
    display.fill(black)
    display.blit(player.images[player.animation_int], (Display_w/2-58, player.ground))
    message_to_screen("Game Over!", red, 2, 0, 0, size="xlarge")
    message_to_screen(f"Score: {score}", white, 2, 0, 75, size="medium") #Add score later
    pygame.display.flip()

    while not Game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        clock.tick(60)

while not Game:
    __title__()
    
while Game:
    __main__()

Death_Screen()
