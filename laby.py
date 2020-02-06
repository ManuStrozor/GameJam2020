import pygame


class Player:

    grid_x = None
    grid_y = None
    speed = 2
    coins = 0
    oxygen_bottle = 0
    chaussure = False

    def __init__(self, pos):
        self.grid_x = int(pos[0]/niveau.size_x)
        self.grid_y = int(pos[1]/niveau.size_y)
        self.rect = pygame.Rect(pos[0], pos[1], niveau.size_x, niveau.size_y)

    def move(self, dx, dy):
        audio_walk.set_volume(0.05)
        audio_walk.play()
        self.rect.x += dx
        self.rect.y += dy

        bloks = walls + caisses + souffleurs + pieces + portes_lock + portes_unlock

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

        # Collision porte verrouillée
        for porte_lock in portes_lock:
            if self.rect.colliderect(porte_lock.rect):
                if dx > 0:  # deplacement right
                    self.rect.right = porte_lock.rect.left
                if dx < 0:  # deplacement left
                    self.rect.left = porte_lock.rect.right
                if dy > 0:  # deplacement bottom
                    self.rect.bottom = porte_lock.rect.top
                if dy < 0:  # deplacement top
                    self.rect.top = porte_lock.rect.bottom

        # Collision dalle electrique SANS chaussures à propulsion
        for dalle_electrique in dalles_electriques:
            if self.rect.colliderect(dalle_electrique.rect) and self.chaussure is not True:
                pygame.mixer.stop()
                audio_electric.set_volume(1)
                audio_electric.play()
                if dx > 0:  # deplacement right
                    self.rect.right = dalle_electrique.rect.left
                if dx < 0:  # deplacement left
                    self.rect.left = dalle_electrique.rect.right
                if dy > 0:  # deplacement bottom
                    self.rect.bottom = dalle_electrique.rect.top
                if dy < 0:  # deplacement top
                    self.rect.top = dalle_electrique.rect.bottom
            # Collision dalle electrique SANS chaussures à propulsion
            if self.rect.colliderect(dalle_electrique.rect) and self.chaussure is True:
                pygame.mixer.stop()
                audio_chaussure_propulsion.set_volume(1)
                audio_chaussure_propulsion.play()

        # Collision porte déverrouillée
        for porte_unlock in portes_unlock:
            if self.rect.colliderect(porte_unlock.rect):
                pygame.mixer.stop()
                audio_door.set_volume(3)
                audio_door.play()

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
                            or self.rect.collidepoint(tmp.x + dx - self.speed, tmp.y + int(tmp.height/2)):
                        caisse.rect.right = self.rect.left
                if dx < 0:  # deplacement left
                    if caisse.way_left(bloks) and self.rect.collidepoint(tmp.x + dx - self.speed, tmp.y + int(tmp.height/2))\
                            or self.rect.collidepoint(tmp.x + dx + tmp.width, tmp.y + int(tmp.height/2)):
                        caisse.rect.left = self.rect.right
                if dy > 0:  # deplacement bottom
                    if caisse.way_bottom(bloks) and self.rect.collidepoint(tmp.x + int(tmp.width / 2), tmp.y + dy + tmp.height)\
                            or self.rect.collidepoint(tmp.x + int(tmp.width / 2), tmp.y + dy - self.speed):
                        caisse.rect.bottom = self.rect.top
                if dy < 0:  # deplacement top
                    if caisse.way_top(bloks) and self.rect.collidepoint(tmp.x + int(tmp.width / 2), tmp.y + dy - self.speed)\
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

        # Collision oxygen_bottle
        for oxygen_bottle in oxygen_bottles:
            if self.rect.colliderect(oxygen_bottle.rect):
                self.oxygen_bottle += 1
                oxygen_bottles.remove(oxygen_bottle)
                get_obj(oxygen_bottle.grid[0], oxygen_bottle.grid[1]).type = None
                pygame.mixer.stop()
                audio_oxygen_bottle.set_volume(3)
                audio_oxygen_bottle.play()

        # Collision chaussure
        for chaussure in chaussures:
            if self.rect.colliderect(chaussure.rect):
                self.chaussure = True
                chaussures.remove(chaussure)
                get_obj(chaussure.grid[0], chaussure.grid[1]).type = None
                print("chaussure récup")
                pygame.mixer.stop()
                audio_chaussure_recup.set_volume(1)
                audio_chaussure_recup.play()

        # Collision button
        for button in buttons:
            if self.rect.colliderect(button.rect):
                buttons.remove(button)
                get_obj(button.grid[0], button.grid[1]).type = "button_pressed"
                pygame.mixer.stop()
                audio_button.set_volume(3)
                audio_button.play()
                print("appui boutton")

                # changer l'etat de la porte verouillé en deverouillé
                for porte_lock in portes_lock:
                    portes_lock.remove(porte_lock)
                    get_obj(porte_lock.grid[0], porte_lock.grid[1]).type = "porte_unlock"


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
        self.grid = [int(pos[0] / niveau.size_x) - int(MARGIN_X / niveau.size_x), int(pos[1] / niveau.size_y) - int(MARGIN_Y / niveau.size_y)]
        self.rect = pygame.Rect(pos[0], pos[1], niveau.size_x, niveau.size_y)


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


