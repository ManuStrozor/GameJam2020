import pygame

from room import Room


class Map:

    surface = None
    pos_x = 50
    pos_y = 50
    origin = (pos_x, pos_y)
    visible = False
    rooms = [
        [1, 1, 1, 0, 0, 0],
        [0, 1, 2, 1, 1, 0],
        [0, 0, 3, 2, 1, 1],
        [0, 1, 2, 1, 1, 0],
        [1, 1, 1, 0, 0, 0],
    ]
    all_rooms = pygame.sprite.Group()
    room_width = 92
    room_height = 66
    room_size = (room_width, room_height)

    def __init__(self, game):
        self.game = game

        self.surface = pygame.Surface((924, 668))
        self.surface.set_alpha(190)
        self.surface.fill((0, 0, 0))

        for y in range(0, len(self.rooms)):
            for x in range(0, len(self.rooms[y])):
                if self.rooms[y][x] != 0:
                    room = Room(self, self.room_width * x + self.pos_x, self.room_height * y + self.pos_y)
                    if self.rooms[y][x] == 1:
                        room.name = "room"
                    else:
                        room.visited = True
                        if self.rooms[y][x] == 3:
                            room.current = True
                    self.all_rooms.add(room)

    def update(self):
        self.visible = self.game.keyPressed.get(pygame.K_TAB)


    def draw(self):
        if self.visible:
            self.game.window.blit(self.surface, self.origin)
            for room in self.all_rooms:
                room.draw()







