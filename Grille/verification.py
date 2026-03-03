import math
from generation import trouver_groupes_horizontaux
from generation import trouver_groupes_verticaux

def compter_solution_V3(grille, dimension, limite = 2):
    
    # Booléens pour savoir si une valeur est utilisée
    liste_ligne = [[True] * dimension for _ in range(dimension)]
    liste_colonne = [[True] * dimension for _ in range(dimension)]
    liste_carre = [[True] * dimension for _ in range(dimension)]
    
    racine = int(math.sqrt(dimension))
    essaie = []  # liste des cases vides
    compteur_de_solution = 0

    # Initialisation
    for ligne in range(dimension):
        for colonne in range(dimension):
            valeur = grille[ligne][colonne]
            if valeur == 0:
                essaie.append((ligne,colonne))
            else:
                indice_valeur = valeur - 1
                liste_ligne[ligne][indice_valeur] = False
                liste_colonne[colonne][indice_valeur] = False
                liste_carre[(ligne // racine) * racine + (colonne // racine)][indice_valeur] = False

    def solveur():
        nonlocal compteur_de_solution

        if compteur_de_solution >= limite:
            return

        if not essaie:  # plus de case à remplir
            compteur_de_solution += 1
            return

        # MRV : choisir la case avec le moins de valeurs possibles
        indice_min = -1
        valeurs_possibles_min = []
        nb_valeurs_min = dimension + 1

        for idx, (ligne, colonne) in enumerate(essaie):
            numero_carre = (ligne // racine) * racine + (colonne // racine)
            
            valeurs_possibles = []

            for indice in range(dimension):
                if liste_ligne[ligne][indice] and liste_colonne[colonne][indice] and liste_carre[numero_carre][indice]:
                    valeurs_possibles.append(indice)
            
            nb_valeurs = len(valeurs_possibles)
            
            if nb_valeurs < nb_valeurs_min:
                nb_valeurs_min = nb_valeurs
                valeurs_possibles_min = valeurs_possibles
                indice_min = idx
            
            if nb_valeurs == 1:
                break  # optimisation

        if nb_valeurs_min == 0:
            return  # abandon

        # Retirer la case choisie
        ligne, colonne = essaie.pop(indice_min)
        numero_carre = (ligne // racine) * racine + (colonne // racine)

        for indice in valeurs_possibles_min:
            # Marquer la valeur comme utilisée
            liste_ligne[ligne][indice] = False
            liste_colonne[colonne][indice] = False
            liste_carre[numero_carre][indice] = False

            solveur()  # récursion

            # Backtracking
            liste_ligne[ligne][indice] = True
            liste_colonne[colonne][indice] = True
            liste_carre[numero_carre][indice] = True

            if compteur_de_solution >= limite:
                break

        # Réinsertion pour les appels supérieurs
        essaie.insert(indice_min, (ligne, colonne))

    solveur()
    return compteur_de_solution

def compter_solution_V2(grille, dimension, limite=2):
    ligne = [0] * dimension
    colonne = [0] * dimension
    carre = [0] * dimension
    essaie = []
    racine = int(math.sqrt(dimension))

    for i in range (dimension): # séparation des case remplie des case vide
        for e in range (dimension):
            valeur = grille[i][e]
            if valeur == 0:
                essaie.append((i, e))
            else :
                mask = 1 << (valeur - 1) # enregistrement de la valeur dans la ligne colonne et carre
                ligne[i] |= mask
                colonne[e] |= mask
                carre[(i // racine) * racine + (e // racine)] |= mask

    compteur_de_solution = 0

    def solve():
        nonlocal compteur_de_solution
        
        if compteur_de_solution >= limite: # on a donc au moins 2 solution, on arrete
            return
        
        if essaie == []: # si essaie vide, alors la grille est remplie, on à trouver une solution
            compteur_de_solution += 1
            return

        min_index = -1 
        min_mask = 0
        min_nombre_valeur_possible = dimension

        for h, (i, e) in enumerate(essaie): # enumeration de tout les couple h(indice dans la liste essaie) et des tuples (ligne, colonne)
            index_carre = (i // racine) * racine + (e // racine) # determination de l'indice du carre (de 0 a 8) (se représenter les carre et leur donner un numero de gauche à droite et de bas en haut
            bit_utilise = ligne[i] | colonne[e] | carre[index_carre] # determination des bit deja utilisé dans la ligne, colonne et carre de la valeur pour faire l'union des trois
            valeur_possible = (~bit_utilise) &  ((1 << dimension) - 1) # obtention de valeur possible par inversion de valeur interdite à valeur possible + limitation au 9 premier bits 
            nombre_de_valeur_possible = valeur_possible.bit_count() # compte le nombre de valeur possible

            if nombre_de_valeur_possible < min_nombre_valeur_possible: # recherche de la case avec le moins de valeur possible pour en retenir les infos
                min_nombre_valeur_possible = nombre_de_valeur_possible
                min_mask = valeur_possible
                min_index = h

            if nombre_de_valeur_possible == 1: # on arrete de cherche pour prendre le chemin
                break
        
        if min_nombre_valeur_possible == 0: # abandon du chemin
            return
        
        i, e = essaie.pop(min_index) # on retirer la case choisie de la liste des cases à essaiyer
        c = (i // racine) * racine + (e // racine)
        valeur_possible = min_mask # attribution comme valeur possible, celle déterminer plus tôt 
        
        while valeur_possible:  # boucle sur chaque valeur possible
            bit = valeur_possible & -valeur_possible # on prend le bit le plus faible
            valeur_possible ^= bit # on retire ce bit du masque 

            ligne[i] |= bit # Marquer le chiffre comme utilisé dans ligne, colonne et bloc
            colonne[e] |= bit
            carre[c] |= bit

            solve() # appel récursif pour remplir la prochaine case

            ligne[i] ^= bit  # annulation des choix (backtracking)
            colonne[e] ^= bit
            carre[c] ^= bit

            if compteur_de_solution >= limite: # stop si on atteint la limite
                break

        essaie.insert(min_index, (i, e))  # réinsertion de la case dans la liste pour les appels supérieurs

    solve() # début résolution récursive
    return compteur_de_solution # renvoie le nombre de solution trouvé

def est_valide(grille, ligne, colonne, valeur, dimension):
    if valeur in grille[ligne]: # Vérifie la ligne
        return False
    if any(grille[i][colonne] == valeur for i in range(dimension)):  # Vérifie la colonne
        return False
    ligne_0, colonne_0 = (ligne // int(math.sqrt(dimension))) * int(math.sqrt(dimension)), (colonne // int(math.sqrt(dimension))) * int(math.sqrt(dimension)) # Vérifie le carré 3x3
    return not any(grille[i][e] == valeur for i in range(ligne_0, ligne_0 + int(math.sqrt(dimension))) for e in range(colonne_0, colonne_0 + int(math.sqrt(dimension))))

def compter_solution_V1(grille, dimension, limite=2):
    compteur = [0] # Compte le nombre de solutions, s'arrête dès qu'on atteint la limite
    def resoudre():  
        if compteur[0] >= limite:
            return
        for i in range(dimension):
            for e in range(dimension):
                if grille[i][e] == 0:
                    for valeur in range(1, dimension + 1):
                        if est_valide(grille, i, e, valeur, dimension):
                            grille[i][e] = valeur
                            resoudre()
                            grille[i][e] = 0
                    return # case vide sans solution valide
        compteur[0] += 1 # grille complète trouvée
    resoudre()
    return compteur[0]

def compter_taille_groupe_horizontal(grille, ligne, colonne, dimension):
    # Compter à gauche
    taille = 0
    c = colonne - 1
    while c >= 0 and grille[ligne][c] == 0:
        taille += 1
        c -= 1

    # Compter à droite
    c = colonne + 1
    while c < dimension and grille[ligne][c] == 0:
        taille += 1
        c += 1

    # Si on coupe un groupe existant, il doit rester >= 2
    if taille == 1:
        return False

    return True

def compter_taille_groupe_horizontal(grille, ligne, colonne, dimension):
    taille = 0
    l = ligne - 1
    while l >= 0 and grille[l][colonne] == 0:
        taille += 1
        l -= 1

    l = ligne + 1
    while l < dimension and grille[l][colonne] == 0:
        taille += 1
        l += 1

    if taille == 1:
        return False

    return True

def compter_solution_kakuro(grille, dimension,
                            groupes_horizontaux, sommes_horizontales,
                            groupes_verticaux, sommes_verticales,
                            limite=2):

    max_val = dimension if dimension > 9 else 9

    # Disponibilité des valeurs par groupe
    dispo_h = [[True]*max_val for _ in range(len(groupes_horizontaux))]
    dispo_v = [[True]*max_val for _ in range(len(groupes_verticaux))]

    # Sommes partielles par groupe
    somme_actuelle_h = [0]*len(groupes_horizontaux)
    somme_actuelle_v = [0]*len(groupes_verticaux)

    # Mapping case -> groupe horizontal / vertical
    case_to_group = {}

    for i, groupe in enumerate(groupes_horizontaux):
        for (l,c) in groupe:
            case_to_group[(l,c)] = [i, None]

    for i, groupe in enumerate(groupes_verticaux):
        for (l,c) in groupe:
            case_to_group[(l,c)][1] = i

    # Liste des cases vides
    cases_vides = []
    for l in range(dimension):
        for c in range(dimension):
            if grille[l][c] == 0:
                cases_vides.append((l,c))
            else:
                val = grille[l][c]
                h, v = case_to_group[(l,c)]

                dispo_h[h][val-1] = False
                dispo_v[v][val-1] = False
                somme_actuelle_h[h] += val
                somme_actuelle_v[v] += val

    compteur = 0

    def solveur():
        nonlocal compteur

        if compteur >= limite:
            return

        if not cases_vides:
            compteur += 1
            return

        # MRV : choisir la case avec le moins de candidats
        meilleur_idx = -1
        meilleurs_valeurs = []
        min_possibilites = max_val + 1

        for idx, (l,c) in enumerate(cases_vides):
            h, v = case_to_group[(l,c)]
            candidats = []

            for val in range(1, max_val+1):
                if not dispo_h[h][val-1]:
                    continue
                if not dispo_v[v][val-1]:
                    continue

                # Vérification somme horizontale
                if somme_actuelle_h[h] + val > sommes_horizontales[h]:
                    continue

                # Vérification somme verticale
                if somme_actuelle_v[v] + val > sommes_verticales[v]:
                    continue

                candidats.append(val)

            if len(candidats) < min_possibilites:
                min_possibilites = len(candidats)
                meilleurs_valeurs = candidats
                meilleur_idx = idx

            if min_possibilites == 1:
                break

        if min_possibilites == 0:
            return

        l, c = cases_vides.pop(meilleur_idx)
        h, v = case_to_group[(l,c)]

        for val in meilleurs_valeurs:

            # Placement
            dispo_h[h][val-1] = False
            dispo_v[v][val-1] = False
            somme_actuelle_h[h] += val
            somme_actuelle_v[v] += val
            grille[l][c] = val

            # Vérification fin de groupe
            complet_h = all(grille[x][y] != 0 for (x,y) in groupes_horizontaux[h])
            complet_v = all(grille[x][y] != 0 for (x,y) in groupes_verticaux[v])

            valide = True
            if complet_h and somme_actuelle_h[h] != sommes_horizontales[h]:
                valide = False
            if complet_v and somme_actuelle_v[v] != sommes_verticales[v]:
                valide = False

            if valide:
                solveur()

            # Backtrack
            dispo_h[h][val-1] = True
            dispo_v[v][val-1] = True
            somme_actuelle_h[h] -= val
            somme_actuelle_v[v] -= val
            grille[l][c] = 0

            if compteur >= limite:
                break

        cases_vides.insert(meilleur_idx, (l,c))

    solveur()
    return compteur

def valider_masque(grille, dimension,):

    max_groupe = dimension

    groupes_h = trouver_groupes_horizontaux(grille, dimension)
    groupes_v = trouver_groupes_verticaux(grille, dimension)

    # Vérifier tailles des groupes
    for g in groupes_h:
        if len(g) < 2 or len(g) > max_groupe:
            return False

    for g in groupes_v:
        if len(g) < 2 or len(g) > max_groupe:
            return False

    # Vérifier que chaque case blanche appartient à 2 groupes
    compteur = [[0]*dimension for _ in range(dimension)]

    for g in groupes_h:
        for (l, c) in g:
            compteur[l][c] += 1

    for g in groupes_v:
        for (l, c) in g:
            compteur[l][c] += 1

    for l in range(dimension):
        for c in range(dimension):
            if grille[l][c] == 0:  # case blanche
                if compteur[l][c] != 2:
                    return False

    return True