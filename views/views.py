import pygame

from utils import time_to_str
from views.view import View, Button

WIDTH = 300
HEIGHT = 50


class Menu(View):

    def __init__(self, game):
        super().__init__(game, "menu")
        self.state = 1
        self.set_title("Lonely Space")

        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250), "Commencer", "game"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250+90), "Options","opts"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250+90+90), "Règles du jeu", "rules"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250+90+90+70), "Crédits", "cred"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250+90+90+70+90), "Quitter le jeu", "exit"))


class Pause(View):

    def __init__(self, game):
        super().__init__(game, "pause")
        self.set_title("Pause")

        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250), "Continuer", "game"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250+90), "Options du jeu", "opts"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250+90+70), "Sauvegarder", "save"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250+90+70+90), "Menu principal", "menu"))

    def update(self):
        self.update_focus()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1\
                    and self.curr_btn.rect.collidepoint(pygame.mouse.get_pos()):
                if self.curr_btn.target == "save":
                    self.save_game()
                else:
                    self.game.goto(self.curr_btn.target)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN or e.key == pygame.K_RIGHT or e.key == pygame.K_UP or e.key == pygame.K_LEFT:
                    self.keyboard_navigation(e.key)
                elif e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    if self.curr_btn is not None:
                        if self.curr_btn.target == "save":
                            self.save_game()
                        else:
                            self.game.goto(self.curr_btn.target)
                elif e.key == pygame.K_ESCAPE:
                    self.game.goto("game")
            if e.type == pygame.QUIT:
                self.game.exit()

    def save_game(self):
        print("Sauvegarder le jeu")
        pass


class Opts(View):

    def __init__(self, game):
        super().__init__(game, "opts")
        self.set_title("Options")

        self.buttons.append(Button((HEIGHT, HEIGHT), (game.window.get_width() / 2 - HEIGHT*3, 200), "-", "volume_down"))
        self.buttons.append(Button((HEIGHT, HEIGHT), (game.window.get_width() / 2 + HEIGHT*2, 200), "+", "volume_up"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250+90+90+70+90), "Retour", None))

    def update(self):
        self.update_focus()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1\
                    and self.curr_btn.rect.collidepoint(pygame.mouse.get_pos()):
                if self.curr_btn.target is not None:
                    self.control_volume()
                else:
                    self.game.goto(self.game.last_view)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN or e.key == pygame.K_RIGHT or e.key == pygame.K_UP or e.key == pygame.K_LEFT:
                    self.keyboard_navigation(e.key)
                elif e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    if self.curr_btn is not None:
                        if self.curr_btn.target is not None:
                            self.control_volume()
                        else:
                            self.game.goto(self.game.last_view)
                elif e.key == pygame.K_ESCAPE:
                    self.game.goto(self.game.last_view)
            if e.type == pygame.QUIT:
                self.game.exit()

    def control_volume(self):
        if self.curr_btn.target == "volume_down":
            if pygame.mixer.music.get_volume() <= 0.1:
                VOLUME = 0
            else:
                VOLUME = pygame.mixer.music.get_volume() - 0.1
        elif self.curr_btn.target == "volume_up":
            VOLUME = pygame.mixer.music.get_volume() + 0.1
        pygame.mixer.music.set_volume(VOLUME)
        for key, value in self.game.audios.items():
            value.set_volume(VOLUME)

    def draw(self):
        super().draw()
        text_volume = self.normal_font.render("Volume : " + "{0:.0f}".format(pygame.mixer.music.get_volume()*100) + "%", 1, self.color)
        self.game.window.blit(text_volume, (self.game.window.get_width() / 2 - text_volume.get_rect().centerx, 215))


class Cred(View):

    def __init__(self, game):
        super().__init__(game, "cred")
        self.set_title("Réalisé par")
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250+90+90+70+90), "Retour", "menu"))

    def draw(self):
        super().draw()

        dev1 = self.normal_font.render("Lead programmeur : Emmanuel Turbet-Delof", 1, self.color)
        dev2 = self.normal_font.render("Level designer : Yann Galan", 1, self.color)
        dev3 = self.normal_font.render("Game designer : Loïc Allemand", 1, self.color)
        dev4 = self.normal_font.render("Programmeur : Yassine El Mimouni", 1, self.color)
        dev5 = self.normal_font.render("Programmeur : Loïc Chareron", 1, self.color)

        self.game.window.blit(dev1, (self.game.window.get_width() / 2 - dev1.get_rect().centerx, 250))
        self.game.window.blit(dev2, (self.game.window.get_width() / 2 - dev2.get_rect().centerx, 300))
        self.game.window.blit(dev3, (self.game.window.get_width() / 2 - dev3.get_rect().centerx, 350))
        self.game.window.blit(dev4, (self.game.window.get_width() / 2 - dev4.get_rect().centerx, 400))
        self.game.window.blit(dev5, (self.game.window.get_width() / 2 - dev5.get_rect().centerx, 450))


class Rules(View):

    def __init__(self, game):
        super().__init__(game, "rules")
        self.set_title("Comment jouer ?")
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250+90+90+70+90), "Retour", "menu"))


class Gameover(View):

    def __init__(self, game):
        super().__init__(game, "gameover")
        self.set_title("Perdu !")
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250+90+90+70+90), "Menu", "menu"))

    def update(self):
        self.update_focus()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1\
                    and self.curr_btn is not None and self.curr_btn.rect.collidepoint(pygame.mouse.get_pos()):
                self.game.goto(self.curr_btn.target)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN or e.key == pygame.K_RIGHT or e.key == pygame.K_UP or e.key == pygame.K_LEFT:
                    self.keyboard_navigation(e.key)
                elif e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    if self.curr_btn is not None:
                        self.game.goto(self.curr_btn.target)
                elif e.key == pygame.K_ESCAPE:
                    self.game.goto("menu")
            if e.type == pygame.QUIT:
                self.game.exit()


class Win(View):

    def __init__(self, game):
        super().__init__(game, "win")
        self.set_title("Vous avez gagné !")
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250+90+90+70+90), "Menu", "menu"))

    def update(self):
        self.update_focus()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1\
                    and self.curr_btn is not None and self.curr_btn.rect.collidepoint(pygame.mouse.get_pos()):
                self.game.goto(self.curr_btn.target)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN or e.key == pygame.K_RIGHT or e.key == pygame.K_UP or e.key == pygame.K_LEFT:
                    self.keyboard_navigation(e.key)
                elif e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    if self.curr_btn is not None:
                        self.game.goto(self.curr_btn.target)
                elif e.key == pygame.K_ESCAPE:
                    self.game.goto("menu")
            if e.type == pygame.QUIT:
                self.game.exit()

    def draw(self):
        super().draw()

        time = self.normal_font.render("Votre temps était : " + time_to_str(self.game.score.time), 1, self.color)
        self.game.window.blit(time, (self.game.window.get_width() / 2 - time.get_rect().centerx, 250))
