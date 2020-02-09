import pygame
from pygame.locals import *
from views.views import Menu, Pause, Opts, Cred, Help, Gameover, Win
from niveau import Niveau
from player import Player


class Score:

    player_coins = None
    player_oxygen_bottle = None
    player_room = None

    def __init__(self, game):
        self.game = game
        self.score_font = pygame.font.SysFont('Consolas', 20)

    def update(self):
        self.player_coins = self.score_font.render(str(self.game.player.coins),
            True, pygame.Color("yellow"), pygame.Color("black"))
        self.player_oxygen_bottle = self.score_font.render(str(float("{0:.2f}".format(self.game.player.oxygen_bottle))),
            True, pygame.Color("lightblue"), pygame.Color("black"))
        self.player_room = self.score_font.render("Salle : " + self.game.niveau.num_level,
            True, pygame.Color("darkorange"), pygame.Color("black"))

    def draw(self):
        self.game.window.blit(pygame.transform.scale(self.game.get_image("coin"), (30, 30)), (0, 0))
        self.game.window.blit(self.player_coins, (30, 10))

        self.game.window.blit(pygame.transform.scale(self.game.get_image("oxygen"), (30, 30)), (0, 30))
        self.game.window.blit(self.player_oxygen_bottle, (30, 40))

        if self.game.player.chaussure:
            self.game.window.blit(pygame.transform.scale(self.game.get_image("chaussure"), (30, 30)), (0, 60))

        self.game.window.blit(self.player_room, (self.game.window.get_width()/1.2, self.game.window.get_height()/20))


class Game:

    WIDTH = 1024
    HEIGHT = 768

    clock = pygame.time.Clock()

    running = 1
    state = 1
    spawn = []
    niveau = None

    def __init__(self, window, framerate):
        self.window = window
        self.framerate = framerate

        self.MARGIN_X = (window.get_width() - self.WIDTH) / 2
        self.MARGIN_Y = (window.get_height() - self.HEIGHT) / 2

        self.views = [Menu(self), Pause(self), Opts(self), Cred(self), Help(self), Gameover(self), Win(self)]
        self.last_view = None
        self.curr_view = "menu"

        self.load_assets()

    def load_assets(self):
        self.audios = {"coins": pygame.mixer.Sound('assets/audio/coins.wav'),
            "walk": pygame.mixer.Sound('assets/audio/walk.wav'),
            "oxygen_bottle": pygame.mixer.Sound('assets/audio/air_fill.wav'),
            "door": pygame.mixer.Sound('assets/audio/close_door_1.wav'),
            "button": pygame.mixer.Sound('assets/audio/button_press.wav'),
            "chaussure_propulsion": pygame.mixer.Sound('assets/audio/chaussure_propulsion.wav'),
            "chaussure": pygame.mixer.Sound('assets/audio/chaussure_lacet.wav'),
            "electric": pygame.mixer.Sound('assets/audio/electric.wav'),
            "water": pygame.mixer.Sound('assets/audio/water.wav'),
            "moving_box": pygame.mixer.Sound('assets/audio/moving_box_s.wav')}

        self.player_images = {"right_0": pygame.image.load('assets/player/right_0.png'),
            "right_1": pygame.image.load('assets/player/right_1.png'),
            "right_2": pygame.image.load('assets/player/right_2.png'),
            "right_3": pygame.image.load('assets/player/right_3.png'),
            "left_0": pygame.image.load('assets/player/left_0.png'),
            "left_1": pygame.image.load('assets/player/left_1.png'),
            "left_2": pygame.image.load('assets/player/left_2.png'),
            "left_3": pygame.image.load('assets/player/left_3.png'),
            "bottom_0": pygame.image.load('assets/player/bottom_0.png'),
            "bottom_1": pygame.image.load('assets/player/bottom_1.png'),
            "bottom_2": pygame.image.load('assets/player/bottom_2.png'),
            "bottom_3": pygame.image.load('assets/player/bottom_3.png'),
            "top_0": pygame.image.load('assets/player/top_0.png'),
            "top_1": pygame.image.load('assets/player/top_1.png'),
            "top_2": pygame.image.load('assets/player/top_2.png'),
            "top_3": pygame.image.load('assets/player/top_3.png')}

        self.images = {"wall": pygame.image.load('assets/wall.png'),
            "wind_jet": pygame.image.load('assets/wind_jet.png'), "box": pygame.image.load('assets/caisse.png'),
            "coin": pygame.image.load('assets/coin.png'), "floor": pygame.image.load('assets/floor.png'),
            "oxygen": pygame.image.load('assets/oxygen_bottle.png'),
            "red_button": pygame.image.load('assets/red_button.png'),
            "grey_button": pygame.image.load('assets/grey_button.png'),
            "porte_unlock": pygame.image.load('assets/porte_unlock.png'),
            "porte_lock": pygame.image.load('assets/porte_lock.png'),
            "dalle_electrique": pygame.image.load('assets/electric.png'),
            "chaussure": pygame.image.load('assets/flashy_boots.png'),
            "dalle_innonde": pygame.image.load('assets/floor_water.png'),
            "decor_etagere": pygame.image.load('assets/decor_etagere.png'),
            "decor_electric_pillar": pygame.image.load('assets/decor_electric_pillar.png'),
            "decor_poubelle": pygame.image.load('assets/decor_poubelle.png'),
            "decor_boite": pygame.image.load('assets/decor_boite.png'),
            "decor_four": pygame.image.load('assets/decor_four.png'),
            "event_fin": pygame.image.load('assets/computer.png'), "saas": pygame.image.load('assets/saas.png')}

    def load_levels(self):
        self.levels = {"room1": Niveau(self, "rooms/room1.txt"), "room2": Niveau(self, "rooms/room2.txt"),
                       "room3": Niveau(self, "rooms/room3.txt"), "room4": Niveau(self, "rooms/room4.txt"),
                       "room5": Niveau(self, "rooms/room5.txt"), "room6": Niveau(self, "rooms/room6.txt"),
                       "room7": Niveau(self, "rooms/room7.txt"), "room8": Niveau(self, "rooms/room8.txt"),
                       "room9": Niveau(self, "rooms/room9.txt"), "room10": Niveau(self, "rooms/room10.txt"),
                       "room11": Niveau(self, "rooms/room11.txt"), "room12": Niveau(self, "rooms/room12.txt"),
                       "room13": Niveau(self, "rooms/room13.txt"), "room14": Niveau(self, "rooms/room14.txt"),
                       "room15": Niveau(self, "rooms/room15.txt"), "room16": Niveau(self, "rooms/room16.txt")}
        self.set_lvl("room1")
        self.player = Player(self, self.spawn)
        self.score = Score(self)

    def run(self, last_view):
        if last_view == "menu":
            self.load_levels()
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
        for saas in self.niveau.all_saas:
            self.window.blit( self.get_image("saas"), (saas.rect.x, saas.rect.y) )

        self.player.draw()

        self.score.draw()

        pygame.display.flip()

    def set_lvl(self, name):
        self.niveau = self.levels.__getitem__(name)

    def get_player_image(self, direction, num):
        return self.player_images.get(direction + "_" + str(num))

    def get_image(self, name):
        if name == "player":
            image = self.get_player_image(self.player.direction, int(self.player.num_sprite / 10))
        else:
            image = self.images.__getitem__(name)
        return pygame.transform.scale(image, (self.niveau.size_x, self.niveau.size_y))

    def get_audio(self, name):
        return self.audios.__getitem__( name )

    def get_saas(self, card):
        for saas in self.niveau.all_saas:
            if saas.cardinal == card:
                return saas

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
