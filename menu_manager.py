import pygame as pg
from pygame.sprite import Sprite, Group
from settings import *


class MenuManager:
  def __init__(self, game):
    self.game = game
    self.create_button_functions()
    self.load_menus()

  def load_menus(self):
    self.menus = {}
    for object_group in self.game.asset_manager.map.tmxdata.objectgroups:
      if object_group.name[-4:] == 'menu':
        self.menus[object_group.name] = Menu(self.game, self, object_group.name)

  def show_menu(self, menu):
    self.active = True
    while self.active:
      self.menus[menu].draw_menu()
      self.game.clock.tick(FPS)
      for event in pg.event.get():
        if event.type == pg.QUIT:
          self.game.quit()
        if event.type == pg.MOUSEBUTTONUP:
          mouse_pos = pg.mouse.get_pos()
          for button in self.menus[menu].buttons:
            if button.rect.collidepoint(mouse_pos):
              self.game.asset_manager.sounds['buttons']['button_click'].set_volume(self.game.volume)
              self.game.asset_manager.sounds['buttons']['button_click'].play()
              button.action()
        if event.type == pg.KEYDOWN:
          if event.key == pg.K_SPACE:
            self.active = False

  def create_button_functions(self):
    self.button_actions = {}
    def play():
      if self.game.game_over:
        play_again()
        return
      self.active = False
    def play_again():
      self.active = False
      self.game.reset_game()
    def increase_sound():
      if self.game.volume < 0.95:
        self.game.volume += 0.1
    def decrease_sound():
      if self.game.volume > 0.05:
        self.game.volume -= 0.1
    
    self.button_actions['Info'] = lambda: self.show_menu('info_menu')
    self.button_actions['Settings'] = lambda: self.show_menu('settings_menu')
    self.button_actions['Play'] = lambda: play()
    self.button_actions['Increase Volume'] = lambda: increase_sound()
    self.button_actions['Decrease Volume'] = lambda: decrease_sound()
    self.button_actions['Sound'] = lambda: adjust_sound()
    self.button_actions['Graphics'] = lambda: print('graphics')
    self.button_actions['Back to main menu'] = lambda: self.show_menu('main_menu')
    self.button_actions['Play again'] = lambda: play_again()
    self.button_actions['Quit'] = lambda: self.game.quit()
    self.button_actions['Credits'] = lambda: self.show_menu('credits_menu')

  def draw_label(self, label):
    def draw_image(image, x, y):
      self.game.screen.blit(image, (x,y))
    def draw_text(text):
      self.game.draw_text(self.game.screen, 'arial', 28, text, WHITE, label.x, label.y, 'center')

    if label.name == 'Info':
      draw_image(self.game.asset_manager.images['widgets']['info'], label.x, label.y)
      return
    if label.name == 'Volume':
      draw_text(str(round(self.game.volume, 1)))
      return
    if label.name == 'Credits':
      draw_image(self.game.asset_manager.images['widgets']['credits'], label.x, label.y)


class Menu:
  def __init__(self, game, menu_manager, menu):
    self.game = game
    self.menu_manager = menu_manager
    self.menu = menu
    self.buttons = Group()
    self.labels = []
    self.load_menu()

  def load_menu(self):
    for object_group in self.game.asset_manager.map.tmxdata.objectgroups:
      if object_group.name == self.menu:
        for widget in object_group:
          if widget.type == 'button':
            action = self.menu_manager.button_actions[widget.name]
            MenuButton(self, widget, action)
          if widget.type == 'label_image' or widget.type == 'label_text':
            self.labels.append(widget)
            
  def draw_menu(self):
    if self.menu == 'victory_menu' or self.menu == 'lost_menu':
      self.game.screen.blit(self.game.asset_manager.images['menu'][self.menu], (0,0))
    elif not self.menu == 'pause_menu':
      self.game.screen.blit(self.game.asset_manager.images['menu']['main_menu'], (0,0))
    self.buttons.draw(self.game.screen)
    for btn in self.buttons:
      self.game.draw_text(self.game.screen, 'arial', 28, btn.name, MENU_BTNS_TXT_COLOR, btn.rect.centerx, btn.rect.centery, 'center')
    for label in self.labels:
      if label.type == 'label_image' or label.type == 'label_text':
        self.menu_manager.draw_label(label)
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
    self.image = self.menu.game.asset_manager.images['widgets']['green_button']
    self.image = pg.transform.scale(self.image, (tile_obj.width, tile_obj.height))
    self.rect = self.image.get_rect()
    self.rect.center = (pos['x'], pos['y'])
    self.action = action