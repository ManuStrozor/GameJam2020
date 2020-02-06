import pygame


class Obj:

    type = None

    def __init__(self, game, pos):
        self.game = game
        self.grid = [int(pos[0] / self.game.niveau.size_x) - int(self.game.MARGIN_X / self.game.niveau.size_x),
                     int(pos[1] / self.game.niveau.size_y) - int(self.game.MARGIN_Y / self.game.niveau.size_y)]
        self.rect = pygame.Rect(pos[0], pos[1], self.game.niveau.size_x, self.game.niveau.size_y)
