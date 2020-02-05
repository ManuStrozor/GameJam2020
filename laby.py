import pygame


class Player:

    grid_x = None
    grid_y = None
    speed = 2
    coins = 0

    def __init__(self, pos):
        self.grid_x = int(pos[0]/SIZE_X)
        self.grid_y = int(pos[1]/SIZE_Y)
        self.rect = pygame.Rect(pos[0], pos[1], SIZE_X, SIZE_Y)

    def move(self, dx, dy):
        audio_walk.set_volume(0.05)
        audio_walk.play()
        self.rect.x += dx
        self.rect.y += dy

        bloks = walls + caisses + souffleurs + pieces

        # Collision mur
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # deplacement right
                    self.rect.right = wall.rect.left
                if dx < 0:  # deplacement left
                    self.rect.left = wall.rect.right
                if dy > 0:  # deplacement bottom
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # deplacement top
                    self.rect.top = wall.rect.bottom

        # Collision caisse (Pousser et Tirer)
        for caisse in caisses:
            if self.rect.colliderect(caisse.rect):  # Pousser la caisse quand on se dirige vers elle
                if dx > 0:  # deplacement right
                    if caisse.way_right(bloks):
                        caisse.rect.right += dx
                    else:
                        self.rect.x -= dx
                if dx < 0:  # deplacement left
                    if caisse.way_left(bloks):
                        caisse.rect.left += dx
                    else:
                        self.rect.x -= dx
                if dy > 0:  # deplacement bottom
                    if caisse.way_bottom(bloks):
                        caisse.rect.bottom += dy
                    else:
                        self.rect.y -= dy
                if dy < 0:  # deplacement top
                    if caisse.way_top(bloks):
                        caisse.rect.top += dy
                    else:
                        self.rect.y -= dy
            if pygame.key.get_pressed()[pygame.K_LCTRL]:  # Tirer la caisse quand la touche (Ctrl gauche) est appuyé
                tmp = caisse.rect
                if dx > 0:  # deplacement right
                    if caisse.way_right(bloks) and self.rect.collidepoint(tmp.x + dx + tmp.width, tmp.y + int(tmp.height/2))\
                            or self.rect.collidepoint(tmp.x + dx - 1, tmp.y + int(tmp.height/2)):
                        caisse.rect.right = self.rect.left
                if dx < 0:  # deplacement left
                    if caisse.way_left(bloks) and self.rect.collidepoint(tmp.x + dx - 1, tmp.y + int(tmp.height/2))\
                            or self.rect.collidepoint(tmp.x + dx + tmp.width, tmp.y + int(tmp.height/2)):
                        caisse.rect.left = self.rect.right
                if dy > 0:  # deplacement bottom
                    if caisse.way_bottom(bloks) and self.rect.collidepoint(tmp.x + int(tmp.width / 2), tmp.y + dy + tmp.height)\
                            or self.rect.collidepoint(tmp.x + int(tmp.width / 2), tmp.y + dy - 1):
                        caisse.rect.bottom = self.rect.top
                if dy < 0:  # deplacement top
                    if caisse.way_top(bloks) and self.rect.collidepoint(tmp.x + int(tmp.width / 2), tmp.y + dy - 1)\
                            or self.rect.collidepoint(tmp.x + int(tmp.width / 2), tmp.y + dy + tmp.height):
                        caisse.rect.top = self.rect.bottom

        # Interaction souffleur
        for souffleur in souffleurs:
            for caisse in caisses:
                tmp = souffleur.rect

                souf_right = pygame.Rect(tmp.x + tmp.width, tmp.y, tmp.width, tmp.height)
                if souf_right.colliderect(caisse.rect):
                    caisse.move(self.speed * 3, 0)
                if souf_right.colliderect(self.rect):
                    self.rect.x += self.speed*3

                souf_left = pygame.Rect(tmp.x - tmp.width, tmp.y, tmp.width, tmp.height)
                if souf_left.colliderect(caisse.rect):
                    caisse.move(-self.speed * 3, 0)
                if souf_left.colliderect(self.rect):
                    self.rect.x -= self.speed*3

                souf_bottom = pygame.Rect(tmp.x, tmp.y + tmp.height, tmp.width, tmp.height)
                if souf_bottom.colliderect(caisse.rect):
                    caisse.move(0, self.speed*3)
                if souf_bottom.colliderect(self.rect):
                    self.rect.y += self.speed*3

                souf_top = pygame.Rect(tmp.x, tmp.y - tmp.height, tmp.width, tmp.height)
                if souf_top.colliderect(caisse.rect):
                    caisse.move(0, -self.speed*3)
                if souf_top.colliderect(self.rect):
                    self.rect.y -= self.speed*3

        # Collision piece (coins)
        for piece in pieces:
            if self.rect.colliderect(piece.rect):
                self.coins += 1
                pieces.remove(piece)
                get_obj(piece.grid[0], piece.grid[1]).type = None
                pygame.mixer.stop()
                audio_coins.set_volume(3)
                audio_coins.play()

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


