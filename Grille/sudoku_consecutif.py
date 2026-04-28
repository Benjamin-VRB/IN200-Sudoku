import random
import copy
import sudoku as Sudoku


def supprimer_valeur(grille_complete, nombre_valeur_a_supprimer: int, dimension: int):
    """
    Transforme notre grille pleine en un sudoku à remplir.
    Tout en s'assurant que le joueur n'aura toujours qu'une seule solution possible.

    Entrée : 
        nombre_valeurs_a_supprimer: Le nombre de cases que l'on veut vider.
        dimension : taille de notre grille
    Sortie : 
        grille_vidée : Une grille de Sudoku prête à être resolue par l'utilisateur
        grille_complete : La solution complète associée"""
    
    grille_vidée = copy.deepcopy(grille_complete)   # On copie la grille complète pour ne pas la modifier directement
    positions = [(ligne, colonne) for ligne in range(dimension) for colonne in range(dimension)]   # création d'une liste de toutes les positions possibles de la grille
    random.shuffle(positions)   # On mélange les positions pour supprimer aléatoirement

    nombre_case_supprime = 0   # initialisation d'un compteur du nombre de cases supprimées

    while nombre_case_supprime < nombre_valeur_a_supprimer:   # Tant qu'on n'a pas supprimé assez de valeurs
        if not positions:   # Si on a testé toutes les positions possibles
            if (nombre_valeur_a_supprimer - nombre_case_supprime) > 5:   
                return supprimer_valeur(grille_complete, nombre_valeur_a_supprimer, dimension)   # On recommence avec une nouvelle tentative (même grille)
            else:
                return grille_vidée, grille_complete   # Sinon on retourne ce qu'on a réussi à faire

        ligne, colonne = positions.pop()   # On prend une position au hasard (et on l'enlève de la liste)
        valeur_originale = grille_vidée[ligne][colonne]   # On sauvegarde la valeur pour pouvoir la remettre si besoin
        grille_vidée[ligne][colonne] = 0   # On supprime la valeur (case vide)

        if Sudoku.compter_solution_V3(grille_vidée, dimension) == 1:   # On vérifie qu'il n'y a qu'une seule solution
            nombre_case_supprime += 1   # Si oui, on valide la suppression
        else:
            grille_vidée[ligne][colonne] = valeur_originale   # Sinon on remet la valeur (suppression refusée)

    return grille_vidée, grille_complete   # On retourne la grille vidée + la solution complète








def generer_sudoku_consecutive(dimension=9):
    """Cette fonction crée une grille de sudoku_consecutif
    
    Entrée:
        Dimension de la grille à générer
    Sortie:
        La grille de Sudoku, la grille vidée et la liste des tuples qui contiennent les coordonnées des 
        cases adjacentes à mettre en valeur."""    

    grille_complete = Sudoku.remplir_grille_V2(dimension)
    
    duos = []
    for i in range(dimension):        # Création d'une liste qui va enregistrer toutes les cass adjacentes.
        for j in range(dimension):

            if j < dimension - 1:           # On enregistre la case de droite
                duos.append(((i, j), (i, j + 1)))       
            if i < dimension - 1:           # On enregistre la case du bas
                duos.append(((i, j), (i + 1, j)))

    duos_consecutifs = []

    for (i1, j1), (i2, j2) in duos:
        if abs(grille_complete[i1][j1] - grille_complete[i2][j2]) == 1:
            duos_consecutifs.append(((i1, j1), (i2, j2)))             # Si on a deux cases consécutives qui contiennent deux chiffres consecutifs on l'enregistre das la liste prévue a cet effet.
    
    grille_vidée, grille_complete = supprimer_valeur(grille_complete, 60, dimension)         # On supprime les valeurs de la grille pour avoir la version finales.

    return grille_complete, grille_vidée, duos_consecutifs


## Pour utiliser ce fichier, il faut appeller:
##                    print(generer_sudoku_consecutive(9))