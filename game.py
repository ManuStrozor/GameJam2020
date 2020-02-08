import pygame
from pygame.locals import *
from views.views import Menu, Pause, Cred, Help, Gameover, Win
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
        self.player_coins = self.score_font.render("Coins : " + str(self.game.player.coins), True, pygame.Color("yellow"), pygame.Color("black"))
        self.player_oxygen_bottle = self.score_font.render("Bouteille d'Oxygène : "
                                                           + str(float("{0:.2f}".format(self.game.player.oxygen_bottle))),
            True, pygame.Color("lightblue"), pygame.Color("black"))
        self.player_room = self.score_font.render("Salle : " + self.game.niveau.num_level, True, pygame.Color("darkorange"), pygame.Color("black"))

        if self.game.player.chaussure is True:
            #etat_chaussure = "        Acquise"
            self.player_chaussure = self.score_font.render("Chaussures à propulsion        Acquise ", True, pygame.Color("green"), pygame.Color("black"))
        elif self.game.player.chaussure is False:
            etat_chaussure = "Non Acquise"
            self.player_chaussure = self.score_font.render("Chaussures à propulsion Non Acquise ", True, pygame.Color("red"), pygame.Color("black"))

    def draw(self):
        self.game.window.blit(self.player_coins, (5, 2))
        self.game.window.blit(self.player_oxygen_bottle, (5, 30))
        self.game.window.blit(self.player_room, (self.game.window.get_width()/1.2, self.game.window.get_height()/20))
        self.game.window.blit(self.player_chaussure, (5, 60))


