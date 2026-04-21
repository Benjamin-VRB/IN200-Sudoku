import random

def generer_dico_irregulier(dimension=9):
    """
    Génère une grille vide avec ses cages.
    Retourne la matrice de la grille et le dictionnaire des cages.
    """

    grille_num = [ [0 for _ in range(dimension)] for _ in range(dimension)]
    cages = {}
    
    # On place le point de départ de chaque cage d'un coup (pour éviter les blocages)
    cases_depart = [(l, c) for l in range(dimension) for c in range(dimension)]
    random.shuffle(cases_depart)
    
    for numero_cage in range(1, dimension + 1):
        l, c = cases_depart.pop()
        grille_num[l][c] = numero_cage
        cages[numero_cage] = [(l, c)]

    def obtenir_voisins_libres(ligne,colonne,grille,dimension):
        """
        Cherche les cases adjacentes (haut, bas, gauche, droite) qui sont vides. 
        """
        cases_vides = []
        directions = [(-1,0),(1,0),(0,1),(0,-1)]
        
        for direc_ligne,direc_colonne in directions : 
            coord_ligne = direc_ligne + ligne
            coord_colonne = direc_colonne + colonne

            if 0 <= coord_ligne < dimension and 0 <= coord_colonne< dimension and grille[coord_ligne][coord_colonne] == 0:
                cases_vides.append((coord_ligne,coord_colonne))
        return cases_vides 

    def choisir_case_la_plus_contrainte(grille,candidats,dimension):
        # On enleve le determinisme pour éviter de repeter la grille impossible  
        random.shuffle(candidats)

        case_isolee = candidats[0]
        nb_voisins_min = 10
        
        for case in candidats:
            l, c = case

            # On compte combien ce candidat a de voisins libres
            nb_v = len(obtenir_voisins_libres(l, c, grille, dimension))
            
            # Si cette case est plus isolée que la meilleure trouvée 
            if nb_v < nb_voisins_min:
                nb_voisins_min = nb_v
                case_isolee = case

        return case_isolee
    

    
    # Agrandissement de la cage (On les fait grandir tour à tour)
    for etape in range(dimension - 1):
        ordre_cages = list(range(1, dimension + 1))
        random.shuffle(ordre_cages)

        for numero_cage in ordre_cages:
            options_possibles = []
            cage_actuelle = cages[numero_cage]

            # On cherche les voisins pour chaque case de notre cage en construction
            for case_l, case_c in cage_actuelle:
                voisins = obtenir_voisins_libres(case_l, case_c, grille_num, dimension)

                for case_voisine in voisins:
                    #verification de l'unicité de nos candidats
                    if case_voisine not in options_possibles:
                        options_possibles.append(case_voisine)
            
            # Si la liste est vide on arrête la boucle
            if len(options_possibles) == 0:
                continue
                
            #Parmi les candidats on prend celui qui a le plus de chance de devenir une case orpheline(c'est à dire celle qui a le moins de voisins)
            nouvelle_l, nouvelle_c = choisir_case_la_plus_contrainte(grille_num,options_possibles,dimension)
            
            # On met à jour la grille et notre liste
            grille_num[nouvelle_l][nouvelle_c] = numero_cage
            cages[numero_cage].append((nouvelle_l, nouvelle_c))
            
    return grille_num, cages

def generer_structure_valide(dimension = 9): 
    """
    Gènerre une structure de 9 cages de 9 éléments
    """
    tentative = 0 
    
    while True : 
        if tentative % 1000 == 0 : 
            print(tentative)
        
        tentative = tentative +1 

        grille_test, cages_test = generer_dico_irregulier(dimension)

        valide = True 

        # On verifie que cette grille contient bien 9 cages 
        if len(cages_test) != dimension: 
            valide = False 

        # On vérifie que chage cage contient bien 9 cases : 
        for indice in cages_test : 
            if len(cages_test[indice]) != dimension : 
                valide = False
                break

        if valide : 
            return grille_test, cages_test,tentative

