import re
import numpy as np
import math
import Entraineur
import Recherche


def main():
    fenetre, enc, chemin = argv[1:]
    trainer = Entraineur(int(fenetre), enc, chemin)

    if trainer.entrainement() == 0:


        rep = None
        while rep != 'q':
            rep = input(
                "\nEntrez un mot, le nombre de synonymes que vous voulez et la méthode de calcul, i.e. produit sclaire:0 least-squares:1, city-block: 2) Choisir 'q' pour quitter\n\n")
            leMot, nbSyn, methode = rep.split()

            search = Recherche(trainer.motsUnique, trainer.matriceCo, leMot, int(methode))

            resultat = search.sortResult()

            if resultat == -1:
                #print erreurà
                pass
            elif resultat == -2:
                #autre erreur
                pass
            else:
                #afficher les résultats selon le nb de syn avec .pop()
                pass






        print("merci")


    else:
        # afficher erreur
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

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
