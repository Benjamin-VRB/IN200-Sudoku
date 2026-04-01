import math

def verification_lignes_colonnes(grille: list[list[int]], coord: tuple[int, int], liste_cases_invalides):
    """"Vérifie que la valeur qui vient dêtre saisie vérifie les conditions lignes et colonnes du Sudoku.
    
    Entrée:
        La grille de sudoku, les coordonnées de la case venant d'ête remplie, et une liste (qui sera une liste vide). 
        par l'utilisateur."""
    
    dimension = len(grille)
    ligne = coord[0]
    colonne = coord[1]
    valeur = grille[ligne][colonne]

    liste_indices_lignes = [i for i in range(dimension)]   # Liste des indices des lignes a tester.
    liste_indices_lignes.remove(ligne)                     # à laquelle on enlève l'indice de la case venant d'être remplie.

    for i in liste_indices_lignes:
        if grille[i][colonne] == valeur:
            liste_cases_invalides.append((i, colonne))     # On regarde dans toute la ligne.


    liste_indices_colonnes = [i for i in range(dimension)]  # Liste des indices des colonnes a tester.
    liste_indices_colonnes.remove(colonne)                  # à laquelle on enlève l'indice de la case venant d'être remplie.

    for i in liste_indices_colonnes:
        if grille[ligne][i] == valeur:
            liste_cases_invalides.append((ligne, i))        # On regarde dans toute la colonne




def verification_carre_Sudoku(grille: list[list[int]], coord: tuple[int, int], liste_cases_invalides):
    """Vérifie que la valeur qui vient dêtre saisie vérifie la condition carré du Sudoku.
    
    Entrée:
        La grille de sudoku, les coordonnées de la case venant d'ête remplie, et une liste (qui sera une liste vide). 
        par l'utilisateur."""

    dimension = len(grille)
    liste_cases_invalides = []     

    ligne = coord[0]
    colonne = coord[1]
    valeur = grille[ligne][colonne]

    taille_bloc = int(math.sqrt(dimension))                 # calcul de la taille d'un carré

    debut_ligne = (ligne // taille_bloc) * taille_bloc          # On regarde dans quel bloc se trouve la case qu'on vient de remplir
    debut_colonne = (colonne // taille_bloc) * taille_bloc

    for i in range(debut_ligne, debut_ligne + taille_bloc):           # On teste toutes les cases de ce bloc.
        for j in range(debut_colonne, debut_colonne + taille_bloc):
            if (i, j) != coord and grille[i][j] == valeur:
                liste_cases_invalides.append((i, j))





def verification_sudoku_classique_complet(grille: list[list[int]], coord: tuple[int, int]):
    """"Vérifie que la valeur qui vient dêtre saisie vérifie toutes les conditions du Sudoku.
    
    Entrée:
        La grille de sudoku et  les coordonnées de la case venant d'ête remplie.
        
    Sortie:
        Renvoie la liste de toutes les cases pour lesquelles cette valeur ne fonctionne pas."""

    liste_cases_invalides = []
    verification_lignes_colonnes(grille, coord, liste_cases_invalides)
    verification_carre_Sudoku(grille, coord, liste_cases_invalides)
    return liste_cases_invalides

