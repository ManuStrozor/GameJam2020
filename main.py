import pygame
import os
from tkinter import *

from game import Game

WIDTH = 1024
HEIGHT = 768

VOLUME = 0

root = Tk()
x = root.winfo_screenwidth() / 2 - WIDTH / 2
y = root.winfo_screenheight() / 2 - HEIGHT / 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Lonely Space v1.0")
pygame.display.set_icon(pygame.image.load("assets/lonely_space_32.png"))
window = pygame.display.set_mode((WIDTH, HEIGHT))

game = Game(window, 120)

THEME = pygame.mixer.music.load("assets/audio/theme/main_theme.ogg")
pygame.mixer.music.set_volume(VOLUME)
if VOLUME != 0:
    pygame.mixer.music.play(loops=-1)
for key, value in game.audios.items():
    value.set_volume(VOLUME)

while game.running:

    for view in game.views:
        view.loop()

pygame.quit()
