import pygame

from views.view import View, Button

WIDTH = 512
HEIGHT = 80


class Menu(View):

    def __init__(self, game):
        super().__init__(game, "menu")
        self.state = 1
        self.set_background("assets/background.png")
        self.set_title("-= Lonely Space =-")
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 200), "Commencer à jouer", "game"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 300), "Options du jeu", "opts"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 400), "Voir les crédits", "cred"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 500), "Voir l'aide", "help"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 600), "Quitter le jeu", "exit"))


class Pause(View):

    def __init__(self, game):
        super().__init__(game, "pause")
        self.set_background("assets/background.png")
        self.set_title("Pause")
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 200), "Continuer", "game"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 300), "Sauvegarder le jeu", "save"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 400), "Options du jeu", "opts"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 500), "Menu principal", "menu"))

    def update(self):
        self.update_focus()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1\
                    and self.curr_btn.rect.collidepoint(pygame.mouse.get_pos()):
                if self.curr_btn.target == "save":
                    print("Sauvegarder le jeu")
                else:
                    self.game.goto(self.curr_btn.target)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN or e.key == pygame.K_RIGHT or e.key == pygame.K_UP or e.key == pygame.K_LEFT:
                    self.keyboard_navigation(e.key)
                elif e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    if self.curr_btn is not None:
                        if self.curr_btn.target == "save":
                            print("Sauvegarder le jeu")
                        else:
                            self.game.goto(self.curr_btn.target)
                elif e.key == pygame.K_ESCAPE:
                    self.game.goto(self.game.last_view)
            if e.type == pygame.QUIT:
                self.game.exit()


class Opts(View):

    def __init__(self, game):
        super().__init__(game, "opts")
        self.set_background("assets/background.png")
        self.set_title("Options")
        self.buttons.append(Button((HEIGHT, HEIGHT), (game.window.get_width() / 2 - HEIGHT*2, 200), "-", "volume_down"))
        self.buttons.append(Button((HEIGHT, HEIGHT), (game.window.get_width() / 2 + HEIGHT, 200), "+", "volume_up"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width() / 2 - WIDTH / 2, 500), "Retour", None))

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
            VOLUME = pygame.mixer.music.get_volume() - 0.1
        elif self.curr_btn.target == "volume_up":
            VOLUME = pygame.mixer.music.get_volume() + 0.1
        pygame.mixer.music.set_volume(VOLUME)
        for key, value in self.game.audios.items():
            value.set_volume(VOLUME)

    def draw(self):
        super().draw()
        text_volume = self.normal_font.render(str(float("{0:.2f}".format(pygame.mixer.music.get_volume()*100))) + " %", 1, self.color)
        self.game.window.blit(text_volume, (self.game.window.get_width() / 2 - text_volume.get_rect().centerx, 230))


class Cred(View):

    def __init__(self, game):
        super().__init__(game, "cred")
        self.set_background("assets/background.png")
        self.set_title("Crédits")
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 500), "Retour au menu principal", "menu"))


class Help(View):

    def __init__(self, game):
        super().__init__(game, "help")
        self.set_background("assets/help.png")
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 400), "Retour au menu principal", "menu"))


class Gameover(View):

    def __init__(self, game):
        super().__init__(game, "gameover")
        self.set_background("assets/game_lost.png")
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 400), "Retour au menu principal", "menu"))


class Win(View):

    def __init__(self, game):
        super().__init__(game, "win")
        self.set_background("assets/game_win.png")
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 400), "Retour au menu principal", "menu"))
