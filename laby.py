#! /usr/bin/env python

import os
import random
import pygame


# Joueur (cube orange)
class Player(object):

    def __init__(self):
        self.rect = pygame.Rect(32, 32, 16, 16)

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


# Wall
class Wall:

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)


pygame.init()

pygame.display.set_caption("Sortez par une porte rouge!")
screen = pygame.display.set_mode((320, 240))

clock = pygame.time.Clock()
walls = []  # Liste des murs
player = Player()  # Creation joueur

# Contenu de la map dans un string
level = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W                  B",
    "W         WWWWWW   W",
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
            porte1 = pygame.Rect(x, y, 16, 16)
        if col == "B":
            porte2 = pygame.Rect(x, y, 16, 16)
        x += 16
    y += 16
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
        raise SystemExit
    if player.rect.colliderect(porte2):
        print("sortie porte 2")
        raise SystemExit

    # Draw
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)

    pygame.draw.rect(screen, (255, 0, 0), porte1)
    pygame.draw.rect(screen, (255, 0, 0), porte2)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    pygame.display.flip()