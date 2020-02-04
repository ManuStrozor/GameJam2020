#! /usr/bin/env python

import os
import random
import pygame


# Joueur (cube orange)
class Player(object):

    def __init__(self):
        self.rect = pygame.Rect(64, 64, 32, 32)

    def move(self, dx, dy):
        # deplacement rect
        self.rect.x += dx
        self.rect.y += dy

        # Collision mur
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # deplacement droit, si coté gauche du mur touché
                    self.rect.right = wall.rect.left
                if dx < 0:  # deplacement gauche, si coté droit du mur touché
                    self.rect.left = wall.rect.right
                if dy > 0:  # deplacement bas, si coté haut du mur touché
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # deplacement haut, si coté bas du mur touché
                    self.rect.top = wall.rect.bottom


        # Collision caisse
        for caisse in caisses:
            if self.rect.colliderect(caisse.rect):
                if dx > 0:  # deplacement droit, si coté gauche caisse touché alors caisse se deplace avec le joueur
                    caisse.rect.right = caisse.rect.right + dx
                if dx < 0:  # deplacement gauche, si coté droit caisse touché alors caisse se deplace avec le joueur
                    caisse.rect.left = caisse.rect.left + dx
                if dy > 0:  # deplacement bas, si coté haut du caisse touché alors caisse se deplace avec le joueur
                    caisse.rect.bottom = caisse.rect.bottom + dy
                if dy < 0:  # deplacement haut, si coté bas du caisse touché alors caisse se deplace avec le joueur
                    caisse.rect.top = caisse.rect.top + dy

        # Collision souffleur
        for souffleur in souffleurs:
            if self.rect.colliderect(souffleur.rect):
                if dx > 0:  # deplacement opposé au souffleur si celui ci est touché
                    self.rect.right = souffleur.rect.left - 20*dx
                if dx < 0:  # deplacement opposé au souffleur si celui ci est touché
                    self.rect.left = souffleur.rect.right - 20*dx
                if dy > 0:  # deplacement opposé au souffleur si celui ci est touché
                    self.rect.bottom = souffleur.rect.top - 20*dy
                if dy < 0:  # deplacement opposé au souffleur si celui ci est touché
                    self.rect.top = souffleur.rect.bottom - 20*dy

        # Collision pieces (coins)
        for piece in pieces:
            if self.rect.colliderect(piece.rect):
                print("+1 score")
                pygame.draw.rect(screen, (0, 0, 0), piece.rect) # à modif, update texture suppr piece


# Wall
class Wall:

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

class Caisse:

    def __init__(self, pos):
        caisses.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

class Souffleur:

    def __init__(self, pos):
        souffleurs.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

class Piece:

    def __init__(self, pos):
        pieces.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

pygame.init()

pygame.display.set_caption("Sortez par une porte rouge!")
screen = pygame.display.set_mode((640, 480))

clock = pygame.time.Clock()
walls = []  # Liste des murs
caisses = [] # Liste des caisses
souffleurs = [] # Liste des souffleurs
pieces = [] # Liste des pieces (coins)
player = Player()  # Creation joueur

# Contenu de la map dans un string
level = [
    "WWWWWWWWWSSWWWWWWWWW",
    "W W     W          B",
    "W     C   WWWWWW   W",
    "W   WWWW       W   W",
    "W   W        WWWW  W",
    "W WWW  WWWW        W",
    "W   W     W W      W",
    "W   W     W   WWW WW",
    "W   WWW WWW   W W  W",
    "W     W   W   W W  W",
    "WWW   W   WWWWW W  W",
    "W W      WW        W",
    "W W   WWWW   WWW   W",
    "W     W       W    E",
    "WWWWWWWWWWWWWWWWWWWW",
]

# pour chaque caracteres du string : W = mur, E = porte du bas, B = porte du haut
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            porte1 = pygame.Rect(x, y, 32, 32)
        if col == "B":
            porte2 = pygame.Rect(x, y, 32, 32)
        if col == "C":
            Caisse((x, y))
        if col == "S":
            Souffleur((x, y))
        if col == "P":
            Piece((x, y))
        x += 32
    y += 32
    x = 0

running = True
while running:

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    # deplacement joueur
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)

    # conditions fin
    if player.rect.colliderect(porte1):
        print("sortie porte 1")
        raise SystemExit # à modif, appel nouvelle fenetre de jeu
    if player.rect.colliderect(porte2):
        print("sortie porte 2")
        raise SystemExit # à modif, appel nouvelle fenetre de jeu

    # Draw
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    for caisse in caisses:
        pygame.draw.rect(screen, (150, 0, 0), caisse.rect)
    for souffleur in souffleurs:
        pygame.draw.rect(screen, (0, 0, 255), souffleur.rect)
    for piece in pieces:
        pygame.draw.rect(screen, (0, 255, 0), piece.rect)
    pygame.draw.rect(screen, (255, 0, 0), porte1)
    pygame.draw.rect(screen, (255, 0, 0), porte2)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    pygame.display.flip()