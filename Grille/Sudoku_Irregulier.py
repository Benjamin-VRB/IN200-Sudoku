import random
import Sudoku

def obtenir_voisins(l, c, dimension):
    """
    On obtient les indices des cases voisines de celle demandée
    """
    voisins = []
    
    if l + 1 < dimension: 
        voisins.append((l + 1, c))
    if c + 1 < dimension: 
        voisins.append((l, c + 1))
    if l - 1 >= 0: 
        voisins.append((l - 1, c))
    if c - 1 >= 0: 
        voisins.append((l, c - 1))
        
    return voisins

def cages(grille):
    """
    A partir d'une grille remplie on en déduit des cages qui fonctionnent
    """
    dimension = len(grille)
    
    # Matrice pour stocker le numéro de la cage attribué à chaque case
    cages_grille = [[0 for _ in range(dimension)] for _ in range(dimension)]
    num_cage = 0
    
    # Dictionnaire pour stocker les valeurs contenues dans chaque cage. 
    # Son format : {num_cage: [valeur1, valeur2, ...]}
    toutes_valeurs_cages = {}

    for i in range(dimension):
        for j in range(dimension):
            
            if cages_grille[i][j] == 0:
                num_cage += 1
                cases_cage = [(i, j)]
                valeurs_cage = [grille[i][j]]
                cages_grille[i][j] = num_cage
                
                # Taille aléatoire de la cage 
                taille_cible = random.randint(2, 5) 
                
                # Agrandissement de la cage par propagation
                while len(cases_cage) < taille_cible: 
                    voisins_potentiels = []
                    
                    # On cherche les voisins de toutes les cases qui composent déjà notre cage
                    for cx, cy in cases_cage:
                        for vx, vy in obtenir_voisins(cx, cy, dimension):
                            
                            # Conditions d'intégration :
                            # 1. La case voisine ne doit pas être déjà dans une cage
                            # 2. Le chiffre de la case ne doit pas créer de doublon dans la cage
                            if cages_grille[vx][vy] == 0 and grille[vx][vy] not in valeurs_cage:
                                
                                # On évite de rajouter des doublons dans les voisins potentiels
                                if (vx, vy) not in voisins_potentiels:
                                    voisins_potentiels.append((vx, vy))

                    # La cage ne peut plus s'aggrandir
                    if not voisins_potentiels: 
                        break 

                    # Choix aléatoire d'un voisin valide pour agrandir la cage
                    choix_x, choix_y = random.choice(voisins_potentiels)
                    
                    cages_grille[choix_x][choix_y] = num_cage
                    cases_cage.append((choix_x, choix_y))
                    valeurs_cage.append(grille[choix_x][choix_y])
                    
                toutes_valeurs_cages[num_cage] = valeurs_cage
                
    return cages_grille, toutes_valeurs_cages

def verification_placement_irregulier(grille, l, c, valeur, cages_grille):
    """
    Verifie si la valeur placé est possible
    """
    
    dimension = len(grille)
    num_cage = cages_grille[l][c]

    # Vérification des lignes/colonnes
    for i in range(dimension):
        if grille[l][i] == valeur: 
            return False
        if grille[i][c] == valeur: 
            return False

    # Vérification des doublons dans la  cage
    for i in range(dimension):
        for j in range(dimension):
            if cages_grille[i][j] == num_cage:
                # On exclut la case qui est étudiée
                if (i, j) != (l, c) and grille[i][j] == valeur:
                    return False

    return True

def compter_solutions_irregulier (grille_test, cages_grille, l=0, c=0):
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
        return compter_solutions_irregulier(grille, cages, lig_suiv, col_suiv)

    nb_solutions = 0

    for val in range(1, dimension + 1):
        # On teste toutes les valeurs possibles
        if verification_placement_irregulier(grille, cages, l, c, val):
            # Valide donc on la place temporairement
            grille[l][c] = val
            # On poursuit pour la case suivante
            nb_solutions += compter_solutions_irregulier(grille, cages, lig_suiv, col_suiv)
            
            grille[l][c] = 0  

            # On s'arrete si on ne respecte plus l'unicité
            if nb_solutions > 1:
                return 2

    return nb_solutions

def supprime_valeurs_irregulier (grille_complete, cages_grille, nb_cases_a_vider):
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

        if compter_solutions_irregulier(grille_tempo, cages_grille) == 1:
            cases_vides += 1
        else:
            # on reprend la derniere valeur
            grille_joueur[l][c] = valeur_sauvegardee
            
    return grille_joueur


#----test----

grille = Sudoku.remplir_grille_V2(dimension=9)

print("\n----Grille de base----\n")
for ligne in grille : 
    print(ligne)

cages_grille,toutes_valeurs_cages = cages(grille)

print("\n----Répartition des cages----\n")

for ligne in cages_grille:
    print(ligne)

grille_joueur = supprime_valeurs_irregulier(grille,cages_grille,60)

print("\n----Grille à résoudre----\n")

for ligne in grille_joueur : 
    print(ligne)