import pygame as pg
from pygame.sprite import Group
import sys
import os
import fnmatch
from settings import *
from sprites import *
from tilemap import *

pg.init()
pg.display.set_mode((1500, 750))


class Game:
  def __init__(self):
    pg.display.set_caption(TITLE)
    self.load_data()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((self.map_rect.width, self.map_rect.height))

  def load_data(self):
    game_folder = os.path.dirname(__file__)
    map_folder = os.path.join(game_folder, "map")
    self.map = TiledMap(os.path.join(map_folder , 'map.tmx'))
    self.map_img = self.map.make_map()
    self.map_rect = self.map_img.get_rect()

    img_folder = os.path.join(game_folder, "images")

    image_folders = []
    for file in os.listdir(img_folder):
      f = os.path.join(img_folder, file)
      if os.path.isdir(f):
        image_folders.append(f)

    self.images = {}

    for folder in image_folders:
      basename = os.path.basename(folder)
      self.images[basename] = {}

      images = fnmatch.filter(os.listdir(folder), '*.png')
      for img in images:
        self.images[basename][img[0:-4]] = pg.image.load(os.path.join(
          folder, img
        )).convert_alpha()

  def set_up_tile_map(self):
    for object_group in self.map.tmxdata.objectgroups:
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
        if tile_object.name == 'next_round_btn':
          self.next_round_btn = NextRoundButton(self, obj_center['x'], obj_center['y'])
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

  def set_up_attributes(self):
    self.tower_areas = []
    self.waypoints = []
    self.mouse_pos = None
    self.money = 55
    self.buying = None
    self.tower_active = None

    self.lives = 10
    self.round = 0
    self.round_object = None
    self.round_active = False
    self.playing = True
    self.victory = False

  def new(self):
    self.all_sprites = Group()
    self.towers = Group()
    self.shop_items = Group()

    self.set_up_attributes()
    self.set_up_tile_map()
    
  def run(self):
    self.playing = True
    while self.playing:
      self.clock.tick(FPS)
      self.events()
      self.update()
      self.draw()

  def draw_text(self, font, size, text, color, x, y, align):
    var = pg.font.Font(pg.font.match_font(font), size)
    var = var.render(text, True, color)
    var_rect = var.get_rect()
    if align == 'left':
      var_rect.bottomleft = (x, y)
    elif align == 'center':
      var_rect.center = (x, y)
    elif align == 'right':
      var_rect.bottomright = (x, y)
    self.screen.blit(var, var_rect)

  def draw_tower_info(self):
    pg.draw.rect(self.screen, RED, (self.info.x, self.info.y, self.info.w, self.info.h))

    dmg = ''
    rng = ''
    rate = ''
    price = ''

    # self.image = self.game.images['info']['general']
    if self.tower_active:
      dmg = self.tower_active.damage
      rng = self.tower_active.range
      rate = self.tower_active.rate
      price = ''
    for item in self.shop_items:
      if item.rect.collidepoint(self.mouse_pos):
        dmg = TOWER_TYPES[item.type]['damage']
        rng = TOWER_TYPES[item.type]['range']
        rate = TOWER_TYPES[item.type]['rate']
        price = TOWER_TYPES[item.type]['price']
        break
    if self.buying:
      dmg = self.buying.damage
      rng = self.buying.range
      rate = self.buying.rate
      price = self.buying.price

    size = 32
    color = BLACK
    align = 'left'
    top = 50
    left = 30

    self.draw_text(
      'arial', size, f'Damage: {str(dmg)}', color,
      self.info.x + left, self.info.y + top, align
    )
    self.draw_text(
      'arial', size, f'Range: {str(rng)}', color,
      self.info.x + left, self.info.y + top + 40, align
    )
    self.draw_text(
      'arial', size, f'Fire rate: {str(dmg)}', color,
      self.info.x + left, self.info.y + top + 80, align
    )
    self.draw_text(
      'arial', size, f'${str(price)}', color,
      self.info.x + left, self.info.y + top + 120, align
    )

  def draw(self):
    self.screen.blit(self.map_img, (0,0))
    if self.buying or self.tower_active:
      if self.buying:
        r = self.buying.range
        x = self.buying.rect.centerx
        y = self.buying.rect.centery
      elif self.tower_active:
        r = self.tower_active.range
        x = self.tower_active.rect.centerx
        y = self.tower_active.rect.centery

      circle_surface = pg.Surface((r*2, r*2), pg.SRCALPHA)
      pg.draw.circle(circle_surface, (255,255,255,50), (r, r), r)
      self.screen.blit(circle_surface, (x - r, y - r))

    self.all_sprites.draw(self.screen)

    self.draw_text( 
      'arial', 22, self.upgrade_btn.text, WHITE, 
      self.upgrade_btn.rect.centerx, self.upgrade_btn.rect.centery, 'center'
    )
    self.draw_text( 
      'arial', 22, self.sell_btn.text, WHITE, 
      self.sell_btn.rect.centerx, self.sell_btn.rect.centery, 'center'
    )
    self.draw_text( 
      'arial', 26, 'Round ' + str(self.round), (0,11,115), 
      self.map_rect.width - 200, 50, 'center'
    )
    self.draw_text( 
      'arial', 26, 'Money: $' + str(self.money), (0,11,115), 
      self.map_rect.width - 200, 90, 'center'
    )
    self.draw_tower_info()
    pg.display.flip()

  def update(self):
    self.mouse_pos = pg.mouse.get_pos()
    self.all_sprites.update()
    if self.round_object:
      self.round_object.update()
    if self.lives <= 0:
      self.playing = False
    elif self.round >= len(list(ROUNDS)) and not self.round_active:
      self.playing = False
      self.victory = True

    if self.round_object:
      print(self.round_object.enemy_counter)

  def events(self):
    for event in pg.event.get():
      if event.type == pg.QUIT:
        self.quit()
      if event.type == pg.MOUSEBUTTONUP:
        
        if self.buying:
          valid_loc_found = False
          for tower_area in self.tower_areas:
            tower_x = self.buying.rect.centerx
            tower_y = self.buying.rect.centery
            tower_area_left = tower_area.x
            tower_area_right = tower_area.x + tower_area.w
            tower_area_top = tower_area.y
            tower_area_bottom = tower_area.y + tower_area.h
            if tower_x < tower_area_right and tower_x > tower_area_left \
              and tower_y < tower_area_bottom and tower_y > tower_area_top:
                tower_present = False
                for t in self.towers:
                  if self.buying is not t:
                    if self.buying.rect.collidepoint((t.rect.centerx, t.rect.centery)):
                      tower_present = True
                if not tower_present:
                  self.buying.placed = True
                  self.tower_active = self.buying
                  self.money -= self.buying.price
                  valid_loc_found = True
                  break
          if not valid_loc_found:
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
            if not self.next_round_btn.rect.collidepoint(self.mouse_pos):
              self.tower_active = None
        
        for item in self.shop_items:
          if item.rect.collidepoint(self.mouse_pos):
            if self.money >= item.price:
              self.buying = Tower(self, item.type, self.mouse_pos)
              break
        
        if not self.round_active:
          if self.next_round_btn.rect.collidepoint(self.mouse_pos):
            self.round += 1
            self.round_active = True
            self.round_object = Round(self, self.round)

  def wait_for_keys(self):
    waiting = True
    while waiting:
      self.clock.tick(FPS)
      for event in pg.event.get():
        if event.type == pg.QUIT:
          self.quit()
        if event.type == pg.MOUSEBUTTONUP:
          waiting = False

  def show_start_screen(self):
    self.screen.blit(self.images['screen']['start'], (0, 0))
    pg.display.flip()
    self.wait_for_keys()

  def show_end_screen(self):
    if self.victory:
      end_image = self.images['screen']['win']
    else:
      end_image = self.images['screen']['lose']
    self.screen.blit(end_image, (0, 0))
    pg.display.flip()
    self.wait_for_keys()
    self.playing = True

  def quit(self):
    pg.quit()
    sys.exit()


g = Game()
g.show_start_screen()
g.playing = True
while g.playing:
  g.new()
  g.run()
  g.show_end_screen()