class Obj:

    type = None

    def __init__(self, pos):
        self.grid = [int(pos[0] / SIZE_X) - int(MARGIN_X / SIZE_X), int(pos[1] / SIZE_Y) - int(MARGIN_Y / SIZE_Y)]
        self.rect = pygame.Rect(pos[0], pos[1], SIZE_X, SIZE_Y)


class Wall(Obj):

    def __init__(self, pos):
        super().__init__(pos)
        self.type = "wall"
        objs.append(self)
        walls.append(self)


class Caisse(Obj):

    def __init__(self, pos):
        super().__init__(pos)
        self.type = "box"
        objs.append(self)
        caisses.append(self)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.colliderect(player.rect):
            if dx > 0:  # deplacement right
                if player.way_right(walls + souffleurs):
                    player.rect.right += dx
                else:
                    self.rect.x -= dx
            if dx < 0:  # deplacement left
                if player.way_left(walls + souffleurs):
                    player.rect.left += dx
                else:
                    self.rect.x -= dx
            if dy > 0:  # deplacement bottom
                if player.way_bottom(walls + souffleurs):
                    player.rect.bottom += dy
                else:
                    self.rect.y -= dy
            if dy < 0:  # deplacement top
                if player.way_top(walls + souffleurs):
                    player.rect.top += dy
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

    def __init__(self, pos):
        super().__init__(pos)
        self.type = "wind_jet"
        objs.append(self)
        souffleurs.append(self)


class Piece(Obj):

    def __init__(self, pos):
        super().__init__(pos)
        self.type = "coin"
        objs.append(self)
        pieces.append(self)


def get_type(x, y):
    index = (y * len(level[0])) + x
    if index < 0 or index >= len(level[0])*len(level):
        return None
    return objs.__getitem__(index).type


def get_obj(x, y):
    return objs.__getitem__(y * len(level[0]) + x)


pygame.init()

pygame.display.set_caption("Sortez par une porte rouge!")
screen = pygame.display.set_mode((1024, 768))

clock = pygame.time.Clock()

audio_coins = pygame.mixer.Sound('assets/audio/coins.wav')  # Son de pieces
audio_walk = pygame.mixer.Sound('assets/audio/walk.wav')  # son de pas (clap, clap)

MARGIN_X = (screen.get_width() - 640) / 2
MARGIN_Y = (screen.get_height() - 480) / 2

objs = []  # Liste de tous les blocs
walls = []  # Liste des murs
caisses = []  # Liste des caisses
souffleurs = []  # Liste des souffleurs
pieces = []  # Liste des pieces (coins)
player = None

# Contenu de la map dans un string
level = [
    "wwwwwwwwwSwwwwwwwwww",
    "w W     W          B",
    "w     C   WWWWWW   w",
    "w X WWWW       W   w",
    "w   W        WWWW  w",
    "w WWW  WWWW        w",
    "w   W     W W      w",
    "w   W  P  W   WWW Ww",
    "w  CWWW WWW   WPW  w",
    "w     W   WW  WCW  w",
    "wWW   W   WWWWW W  w",
    "wPW      WW        S",
    "w W   WWWW   WW    w",
    "w     W       W    E",
    "wwwwwwwwwwwwwwwwwwww",
]

