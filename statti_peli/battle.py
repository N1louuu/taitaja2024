import sys
import pygame
import math
import random
import threading
import screeninfo

import statti_peli_main as main

player_team = [
    0,
    {
        "name": "skeleton",
        "health" : 18,
        "strength" : 5,
        "defence": 2,
        "speed": 7,
        "passives": [],
        "weapons": [],
        "moves": ["swipe"]
    },
        {
        "name": "knight",
        "health" : 24,
        "strength" : 6,
        "defence": 5,
        "speed": 5,
        "passives": [],
        "weapons": [],
        "moves": ["swipe"]
    },
        {
        "name": "knight",
        "health" : 24,
        "strength" : 6,
        "defence": 5,
        "speed": 5,
        "passives": [],
        "weapons": [],
        "moves": ["swipe"]
    }
]

enemy_team = [
    1,
    {
        "name": "skeleton",
        "health" : 10,
        "strength" : 5,
        "defence": 2,
        "speed": 7,
        "passives": [],
        "weapons": [],
        "moves": ["swipe"]
    },
        {
        "name": "gremlin",
        "health" : 4,
        "strength" : 6,
        "defence": 5,
        "speed": 10,
        "passives": [],
        "weapons": [],
        "moves": ["tik tok swipe"]
    },
        {
        "name": "bludeerius",
        "health" : 12,
        "strength" : 2,
        "defence": 0,
        "speed": 6,
        "passives": [],
        "weapons": [],
        "moves": ["swipe"]
    }
]

statfont = pygame.font.SysFont("Droid sans monoregular", 30)

class player:
    def __init__(self, ind, unit, side):
        self.side = side
        self.unit = unit
        self.ind = ind
    
    def set_window_size(self, width, height):
        self.width = width
        self.height = height
    
    def validate(self, num):
        return num != 0

    def get_height(self):
        return self.height if validate(self.height) else 0

    def get_width(self):
        return self.width if validate(self.width) else 0

    def draw_player(self, ind):
        global statfont
        x = (self.width-200)/(len(player_team))+ self.width/(len(player_team))*ind
        y = self.height-400
        y = y*((-self.side+1)/2*1.5+0.25)
        shortened = {
            "name": "",
            "health": "hp",
            "strength": "str",
            "defence": "def",
            "speed": "spd",
        }
        
        pygame.draw.rect(main.screen, (120, 120, 120), ((x, y, 100, 100)))
        for (ind, name) in enumerate(shortened.keys()):
            rational_y = 100 if ind == 0 else 110 + ind * 25
            name2 = str(self.unit[name])
            prefix = "" if shortened[name] == "" else shortened[name] + ": "
            font = main.buttonfont if ind == 0 else statfont
            label = font.render(f"{prefix}{name2}", 1, (0, 0, 0))
            main.screen.blit(label, (x, y+rational_y))

def draw_team(team):
    side = team[0]
    team = team[1:]
    #print(team)
    w, h = main.screen.get_size()
    for (ind, unit) in enumerate(team):
        player_instance = player(ind,unit,side)
        player_instance.set_window_size(w,h)
        player_instance.draw_player(ind)

turn = 0 # player turn: 0 and enemy: 1
chosen_moves = []

chosen_char = 0

def battle_update():
    pass

def battle_draw(p_team, e_team):
    main.screen.fill((230, 230, 230))
  
    draw_team(p_team)
    draw_team(e_team)

    if turn == 0:
        move_select(p_team)

    
    pygame.display.flip()

def move_select(p_team):
    global turn, chosen_moves, chosen_char
    for move in p_team[chosen_char]["moves"]:

        x=40
        y=500
        pygame.draw.rect(main.screen, (120, 120, 120), ((x, y, 100, 300)))

def input_handle(p_team, e_team):
    global turn, chosen_moves, chosen_char
    for (ind, unit) in enumerate(p_team):
        w, h = main.screen.get_size()
        x = (w-200)/(len(player_team))+ w/(len(player_team))*ind
        y = h-400
        y = y*((-0+1)/2*1.5+0.25)
        

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
            m_pos = pygame.mouse.get_pos()

            for (ind, unit) in enumerate(p_team):
                w, h = main.screen.get_size()
                x = (w-200)/(len(player_team))+ w/(len(player_team))*ind
                y = h-400
                y = y*((-0+1)/2*1.5+0.25)

                if m_pos[0] >= x and m_pos[0] <= x+100 and m_pos[1] >= y and m_pos[1] <= y+100 and mouse_pressed[0]:
                    chosen_char = ind

def battle_loop(p_team, e_team):
    global turn, chosen_moves, chosen_char

    battle_running = True

    p_team = p_team[1:]
    e_team = e_team[1:]

    while battle_running:

        battle_update()

        input_handle(p_team, e_team)

        battle_draw(p_team, e_team)

        main.fpsClock.tick(main.fps)