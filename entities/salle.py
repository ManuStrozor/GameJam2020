import pygame


class Salle:

    width = 0
    height = 0

    # Classe permettant de créer une salle
    def __init__(self, game, fichier):
        self.game = game
        self.fichier = fichier
        self.structure = []

    def generer(self):
        #Méthode permettant de générer la salle en fonction du fichier.
        with open(self.fichier, "r") as fichier:
            structure_salle = []
            for ligne in fichier:
                ligne_salle = []
                self.width = 0
                for sprite in ligne:
                    if sprite != '\n':
                        ligne_salle.append(sprite)
                        self.width += 1
                structure_salle.append(ligne_salle)
                self.height += 1
            self.structure = structure_salle

    def afficher(self, fenetre):
        #Méthode permettant d'afficher la salle en fonction de generer()
        mur = pygame.Surface((self.game.window.get_width()/self.width, self.game.window.get_height()/self.height))
        #depart = pygame.draw.rect((20,20), [255,255,255])
        arrivee = pygame.Surface((100, 100))

        num_ligne = 0
        for ligne in self.structure:
            num_case = 0
            for sprite in ligne:
                x = num_case * 110 #taille_sprite
                y = num_ligne * 110 #taille_sprite
                if sprite == 'm':
                    fenetre.blit(mur, (x, y))
                #elif sprite == 'd':
                    #fenetre.blit(depart, (x,y))
                elif sprite == 'a':
                    fenetre.blit(arrivee, (x,y))
                num_case +=1
            num_ligne+=1

    def set_height(self, size):
        self.height = size

    def set_width(self, size):
        self.width = size
