import math
import Grille.kenken as kenken
import Grille.sudoku_chaos as irregulier
import Grille.windoku as windoku
import Grille.sudoku as sudoku

def indicateur_sudoku(grille_joueur : list, grille_complete : list, dimension : int):
    """permet d'indiquer à l'utilisateur une case d'une grille de sudoku
    Entrée : 
        grille_joueur : la grille actuelle du joueur pouvant contenir des erreurs
        grille_complete : la grille solution
    Sortie : 
        Statut ("Erreur" ou "Correct"), (Valeur, Coordonnées)
    """
    
    racine = int(math.sqrt(dimension))

    # On verifie que la grille est déjà correcte
    for lig in range(dimension): 
        for col in range(dimension):
            # Si la case n'est pas vide et differente de la solution on l'indique au joueur
            if grille_joueur[lig][col] != 0 and grille_joueur[lig][col] != grille_complete[lig][col] : 
                return "Erreur", (grille_complete[lig][col], (lig, col))

    def obtenir_candidats(grille, lig, col):
        """Retourne la liste des chiffres possibles pour une case donnée."""
        candidats_possibles = []
        
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
                    return "Correct", (grille_complete[lig][col], (lig, col))

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
                    return "Correct", (grille_complete[lig][col], (lig, col))

    # En dernier recours, on donne simplement la solution de la case la plus contrainte
    lig, col = coords
    return "Correct", (grille_complete[lig][col], (lig, col))

def indicateur_kenken(grille_joueur : list, grille_complete : list, dictionnaire_cages : dict, dimension : int):
    """permet d'indiquer à l'utilisateur une case d'une grille de kenken
    Entrée : 
        grille_joueur : la grille actuelle du joueur pouvant contenir des erreurs
        grille_complete : la grille solution
    Sortie : 
        Statut ("Erreur" ou "Correct"), (Valeur, Coordonnées)
    """

    # On verifie que la grille est déjà correcte
    for lig in range(dimension): 
        for col in range(dimension):
            # Si la case n'est pas vide et differente de la solution on l'indique au joueur
            if grille_joueur[lig][col] != 0 and grille_joueur[lig][col] != grille_complete[lig][col] : 
                return "Erreur", (grille_complete[lig][col], (lig, col))
        
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
                    return "Correct", (grille_complete[lig][col], (lig, col))

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
                    return "Correct", (grille_complete[lig][col], (lig, col))

    # En dernier recours, on donne simplement la solution de la case la plus contrainte
    lig, col = coords
    return "Correct", (grille_complete[lig][col], (lig, col))

def indicateur_irregulier (grille_joueur : list, grille_complete : list, plan_cage : list):
    """permet d'indiquer à l'utilisateur une case à partir d'une grille d'un Sudoku Irregulier
    Entrée : 
        grille_joueur : la grille actuelle du joueur pouvant contenir des erreurs
        grille_complete : la grille solution
        plan_cage : une grille avec le numéro des cages
    Sortie : 
        Statut ("Erreur" ou "Correct"), (Valeur, Coordonnées)
    """
    dimension = len(grille_joueur)
    
    # On verifie que la grille est déjà correcte
    for lig in range(dimension): 
        for col in range(dimension):
            # Si la case n'est pas vide et differente de la solution on l'indique au joueur
            if grille_joueur[lig][col] != 0 and grille_joueur[lig][col] != grille_complete[lig][col] : 
                return "Erreur", (grille_complete[lig][col], (lig, col))
            
    l_u, c_u, cage_u = irregulier.initialiser_contraintes(grille_joueur, plan_cage, dimension)
    
    # On cherche d'abord s'il y a une case avec un seul candidat
    coords, candidats = irregulier.trouver_meilleure_case(grille_joueur, plan_cage, l_u, c_u, cage_u, dimension)
    
    # Dans le cas où la grille est déjà remplie
    if coords is None:
        return None, None
    
    l_meilleure, c_meilleure = coords

    if coords and len(candidats) == 1:
        return "Correct", (grille_complete[l_meilleure][c_meilleure], (l_meilleure, c_meilleure))

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
                    return "Correct", (grille_complete[l][c], (l, c))

    # En dernier recours, on donne simplement la solution de la case la plus contrainte
    l,c = coords
    return "Correct", (grille_complete[l][c], (l, c))

