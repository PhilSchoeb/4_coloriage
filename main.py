# 4-coloriage du graphe du devoir 5 #4 c) IFT3655 avec la méthode de Gibbs, balayage systématique

import numpy as np
import matplotlib.pyplot as plt
import math
from random import random

n = 216000  # nombre d'itérations
k = 4  # nombre de couleurs
col = [0, 1, 2, 3]  # couleurs
color_counts = {}  # dictionnaire qui garde les comptes des coloriages


# Pour le coloriage, les couleurs vont de 0 à k-1 et soit m sommets, les sommets sont numérotés de 0 à m-1.
class Coloriage:
    def __init__(self, col0, col1, col2, col3, col4):
        self.col0 = col0
        self.col1 = col1
        self.col2 = col2
        self.col3 = col3
        self.col4 = col4

    def __eq__(self, other):
        return self.col0 == other.col0 and self.col1 == other.col1 and self.col2 == other.col2 and self.col3 == \
            other.col3 and self.col4 == other.col4

    def __hash__(self):
        h = self.col0.__hash__() + self.col1.__hash__() + self.col2.__hash__() + self.col3.__hash__() + \
            self.col4.__hash__()
        return h

    def __str__(self):
        return str(self.col0) + "_" + str(self.col1) + "_" + str(self.col2) + "_" + str(self.col3) + "_" + \
            str(self.col4)

    def modif(self, sommet, new_col):
        if sommet == 0:
            self.col0 = new_col
        elif sommet == 1:
            self.col1 = new_col
        elif sommet == 2:
            self.col2 = new_col
        elif sommet == 3:
            self.col3 = new_col
        else:
            self.col4 = new_col

    def get_possible_col(self, sommet):
        possible_col = col.copy()
        if sommet == 0:
            if self.col1 in possible_col:
                possible_col.remove(self.col1)
        elif sommet == 1:
            if self.col0 in possible_col:
                possible_col.remove(self.col0)
            if self.col2 in possible_col:
                possible_col.remove(self.col2)
            if self.col4 in possible_col:
                possible_col.remove(self.col4)
        elif sommet == 2:
            if self.col1 in possible_col:
                possible_col.remove(self.col1)
            if self.col4 in possible_col:
                possible_col.remove(self.col4)
        elif sommet == 3:
            if self.col4 in possible_col:
                possible_col.remove(self.col4)
        else:
            if self.col1 in possible_col:
                possible_col.remove(self.col1)
            if self.col2 in possible_col:
                possible_col.remove(self.col2)
            if self.col3 in possible_col:
                possible_col.remove(self.col3)
        return possible_col

    def test_color(self):
        if self.col0 == self.col1:
            return False
        if self.col1 == self.col2 or self.col1 == self.col4:
            return False
        if self.col2 == self.col4:
            return False
        if self.col3 == self.col4:
            return False
        return True


first_color = Coloriage(0, 1, 0, 0, 2)  # coloriage accepté


def gibbs_bs():
    global color_counts
    color = first_color
    num_pos_test = 0
    for i in range(n):
        # Augmenter le compte du coloriage présent de 1.
        if color_counts.get(color):
            count = color_counts.get(color)
        else:
            count = 0
        color_counts.update({color: count + 1})

        # Tester si le coloriage est accepté
        if color.test_color():
            num_pos_test += 1

        # Changer de coloriage, balayage systématique
        cols = [color.col0, color.col1, color.col2, color.col3, color.col4]
        for j in range(5):
            possible_col = color.get_possible_col(j)
            nb_col = len(possible_col)
            new_col_index = math.floor(random() * nb_col)
            new_col = possible_col[new_col_index]
            cols[j] = new_col
            color = Coloriage(cols[0], cols[1], cols[2], cols[3], cols[4])
    acception_rate = float(num_pos_test) / n
    print("Acception rate : " + str(acception_rate))


gibbs_bs()
print(len(color_counts))


def get_counts():
    ys = []
    for key in color_counts:
        y = color_counts.get(key)
        ys.append(y)
    return ys


# Visualisation
x = np.arange(0, 216, 1)
y = get_counts()
plt.scatter(x, y)
plt.xlabel("Différents coloriages")
plt.ylabel("Comptes des coloriages")
plt.title("Nombre de fois que chaque coloriage est obtenu")
#plt.savefig("color.png")
plt.show()


# Test Chi-deux
def chi_deux(counts):
    sum = 0
    for y in counts:
        sum += ((y - 1000) ** 2) / 1000
    return sum


chi2 = chi_deux(y)
print(chi2)

# Pour calculer la p-valeur j'ai utilisé les deux sites suivants :
# https://www.graphpad.com/quickcalcs/pValue2/
# https://www.socscistatistics.com/pvalues/chidistribution.aspx
