import pygame as pg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LEAF_GREEN = (33, 162, 31)
BLUE = (0, 0, 255)
DARK_BLUE = (100, 100, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 255, 100)
BROWN = (162, 93, 65)

WIDTH = 1280
HEIGHT = 720
FPS = 30
TITLE = "Tower Defense"
SELL_BTN_COLOR = (148,0,0)
INACTIVE_BTN_COLOR = DARKGREY
UPGRADE_BTN_COLOR = (9,111,0)
INTEREST_RATE = 1.1

TOWER_TYPES = {
  'tower_1': {
    'damage': 1,
    'price': 30,
    'range': 200,
    'size': 40,
    'rate': 1000,
  },
  'tower_1_upgraded': {
    'damage': 2,
    'price': 20,
    'range': 300,
    'size': 40,
    'rate': 666,
  },
  'tower_2': {
    'damage': 2,
    'price': 50,
    'range': 100,
    'size': 40,
    'rate': 500,
  },
  'tower_2_upgraded': {
    'damage': 3,
    'price': 20,
    'range': 200,
    'size': 40,
    'rate': 333,
  },
  'tower_3': {
    'damage': 3,
    'price': 70,
    'range': 300,
    'size': 40,
    'rate': 1000,
  },
  'tower_3_upgraded': {
    'damage': 5,
    'price': 50,
    'range': 400,
    'size': 40,
    'rate': 500,
  },
}

ENEMY_TYPES = ['enemy_1', 'enemy_2', 'enemy_3']

ENEMY_PROPS = {
  'enemy_1': {
    'health': 1,
    'speed': 3,
  },
  'enemy_2': {
    'health': 2,
    'speed': 4,
  },
  'enemy_3': {
    'health': 3,
    'speed': 6,
  },
}

ROUNDS = {
  '1': {
    'weights': [100,0,0],
    'rate': 800,
    'n': 1
  },
  # '2': {
  #   'weights': [70,30,0],
  #   'rate': 800,
  #   'n': 1
  # },
  # '3': {
  #   'weights': [50,30,20],
  #   'rate': 800,
  #   'n': 1
  # },
}