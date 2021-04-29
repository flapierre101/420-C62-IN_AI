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
  
        self.centroides = []    
        self.clustersData = []
        self.iteration = 0
        self.nbChangements = 0
        self.nbMots = int(nbMots)
        self.nbCentroides = int(nbCentroides)
        self.stable = False

    def initialize(self):
        self.tempsGlobal = time()
        self.tempsIteration = time()    
        self.clusterDictArray = []    
        self.clustersData = []
        indexCentroides = random.sample(range(0, len(self.motsUnique)), self.nbCentroides)
        
        for i in range(0, self.nbCentroides):          
            self.centroides.append(self.concMatrix[indexCentroides[i]])
            self.clusterDictArray.append({})
            self.clustersData.append([])       
    
        # Met chaque mot dans un cluster
        self.attribuerCluster(self.centroides, self.clusterDictArray)   

        self.nbChangements = len(self.motsUnique)

        self.printIteration()       
       

    
    def printIteration(self):      
        print("\n============================================================================")
        print(f'Itération {self.iteration}')
        print(f'{self.nbChangements} changements de cluster en {round((time() - self.tempsIteration), 2)} secondes.\n')
        for i in range(0, self.nbCentroides):
            print(f'Il y a {len(self.clusterDictArray[i])} points (mots) regroupés autour du centroïde no {i}')
        

    def start(self):        
        while(not self.stable):
            self.tempsIteration = time()
            self.iterate()
            self.printIteration()
        self.afficherResultats()
        
        return 1

    def iterate(self):        
        self.nbChangements = 0       
        newCentroides = []
        self.clustersData = []
        self.newClusterDictArray = []
               
        for cluster in self.clusterDictArray:
            clusterNP = np.array(list(cluster.values()))          
            self.clustersData.append([])
            self.newClusterDictArray.append({})
            newCentroides.append(np.average(clusterNP, axis=0))        
       
        self.attribuerCluster(newCentroides, self.newClusterDictArray)

        self.iteration += 1

        self.calculateChange(newCentroides)

        #print("Fin calcul changement")
    
    def attribuerCluster(self, centroides, clusterDict):
        for mot, value in self.motsUnique.items():
            resultatsTemp = []       
            for i in range(0, self.nbCentroides):                         
                resultatsTemp.append(self.__leastSquares(centroides[i], self.concMatrix[value])) 

            # minElement = le plus petit score, soit le meilleur pour least-square
            minElement = np.amin(resultatsTemp)
            # result[0][0] = l'index du cluster ou insérer le mot
            result = np.where(resultatsTemp == minElement)   
            indexCluster = result[0][0]        
            self.clustersData[indexCluster].append((mot, minElement))
            clusterDict[indexCluster][value] = self.concMatrix[value]
            
    def afficherResultats(self):    
        for i in range(len(self.clustersData)):
            print("\n****************************************************************************\n")
            print("Groupe ", i, "\n")
            self.clustersData[i] = sorted(self.clustersData[i],  key=lambda x: x[1])
            for j in range(self.nbMots):
                if j < len(self.clustersData[i]):
                    print(f"{self.clustersData[i][j][0]} --> {str(self.clustersData[i][j][1])}")
        print(f'\n\nClustering en {self.iteration} itérations. Temps écoulés : {round((time() - self.tempsGlobal), 2)} secondes')
 


    def calculateChange(self, newCentroides):
        self.nbChangements = 0

        for i in range(self.nbCentroides):            
            if self.clusterDictArray[i].keys() != self.newClusterDictArray[i].keys():   
                self.nbChangements += self.dict_compare(self.clusterDictArray[i], self.newClusterDictArray[i])
            self.clusterDictArray[i] = self.newClusterDictArray[i]
            if len(self.clusterDictArray[i]) > 0:
                self.centroides[i] = newCentroides[i]        
        
        if self.nbChangements == 0:
            self.stable = True


        


    def dict_compare(self, d1, d2):
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        removed = d2_keys - d1_keys
        return len(removed)

    def __leastSquares(self, motA, motB):  # motA & motB = type np.array(1,y)
        return np.sum(np.square(motA - motB))