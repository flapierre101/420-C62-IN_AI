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