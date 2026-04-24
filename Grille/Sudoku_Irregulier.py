import random


# I. Création de la structure des cages 


def creer_plan(dimension=9):
    """Crée un plan de 9 blocs 3x3 classiques."""
    
    plan = [[0 for _ in range(dimension)] for _ in range(dimension)]
    
    for l in range(dimension):
        for c in range(dimension):
            # On donne un numéro aux cages suivant leur position horizontale et verticale le + 1 est pour commencer le marquage à 1 
            num_cage = (l // 3) * 3 + (c // 3) + 1
            plan[l][c] = num_cage
    return plan

def est_joint(plan : list, num_cage : int, dimension=9):
    """
    On verifie si notre cage est toujours en un seul tenant
    """

    cases = []
    
    # On cherche les coordonnées des cases de notre cage
    for l in range(dimension):
        for c in range(dimension):
            if plan[l][c] == num_cage:
                cases.append((l, c))

    if not cases: 
        return False
    
    a_visiter = [cases[0]]  
    vus = set()

    # Pour chaque case à partir de la premiere on va voir si on peut trouver toutes les cases par propagation
    while a_visiter:
        actuelle = a_visiter.pop()
        # On fait le tri maintenant des cases qui ne sont pas dans notre cage
        if actuelle in cases and actuelle not in vus:
            vus.add(actuelle)
            l, c = actuelle

            # On ajoute les voisins de cette case
            a_visiter.extend([(l-1, c), (l+1, c), (l, c-1), (l, c+1)])
            
    return len(vus) == len(cases) 

def interchanger_cages(plan : list, dimension : int, iterations=500):
    """
    Déforme les cages par échanges de cases frontalières de cages differentes
    """
    # On compte le nombre cases échangées
    succes = 0
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    # On cherche toutes les cases qui sont en conctats avec deux cages ce qu'on appelle frontiere
    frontieres = set() 
    for l in range(dimension):
        for c in range(dimension):
            num_1 = plan[l][c]
            for dl, dc in directions:
                l2, c2 = l + dl, c + dc

                # On vérifie que cette nouvelle case est bien comprise dans la grille
                if 0 <= l2 < dimension and 0 <= c2 < dimension:
                    num_2 = plan[l2][c2]
                    if num_1 != num_2:
                        frontieres.add((l, c))

    for _ in range(iterations):
        # Sécurité dans le cas où notre liste est vide
        if not frontieres: 
            break

        # On choisit au hasard une case qui touche une autre cage 
        lig_1, col_1= random.choice(list(frontieres))
        cage_a = plan[lig_1][col_1]

        # Trouver les cases voisines de cette case pour voir les cages qu'elle touche 
        voisines_possibles = set()
        for dl, dc in directions:
            nl, nc = lig_1 + dl, col_1 + dc
            if 0 <= nl < dimension and 0 <= nc < dimension:
                if plan[nl][nc] != cage_a:
                    # Ajoutons cette case qui a une cage differente
                    voisines_possibles.add(plan[nl][nc])
        
        if not voisines_possibles:
            continue
            
        # On choisit au hasard l'une des cages voisines pour être notre cage_b
        cage_b = random.choice(list(voisines_possibles))

        candidats = []
        for lig_f,col_f in frontieres:
            cage_f = plan[lig_f][col_f]
            # Cette deuxieme case doit appartenir à la cage b
            if cage_f == cage_b : 
                #Cette deuxieme case doit toucher la cage a
                touche_a = False
                for dl, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                    if 0 <= lig_f+dl < dimension and 0 <= col_f+dc < dimension:
                        if plan[lig_f+dl][col_f+dc] == cage_a:
                            touche_a = True
                            break
                
                if touche_a:
                    # Cette deuxieme case ne doit pas toucher notre premiere case pour eviter les trous dans l'une des cages
                    # Ce qu'on fait en verifiant la distance entre c'est deux cases
                    if abs(lig_f - lig_1) + abs(col_f - col_1) > 1:
                        candidats.append((lig_f, col_f))

        # Par sécurité s'il n'y a aucun candidats 
        if not candidats:
            continue

        # On prend une case au hasard parmi celles qui valident les conditions
        lig_2, col_2= random.choice(candidats)

        # On tente le double échange
        plan[lig_1][col_1], plan[lig_2][col_2] = cage_b, cage_a
        
        # On vérifie si les deux cages sont toujours d'un seul tenant
        if est_joint(plan, cage_a) and est_joint(plan, cage_b):
            succes += 1
            # On met à jour nos set :
            # On définit la zone impactée : les 2 cases échangées + leurs voisins
            cases_a_verifier = set()
            for l, c in [(lig_1, col_1), (lig_2, col_2)]:
                cases_a_verifier.add((l, c))
                for dl, dc in directions:
                    nl, nc = l + dl, c + dc
                    if 0 <= nl < dimension and 0 <= nc < dimension:
                        cases_a_verifier.add((nl, nc))

            # Pour chaque case de cette zone, on décide si elle doit être dans le set ou non
            for l, c in cases_a_verifier:
                est_frontiere = False
                val_case = plan[l][c]
                
                # On regarde ses voisins pour voir si elle touche une cage différente
                for dl, dc in directions:
                    nl, nc = l + dl, c + dc
                    if 0 <= nl < dimension and 0 <= nc < dimension:
                        if plan[nl][nc] != val_case:
                            est_frontiere = True
                            break
                
                if est_frontiere:
                    frontieres.add((l, c))
                else:
                    # .discard retire l'élément s'il existe, sinon ne fait rien
                    frontieres.discard((l, c))
        else:
            # Si ce n'est pas le cas on annule l'échange
            plan[lig_1][col_1], plan[lig_2][col_2] = cage_a, cage_b

    return plan

def generer_structure_valide(dimension=9):
    """Genère la structure des cages pour un sudoku irrégulier"""
    # On part d'un plan classique de Sudoku
    plan = creer_plan(dimension)
    
    # On déforme ce plan 
    interchanger_cages(plan, dimension, iterations=200)
    
    # On crée le dictionnaire de nos cages lié à notre nouveau plan
    dico_cage = {}
    for l in range(dimension):
        for c in range(dimension):
            num_cage = plan[l][c]
        
            # Si la cage n'est pas encore dans le dico on crée sa liste
            if num_cage not in dico_cage:
                dico_cage[num_cage] = []
            
            # On ajoute la coordonnée
            dico_cage[num_cage].append((l, c))
            
    return plan, dico_cage


# II. Remplissage de cette structure de cages


def initialiser_contraintes(grille, plan_cage, dimension=9):
    """Pour preparer les set contenant les informations des lignes/colonnes/cages"""

    lignes_utilisees = [set() for _ in range(dimension)]
    cols_utilisees = [set() for _ in range(dimension)]
    
    cages_utilisees = {}

    for l in range(dimension):
        for c in range(dimension):
            val = grille[l][c]
            num_cage = plan_cage[l][c]
            
            # Initialisation du set pour la cage si pas encore fait
            if num_cage not in cages_utilisees:
                cages_utilisees[num_cage] = set()
                
            if val != 0:
                lignes_utilisees[l].add(val)
                cols_utilisees[c].add(val)
                cages_utilisees[num_cage].add(val)
                
    return lignes_utilisees, cols_utilisees, cages_utilisees

def trouver_meilleure_case(grille : list, plan_cage : list, lignes_u : set, cols_u :set, cages_u : dict, dimension=9):
    min_candidats = dimension + 1
    meilleure_case = None
    candidats_meilleure = []

    for l in range(dimension):
        for c in range(dimension):
            # Si notre case est nulle :
            if grille[l][c] == 0:
                num_cage = plan_cage[l][c]

                candidats = []
                # Déterminons les candidats pour cette case
                for val in range(1, dimension + 1):
                    if val not in lignes_u[l] and val not in cols_u[c] and val not in cages_u[num_cage]:
                        candidats.append(val)
                

                nb_candidats = len(candidats)

                if nb_candidats == 0:
                    return (l, c), []
                
                # Si notre case a moins de possibilités elle devient la meilleure case
                if nb_candidats < min_candidats:
                    min_candidats = nb_candidats
                    meilleure_case = (l, c)
                    candidats_meilleure = candidats
                # Si une case a 1 seule possibilité on s'arrete puisqu'on ne trouver pas mieux
                if min_candidats == 1:
                    return meilleure_case, candidats_meilleure

    return meilleure_case, candidats_meilleure

def generer_grille_complete(grille : list, plan_cage : list, lignes_u : set, cols_u :set, cages_u : dict, dimension=9, compteur=None):    
    """Genère une grille complétée à partir du plan des cages"""
    # On initialise notre compteur
    if compteur is None:
        compteur = [0]

    compteur[0] += 1

    dimension = len(grille)

    # Si c'est trop long on arrete cette tentative
    if compteur[0] > 50000:         
        return False
    
    # On cherche la meilleure case vide avec le moins de possibilités
    meilleure_case, candidats_meilleure = trouver_meilleure_case(grille, plan_cage, lignes_u, cols_u, cages_u, dimension)

    # Si on a aucune meilleure case c'est que la grille est terminée 
    if meilleure_case is None:
        return grille
    
    l, c = meilleure_case
    num_cage = plan_cage[l][c]

    # On mélange pour ne pas toujours avoir la même grille
    random.shuffle(candidats_meilleure)

    for val in candidats_meilleure : 
        if  val not in lignes_u[l] and val not in cols_u[c] and val not in cages_u[num_cage]:
            
            # On maintient nos 3 set à jour avec la nouvelle valeur
            grille[l][c] = val
            lignes_u[l].add(val)
            cols_u[c].add(val)
            cages_u[num_cage].add(val)
            
            resultat = generer_grille_complete(grille, plan_cage, lignes_u, cols_u, cages_u, dimension, compteur)            
            
            # Si on a fini c'est à dire qu'on est arrivés à la derniere ligne la fonction renvoit la grille ce qui donnera True ici
            if resultat :
                return resultat
            
            # Si ça ne mène à rien, on revient en arriere 
            grille[l][c] = 0
            lignes_u[l].remove(val)
            cols_u[c].remove(val)
            cages_u[num_cage].remove(val)

    return False

def compter_solutions_irregulier (grille : list, plan_cage : list, lignes_u : set, cols_u : set, cages_u :set):
    """
    S'arrête dès qu'il trouve 2 solutions pour prouver que la grille n'est pas unique.
    """
    dimension = len(grille)

    # On cherche la case avec le moins de possibilités
    meilleure_case, candidats_meilleure = trouver_meilleure_case(grille, plan_cage, lignes_u, cols_u, cages_u, dimension)

    # Si meilleure case est vide que notre grille est terminée
    if meilleure_case is None:
        return 1

    l, c = meilleure_case
    num_cage = plan_cage[l][c]
    nb_solutions = 0

    for val in candidats_meilleure :
        # On teste toutes les candidats possibles
        if val not in lignes_u[l] and val not in cols_u[c] and val not in cages_u[num_cage]:     

            # Valide donc on la place temporairement
            grille[l][c] = val
            lignes_u[l].add(val)
            cols_u[c].add(val)
            cages_u[num_cage].add(val)

            # On poursuit pour la case suivante
            nb_solutions += compter_solutions_irregulier(grille, plan_cage, lignes_u, cols_u, cages_u)

            # On revient en arriere
            grille[l][c] = 0
            lignes_u[l].remove(val)
            cols_u[c].remove(val)
            cages_u[num_cage].remove(val) 

            # On s'arrete si on ne respecte plus l'unicité
            if nb_solutions > 1:
                return 2

    return nb_solutions


# III. Création de la grille à résoudre


def cree_grille_a_resoudre (grille_complete : list, plan_cage : list, nb_cases_a_vider : int):
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
        l_u, c_u, cage_u = initialiser_contraintes(grille_joueur, plan_cage, dimension)

        if compter_solutions_irregulier(grille_joueur, plan_cage, l_u, c_u, cage_u) == 1:
            cases_vides += 1
        else:
            # on reprend la derniere valeur
            grille_joueur[l][c] = valeur_sauvegardee
            
    return grille_joueur


# IV. Exécution


def afficher_grille(grille):
    """Affiche la grille de maniere lisible."""
    for ligne in grille:
        for val in ligne:
            # Si la case est vide on affiche un point pour la lisibilité
            if val == 0:
                print(".", end=" ")
            else:
                print(val, end=" ")
        print()
    print()

def main(nb_cases_a_vider : int):

    grille_generee = False
    tentatives = 0
    dimension = 9
    
    while not grille_generee :
        tentatives += 1
        print(f"Tentative n°{tentatives}...")

        # On crée une structure de cages
        plan_cage, dico_cage = generer_structure_valide(dimension)
        
        # On prépare une grille vide et les contraintes
        grille_vide = [[0 for _ in range(dimension)] for _ in range(dimension)]
        l_u, c_u, cage_u = initialiser_contraintes(grille_vide, plan_cage, dimension)

        # On tente de remplir cette structure 
        # Si generer_grille_complete échoue, elle renvoie False
        resultat = generer_grille_complete(grille_vide, plan_cage, l_u, c_u, cage_u, dimension)

        if resultat:
            grille_complete = resultat
            grille_generee = True
            print("Grille générée")
        else:
            print("Échec du remplissage")

    print("\nPlan_cage :")
    afficher_grille(plan_cage)

    
    print("\nGrille complète :")
    afficher_grille(grille_complete)

    print("Remplissage de la grille")
    grille_joueur = cree_grille_a_resoudre(grille_complete, plan_cage, nb_cases_a_vider)
    
    print("\nGrille à résoudre :")
    afficher_grille(grille_joueur)

main(50)

