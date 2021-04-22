"""

•	-t <taille> : taille de fenêtre. <taille> doit suivre -t, précédé d’un espace
•	-n <nombre>: nombre maximal de mots à afficher par cluster (à la fin de l’exécution)
•	-k <nombre> : nombre de centroïdes, une valeur entière. Avec cette option, vous devez choisir <nombre> vecteur(s) de votre matrice aléatoirement. Ces vecteurs sont les coordonnées initiales des centroïdes.


Init : 
1)Chaque cluster est un vecteur de mot prit au hasard dans le dictionnaire - on sors le vecteur de ce mot dans la matrice reconstituée

======
2)Ensuite  CHAQUE mot se compare à l'un des cluster choisi (avec least-square) et s'ajoute dans "l'équipe" du cluster avec le meilleur mot.

3)On prend une "capture d'écran" des équipes. 

4)On calcule la moyenne "np.average(data, axis=0)" des vecteurs à 24000 dimensions de chacune des équipes pour déterminer le nouveau centroide.
======

5)On refait l'étape 2 à 4 jusqu'à temps que les coordonnées des centroides restent identique = CONVERGENCE

6) SUCCESS!


"""

import numpy as np
import random
from time import time
from connexionDB import *

class Kmeans:

    def __init__(self, tailleFenetre, nbMots, nbCentroides):
        self.fenetre = int(tailleFenetre)
        self.connexion = ConnexionDB()
        self.motsUnique = self.connexion.get_words()
        self.concMatrix = self.connexion.get_cooc_mat(len(self.motsUnique), int(tailleFenetre))
        self.clusters = []  
        self.centroides = []    
        self.iteration = 0
        self.nbChangements = 0
        self.nbMots = int(nbMots)
        self.nbCentroides = int(nbCentroides)
        self.stable = False

    def initialize(self):
        self.tempsGlobal = time()
        self.tempsIteration = time()
        for i in range(0, self.nbCentroides):
            arr = np.array(random.choice(self.concMatrix))
            self.centroides.append(arr)
            self.clusters.append([])
            
            
        for mot, value in self.motsUnique.items():
            resultatsTemp = []       
            for i in range(0, self.nbCentroides):                         
                resultatsTemp.append(self.__leastSquares(self.centroides[i], self.concMatrix[value])) 

            minElement = np.amin(resultatsTemp)
            result = np.where(resultatsTemp == np.amin(resultatsTemp))                 
            self.clusters[result[0][0]].append(self.concMatrix[value])

        self.nbChangements = len(self.motsUnique)
        self.printIteration()
        
       

    
    def printIteration(self):
        print("\n")
        print("============================================================================")
        print(f'Itération {self.iteration}')
        print(f'{self.nbChangements} changements de cluster en {round((time() - self.tempsIteration), 2)} secondes.\n')
        for i in range(0, self.nbCentroides):
            print(f'Il y a {len(self.clusters[i])} points (mots) regroupés autour du centroïde no {i}')
        print("\n============================================================================")

    def start(self):
        while(not self.stable):
            self.tempsIteration = time()
            self.iterate()
            self.printIteration()
        self.afficherResultats()
        print(f'Temps global: {round((time() - self.tempsGlobal), 2)} secondes')
        return 1

    def iterate(self):        
        #print("Début de l'itération")
        self.newClusters = []
        self.nbChangements = 0
        self.newCentroides = []
        #print("Début de la création des nouveaux centroides")
        for cluster in self.clusters:
            cluster = np.array(cluster)
            self.newClusters.append([])
            self.newCentroides.append(np.average(cluster, axis=0))
        #print("Fin de la création des nouveaux centroides")

        #print("Début de checkConvergence")
        #self.checkConvergence()
        #print("Fin de checkConvergence")
        

        
        #print("Début calcul scores de chaque mot")
        for mot, value in self.motsUnique.items():
            resultatsTemp = []       
            for i in range(0, self.nbCentroides):                         
                resultatsTemp.append(self.__leastSquares(self.newCentroides[i], self.concMatrix[value])) 

            minElement = np.amin(resultatsTemp)
            result = np.where(resultatsTemp == np.amin(resultatsTemp))                 
            self.newClusters[result[0][0]].append(self.concMatrix[value])

        #print("Fin calcul scores de chaque mot")
        self.iteration += 1
        #print("Début calcul changement")
        self.calculateChange()

        if self.nbChangements == 0:
            self.stable = True
        #print("Fin calcul changement")
            
    def afficherResultats(self):
        pass            

    def checkConvergence(self):
        egal = True
        for i in range(0, self.nbCentroides):
            if not np.array_equal(self.newCentroides[i], self.centroides[i]):
                egal = False

        if egal:
            self.stable = True

    def calculateChange(self):
        for i in range(0, self.nbCentroides):
            self.nbChangements += np.absolute(len(self.newClusters[i]) - len(self.clusters[i]))
            self.clusters[i] = self.newClusters[i]

        self.nbChangements /= 2 

    def __leastSquares(self, motA, motB):  # motA & motB = type np.array(1,y)
        return np.sum(np.square(motA - motB))