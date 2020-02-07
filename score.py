import pygame


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
