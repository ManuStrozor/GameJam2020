import pygame
import os
from tkinter import *

from game import Game

WIDTH = 1280
HEIGHT = 720

VOLUME = 0.5

root = Tk()
x = root.winfo_screenwidth() / 2 - WIDTH / 2
y = root.winfo_screenheight() / 2 - HEIGHT / 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

pygame.display.set_caption("Lonely Space v1.0")
pygame.display.set_icon(pygame.image.load("assets/lonely_space_32.png"))
window = pygame.display.set_mode((WIDTH, HEIGHT))

game = Game(window, 30)

THEME = pygame.mixer.music.load("assets/audio/theme/main_theme.ogg")
pygame.mixer.music.set_volume(VOLUME)
pygame.mixer.music.play(loops=-1)
for key, value in game.audios.items():
    value.set_volume(VOLUME)

while game.running:

    for view in game.views:
        view.loop()

pygame.quit()
