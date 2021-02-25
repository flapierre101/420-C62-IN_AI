def produitScalaire(motA, motB):  # motA & motB = type np.array(1,y)
    # self.result = np.sum(motA * motB)
    return np.sum(motA * motB)


def leastSquares(motA, motB):  # motA & motB = type np.array(1,y)
    # donne le least square entre 2 mots
    # return np.sum(motA**2 - motB**2)
    return np.sum(np.square(motA) - np.square(motB))


def comparator(lq1, lq2):  # Entier resultat optenu de la methode leastSquare ou cityBlock
    # Compare les valeurs des least-squares et retoure le meilleur des 2(lowest)
    if lq1 < lq2:
        return lq1
    else:
        return lq2


def cityBlock(motA, motB):
    # donne le city-block entre 2 mots
    return np.sum(np.absolute(motA - motB))