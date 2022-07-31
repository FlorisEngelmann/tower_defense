import math
import random
import pygame as pg
from pygame.sprite import Group
from pygame.sprite import Sprite
from settings import *
vec = pg.math.Vector2


def animate(obj, angle, scale, loop=True):
  n_images = len(obj.images.keys())
  obj.image = obj.images[f'frame_{(obj.frame % n_images)}']
  obj.frame += 1
  if obj.frame > n_images and not loop:
    obj.kill()

  obj.image = pg.transform.scale(obj.image, scale)
  obj.image = pg.transform.rotate(obj.image, -angle)


class Tower(Sprite):
  def __init__(self, game, _type, pos):
    Sprite.__init__(self, game.all_sprites, game.towers)
    self.game = game
    self.type = _type
    self.set_up_attributes()
    self.last_shot = 0
    self.value = self.price
    self.placed = False
    self.image = self.game.asset_manager.images['towers'][self.type]
    self.rect = self.image.get_rect()
    self.rect.center = (pos)
    self.barrel = Barrel(self.game, self.type, pos)

  def is_valid_loc(self):
    ''' checks if tower is in a valid location '''
    valid_loc_found = False
    for tower_area in self.game.tower_areas:
      tower_x = self.rect.centerx
      tower_y = self.rect.centery
      tower_area_left = tower_area.x
      tower_area_right = tower_area.x + tower_area.w
      tower_area_top = tower_area.y
      tower_area_bottom = tower_area.y + tower_area.h
      if tower_x < tower_area_right and tower_x > tower_area_left \
        and tower_y < tower_area_bottom and tower_y > tower_area_top:
          tower_present = False
          for t in self.game.towers:
            if self is not t:
              if self.rect.collidepoint((t.rect.centerx, t.rect.centery)):
                tower_present = True
                break
          if not tower_present:
            valid_loc_found = True
            break

    return valid_loc_found

  def set_up_attributes(self):
    self.damage = TOWER_TYPES[self.type]['damage']
    self.price = TOWER_TYPES[self.type]['price']
    self.range = TOWER_TYPES[self.type]['range']
    self.size = TOWER_TYPES[self.type]['size']
    self.rate = TOWER_TYPES[self.type]['rate']

  def update(self):
    if not self.placed: # refactor
      self.rect.center = self.game.mouse_pos
      self.barrel.rect.center = self.rect.center
      return
    
    if self.game.level_manager.level_active:
      ticks = pg.time.get_ticks()
      if ticks - self.last_shot > self.rate:
        enemies_in_range = self.enemies_in_range()
        if enemies_in_range:
          first_enemy = max(enemies_in_range, key=lambda x: x.distance_walked)

          distance_x = (first_enemy.rect.centerx - self.rect.centerx)
          distance_y = (first_enemy.rect.centery - self.rect.centery)
          angle = math.atan2(distance_y, distance_x) * (180/math.pi)
          self.barrel.rotate(angle)

          self.shoot(first_enemy)
          self.last_shot = ticks

  def upgrade(self):
    self.type = self.type + '_upgraded'
    self.set_up_attributes()
    self.value += self.price
    self.image = self.game.asset_manager.images['towers'][self.type]

  def enemies_in_range(self):
    enemies = []
    for enemy in self.game.level_manager.level_object.enemies:
      distance_x = abs(self.rect.centerx - enemy.rect.centerx)
      distance_y = abs(self.rect.centery - enemy.rect.centery)
      distance = math.sqrt(distance_x**2 + distance_y**2)
      
      if distance <= self.range:
        enemies.append(enemy)
      
    return enemies

  def shoot(self, enemy):
    HitAnimation(self.game, self, enemy)
    enemy.health -= self.damage
      

class Barrel(Sprite):
  def __init__(self, game, _type, pos):
    Sprite.__init__(self, game.all_sprites, game.barrels)
    self.game = game
    self.original_image = self.game.asset_manager.images['towers'][f'{_type}_barrel']
    self.image = self.original_image
    self.rect = self.image.get_rect()
    self.rect.center = pos

  def rotate(self, angle):
    self.image = pg.transform.rotate(self.original_image, -angle - 90)
    self.rect = self.image.get_rect(center=self.rect.center)

  def update(self):
    pass


class ShopItem(Sprite):
  def __init__(self, game, type, x, y):
    Sprite.__init__(self, game.all_sprites, game.shop_items)
    self.game = game
    self.type = type
    self.price = TOWER_TYPES[self.type]['price']
    self.size = TOWER_TYPES[self.type]['size']
    self.image = self.game.asset_manager.images['towers'][self.type]
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)


class Enemy(Sprite):
  def __init__(self, game, level, _type):
    Sprite.__init__(self, game.all_sprites, level.enemies)
    self.game = game
    self.type = _type
    self.original_image = self.game.asset_manager.images['enemies'][self.type]
    self.image = self.original_image
    self.waypoint_n = 0
    x = self.game.waypoints[self.waypoint_n]['x']
    y = self.game.waypoints[self.waypoint_n]['y']
    self.rect = self.image.get_rect()
    self.rect.center = vec(x, y)
    self.waypoint_pos = vec(x, y)
    self.speed = ENEMY_PROPS[self.type]['speed']
    self.health = ENEMY_PROPS[self.type]['health']
    self.distance_walked = 0

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
    self.direction = (self.waypoint_pos - self.rect.center).normalize()
    self.rect.center += self.direction * self.speed
 
  def rotate(self):
    angle = math.atan2(self.direction[1], self.direction[0]) * (180/math.pi)
    self.image = pg.transform.rotate(self.original_image, -angle - 90)

  def update_distance(self):
    self.distance_walked += self.speed 

  def update(self):
    if self.health <= 0:
      self.game.money += ENEMY_PROPS[self.type]['health']
      self.kill()
    self.move()
    self.rotate()
    self.update_distance()


class TowerArea:
  def __init__(self, x, y, w, h):
    self.x = x
    self.y = y
    self.w = w
    self.h = h


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


class NextLevelButton(Button):
  def __init__(self, game, x, y):
    Button.__init__(self, game)
    self.image = self.game.asset_manager.images['widgets']['next_level_btn']
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)

  def update(self):
    if self.game.level_manager.level_active:
      self.image = self.game.asset_manager.images['widgets']['next_level_btn_inactive']
    else:
      self.image = self.game.asset_manager.images['widgets']['next_level_btn']


class HitAnimation(Sprite):
  def __init__(self, game, tower, enemy):
    self.game = game
    Sprite.__init__(self, self.game.all_sprites)
    self.images = self.game.asset_manager.images['hit_animation']
    self.tower = tower
    self.enemy = enemy
    self.frame = 0

    distance_x = self.enemy.rect.centerx - self.tower.rect.centerx
    distance_y = self.enemy.rect.centery - self.tower.rect.centery
    self.distance = math.sqrt(distance_x**2 + distance_y**2)
    self.angle = math.atan2(distance_y, distance_x) * (180/math.pi)
    self.center_point = (self.tower.rect.centerx + distance_x/2, self.tower.rect.centery + distance_y/2)

    self.image = self.game.asset_manager.images['hit_animation']['frame_1']
    self.scale = (self.distance, 10)
    self.image = pg.transform.scale(self.image, self.scale)
    self.image = pg.transform.rotate(self.image, -self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.center_point

  def update(self):
    animate(self, self.angle, self.scale, loop=False)