class Chaussure(Obj):

    def __init__(self, pos):
        super().__init__(pos)
        self.type = "chaussure"
        objs.append(self)
        chaussures.append(self)


class Oxygen_bottle(Obj):

    def __init__(self, pos):
        super().__init__(pos)
        self.type = "oxygen"
        objs.append(self)
        oxygen_bottles.append(self)


class Button(Obj):

    def __init__(self, pos):
        super().__init__(pos)
        self.type = "button"
        objs.append(self)
        buttons.append(self)


class ButtonPressed(Obj):

    def __init__(self, pos):
        super().__init__(pos)
        self.type = "button_pressed"
        objs.append(self)
        buttons_pressed.append(self)


class PorteUnlock(Obj):

    def __init__(self, pos):
        super().__init__(pos)
        self.type = "porte_unlock"
        objs.append(self)
        portes_unlock.append(self)


class PorteLock(Obj):

    def __init__(self, pos):
        super().__init__(pos)
        self.type = "porte_lock"
        objs.append(self)
        portes_lock.append(self)


class DalleElectrique(Obj):

    def __init__(self, pos):
        super().__init__(pos)
        self.type = "dalle_electrique"
        objs.append(self)
        dalles_electriques.append(self)

class Score:

    player_coins = None
    player_oxygen_bottle = None
    player_room = None

    def __init__(self):
        self.coins = player.coins
        self.oxygen_bottle = player.oxygen_bottle
        self.room = niveau
        self.chaussure = player.chaussure
        self.score_font = pygame.font.SysFont('Consolas', 30)

    def update(self):
        self.player_coins = self.score_font.render("Coins : "+str(self.coins), True, pygame.Color("yellow"), pygame.Color("black"))
        self.player_oxygen_bottle = self.score_font.render("Bouteille d'Oxygène : "+str(self.oxygen_bottle), True, pygame.Color("lightblue"), pygame.Color("black"))
        self.player_room = self.score_font.render("Salle : "+niveau.num_level, True, pygame.Color("green"), pygame.Color("black"))
        if player.chaussure is True:
            etat_chaussure = "Acquise"
        elif player.chaussure is False:
            etat_chaussure = "Non Acquise"
        self.player_chaussure = self.score_font.render("Chaussures à propulsion : "+str(etat_chaussure), True, pygame.Color("red"), pygame.Color("black"))

    def draw(self):
        screen.blit(self.player_coins, (5, 2))
        screen.blit(self.player_oxygen_bottle, (5, 40))
        screen.blit(self.player_room, (screen.get_width()/1.2, screen.get_height()/20))
        screen.blit(self.player_chaussure, (5, 80))


