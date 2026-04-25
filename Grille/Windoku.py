import math
import copy
import random

def compter_solution_V3(grille : list[list:int], dimension : int, limite : int = 2):
    liste_ligne = [[True] * dimension for _ in range(dimension)]
    liste_colonne = [[True] * dimension for _ in range(dimension)]
    liste_carre = [[True] * dimension for _ in range(dimension)]
    
    # Dico pour les 4 fenêtres Windoku
    fenetres = {(1, 1): [True]*9, (1, 5): [True]*9, (5, 1): [True]*9, (5, 5): [True]*9}
    
    racine = int(math.sqrt(dimension))
    essaie = []
    compteur_de_solution = 0

    for ligne in range(dimension):
        for colonne in range(dimension):
            valeur = grille[ligne][colonne]
            if valeur == 0:
                essaie.append((ligne,colonne))
            else:
                idx_v = valeur - 1
                liste_ligne[ligne][idx_v] = False
                liste_colonne[colonne][idx_v] = False
                liste_carre[(ligne // racine) * racine + (colonne // racine)][idx_v] = False
                # Maj dico fenêtres
                for (rf, cf) in fenetres:
                    if rf <= ligne < rf + 3 and cf <= colonne < cf + 3:
                        fenetres[(rf, cf)][idx_v] = False

    def solveur():
        nonlocal compteur_de_solution
        if compteur_de_solution >= limite: return
        if not essaie:
            compteur_de_solution += 1
            return

        indice_min = -1
        valeurs_possibles_min = []
        nb_valeurs_min = dimension + 1

        for idx, (l, c) in enumerate(essaie):
            num_c = (l // racine) * racine + (c // racine)
            
            v_possibles = []
            for i in range(dimension):
                # On vérifie la condition standard
                if liste_ligne[l][i] and liste_colonne[c][i] and liste_carre[num_c][i]:
                    # On vérifie si la case est dans une fenêtre Windoku
                    dans_fenetre_et_valide = True
                    for (rf, cf) in fenetres:
                        if rf <= l < rf + 3 and cf <= c < cf + 3:
                            if not fenetres[(rf, cf)][i]:
                                dans_fenetre_et_valide = False
                    
                    if dans_fenetre_et_valide:
                        v_possibles.append(i)
            
            if len(v_possibles) < nb_valeurs_min:
                nb_valeurs_min, valeurs_possibles_min, indice_min = len(v_possibles), v_possibles, idx
            if nb_valeurs_min == 1: break

        if nb_valeurs_min == 0: return

        l, c = essaie.pop(indice_min)
        num_c = (l // racine) * racine + (c // racine)

        for i in valeurs_possibles_min:
            liste_ligne[l][i] = liste_colonne[c][i] = liste_carre[num_c][i] = False
            # Backtrack fenêtres
            for (rf, cf) in fenetres:
                if rf <= l < rf + 3 and cf <= c < cf + 3:
                    fenetres[(rf, cf)][i] = False
            
            solveur()
            
            liste_ligne[l][i] = liste_colonne[c][i] = liste_carre[num_c][i] = True
            for (rf, cf) in fenetres:
                if rf <= l < rf + 3 and cf <= c < cf + 3:
                    fenetres[(rf, cf)][i] = True
            
            if compteur_de_solution >= limite: break

        essaie.insert(indice_min, (l, c))

    solveur()
    return compteur_de_solution

def remplir_grille_V2(dimension : int):
    racine = int(math.sqrt(dimension))
    grille = [[0] * dimension for i in range(dimension)]
    liste_ligne = [[True]*dimension for _ in range(dimension)]
    liste_colonne = [[True]*dimension for _ in range(dimension)]
    liste_carre = [[True]*dimension for _ in range(dimension)]
    fenetres = {(1, 1): [True]*9, (1, 5): [True]*9, (5, 1): [True]*9, (5, 5): [True]*9}

    essaie = [(i,e) for i in range(dimension) for e in range(dimension)]

    def solveur():
        if not essaie: return True

        indice_min = -1
        v_possibles_min = []
        nb_valeurs_min = dimension + 1

        for idx, (l, c) in enumerate(essaie):
            num_c = (l//racine)*racine + (c//racine)
            
            candidats = []
            for v in range(dimension):
                if liste_ligne[l][v] and liste_colonne[c][v] and liste_carre[num_c][v]:
                    valide = True
                    for (rf, cf) in fenetres:
                        if rf <= l < rf + 3 and cf <= c < cf + 3:
                            if not fenetres[(rf, cf)][v]:
                                valide = False
                    if valide: candidats.append(v)

            if len(candidats) < nb_valeurs_min:
                nb_valeurs_min, v_possibles_min, indice_min = len(candidats), candidats, idx
            if nb_valeurs_min == 1: break

        if nb_valeurs_min == 0 or indice_min == -1: return False

        l, c = essaie.pop(indice_min)
        num_c = (l//racine)*racine + (c//racine)
        random.shuffle(v_possibles_min)

        for i in v_possibles_min:
            grille[l][c] = i + 1
            liste_ligne[l][i] = liste_colonne[c][i] = liste_carre[num_c][i] = False
            for (rf, cf) in fenetres:
                if rf <= l < rf + 3 and cf <= c < cf + 3:
                    fenetres[(rf, cf)][i] = False
            
            if solveur(): return True
            
            grille[l][c] = 0
            liste_ligne[l][i] = liste_colonne[c][i] = liste_carre[num_c][i] = True
            for (rf, cf) in fenetres:
                if rf <= l < rf + 3 and cf <= c < cf + 3:
                    fenetres[(rf, cf)][i] = True

        essaie.insert(indice_min, (l, c))
        return False

    return grille if solveur() else None
        
def supprimer_valeur(nombre_valeur_a_supprimer : int, dimension : int):
    grille_complete = remplir_grille_V2(dimension)
    grille_vidée = copy.deepcopy(grille_complete)
    positions = [(ligne, colonne) for ligne in range(dimension) for colonne in range(dimension)]
    random.shuffle(positions)

    nombre_case_supprime = 0
    while nombre_case_supprime < nombre_valeur_a_supprimer:
        if not positions:
            if (nombre_valeur_a_supprimer - nombre_case_supprime) > 5:   
                return supprimer_valeur(nombre_valeur_a_supprimer, dimension)
            else:
                return grille_vidée

        ligne, colonne = positions.pop()
        valeur_originale = grille_vidée[ligne][colonne]
        grille_vidée[ligne][colonne] = 0

        if compter_solution_V3(grille_vidée, dimension) == 1:
            nombre_case_supprime += 1
        else:
            grille_vidée[ligne][colonne] = valeur_originale

    return grille_vidée




