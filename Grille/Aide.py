import random,math
import kenken as kenken
import sudoku_chaos as irregulier
import windoku as windoku
import sudoku as sudoku

def indicateur_sudoku(grille_joueur : list, grille_complete : list, dimension : int):
    """permet d'indiquer à l'utilisateur une case d'une grille de sudoku"""
    
    racine = int(math.sqrt(dimension))

    def obtenir_candidats(grille, lig, col):
        """Retourne la liste des chiffres possibles pour une case donnée."""
        candidats_possibles = []
        numero_carre = (lig // racine) * racine + (col // racine)
        
        for valeur in range(1, dimension + 1):
            valide = True
            
            # Vérification ligne
            if valeur in grille[lig]:
                valide = False
            
            # Vérification colonne
            if valide:
                for i in range(dimension):
                    if grille[i][col] == valeur:
                        valide = False
                        break
            
            # Vérification carré
            if valide:
                debut_lig = (lig // racine) * racine
                debut_col = (col // racine) * racine
                for i in range(debut_lig, debut_lig + racine):
                    for j in range(debut_col, debut_col + racine):
                        if grille[i][j] == valeur:
                            valide = False
                            break
                    if not valide: 
                        break
            
            if valide:
                candidats_possibles.append(valeur)
        return candidats_possibles

    # On cherche d'abord s'il y a une case avec un seul candidat
    coords = None
    nb_candidats_min = dimension + 1

    for lig in range(dimension):
        for col in range(dimension):
            if grille_joueur[lig][col] == 0:
                candidats_actuels = obtenir_candidats(grille_joueur, lig, col)
                
                # On choisit la case avec le moins de valeurs possibles
                if len(candidats_actuels) < nb_candidats_min:
                    nb_candidats_min = len(candidats_actuels)
                    coords = (lig, col)
                
                # Si une case n'a qu'une seule valeur possible, on s'arrête
                if len(candidats_actuels) == 1:
                    return grille_complete[lig][col], (lig, col)

    if not coords:
        return None, None

    # Si aucune case n'est évidente, on cherche la case qui devient évidente en regardant juste un coup plus loin
    for lig in range(dimension):
        for col in range(dimension):
            if grille_joueur[lig][col] == 0:
                candidats_actuels = obtenir_candidats(grille_joueur, lig, col)
                valides_apres_test = []
                
                for valeur in candidats_actuels:
                    # Test temporaire
                    grille_joueur[lig][col] = valeur
                    
                    # Si ce chiffre permet toujours de finir la grille on la garde
                    if sudoku.compter_solution_V3(grille_joueur, dimension, limite=1) == 1:
                        valides_apres_test.append(valeur)
                    
                    # On retire la valeur
                    grille_joueur[lig][col] = 0
                
                # Si apres on a qu'une seule valeur qui ne bloque pas la grille on la renvoie
                if len(valides_apres_test) == 1:
                    return grille_complete[lig][col], (lig, col)

    # En dernier recours, on donne simplement la solution de la case la plus contrainte
    lig, col = coords
    return grille_complete[lig][col], (lig, col)

def indicateur_kenken(grille_joueur : list, grille_complete : list, dictionnaire_cages : dict, dimension : int):
    """permet d'indiquer à l'utilisateur une case d'une grille de kenken"""

    def obtenir_candidats(grille, lig, col):
        """Retourne la liste des chiffres possibles pour une case donnée."""
        candidats_possibles = []
        
        # On identifie la cage à laquelle appartient la case 
        cage_actuelle = None
        for cage in dictionnaire_cages.values():
            if (lig, col) in cage["cases"]:
                cage_actuelle = cage
                break

        for valeur in range(1, dimension + 1):
            valide = True
            
            # Vérification ligne 
            if valeur in grille[lig]:
                valide = False
            
            # Vérification colonne 
            if valide:
                for i in range(dimension):
                    if grille[i][col] == valeur:
                        valide = False
                        break
            
            # Vérification de l'opération de la cage
            if valide and cage_actuelle:
                # On place temporairement la valeur pour tester la validité de la cage
                grille[lig][col] = valeur
                if not kenken.verifier_cage(grille, cage_actuelle):
                    valide = False
                # On remet à zéro 
                grille[lig][col] = 0
            
            if valide:
                candidats_possibles.append(valeur)
                
        return candidats_possibles

    # On cherche d'abord s'il y a une case avec un seul candidat
    coords = None
    candidats = [0] * (dimension + 1)

    for lig in range(dimension):
        for col in range(dimension):
            # On ne s'intéresse qu'aux cases vides
            if grille_joueur[lig][col] == 0:
                candidats_actuels = obtenir_candidats(grille_joueur, lig, col)
                
                # On cherche la case avec le minimum de candidats 
                if len(candidats_actuels) < len(candidats):
                    candidats = candidats_actuels
                    coords = (lig, col)
                
                # Si la case n'a qu'un seul choix on a fini
                if len(candidats_actuels) == 1: 
                    return grille_complete[lig][col], (lig, col)

    if not coords: 
        return None, None

    # Si aucune case n'est évidente, on cherche la case qui devient évidente en regardant juste un coup plus loin comme ses autres candidats sont devenus invalides
    for lig in range(dimension):
        for col in range(dimension):
            if grille_joueur[lig][col] == 0:
                candidats_actuels = obtenir_candidats(grille_joueur, lig, col)
                valides_apres_test = []
                
                for valeur in candidats_actuels:
                    # Test temporaire
                    grille_joueur[lig][col] = valeur
                    
                    # Si ce chiffre permet toujours de finir la grille on la garde alors 
                    if kenken.verifier_unicite_kenken(dimension, dictionnaire_cages, limite=1):
                        valides_apres_test.append(valeur)
                    
                    # On retire la valeur
                    grille_joueur[lig][col] = 0 
                
                # Si apres on a qu'une seule valeur qui ne bloque pas la grille on la renvoie
                if len(valides_apres_test) == 1:
                    return grille_complete[lig][col], (lig, col)

    # En dernier recours, on donne simplement la solution de la case la plus contrainte
    lig, col = coords
    return grille_complete[lig][col], (lig, col)

def indicateur_irregulier (grille_joueur : list, plan_cage : list, grille_complete : list):
    """permet d'indiquer à l'utilisateur une case à partir d'une grille d'un Sudoku Irregulier"""
    dimension = len(grille_joueur)
    l_u, c_u, cage_u = irregulier.initialiser_contraintes(grille_joueur, plan_cage, dimension)
    
    # On cherche d'abord s'il y a une case avec un seul candidat
    coords, candidats = irregulier.trouver_meilleure_case(grille_joueur, plan_cage, l_u, c_u, cage_u, dimension)
    
    # Dans le cas où la grille est déjà remplie
    if coords is None:
        return None, None
    
    l_meilleure, c_meilleure = coords

    if coords and len(candidats) == 1:
        return grille_complete[l_meilleure][c_meilleure],coords
    

    # Si aucune case n'est évidente, on cherche la case qui devient évidente en regardant juste un coup plus loin comme ses autres candidats sont devenus invalides
    for l in range(dimension):
        for c in range(dimension):
            if grille_joueur[l][c] == 0:
                num_cage = plan_cage[l][c]
                candidats_possibles = []
                
                # On cherche les candidats possibles pour l'instant
                for v in range(1, dimension + 1):
                    if v not in l_u[l] and v not in c_u[c] and v not in cage_u[num_cage]:
                        candidats_possibles.append(v)
                
                # Pour chaque candidat, on regarde si le placer bloque toute la grille plus loin
                candidats_valides = []
                for v in candidats_possibles:
                    # Test temporaire
                    grille_joueur[l][c] = v
                    l_temp, c_temp, cage_temp = irregulier.initialiser_contraintes(grille_joueur, plan_cage, dimension)
                    
                    # Si avec ce chiffre, la grille reste possible on le conserve
                    if irregulier.compter_solutions_irregulier(grille_joueur, plan_cage, l_temp, c_temp, cage_temp) > 0:
                        candidats_valides.append(v)
                    
                    # On remet à zéro
                    grille_joueur[l][c] = 0
                
                # Si après ce test au rang d'apres il ne reste qu'un seul candidat valide on le renvoie
                if len(candidats_valides) == 1:
                    return grille_complete[l][c],(l, c)

    # En dernier recours, on donne simplement la solution de la case la plus contrainte
    l,c = coords
    return grille_complete[l][c],(l,c)

# Irregulier : 
grille_complete = [[7, 6, 5, 1, 2, 8, 9, 3, 4], [5, 1, 3, 7, 9, 6, 4, 8, 2], [4, 8, 9, 2, 3, 7, 6, 5, 1], [6, 2, 7, 3, 1, 9, 5, 4, 8], [3, 4, 2, 6, 8, 5, 1, 7, 9], [9, 5, 1, 8, 4, 2, 3, 6, 7], [1, 9, 8, 4, 6, 3, 7, 2, 5], [8, 3, 4, 5, 7, 1, 2, 9, 6], [2, 7, 6, 9, 5, 4, 8, 1, 3]]
grille_joueur = [[7, 0, 0, 1, 0, 8, 9, 0, 0], [0, 0, 3, 7, 9, 6, 0, 0, 0], [0, 8, 9, 2, 0, 7, 0, 0, 0], [0, 0, 7, 0, 0, 9, 0, 0, 0], [3, 0, 0, 6, 0, 0, 1, 7, 0], [9, 5, 1, 8, 0, 2, 0, 0, 0], [1, 0, 0, 0, 0, 3, 7, 2, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 7, 0, 0, 5, 0, 0, 1, 0]]
plan_cage = [[1, 1, 2, 2, 2, 3, 3, 3, 3], [1, 1, 2, 2, 2, 2, 2, 2, 3], [1, 1, 1, 1, 1, 3, 3, 3, 3], [4, 4, 4, 5, 5, 5, 5, 5, 6], [7, 4, 5, 5, 5, 6, 6, 5, 6], [7, 4, 4, 8, 6, 6, 6, 6, 6], [7, 4, 4, 8, 8, 8, 9, 9, 9], [7, 4, 7, 7, 8, 8, 8, 9, 9], [7, 7, 7, 8, 8, 9, 9, 9, 9]]
print("indicateur Irregulier")
print(indicateur_irregulier(grille_joueur,plan_cage,grille_complete))

def indicateur_windoku(grille_joueur : list, grille_complete : list, dimension : int = 9):
    """permet d'indiquer à l'utilisateur une case d'une grille de windoku"""

    racine = int(math.sqrt(dimension))
    # Positions des coins supérieurs gauches des 4 fenêtres Windoku
    fenetres_pos = [(1, 1), (1, 5), (5, 1), (5, 5)]

    def obtenir_candidats(grille, lig, col):
        """Retourne la liste des chiffres possibles pour une case donnée."""
        candidats_possibles = []
        for valeur in range(1, dimension + 1):
            
            # Vérification ligne / colonne
            valide = True
            if valeur in grille[lig]: 
                valide = False
            
            # Les nombres contenus dans sa colonne : 
            chiffres_colonne = []
            for i in range(dimension):
                chiffres_colonne.append(grille[i][col])

            if valeur in chiffres_colonne:
                valide = False
            
            # On le trouve le coin du carré pour notre case afin de la balayer
            coin_lig = (lig // racine) * racine
            coin_col = (col // racine) * racine
            
            # On vérifie la validité dans le carré 3x3 classique :
            for l_carre in range(coin_lig, coin_lig + racine):
                for c_carre in range(coin_col, coin_col + racine):
                    if grille[l_carre][c_carre] == valeur: 
                        valide = False
            
            # Maintenant on verifie la validité dans la fenetre
            if valide:
                for (lig_f, col_f) in fenetres_pos:
                    # On vérifie si la case appartient à la fenêtre Windoku actuelle
                    if lig_f <= lig < lig_f + 3 and col_f <= col < col_f + 3:
                        # Si oui on vérifie que la valeur n'est pas déjà dans les 9 cases de cette fenêtre
                        for l_fen in range(lig_f, lig_f + 3):
                            for c_fen in range(col_f, col_f + 3):
                                if grille[l_fen][c_fen] == valeur:
                                    valide = False
            
            if valide: 
                candidats_possibles.append(valeur)
        return candidats_possibles

    # On cherche d'abord s'il y a une case avec un seul candidat
    coords_meilleure = None
    candidats_meilleure = [0] * (dimension + 1)

    for lig in range(dimension):
        for col in range(dimension):
            if grille_joueur[lig][col] == 0:
                candidats_actuels = obtenir_candidats(grille_joueur, lig, col)
                
                # On cherche la case avec le minimum de candidats 
                if len(candidats_actuels) < len(candidats_meilleure):
                    candidats_meilleure = candidats_actuels
                    coords_meilleure = (lig, col)
                # Si la case n'a qu'un seul choix on a fini
                if len(candidats_actuels) == 1: 
                    return grille_complete[lig][col], (lig, col)

    if not coords_meilleure: 
        return None, None

    # Si aucune case n'est évidente, on cherche la case qui devient évidente en regardant juste un coup plus loin comme ses autres candidats sont devenus invalides
    lig_m, col_m = coords_meilleure
    valides_apres_test = []
    for valeur in candidats_meilleure:
        grille_joueur[lig_m][col_m] = valeur
        
        # On regarde si avec cette valeur cela reste valide au rang d'apres
        if windoku.compter_solution_V3(grille_joueur, dimension, limite=1) > 0:
            valides_apres_test.append(valeur)
                
        grille_joueur[lig_m][col_m] = 0

        #Si apres ce test il reste qu'un candidats on arrete
        if len(valides_apres_test) == 1:
            return grille_complete[lig_m][col_m], (lig_m, col_m)

    # En dernier recours, on donne simplement la solution de la case la plus contrainte
    lig, col = coords_meilleure
    return grille_complete[lig][col], (lig, col)

#Windoku 
grille_windoku_test = [[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 8, 4, 0, 0, 0, 3, 5, 0],[0, 6, 2, 0, 0, 0, 1, 7, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 5, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 2, 1, 0, 0, 0, 8, 3, 0],[0, 4, 3, 0, 0, 0, 5, 9, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0]]
solution_windoku = [[4, 6, 8, 9, 2, 5, 1, 3, 7],[2, 3, 7, 1, 8, 4, 6, 5, 9],[9, 5, 1, 3, 6, 7, 4, 2, 8],[3, 2, 6, 5, 9, 8, 7, 1, 4],[7, 8, 9, 6, 1, 4, 3, 5, 2],[5, 4, 1, 7, 3, 2, 9, 8, 6],[6, 9, 3, 4, 5, 1, 2, 7, 0],[8, 7, 2, 4, 5, 1, 9, 6, 3],[1, 7, 4, 2, 3, 9, 5, 8, 6]]
print("indicateur Windoku")
print(indicateur_windoku(grille_windoku_test,solution_windoku))

def indicateur_consecutif(grille_joueur : list, grille_complete : list, duos_consecutifs : list, dimension : int = 9):
    """permet d'indiquer à l'utilisateur une case d'une grille de sudoku consécutif"""

    racine = int(math.sqrt(dimension))

    def obtenir_candidats(grille, lig, col):
        """Retourne la liste des chiffres possibles pour une case donnée."""
        candidats_possibles = []
        for valeur in range(1, dimension + 1):
            
            # Vérification ligne / colonne
            valide = True
            if valeur in grille[lig]: 
                valide = False
            
            # Les nombres contenus dans sa colonne : 
            chiffres_colonne = []
            for i in range(dimension):
                chiffres_colonne.append(grille[i][col])

            if valeur in chiffres_colonne:
                valide = False
            
            # On le trouve le coin du carré pour notre case afin de la balayer
            coin_lig = (lig // racine) * racine
            coin_col = (col // racine) * racine
            
            # On vérifie la validité dans le carré 3x3 classique :
            for l_carre in range(coin_lig, coin_lig + racine):
                for c_carre in range(coin_col, coin_col + racine):
                    if grille[l_carre][c_carre] == valeur: 
                        valide = False
            
            # Maintenant on verifie la validité pour les cases consecutives
            if valide:
                for (pos1, pos2) in duos_consecutifs:
                    # On vérifie si la case appartient à un duo 
                    if (lig, col) == pos1 or (lig, col) == pos2:
                        # On identifie la case voisine dans le duo
                        voisine = pos2 if (lig, col) == pos1 else pos1
                        lig_v, col_v = voisine
                        valeur_voisine = grille[lig_v][col_v]
                        
                        # Si la voisine est remplie et on vérifie que l'écart est bien de 1
                        if valeur_voisine != 0:
                            if abs(valeur - valeur_voisine) != 1:
                                valide = False
            
            if valide: 
                candidats_possibles.append(valeur)
        return candidats_possibles

    # On cherche d'abord s'il y a une case avec un seul candidat
    coords = None
    candidats = [0] * (dimension + 1)

    for lig in range(dimension):
        for col in range(dimension):
            if grille_joueur[lig][col] == 0:
                candidats_actuels = obtenir_candidats(grille_joueur, lig, col)
                
                # On cherche la case avec le minimum de candidats 
                if len(candidats_actuels) < len(candidats):
                    candidats = candidats_actuels
                    coords = (lig, col)
                
                # Si la case n'a qu'un seul choix on a fini
                if len(candidats_actuels) == 1: 
                    return grille_complete[lig][col], (lig, col)

    if not coords: 
        return None, None

    # Si aucune case n'est évidente, on cherche la case qui devient évidente en regardant juste un coup plus loin comme ses autres candidats sont devenus invalides
    for lig in range(dimension):
        for col in range(dimension):
            if grille_joueur[lig][col] == 0:
                candidats_actuels = obtenir_candidats(grille_joueur, lig, col)
                valides_apres_test = []
                
                for valeur in candidats_actuels:
                    # Test temporaire 
                    grille_joueur[lig][col] = valeur

                    # Si ce chiffre permet toujours de finir la grille on la garde
                    if sudoku.compter_solution_V3(grille_joueur, dimension, limite=1) > 0:
                        valides_apres_test.append(valeur)
                    
                    # On retire la valeur
                    grille_joueur[lig][col] = 0 

                # Si apres on a qu'une seule valeur qui ne bloque pas la grille on la renvoie
                if len(valides_apres_test) == 1:
                    return grille_complete[lig][col], (lig, col)

    # En dernier recours, on donne simplement la solution de la case la plus contrainte
    lig, col = coords
    return grille_complete[lig][col], (lig, col)

#consecutif
grille_complete_consectutif = [[9, 5, 4, 7, 3, 8, 2, 6, 1], [8, 3, 6, 9, 1, 2, 7, 4, 5], [1, 7, 2, 5, 4, 6, 9, 3, 8], [2, 1, 7, 4, 5, 9, 3, 8, 6], [3, 4, 8, 6, 2, 1, 5, 7, 9], [6, 9, 5, 8, 7, 3, 1, 2, 4], [4, 8, 1, 3, 9, 7, 6, 5, 2], [5, 2, 3, 1, 6, 4, 8, 9, 7], [7, 6, 9, 2, 8, 5, 4, 1, 3]]
grille_vidée_consecutif = [[9, 5, 0, 0, 0, 8, 0, 6, 0], [0, 0, 0, 0, 1, 0, 7, 0, 0], [0, 7, 0, 5, 4, 6, 0, 0, 0], [0, 1, 0, 0, 0, 9, 3, 8, 0], [0, 4, 8, 0, 0, 0, 0, 7, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 5, 0], [0, 0, 3, 0, 0, 4, 0, 0, 0], [0, 0, 9, 2, 0, 0, 0, 0, 0]]
duos =[((0, 0), (1, 0)), ((0, 1), (0, 2)), ((1, 4), (1, 5)), ((1, 7), (1, 8)), ((1, 7), (2, 7)), ((2, 0), (3, 0)), ((2, 3), (2, 4)), ((2, 3), (3, 3)), ((2, 4), (3, 4)), ((3, 0), (3, 1)), ((3, 0), (4, 0)), ((3, 2), (4, 2)), ((3, 3), (3, 4)), ((3, 7), (4, 7)), ((4, 0), (4, 1)), ((4, 4), (4, 5)), ((5, 1), (6, 1)), ((5, 3), (5, 4)), ((5, 6), (5, 7)), ((6, 0), (7, 0)), ((6, 5), (6, 6)), ((6, 6), (6, 7)), ((7, 1), (7, 2)), ((7, 3), (8, 3)), ((7, 5), (8, 5)), ((7, 6), (7, 7)), ((8, 0), (8, 1)), ((8, 5), (8, 6))]
print("indicateur consecutif")
print(indicateur_consecutif(grille_vidée_consecutif,grille_complete_consectutif,duos))

def indicateur_kakuro(grille_joueur : list, grille_complete : list, dimension : int = 9):
    """permet d'indiquer à l'utilisateur une case d'une grille de kakuro"""

    def obtenir_candidats(grille, lig, col):
        """Retourne la liste des chiffres possibles pour une case donnée."""
        candidats_possibles = []
        
        # indices horizontaux
        col_debut = col
        # On verifie qu'on ne sort pas de la grille et qu'on ne tombe pas sur une cases noire (un tuple)
        # On fait de meme pour la fin de la colonne et pour les indices verticales
        while col_debut > 0 and isinstance(grille[lig][col_debut - 1], int):
            col_debut -= 1
        col_fin = col
        while col_fin < dimension - 1 and isinstance(grille[lig][col_fin + 1], int):
            col_fin += 1
        
        # Pour gerer les cases noires qui sont [Somme_h,Somme_v] = [None, 12] ce qui bloquerait apres les calculs si on garde None
        if col_debut > 0:
            indice_h = grille[lig][col_debut - 1][0]
        else:
            indice_h = None
        
        # indices verticaux
        lig_debut = lig
        while lig_debut > 0 and isinstance(grille[lig_debut - 1][col], int):
            lig_debut -= 1
        lig_fin = lig
        while lig_fin < dimension - 1 and isinstance(grille[lig_fin + 1][col], int):
            lig_fin += 1

        if lig_debut > 0:
            indice_v =  grille[lig_debut - 1][col][1]
        else:
            indice_v = None

        # La somme actuelle dans le segment horizontale
        somme_h_actuelle = 0
        # On regarde le nombre de cases vides sur le segment 
        vides_h = 0
        # Les chiffres déjà présents dans notre ligne
        valeurs_h = []
        for c_k in range(col_debut, col_fin + 1):
            if c_k != col:
                val = grille[lig][c_k]
                if val == 0: 
                    vides_h += 1
                else: 
                    somme_h_actuelle += val
                    valeurs_h.append(val)

        # On fait de meme pour les cases verticales
        somme_v_actuelle = 0    
        vides_v = 0
        valeurs_v = []
        for l_k in range(lig_debut, lig_fin + 1):
            if l_k != lig:
                val = grille[l_k][col]
                if val == 0: vides_v += 1
                else:
                    somme_v_actuelle += val
                    valeurs_v.append(val)

        for valeur in range(1, 10):
            valide = True
            
            # Vérification ligne / colonne 
            if valeur in valeurs_h or valeur in valeurs_v:
                valide = False
            
            # Vérification validité somme horizontale
            if valide and indice_h is not None:
                # S'il reste qu'une case à remplir (vides_h=0) et que la somme avec notre valeur est fausse on arrete la tentative
                if vides_h == 0: 
                    if somme_h_actuelle + valeur != indice_h:
                        valide = False
                
                else:
                    # Le minimum pour remplir les autres cases restantes
                    minimum_requis_restant = sum(range(1, vides_h + 1))
                    # On regarde si notre valeur est acceptable par rapport à la somme cible
                    if somme_h_actuelle + valeur + minimum_requis_restant > indice_h:
                        # Si trop grande on l'invalide
                        valide = False

            # Vérification validité somme verticale
            if valide and indice_v is not None:
                if vides_v == 0:
                    if somme_v_actuelle + valeur != indice_v:
                        valide = False
                else:
                    minimum_requis_restant = sum(range(1, vides_v + 1))
                    if somme_v_actuelle + valeur + minimum_requis_restant > indice_v:
                        valide = False

            if valide:
                candidats_possibles.append(valeur)
                
        return candidats_possibles

    # On cherche d'abord s'il y a une case avec un seul candidat
    coords = None
    candidats = [0] * 10

    for lig in range(dimension):
        for col in range(dimension):
            if isinstance(grille_joueur[lig][col], int) and grille_joueur[lig][col] == 0:
                candidats_actuels = obtenir_candidats(grille_joueur, lig, col)
                
                # On cherche la case avec le minimum de candidats 
                if len(candidats_actuels) < len(candidats):
                    candidats = candidats_actuels
                    coords = (lig, col)
                
                # Si la case n'a qu'un seul choix on a fini
                if len(candidats_actuels) == 1: 
                    return grille_complete[lig][col], (lig, col)

    if not coords: 
        return None, None

    # Si aucune case n'est évidente, on cherche la case qui devient évidente en regardant juste un coup plus loin comme ses autres candidats sont devenus invalides
    for lig in range(dimension):
        for col in range(dimension):
            if isinstance(grille_joueur[lig][col], int) and grille_joueur[lig][col] == 0:
                candidats_actuels = obtenir_candidats(grille_joueur, lig, col)
                valides_apres_test = []
                
                for valeur in candidats_actuels:
                    # Test temporaire 
                    grille_joueur[lig][col] = valeur
                    cree_impasse = False
                    
                    # Si ce chiffre permet toujours de finir la grille on la garde
                    for r in range(dimension):
                        for c in range(dimension):
                            if isinstance(grille_joueur[r][c], int) and grille_joueur[r][c] == 0:
                                if len(obtenir_candidats(grille_joueur, r, c)) == 0:
                                    cree_impasse = True
                                    break
                        if cree_impasse: 
                            break
                    
                    if not cree_impasse:
                        valides_apres_test.append(valeur)
                        
                    # On retire la valeur
                    grille_joueur[lig][col] = 0 
                
                # Si apres on a qu'une seule valeur qui ne bloque pas la grille on la renvoie
                if len(valides_apres_test) == 1:
                    return grille_complete[lig][col], (lig, col)

    # En dernier recours, on donne simplement la solution de la case la plus contrainte
    lig, col = coords
    return grille_complete[lig][col], (lig, col)
    
#Kakuro 
grille_kakuro_joueur = [[[None, None], [None, 11], [None, 13], [None, 24], [None, 11], [None, 4], [None, 22], [None, 10], [None, 3]],[[12, None], 0, 0, [3, None], 0, 0, [4, None], 0, 0],[[10, 10], 0, 0, [15, 12], 0, 0, [17, 13], 0, 0],[[None, 17], [13, None], 0, 0, 0, 0, [10, 9], 0, 0],[[35, None], 0, 0, 0, 0, 0, 0, 0, 0],[[11, 10], 0, 0, [None, 21], [15, 15], 0, 0, [None, None], [None, None]],[[None, 14], [10, None], 0, 0, 0, 0, [12, 10], 0, 0],[[32, None], 0, 0, 0, 0, 0, 0, 0, 0],[[10, None], 0, 0, [7, None], 0, 0, [3, None], 0, 0]]
grille_kakuro_complete = [[[None, None], [None, 11], [None, 13], [None, 24], [None, 11], [None, 4], [None, 22], [None, 10], [None, 3]],[[12, None], 4, 8, [3, None], 2, 1, [4, None], 3, 1],[[10, 10], 7, 3, [15, 12], 9, 6, [17, 13], 9, 8],[[None, 17], [13, None], 2, 4, 6, 1, [10, 9], 8, 2],[[35, None], 9, 1, 3, 4, 2, 5, 7, 4],[[11, 10], 8, 3, [None, 21], [15, 15], 6, 9, [None, None], [None, None]],[[None, 14], [10, None], 1, 2, 4, 3, [12, 10], 9, 3],[[32, None], 6, 7, 8, 5, 4, 1, 2, 9],[[10, None], 3, 7, [7, None], 5, 2, [3, None], 1, 2]]

print("indicateur kakuro")
print(indicateur_kakuro(grille_kakuro_joueur,grille_kakuro_complete))