import re
import numpy as np
from traceback import print_exc

"""
     # Gestion des arguments (tailleFenetre,encodage, chemin)
     Affichage des erreurs si arguments invalide
     
     
     # Dans le init, se créer une instance d'Entraineur
     
     # Logique d'entraineur :
     - Créer liste des mots uniques 
     - Créer liste des stop-word avec un count de la liste des mots les plus courants** 
     - Créer matrice selon taille de la taille du dictionnaire
     - Créer dictionnaire{Str:Mot, Int:Index}
    """


class Entraineur:

    def __init__(self, tailleFenetre, encodage, path):
        self.fenetre = int(tailleFenetre)
        self.encodage = encodage
        self.path = path
        self.matriceCo = None
        self.motsUnique = None

    def entrainement(self):
        try:
            liste_mots = re.findall('\w+', open(self.path, 'r', encoding=self.encodage).read())
            liste_mots = [x.lower() for x in liste_mots]

            self.motsUnique = self.__creerListeUnique(liste_mots)
            
            self.matriceCo = np.zeros((len(self.motsUnique), len(self.motsUnique)))

            self.__parcourirMatrice(self.motsUnique, liste_mots)

            return 0


        except:
            print("\n*** Svp entrer des paramètres valides: taille de la fenêtre, encodage et chemin vers le texte voulu ***")
            print_exc()
            return 1

    def __creerListeUnique(self, liste_mots):
        motUnique = {}
        

        for mot in liste_mots:
            if mot not in motUnique:
                motUnique[mot] = len(motUnique)
                

        return motUnique

    def __parcourirMatrice(self, motsUnique, liste_mots):

        moitieF = self.fenetre // 2
        for i in range(len(liste_mots)):
            motCentral = motsUnique[liste_mots[i]]
            for j in range(1, moitieF + 1):
                if not i - j < 0 and motCentral != motsUnique[liste_mots[i - j]]:
                    self.matriceCo[motCentral][motsUnique[liste_mots[i - j]]] += 1
                if not i + j >= len(liste_mots) and motCentral != motsUnique[liste_mots[i + j]]:
                    self.matriceCo[motCentral][motsUnique[liste_mots[i + j]]] += 1
