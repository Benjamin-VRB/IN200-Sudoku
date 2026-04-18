import random




def voisins_vides(ligne,colonne,grille,dimension):
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


def generation_grille(dimension=9):
    """
    Génère une grille de Suguru vide avec ses cages.
    Retourne la matrice de la grille et le dictionnaire des cages.
    """
    
    grille = []
    grille = [ [0 for _ in range(dimension)] for _ in range(dimension)]

    cages = {}
    numero_cage = 1

    for ligne in range(dimension):
        for colonne in range(dimension): 
            
            # Si la case n'appartient encore à aucune cage
            if grille[ligne][colonne] == 0: 
                
                taille_voulue = random.randint(1, 5)
                cage_actuelle = [(ligne, colonne)]
                grille[ligne][colonne] = numero_cage

                # Agrandissement de la cage
                for etape in range(taille_voulue - 1):
                    options_possibles = []

                    # On cherche les voisins pour chaque case de notre cage en construction
                    for case_l, case_c in cage_actuelle:
                        voisins = voisins_vides(case_l, case_c, grille, dimension)
                        
                        for case_voisine in voisins:
                            if case_voisine not in options_possibles:
                                options_possibles.append(case_voisine)
                    
                    # Si la liste est vide on arrête la boucle
                    if len(options_possibles) == 0:
                        break

                    nouvelle_l, nouvelle_c = random.choice(options_possibles)
                    
                    # On met à jour la grille et notre liste
                    grille[nouvelle_l][nouvelle_c] = numero_cage
                    cage_actuelle.append((nouvelle_l, nouvelle_c))

                cages[numero_cage] = cage_actuelle
                numero_cage += 1
                
    return grille, cages

grille_generee, dico_cage = generation_grille()

#Test
for ligne in grille_generee:
    print(ligne)


