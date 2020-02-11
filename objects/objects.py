import pygame
from objects.object import Object, Movable


# Non interactifs


#       Solides


class Wall(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "wall"


class EventFin(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "event_fin"


# Interactifs


#       Solides


class Caisse(Movable):

    def __init__(self, niveau, pos):
        super().__init__(niveau, pos)
        self.type = "box"

    def move(self, dx, dy):
        super().move(dx, dy)

        if self.rect.colliderect(self.niveau.game.player.rect):
            if dx > 0:  # deplacement right
                if self.niveau.game.player.has_way(dx, dy, self.niveau.walls + self.niveau.souffleurs):
                    self.niveau.game.player.rect.right += dx
                else:
                    self.rect.x -= dx
            if dx < 0:  # deplacement left
                if self.niveau.game.player.has_way(dx, dy, self.niveau.walls + self.niveau.souffleurs):
                    self.niveau.game.player.rect.left += dx
                else:
                    self.rect.x -= dx
            if dy > 0:  # deplacement bottom
                if self.niveau.game.player.has_way(dx, dy, self.niveau.walls + self.niveau.souffleurs):
                    self.niveau.game.player.rect.bottom += dy
                else:
                    self.rect.y -= dy
            if dy < 0:  # deplacement top
                if self.niveau.game.player.has_way(dx, dy, self.niveau.walls + self.niveau.souffleurs):
                    self.niveau.game.player.rect.top += dy
                else:
                    self.rect.y -= dy


class Souffleur(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "wind_jet"

        self.jets = [
            pygame.Rect(self.rect.x - self.rect.width, self.rect.y, self.rect.width, self.rect.height),
            pygame.Rect(self.rect.x + self.rect.width, self.rect.y, self.rect.width, self.rect.height),
            pygame.Rect(self.rect.x, self.rect.y - self.rect.height, self.rect.width, self.rect.height),
            pygame.Rect(self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height)
        ]


#       Sols


class DalleElectrique(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "dalle_electrique"


class DalleInnonde(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "dalle_innonde"


#       Objets


class Piece(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "coin"


class Chaussure(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "chaussure"


class OxygenBottle(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "oxygen"


#       Divers


class Saas(Object):

    cardinal = None

    def __init__(self, niv, pos, cardinal):
        super().__init__(niv, pos)
        self.cardinal = cardinal
        self.type = "saas"


class Button(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "button"

    def press(self):
        self.type = "button_pressed"
        self.niveau.d_objs["button"].remove(self)
        self.niveau.d_objs["button_pressed"].append(self)


class Porte(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "porte"

    def lock(self):
        self.type = "porte_lock"
        self.niveau.d_objs["porte"].remove(self)
        self.niveau.d_objs["porte_lock"].append(self)

    def unlock(self):
        self.type = "porte"
        self.niveau.d_objs["porte_lock"].remove(self)
        self.niveau.d_objs["porte"].append(self)
