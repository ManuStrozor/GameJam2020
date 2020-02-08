from objects.object import Object, Movable


class Caisse(Movable):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "box"

    def move(self, dx, dy):
        super().move(dx, dy)

        if self.rect.colliderect(self.niveau.game.player.rect):
            if dx > 0:  # deplacement right
                if self.niveau.game.player.way_right(self.niveau.walls + self.niveau.souffleurs):
                    self.niveau.game.player.rect.right += dx
                else:
                    self.rect.x -= dx
            if dx < 0:  # deplacement left
                if self.niveau.game.player.way_left(self.niveau.walls + self.niveau.souffleurs):
                    self.niveau.game.player.rect.left += dx
                else:
                    self.rect.x -= dx
            if dy > 0:  # deplacement bottom
                if self.niveau.game.player.way_bottom(self.niveau.walls + self.niveau.souffleurs):
                    self.niveau.game.player.rect.bottom += dy
                else:
                    self.rect.y -= dy
            if dy < 0:  # deplacement top
                if self.niveau.game.player.way_top(self.niveau.walls + self.niveau.souffleurs):
                    self.niveau.game.player.rect.top += dy
                else:
                    self.rect.y -= dy


class Saas(Object):

    cardinal = None

    def __init__(self, niv, pos, cardinal):
        super().__init__(niv, pos)
        self.cardinal = cardinal
        self.type = "saas"


class Wall(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "wall"


class Souffleur(Object):

    activated = True

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "wind_jet"


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


class Button(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "button"


class ButtonPressed(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "button_pressed"


class PorteUnlock(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "porte_unlock"


class PorteLock(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "porte_lock"


class DalleElectrique(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "dalle_electrique"


class DalleInnonde(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "dalle_innonde"


class EventFin(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "event_fin"
