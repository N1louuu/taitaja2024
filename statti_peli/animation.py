import sys
import pygame
import math
import random
import threading
import screeninfo

import statti_peli_main as main
import battle
import moves

all_animations = []

def play_animation(anim):
  global all_animations

  if anim == "":
    pass
  
  elif anim['name'] == "play_attack_animations":
    for (ind, move) in enumerate(battle.chosen_moves):
      all_animations.append({'timer': 40*ind, 'name':'play_attack', 'ind':move['user'], 'target':move['target'], 'id':move['id'], 'move':move})
    all_animations.append({'timer': 40*len(battle.chosen_moves), 'name': "end_of_attack_animation"})

  elif anim['name'] == "play_attack":
    all_animations.append({'timer': 5, 'name':'attack', 'ind':anim['ind'], 'killid':anim['id']})
    battle.p_anim_list[anim['ind']]['timer'] = 80
    battle.p_anim_list[anim['ind']]['target'] = anim['target']
    battle.p_anim_list[anim['ind']]['move'] = anim['move']

  elif anim['name'] == "attack":
    for move in battle.chosen_moves:
      if anim['killid'] == move['id']:
        battle.chosen_moves.remove(move)

  elif anim['name'] == "end_of_attack_animation":
    battle.turn = 0

def animations():
  global all_animations
  
  for animation in all_animations:
    if animation['timer'] == 0:
      play_animation(animation)
      all_animations.remove(animation)

    animation['timer']-=1