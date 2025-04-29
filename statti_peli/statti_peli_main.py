# statti peli
 
import sys
import pygame
import math
import random
import threading
import screeninfo

import battle

pygame.init()

fps = 60.0
fpsClock = pygame.time.Clock()

# Set up the window.
screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)

buttonfont = pygame.font.SysFont("Droid sans monoregular", 45)

DX = 0
DY = 1
X = 0
Y = 1

w, h = screen.get_size()
play_area = pygame.Rect(0, 0, 10, 10)
play_area.center = [w*0.5, h*0.5]
play_area_offset = [w*0.5, h*0.5]

time_list = []

def clamp(sx, bx, x):
    rx = min(max(x, sx), bx)
    return rx

def cycle(max, x):
    if x + 1 > max:
        return 0
    else:
        return x+1

def text(pos, text, font=buttonfont):
    label = buttonfont.render(str(text), 1, (0, 0, 0))
    screen.blit(label, pos)

class Button:
    def __init__(self, txt, pos, font):
        self.text = txt
        self.font = font
        self.pos = pos
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (260, 40))

    def draw(self):
        pygame.draw.rect(screen, 'light gray', self.button, 0, 5)
        pygame.draw.rect(screen, 'dark gray', [self.pos[0], self.pos[1], 260, 40], 5, 5)
        text2 = self.font.render(self.text, True, 'black')
        screen.blit(text2, (self.pos[0] + 15, self.pos[1] + 7))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

def update(dt, Map_size):
    global all_players, all_bullets, all_particles, time_list, slider_grabbed, slider_y, grab_offset_y
  
    # Go through events that are passed to the script by the window.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()

    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
 
def draw(Map_size):

    """
    Draw things to the window. Called once per frame.
    """
    screen.fill((230, 230, 230))

    label = buttonfont.render(str(round(fpsClock.get_fps(), 2)), 1, (0, 0, 0))
    screen.blit(label, (50, 240))
    # Redraw screen here.
  
    # Flip the display so that the things we drew actually show up.
    pygame.display.flip()

def GamePlay(Map_size):
    global w, h, play_area, play_area_offset

    dt = 1/fps # dt is the time since last frame.
    while 1:
        battle.battle_loop(battle.player_team, battle.enemy_team)

        update(dt, Map_size)
        draw(Map_size)

        fpsClock.tick(fps)

def GameStart():
    # Initialise PyGame.
  
    # Main game loop.
    MainMenu()

def MainMenu():
    GamePlay([w, h])

if __name__ == "__main__":
    GameStart()