class Game:

    WIDTH = 800
    HEIGHT = 600

    clock = pygame.time.Clock()

    running = 1
    state = 1
    spawn = []

    def __init__(self, window, framerate):
        self.window = window
        self.framerate = framerate

        self.MARGIN_X = (window.get_width() - self.WIDTH) / 2
        self.MARGIN_Y = (window.get_height() - self.HEIGHT) / 2

        self.views = [Menu(self), Pause(self), Cred(self), Help(self), Gameover(self), Win(self)]

        self.player_right_images = {0: pygame.image.load('assets/player/right_0.png'),
                                    1: pygame.image.load('assets/player/right_1.png'),
                                    2: pygame.image.load('assets/player/right_2.png'),
                                    3: pygame.image.load('assets/player/right_3.png')}

        self.player_left_images = {0: pygame.image.load('assets/player/left_0.png'),
                                   1: pygame.image.load('assets/player/left_1.png'),
                                   2: pygame.image.load('assets/player/left_2.png'),
                                   3: pygame.image.load('assets/player/left_3.png')}

        self.player_bottom_images = {0: pygame.image.load('assets/player/bottom_0.png'),
                                     1: pygame.image.load('assets/player/bottom_1.png'),
                                     2: pygame.image.load('assets/player/bottom_2.png'),
                                     3: pygame.image.load('assets/player/bottom_3.png')}

        self.player_top_images = {0: pygame.image.load('assets/player/top_0.png'),
                                  1: pygame.image.load('assets/player/top_1.png'),
                                  2: pygame.image.load('assets/player/top_2.png'),
                                  3: pygame.image.load('assets/player/top_3.png')}

        self.audios = {"coins": pygame.mixer.Sound('assets/audio/coins.wav'),
                       "walk": pygame.mixer.Sound('assets/audio/walk.wav'),
                       "oxygen_bottle": pygame.mixer.Sound('assets/audio/air_fill.wav'),
                       "door": pygame.mixer.Sound('assets/audio/close_door_1.wav'),
                       "button": pygame.mixer.Sound('assets/audio/button_press.wav'),
                       "chaussure_propulsion": pygame.mixer.Sound('assets/audio/chaussure_propulsion.wav'),
                       "chaussure": pygame.mixer.Sound('assets/audio/chaussure_lacet.wav'),
                       "electric": pygame.mixer.Sound('assets/audio/electric.wav'),
                       "water": pygame.mixer.Sound('assets/audio/water.wav'),
                       "moving_box": pygame.mixer.Sound('assets/audio/moving_box_s.wav'),
                       "theme": pygame.mixer.Sound('assets/audio/theme/main_theme.ogg')}

        self.images = {"wall": pygame.image.load('assets/wall.png'),
                       "wind_jet": pygame.image.load('assets/wind_jet.png'),
                       "caisse": pygame.image.load('assets/caisse.png'), "coin": pygame.image.load('assets/coin.png'),
                       "floor": pygame.image.load('assets/floor.png'),
                       "oxygen_bottle": pygame.image.load('assets/oxygen_bottle.png'),
                       "red_button": pygame.image.load('assets/red_button.png'),
                       "grey_button": pygame.image.load('assets/grey_button.png'),
                       "porte_unlock": pygame.image.load('assets/porte_unlock.png'),
                       "porte_lock": pygame.image.load('assets/porte_lock.png'),
                       "electric": pygame.image.load('assets/electric.png'),
                       "flashy_boots": pygame.image.load('assets/flashy_boots.png'),
                       "floor_water": pygame.image.load('assets/floor_water.png'),
                       "decor_etagere": pygame.image.load('assets/decor_etagere.png'),
                       "decor_electric_pillar": pygame.image.load('assets/decor_electric_pillar.png'),
                       "decor_poubelle": pygame.image.load('assets/decor_poubelle.png'),
                       "decor_boite": pygame.image.load('assets/decor_boite.png'),
                       "decor_four": pygame.image.load('assets/decor_four.png'),
                       "event_fin": pygame.image.load('assets/computer.png'),
                       "saas": pygame.image.load('assets/saas.png')}

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
            self.set_lvl("room1")
            self.player = Player(self, self.spawn)
            self.score = Score(self)
        self.state = 1
        while self.state:
            self.update()
            self.draw()

    def update(self):

        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                self.goto("pause")
            if e.type == QUIT:
                self.exit()

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
            image = None
            if obj.type == "wall":
                image = self.get_image( "wall" )
            elif obj.type == "wind_jet":
                image = self.get_image( "wind_jet" )
            elif obj.type == "box":
                image = self.get_image( "caisse" )
            elif obj.type == "coin":
                image = self.get_image( "coin" )
            elif obj.type == "oxygen":
                image = self.get_image( "oxygen_bottle" )
            elif obj.type == "button":
                image = self.get_image( "red_button" )
            elif obj.type == "button_pressed":
                image = self.get_image( "grey_button" )
            elif obj.type == "porte_lock":
                image = self.get_image( "porte_lock" )
            elif obj.type == "porte_unlock":
                image = self.get_image( "porte_unlock" )
            elif obj.type == "dalle_electrique":
                image = self.get_image( "electric" )
            elif obj.type == "chaussure":
                image = self.get_image( "flashy_boots" )
            elif obj.type == "saas":
                image = self.get_image( "saas" )
            elif obj.type == "dalle_innonde":
                image = self.get_image( "floor_water" )
            elif obj.type == "event_fin":
                image = self.get_image( "event_fin" )

            if image is not None:
                self.window.blit( image, (obj.rect.x, obj.rect.y) )

        # Affichage des saas
        for saas in self.niveau.all_saas:
            self.window.blit( self.get_image("saas"), (saas.rect.x, saas.rect.y) )

        self.player.draw()

        self.score.draw()

        pygame.display.flip()

    def set_lvl(self, name):
        self.niveau = self.levels.__getitem__(name)

    def get_player_image(self, direction, num):
        image = None
        if direction == 0:
            image = self.player_bottom_images.get(num)
        elif direction == 1:
            image = self.player_right_images.get(num)
        elif direction == 2:
            image = self.player_top_images.get(num)
        elif direction == 3:
            image = self.player_left_images.get(num)
        return pygame.transform.scale(image, (self.niveau.size_x, self.niveau.size_y))

    def get_image(self, name):
        return pygame.transform.scale( self.images.__getitem__( name ), (self.niveau.size_x, self.niveau.size_y) )

    def get_audio(self, name):
        return self.audios.__getitem__( name )

    def get_saas(self, card):
        for saas in self.niveau.all_saas:
            if saas.cardinal == card:
                return saas

    def goto(self, name):
        if name != "game":
            self.state = 0
        for view in self.views:
            if view.name == name:
                view.state = 1
            else:
                view.state = 0

    def exit(self):
        self.running = 0
        self.state = 0
        for view in self.views:
            view.state = 0
