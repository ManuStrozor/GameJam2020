import pygame
import os
from tkinter import *

from game import Game

WIDTH = 1024
HEIGHT = 768
MAX_FPS = 120

root = Tk()
x = root.winfo_screenwidth() / 2 - WIDTH / 2
y = root.winfo_screenheight() / 2 - HEIGHT / 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

pygame.init()
pygame.display.set_caption("Lonely Space v1.0")
pygame.display.set_icon(pygame.image.load("assets/lonely_space_32.png"))
window = pygame.display.set_mode((WIDTH, HEIGHT))

game = Game(window, MAX_FPS)

game.get_audio("theme").set_volume(0.05)
game.get_audio("theme").play(loops=-1)

while game.running:

    for view in game.views:
        view.loop()

pygame.quit()
