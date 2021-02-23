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
    b = np.zeros((len(count), len(count)))

    print(list_mots[1])






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


    # Version courte ! B
    tailleF = 5
    moitieF = math.floor(tailleF / 2)
    for i in range(len(list_mots)):
        motCentral = count[list_mots[i]]
        for j in range(1, moitieF+1):
            if not i - j < 0:
                b[motCentral][count[list_mots[i - j]]] += 1
            if not i + j >= len(list_mots):
                b[motCentral][count[list_mots[i + j]]] += 1



    print("ici A")

    print(a)
    print("ici B")
    print(b)














