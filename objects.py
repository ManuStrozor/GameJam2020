from obj import Obj


class Saas(Obj):

    cardinal = None

    def __init__(self, game, pos, cardinal):
        super().__init__(game, pos)
        self.cardinal = cardinal
        self.type = "saas"
        self.game.objs.append(self)
        self.game.all_saas.append(self)


class Wall(Obj):

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.type = "wall"
        self.game.objs.append(self)
        self.game.walls.append(self)


class Caisse(Obj):

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.type = "box"
        self.game.objs.append(self)
        self.game.caisses.append(self)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.colliderect(self.game.player.rect):
            if dx > 0:  # deplacement right
                if self.game.player.way_right(self.game.walls + self.game.souffleurs):
                    self.game.player.rect.right += dx
                else:
                    self.rect.x -= dx
            if dx < 0:  # deplacement left
                if self.game.player.way_left(self.game.walls + self.game.souffleurs):
                    self.game.player.rect.left += dx
                else:
                    self.rect.x -= dx
            if dy > 0:  # deplacement bottom
                if self.game.player.way_bottom(self.game.walls + self.game.souffleurs):
                    self.game.player.rect.bottom += dy
                else:
                    self.rect.y -= dy
            if dy < 0:  # deplacement top
                if self.game.player.way_top(self.game.walls + self.game.souffleurs):
                    self.game.player.rect.top += dy
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

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.type = "wind_jet"
        self.game.objs.append(self)
        self.game.souffleurs.append(self)


class Piece(Obj):

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.type = "coin"
        self.game.objs.append(self)
        self.game.pieces.append(self)


class Chaussure(Obj):

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.type = "chaussure"
        self.game.objs.append(self)
        self.game.chaussures.append(self)


class OxygenBottle(Obj):

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.type = "oxygen"
        self.game.objs.append(self)
        self.game.oxygen_bottles.append(self)


class Button(Obj):

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.type = "button"
        self.game.objs.append(self)
        self.game.buttons.append(self)


class ButtonPressed(Obj):

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.type = "button_pressed"
        self.game.objs.append(self)
        self.game.buttons_pressed.append(self)


class PorteUnlock(Obj):

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.type = "porte_unlock"
        self.game.objs.append(self)
        self.game.portes_unlock.append(self)


class PorteLock(Obj):

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.type = "porte_lock"
        self.game.objs.append(self)
        self.game.portes_lock.append(self)


class DalleElectrique(Obj):

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.type = "dalle_electrique"
        self.game.objs.append(self)
        self.game.dalles_electriques.append(self)


class DalleInnonde(Obj):

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.type = "dalle_innonde"
        self.game.objs.append(self)
        self.game.dalles_innondes.append(self)
