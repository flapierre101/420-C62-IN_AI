import re
from connexionDB import *
from time import time


class Entraineur:

    def __init__(self, tailleFenetre, encodage, path):
        self.fenetre = int(tailleFenetre)
        self.encodage = encodage
        self.path = path
        self.motsUnique = None
        self.connexion = ConnexionDB()
        self.connexion.creer_tables()

    def entrainement(self):
        trainerT = time()
        try:
            # Vérification si le fichier avec la fenêtre de recherche à déjà été entré dans la BD
            check_file = self.connexion.get_file_db()


            existe = False
            for entry in check_file:
                ([5], '../textes/LeVentreDeParisUTF8.txt')
                if entry[0][0] == self.fenetre and self.path == entry[1]:
                    existe = True

            if not existe:
                liste_mots = re.findall(
                    '\w+', open(self.path, 'r', encoding=self.encodage).read())
                liste_mots = [x.lower() for x in liste_mots]
                self.connexion.insert_new_file(self.path, self.fenetre)
            else:
                print(
                    '''\n Le fichier est déjà dans la BD, veuillez entrez un nouveau fichier ou une autre taille de fenêtre''')
                return 0

        except:
            print(
                "\n*** Fichier non reconnu ou type d'encodage invalide, veuillez entrez un chemin valide ou changer le type d'encodage et reesayer ***")
            return 1

        self.motsUnique = self.__creerListeUnique(liste_mots)

        self.__coocurences(self.motsUnique, liste_mots)

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

    def __coocurences(self, motsUnique, liste_mots):
        moitieF = self.fenetre // 2

        dict_cooc = {}

        # Ajoute les données dans un dictionnaire au lieu d'une matrice.
        # La clé est un tuple des coordonnées d'une matrice
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

        listetuplesupdate = []  # données devant être modifiées
        listetuplesnew = []  # données à  ajouter
        dict_new = {}  # les nouveaux mots ajoutés

        dict_vieux = self.connexion.get_cooc_dict(
            self.fenetre)  # Les coocurences déjà existantes

        for key in dict_cooc:
            # Si mots existent, valeurs doit être modifiées
            if (key[0], key[1]) in dict_vieux:
                valeur = dict_cooc[key[0], key[1]] + dict_vieux[key[0], key[1]]
                listetuplesupdate.append(
                    (valeur, key[0], key[1], self.fenetre))
            # Sinon doit être ajoutée comme une nouvelle valeur.
            elif (key[1], key[0]) not in dict_new:
                listetuplesnew.append(
                    (key[0], key[1], dict_cooc[(key[0], key[1])],  self.fenetre))
                dict_new[(key[0], key[1])] = dict_cooc[(key[0], key[1])]

        self.connexion.insert_mat(listetuplesnew)
        if len(dict_vieux) > 1:
            self.connexion.update_mat(listetuplesupdate)
