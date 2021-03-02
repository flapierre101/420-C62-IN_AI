import numpy as np
import re

from numpy.core.fromnumeric import sort

class Recherche:

    def __init__(self, wordDict, concMatrix, searchWord, method):
        self.predictMethod = {0:self.produitScalaire, 1:self.leastSquares, 2:self.cityBlock}
        self.methodInt = method
        self.leMot = searchWord
        self.wordDict = wordDict
        self.stopWord = []
        self.concMatrix = concMatrix
        self.prelimResult = []
        self.method = self.predictMethod[method]


    def operation (self):
        self.verif()
        self.getStopWord()
        self.method()
        #scalaire décroissant - reste croissant

        for key,value in self.wordDict.items():
            if key != self.leMot:
                tempo = self.method(self.leMot, value)
                self.prelimResult.append((key, tempo))
        if self.methodInt == 0:
            return sorted(self.prelimResult, reverse=True)
        else:
            return sorted(self.prelimResult)

    def getStopWord(self):
        self.stopWord = re.findall('\w+', open('..\src\stop_words.py', 'r', encoding="UTF-8").read())

    def verif (self):
        if self.leMot not in self.wordDict:
            print("Ce mot n'est pas présent dans la liste")
            return -1
        else:
            self.index = self.wordDict[self.leMot]
            self.motArray = self.concMatrix[self.index]

    def produitScalaire(self, motA, motB):
        return np.sum(motA * motB)


    def leastSquares(self, motA, motB):  # motA & motB = type np.array(1,y)
        return np.sum(np.square(motA - motB))

    def cityBlock(self, motA, motB):
        # donne le city-block entre 2 mots
        return np.sum(np.absolute(motA - motB))

    def sortResult(self):
        return sorted(self.prelimResult, key=1)
