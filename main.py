import pygame
import os
from game import Game

from tkinter import *

root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

x = width / 2 - 1024 / 2
y = height / 2 - 768 / 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

pygame.init()
pygame.display.set_caption("Lonely Space v1.0")
win = pygame.display.set_mode((1024, 768))
icon_32x32 = pygame.image.load("assets/lonely_space_32.png")
pygame.display.set_icon(icon_32x32)

font_titre = pygame.font.SysFont('comicsans', 85, True)
font = pygame.font.SysFont('comicsans', 40, True)

game = Game(win, 120)

TEXT = None
GREY = (220, 220, 220)
size = (512, 80)


###################### Ecran Menu  ########################

bouton_play = pygame.Surface(size)
rect_play = bouton_play.get_rect()
rect_play.x = 256
rect_play.y = 250

bouton_cred = pygame.Surface(size)
rect_cred = bouton_cred.get_rect()
rect_cred.x = 256
rect_cred.y = 350

bouton_help = pygame.Surface(size)
rect_help = bouton_help.get_rect()
rect_help.x = 256
rect_help.y = 450

bouton_back2 = pygame.Surface(size)
rect_back2 = bouton_back2.get_rect()
rect_back2.x = 256
rect_back2.y = 400

bouton_back = pygame.Surface(size)
rect_back = bouton_back.get_rect()
rect_back.x = 256
rect_back.y = 550

bouton_quit = pygame.Surface(size)
rect_quit = bouton_quit.get_rect()
rect_quit.x = 256
rect_quit.y = 550


#################### Ecran Pause  ########################


bouton_resume = pygame.Surface(size)
rect_resume = bouton_resume.get_rect()
rect_resume.x = 256
rect_resume.y = 250

bouton_save = pygame.Surface(size)
rect_save = bouton_save.get_rect()
rect_save.x = 256
rect_save.y = 350

bouton_return = pygame.Surface(size)
rect_return = bouton_return.get_rect()
rect_return.x = 256
rect_return.y = 550


##################### Game Over ########################


################## Winner Ending ########################

def draw_menu():
    # Dessins
    pygame.draw.rect(win, GREY, rect_play)
    pygame.draw.rect(win, GREY, rect_cred)
    pygame.draw.rect(win, GREY, rect_help)
    pygame.draw.rect(win, GREY, rect_quit)

    # Textes
    win.blit(pygame.image.load('assets/background.png'), (0, 0))
    text_menu = font_titre.render('-= Lonely Space =-', 1, (255, 0, 255))
    text_play = font.render('Jouer', 1, (255, 0, 255))
    text_cred = font.render('Crédits', 1, (255, 0, 255))
    text_help = font.render('Aide', 1, (255, 0, 255))
    text_quit = font.render('Quitter', 1, (255, 0, 255))
    text_survol = font.render(TEXT, 1, (255, 0, 255))

    # Blit
    win.blit(text_menu, (512-text_menu.get_rect().centerx, 130))
    win.blit(bouton_play, (256, 250))
    win.blit(text_play, (512-text_play.get_rect().centerx, 250+bouton_play.get_rect().centery-15))
    win.blit(bouton_cred, (256, 350))
    win.blit(text_cred, (512-text_cred.get_rect().centerx, 350+bouton_cred.get_rect().centery-15))
    win.blit(bouton_help, (256, 450))
    win.blit(text_help, (512-text_help.get_rect().centerx, 450+bouton_help.get_rect().centery-15))
    win.blit(bouton_quit, (256, 550))
    win.blit(text_quit, (512-text_quit.get_rect().centerx, 550+bouton_quit.get_rect().centery-15))
    win.blit(text_survol, (512-text_survol.get_rect().centerx, 650))

    pygame.display.flip()


def update_menu():
    global TEXT

    over_play = None
    over_cred = None
    over_help = None
    over_quit = None

    # Si le focus est sur la fenêtre.
    if pygame.mouse.get_focused():
        # Trouve position de la souris
        x, y = pygame.mouse.get_pos()
        over_play = rect_play.collidepoint(x, y)
        over_cred = rect_cred.collidepoint(x, y)
        over_help = rect_help.collidepoint(x, y)
        over_quit = rect_quit.collidepoint(x, y)

        if over_play:
            TEXT = 'Commencer a jouer'
        elif over_cred:
            TEXT = 'Voir les crédits'
        elif over_help:
            TEXT = 'Voir l\'aide'
        elif over_quit:
            TEXT = 'Quitter le jeu'
        else:
            TEXT = None

    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if over_play:  # 0=gauche, 1=milieu, 2=droite
                game.goto("game")
            elif over_cred:
                game.goto("cred")
                pass
            elif over_help:
                game.goto("help")
            elif over_quit:
                game.views.clear()
        if e.type == pygame.QUIT:
            game.views.clear()


def draw_pause():
    # Dessins
    pygame.draw.rect(win, GREY, rect_resume)
    pygame.draw.rect(win, GREY, rect_save)
    pygame.draw.rect(win, GREY, rect_return)
    # Textes
    win.blit(pygame.image.load('assets/background.png'), (0, 0))
    text_pause = font_titre.render('Pause', 1, (255, 0, 255))
    text_resume = font.render('Reprendre', 1, (255, 0, 255))
    text_save = font.render('Sauvegarder', 1, (255, 0, 255))
    text_return = font.render('Retour au menu', 1, (255, 0, 255))
    text_survol = font.render(TEXT, 1, (255, 0, 255))

    # Blit
    win.blit(text_pause, (512-text_pause.get_rect().centerx, 130))
    win.blit(bouton_play, (256, 250))
    win.blit(text_resume, (512-text_resume.get_rect().centerx, 250+bouton_play.get_rect().centery-15))
    win.blit(bouton_save, (256, 350))
    win.blit(text_save, (512-text_save.get_rect().centerx, 350+bouton_save.get_rect().centery-15))
    win.blit(bouton_return, (256, 550))
    win.blit(text_return, (512-text_return.get_rect().centerx, 550+bouton_return.get_rect().centery-15))
    win.blit(text_survol, (512-text_survol.get_rect().centerx, 650))

    pygame.display.flip()


