import math

def verification_condition_sudoku(dimension: int, grille: list[list[int]], coord: tuple[int, int]):
    liste_cases_invalides = []

    ligne = coord[0]
    colonne = coord[1]
    valeur = grille[ligne][colonne]

    liste_indices_lignes = [i for i in range(dimension)]
    liste_indices_lignes.remove(ligne)

    for i in liste_indices_lignes:
        if grille[i][colonne] == valeur:
            liste_cases_invalides.append((i, colonne))


    liste_indices_colonnes = [i for i in range(dimension)]
    liste_indices_colonnes.remove(colonne)

    for i in liste_indices_colonnes:
        if grille[ligne][i] == valeur:
            liste_cases_invalides.append((ligne, i))


    taille_bloc = int(math.sqrt(dimension))

    debut_ligne = (ligne // taille_bloc) * taille_bloc
    debut_colonne = (colonne // taille_bloc) * taille_bloc

    for i in range(debut_ligne, debut_ligne + taille_bloc):
        for j in range(debut_colonne, debut_colonne + taille_bloc):
            if (i, j) != coord and grille[i][j] == valeur:
                liste_cases_invalides.append((i, j))

    return liste_cases_invalides


a = verification_condition_sudoku(9, [[0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 2, 0, 0, 0, 4, 0, 0, 0], [0, 6, 5, 0, 0, 0, 4, 0, 5], [0, 7, 0, 1, 0, 0, 0, 0, 0], [6, 4, 2, 0, 0, 0, 0, 0, 9], [0, 0, 5, 0, 0, 0, 8, 0, 0], [3, 0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 6, 0, 9, 0, 1, 0], [0, 0, 9, 3, 4, 0, 0, 6, 0]], (2, 2))
print(a)