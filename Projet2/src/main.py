import sys
from sys import argv
import argparse
import numpy as np
from entrainementBD import *
from rechercheBD import *
from time import time
from traceback import print_exc

"""
 TODO Fichier connexion - avec fonctions d'accès, création de table - TRÈS similaire à l'exemple du prof
 TODO Gestion des arguments - https://docs.python.org/3/library/argparse.html
            -e (entrainement) - t (taille) --enc (encodage) --chemin (path)
            -r : rechercher des synonymes -t <taille> : taille de fenêtre. <taille> doit suivre -t, précédé d’un espace.
            -b générer BD (delete DB)
TODO Modifier entrainement pour entrainementBD
TODO Modifier recherche pour rechercheBD

 """

def main():
    fenetre = enc = chemin = None
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', dest='command', action='store_const', const='entrainement')
    group.add_argument('-r', dest='command', action='store_const', const='recherche')
    group.add_argument('-b', dest='command', action='store_const', const='resetDB')

    args, option_args = parser.parse_known_args()

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
        except argparse.ArgumentError or argparse.ArgumentTypeError:
            print("\nVeuillez entrer une taille de recherche valide (nombre)")

    elif args.command == 'resetDB':

        unknown = argv[2:]
        # si autre arguments entrés, mis dans une liste

        if len(unknown) == 0:
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

    """
     # Gestion des arguments (tailleFenetre,encodage, chemin)
     Affichage des erreurs si arguments invalide


     # Dans le init, se créer une instance d'Entraineur

     # Logique d'entraineur :
     - Créer liste des mots uniques
     - Créer liste des stop-word avec un count de la liste des mots les plus courants**
     - Créer matrice selon taille de la taille du dictionnaire
     - Créer dictionnaire{Str:Mot, Int:Index}



     #
     INPUT "Entrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, i.e. produit sclaire:0 least-squares:1, city-block: 2

     Tapez q pour quitter"

     (while not q) blablabla
            Validation des inputs
            -Notez le temps de départ
            Si pas d'erreur retourné, main initialise recherche : (dict_mot, matrice de coocurences, leMot, nbSyn, methCalc)


            #Logique de recherche

                -Selon logique calcul - notez si le sort doit être croissant ou decroissant
                -Notez l'index du mot dans dict_mot (ou afficher erreur si mot n'Est pas présent)

                -Pour chaque Ligne dans Matrice de Coocurences EXCEPT ligne du LeMOT
                    -Méthode de calcul de LeMot vs tout les autres mots
                    -Enregistrer le résultat dans une structure de données
                    -Sorter structure de donner selon l'ordre

                Créer réponse (pop() selon nombre demandé dans nouvelle liste.

                Return Réponse

            # Retour au main
                -Notez le temps de fin
                -Faire l'affichage

    -----
    Fin du programme





     -- Stop-list - peut prendre un corpus ou par programmation?
     -- Est-ce qu'on doit prendre en considération les phrases dans la fenêtre?
     -- Le UI?
    """