def update_pause():
    global TEXT

    over_resume = None
    over_save = None
    over_return = None

    # Si le focus est sur la fenêtre.
    if pygame.mouse.get_focused():
        # Trouve position de la souris
        x, y = pygame.mouse.get_pos()
        over_resume = rect_resume.collidepoint(x, y)
        over_save = rect_save.collidepoint(x, y)
        over_return = rect_return.collidepoint(x, y)
        if over_resume:
            TEXT = 'Reprendre la partie'
        elif over_save:
            TEXT = 'Sauvegarder la partie'
        elif over_return:
            TEXT = 'Retourner a l\'acceuil'
        else:
            TEXT = None

    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if over_resume:  # 0=gauche, 1=milieu, 2=droite
                game.goto("game")
            elif over_save:  # 0=gauche, 1=milieu, 2=droite
                game.save_game()
            elif over_return:  # 0=gauche, 1=milieu, 2=droite
                game.goto("menu")
        if e.type == pygame.QUIT:
            game.views.clear()


def draw_cred():

    # Textes
    win.blit(pygame.image.load('assets/background.png'), (0, 0))
    text_credis = font_titre.render('Made by ToutSaufLaSalle21', 1, (255, 0, 255))
    text_manu = font.render('The Full of lover : Emmanuel Turbet-Delof', 1, (255, 0, 255))
    text_loic1 = font.render('The Glitcher : Loïc Allemand', 1, (255, 0, 255))
    text_yassine = font.render('The Debuger : Yassine El Mimouni', 1, (255, 0, 255))
    text_loic2 = font.render('The Assets finder : Loïc Chareron', 1, (255, 0, 255))
    text_yann = font.render('The Canada dryer : Yann Galan', 1, (255, 0, 255))
    text_quit = font.render('Retour', 1, (255, 0, 255))
    text_survol = font.render(TEXT, 1, (255, 0, 255))

    # Blit
    win.blit(text_credis, (512 - text_credis.get_rect().centerx, 130))
    win.blit(text_manu, (512 - text_manu.get_rect().centerx, 250 + bouton_play.get_rect().centery - 15))
    win.blit(text_loic1, (512 - text_loic1.get_rect().centerx, 300 + bouton_cred.get_rect().centery - 15))
    win.blit(text_yassine, (512 - text_yassine.get_rect().centerx, 350 + bouton_help.get_rect().centery - 15))
    win.blit(text_loic2, (512 - text_loic2.get_rect().centerx, 400 + bouton_quit.get_rect().centery - 15))
    win.blit(text_yann, (512 - text_yann.get_rect().centerx, 450 + bouton_quit.get_rect().centery - 15))
    win.blit(bouton_back, rect_back)
    win.blit(text_quit, (512 - text_quit.get_rect().centerx, 550 + bouton_quit.get_rect().centery - 15))
    win.blit(text_survol, (512 - text_survol.get_rect().centerx, 650))

    pygame.display.flip()


def update_cred():
    global TEXT

    over_back = None

    # Si le focus est sur la fenêtre.
    if pygame.mouse.get_focused():
        # Trouve position de la souris
        x, y = pygame.mouse.get_pos()
        over_back = rect_back.collidepoint(x, y)

        if over_back:
            TEXT = 'Retour au menu'
        else:
            TEXT = None

    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if over_back:  # 0=gauche, 1=milieu, 2=droite
                game.goto("menu")
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            game.goto("menu")
        if e.type == pygame.QUIT:
            game.views.clear()


def update_help():
    global TEXT

    over_back = None

    # Si le focus est sur la fenêtre.
    if pygame.mouse.get_focused():
        # Trouve position de la souris
        x, y = pygame.mouse.get_pos()
        over_back = rect_back2.collidepoint(x, y)

        if over_back:
            TEXT = 'Retour au menu'
        else:
            TEXT = None

    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if over_back:  # 0=gauche, 1=milieu, 2=droite
                game.goto("menu")
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            game.goto("menu")
        if e.type == pygame.QUIT:
            game.views.clear()


def draw_help():
    win.blit(pygame.image.load('assets/help.png'), (0, 0))
    text_quit = font.render('Retour', 1, (255, 0, 255))
    text_survol = font.render(TEXT, 1, (255, 0, 255))

    win.blit(bouton_back2, rect_back2)
    win.blit(text_quit, (512 - text_quit.get_rect().centerx, 400 + bouton_back2.get_rect().centery - 15))
    win.blit(text_survol, (512 - text_survol.get_rect().centerx, 500))

    pygame.display.flip()


def update_gameover():
    print("update gameover")
    pass


def draw_gameover():
    print("draw gameover")
    pass


def update_win():
    print("update Win")
    pass


def draw_win():
    print("draw Win")
    pass


game.get_audio("theme").set_volume(0.05)
game.get_audio("theme").play(loops=-1)

while game.views.get("run"):

    while game.views.get("menu"):
        update_menu()
        draw_menu()

    while game.views.get("game"):
        game.update()
        game.draw()

    while game.views.get("pause"):
        update_pause()
        draw_pause()

    while game.views.get("cred"):
        update_cred()
        draw_cred()

    while game.views.get("help"):
        update_help()
        draw_help()

    while game.views.get("gameover"):
        update_gameover()
        draw_gameover()

    while game.views.get("win"):
        update_win()
        draw_win()

pygame.quit()
