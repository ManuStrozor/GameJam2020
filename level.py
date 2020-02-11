from collections import defaultdict
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

        self.objs = []  # Liste des blocs
        self.d_objs = defaultdict(list)  # Dictionnaire ordonnée/groupée des blocs

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
                    self.game.set_lvl(self.num_level)
                elif ch == "#":
                    item = Wall(self, (x, y))
                elif ch == "N":
                    item = Saas(self, (x, y), "North")
                elif ch == "S":
                    item = Saas(self, (x, y), "South")
                elif ch == "E":
                    item = Saas(self, (x, y), "East")
                elif ch == "W":
                    item = Saas(self, (x, y), "West")
                elif ch == "Z":
                    item = Souffleur(self, (x, y))
                elif ch == "C":
                    item = Caisse(self, (x, y))
                elif ch == "P":
                    item = Piece(self, (x, y))
                elif ch == "O":
                    item = OxygenBottle(self, (x, y))
                elif ch == "U":
                    item = Porte(self, (x, y))
                elif ch == "Y":
                    item = Porte(self, (x, y))
                    item.type = "porte_lock"
                elif ch == "M":
                    item = Button(self, (x, y))
                elif ch == "I":
                    item = Button(self, (x, y))
                    item.type = "button_pressed"
                elif ch == "G":
                    item = DalleElectrique(self, (x, y))
                elif ch == "J":
                    item = Chaussure(self, (x, y))
                elif ch == "_":
                    item = DalleInnonde(self, (x, y))
                elif ch == "F":
                    item = EventFin(self, (x, y))

                self.objs.append(item)

                if item.type is not None:
                    self.d_objs[item.type].append(item)

                num_case += 1
            num_ligne += 1

    def get_saas(self, card):
        for saas in self.d_objs["saas"]:
            if saas.cardinal == card:
                return saas

    def remove(self, item):
        self.objs.remove(item)
        self.d_objs[item.type].remove(item)


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
