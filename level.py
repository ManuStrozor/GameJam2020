from objects.objects import *


class Level:

    def __init__(self, game):
        self.game = game

        self.width = 0
        self.height = 0
        self.size_x = 0
        self.size_y = 0
        self.structure = []
        self.num_level = None

        self.sortieN = None
        self.sortieW = None
        self.sortieE = None
        self.sortieS = None
        self.event_fin = None

        self.objs = []  # Liste de tous les blocs--------------------------

        self.caisses = []  # Liste des caisses-----------------------------
        self.pieces = []  # Liste des pieces (coins)-----------------------
        self.oxygen_bottles = []  # Liste des bouteilles d'oxygene---------
        self.buttons = []  # Liste des boutons-----------------------------
        self.buttons_pressed = []  # Liste des boutons activés-------------
        self.portes_unlock = []  # Liste des portes deverouilles-----------
        self.portes_lock = []  # Liste des portes verouilles---------------
        self.chaussures = []  # Liste des chaussures à propulsion----------
        self.walls = []  # Liste des murs----------------------------------
        self.souffleurs = []  # Liste des souffleurs-----------------------
        self.dalles_electriques = []  # Liste des dalles electriques-------
        self.dalles_innondes = []  # Liste des dalles innondes-------------
        self.all_saas = []  # liste des saas-------------------------------

    def init_structure(self):
        # Méthode permettant d'afficher le niveau en fonction de la liste de structure renvoyé par la fonction generer
        num_ligne = 0
        for ligne in self.structure:

            num_case = 0
            for ch in ligne:

                x = num_case * self.size_x + self.game.MARGIN_X
                y = num_ligne * self.size_y + self.game.MARGIN_Y

                item = Object(self, (x, y))
                if ch == "X":
                    self.game.spawn = (x, y)
                elif ch == "#":
                    item = Wall(self, (x, y))
                    self.walls.append(item)
                elif ch == "N":
                    item = Saas(self, (x, y), "North")
                    self.all_saas.append(item)
                elif ch == "S":
                    item = Saas(self, (x, y), "South")
                    self.all_saas.append(item)
                elif ch == "E":
                    item = Saas(self, (x, y), "East")
                    self.all_saas.append(item)
                elif ch == "W":
                    item = Saas(self, (x, y), "West")
                    self.all_saas.append(item)
                elif ch == "Z":
                    item = Souffleur(self, (x, y))
                    self.souffleurs.append(item)
                elif ch == "C":
                    item = Caisse(self, (x, y))
                    self.caisses.append(item)
                elif ch == "P":
                    item = Piece(self, (x, y))
                    self.pieces.append(item)
                elif ch == "O":
                    item = OxygenBottle(self, (x, y))
                    self.oxygen_bottles.append(item)
                elif ch == "Y":
                    item = PorteLock(self, (x, y))
                    self.portes_lock.append(item)
                elif ch == "U":
                    item = PorteUnlock(self, (x, y))
                    self.portes_unlock.append(item)
                elif ch == "M":
                    item = Button(self, (x, y))
                    self.buttons.append(item)
                elif ch == "I":
                    item = ButtonPressed(self, (x, y))
                    self.buttons_pressed.append(item)
                elif ch == "G":
                    item = DalleElectrique(self, (x, y))
                    self.dalles_electriques.append(item)
                elif ch == "J":
                    item = Chaussure(self, (x, y))
                    self.chaussures.append(item)
                elif ch == "_":
                    item = DalleInnonde(self, (x, y))
                    self.dalles_innondes.append(item)
                elif ch == "F":
                    item = EventFin(self, (x, y))
                    self.event_fin = item

                self.objs.append(item)

                num_case += 1

            num_ligne += 1


def gen_levels(game, path):
    f = open(path, "r")
    lines = f.readlines()
    f.close()

    levels = []

    i = 0
    while lines[i] != "END\n":

        lvl = Level(game)
        lvl.num_level = int(lines[i])

        i += 1
        while lines[i] != "\n":

            lvl.width = len(lines[i])-1
            lvl.structure.append(lines[i])
            lvl.height += 1

            i += 1

        lvl.size_x = int(game.WIDTH / lvl.width)
        lvl.size_y = int(game.HEIGHT / lvl.height)

        i += 1
        while lines[i] != "\n":

            if lines[i][0] == 'N':
                lvl.sortieN = int(lines[i][1:-1])
            elif lines[i][0] == 'W':
                lvl.sortieW = int(lines[i][1:-1])
            elif lines[i][0] == 'E':
                lvl.sortieE = int(lines[i][1:-1])
            elif lines[i][0] == 'S':
                lvl.sortieS = int(lines[i][1:-1])

            i += 1

        levels.append(lvl)

        i += 1

    return levels
