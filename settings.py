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
MENU_BTNS_COLOR = BROWN
MENU_BTNS_TXT_COLOR = WHITE
INFO_BOX_COLOR = (0,0,0,30)

TOWER_TYPES = {
  'green_tank': {
    'damage': 1,
    'price': 50,
    'range': 170,
    'rate': 2000,
  },
  'green_tank_upgraded': {
    'damage': 2,
    'price': 35,
    'range': 230,
    'rate': 1500,
  },
  'blue_tank': {
    'damage': 2,
    'price': 80,
    'range': 120,
    'rate': 1200,
  },
  'blue_tank_upgraded': {
    'damage': 3,
    'price': 60,
    'range': 150,
    'rate': 1000,
  },
  'sand_tank': {
    'damage': 3,
    'price': 150,
    'range': 200,
    'rate': 1000,
  },
  'sand_tank_upgraded': {
    'damage': 5,
    'price': 110,
    'range': 270,
    'rate': 700,
  },
  'red_tank': {
    'damage': 6,
    'price': 200,
    'range': 180,
    'rate': 2000,
  },
  'red_tank_upgraded': {
    'damage': 8,
    'price': 140,
    'range': 230,
    'rate': 1500,
  },
  'black_tank': {
    'damage': 4,
    'price': 350,
    'range': 200,
    'rate': 500,
  },
  'black_tank_upgraded': {
    'damage': 6,
    'price': 220,
    'range': 300,
    'rate': 350,
  },
}

ENEMY_TYPES = [
  'green_bike', 'blue_bike', 'yellow_bike', 'red_bike', 'black_bike', 
  'green_car', 'blue_car', 'yellow_car', 'red_car', 'black_car']

ENEMY_PROPS = {
  'green_bike': {
    'health': 1,
    'value': 2,
    'speed': 3,
  },
  'blue_bike': {
    'health': 2,
    'value': 3,
    'speed': 4,
  },
  'yellow_bike': {
    'health': 4,
    'value': 4,
    'speed': 5,
  },
  'red_bike': {
    'health': 5,
    'value': 5,
    'speed': 6,
  },
  'black_bike': {
    'health': 6,
    'value': 5,
    'speed': 7,
  },
  'green_car': {
    'health': 10,
    'value': 6,
    'speed': 3,
  },
  'blue_car': {
    'health': 11,
    'value': 6,
    'speed': 4,
  },
  'yellow_car': {
    'health': 13,
    'value': 7,
    'speed': 5,
  },
  'red_car': {
    'health': 15,
    'value': 7,
    'speed': 6,
  },
  'black_car': {
    'health': 20,
    'value': 8,
    'speed': 7,
  },
}

LEVELS = {
  '1': {
    'weights': [100,0,0,0,0,0,0,0,0,0],
    'rate': 800,
    'n': 15
  },
  '2': {
    'weights': [50,50,0,0,0,0,0,0,0,0],
    'rate': 800,
    'n': 20
  },
  '3': {
    'weights': [40,30,30,0,0,0,0,0,0,0],
    'rate': 800,
    'n': 25
  },
  '4': {
    'weights': [30,20,20,30,0,0,0,0,0,0],
    'rate': 500,
    'n': 30
  },
  '5': {
    'weights': [20,20,20,20,20,0,0,0,0,0],
    'rate': 500,
    'n': 35
  },
  '6': {
    'weights': [10,10,20,20,20,20,0,0,0,0],
    'rate': 500,
    'n': 40
  },
  '7': {
    'weights': [10,10,10,10,20,20,20,0,0,0],
    'rate': 500,
    'n': 40
  },
  '8': {
    'weights': [10,10,10,10,10,10,40,0,0,0],
    'rate': 500,
    'n': 40
  },
  '9': {
    'weights': [0,0,10,10,10,10,30,30,0,0],
    'rate': 500,
    'n': 40
  },
  '10': {
    'weights': [0,0,10,10,10,10,10,50,0,0],
    'rate': 500,
    'n': 40
  },
  '11': {
    'weights': [0,0,0,10,10,10,10,40,20,0],
    'rate': 500,
    'n': 40
  },
  '12': {
    'weights': [0,0,0,10,10,10,10,20,40,0],
    'rate': 500,
    'n': 40
  },
  '13': {
    'weights': [0,0,0,0,10,10,10,10,40,20],
    'rate': 500,
    'n': 40
  },
  '14': {
    'weights': [0,0,0,0,10,10,10,10,20,40],
    'rate': 500,
    'n': 40
  },
  '15': {
    'weights': [0,0,0,0,0,10,10,10,20,50],
    'rate': 500,
    'n': 40
  },
  '16': {
    'weights': [0,0,0,0,30,0,0,0,10,60],
    'rate': 500,
    'n': 40
  },
}