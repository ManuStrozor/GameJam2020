import pygame


class Object:

    type = None

    def __init__(self, niveau, pos):
        self.rect = pygame.Rect(pos[0], pos[1], niveau.size_x, niveau.size_y)
