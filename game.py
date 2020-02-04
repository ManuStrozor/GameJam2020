import pygame
from pygame.locals import *
import pickle
import tkinter as tk
from tkinter import ttk
from entities.player import Player
from entities.alien import Alien
from map import Map


class Game:

    def __init__(self, window, framerate):
        self.window = window
        self.clock = pygame.time.Clock()
        self.framerate = framerate
        self.font = pygame.font.SysFont('comicsans', 30, True)
        self.screens = {"run": 1, "menu": 1, "game": 0, "gameover": 0}
        self.keyPressed = {}

        self.background = pygame.image.load("assets/room.png")
        self.bgRect = self.background.get_rect()

        self.map = Map(self)

        self.max_score = 0
        self.score = 0
        try:
            with open("save.data", "rb") as f:
                self.max_score = pickle.load(f)
        except IOError:
            self.popupmsg("Warning message !!!", "The save file \"save.data\" does not exist !\n"
                                               "Will be created at the next quit")
        self.gameover = False
        self.player = Player(self)
        self.all_aliens = pygame.sprite.Group()
        self.max_spw_delay = 120
        self.spw_delay = 0

    def update(self):
        if self.gameover:
            # Sauvegarde du score avant de Quitter
            self.save_game()
            self.screen("gameover")

        self.max_score = max(self.score, self.max_score)

        if self.spw_delay < self.max_spw_delay:
            self.spw_delay += 1
        else:
            self.spw_delay = 0
            # self.all_aliens.add(Alien(self))

        # Evenements (clavier + souris)
        for event in pygame.event.get():

            # Evenements clavier
            if event.type == KEYDOWN:
                self.keyPressed[event.key] = True
                if event.key == K_ESCAPE:
                    self.save_game()
                    self.screen("menu")
            elif event.type == KEYUP:
                self.keyPressed[event.key] = False

            # Quitter la fenetre
            if event.type == QUIT:
                # Sauvegarde du score avant de Quitter
                self.save_game()
                self.screen("")
                self.screens.__setitem__("run", 0)

        self.map.update()
        for alien in self.all_aliens:
            alien.update()
        self.player.update()

    def draw(self):
        self.window.blit(self.background, self.bgRect)
        self.draw_text('Score: ' + str(self.score), (10, 30), (0, 0, 0))
        self.draw_text('Max score: ' + str(self.max_score), (10, 10), (0, 0, 0))

        for alien in self.all_aliens:
            alien.draw()
        self.player.draw()
        self.map.draw()

        pygame.display.flip()
        self.clock.tick(self.framerate)

    def draw_text(self, txt, position, color):
        self.window.blit(self.font.render(txt, 1, color), position)

    def setImage(self, entity, newImage):
        if entity.image != newImage:
            entity.image = newImage

    def save_game(self):
        with open("save.data", "wb") as f:
            pickle.dump(self.max_score, f)

    def screen(self, screen):
        self.screens.clear()
        self.screens.__setitem__("run", 1)
        if screen != "":
            self.screens.__setitem__(screen, 1)

    def popupmsg(self, title, msg):
        popup = tk.Tk()
        popup.wm_title(title)
        label = ttk.Label(popup, text=msg, font=('comicsans', 10))
        label.pack(side="top", fill="x", pady=10)
        b1 = ttk.Button(popup, text="OK", command=popup.destroy)
        b1.pack()
        popup.mainloop()
