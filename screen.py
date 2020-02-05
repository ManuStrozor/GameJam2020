import pygame
pygame.font.init()

pygame.init()
win = pygame.display.set_mode((1024, 768))

font_titre = pygame.font.SysFont('comicsans', 85, True)
font = pygame.font.SysFont('comicsans', 40, True)

TEXT = 'Rien..'

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



################### Score screen ########################



def draw_menu():
    # Dessins
    pygame.draw.rect(win, GREY, rect_play)
    pygame.draw.rect(win, GREY, rect_cred)
    pygame.draw.rect(win, GREY, rect_help)
    pygame.draw.rect(win, GREY, rect_quit)
    # Textes
    win.blit(pygame.image.load('assets/background.png'), (0, 0))
    text_menu = font_titre.render('Menu', 1, (255, 0, 255))
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

    gerer_event_menu()

def gerer_event_menu():
    global TEXT
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
            TEXT = 'Rien..'

        ## Détecte les clique de souris.
        pressed = pygame.mouse.get_pressed()
        if pressed[0] and over_play:  # 0=gauche, 1=milieu, 2=droite
            draw_pause()
            pygame.display.update()
        if pressed[0] and over_cred:
            TEXT = 'Voir les crédits'
        if pressed[0] and over_help:
            TEXT = 'Voir l\'aide'
        if pressed[0] and over_quit:
            TEXT = 'Quitter le jeu'


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

    gerer_event_pause()

def gerer_event_pause():
    global TEXT
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
            TEXT = 'Sauvegarder et retourner a l\'acceuil'
        else:
            TEXT = 'Rien..'

        ## Détecte les clique de souris.
        pressed = pygame.mouse.get_pressed()
        if pressed[0] and over_resume:  # 0=gauche, 1=milieu, 2=droite
            TEXT = 'Reprendre la partie'
        if pressed[0] and over_save:  # 0=gauche, 1=milieu, 2=droite
            TEXT = 'Sauvegarder la partie'
        if pressed[0] and over_return:  # 0=gauche, 1=milieu, 2=droite
            draw_menu()
            pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    draw_menu()
    pygame.display.update()

pygame.quit()
