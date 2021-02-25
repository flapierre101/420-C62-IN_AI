import re
import numpy as np
import math

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    motUnique = {}
    i = 0
    list_mots = re.findall('\w+', open('../textes/PetitMousquetaire.txt', 'r', encoding="UTF-8").read())
    list_mots = [x.lower() for x in list_mots]
    for mot in list_mots:
        if mot in motUnique:
            pass
        else:
            motUnique[mot] = i
            i += 1

    print(motUnique)

    b = np.zeros((len(motUnique), len(motUnique)))

    print(list_mots[1])









    # Version courte ! B
    tailleF = 9
    moitieF = tailleF // 2
    for i in range(len(list_mots)):
        motCentral = motUnique[list_mots[i]]
        for j in range(1, moitieF+1):
            if not i - j < 0 and motCentral != motUnique[list_mots[i - j]]:
                b[motCentral][motUnique[list_mots[i - j]]] += 1
            if not i + j >= len(list_mots) and motCentral != motUnique[list_mots[i + j]]:
                b[motCentral][motUnique[list_mots[i + j]]] += 1




    print("ici B")
    print(b)














