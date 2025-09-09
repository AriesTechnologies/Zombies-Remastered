# --- Imports --- #

import sys
import pygame
from enum import Enum, auto

from gfx import Button, Label, Align, Palette, Text, TextSize, BLACK, GREEN, RED, WHITE
from background import Background
from enemy import Enemy, ATTACK_EVENT
from player import Player, REGEN_EVENT
from weapons import Bullet

pygame.key.set_repeat(225,35)


# --- Variables --- #

display_w = 1280
display_h = 700
display_size = (display_w,display_h)
TITLE = "Zombies: Remastered"

pygame.display.set_caption(TITLE)
display = pygame.display.set_mode(display_size, pygame.RESIZABLE)


# --- Game State Class --- #

class State(Enum):
    MENU = auto()
    GAME = auto()
    PAUSED = auto()


# --- Game --- #

class Game:
    FPS = 60
    
    def __init__(self):
        self.clock = pygame.time.Clock()

        #Timers
        self.enemy_attack_timer = None
        self.player_regen_timer = None

        self.quit = False
        self.debug = True
        self.state = State.MENU
##        self.round = 1
        self.round_enemy_amount = 1
        self.score = 0

        self.ui = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.background = Background()
        self.player = Player()

        self.debug_sprite = Label("FPS: {round(self.clock.get_fps(),2)}", WHITE, TextSize.SMALL, Align.RIGHT, (display_w-5,5))
        
        self.copyright_sprite = Label("©2025 AriesTechnologies", WHITE, TextSize.SMALL)
        self.copyright_sprite.rect.midbottom = display_w//2, display_h-5

        self.menus_path = [self.title_menu]
        self.menus_path[-1]()

    @property
    def game(self) -> bool:
        return self.state == State.GAME

    @property
    def paused(self) -> bool:
        return self.state == State.PAUSED

    @property
    def menu(self) -> bool:
        return self.state == State.MENU

    def title_menu(self):
        self.ui.empty()
        lbl = Label("Zombies", GREEN, TextSize.XLARGE, Align.CENTER, (display_w//2,5))
        self.ui.add(lbl)

        btnTexts = (("Play",self.play), ("Options",self.options_menu), ("Updates",self.updates_menu))
        btnRect = pygame.Rect(536,371,208,58)
        for idx,text in enumerate(btnTexts):
            btn = Button(btnRect.size, text[0], onclick=text[1])
            btn.rect.topleft = btnRect.x, btnRect.y+btnRect.h*idx
            self.ui.add(btn)

        self.ui.add(self.copyright_sprite)

    def options_menu(self):
        self.ui.empty()
        lbl = Label("Instructions:", GREEN, TextSize.XLARGE, Align.CENTER, (display_w//2,5))
        self.ui.add(lbl)

        lbls = ("Right Arrow and Left Arrow Keys: Movement",
                "Up Arrow Key: Jump",
                "Down Arrow Key: Change Weapon",
                "Shift Keys: Aim Weapon",
                "Spacebar: Shoot Weapon"
                )

        for index,label_text in enumerate(lbls):
            lbl = Label(label_text, WHITE, TextSize.MEDIUM, Align.CENTER, (display_w//2,50*index+150)) #(0,0),
            self.ui.add(lbl)

        self.ui.add(self.copyright_sprite)

    def updates_menu(self):
        self.ui.empty()
        lbl = Label("Updates:", GREEN, TextSize.XLARGE, Align.CENTER, (display_w//2,5))
        self.ui.add(lbl)

        self.ui.add(self.copyright_sprite)

    def play(self):
        self.menus_path.clear()
        self.ui.empty()
        self.state = State.GAME
        self.background.animation_int = 0
        self.background.update()

        lbl = Label(f"Score: {self.score}", WHITE, TextSize.SMALL)
        lbl.rect.topleft = (5,5)
        self.ui.add(lbl)

        if self.debug:
            self.ui.add(self.debug_sprite)

        self.enemy_attack_timer = pygame.time.set_timer(ATTACK_EVENT, 750, loops=0) #Every 3/4 seconds
        self.player_regen_timer = pygame.time.set_timer(REGEN_EVENT, 1000, loops=0) #Every second

    def paused_menu(self):
        self.ui.empty()
        lbl = Label("Paused", RED, TextSize.LARGE)
        lbl.rect.center = display_w//2, display_h//2
        self.ui.add(lbl)
        
        lbl1 = Label(f"Score: {self.score}", WHITE, TextSize.MEDIUM)
        lbl1.rect.midbottom = display_w//2, lbl.rect.top
        self.ui.add(lbl1)

    def game_over(self):
        self.ui.empty()
        self.bullets.empty()
        self.enemies.empty()
        self.player.die()
        lbl = Label("Game Over!", RED, TextSize.XLARGE)
        lbl.rect.center = display_w//2, display_h//2
        self.ui.add(lbl)

        lbl1 = Label(f"Score: {self.score}", WHITE, TextSize.MEDIUM)
        lbl1.rect.midtop = lbl.rect.midbottom
        lbl1.rect.y += lbl1.rect.height
        self.ui.add(lbl1)

        self.enemy_attack_timer = pygame.time.set_timer(ATTACK_EVENT, 0, loops=0)
        self.player_regen_timer = pygame.time.set_timer(REGEN_EVENT, 0, loops=0)
        
    def menu_events(self, event: pygame.event.Event):
        buttons = filter(lambda sprite: isinstance(sprite, Button), self.ui)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == State.MENU:
                    return
                self.state = State.GAME
                self.play()
            elif event.key == pygame.K_BACKSPACE:
                if self.menu and len(self.menus_path) > 1:
                    del self.menus_path[-1]
                if len(self.menus_path) > 0:
                    self.menus_path[-1]()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                button = next(filter(lambda button: button.active, buttons), None)
                if button is None:
                    return
                self.menus_path.append(button.onclick)
                self.menus_path[-1]()
                
        for button in buttons:
            button.collide(pygame.mouse.get_pos())
            button.update()

    def game_events(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.player.dead:
                    self.__init__()
                else:
                    self.state = State.PAUSED
                    self.menus_path.append(self.paused_menu)
                    self.menus_path[-1]()
        elif event.type == ATTACK_EVENT:
            for enemy in self.enemies: #Checks for Zombie touching Player
                enemy.attack = pygame.sprite.spritecollide(enemy,self.player,False)
                enemy.moving = not enemy.attack
                if not enemy.attack:
                    continue
                
                self.player.health -= enemy.damage

##            print(self.player.health, enemy.attack)
            if self.player.dead:
                self.menus_path.append(self.game_over)
                self.menus_path[-1]()
             
        if self.player.dead:
            return
        self.player.events(event)

    def events(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.K_F1:
            self.debug = not self.debug
            if self.debug:
                self.ui.add(self.debug_sprite)
            else:
                self.ui.remove(self.debug_sprite)
            
        match self.state:
            case State.MENU | State.PAUSED: self.menu_events(event)
            case State.GAME: self.game_events(event)

    def update(self):
        if self.menu or self.paused or self.player.dead:
            return
        
        if self.player.shooting and len(self.bullets) == 0:
            self.bullets.add(Bullet(self.player.sprite.rect.center,(self.player.direction == "Left")))
        if len(self.enemies) != self.round_enemy_amount:
            self.enemies.add(Enemy((self.player.direction == "Left")))

        for bullet in self.bullets:
            bullet.update()

        for enemy in self.enemies: #Checks for bullet touching Enemy
            enemy.update(self.player.sprite.rect.x)
            if pygame.sprite.groupcollide(self.enemies,self.bullets,False,True):
                enemy.health -= self.player.weapon.damage
                if not enemy.dead:
                    continue
                
                enemy.kill()
                self.score += 50

    def draw(self):
        display.fill(BLACK)
        if not self.paused and not self.player.dead:
            self.background.draw(display)

        if self.game:
            self.player.draw(display)
            self.bullets.draw(display)
            self.enemies.draw(display)
            
        self.ui.draw(display)
        pygame.display.flip()

    def main(self):
        while not self.quit:
            if self.debug:
                self.debug_sprite.text = f"FPS: {round(self.clock.get_fps(),2)}"
            self.events()
            self.update()
            self.draw()
            self.clock.tick(Game.FPS)

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    Game().main()
