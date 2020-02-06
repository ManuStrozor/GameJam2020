import pygame
from pygame.locals import *
import pickle

from niveau import Niveau
from score import Score


class Game:

    WIDTH = 800
    HEIGHT = 600

    clock = pygame.time.Clock()

    views = {
        "run": 1,
        "menu": 1,
        "game": 0,
        "pause": 0,
        "cred": 0,
        "help": 0,
        "gameover": 0
    }

    all_saas = []  # liste des saas
    objs = []  # Liste de tous les blocs
    walls = []  # Liste des murs
    caisses = []  # Liste des caisses
    souffleurs = []  # Liste des souffleurs
    pieces = []  # Liste des pieces (coins)
    oxygen_bottles = []  # Liste des bouteilles d'oxygene
    buttons = []  # Liste des boutons
    buttons_pressed = []  # Liste des boutons activés
    portes_unlock = []  # Liste des portes deverouilles
    portes_lock = []  # Liste des portes verouilles
    dalles_electriques = []  # Liste des dalles electriques
    chaussures = []  # Liste des chaussures à propulsion
    dalles_innondes = []  # Liste des dalles innondes

    game_lost = False
    max_score = 0
    score = 0

    def __del__(self):
        pass

    def __init__(self, window, framerate):
        self.window = window
        self.framerate = framerate

        self.MARGIN_X = (window.get_width() - self.WIDTH) / 2
        self.MARGIN_Y = (window.get_height() - self.HEIGHT) / 2

        self.niveau = Niveau(self)
        self.niveau.generer("rooms/room1.txt")
        self.player = self.niveau.afficher()
        self.score = Score(self)

        self.audio_coins = pygame.mixer.Sound('assets/audio/coins.wav')  # Son de pieces
        self.audio_walk = pygame.mixer.Sound('assets/audio/walk.wav')  # son de pas (clap, clap)
        self.audio_oxygen_bottle = pygame.mixer.Sound('assets/audio/air_fill.wav')  # Son de bouteille oxygene
        self.audio_door = pygame.mixer.Sound('assets/audio/close_door_1.wav')  # son de porte
        self.audio_button = pygame.mixer.Sound('assets/audio/button_press.wav')  # son de boutton
        self.audio_chaussure_propulsion = pygame.mixer.Sound('assets/audio/chaussure_propulsion.wav')  # son de propulsion air
        self.audio_chaussure_recup = pygame.mixer.Sound('assets/audio/chaussure_lacet.wav')  # son d'enfilage de chaussure
        self.audio_electric = pygame.mixer.Sound('assets/audio/electric.wav')  # son d'electricité
        self.audio_moving_box = pygame.mixer.Sound('assets/audio/moving_box_s.wav')  # son d'electricité

        self.wall_image = pygame.transform.scale(pygame.image.load('assets/wall.png'), (self.niveau.size_x, self.niveau.size_y))
        self.wind_image = pygame.transform.scale(pygame.image.load('assets/wind_jet.png'), (self.niveau.size_x, self.niveau.size_y))
        self.box_image = pygame.transform.scale(pygame.image.load('assets/caisse.png'), (self.niveau.size_x, self.niveau.size_y))
        self.coin_image = pygame.transform.scale(pygame.image.load('assets/coin.png'), (self.niveau.size_x, self.niveau.size_y))
        self.floor_image = pygame.transform.scale(pygame.image.load('assets/floor.png'), (self.niveau.size_x, self.niveau.size_y))
        self.oxygen_image = pygame.transform.scale(pygame.image.load('assets/oxygen_bottle.png'), (self.niveau.size_x, self.niveau.size_y))
        self.button_image = pygame.transform.scale(pygame.image.load('assets/red_button.png'), (self.niveau.size_x, self.niveau.size_y))
        self.button_pressed_image = pygame.transform.scale(pygame.image.load('assets/grey_button.png'), (self.niveau.size_x, self.niveau.size_y))
        self.porte_unlock_image = pygame.transform.scale(pygame.image.load('assets/porte_unlock.png'), (self.niveau.size_x, self.niveau.size_y))
        self.porte_lock_image = pygame.transform.scale(pygame.image.load('assets/porte_lock.png'), (self.niveau.size_x, self.niveau.size_y))
        self.dalle_electrique_image = pygame.transform.scale(pygame.image.load('assets/electric.png'), (self.niveau.size_x, self.niveau.size_y))
        self.chaussure_image = pygame.transform.scale(pygame.image.load('assets/flashy_boots.png'), (self.niveau.size_x, self.niveau.size_y))
        self.dalle_innonde_image = pygame.transform.scale(pygame.image.load('assets/floor_water.png'), (self.niveau.size_x, self.niveau.size_y))
        self.decor_etagere_image = pygame.transform.scale(pygame.image.load('assets/decor_etagere.png'), (self.niveau.size_x, self.niveau.size_y))
        self.decor_pillier_electrique_image = pygame.transform.scale(pygame.image.load('assets/decor_electric_pillar.png'), (self.niveau.size_x, self.niveau.size_y))
        self.decor_poubelle_image = pygame.transform.scale(pygame.image.load('assets/decor_poubelle.png'), (self.niveau.size_x, self.niveau.size_y))
        self.decor_boite_image = pygame.transform.scale(pygame.image.load('assets/decor_boite.png'), (self.niveau.size_x, self.niveau.size_y))
        self.decor_four_image = pygame.transform.scale(pygame.image.load('assets/decor_four.png'), (self.niveau.size_x, self.niveau.size_y))
        self.saas_image = pygame.transform.scale(pygame.image.load('assets/saas.png'), (self.niveau.size_x, self.niveau.size_y))

        try:
            with open("save.data", "rb") as f:
                self.max_score = pickle.load(f)
        except IOError:
            pass

    def update(self):

        self.clock.tick(self.framerate)

        if self.game_lost:
            self.save_game()
            self.goto("gameover")

        self.player.update()
        self.score.update()

        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                self.goto("pause")
            if e.type == QUIT:
                self.save_game()
                self.views.clear()

    def draw(self):
        # Affichage du sol
        self.window.fill((0, 0, 0))
        y = 0
        while y < self.niveau.height:
            x = 0
            while x < self.niveau.width:
                self.window.blit(self.floor_image, (x * self.niveau.size_x + self.MARGIN_X, y * self.niveau.size_y + self.MARGIN_Y))
                x += 1
            y += 1

        # Affichage des blocs
        for obj in self.objs:
            image = None
            if obj.type == "wall":
                image = self.wall_image
            elif obj.type == "box":
                image = self.box_image
            elif obj.type == "wind_jet":
                image = self.wind_image
            elif obj.type == "coin":
                image = self.coin_image
            elif obj.type == "oxygen":
                image = self.oxygen_image
            elif obj.type == "button":
                image = self.button_image
            elif obj.type == "button_pressed":
                image = self.button_pressed_image
            elif obj.type == "porte_lock":
                image = self.porte_lock_image
            elif obj.type == "porte_unlock":
                image = self.porte_unlock_image
            elif obj.type == "dalle_electrique":
                image = self.dalle_electrique_image
            elif obj.type == "chaussure":
                image = self.chaussure_image
            elif obj.type == "saas":
                image = self.saas_image
            elif obj.type == "dalle_innonde":
                image = self.dalle_innonde_image

            if image is not None:
                self.window.blit(image, (obj.rect.x, obj.rect.y))

        # Affichage des saas
        for saas in self.all_saas:
            self.window.blit(self.saas_image, (saas.rect.x, saas.rect.y))

        pygame.draw.rect(self.window, (255, 255, 0), self.player.rect)

        self.score.draw()

        pygame.display.flip()

    def clear_bloks(self):
        self.walls.clear()
        self.caisses.clear()
        self.souffleurs.clear()
        self.pieces.clear()
        self.oxygen_bottles.clear()
        self.chaussures.clear()
        self.dalles_electriques.clear()
        self.dalles_innondes.clear()
        self.portes_lock.clear()
        self.portes_unlock.clear()
        self.all_saas.clear()
        self.objs.clear()

    def get_saas(self, card):
        for saas in self.all_saas:
            if saas.cardinal == card:
                return saas

    def get_obj(self, x, y):
        return self.objs.__getitem__(y * 20 + x)

    #def draw_text(self, txt, position, col):
        #self.window.blit(self.font.render(txt, 1, col), position)

    def goto(self, screen):
        self.views.clear()
        self.views.__setitem__("run", 1)
        self.views.__setitem__(screen, 1)

    def get_view(self, view):
        return self.views.get(view)

    def save_game(self):
        with open("save.data", "wb") as f:
            pickle.dump(self.max_score, f)
