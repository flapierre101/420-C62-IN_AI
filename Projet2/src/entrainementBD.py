import re
import numpy as np
from traceback import print_exc

from connexionDB import *
from time import time

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
        self.motsUnique = None
        self.connexion = ConnexionDB()

        # self.connexion.drop_tables()
        self.connexion.creer_tables()

    def entrainement(self):
        trainerT = time()
        try:
            liste_mots = re.findall(
                '\w+', open(self.path, 'r', encoding=self.encodage).read())
            liste_mots = [x.lower() for x in liste_mots]
        except:
            print(
                "\n*** Fichier non reconnu, veuillez entrez un chemin valide et reesayer ***")
            return 1

        self.motsUnique = self.__creerListeUnique(liste_mots)

        self.__parcourirMatrice(self.motsUnique, liste_mots)

        print(
            f'Temps de l\'entraîneur: {round((time() - trainerT), 2)} secondes')

        return 0

    def __creerListeUnique(self, liste_mots):

        motUnique = self.connexion.get_words()

        listetuples = []

        for mot in liste_mots:
            if mot not in motUnique:
                listetuples.append((len(motUnique), mot))
                motUnique[mot] = len(motUnique)

        self.connexion.insert_new_word(listetuples)

        return motUnique

    # version en utilisant la symétrie, pas besoin de regarder l'index précédent. Gain de 0.05 secondes.
    def __parcourirMatrice(self, motsUnique, liste_mots):
        moitieF = self.fenetre // 2

        dict_cooc = {}

        dict_vieux = self.connexion.get_cooc_dict()

        for i in range(len(liste_mots)):
            motCentral = motsUnique[liste_mots[i]]
            for j in range(1, moitieF + 1):
                if not i + j >= len(liste_mots) and motCentral != motsUnique[liste_mots[i + j]]:

                    indexcooc = motsUnique[liste_mots[i + j]]
                    if (motCentral, indexcooc) not in dict_cooc:
                        dict_cooc[(motCentral, indexcooc)] = 1
                    else:
                        dict_cooc[(motCentral, indexcooc)] += 1

                    if (indexcooc, motCentral) not in dict_cooc:
                        dict_cooc[(indexcooc, motCentral)] = 1
                    else:
                        dict_cooc[(indexcooc, motCentral)] += 1

    # comparer dict_vieux avec nouveau dict  (dict_cooc):
        listetuplesupdate = []
        listetuplesnew = []

        dict_new = {}

        for key in dict_cooc:
            if (key[0], key[1]) in dict_vieux:
                valeur = dict_cooc[key[0], key[1]] + dict_vieux[key[0], key[1]]
                listetuplesupdate.append(
                    (valeur, key[0], key[1], self.fenetre))
            elif (key[1], key[0]) not in dict_new:
                listetuplesnew.append((key[0], key[1], dict_cooc[(key[0], key[1])],  self.fenetre))
                dict_new[(key[0], key[1])] = dict_cooc[(key[0], key[1])]

        self.connexion.insert_mat(listetuplesnew)
        if len(dict_vieux) > 1:
            self.connexion.update_mat(listetuplesupdate)