def indicateur_windoku(grille_joueur : list, grille_complete : list, dimension : int = 9):
    """permet d'indiquer à l'utilisateur une case d'une grille de windoku
    Entrée : 
        grille_joueur : la grille actuelle du joueur pouvant contenir des erreurs
        grille_complete : la grille solution
    Sortie : 
        Statut ("Erreur" ou "Correct"), (Valeur, Coordonnées)
    """
    racine = int(math.sqrt(dimension))
    # Positions des coins supérieurs gauches des 4 fenêtres Windoku
    fenetres_pos = [(1, 1), (1, 5), (5, 1), (5, 5)]

    # On verifie que la grille est déjà correcte
    for lig in range(dimension): 
        for col in range(dimension):
            # Si la case n'est pas vide et differente de la solution on l'indique au joueur
            if grille_joueur[lig][col] != 0 and grille_joueur[lig][col] != grille_complete[lig][col] : 
                return "Erreur", (grille_complete[lig][col], (lig, col))

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
                    return "Correct", (grille_complete[lig][col], (lig, col))

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
            return "Correct", (grille_complete[lig_m][col_m], (lig_m, col_m))

    # En dernier recours, on donne simplement la solution de la case la plus contrainte
    lig, col = coords_meilleure
    return "Correct", (grille_complete[lig][col], (lig, col))

def indicateur_consecutif(grille_joueur : list, grille_complete : list, duos_consecutifs : list, dimension : int = 9):
    """permet d'indiquer à l'utilisateur une case d'une grille de sudoku consécutif
    Entrée : 
        grille_joueur : la grille actuelle du joueur pouvant contenir des erreurs
        grille_complete : la grille solution
    Sortie : 
        Statut ("Erreur" ou "Correct"), (Valeur, Coordonnées)
    """
    racine = int(math.sqrt(dimension))

    # On verifie que la grille est déjà correcte
    for lig in range(dimension): 
        for col in range(dimension):
            # Si la case n'est pas vide et differente de la solution on l'indique au joueur
            if grille_joueur[lig][col] != 0 and grille_joueur[lig][col] != grille_complete[lig][col] : 
                return "Erreur", (grille_complete[lig][col], (lig, col))
            
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
                    return "Correct", (grille_complete[lig][col], (lig, col))

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
                    return "Correct", (grille_complete[lig][col], (lig, col))

    # En dernier recours, on donne simplement la solution de la case la plus contrainte
    lig, col = coords
    return "Correct", (grille_complete[lig][col], (lig, col))

def indicateur_kakuro(grille_joueur : list, grille_complete : list, dimension : int = 9):
    """permet d'indiquer à l'utilisateur une case d'une grille de kakuro
    Entrée : 
        grille_joueur : la grille actuelle du joueur pouvant contenir des erreurs
        grille_complete : la grille solution
    Sortie : 
        Statut ("Erreur" ou "Correct"), (Valeur, Coordonnées)
    """
    
    # On verifie que la grille est déjà correcte
    for lig in range(dimension): 
        for col in range(dimension):
            # Si la case n'est pas vide et differente de la solution on l'indique au joueur
            if grille_joueur[lig][col] != 0 and grille_joueur[lig][col] != grille_complete[lig][col] : 
                return "Erreur", (grille_complete[lig][col], (lig, col))
            
    def obtenir_candidats(grille, lig, col):
        """Retourne la liste des chiffres possibles pour une case donnée."""
        candidats_possibles = []
        
        # indices horizontaux
        col_debut = col
        while col_debut > 0 and isinstance(grille[lig][col_debut - 1], int):
            col_debut -= 1
        col_fin = col
        while col_fin < dimension - 1 and isinstance(grille[lig][col_fin + 1], int):
            col_fin += 1
        
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
        vides_h = 0
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
                if vides_h == 0: 
                    if somme_h_actuelle + valeur != indice_h:
                        valide = False
                else:
                    minimum_requis_restant = sum(range(1, vides_h + 1))
                    if somme_h_actuelle + valeur + minimum_requis_restant > indice_h:
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
                    return "Correct", (grille_complete[lig][col], (lig, col))

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
                    return "Correct", (grille_complete[lig][col], (lig, col))

    # En dernier recours, on donne simplement la solution de la case la plus contrainte
    lig, col = coords
    return "Correct", (grille_complete[lig][col], (lig, col))