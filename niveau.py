from objects import *
from player import Player


class Niveau:

    width = None
    height = None
    size_x = None
    size_y = None
    num_level = None

    sortieN = None
    sortieW = None
    sortieE = None
    sortieS = None

    def __init__(self, game):
        self.game = game
        self.structure = None

    def generer(self, fichier):  # Méthode permettant de générer le niveau en fonction du fichier
        self.num_level = fichier[10:-4]

        f = open(fichier, "r")

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
            for ch in ligne:
                x = num_case * self.size_x + self.game.MARGIN_X
                y = num_ligne * self.size_y + self.game.MARGIN_Y

                if ch == ".":
                    Wall(self.game, (x, y))
                elif ch == "C":
                    Caisse(self.game, (x, y))
                elif ch == "N":
                    Saas(self.game, (x, y), "North")
                elif ch == "S":
                    Saas(self.game, (x, y), "South")
                elif ch == "E":
                    Saas(self.game, (x, y), "East")
                elif ch == "W":
                    Saas(self.game, (x, y), "West")
                elif ch == "Z" or ch == "z" or ch == 'Z' or ch == 'z':
                    Souffleur(self.game, (x, y))
                elif ch == "P":
                    Piece(self.game, (x, y))
                elif ch == "O":
                    OxygenBottle(self.game, (x, y))
                elif ch == "X":
                    playerlol = Player(self.game, (x, y))  # Creation joueur ('X' sur la grille)
                    self.game.objs.append(Obj(self.game, (x, y)))
                elif ch == "Y":
                    PorteLock(self.game, (x, y))
                elif ch == "U":
                    PorteUnlock(self.game, (x, y))
                elif ch == "M":
                    Button(self.game, (x, y))
                elif ch == "I":
                    ButtonPressed(self.game, (x, y))
                elif ch == "G":
                    DalleElectrique(self.game, (x, y))
                elif ch == "J":
                    Chaussure(self.game, (x, y))
                elif ch == "Q":
                    DalleInnonde(self.game, (x, y))
                else:
                    self.game.objs.append(Obj(self.game, (x, y)))
                num_case += 1
            num_ligne += 1

        return playerlol