class Niveau:

    num_level = None

    width = None
    height = None
    size_x = None
    size_y = None

    porteE = None
    porteS = None
    porteW = None
    porteN = None

    sortieN = None
    sortieW = None
    sortieE = None
    sortieS = None

    def __del__(self):
        pass

    def __init__(self, fichier):
        self.fichier = fichier
        self.num_level = fichier[10:-4]
        self.structure = None

    def generer(self):
        # Méthode permettant de générer le niveau en fonction du fichier

        f = open(self.fichier, "r")

        first_line = f.readline()

        self.width = int(first_line[:2])
        self.height = int(first_line[3:])

        self.size_x = int(640 / self.width)
        self.size_y = int(480 / self.height)

        structure_niveau = []
        for line in f:
            if line != "\n":
                ligne_niveau = []
                for car in line:
                    if car != '\n':
                        ligne_niveau.append(car)
                structure_niveau.append(ligne_niveau)
            else:
                break
        self.structure = structure_niveau

        for line in f:
            if line[0] == 'N':
                self.sortieN = 'rooms/' + line[2:-1] + '.txt'
            elif line[0] == 'W':
                self.sortieW = 'rooms/' + line[2:-1] + '.txt'
            elif line[0] == 'E':
                self.sortieE = 'rooms/' + line[2:-1] + '.txt'
            elif line[0] == 'S':
                self.sortieS = 'rooms/' + line[2:-1] + '.txt'

        f.close()

    def afficher(self):
        # Méthode permettant d'afficher le niveau en fonction de la liste de structure renvoyé par la fonction generer
        playerlol = None
        num_ligne = 0
        for ligne in self.structure:
            num_case = 0
            for sprite in ligne:
                x = num_case * self.size_x + MARGIN_X
                y = num_ligne * self.size_y + MARGIN_Y
                if sprite == ".":
                    Wall((x, y))
                elif sprite == "C":
                    Caisse((x, y))
                elif sprite == "N":
                    self.porteN = pygame.Rect(x, y, self.size_x, self.size_y)
                    objs.append(Obj((x, y)))
                elif sprite == "S":
                    self.porteS = pygame.Rect(x, y, self.size_x, self.size_y)
                    objs.append(Obj((x, y)))
                elif sprite == "E":
                    self.porteE = pygame.Rect(x, y, self.size_x, self.size_y)
                    objs.append(Obj((x, y)))
                elif sprite == "W":
                    self.porteW = pygame.Rect(x, y, self.size_x, self.size_y)
                    objs.append(Obj((x, y)))
                elif sprite == "Z":
                    Souffleur((x, y))
                elif sprite == "P":
                    Piece((x, y))
                elif sprite == "O":
                    Oxygen_bottle((x, y))
                elif sprite == "X":
                    playerlol = Player((x, y))  # Creation joueur ('X' sur la grille)
                    objs.append(Obj((x, y)))
                elif sprite == "Y":
                    PorteLock((x, y))
                elif sprite == "U":
                    PorteUnlock((x, y))
                elif sprite == "M":
                    Button((x, y))
                elif sprite == "I":
                    ButtonPressed((x, y))
                elif sprite == "G":
                    DalleElectrique((x, y))
                elif sprite == "J":
                    Chaussure((x, y))
                else:
                    objs.append(Obj((x, y)))
                num_case += 1
            num_ligne += 1

        return playerlol


# ----------------------------------------------------------------------------------------------------------------------


def clear_all():
    walls.clear()
    caisses.clear()
    souffleurs.clear()
    pieces.clear()
    oxygen_bottles.clear()
    chaussures.clear()
    dalles_electriques.clear()
    objs.clear()


def get_type(x, y):
    index = (y * 20) + x
    if index < 0 or index >= 20*15:
        return None
    return objs.__getitem__(index).type


def get_obj(x, y):
    return objs.__getitem__(y * 20 + x)


pygame.init()

pygame.display.set_caption("Sortez par une porte rouge!")
screen = pygame.display.set_mode((1024, 768))

clock = pygame.time.Clock()

audio_coins = pygame.mixer.Sound('assets/audio/coins.wav')  # Son de pieces
audio_walk = pygame.mixer.Sound('assets/audio/walk.wav')  # son de pas (clap, clap)
audio_oxygen_bottle = pygame.mixer.Sound('assets/audio/air_fill.wav')  # Son de bouteille oxygene
audio_door = pygame.mixer.Sound('assets/audio/close_door_1.wav')  # son de porte
audio_button = pygame.mixer.Sound('assets/audio/button_press.wav')  # son de boutton
audio_chaussure_propulsion = pygame.mixer.Sound('assets/audio/chaussure_propulsion.wav')  # son de propulsion air
audio_chaussure_recup = pygame.mixer.Sound('assets/audio/chaussure_lacet.wav')  # son d'enfilage de chaussure
audio_electric = pygame.mixer.Sound('assets/audio/electric.wav')  # son d'electricité


MARGIN_X = (screen.get_width() - 640) / 2
MARGIN_Y = (screen.get_height() - 480) / 2

objs = []  # Liste de tous les blocs
walls = []  # Liste des murs
caisses = []  # Liste des caisses
souffleurs = []  # Liste des souffleurs
pieces = []  # Liste des pieces (coins)
oxygen_bottles = []  # Liste des bouteilles d'oxygene
buttons = []  # Liste des boutons
buttons_pressed = []  # Liste des boutons activés
portes_unlock = []  # Liste des portes deverouilles
portes_lock = []  # Liste des portes verouilles
dalles_electriques = []  # Liste des dalles electriques
chaussures = [] # Liste des chaussures à propulsion


niveau = Niveau("rooms/room1.txt")
niveau.generer()
player = niveau.afficher()

