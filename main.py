import pygame
from pygame.locals import *
from game import Game
pygame.init()

# Fenêtre du jeu
pygame.display.set_caption("GameJam 2020")
win = pygame.display.set_mode((1024, 768))

# Chargement du jeu
game = Game(win, 120)

font = pygame.font.SysFont('comicsans', 30, True)

# Boucle infinie
while game.screens.get("run"):

    while game.screens.get("menu"):
        win.blit(pygame.image.load('assets/background.png'), (0, 0))
        text = font.render('Menu', 1, (255, 0, 255))
        win.blit(text, (10, 10))
        pygame.display.flip()

        for event in pygame.event.get():
            # Quitter la fenetre
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    game.screen("game")
                if event.key == K_ESCAPE:
                    game.screen("")
                    game.screens.__setitem__("run", 0)

    while game.screens.get("game"):
        # Update du jeu
        game.update()
        # Affichage du jeu + Refresh
        game.draw()

    while game.screens.get("gameover"):
        win.blit(pygame.image.load('assets/background.png'), (0, 0))
        text = font.render('GameOver', 1, (255, 0, 0))
        win.blit(text, (10, 10))
        pygame.display.flip()

        for event in pygame.event.get():
            # Quitter la fenetre
            if event.type == KEYDOWN:
                game.screen("menu")
                game = Game(win, 120)
            elif event.type == QUIT:
                game.screen("")
                game.screens.__setitem__("run", 0)

pygame.quit()
