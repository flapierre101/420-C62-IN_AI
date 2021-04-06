import numpy as np
import re
from connexionDB import *


class Recherche:

    def __init__(self, searchWord, method):
        self.predictMethod = {0: self.__produitScalaire,
                              1: self.__leastSquares, 2: self.__cityBlock}
        self.methodInt = method
        self.connexion = ConnexionDB()
        self.leMot = searchWord
        self.wordDict = self.connexion.get_words()
        self.stopWord = []
        self.concMatrix = self.connexion.get_cooc_mat(len(self.wordDict))
        self.prelimResult = []
        self.method = self.predictMethod[method]

    def operation(self):
        self.__verif()
        self.__getStopWord()
        for mot, value in self.wordDict.items():
            if mot != self.leMot and mot not in self.stopWord:
                tempo = self.method(self.motArray, self.concMatrix[value])
                self.prelimResult.append((mot, tempo))
        # scalaire décroissant - reste croissant
        if self.methodInt == 0:
            # lambda x: x[1] :Trier selon l'index [1] du tuple, soit les scores.
            return sorted(self.prelimResult, reverse=True, key=lambda x: x[1])
        else:
            return sorted(self.prelimResult,  key=lambda x: x[1])

    def __getStopWord(self):
        self.stopWord = re.findall(
            '\w+', open('..\src\stop_words.py', 'r', encoding="UTF-8").read())

    def __verif(self):
        if self.leMot not in self.wordDict:
            print("Ce mot n'est pas présent dans la liste")
            return -1
        else:
            self.index = self.wordDict[self.leMot]
            self.motArray = self.concMatrix[self.index]

    def __produitScalaire(self, motA, motB):
        return np.sum(motA * motB)

    def __leastSquares(self, motA, motB):  # motA & motB = type np.array(1,y)
        return np.sum(np.square(motA - motB))

    def __cityBlock(self, motA, motB):
        # donne le city-block entre 2 mots
        return np.sum(np.absolute(motA - motB))
