import pygame
from game import Game
pygame.init()

# Fenêtre du jeu
pygame.display.set_caption("GameJam 2020")
win = pygame.display.set_mode((1280, 720))


# Chargement du jeu
game = Game(win, 60)

# Boucle infinie
running = 1
while running:

    # Update du jeu
    running = game.update()

    # Affichage du jeu + Refresh
    game.draw()

pygame.quit()