wall_image = pygame.transform.scale(pygame.image.load('assets/wall.png'), (niveau.size_x, niveau.size_y))
wind_image = pygame.transform.scale(pygame.image.load('assets/wind_jet.png'), (niveau.size_x, niveau.size_y))
box_image = pygame.transform.scale(pygame.image.load('assets/Caisse1.png'), (niveau.size_x, niveau.size_y))
coin_image = pygame.transform.scale(pygame.image.load('assets/coin.png'), (niveau.size_x, niveau.size_y))
floor_image = pygame.transform.scale(pygame.image.load('assets/floor.png'), (niveau.size_x, niveau.size_y))
room_image = pygame.transform.scale(pygame.image.load('assets/room.png'), (niveau.size_x, niveau.size_y))
oxygen_image = pygame.transform.scale(pygame.image.load('assets/Oxygen_Bottle.png'), (niveau.size_x, niveau.size_y))
button_image = pygame.transform.scale(pygame.image.load('assets/Red_Button.png'), (niveau.size_x, niveau.size_y))
button_pressed_image = pygame.transform.scale(pygame.image.load('assets/Grey_Button_.png'), (niveau.size_x, niveau.size_y))
porte_unlock_image = pygame.transform.scale(pygame.image.load('assets/Porte_Unlock.png'), (niveau.size_x, niveau.size_y))
porte_lock_image = pygame.transform.scale(pygame.image.load('assets/Porte_Lock.png'), (niveau.size_x, niveau.size_y))
dalle_electrique_image = pygame.transform.scale(pygame.image.load('assets/Electric.png'), (niveau.size_x, niveau.size_y))
chaussure_image = pygame.transform.scale(pygame.image.load('assets/Flashy_Boots.png'), (niveau.size_x, niveau.size_y))

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

    # collisions portes
    if niveau.porteE is not None and player.rect.colliderect(niveau.porteE):
        clear_all()
        a = niveau.sortieE
        niveau.__del__()
        niveau = Niveau(a)
        niveau.generer()
        niveau.afficher()
        player.rect.x = niveau.porteW.x + niveau.size_x
        player.rect.y = niveau.porteW.y
    elif niveau.porteS is not None and player.rect.colliderect(niveau.porteS):
        clear_all()
        a = niveau.sortieS
        niveau.__del__()
        niveau = Niveau(a)
        niveau.generer()
        niveau.afficher()
        player.rect.x = niveau.porteN.x
        player.rect.y = niveau.porteN.y + niveau.size_y
    elif niveau.porteN is not None and player.rect.colliderect(niveau.porteN):
        clear_all()
        a = niveau.sortieN
        niveau.__del__()
        niveau = Niveau(a)
        niveau.generer()
        niveau.afficher()
        player.rect.x = niveau.porteS.x
        player.rect.y = niveau.porteS.y - niveau.size_y
    elif niveau.porteW is not None and player.rect.colliderect(niveau.porteW):
        clear_all()
        a = niveau.sortieW
        niveau.__del__()
        niveau = Niveau(a)
        niveau.generer()
        niveau.afficher()
        player.rect.x = niveau.porteE.x - niveau.size_x
        player.rect.y = niveau.porteE.y

    # Affichage du sol
    y = 0
    while y < niveau.height:
        x = 0
        while x < niveau.width:
            screen.blit(floor_image, (x * niveau.size_x + MARGIN_X, y * niveau.size_y + MARGIN_Y))
            x += 1
        y += 1

    # Affichage des blocs
    for obj in objs:
        image = None
        if obj.type == "wall":
            image = wall_image
        elif obj.type == "box":
            image = box_image
        elif obj.type == "wind_jet":
            image = wind_image
        elif obj.type == "coin":
            image = coin_image
        elif obj.type == "oxygen":
            image = oxygen_image
        elif obj.type == "button":
            image = button_image
        elif obj.type == "button_pressed":
            image = button_pressed_image
        elif obj.type == "porte_lock":
            image = porte_lock_image
        elif obj.type == "porte_unlock":
            image = porte_unlock_image
        elif obj.type == "dalle_electrique":
            image = dalle_electrique_image
        elif obj.type == "chaussure":
            image = chaussure_image

        if image is not None:
            screen.blit(image, (obj.rect.x, obj.rect.y))

    score = Score()
    score.update()

    if niveau.porteE is not None:
        pygame.draw.rect(screen, (255, 0, 0), niveau.porteE)
    if niveau.porteS is not None:
        pygame.draw.rect(screen, (255, 0, 0), niveau.porteS)
    if niveau.porteN is not None:
        pygame.draw.rect(screen, (255, 0, 0), niveau.porteN)
    if niveau.porteW is not None:
        pygame.draw.rect(screen, (255, 0, 0), niveau.porteW)

    pygame.draw.rect(screen, (255, 255, 0), player.rect)
    score.draw()
    pygame.display.flip()
