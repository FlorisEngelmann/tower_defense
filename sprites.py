import math
import random
import pygame as pg
from pygame.sprite import Group
from pygame.sprite import Sprite
from settings import *
vec = pg.math.Vector2


class Tower(Sprite):
  def __init__(self, game, type, pos):
    Sprite.__init__(self, game.all_sprites, game.towers)
    self.game = game
    self.type = type
    self.set_up_attributes()
    self.last_shot = 0
    self.value = self.price
    self.placed = False
    self.image = self.game.images['towers'][self.type]
    self.rect = self.image.get_rect()
    self.rect.center = (pos)

  def set_up_attributes(self):
    self.damage = TOWER_TYPES[self.type]['damage']
    self.price = TOWER_TYPES[self.type]['price']
    self.range = TOWER_TYPES[self.type]['range']
    self.size = TOWER_TYPES[self.type]['size']
    self.rate = TOWER_TYPES[self.type]['rate']

  def update(self):
    if not self.placed:
      x,y = pg.mouse.get_pos()
      self.rect.centerx = x
      self.rect.centery = y
      return
    if self.game.round_active:
      self.detect_enemy()

  def upgrade(self):
    self.type = self.type + '_upgraded'
    self.set_up_attributes()
    self.value += self.price
    self.image = self.game.images['towers'][self.type]

  def detect_enemy(self):
    for enemy in self.game.round_object.enemies:
      distance_x = abs(self.rect.centerx - enemy.rect.centerx)
      distance_y = abs(self.rect.centery - enemy.rect.centery)
      distance = math.sqrt(distance_x**2 + distance_y**2)
      if distance <= self.range:
        self.shoot(enemy)

  def shoot(self, enemy):
    ticks = pg.time.get_ticks()
    if ticks - self.last_shot > self.rate:
      distance_x = enemy.rect.centerx - self.rect.centerx
      distance_y = enemy.rect.centery - self.rect.centery
      direction = vec(distance_x, distance_y).normalize() * 30
      Bullet(self.game, self.rect.centerx, self.rect.centery, direction, self.damage)
      self.last_shot = ticks


class ShopItem(Sprite):
  def __init__(self, game, type, x, y):
    Sprite.__init__(self, game.all_sprites, game.shop_items)
    self.game = game
    self.type = type
    self.price = TOWER_TYPES[self.type]['price']
    self.size = TOWER_TYPES[self.type]['size']
    self.image = self.game.images['towers'][self.type]
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)


class Enemy(Sprite):
  def __init__(self, game, round, type):
    Sprite.__init__(self, game.all_sprites, game.round_object.enemies)
    self.game = game
    self.round = round
    self.type = type
    self.image = self.game.images['enemies'][type]
    self.waypoint_n = 0
    x = self.game.waypoints[self.waypoint_n]['x']
    y = self.game.waypoints[self.waypoint_n]['y']
    self.rect = self.image.get_rect()
    self.rect.center = vec(x, y)
    self.waypoint_pos = vec(x, y)
    self.speed = ENEMY_PROPS[type]['speed']
    self.health = ENEMY_PROPS[type]['health']

  def move(self):
    if self.rect.collidepoint(self.waypoint_pos):
      self.waypoint_n += 1
    if self.waypoint_n >= len(self.game.waypoints):
      self.game.lives -= 1
      self.kill()
      return
    self.waypoint_pos = vec(
      self.game.waypoints[self.waypoint_n]['x'], 
      self.game.waypoints[self.waypoint_n]['y']
    )
    self.rect.center += (self.waypoint_pos - self.rect.center).normalize() * self.speed

  def check_for_hit(self):
    for bullet in self.game.round_object.bullets:
      if pg.sprite.collide_rect(self, bullet):
        if self.health > bullet.damage: # enemy survives
          self.game.money += bullet.damage
          self.health -= bullet.damage
          bullet.kill()
        else: # enemy dies
          self.game.money += self.health
          bullet.damage -= self.health
          if bullet.damage <= 0: bullet.kill()
          self.kill()

  def update(self):
    self.check_for_hit()
    self.move()


