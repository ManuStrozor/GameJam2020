from laby import *
import pygame

class Niveau:

    porteE = None
    porteS = None
    porteW = None
    porteN = None
    sortie = None
    roomsuivante = None

    def __init__(self, fichier):
        self.fichier = fichier
        self.structure = 0

    def generer(self):
        #Méthode permettant de générer le niveau en fonction du fichier
        with open(self.fichier, "r") as fichier:
            structure_niveau = []
            for ligne in fichier:
                ligne_niveau = []
                for sprite in ligne:
                    if sprite == '@':
                        self.sortie = ligne[1:2]
                        self.roomsuivante = ligne[2:17]
                        break
                    elif sprite != '\n':
                        ligne_niveau.append(sprite)
                structure_niveau.append(ligne_niveau)
            self.structure = structure_niveau

    def afficher(self, fenetre):
        #Méthode permettant d'afficher le niveau en fonction de la liste de structure renvoyé par la fonction generer

        num_ligne = 0
        for ligne in self.structure:
            num_case = 0
            for sprite in ligne:
                x = num_case * SIZE_X + MARGIN_X
                y = num_ligne * SIZE_Y + MARGIN_Y
                if sprite == '.':
                    Wall((x, y))
                elif sprite == 'C':
                    Caisse((x, y))
                elif sprite == "N":
                    self.porteN = pygame.Rect(x, y, SIZE_X, SIZE_Y)
                    objs.append(Obj((x, y)))
                elif sprite == "S":
                    self.porteS = pygame.Rect(x, y, SIZE_X, SIZE_Y)
                    objs.append(Obj((x, y)))
                elif sprite == "E":
                    self.porteE = pygame.Rect(x, y, SIZE_X, SIZE_Y)
                    objs.append(Obj((x, y)))
                elif sprite == "W":
                    self.porteW = pygame.Rect(x, y, SIZE_X, SIZE_Y)
                    objs.append(Obj((x, y)))
                elif sprite == 'Z':
                    Souffleur((x, y))
                elif sprite == 'P':
                    Piece((x, y))
                elif sprite == "O":
                    Oxygen_bottle((x, y))
                elif sprite== "X":
                    Player.player = Player((x, y))  # Creation joueur ('X' sur la grille)
                    print(str(player))
                    objs.append(Obj((x, y)))
                else:
                    objs.append(Obj((x, y)))
                num_case += 1
            num_ligne += 1

