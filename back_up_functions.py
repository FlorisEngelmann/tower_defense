# def button_functions(self):
#   self.button_actions = {}
#   def play():
#     self.playing = True
#   def play_again():
#     self.reset_game()

#   self.button_actions['Help'] = lambda: print('help')
#   self.button_actions['Settings'] = lambda: self.show_menu('settings_menu')
#   self.button_actions['Play'] = lambda: play()
#   self.button_actions['Sound'] = lambda: print('sound')
#   self.button_actions['Graphics'] = lambda: print('graphics')
#   self.button_actions['Back to main menu'] = lambda: self.show_menu('main_menu')
#   self.button_actions['Play again'] = lambda: play_again()
#   self.button_actions['Quit'] = lambda: self.quit()

# def load_menus(self):
#   self.menus = {}
#   for object_group in self.map.tmxdata.objectgroups:
#     if object_group.name[-4:] == 'menu':
#       self.menus[object_group.name] = Menu(self, object_group.name)

# def show_menu(self, menu):
#   self.playing = False
#   self.menus[menu].draw_menu()
#   while not self.playing:
#     self.clock.tick(FPS)
#     for event in pg.event.get():
#       if event.type == pg.QUIT:
#         self.quit()
#       if event.type == pg.MOUSEBUTTONUP:
#         mouse_pos = pg.mouse.get_pos()
#         for button in self.menus[menu].buttons:
#           if button.rect.collidepoint(mouse_pos):
#             button.action()



# class Bullet(Sprite):
#   def __init__(self, game, x, y, direction, damage):
#     Sprite.__init__(self, game.all_sprites, game.level_object.bullets)
#     self.game = game
#     self.direction = direction
#     self.image = pg.Surface((10, 10))
#     self.image.fill(BLACK)
#     self.rect = self.image.get_rect()
#     self.rect.center = vec(x, y)
#     self.damage = damage

#   def move(self):
#     self.rect.centerx += self.direction[0]
#     self.rect.centery += self.direction[1]

#   def update(self):
#     self.move()
#     if self.rect.centerx < 0 or self.rect.centerx > self.game.map_rect.width:
#       if self.rect.centery < 0 or self.rect.centery > self.game.map_rect.height:
#         self.kill()