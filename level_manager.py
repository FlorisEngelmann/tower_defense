import pygame as pg
from pygame.sprite import Sprite, Group
import random
import math
from settings import *
from sprites import Enemy
vec = pg.math.Vector2


class LevelManager:
  def __init__(self, game):
    self.game = game
    self.level = 0
    self.level_object = None
    self.level_active = False

  def next_level(self):
    self.level += 1
    self.level_active = True
    self.level_object = Level(self.game, self, self.level)

  def update(self):
    if self.level_active:
      self.level_object.update()
    if self.game.lives <= 0:
      self.game.game_over = True
    if self.level >= len(list(LEVELS)) and not self.level_active:
      self.game.game_over = True
      self.game.victory = True
      del self


class Level:
  '''
  Input: levelnumber (int)
  Handles enemy spawning
  Destroys itself when all enemies are destroyed.
  '''
  def __init__(self, game, level_manager, level):
    self.game = game
    self.level_manager = level_manager
    self.enemies = Group()
    self.level = str(level)
    self.last_enemy = 0
    self.enemy_order = self.get_enemies()
    self.enemy_counter = 0

  def get_enemies(self):
    n = LEVELS[self.level]['n']
    weights = LEVELS[self.level]['weights']
    return random.choices(ENEMY_TYPES, weights=weights, k=n)

  def update(self):
    '''Spawns an enemy once in a timeframe'''
    ticks = pg.time.get_ticks()
    if ticks - self.last_enemy > LEVELS[self.level]['rate']: 
      if self.enemy_counter < len(self.enemy_order):
        Enemy(self.game, self, self.enemy_order[self.enemy_counter])
        self.enemy_counter += 1
        self.last_enemy = ticks
      else:
        if not self.enemies:
          self.level_manager.level_active = False
          self.level_manager.level_object = None
          del self


