# --- Imports --- #

import sys
import pygame

from gfx import Button, Label, Palette, text_obj, BLACK, GREEN, RED, WHITE
from background import Background
from enemy import Enemy
from player import Player
from weapons import Bullet

pygame.key.set_repeat(225,35)


# --- Variables --- #

display_w = 1280
display_h = 700
display_size = (display_w,display_h)
pygame.display.set_caption("Zombies")
display = pygame.display.set_mode(display_size, pygame.RESIZABLE)


# --- Definitions --- #

def message_to_screen(msg: str, color: pygame.Color, x_pos: int, x_Displace: int = 0, y_Displace: int = 0, size: str = "small"):
    textSurf, textRect = text_obj(msg, color, size)
    match x_pos:
        case 1: textRect.left = (display_w//6+x_Displace, display_h//2+y_Displace)
        case 1.5: textRect = (display_w//3+x_Displace, display_h//2+y_Displace)
        case 2: textRect.center = (display_w//2+x_Displace, display_h//2+y_Displace)
        case 3: textRect.right = (display_w//1.5+x_Displace, display_h//2+y_Displace)
##    textRect.topleft = pos
    display.blit(textSurf, textRect)


# --- Game --- #

class Game:
    FPS = 60
    
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.menus_path = [self.title_menu]
        self.menu = pygame.sprite.Group()

        self.round = 1
        self.round_enemy_amount = 5
        self.score = 0

        self.background = Background()
        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.quit = False
        self.paused = False
        self.game = False

        self.score_sprite_small = Label(f"Score: {self.score}", WHITE, "small")

        self.score_sprite = Label(f"Score: {self.score}", WHITE, "medium")

        self.menus_path[-1]()

    def title_menu(self):
        self.menu.empty()
        lbl = Label("Zombies", GREEN,  "xlarge") #(0,0), 
        lbl.rect.x = display_w//2-lbl.rect.w//2
        self.menu.add(lbl)

        btnTexts = ("Play", "Options", "Updates")
        btnRect = pygame.Rect(536,371,208,58)
        for idx,text in enumerate(btnTexts):
            btn = Button(btnRect.size, text)
            btn.rect.x = btnRect.x
            btn.rect.y = btnRect.y+btn.rect.h*idx
            self.menu.add(btn)

    def options_menu(self):
        self.menu.empty()
        lbl = Label("Instructions:", GREEN, "xlarge") #(0,0), 
        lbl.rect.x = display_w//2-lbl.rect.w//2
        self.menu.add(lbl)

        lbls = ("Right Arrow and Left Arrow Keys: Movement",
                "Up Arrow Key: Jump",
                "Down Arrow Key: Change Weapon",
                "Shift Keys: Aim Weapon",
                "Spacebar: Shoot Weapon"
                )

        for index,label_text in enumerate(lbls):
            lbl = Label(label_text, WHITE, "medium") #(0,0), 
            lbl.rect.x = display_w//2-lbl.rect.w//2
            lbl.rect.y = 50*index+150 #Insert random number currently
            self.menu.add(lbl)

    def updates_menu(self):
        self.menu.empty()
        lbl = Label("Updates:", GREEN, "xlarge") #(0,0), 
        lbl.rect.x = display_w//2-lbl.rect.w//2
        self.menu.add(lbl)

    def paused_menu(self):
        self.menu.empty()
        lbl = Label("Paused", RED, "large") #(0,0), 
        lbl.rect.center = display_w//2, display_h//2
        self.menu.add(lbl)

        lbl1 = Label(f"Score: {self.score}", WHITE, "medium") #(0,0), 
        lbl1.rect.x = display_w//2-lbl1.rect.w//2
        lbl1.rect.y = display_h//2-lbl.rect.h
        self.menu.add(lbl1)

    def events(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if self.game and event.key == pygame.K_ESCAPE:
                self.game = False
                self.paused = True
                self.menus_path.append(self.paused_menu)
                self.menus_path[-1]()
            elif not self.game and event.key in {pygame.K_ESCAPE, pygame.K_BACKSPACE}:
                if len(self.menus_path) > 1:
                    del self.menus_path[-1]
                if self.paused:
                    del self.menus_path[-1]
                    self.paused = False
                    self.game = True
                if len(self.menus_path) > 0:
                    self.menus_path[-1]()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not self.game and event.button == 1:
                buttons = tuple(self.menu.sprites())[1:]
                if buttons[0].active:
                    self.menus_path.clear()
                    self.game = True
                    self.background.animation_int = 0
                    self.background.update()
                elif buttons[1].active:
                    self.menus_path.append(self.options_menu)
                    self.menus_path[-1]()
                elif buttons[2].active:
                    self.menus_path.append(self.updates_menu)
                    self.menus_path[-1]()
                    
        if not self.game:
            buttons = tuple(self.menu.sprites())[1:]
            cur_pos = pygame.mouse.get_pos()
            for button in buttons:
                button.collide(cur_pos)
                button.update()
            return
        if self.player.dead:
            return
                
        self.player.events(event)
        if self.player.shooting and len(self.bullets) == 0:
            self.bullets.add(Bullet(self.player.sprite.rect.center,(self.player.direction == "Left")))
        if len(self.enemies) == 0:
            self.enemies.add(Enemy((self.player.direction == "Left")))

        for bullet in self.bullets:
            bullet.update()
            
        for enemy in self.enemies:
            enemy.update(self.player.sprite.rect.x)

        for enemy in self.enemies: #Checks for bullet touching Enemy
            if enemy.dead:
                continue
            if pygame.sprite.groupcollide(self.enemies,self.bullets,False,True):
                enemy.health -= self.player.weapon.damage
                if not enemy.dead:
                    continue
                
                enemy.kill()
                self.score += 50

        for enemy in self.enemies: #Checks for Zombie touching Player
            enemy.attack = pygame.sprite.spritecollide(enemy,self.player,False)
            enemy.moving = not enemy.attack
            if not enemy.attack:
                continue
            
            self.player.health -= enemy.damage
            if self.player.dead:
                self.player.die()

    def draw(self):
        display.fill(BLACK)
        self.background.draw(display)

        if not self.game:
            if self.paused:
                display.fill(BLACK)
            self.menu.draw(display)
            if not self.paused:
                message_to_screen("©2025 AriesTechnologies", WHITE, 2, 0, 305, size="small")
        else:
            if self.player.dead:
                display.fill(BLACK)
                self.player.draw(display)
                message_to_screen("Game Over!", RED, 2, 0, 0, size="xlarge")
                message_to_screen(f"Score: {self.score}", WHITE, 2, 0, 75, size="medium") #Add score later
            else:
                self.player.draw(display)
                self.bullets.draw(display)
                self.enemies.draw(display)
##                message_to_screen(f"Score: {self.score}", WHITE, (0,0), size="small")
                message_to_screen(f"Score: {self.score}", WHITE, 2, -575, -325, size="small")

        pygame.display.flip()

    def main(self):
        while not self.quit:
            pygame.display.set_caption(f"Zombies FPS: {round(self.clock.get_fps(),2)}")
            self.events()
            self.draw()
            self.clock.tick(Game.FPS)

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    Game().main()