def est_placement_valide(grille : list, dico_cage : dict, plan_cage, l, c, val):
    """
    Verifie si la valeur placé est possible
    """
    
    dimension = len(grille)
    num_cage = plan_cage[l][c]

    # Vérification des lignes/colonnes
    for i in range(dimension):
        if grille[l][i] == val: 
            return False
        if grille[i][c] == val: 
            return False

    # Vérification des doublons dans la  cage
    for i,j in dico_cage[num_cage] :
        if (i, j) != (l, c) and grille[i][j] == val:
                return False

    return True

def generer_grille_complete(grille : list, dico_cage : dict, plan_cage, l=0, c=0):   
    
    dimension = len(grille)

    # On arrete dès qu'on a depassé la derniere ligne
    if l  == dimension:
        return grille

    # Calcul de la case suivante
    if c == dimension - 1:
        lig_suiv = l + 1
        col_suiv = 0
    else:
        lig_suiv = l
        col_suiv = c + 1

    # Si la case est déjà remplie on poursuit
    if grille[l][c] != 0:
        return generer_grille_complete(grille, dico_cage, plan_cage, lig_suiv, col_suiv)

    # Pour éviter d'avoir toujours la meme grille on mélange les valeurs
    valeurs =list(range(1,dimension+1))
    random.shuffle(valeurs)

    for val in valeurs : 
        if est_placement_valide(grille, dico_cage,plan_cage, l, c, val):
            grille[l][c] = val
            
            resultat = generer_grille_complete(grille, dico_cage, plan_cage, lig_suiv, col_suiv)

            # Si resultat contient la grille (donc True) alors c'est qu'on a fini 
            if resultat :
                return resultat
            
            # Si ça ne mène à rien, on revient en arriere 
            grille[l][c] = 0

    return False

def compter_solutions_irregulier (grille : list, dico_cage : dict, plan_cage, l=0, c=0):
    """
    S'arrête dès qu'il trouve 2 solutions pour prouver que la grille n'est pas unique.
    """
    dimension = len(grille)

    # On arrete dès qu'on a depassé la derniere ligne
    if l  == dimension:
        return 1

    # Calcul de la case suivante
    if c == dimension - 1:
        lig_suiv = l + 1
        col_suiv = 0
    else:
        lig_suiv = l
        col_suiv = c + 1

    # Si la case est déjà remplie on poursuit
    if grille[l][c] != 0:
        return compter_solutions_irregulier(grille, dico_cage,plan_cage, lig_suiv, col_suiv)

    nb_solutions = 0

    for val in range(1, dimension + 1):
        # On teste toutes les valeurs possibles
        if est_placement_valide(grille, dico_cage, plan_cage,  l, c, val):
            # Valide donc on la place temporairement
            grille[l][c] = val
            # On poursuit pour la case suivante
            nb_solutions += compter_solutions_irregulier(grille, dico_cage, plan_cage, lig_suiv, col_suiv)
            
            grille[l][c] = 0  

            # On s'arrete si on ne respecte plus l'unicité
            if nb_solutions > 1:
                return 2

    return nb_solutions

def cree_grille_a_resoudre (grille_complete : list, dico_cage : dict, plan_cage, nb_cases_a_vider):
    """
    Crée un Sudoku irrégulier à résoudre qui verifie que la solution reste unique
    """
    dimension = len(grille_complete)
    toutes_les_cases=[]

    # On fait une copie de notre grille résolue
    grille_joueur=[ligne[:] for ligne in grille_complete]

    # liste de toutes les coordonnées possibles pour les mélanger
    for i in range(dimension):        
        for j in range(dimension):   
            coordonnee = (i, j)       
            toutes_les_cases.append(coordonnee)
    random.shuffle(toutes_les_cases)
    
    cases_vides = 0
    
    # On arrete quand on a vidé assez de cases
    for l, c in toutes_les_cases:
        if cases_vides >= nb_cases_a_vider:
            break
            
        # Sauvegarde de notre derniere valeur supprimée pour permettre de retourner en arriere
        valeur_sauvegardee = grille_joueur[l][c]
        
        grille_joueur[l][c] = 0
        
        # On vérifie l'unicité
        grille_tempo=[ligne[:] for ligne in grille_joueur]

        if compter_solutions_irregulier(grille_tempo, dico_cage, plan_cage) == 1:
            cases_vides += 1
        else:
            # on reprend la derniere valeur
            grille_joueur[l][c] = valeur_sauvegardee
            
    return grille_joueur