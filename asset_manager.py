import pygame as pg
import os
import fnmatch

from settings import *
from tilemap import *

class AssetManager:
  def __init__(self, game):
    self.game = game
    self.load_data()


  def load_data(self):
    game_folder = os.path.dirname(__file__)
    map_folder = os.path.join(game_folder, "map")
    self.map = TiledMap(os.path.join(map_folder , 'map.tmx'))
    self.map_img = self.map.make_map()
    self.map_rect = self.map_img.get_rect()

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
        sounds_folders.append(f)

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