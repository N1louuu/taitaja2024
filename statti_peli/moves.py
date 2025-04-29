import sys
import pygame
import math
import random
import threading
import screeninfo

import statti_peli_main as main
import battle

all_moves = [
    {
        "name": "swipe",
        "damage": 2,
        "speed":6
    },
    {
        "name": "punch",
        "damage": 3,
        "speed":4
    },
    {
        "name": "slash",
        "damage": 6,
        "speed":4
    },
    {
        "name": "great slash",
        "damage": 12,
        "speed":2
    },
    {
        "name": "creep",
        "damage": 7,
        "speed":7
    }
]