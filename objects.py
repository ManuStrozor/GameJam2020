from obj import Obj


class Saas(Obj):

    cardinal = None

    def __init__(self, niv, pos, cardinal):
        super().__init__(niv, pos)
        self.cardinal = cardinal
        self.type = "saas"


class Wall(Obj):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "wall"


class Caisse(Obj):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "box"

    def move(self, dx, dy, niv):
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.colliderect(niv.game.player.rect):
            if dx > 0:  # deplacement right
                if niv.game.player.way_right(niv.walls + niv.souffleurs):
                    niv.game.player.rect.right += dx
                else:
                    self.rect.x -= dx
            if dx < 0:  # deplacement left
                if niv.game.player.way_left(niv.walls + niv.souffleurs):
                    niv.game.player.rect.left += dx
                else:
                    self.rect.x -= dx
            if dy > 0:  # deplacement bottom
                if niv.game.player.way_bottom(niv.walls + niv.souffleurs):
                    niv.game.player.rect.bottom += dy
                else:
                    self.rect.y -= dy
            if dy < 0:  # deplacement top
                if niv.game.player.way_top(niv.walls + niv.souffleurs):
                    niv.game.player.rect.top += dy
                else:
                    self.rect.y -= dy

    def way_right(self, list_of_items):
        for item in list_of_items:
            if self.rect.collidepoint(item.rect.midleft[0]-1, item.rect.midleft[1]):
                self.rect.right = item.rect.left
                return False
            if self.rect.collidepoint(item.rect.topleft[0]-1, item.rect.topleft[1]):
                return False
            if self.rect.collidepoint(item.rect.bottomleft[0]-1, item.rect.bottomleft[1]-1):
                return False
        return True

    def way_left(self, list_of_items):
        for item in list_of_items:
            if self.rect.collidepoint(item.rect.midright[0]+1, item.rect.midright[1]):
                self.rect.left = item.rect.right
                return False
            if self.rect.collidepoint(item.rect.topright[0]+1, item.rect.topright[1]):
                return False
            if self.rect.collidepoint(item.rect.bottomright[0]+1, item.rect.bottomright[1]-1):
                return False
        return True

    def way_top(self, list_of_items):
        for item in list_of_items:
            if self.rect.collidepoint(item.rect.midbottom[0], item.rect.midbottom[1]+1):
                self.rect.top = item.rect.bottom
                return False
            if self.rect.collidepoint(item.rect.bottomleft[0], item.rect.bottomleft[1]+1):
                return False
            if self.rect.collidepoint(item.rect.bottomright[0]-1, item.rect.bottomright[1]):
                return False
        return True

    def way_bottom(self, list_of_items):
        for item in list_of_items:
            if self.rect.collidepoint(item.rect.midtop[0], item.rect.midtop[1]-1):
                self.rect.bottom = item.rect.top
                return False
            if self.rect.collidepoint(item.rect.topleft[0], item.rect.topleft[1]-1):
                return False
            if self.rect.collidepoint(item.rect.topright[0]-1, item.rect.topright[1]-1):
                return False
        return True


class Souffleur(Obj):

    activated = True

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "wind_jet"


class Piece(Obj):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "coin"


class Chaussure(Obj):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "chaussure"


class OxygenBottle(Obj):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "oxygen"


class Button(Obj):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "button"


class ButtonPressed(Obj):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "button_pressed"


class PorteUnlock(Obj):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "porte_unlock"


class PorteLock(Obj):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "porte_lock"


class DalleElectrique(Obj):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "dalle_electrique"


class DalleInnonde(Obj):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)
        self.type = "dalle_innonde"
