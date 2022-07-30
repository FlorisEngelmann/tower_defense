d = {'frame_0': 100, 'frame_1': 200, 'frame_2': 300}
frame = 0


def animate(folder):
  global frame
  n_images = len(folder.keys())
  print(frame)
  image = folder[f'frame_{(frame % n_images)}']
  frame += 1

  return image
