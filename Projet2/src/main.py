from os import error
import sys
from sys import argv
import argparse
import numpy as np
from entrainementBD import *
from rechercheBD import *
from time import time
from traceback import print_exc
from connexionDB import *


def main():
    fenetre = enc = chemin = None
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', dest='command', action='store_const', const='entrainement')
    group.add_argument('-r', dest='command', action='store_const', const='recherche')
    group.add_argument('-b', dest='command', action='store_const', const='resetDB')

    try:
        args, option_args = parser.parse_known_args()
    except:
        print("\n Commande invalide! veuillez relancer le programme! \n Commande valide : -e -r -b")
        exit()

    if args.command == 'entrainement':
        parser.add_argument('-t', dest='taille', action='store', type=int, required=True)
        parser.add_argument('--enc', dest='encodage', action='store', required=True)
        parser.add_argument('--chemin', dest='chemin', action='store', required=True)

        parser.parse_args(option_args, namespace=args)

        try:
            fenetre = args.__getattribute__('taille')
            enc = args.__getattribute__('encodage')
            chemin = args.__getattribute__('chemin')
        except argparse.ArgumentError or argparse.ArgumentTypeError:
            print("\nVeuillez entrer des arguments valides: taille de la fenêtre, encodage et chemin")
            exit()


        trainer = Entraineur(fenetre, enc, chemin)
        trainer.entrainement()

    elif args.command == 'recherche':
        parser.add_argument('-t', dest='taille', action='store', type=int, required=True)

        parser.parse_args(option_args, namespace=args)

        try:
            fenetre = args.__getattribute__('taille')
        except argparse.ArgumentError or argparse.ArgumentTypeError:
            print("\nVeuillez entrer une taille de recherche valide (nombre)")

        print("Taille: ", fenetre)
        rep = input(
            "\nEntrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, i.e. produit sclaire:0 least-squares:1, city-block: 2) Choisir 'q' pour quitter\n\n")

        while rep != 'q':
            try:
                leMot, nbSyn, methode = rep.split()

                searchT = time()
                research = Recherche(leMot.lower(), int(methode))
                ShowResults(research.operation(), int(nbSyn))
                print(f'\nTemps de la recherche: {round((time() - searchT), 2)} secondes')

            except:
                print_exc()
                #print("\nVous navez pas entrez le nombre suffisents d'arguments, Veuillez reesayer")

            rep = input(
                "\nEntrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, i.e. produit sclaire:0 least-squares:1, city-block: 2) Choisir 'q' pour quitter\n\n")

        print("\nmerci")

        exit()


    elif args.command == 'resetDB':
        unknown = argv[2:]
        # si autre arguments entrés, mis dans une liste

        if len(unknown) == 0:
            db = ConnexionDB()
            db.drop_tables()

            print("DB HAS BEEN RESET")
        else:
            print("\nInvalide - l'option '-b' ne prend aucun argument")

def ShowResults(resultList , nbSyn):

    print("\n")
    i = 0
    for result in resultList:
        i+= 1
        print(f"{result[0]} --> {str(result[1])}")
        if i == nbSyn:
            break



if __name__ == '__main__':
    quit(main())
