def afficher_contraintes_classique(coord):
    """Fonction qui affiche les cases sur lesquelles portent les contraintes, en fonction de la case sélectionnée.
    
    Entrée:
        Coordonées de la case venant d'être séléctionnée.
    Sortie:
        liste des cases sur lesquelles portent les contraintes."""
    
    affichage_cases = []

    ligne, colonne = coord

    for i in range(9):       # On ajoute à la liste des cases à afficher la ligne de la case sélectionnée
        affichage_cases.append((ligne, i))    

    for i in range(9):       # On ajoute à la liste des cases à afficher la colonne de la case sélectionnée
        affichage_cases.append((i,colonne))
    
    debut_ligne = (ligne // 3) * 3
    debut_col = (colonne // 3) * 3
    for i in range(3):       # On ajoute à la liste des cases à afficher le carré dans lequel se trouve la case en question
        for j in range(3):
            affichage_cases.append(debut_ligne + i, debut_col + j)
    
    affichage_cases = set(affichage_cases)  # On supprime les répétitions dans la liste gràce à un set.
    affichage_cases = list(affichage_cases)
    return affichage_cases

def afficher_contraintes_consecutif(coord, liste_doublons):
    """Fonction qui affiche les coordonnées des cases sur lesquelles portent lew contraintes du jeu en fonction
    de la case sélectionnée.
    
    Entrée:
        Coordonnées de la case venant d'être sélecionnée, liste des doublons de cases consécutives.
    Sortie:
        Liste des coordonnées des cases à mettre en évidence"""
    
    affichage_cases = []

    ligne, colonne = coord

    for i in range(9):       # On ajoute à la liste des cases à afficher la ligne de la case sélectionnée
        affichage_cases.append((ligne, i))    

    for i in range(9):       # On ajoute à la liste des cases à afficher la colonne de la case sélectionnée
        affichage_cases.append((i,colonne))
    
    debut_ligne = (ligne // 3) * 3
    debut_col = (colonne // 3) * 3
    for i in range(3):       # On ajoute à la liste des cases à afficher le carré dans lequel se trouve la case en question
        for j in range(3):
            affichage_cases.append(debut_ligne + i, debut_col + j)
    
    for i in liste_doublons: # On recherche si la case fait partie d'un doublon consécutif
        if coord in i:
            doublon = i
    
    if doublon[0] == coord:  # Si oui on ajoute à la liste des cases à afficher la deuxième case du doublon.
        affichage_cases.appenddoublon[1]
    elif doublon[1] == coord:
        affichage_cases.append(doublon[0])
    
    affichage_cases = set(affichage_cases)  # On supprime les répétitions dans la liste gràce à un set.
    affichage_cases = list(affichage_cases)
    return affichage_cases


def afficher_contraintes_Kenken(coord, dictionnaire_cages):
    """Fonction qui affiche les coordonnées des cases sur lesquelles portent lew contraintes du jeu en fonction
    de la case sélectionnée.
    
    Entrée:
        Coordonnées de la case venant d'être sélecionnée, dictionnaire contenant les informations des cages.
    Sortie:
        Liste des coordonnées des cases à mettre en évidence"""
    
    affichage_cases = []

    ligne, colonne = coord

    for i in range(9):       # On ajoute à la liste des cases à afficher la ligne de la case sélectionnée
        affichage_cases.append((ligne, i))    

    for i in range(9):       # On ajoute à la liste des cases à afficher la colonne de la case sélectionnée
        affichage_cases.append((i,colonne))
    
    debut_ligne = (ligne // 3) * 3
    debut_col = (colonne // 3) * 3
    for i in range(3):       # On ajoute à la liste des cases à afficher le carré dans lequel se trouve la case en question
        for j in range(3):
            affichage_cases.append(debut_ligne + i, debut_col + j)

    for cage in dictionnaire_cages.values():   # On cherche la cage dans laquelle se trouve la case sélectionnée
        if coord in cage["cases"]:
            a = cage["cases"]
    
    for i in a:     # On ajoute toutes les cases de cette case à la liste des cases à mettre en évidence
        affichage_cases.append(i)
    
    affichage_cases = set(affichage_cases)  # On supprime les répétitions dans la liste gràce à un set.
    affichage_cases = list(affichage_cases)
    return affichage_cases 



def affichage_contraintes_Windoku(coord):
    """Fonction qui affiche les cases sur lesquelles portent les contraintes, en fonction de la case sélectionnée.
    
    Entrée:
        Coordonées de la case venant d'être séléctionnée.
    Sortie:
        liste des cases sur lesquelles portent les contraintes."""
    
        
    affichage_cases = []

    ligne, colonne = coord

    for i in range(9):       # On ajoute à la liste des cases à afficher la ligne de la case sélectionnée
        affichage_cases.append((ligne, i))    

    for i in range(9):       # On ajoute à la liste des cases à afficher la colonne de la case sélectionnée
        affichage_cases.append((i,colonne))
    
    debut_ligne = (ligne // 3) * 3
    debut_col = (colonne // 3) * 3
    for i in range(3):       # On ajoute à la liste des cases à afficher le carré dans lequel se trouve la case en question
        for j in range(3):
            affichage_cases.append(debut_ligne + i, debut_col + j)

  
    premier_carré = [(i, j) for i in range(1, 4) for j in range(1, 4)],      # fenêtre 1 (haut-gauche)
    deuxieme_carré = [(i, j) for i in range(1, 4) for j in range(5, 8)],     # fenêtre 2 (haut-droite)
    troisième_carré = [(i, j) for i in range(5, 8) for j in range(1, 4)],     # fenêtre 3 (bas-gauche)
    quatrième_carré = [(i, j) for i in range(5, 8) for j in range(5, 8)]      # fenêtre 4 (bas-droite)

    tous_les_carrés = [premier_carré, deuxieme_carré, troisième_carré, quatrième_carré]

    def récupérer_informations_carré(i, j):   # On regarde si la case sélectionnée se trouve dans un des carrés en plus du windoku
        for carré in tous_les_carrés:
            if (i, j) in carré:
                return carré         # Si oui on renvoie le carré
        return 0  # la case n'est dans aucun des carrés
    
    récupération = récupérer_informations_carré(ligne, colonne)

    if récupération == 0:     
        affichage_cases = set(affichage_cases)  # On supprime les répétitions dans la liste gràce à un set.
        affichage_cases = list(affichage_cases)
        return affichage_cases
    
    else:                                  # On ajoute à la liste les nouvelles cases trouvées.
        for i in récupération:
            affichage_cases.append(i)

    affichage_cases = set(affichage_cases)  # On supprime les répétitions dans la liste gràce à un set.
    affichage_cases = list(affichage_cases)

    return affichage_cases



def afficher_contraintes_kakuro(grille_indices, r, c):
    """Trouve les cases appartenant aux cages H et V de la cellule (r, c)."""
    taille = len(grille_indices)
    
    # Cage Horizontale
    c_start = c
    while c_start >= 0 and not isinstance(grille_indices[r][c_start], list):
        c_start -= 1
    # L'indice est à (r, c_start). Les cases blanches commencent à c_start + 1
    c_end = c
    while c_end < taille and not isinstance(grille_indices[r][c_end], list):
        c_end += 1
    segment_h = [(r, i) for i in range(c_start + 1, c_end)]
    indice_h = grille_indices[r][c_start][0] # La somme attendue en ligne

    # Cage Verticale
    r_start = r
    while r_start >= 0 and not isinstance(grille_indices[r_start][c], list):
        r_start -= 1
    # L'indice est à (r_start, c). Les cases blanches commencent à r_start + 1
    r_end = r
    while r_end < taille and not isinstance(grille_indices[r_end][c], list):
        r_end += 1
    segment_v = [(i, c) for i in range(r_start + 1, r_end)]
    indice_v = grille_indices[r_start][c][1] # La somme attendue en colonne

    return {
        'h': {'cases': segment_h, 'cible': indice_h},
        'v': {'cases': segment_v, 'cible': indice_v}
    }