SIZE_X = int(640 / len(level[0]))
SIZE_Y = int(480 / len(level))

# pour chaque caracteres du string : W = mur, E = porte du bas, B = porte du haut
y = MARGIN_Y
for row in level:
    x = MARGIN_X
    for col in row:
        if col == "W" or col == "w":
            Wall((x, y))
        elif col == "E":
            porte1 = pygame.Rect(x, y, SIZE_X, SIZE_Y)
            objs.append(Obj((x, y)))
        elif col == "B":
            porte2 = pygame.Rect(x, y, SIZE_X, SIZE_Y)
            objs.append(Obj((x, y)))
        elif col == "C":
            Caisse((x, y))
        elif col == "S":
            Souffleur((x, y))
        elif col == "P":
            Piece((x, y))
        elif col == "X":
            player = Player((x, y))  # Creation joueur ('X' sur la grille)
            objs.append(Obj((x, y)))
        else:
            objs.append(Obj((x, y)))
        x += SIZE_X
    y += SIZE_Y

if player is None:
    player = Player((64, 96))  # Creation joueur si rien sur la grille

wall_image = pygame.transform.scale(pygame.image.load('assets/wall.png'), (SIZE_X, SIZE_Y))
wind_image = pygame.transform.scale(pygame.image.load('assets/wind_jet.png'), (SIZE_X, SIZE_Y))
box_image = pygame.transform.scale(pygame.image.load('assets/box.png'), (SIZE_X, SIZE_Y))
coin_image = pygame.transform.scale(pygame.image.load('assets/coin.png'), (SIZE_X, SIZE_Y))
floor_image = pygame.transform.scale(pygame.image.load('assets/floor.png'), (SIZE_X, SIZE_Y))
room_image = pygame.transform.scale(pygame.image.load('assets/room.png'), (SIZE_X, SIZE_Y))

running = True
while running:

    clock.tick(120)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    # deplacement joueur
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-player.speed, 0)
    if key[pygame.K_RIGHT]:
        player.move(player.speed, 0)
    if key[pygame.K_UP]:
        player.move(0, -player.speed)
    if key[pygame.K_DOWN]:
        player.move(0, player.speed)

    # conditions fin
    if player.rect.colliderect(porte1):
        print("sortie porte 1")
        raise SystemExit # à modif, appel nouvelle fenetre de jeu
    if player.rect.colliderect(porte2):
        print("sortie porte 2")
        raise SystemExit # à modif, appel nouvelle fenetre de jeu

    # Draw
    screen.fill((0, 0, 0))
    for obj in objs:
        if get_type(obj.grid[0], obj.grid[1]) == "wall":
            image = wall_image
        if get_type(obj.grid[0], obj.grid[1]) == "wind_jet":
            image = wind_image
        if get_type(obj.grid[0], obj.grid[1]) is None or get_type(obj.grid[0], obj.grid[1]) == "coin" or get_type(obj.grid[0], obj.grid[1]) == "box":
            image = floor_image
        screen.blit(image, (obj.rect.x, obj.rect.y))
        if get_type(obj.grid[0], obj.grid[1]) == "coin":
            image = coin_image
        screen.blit(image, (obj.rect.x, obj.rect.y))
        if get_type(obj.grid[0], obj.grid[1]) == "box":
            image = box_image
        screen.blit(image, (obj.rect.x, obj.rect.y))

    #for wall in walls:
        #pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    #for caisse in caisses:
        #pygame.draw.rect(screen, (255, 0, 255), caisse.rect)
    #for souffleur in souffleurs:
        #pygame.draw.rect(screen, (0, 0, 255), souffleur.rect)
    #for piece in pieces:
        #pygame.draw.rect(screen, (0, 255, 0), piece.rect)

    pygame.draw.rect(screen, (255, 0, 0), porte1)
    pygame.draw.rect(screen, (255, 0, 0), porte2)
    pygame.draw.rect(screen, (255, 255, 0), player.rect)

    pygame.display.flip()
