import pygame as pg
from pygame.sprite import Sprite
import sys
import os
import fnmatch
vec = pg.math.Vector2

pg.init()
pg.display.set_mode((1500, 750))

def load_data(self):
  game_folder = os.path.dirname(__file__)
  img_folder = os.path.join(game_folder, "images")
  snd_folder = os.path.join(game_folder, "sounds")

  image_folders = []
  sound_folders = []
  for file in os.listdir(img_folder):
    f = os.path.join(img_folder, file)
    if os.path.isdir(f):
      image_folders.append(f)

  for file in os.listdir(snd_folder):
    f = os.path.join(snd_folder, file)
    if os.path.isdir(f):
      sound_folders.append(f)

  self.images = {}
  self.sounds = {}

  for folder in image_folders:
    basename = os.path.basename(folder)
    self.images[basename] = {}

    images = fnmatch.filter(os.listdir(folder), '*.png')
    for img in images:
      self.images[basename][img[0:-4]] = pg.image.load(
        os.path.join(folder, img)).convert_alpha()

  for folder in sound_folders:
    basename = os.path.basename(folder)
    self.sounds[basename] = {}

    sounds = fnmatch.filter(os.listdir(folder), '*.wav')
    for snd in sounds:
      self.sounds[basename][snd[0:-4]] = pg.mixer.Sound(
        os.path.join(folder, snd))


class Tank(Sprite):
  def __init__(self, game):
    Sprite.__init__(self, game.tanks)
    self.game = game
    self.image = self.game.images['towers']['blue_tank']
    self.rect = self.image.get_rect()
    self.rect.center = (200, 200)
    self.barrel = Barrel(self.game, self.rect.center)

  def update(self):
    pass


class Barrel(Sprite):
  def __init__(self, game, pos):
    Sprite.__init__(self, game.barrels)
    self.game = game
    self.original_image = self.game.images['towers']['blue_tank_barrel']
    self.image = self.original_image
    self.rect = self.image.get_rect()
    self.rect.center = pos
    self.rot = 0

  def rotate(self):
    self.image = pg.transform.rotate(self.original_image, self.rot)
    self.rect = self.image.get_rect(center=self.rect.center)
    self.rot += 1

  def update(self):
    self.rotate()


class Game:
  def __init__(self):
    pg.display.set_caption('try-out')
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((1500, 750))
    load_data(self)

  def new(self):
    self.tanks = pg.sprite.Group()
    self.barrels = pg.sprite.Group()
    Tank(self)
    
  def run(self):
    self.playing = True
    while self.playing:
      self.clock.tick(30)
      self.events()
      self.update()
      self.draw()

  def draw(self):
    self.screen.fill((255,255,255))
    self.tanks.draw(self.screen)
    self.barrels.draw(self.screen)
    pg.display.flip()

  def update(self):
    self.tanks.update()
    self.barrels.update()

  def events(self):
    for event in pg.event.get():
      if event.type == pg.QUIT:
        self.quit()

  def quit(self):
    pg.quit()
    sys.exit()


g = Game()
while True:
  g.new()
  g.run()