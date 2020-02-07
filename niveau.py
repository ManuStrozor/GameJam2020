from objects import *


class Niveau:

    def __init__(self, game, path):
        self.game = game

        self.width = None
        self.height = None
        self.size_x = None
        self.size_y = None
        self.structure = None
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

        self.walls = []  # Liste des murs
        self.souffleurs = []  # Liste des souffleurs
        self.dalles_electriques = []  # Liste des dalles electriques
        self.dalles_innondes = []  # Liste des dalles innondes
        self.all_saas = []  # liste des saas

        self.generer(path)
        self.afficher()

    def generer(self, path):  # Méthode permettant de générer le niveau en fonction du fichier
        self.num_level = path[10:-4]

        f = open(path, "r")

        first_line = f.readline()

        self.width = int(first_line[:2])
        self.height = int(first_line[3:])

        self.size_x = int(self.game.WIDTH / self.width)
        self.size_y = int(self.game.HEIGHT / self.height)

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
                self.sortieN = line[2:-1]
            elif line[0] == 'W':
                self.sortieW = line[2:-1]
            elif line[0] == 'E':
                self.sortieE = line[2:-1]
            elif line[0] == 'S':
                self.sortieS = line[2:-1]

        f.close()

    def afficher(self):
        # Méthode permettant d'afficher le niveau en fonction de la liste de structure renvoyé par la fonction generer
        num_ligne = 0
        for ligne in self.structure:
            num_case = 0
            for ch in ligne:
                x = num_case * self.size_x + self.game.MARGIN_X
                y = num_ligne * self.size_y + self.game.MARGIN_Y

                item = Obj(self, (x, y))
                if ch == ".":
                    item = Wall(self, (x, y))
                    self.walls.append(item)
                elif ch == "X":
                    self.game.spawn = (x, y)
                elif ch == "C":
                    item = Caisse(self, (x, y))
                    self.caisses.append(item)
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
                elif ch == "Q":
                    item = DalleInnonde(self, (x, y))
                    self.dalles_innondes.append(item)
                elif ch == "F":
                    item = EventFin(self, (x, y))
                    self.event_fin = item
                self.objs.append(item)
                num_case += 1
            num_ligne += 1