class TowerArea:
  def __init__(self, x, y, w, h):
    self.x = x
    self.y = y
    self.w = w
    self.h = h


class Bullet(Sprite):
  def __init__(self, game, x, y, direction, damage):
    Sprite.__init__(self, game.all_sprites, game.round_object.bullets)
    self.game = game
    self.direction = direction
    self.image = pg.Surface((10, 10))
    self.image.fill(BLACK)
    self.rect = self.image.get_rect()
    self.rect.center = vec(x, y)
    self.damage = damage

  def move(self):
    self.rect.centerx += self.direction[0]
    self.rect.centery += self.direction[1]

  def update(self):
    self.move()
    if self.rect.centerx < 0 or self.rect.centerx > self.game.map_rect.width:
      if self.rect.centery < 0 or self.rect.centery > self.game.map_rect.height:
        self.kill()


class Round:
  '''
  Input: roundnumber (int)
  Handles enemy spawning
  Destroys itself when all enemies are destroyed.
  '''
  def __init__(self, game, round):
    self.game = game
    self.enemies = Group()
    self.bullets = Group()
    self.round = str(round)
    self.last_enemy = 0
    self.enemy_order = self.get_enemies()
    self.enemy_counter = 0
    

  def get_enemies(self):
    n = ROUNDS[self.round]['n']
    weights = ROUNDS[self.round]['weights']
    return random.choices(ENEMY_TYPES, weights=weights, k=n)

  def update(self):
    '''Spawns an enemy once in a timeframe'''
    ticks = pg.time.get_ticks()
    if ticks - self.last_enemy > ROUNDS[self.round]['rate']: 
      if self.enemy_counter < len(self.enemy_order):
        Enemy(self.game, self, self.enemy_order[self.enemy_counter])
        self.enemy_counter += 1
        self.last_enemy = ticks
      else:
        if not self.enemies:
          self.game.round_active = False
          self.game.round_object = None
          del self


class Information:
  def __init__(self, x, y, w, h):
    self.x = x
    self.y = y
    self.w = w
    self.h = h


class Button(Sprite):
    def __init__(self, game):
      Sprite.__init__(self, game.all_sprites)
      self.game = game


class SellButton(Button):
  def __init__(self, game, x, y, w, h):
    Button.__init__(self, game)
    self.image = pg.Surface((w, h))
    self.image.fill(INACTIVE_BTN_COLOR)
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.text = 'Sell'

  def update(self):
    self.text = 'Sell'
    if self.game.tower_active:
      self.text = 'Sell: $' + str(int(self.game.tower_active.value * 0.8))
      self.image.fill(SELL_BTN_COLOR)
    else:
      self.image.fill(INACTIVE_BTN_COLOR)


class UpgradeButton(Button):
  def __init__(self, game, x, y, w, h):
    Button.__init__(self, game)
    self.image = pg.Surface((w, h))
    self.image.fill(INACTIVE_BTN_COLOR)
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.text = 'Upgrade'
    
  def update(self):
    self.text = 'Upgrade'
    if self.game.tower_active:
      if not 'upgraded' in self.game.tower_active.type:
        self.text = 'Upgrade: $' + str(TOWER_TYPES[f'{self.game.tower_active.type}_upgraded']['price'])
        self.image.fill(UPGRADE_BTN_COLOR)
      else:
        self.text = 'Upgraded'
        self.image.fill(INACTIVE_BTN_COLOR)
    else:
      self.image.fill(INACTIVE_BTN_COLOR)


class NextRoundButton(Button):
  def __init__(self, game, x, y):
    Button.__init__(self, game)
    self.image = self.game.images['widgets']['next_round_btn']
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)

  def update(self):
    if self.game.round_active:
      self.image = self.game.images['widgets']['next_round_btn_inactive']
    else:
      self.image = self.game.images['widgets']['next_round_btn']