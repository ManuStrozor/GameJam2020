from views.view import View, Button

WIDTH = 512
HEIGHT = 80

class Menu(View):

    def __init__(self, game):
        super().__init__(game, "menu")
        self.state = 1
        self.set_background("assets/background.png")
        self.set_title("-= Lonely Space =-")
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250), "Commencer à jouer", "game"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 350), "Voir les crédits", "cred"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 450), "Voir l'aide", "help"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 550), "Quitter le jeu", "exit"))


class Pause(View):

    def __init__(self, game):
        super().__init__(game, "pause")
        self.set_background("assets/background.png")
        self.set_title("Pause")
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 250), "Continuer", "game"))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 350), "Sauvegarder le jeu", None))
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 550), "Menu principal", "menu"))

    def action(self):
        print("sauvegarder")


class Cred(View):

    def __init__(self, game):
        super().__init__(game, "cred")
        self.set_background("assets/background.png")
        self.set_title("Crédits")
        self.buttons.append(Button((WIDTH, HEIGHT), (game.window.get_width()/2 - WIDTH/2, 550), "Retour au menu principal", "menu"))


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
