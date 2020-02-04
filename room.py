import pygame


class Room(pygame.sprite.Sprite):

    surface = None
    name = None
    pos_x = None
    pos_y = None
    visited = False
    current = False
    doors = [
        {"cardinal": "north", "visible": False, "locked": True},
        {"cardinal": "south", "visible": False, "locked": True},
        {"cardinal": "west",  "visible": False, "locked": True},
        {"cardinal": "east",  "visible": False, "locked": True}
    ]

    def __init__(self, map, x, y):
        super().__init__()
        self.map = map

        self.pos_x = x
        self.pos_y = y

        self.surface = pygame.Surface(self.map.room_size)
        self.surface.set_alpha(200)
        self.surface.fill((200, 200, 200))

    def draw(self):
        if self.visited:
            if self.current:
                self.surface.set_alpha(255)
                self.surface.fill((255, 255, 255))
            self.map.game.window.blit(self.surface, (self.pos_x, self.pos_y))

    def set_door(self, card, attr, val):
        for i in range(0, len(self.doors)):
            if self.doors[i].__getattribute__("cardinal") == card:
                self.doors[i].__setattr__(attr, val)
