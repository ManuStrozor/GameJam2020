import pygame


class Object:

    type = None

    def __init__(self, niveau, pos):
        self.niveau = niveau
        self.surface = pygame.Surface((self.niveau.size_x, self.niveau.size_y))
        self.rect = pygame.Rect(pos[0], pos[1], self.niveau.size_x, self.niveau.size_y)

    def draw(self):
        if self.type == "player" or self.type == "wind_jet":
            self.niveau.game.blit_tile(self)
        else:
            self.niveau.game.window.blit(self.niveau.game.get_image(self.type), self.rect)

        # Affichage des hitboxes
        # if self.type == "player":
        #     pygame.draw.rect(self.niveau.game.window, (255, 0, 0), self.rect, 1)
        # elif self.type == "box":
        #     pygame.draw.rect(self.niveau.game.window, (255, 255, 0), self.rect, 1)
        # elif self.type == "wind_jet":
        #     for jet_rect in self.jets:
        #         pygame.draw.rect(self.niveau.game.window, (0, 255, 0), jet_rect, 1)


class Movable(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def has_no_obstacles(self, dx, dy):
        for souffleur in self.game.niveau.d_objs["wind_jet"]:  # self.niveau.num_level reste à 1 pour le player !!!
            for jet_rect in souffleur.jets:
                if self.rect.colliderect(jet_rect):
                    if dx > 0:  # Deplacement right
                        self.rect.right = jet_rect.left
                        return False
                    elif dx < 0:  # Deplacement left
                        self.rect.left = jet_rect.right
                        return False
                    elif dy > 0:  # Deplacement bottom
                        self.rect.bottom = jet_rect.top
                        return False
                    elif dy < 0:  # Deplacement top
                        self.rect.top = jet_rect.bottom
                        return False

        # Ca marche pas tout les temps !!! A corriger !!!
        # idée : utiliser la position relative a la map pour repérer les caisses autour du player ???
        for caisse in self.game.niveau.d_objs["box"]:
            if self.rect.colliderect(caisse.rect):
                if dx > 0:  # Deplacement right
                    self.rect.right = caisse.rect.left
                    return False
                elif dx < 0:  # Deplacement left
                    self.rect.left = caisse.rect.right
                    return False
                elif dy > 0:  # Deplacement bottom
                    self.rect.bottom = caisse.rect.top
                    return False
                elif dy < 0:  # Deplacement top
                    self.rect.top = caisse.rect.bottom
                    return False
        return True

    def has_way(self, dx, dy, list_of_items):
        for souffleur in self.niveau.d_objs["wind_jet"]:
            for jet_rect in souffleur.jets:
                if self.rect == jet_rect:
                    return False
        for item in list_of_items:
            if dx > 0:  # Deplacement right
                if self.rect.collidepoint(item.rect.midleft[0] - 1, item.rect.midleft[1]):
                    self.rect.right = item.rect.left
                    return False
            elif dx < 0:  # Deplacement left
                if self.rect.collidepoint(item.rect.midright[0] + 1, item.rect.midright[1]):
                    self.rect.left = item.rect.right
                    return False
            elif dy > 0:  # Deplacement bottom
                if self.rect.collidepoint(item.rect.midtop[0], item.rect.midtop[1] - 1):
                    self.rect.bottom = item.rect.top
                    return False
            elif dy < 0:  # Deplacement top
                if self.rect.collidepoint(item.rect.midbottom[0], item.rect.midbottom[1] + 1):
                    self.rect.top = item.rect.bottom
                    return False
        return True
