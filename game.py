import pygame
from pygame.locals import *

from level import gen_levels
from player import Player
from views.views import Menu, Pause, Opts, Cred, Help, Gameover, Win


def float_to_str(n, d=0):
    f = "{0:."+str(d)+"f}"
    return f.format(n)


class Score:

    player_coins = None
    player_oxygen_bottle = None

    def __init__(self, game):
        self.game = game
        self.score_font = pygame.font.SysFont('Consolas', 20)

    def update(self):
        self.fps_info = self.score_font.render("FPS : " + float_to_str(self.game.clock.get_fps()), True,
            pygame.Color("red"), pygame.Color("black"))

        self.player_coins = self.score_font.render(str(self.game.player.coins), True,
            pygame.Color("yellow"), pygame.Color("black"))

        self.player_oxygen_bottle = self.score_font.render(float_to_str(self.game.player.oxygen_bottle), True,
            pygame.Color("lightblue"), pygame.Color("black"))

    def draw(self):
        self.game.window.blit(self.fps_info, (self.game.window.get_width() - 120, 10))

        self.game.window.blit(pygame.transform.scale(self.game.get_image("coin"), (30, 30)), (0, 0))
        self.game.window.blit(self.player_coins, (30, 10))

        self.game.window.blit(pygame.transform.scale(self.game.get_image("oxygen"), (30, 30)), (0, 30))
        self.game.window.blit(self.player_oxygen_bottle, (30, 40))

        if self.game.player.chaussure:
            self.game.window.blit(pygame.transform.scale(self.game.get_image("chaussure"), (30, 30)), (0, 60))


class Game:

    WIDTH = 1024
    HEIGHT = 720

    running = 1
    state = 1

    levels = []
    niveau = None

    player = None
    spawn = (-1, -1)

    def __init__(self, window, framerate):
        self.window = window
        self.framerate = framerate
        self.clock = pygame.time.Clock()

        self.MARGIN_X = (window.get_width() - self.WIDTH) / 2
        self.MARGIN_Y = (window.get_height() - self.HEIGHT) / 2

        self.views = [Menu(self), Pause(self), Opts(self), Cred(self), Help(self), Gameover(self), Win(self)]
        self.last_view = None
        self.curr_view = "menu"

        self.load_assets()

    def load_assets(self):
        self.audios = {
            "coins": pygame.mixer.Sound('assets/audio/coins.wav'),
            "walk": pygame.mixer.Sound('assets/audio/walk.wav'),
            "oxygen_bottle": pygame.mixer.Sound('assets/audio/air_fill.wav'),
            "door": pygame.mixer.Sound('assets/audio/close_door_1.wav'),
            "button": pygame.mixer.Sound('assets/audio/button_press.wav'),
            "chaussure_propulsion": pygame.mixer.Sound('assets/audio/chaussure_propulsion.wav'),
            "chaussure": pygame.mixer.Sound('assets/audio/chaussure_lacet.wav'),
            "electric": pygame.mixer.Sound('assets/audio/electric.wav'),
            "water": pygame.mixer.Sound('assets/audio/water.wav'),
            "moving_box": pygame.mixer.Sound('assets/audio/moving_box_s.wav')
        }

        self.images = {
            "player": pygame.image.load('assets/player.png'),
            "wall": pygame.image.load('assets/wall.png'),
            "wind_jet": pygame.image.load('assets/wind_jet.png'),
            "box": pygame.image.load('assets/caisse.png'),
            "coin": pygame.image.load('assets/coin.png'),
            "floor": pygame.image.load('assets/floor.png'),
            "oxygen": pygame.image.load('assets/oxygen_bottle.png'),
            "button": pygame.image.load('assets/red_button.png'),
            "button_pressed": pygame.image.load('assets/grey_button.png'),
            "porte": pygame.image.load('assets/porte_unlock.png'),
            "porte_lock": pygame.image.load('assets/porte_lock.png'),
            "dalle_electrique": pygame.image.load('assets/electric.png'),
            "chaussure": pygame.image.load('assets/flashy_boots.png'),
            "dalle_innonde": pygame.image.load('assets/floor_water.png'),
            "decor_etagere": pygame.image.load('assets/decor_etagere.png'),
            "decor_electric_pillar": pygame.image.load('assets/decor_electric_pillar.png'),
            "decor_poubelle": pygame.image.load('assets/decor_poubelle.png'),
            "decor_boite": pygame.image.load('assets/decor_boite.png'),
            "decor_four": pygame.image.load('assets/decor_four.png'),
            "event_fin": pygame.image.load('assets/computer.png'),
            "saas": pygame.image.load('assets/saas.png')
        }

    def load_levels(self):
        self.levels = gen_levels(self, "levels.txt")
        for level in self.levels:
            level.init_structure()
        if self.spawn == (-1, -1):
            print("[ERROR] Il n'y a pas de point de spawn défini pour le joueur !")
            exit()

    def run(self, last_view):
        if last_view == "menu":
            self.load_levels()
            self.player = Player(self, self.spawn)
            self.score = Score(self)
        self.state = 1
        while self.state:
            self.update()
            self.draw()

    def exit(self):
        self.running = 0
        self.state = 0
        for view in self.views:
            view.state = 0

    def update(self):

        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                self.goto("pause")
            if e.type == QUIT:
                self.goto("exit")

        self.player.update()
        self.score.update()

        self.clock.tick(self.framerate)

    def draw(self):

        # Affichage du sol
        self.window.fill((0, 0, 0))
        y = 0
        while y < self.niveau.height:
            x = 0
            while x < self.niveau.width:
                self.window.blit(self.get_image("floor"),
                    (x * self.niveau.size_x + self.MARGIN_X, y * self.niveau.size_y + self.MARGIN_Y))
                x += 1
            y += 1

        # Affichage des blocs
        for obj in self.niveau.objs:
            if obj.type is not None:
                obj.draw()

        # Affichage des saas
        for saas in self.niveau.d_objs["saas"]:
            self.window.blit(self.get_image("saas"), (saas.rect.x, saas.rect.y))

        self.player.draw()

        self.score.draw()

        pygame.display.flip()

    def set_lvl(self, num):
        self.niveau = self.levels[num-1]
        if self.player is not None:
            self.player.rect.width = self.niveau.size_x
            self.player.rect.height = self.niveau.size_y

    def get_image(self, name):
        if name == "player":
            return pygame.transform.scale(self.images.__getitem__(name), (self.niveau.size_x*4, self.niveau.size_y*4))
        else:
            return pygame.transform.scale(self.images.__getitem__(name), (self.niveau.size_x, self.niveau.size_y))

    def get_audio(self, name):
        return self.audios.__getitem__(name)

    def goto(self, next_view):
        if next_view is not None:
            if next_view != "menu":
                self.last_view = self.curr_view
            else:
                self.last_view = None
            self.curr_view = next_view
            for view in self.views:
                if view.name == next_view:
                    view.state = 1
                else:
                    view.state = 0
            if next_view != "game":
                self.state = 0
            else:
                self.run(self.last_view)
            if next_view == "exit":
                self.exit()
