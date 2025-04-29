import sys
import pygame
import math
import random
import threading
import screeninfo

import statti_peli_main as main
import animation as anim

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
        "moves": ["swipe", "slash"]
    },
        {
        "name": "knight",
        "health" : 24,
        "strength" : 6,
        "defence": 5,
        "speed": 5,
        "passives": [],
        "weapons": [],
        "moves": ["swipe", "greater slash"]
    }
]

enemy_team = [
    1,
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

p_team=[]
e_team=[]

p_anim_list = []
e_anim_list = []

statfont = pygame.font.SysFont("Droid sans monoregular", 30)

def draw_team(team):
    global statfont, p_anim_list, e_anim_list, p_team, e_team
    side = team[0]
    team = team[1:]

    w, h = main.screen.get_size()

    for (ind, p) in enumerate(p_team):
        x = (w-200)/len(p_team)+ w/len(p_team)*ind
        y = h-400
        y = y*((-0+1)/2*1.5+0.25)
        if p_anim_list[ind]['timer'] == 0:
            p_anim_list[ind]['x'] = x
            p_anim_list[ind]['y'] = y
        else:
            t_x = (w-200)/len(e_team)+ w/len(e_team)*p_anim_list[ind]['target']
            t_y = y*((-1+1)/2*1.5+0.25)
            p_anim_list[ind]['x'] = x+(t_x-x)*(1-abs(p_anim_list[ind]['timer']-40)/40)
            p_anim_list[ind]['y'] = y+(t_y-y)*(1-abs(p_anim_list[ind]['timer']-40)/40)
            p_anim_list[ind]['timer'] -= 1

    for (ind, e) in enumerate(e_team):
        x = (w-200)/len(e_team)+ w/len(e_team)*ind
        y = h-400
        y = y*((-1+1)/2*1.5+0.25)
        if e_anim_list[ind]['timer'] == 0:
            e_anim_list[ind]['x'] = x
            e_anim_list[ind]['y'] = y
        else:
            e_anim_list[ind]['x'] = x
            e_anim_list[ind]['y'] = y
            e_anim_list[ind]['timer'] -= 1

    for (ind, unit) in enumerate(team):
        shortened = {
            "name": "",
            "health": "hp",
            "strength": "str",
            "defence": "def",
            "speed": "spd",
        }
        x = p_anim_list[ind]['x'] if side == 0 else e_anim_list[ind]['x']
        y = p_anim_list[ind]['y'] if side == 0 else e_anim_list[ind]['y']

        rect_color = (120, 120, 120)
        if unit['health'] <= 0:
            rect_color = (150, 20, 20)
        
        pygame.draw.rect(main.screen, rect_color, ((x, y, 100, 100)))
        for (ind, name) in enumerate(shortened.keys()):
            rational_y = 100 if ind == 0 else 110 + ind * 25
            name2 = str(unit[name])
            prefix = "" if shortened[name] == "" else shortened[name] + ": "
            font = main.buttonfont if ind == 0 else statfont
            label = font.render(f"{prefix}{name2}", 1, (0, 0, 0))
            main.screen.blit(label, (x, y+rational_y))

turn = 0 # player turn: 0 and enemy: 1
chosen_moves = []

chosen_char = 0

move_select_active = False
move_select_offset = [0,0]

current_move = {}
enemy_select = False

def battle_update():
    global e_team, p_team

    p_team_cut = p_team[1:]
    e_team_cut = e_team[1:]    

    # move trigger
    for (ind, anim) in enumerate(p_anim_list):
        if anim['timer'] == 40:
            e_team_cut[anim["move"]["target"]]["health"] -= max(anim["move"]["strength"]-e_team_cut[anim["move"]["target"]]["defence"], 0)
            if e_team_cut[anim["move"]["target"]]["health"] <= 0:
                e_team_cut[anim["move"]["target"]]["health"]=0

def move_select():
    global turn, chosen_moves, chosen_char, p_team
    p_team_cut = p_team[1:]
    e_team_cut = e_team[1:]
    mouse_pressed = pygame.mouse.get_pressed()
    m_pos = pygame.mouse.get_pos()

    x=move_select_offset[0]
    y=move_select_offset[1]
    pygame.draw.rect(main.screen, (170, 170, 170), ((x, y, 180, 280)))
    for (ind, move) in enumerate(p_team_cut[chosen_char]["moves"]):
        
        r_y = 25
        if (m_pos[0] >= x and m_pos[0] <= x+180 and m_pos[1] >= y+r_y*ind and m_pos[1] <= y+r_y*(ind+1)):
            pygame.draw.rect(main.screen, (190, 190, 190), ((x, y+r_y*ind, 180, r_y)))
        label = statfont.render(f"{move}", 1, (0, 0, 0))
        main.screen.blit(label, (x, y+r_y*ind))

def draw_enemy_select():
    global turn, chosen_moves, chosen_char, move_select_offset, move_select_active, enemy_select
    m_pos = pygame.mouse.get_pos()

    w, h = main.screen.get_size()
    x = (w-200)/(len(player_team))+ w/(len(player_team))*current_move['user'] +50
    y = h-400 +50

    pygame.draw.line(main.screen, (255, 60, 60), m_pos, [x, y], width=5)

def draw_attack_lines():
    
    w, h = main.screen.get_size()

    for move in chosen_moves:
        y = h-400
        px = (w-200)/(len(p_team))+ w/(len(p_team))*move['user'] +50
        py = y*((-0+1)/2*1.5+0.25) +50
        ex = (w-200)/(len(e_team))+ w/(len(e_team))*move['target'] +50
        ey = y*((-1+1)/2*1.5+0.25) +50
        pygame.draw.line(main.screen, (255, 60, 60), [px, py], [ex, ey], width=5)

def draw_UI():
    w, h = main.screen.get_size()
    x = w-200
    y = h-90

    font_color = (190, 190, 190)
    if len(p_team)-1 == len(chosen_moves):
        font_color = (90, 255, 90)

    m_pos = pygame.mouse.get_pos()
    if (m_pos[0] >= x and m_pos[0] <= x+180 and m_pos[1] >= y and m_pos[1] <= y+70) or turn == 1:
        font_color = (90, 205, 90)

    pygame.draw.rect(main.screen, font_color, ((x, y, 180, 70)))
    label = main.buttonfont.render(f"end turn", 1, (0, 0, 0))
    main.screen.blit(label, (x+25, y+15))
    
def battle_draw():
    p_team_cut = p_team[1:]
    e_team_cut = e_team[1:]

    main.screen.fill((230, 230, 230))
  
    draw_team(p_team)
    draw_team(e_team)

    draw_UI()

    draw_attack_lines()

    if turn == 0 and move_select_active:
        move_select()

    if enemy_select:
        draw_enemy_select()

    pygame.display.flip()

def input_handle():
    global turn, chosen_moves, chosen_char, move_select_offset, move_select_active, enemy_select, current_move

    p_team_cut = p_team[1:]
    e_team_cut = e_team[1:]      

    w, h = main.screen.get_size()  

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

            if turn == 0:

              if enemy_select:

                # select enemy
                for (ind, unit) in enumerate(e_team_cut):
                    x = (w-200)/(len(e_team))+ w/(len(e_team))*ind
                    y = h-400
                    y = y*((-1+1)/2*1.5+0.25)

                    if m_pos[0] >= x and m_pos[0] <= x+100 and m_pos[1] >= y and m_pos[1] <= y+100 and mouse_pressed[0]:
                        enemy_select = False
                        current_move['target'] = ind
                        current_move['id'] = len(chosen_moves)
                        chosen_moves.append(current_move)
                        current_move = {}

                if mouse_pressed[2]:
                    enemy_select = False
                    current_move = {}
                  
              else:

                #use menu
                if move_select_active:
                    x=move_select_offset[0]
                    y=move_select_offset[1]
                    pygame.draw.rect(main.screen, (170, 170, 170), ((x, y, 180, 280)))
                    for (ind, move) in enumerate(p_team_cut[chosen_char]["moves"]):
                        
                        r_y = 25
                        if (m_pos[0] >= x and m_pos[0] <= x+180 and m_pos[1] >= y+r_y*ind and m_pos[1] <= y+r_y*(ind+1)) and mouse_pressed[0]:
                            move_select_active = False
                            move_select_offset = [0, 0]
                            enemy_select = True
                            current_move["move"] = move
                            current_move["user"] = chosen_char
                            current_move["strength"] = p_team_cut[chosen_char]["strength"]
                            current_move["speed"] = p_team_cut[chosen_char]["speed"]

                if not enemy_select:
                  # open up menu
                  for (ind, unit) in enumerate(p_team_cut):
                      
                      c = False
                      for move in chosen_moves:
                          if ind == move['user']:
                              c = True
                              break
                      if c:
                          continue
                      
                      x = (w-200)/(len(p_team))+ w/(len(p_team))*ind
                      y = h-400
                      y = y*((-0+1)/2*1.5+0.25)

                      if m_pos[0] >= x and m_pos[0] <= x+100 and m_pos[1] >= y and m_pos[1] <= y+100 and mouse_pressed[0]:
                          if not (m_pos[0] >= move_select_offset[0] and m_pos[0] <= move_select_offset[0]+180 and m_pos[1] >= move_select_offset[1] and m_pos[1] <= move_select_offset[1]+280):
                              chosen_char = ind
                              move_select_offset = m_pos
                              move_select_active = True
                              break
                      else:
                          if not (m_pos[0] >= move_select_offset[0] and m_pos[0] <= move_select_offset[0]+180 and m_pos[1] >= move_select_offset[1] and m_pos[1] <= move_select_offset[1]+280) and (mouse_pressed[0] or mouse_pressed[2]):
                              move_select_active = False
                              move_select_offset = [0, 0]

                # end turn button
                x = w-200
                y = h-90
                if m_pos[0] >= x and m_pos[0] <= x+180 and m_pos[1] >= y and m_pos[1] <= y+70 and mouse_pressed[0]:
                  turn=1
                  anim.all_animations.append({'timer': 40, 'name':'play_attack_animations'})

def battle_loop(given_p_team, given_e_team):
    global turn, chosen_moves, chosen_char, p_team, e_team, p_anim_list, e_anim_list

    battle_running = True

    w, h = main.screen.get_size()  

    p_team = given_p_team
    e_team = given_e_team

    for (ind, p) in enumerate(p_team):
        x = (w-200)/len(p_team)+ w/len(p_team)*ind
        y = h-400
        y = y*((-0+1)/2*1.5+0.25)
        p_anim_list.append({'ind': ind, 'x':x, 'y':y, 'timer':0, 'target':0})

    for (ind, e) in enumerate(e_team):
        x = (w-200)/len(e_team)+ w/len(e_team)*ind
        y = h-400
        y = y*((-1+1)/2*1.5+0.25)
        e_anim_list.append({'ind': ind, 'x':x, 'y':y, 'timer':0, 'target':0})
  
    while battle_running:

        battle_update()

        input_handle()

        anim.animations()

        battle_draw()

        main.fpsClock.tick(main.fps)