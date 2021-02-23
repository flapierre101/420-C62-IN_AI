import re
import numpy as np
import math

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    count = {}
    i = 0
    list_mots = re.findall('\w+', open('../textes/PetitMousquetaire.txt', 'r', encoding="UTF-8").read())
    list_mots = [x.lower() for x in list_mots]
    for mot in list_mots:
        if mot in count:
            pass
        else:
            count[mot] = i
            i += 1

    print(count)

    a = np.zeros((len(count), len(count)))

    print(a)
    print(list_mots[1])

    tailleF = 15
    moitieF = math.floor(tailleF / 2)
    for i in range(len(list_mots)):
        for j in range(tailleF):
            pass

    # exemple fenetre de 5 hardcodé
    for i in range(len(list_mots)):
        if i == 0:
            indexMotCentral = count[list_mots[i]]
            a[indexMotCentral][count[list_mots[i+1]]] += 1
            a[indexMotCentral][count[list_mots[i+2]]] += 1
        elif i == 1:
            indexMotCentral = count[list_mots[i]]
            a[indexMotCentral][count[list_mots[i + 1]]] += 1
            a[indexMotCentral][count[list_mots[i + 2]]] += 1
            a[indexMotCentral][count[list_mots[i - 1]]] += 1
        elif i == len(list_mots)-2:
            indexMotCentral = count[list_mots[i]]
            a[indexMotCentral][count[list_mots[i + 1]]] += 1
            a[indexMotCentral][count[list_mots[i - 2]]] += 1
            a[indexMotCentral][count[list_mots[i - 1]]] += 1
        elif i == len(list_mots) - 1:
            indexMotCentral = count[list_mots[i]]
            a[indexMotCentral][count[list_mots[i - 1]]] += 1
            a[indexMotCentral][count[list_mots[i - 2]]] += 1
        else:
            indexMotCentral = count[list_mots[i]]
            a[indexMotCentral][count[list_mots[i + 1]]] += 1
            a[indexMotCentral][count[list_mots[i + 2]]] += 1
            a[indexMotCentral][count[list_mots[i - 1]]] += 1
            a[indexMotCentral][count[list_mots[i - 2]]] += 1

















