import random

def voisins_vides(ligne, colonne, grille, dimension):
    """
    Cherche les cases adjacentes (haut, bas, gauche, droite) qui sont vides. 
    """
    cases_vides = []
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    
    for direc_ligne, direc_colonne in directions: 
        coord_ligne = direc_ligne + ligne
        coord_colonne = direc_colonne + colonne

        if 0 <= coord_ligne < dimension and 0 <= coord_colonne < dimension and grille[coord_ligne][coord_colonne] == 0:
            cases_vides.append((coord_ligne, coord_colonne))
    return cases_vides 


def generation_structure_cages(dimension=9):
    """
    Génère une grille de Suguru vide avec ses cages.
    Retourne la matrice de la grille et le dictionnaire des cages.
    """
    
    matrice_cages = [[0 for _ in range(dimension)] for _ in range(dimension)]

    dico_cages = {}
    numero_cage = 1

    for ligne in range(dimension):
        for colonne in range(dimension): 
            
            # Si la case n'appartient encore à aucune cage
            if matrice_cages[ligne][colonne] == 0: 
                
                taille_voulue = random.randint(1, 5)
                cage_actuelle = [(ligne, colonne)]
                matrice_cages[ligne][colonne] = numero_cage

                # Agrandissement de la cage
                for etape in range(taille_voulue - 1):
                    options_possibles = []

                    # On cherche les voisins pour chaque case de notre cage en construction
                    for case_l, case_c in cage_actuelle:
                        voisins = voisins_vides(case_l, case_c, matrice_cages, dimension)
                        
                        for case_voisine in voisins:
                            if case_voisine not in options_possibles:
                                options_possibles.append(case_voisine)
                    
                    # Si la liste est vide on arrête la boucle
                    if len(options_possibles) == 0:
                        break

                    nouvelle_l, nouvelle_c = random.choice(options_possibles)
                    
                    # On met à jour la grille et notre liste
                    matrice_cages[nouvelle_l][nouvelle_c] = numero_cage
                    cage_actuelle.append((nouvelle_l, nouvelle_c))

                dico_cages[numero_cage] = cage_actuelle
                numero_cage += 1
                
    return matrice_cages, dico_cages 

grille_generee, dico_cage = generation_structure_cages()


def mouvement_est_valide(grille_valeurs, grille_cages, ligne, colonne, valeur):
    dimension = len(grille_valeurs)
    numero_cage = grille_cages[ligne][colonne]
    
    # Vérifier que la valeur n'est pas déjà dans la même cage
    for l in range(dimension):
        for c in range(dimension):
            if grille_cages[l][c] == numero_cage and grille_valeurs[l][c] == valeur:
                return False
                
    # Vérifier les cases adjacentes 
    directions_adjacentes = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    for dl, dc in directions_adjacentes:
        nl, nc = ligne + dl, colonne + dc
        if 0 <= nl < dimension and 0 <= nc < dimension:
            if grille_valeurs[nl][nc] == valeur:
                return False
                
    return True


def resoudre_grille(grille_valeurs, grille_cages, dico_cages):
    dimension = len(grille_valeurs)
    
    # Chercher la première case vide 
    ligne_vide, col_vide = -1, -1
    for l in range(dimension):
        for c in range(dimension):
            if grille_valeurs[l][c] == 0:
                ligne_vide, col_vide = l, c
                break
        if ligne_vide != -1: break
    
    if ligne_vide == -1:
        return True
        
    # Récupérer la taille de la cage pour savoir jusqu'à quel chiffre on peut aller
    numero_cage = grille_cages[ligne_vide][col_vide]
    taille_cage = len(dico_cages[numero_cage])
    
    # Tester les chiffres possibles 
    for valeur_test in range(1, taille_cage + 1):
        if mouvement_est_valide(grille_valeurs, grille_cages, ligne_vide, col_vide, valeur_test):
            # Placer le chiffre
            grille_valeurs[ligne_vide][col_vide] = valeur_test
            
            #On continue
            if resoudre_grille(grille_valeurs, grille_cages, dico_cages):
                return True
            
            #Si cela mène à rien on revient en arrière    
            grille_valeurs[ligne_vide][col_vide] = 0
            
    return False

def grille_videe(grille_complete, nb_cases_a_conserver):
    """
    Prend une grille remplie et ne garde qu'un nombre précis de chiffres.
    """
    dimension = len(grille_complete)
    nouvelle_grille_videe = [[0 for _ in range(dimension)] for _ in range(dimension)]
    
    # On liste toutes les coordonnées possibles 
    toutes_les_positions = []
    for l in range(dimension):
        for c in range(dimension):
            toutes_les_positions.append((l, c))
            
    # On choisit au hasard les positions que l'on va garder
    nb_cases_max = dimension**2
    nb_a_garder = min(nb_cases_a_conserver, nb_cases_max)
    
    positions_selectionnees = random.sample(toutes_les_positions, nb_a_garder)
    
    # On garde uniquement les valeurs des positions sélectionnées
    for ligne, colonne in positions_selectionnees:
        nouvelle_grille_videe[ligne][colonne] = grille_complete[ligne][colonne]
        
    return nouvelle_grille_videe

cages, dico = generation_structure_cages()
print("Aperçu des cages générées :")
for ligne in cages:
    print(ligne)
        

#-------TEST-------

#Les cages : 
cages, dico = generation_structure_cages(4)

#la grille vide à résoudre
solution = [[0 for _ in range(4)] for _ in range(4)]
    
if resoudre_grille(solution, cages, dico):
    print("\nGrille solution :")
    for ligne in solution:
        print(ligne)
    
    print("\nGrille à résoudre :")
    puzzle = grille_videe(solution, 10 )
    for ligne in puzzle:
        print(ligne)
else:
    print("Échec")