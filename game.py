import pygame
from pygame.locals import *
import pickle
from entities.player import Player
from entities.alien import Alien
from map import Map

screen = pygame.display.set_mode((1024, 768))
class Wall:

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 50, 50)

walls = []  # Liste des murs
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
    "WWWWWWWW   WWWWWWWWW",
]

# pour chaque caracteres du string : W = mur, E = porte du bas, B = porte du haut
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            porte1 = pygame.Rect(x, y, 50, 50)
        if col == "B":
            porte2 = pygame.Rect(x, y, 50, 50)
        x += 50
    y += 50
    x = 0


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
            pass
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
        # Murs
        for wall in walls:
            pygame.draw.rect(screen, (255, 255, 255), wall.rect)

        pygame.draw.rect(screen, (0, 255, 0), porte1)
        pygame.draw.rect(screen, (255, 0, 0), porte2)

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
