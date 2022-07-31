import pygame as pg
from pygame.sprite import Sprite, Group
from settings import *


class MenuManager:
  def __init__(self, game):
    self.game = game
    self.button_functions()
    self.load_menus()

  def load_menus(self):
    self.menus = {}
    for object_group in self.game.asset_manager.map.tmxdata.objectgroups:
      if object_group.name[-4:] == 'menu':
        self.menus[object_group.name] = Menu(self.game, self, object_group.name)

  def show_menu(self, menu):
    self.active = True
    self.menus[menu].draw_menu()
    while self.active:
      self.game.clock.tick(FPS)
      for event in pg.event.get():
        if event.type == pg.QUIT:
          self.game.quit()
        if event.type == pg.MOUSEBUTTONUP:
          mouse_pos = pg.mouse.get_pos()
          for button in self.menus[menu].buttons:
            if button.rect.collidepoint(mouse_pos):
              self.game.asset_manager.sounds['buttons']['button_click'].play()
              button.action()
        if event.type == pg.KEYDOWN:
          if event.key == pg.K_SPACE:
            self.active = False

  def button_functions(self):
    self.button_actions = {}
    def play():
      self.active = False
    def play_again():
      self.active = False
      self.game.reset_game()
    
    self.button_actions['Help'] = lambda: print('help')
    self.button_actions['Settings'] = lambda: self.show_menu('settings_menu')
    self.button_actions['Play'] = lambda: play()
    self.button_actions['Sound'] = lambda: print('sound')
    self.button_actions['Graphics'] = lambda: print('graphics')
    self.button_actions['Back to main menu'] = lambda: self.show_menu('main_menu')
    self.button_actions['Play again'] = lambda: play_again()
    self.button_actions['Quit'] = lambda: self.game.quit()


class Menu:
  def __init__(self, game, menu_manager, menu):
    self.game = game
    self.menu_manager = menu_manager
    self.menu = menu
    self.buttons = Group()
    self.load_menu()

  def load_menu(self):
    for object_group in self.game.asset_manager.map.tmxdata.objectgroups:
      if object_group.name == self.menu:
        for btn in object_group:
          action = self.menu_manager.button_actions[btn.name]
          MenuButton(self, btn, action)

  def draw_menu(self):
    self.game.screen.blit(self.game.asset_manager.map_img, (0,0))
    self.buttons.draw(self.game.screen)
    for btn in self.buttons:
      self.game.draw_text(self.game.screen, 'arial', 28, btn.name, MENU_BTNS_TXT_COLOR, btn.rect.centerx, btn.rect.centery, 'center')
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
    self.image.fill(MENU_BTNS_COLOR)
    self.rect = self.image.get_rect()
    self.rect.center = (pos['x'], pos['y'])
    self.action = action

  def clicked(self):
    self.action()