import pygame as pg
from pygame.sprite import Sprite, Group
from settings import *

class Menu:
  def __init__(self, game, menu):
    self.game = game
    self.menu = menu
    self.buttons = Group()
    self.load_menu()

  def load_menu(self):
    for object_group in self.game.map.tmxdata.objectgroups:
      if object_group.name == self.menu:
        for btn in object_group:
          action = self.game.button_actions[btn.name]
          MenuButton(self, btn, action)

  def draw_menu(self):
    self.game.screen.blit(self.game.map_img, (0,0))
    self.buttons.draw(self.game.screen)
    for btn in self.buttons:
      self.game.draw_text('arial', 16, btn.name, BLACK, btn.rect.centerx, btn.rect.centery, 'center')
    pg.display.flip()


class MenuButton(Sprite):
  def __init__(self, menu, tile_obj, action):
    self.menu = menu
    Sprite.__init__(self, self.menu.buttons)
    self.name = tile_obj.name
    pos = {
      'x': tile_obj.x + tile_obj.width / 2,
      'y': tile_obj.y + tile_obj.height / 2
    }
    self.image = pg.Surface((tile_obj.width, tile_obj.height))
    self.image.fill(RED)
    self.rect = self.image.get_rect()
    self.rect.center = (pos['x'], pos['y'])
    self.action = action

  def clicked(self):
    self.action()