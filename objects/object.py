import pygame


class Object:

    type = None

    def __init__(self, niveau, pos):
        self.niveau = niveau
        self.surface = pygame.Surface((self.niveau.size_x, self.niveau.size_y))
        self.rect = pygame.Rect(pos[0], pos[1], self.niveau.size_x, self.niveau.size_y)

    def draw(self):
        if self.type == "player":
            self.niveau.game.window.blit(self.niveau.game.get_image("player"), self.rect,
                (self.rect.width*self.num_sprite, self.rect.height*self.direction, self.rect.width, self.rect.height))
        else:
            self.niveau.game.window.blit(self.niveau.game.get_image(self.type), self.rect)

        # Affichage des hitboxes
        if self.type == "player":
            pygame.draw.rect(self.niveau.game.window, (255, 0, 0), self.rect, 1)
        elif self.type == "box":
            pygame.draw.rect(self.niveau.game.window, (255, 255, 0), self.rect, 1)
        elif self.type == "wind_jet":
            for jet_rect in self.jets:
                pygame.draw.rect(self.niveau.game.window, (0, 255, 0), jet_rect, 1)


class Movable(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def has_no_jet(self, dx, dy):
        for souffleur in self.game.niveau.d_objs["wind_jet"]:  # self.game.niveau car self.niveau ne change pas pour le player !!!
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
        return True

    def has_way(self, dx, dy, list_of_items):
        for souffleur in self.niveau.d_objs["wind_jet"]:
            for jet_rect in souffleur.jets:
                if self.rect == jet_rect:
                    return False
        if dx > 0:  # Deplacement right
            for item in list_of_items:
                if self.rect.collidepoint(item.rect.midleft[0] - 1, item.rect.midleft[1]):
                    self.rect.right = item.rect.left
                    return False
        elif dx < 0:  # Deplacement left
            for item in list_of_items:
                if self.rect.collidepoint(item.rect.midright[0] + 1, item.rect.midright[1]):
                    self.rect.left = item.rect.right
                    return False
        elif dy > 0:  # Deplacement bottom
            for item in list_of_items:
                if self.rect.collidepoint(item.rect.midtop[0], item.rect.midtop[1] - 1):
                    self.rect.bottom = item.rect.top
                    return False
        elif dy < 0:  # Deplacement top
            for item in list_of_items:
                if self.rect.collidepoint(item.rect.midbottom[0], item.rect.midbottom[1] + 1):
                    self.rect.top = item.rect.bottom
                    return False
        return True
