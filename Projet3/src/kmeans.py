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
        self.clustersData = [] # garder les scores pour l'affichage
        self.iteration = 0
        self.nbChangements = 0
        self.nbMots = int(nbMots)
        self.nbCentroides = int(nbCentroides)
        self.stable = False

    def initialize(self):
        self.tempsGlobal = time()
        self.tempsIteration = time()    
        self.clusters = []    
        self.clustersData = []
        indexCentroides = random.sample(range(0, len(self.motsUnique)), self.nbCentroides)
        
        for i in range(0, self.nbCentroides):          
            self.centroides.append(self.concMatrix[indexCentroides[i]])
            self.clusters.append({})
            self.clustersData.append([])       
    
        # Met chaque mot dans un cluster
        self.attribuerCluster(self.centroides, self.clusters)   

        #première initialisation - nb de changements = au nombre de mots
        self.nbChangements = len(self.motsUnique)

        self.printIteration()       
       

    
    def printIteration(self):      
        print("\n============================================================================")
        print(f'Itération {self.iteration}')
        print(f'{self.nbChangements} changements de cluster en {round((time() - self.tempsIteration), 2)} secondes.\n')
        for i in range(0, self.nbCentroides):
            print(f'Il y a {len(self.clusters[i])} points (mots) regroupés autour du centroïde no {i}')
        

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
        self.newClusters = []
               
        for cluster in self.clusters:
            cluster = np.array(list(cluster.values()))          
            self.clustersData.append([]) # pour affichage des scores seulement
            self.newClusters.append({}) # pour calcul des centroides
            newCentroides.append(np.average(cluster, axis=0))        
       
        self.attribuerCluster(newCentroides, self.newClusters)

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
            #calculer les changements
            if self.clusters[i].keys() != self.newClusters[i].keys():                   
                self.nbChangements += self.dict_compare(self.clusters[i], self.newClusters[i])

            # remplacer les anciens clusters et centroides par les nouveaux
            self.clusters[i] = self.newClusters[i]
            if len(self.clusters[i]) > 0:
                self.centroides[i] = newCentroides[i]        
        
        if self.nbChangements == 0:
            self.stable = True


        

    # return le nombre d'élément enlevé seulement, ne tiens pas en compte les éléments ajoutés dans un cluster
    def dict_compare(self, d1, d2):
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        removed = d2_keys - d1_keys
        return len(removed)

    def __leastSquares(self, motA, motB):  # motA & motB = type np.array(1,y)
        return np.sum(np.square(motA - motB))