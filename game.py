import pygame
from pygame.locals import *
import pickle
import tkinter as tk
from tkinter import ttk
from entities.player import Player
from entities.alien import Alien


class Game:

    def __init__(self, window, framerate):
        self.window = window
        self.clock = pygame.time.Clock()
        self.framerate = framerate
        self.font = pygame.font.SysFont('comicsans', 30, True)
        self.keyPressed = {}

        self.background = pygame.image.load("assets/background.png")
        self.bgRect = self.background.get_rect()
        self.bgDecalageX = -100
        self.bgDecalageY = -300
        self.bgRect.x += self.bgDecalageX
        self.bgRect.y += self.bgDecalageY

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
            return 0

        self.max_score = max(self.score, self.max_score)

        if self.spw_delay < self.max_spw_delay:
            self.spw_delay += 1
        else:
            self.spw_delay = 0
            self.all_aliens.add(Alien(self))

        # Evenements (clavier + souris)
        for event in pygame.event.get():

            # Evenements clavier
            if event.type == KEYDOWN:
                self.keyPressed[event.key] = True
            elif event.type == KEYUP:
                self.keyPressed[event.key] = False

            # Evenements souris
            if event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == pygame.BUTTON_LEFT:
                    self.player.weapon.fire()

            # Quitter la fenetre
            if event.type == QUIT:
                # Sauvegarde du score avant de Quitter
                self.save_game()
                return 0

        for alien in self.all_aliens:
            alien.update()
        self.player.update()
        return 1

    def draw(self):
        self.window.blit(self.background, self.bgRect)
        score = self.font.render('Score: ' + str(self.score), 1, (0, 0, 0))
        max_score = self.font.render('Max score: ' + str(self.max_score), 1, (0, 0, 0))
        self.window.blit(score, (10, 30))
        self.window.blit(max_score, (10, 10))

        for alien in self.all_aliens:
            alien.draw()

        self.player.draw()

        for bullet in self.player.weapon.all_bullets:
            bullet.move()
        self.player.weapon.all_bullets.draw(self.window)

        pygame.display.flip()
        self.clock.tick(self.framerate)

    def draw_lifebar(self, entity):
        pygame.draw.rect(self.window, (0, 0, 0), (entity.rect.x, entity.rect.y - 20, 50, 5))
        if entity.health > 0:
            pygame.draw.rect(self.window, (255, 0, 0),
                             (entity.rect.x, entity.rect.y - 20, (entity.health / entity.max_health) * 50, 5))

    def setImage(self, entity, newImage):
        if entity.image != newImage:
            entity.image = newImage

    def moveBGY(self, y):
        self.bgDecalageY += y / (self.window.get_height() / 2 / 50)
        self.bgRect.y = int(self.bgDecalageY)

    def moveBGX(self, x):
        self.bgDecalageX += x / (self.window.get_width() / 2 / 100)
        self.bgRect.x = int(self.bgDecalageX)

    def save_game(self):
        with open("save.data", "wb") as f:
            pickle.dump(self.max_score, f)

    def popupmsg(self, title, msg):
        popup = tk.Tk()
        popup.wm_title(title)
        label = ttk.Label(popup, text=msg, font=('comicsans', 10))
        label.pack(side="top", fill="x", pady=10)
        b1 = ttk.Button(popup, text="OK", command=popup.destroy)
        b1.pack()
        popup.mainloop()
