import sys
from sys import argv
import argparse
from entrainementBD import *
from rechercheBD import *
from kmeans import *
from time import time
from connexionDB import *


class Options:
    def __init__(self):
        self.fenetre = self.enc = self.chemin = None
        self.parser = argparse.ArgumentParser()
        self.group = self.parser.add_mutually_exclusive_group()

    def start(self):
        
        self.checkargs()       

        # Si entraînement choisi, ajout des arguments spécifiques à l'entraînement
        if self.args.command == 'entrainement':
            self.entrainement()

        # Si recherche choisie, ajout des arguments spécifiques à la recherche
        elif self.args.command == 'recherche':
            self.recherche()

        # Pour le clustering
        elif self.args.command == 'clustering':
            self.clustering()

        # Si reset de DB choisie, vérification si seul argument
        elif self.args.command == 'resetDB':
            self.reset()


    def checkargs(self):
         # Groupe mutuellement exclusif afin d'assurer une seule option choisie parmi les trois
        self.group.add_argument('-e', dest='command',
                        action='store_const', const='entrainement')
        self.group.add_argument('-r', dest='command',
                        action='store_const', const='recherche')
        self.group.add_argument('-b', dest='command',
                        action='store_const', const='resetDB')
        self.group.add_argument('-c', dest='command',
                        action='store_const', const='clustering')

        # Reste des arguments seront ajoutés et validés séparément car dépend de l'option choisie
        self.args, self.option_args = self.parser.parse_known_args()

        # Si aucun argument donné au lancement du script
        if len(sys.argv) == 1:
            print("\nErreur - Veuillez entrer les arguments nécessaires au lancement du script")
            exit()

    def entrainement(self):
        self.parser.add_argument('-t', dest='taille',
                                action='store', type=int, required=True)
        self.parser.add_argument('--enc', dest='encodage',
                            action='store', required=True)
        self.parser.add_argument('--chemin', dest='chemin',
                            action='store', required=True)

        try:
            self.parser.parse_args(self.option_args, namespace=self.args)
        except:
            print(
                "\nNombre d'arguments insuffisant. Veuillez entrer une taille de fenêtre, l'encodage et le chemin du texte voulu")
            exit()

        try:
            self.fenetre = self.args.__getattribute__('taille')
            self.enc = self.args.__getattribute__('encodage')
            self.chemin = self.args.__getattribute__('chemin')
        except argparse.ArgumentError or argparse.ArgumentTypeError:
            print(
                "\nVeuillez entrer des arguments valides: taille de la fenêtre (nombre entier), encodage (utf-8) et chemin")
            exit()

        trainer = Entraineur(self.fenetre, self.enc, self.chemin)
        reponse = trainer.entrainement()
        if reponse == 1:
            exit()

    def recherche(self):
        self.parser.add_argument('-t', dest='taille',
                                action='store', type=int, required=True)

        try:
            self.parser.parse_args(self.option_args, namespace=self.args)
        except:
            print(
                "\nNombre d'arguments insuffisant. Veuillez entrer une taille de fenêtre, l'encodage et le chemin du texte voulu")
            exit()

        try:
            self.fenetre = self.args.__getattribute__('taille')

            rep = input(
                "\nEntrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, i.e. produit scalaire:0 least-squares:1, city-block: 2) Choisir 'q' pour quitter\n\n")

            while rep != 'q':
                try:
                    leMot, nbSyn, methode = rep.split()

                    searchT = time()
                    research = Recherche(leMot.lower(), int(methode), self.fenetre)
                    resultats = research.operation()
                    if resultats[0] == "Invalide":
                        print(
                            "\nLa taille de la fenêtre ne retourne aucun résultat \nVeuillez relancer le script")
                        rep = 'q'
                    else:
                        ShowResults(resultats, int(nbSyn))
                        print(
                            f'\nTemps de la recherche: {round((time() - searchT), 2)} secondes')

                        rep = input(
                            "\nEntrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, i.e. produit scalaire:0 least-squares:1, city-block: 2) Choisir 'q' pour quitter\n\n")

                except:
                    print(
                        "\nInvalide - Veuillez entrer un mot, le nombre de synonymes voulu et une méthode de recherche")
                    exit()

            print("\nMerci")
            exit()

        except argparse.ArgumentError or argparse.ArgumentTypeError:
            print("\nVeuillez entrer une taille de recherche valide (nombre)")

    def clustering(self):
        self.parser.add_argument('-t', dest='taille',
                                action='store', type=int, required=True)
        self.parser.add_argument('-n', dest='nombreMots',
                            action='store', required=True)
        self.parser.add_argument('-k', dest='nombreCentroides',
                            action='store', required=True)

        try:
            self.parser.parse_args(self.option_args, namespace=self.args)
        except:
            print(
                "\nNombre d'arguments insuffisant. Veuillez entrer une taille de fenêtre, l'encodage et le chemin du texte voulu")
            exit()

        try:
            self.fenetre = self.args.__getattribute__('taille')
            nbMots = self.args.__getattribute__('nombreMots')
            nbCentroides = self.args.__getattribute__('nombreCentroides')
        except argparse.ArgumentError or argparse.ArgumentTypeError:
            print(
                "\nVeuillez entrer des arguments valides: taille de la fenêtre (nombre entier), encodage (utf-8) et chemin")
            exit()

        kmeans = Kmeans(self.fenetre, nbMots, nbCentroides)
        kmeans.initialize()
        reponse = kmeans.start()
        if reponse == 1:
            exit()

def reset(self):
    unknown = argv[2:]
            # si autre arguments entrés, mis dans une liste
    if len(unknown) == 0:
        db = ConnexionDB()
        db.drop_tables()
        print("\nLa base de données a été réinitialisée")
    else:
        print("\nInvalide - l'option '-b' ne prend aucun argument")

def ShowResults(resultList, nbSyn):
    print("\n")
    i = 0
    for result in resultList:
        i += 1
        print(f"{result[0]} --> {str(result[1])}")
        if i == nbSyn:
            break