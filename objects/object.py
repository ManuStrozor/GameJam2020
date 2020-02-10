import pygame


class Object:

    type = None

    def __init__(self, niveau, pos):
        self.niveau = niveau
        self.surface = pygame.Surface((self.niveau.size_x, self.niveau.size_y))
        self.rect = pygame.Rect(pos[0], pos[1], self.niveau.size_x, self.niveau.size_y)

    def draw(self):
        self.niveau.game.window.blit(self.niveau.game.get_image(self.type), self.rect)

        if self.type == "player":
            if self.grabbing:
                pygame.draw.rect(self.niveau.game.window, (255, 0, 0), self.rect, 1)
            else:
                pygame.draw.rect(self.niveau.game.window, (255, 150, 150), self.rect, 1)
        elif self.type == "box":
            pygame.draw.rect(self.niveau.game.window, (255, 255, 0), self.rect, 1)
        elif self.type == "wind_jet":
            left = pygame.Rect(self.rect.x - self.rect.width, self.rect.y, self.rect.width, self.rect.height)
            right = pygame.Rect(self.rect.x + self.rect.width, self.rect.y, self.rect.width, self.rect.height)
            top = pygame.Rect(self.rect.x, self.rect.y - self.rect.height, self.rect.width, self.rect.height)
            bottom = pygame.Rect(self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height)
            pygame.draw.rect(self.niveau.game.window, (0, 255, 0), left, 1)
            pygame.draw.rect(self.niveau.game.window, (0, 255, 0), right, 1)
            pygame.draw.rect(self.niveau.game.window, (0, 255, 0), top, 1)
            pygame.draw.rect(self.niveau.game.window, (0, 255, 0), bottom, 1)


class Movable(Object):

    def __init__(self, niv, pos):
        super().__init__(niv, pos)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def way_right(self, list_of_items):
        for item in list_of_items:
            if self.rect.collidepoint(item.rect.midleft[0]-1, item.rect.midleft[1]):
                self.rect.right = item.rect.left
                return False
        return True

    def way_left(self, list_of_items):
        for item in list_of_items:
            if self.rect.collidepoint(item.rect.midright[0]+1, item.rect.midright[1]):
                self.rect.left = item.rect.right
                return False
        return True

    def way_top(self, list_of_items):
        for item in list_of_items:
            if self.rect.collidepoint(item.rect.midbottom[0], item.rect.midbottom[1]+1):
                self.rect.top = item.rect.bottom
                return False
        return True

    def way_bottom(self, list_of_items):
        for item in list_of_items:
            if self.rect.collidepoint(item.rect.midtop[0], item.rect.midtop[1]-1):
                self.rect.bottom = item.rect.top
                return False
        return True
