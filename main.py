import pygame
import os
from game import Game

from tkinter import *

root = Tk()
x = root.winfo_screenwidth() / 2 - 1024 / 2
y = root.winfo_screenheight() / 2 - 768 / 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

pygame.init()

pygame.display.set_caption("Lonely Space v1.0")
pygame.display.set_icon(pygame.image.load("assets/lonely_space_32.png"))

win = pygame.display.set_mode((1024, 768))
game = Game(win, 120)

game.get_audio("theme").set_volume(0.05)
game.get_audio("theme").play(loops=-1)

while game.running:

    if game.game_win or game.game_lost:
        game.__del__()
        game = Game(win, 120)

    while game.gameloop:
        game.update()
        game.draw()

    for view in game.views:
        view.loop()

pygame.quit()
