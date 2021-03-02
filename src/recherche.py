import numpy as np
import re

class Recherche:
    def __init__(self, wordDict, concArray, searchWord, method):
        self.leMot = searchWord
        self.verif(searchWord)
        self.stopWord = []
        self.predictMethod = method
        self.wordDict = wordDict
        self.concArray = concArray
        self.prelimResult = []

    def getStopWord(self):
        self.stopWord = re.findall('\w+', open('..\src\stop_words.py', 'r', encoding="UTF-8").read())

    def verif (self, mot):
        if mot not in self.wordDict:
            print("Ce mot n'est pas présent dans la liste")
            return -1
        else:
            self.index = self.wordDict[mot]
            self.motArray = self.concArray[self.index]

    def produitScalaire(self):
        # self.result = np.sum(motA * motB)
        for wArray in self.concArray:
            tempo = np.sum(self.motArray * wArray)
            self.prelimresult.append((self.wordDict[self.leMot], tempo)) #le mot avec lequel le search word est comparer et sa valeur après calcul
        return self.prelimresult


    def leastSquares(motA, motB):  # motA & motB = type np.array(1,y)
        # donne le least square entre 2 mots
        # return np.sum(motA**2 - motB**2)
        # return np.sum(np.square(motA) - np.square(motB))
        return np.sum(np.square(motA - motB))

    def cityBlock(motA, motB):
        # donne le city-block entre 2 mots
        return np.sum(np.absolute(motA - motB))

    def sort(self):
        return sorted(self.prelimResult, key=1)
