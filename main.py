import pygame as pg
from pygame.sprite import Group
import sys
import os
import fnmatch
from settings import *
from sprites import *
from tilemap import *
from menu_manager import MenuManager
from level_manager import LevelManager
from asset_manager import AssetManager

pg.init()
pg.display.set_mode((1600, 800))



class Game:
  def __init__(self):
    pg.display.set_caption(TITLE)
    self.clock = pg.time.Clock()
    self.volume = 0.5
    self.asset_manager = AssetManager(self)
    self.menu_manager = MenuManager(self)
    self.screen = pg.display.set_mode(
      (self.asset_manager.map_rect.width, self.asset_manager.map_rect.height)
    )
    self.game_over = False

  def set_up_tile_map(self):
    for object_group in self.asset_manager.map.tmxdata.objectgroups:
      for tile_object in object_group:
        obj_center = {
          'x': tile_object.x + tile_object.width / 2,
          'y': tile_object.y + tile_object.height / 2
        }
        if object_group.name == 'shop_items':
          ShopItem(self, tile_object.name, obj_center['x'], obj_center['y'])
        if tile_object.name == 'sell_btn':
          self.sell_btn = SellButton(
            self, obj_center['x'], obj_center['y'], tile_object.width, tile_object.height
          )
        if tile_object.name == 'upgrade_btn':
          self.upgrade_btn = UpgradeButton(
            self, obj_center['x'], obj_center['y'], tile_object.width, tile_object.height
          )
        if tile_object.name == 'next_level_btn':
          self.next_level_btn = NextLevelButton(self, obj_center['x'], obj_center['y'])
        if tile_object.name == 'info_lbl':
          self.info = Information(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        if object_group.name == 'waypoints':
          self.waypoints.append(
            {
              'n': int(tile_object.name), 
              'x': int(obj_center['x']), 
              'y': int(obj_center['y'])
            }
          )
        if object_group.name == 'tower_areas':
          self.tower_areas.append(
            TowerArea(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
          )
    self.waypoints = sorted(self.waypoints, key=lambda x: x['n'])

  def reset_game(self):
    self.tower_areas = []
    self.waypoints = []
    self.mouse_pos = None
    self.money = 100
    self.buying = None
    self.tower_active = None

    self.lives = 50
    self.level_manager = LevelManager(self)

    self.victory = False
    self.game_over = False

  def new(self):
    self.all_sprites = Group()
    self.towers = Group()
    self.barrels = Group()
    self.shop_items = Group()

    self.reset_game()
    self.set_up_tile_map()
    
  def run(self):
    while not self.game_over:
      self.clock.tick(FPS)
      self.events()
      self.update()
      self.draw()

  def draw_text(self, surface, font, size, text, color, x, y, align):
    var = pg.font.Font(pg.font.match_font(font), size)
    var = var.render(text, True, color)
    var_rect = var.get_rect()
    if align == 'left':
      var_rect.bottomleft = (x, y)
    elif align == 'center':
      var_rect.center = (x, y)
    elif align == 'right':
      var_rect.bottomright = (x, y)
    surface.blit(var, var_rect)

  def draw_tower_info(self):
    dmg = ''
    rng = ''
    rate = ''
    price = ''

    if self.tower_active:
      dmg = self.tower_active.damage
      rng = self.tower_active.range
      rate = round(1000 / int(self.tower_active.rate), 1)
      price = ''
    for item in self.shop_items:
      if item.rect.collidepoint(self.mouse_pos):
        dmg = TOWER_TYPES[item.type]['damage']
        rng = TOWER_TYPES[item.type]['range']
        rate = round(1000 / int(TOWER_TYPES[item.type]['rate']), 1)
        price = TOWER_TYPES[item.type]['price']
        break
    if self.buying:
      dmg = self.buying.damage
      rng = self.buying.range
      rate = round(1000 / int(self.buying.rate), 1)
      price = self.buying.price

    info_surface = pg.Surface((self.info.w, self.info.h), pg.SRCALPHA)
    info_surface.fill(INFO_BOX_COLOR)

    size = 32
    color = BLACK
    align = 'left'
    top = 50
    left = 30

    self.draw_text(
      info_surface, 'arial', size, f'Damage: {str(dmg)}', color,
      left, top, align
    )
    self.draw_text(
      info_surface, 'arial', size, f'Range: {str(rng)}', color,
      left, top + 40, align
    )

    self.draw_text(
      info_surface, 'arial', size, f'Fire rate: {rate}/s', color,
      left, top + 80, align
    )
    self.draw_text(
      info_surface, 'arial', size, f'${str(price)}', color,
      left, top + 120, align
    )

    self.screen.blit(info_surface, (self.info.x, self.info.y))

  def draw(self):
    self.screen.blit(self.asset_manager.map_img, (0,0))
    if self.buying or self.tower_active:
      color = (255,255,255,50)
      if self.tower_active:
        r = self.tower_active.range
        x = self.tower_active.rect.centerx
        y = self.tower_active.rect.centery
      if self.buying:
        r = self.buying.range
        x = self.buying.rect.centerx
        y = self.buying.rect.centery
        if not self.buying.is_valid_loc(): 
          color = (255,0,0,50)

      circle_surface = pg.Surface((r*2, r*2), pg.SRCALPHA)
      pg.draw.circle(circle_surface, color, (r, r), r)
      self.screen.blit(circle_surface, (x - r, y - r))

    self.all_sprites.draw(self.screen)
    self.barrels.draw(self.screen)

    self.draw_text( 
      self.screen, 'arial', 22, self.upgrade_btn.text, WHITE, 
      self.upgrade_btn.rect.centerx, self.upgrade_btn.rect.centery, 'center'
    )
    self.draw_text( 
      self.screen, 'arial', 22, self.sell_btn.text, WHITE, 
      self.sell_btn.rect.centerx, self.sell_btn.rect.centery, 'center'
    )
    self.draw_text( 
      self.screen, 'arial', 26, 'Level ' + str(self.level_manager.level), (0,11,115), 
      self.asset_manager.map_rect.width - 200, 50, 'center'
    )
    self.draw_text( 
      self.screen, 'arial', 26, 'Money: $' + str(self.money), (0,11,115), 
      self.asset_manager.map_rect.width - 280, 90, 'center'
    )
    self.draw_text( 
      self.screen, 'arial', 26, 'Lives: ' + str(self.lives), (0,11,115), 
      self.asset_manager.map_rect.width - 120, 90, 'center'
    )
    self.draw_tower_info()
    pg.display.flip()

  def update(self):
    self.mouse_pos = pg.mouse.get_pos()
    self.all_sprites.update()
    self.level_manager.update()

  def events(self):
    for event in pg.event.get():
      if event.type == pg.QUIT:
        self.quit()

      if event.type == pg.MOUSEBUTTONUP:
        
        if self.buying:
          if self.buying.is_valid_loc():
            self.buying.placed = True
            self.tower_active = self.buying
            self.money -= self.buying.price
          else:
            self.buying.kill()
          self.buying = None
          break
        
        for tower in self.towers:
          if tower.rect.collidepoint(self.mouse_pos):
            self.tower_active = tower
            break
        
        if self.tower_active:
          if self.sell_btn.rect.collidepoint(self.mouse_pos):
            self.money += int(self.tower_active.value * 0.8)
            self.tower_active.barrel.kill()
            self.tower_active.kill()
            self.tower_active = None
            break
          if self.upgrade_btn.rect.collidepoint(self.mouse_pos):
            if not 'upgraded' in self.tower_active.type:
              if self.money >= TOWER_TYPES[self.tower_active.type + '_upgraded']['price']:
                self.tower_active.upgrade()
                self.money -= self.tower_active.price
                break
          if not self.tower_active.rect.collidepoint(self.mouse_pos):
            if not self.next_level_btn.rect.collidepoint(self.mouse_pos):
              self.tower_active = None
        
        for item in self.shop_items:
          if item.rect.collidepoint(self.mouse_pos):
            if self.money >= item.price:
              self.buying = Tower(self, item.type, self.mouse_pos)
              break
        
        if self.next_level_btn.rect.collidepoint(self.mouse_pos):
          if not self.level_manager.level_active:
            self.level_manager.next_level()

      if event.type == pg.KEYDOWN:
        if event.key == pg.K_SPACE:
          self.menu_manager.show_menu('pause_menu')

  def quit(self):
    pg.quit()
    sys.exit()


g = Game()
g.menu_manager.show_menu('main_menu')
while not g.game_over:
  g.new()
  g.run()
  g.menu_manager.show_menu('game_over_menu')