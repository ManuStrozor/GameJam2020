import pygame
from math import pi
from pygame.locals import *
pygame.font.init()

pygame.init()
win = pygame.display.set_mode((1024, 768))

font_titre = pygame.font.SysFont('comicsans', 85, True)
font = pygame.font.SysFont('comicsans', 40, True)

GREY = pygame.Color(220, 220, 220)
size = (500, 80)
bouton = pygame.Surface(size)
pygame.draw.rect(bouton, GREY, bouton.get_rect())
bouton_play = bouton
bouton_cred = bouton
bouton_help = bouton
bouton_quit = bouton

TEXT = 'Rien..'

def draw_menu():
    # Textes
    win.blit(pygame.image.load('assets/background.png'), (0, 0))
    text_menu = font_titre.render('Menu', 1, (255, 0, 255))
    text_play = font.render('Jouer', 1, (255, 0, 255))
    text_cred = font.render('Crédits', 1, (255, 0, 255))
    text_help = font.render('Aide', 1, (255, 0, 255))
    text_quit = font.render('Quitter', 1, (255, 0, 255))
    text_survol = font.render(TEXT, 1, (255, 0, 255))

    # Blit
    win.blit(text_menu, (420, 130))
    win.blit(bouton_play, (256, 250))
    win.blit(text_play, (256, 250))
    win.blit(bouton_cred, (256, 350))
    win.blit(text_cred, (256, 350))
    win.blit(bouton_help, (256, 450))
    win.blit(text_help, (256, 450))
    win.blit(bouton_quit, (256, 550))
    win.blit(text_quit, (256, 550))
    win.blit(text_survol, (256, 650))

def gerer_event():
    global TEXT
    # Si le focus est sur la fenêtre.
    if pygame.mouse.get_focused():
        # Trouve position de la souris
        x, y = pygame.mouse.get_pos()
        over_play = bouton_play.get_rect().collidepoint(x, y)
        over_cred = bouton_cred.get_rect().collidepoint(x, y)
        over_help = bouton_help.get_rect().collidepoint(x, y)
        over_quit = bouton_quit.get_rect().collidepoint(x, y)
        if over_play:
            TEXT = 'Je veux jouer'
        if over_cred:
            TEXT = 'Voir les crédits'
        if over_help:
            TEXT = 'Voir l\'aide'
        if over_quit:
            TEXT = 'Quitter le jeu'
        else :
            TEXT = 'Rien..'

        ## Détecte les clique de souris.
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:  # 0=gauche, 1=milieu, 2=droite
            print('Click gauche')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    draw_menu()
    gerer_event()
    pygame.display.flip()
    pygame.display.update()

pygame.quit()
