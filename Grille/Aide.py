import random

import Sudoku_Irregulier as irregulier


def verificateur_ligne_colonne(valeur,dimension,grille,ligne,colonne): 
 
    #verification de la lignes : 
    if valeur in grille[ligne]:
        return False
    #verification de la colonnes : 
    for i in range(dimension):
        if valeur == grille[i][colonne]:
                return False
    return True

def indicateur_Sudoku(grille_actuelle : list[list:int],grille_solution : list[list:int],dimension : int):
    """permet d'indiquer à l'utilisateur une case"""
    Cases_vides= [(l,c) for l in range(dimension) for c in range(dimension) if grille_actuelle[l][c] == 0]
    
    #eviter de donner toujours les cases en haut à gauche 
    random.shuffle(Cases_vides)

    for l,c in Cases_vides : 
        
        #pour regler le probleme de l'unicite on recupere directement la solution attendue
        solution_attendue = grille_solution[l][c]

        #on verifie si cela est possible avec la grille actuelle
        if verificateur_ligne_colonne(solution_attendue,dimension,grille_actuelle,l,c): 
            return  solution_attendue,(l,c)
    
    return None

def indicateur_kenken(dimension,grille_actuelle):
    grille_valeurs = grille_actuelle[0]
    dico_cage = grille_actuelle[1]

    #determination des cases libres :
    cases_libres= []
    for i in range(dimension):
        for j in range(dimension):
            if grille_valeurs[i][j] == 0 : 
                cases_libres.append((i,j))
    
    for l,c in cases_libres :
        for valeur in range(1, dimension +1): 
        
            if not verificateur_ligne_colonne(valeur,dimension,grille_valeurs,l,c) : 
                continue

            #On l'ajoute pour l'instant dans la grille : 
            grille_tempo = [ligne[:] for ligne in grille_valeurs]
            grille_tempo[l][c] = valeur

            #Retrouver sa cage : 
            cage= None

            for cage_test in dico_cage.values():
                if (l,c) in cage_test["cases"] : 
                    cage = cage_test
                    break

            #validité de la cage trouvée : 
            valeurs = []
            cage_incomplete = False
            operation = cage["opération"]
            resultat = cage["résultat"]
            cases = cage["cases"]
            
            for (i,j) in cases:  
                if grille_tempo[i][j] == 0:
                    cage_incomplete = True
                    break
                valeurs.append(grille_tempo[i][j])
            
            if cage_incomplete: 
                continue

            if operation == "+":     # Test pour le cas d'une somme
                if sum(valeurs) == resultat :
                    return valeur, (l,c)

            if operation == "*":     # Test pour le cas s'un produit
                produit = 1
                for v in valeurs:
                    produit *= v
                if produit == resultat : 
                    return valeur, (l,c)

            if operation == "-":     # Test pour le cas d'une différence
                a,b = valeurs
                if abs(a-b) == resultat : 
                    return valeur, (l,c)

            if operation == "/":     # test pour le cas d'un quotient
                a,b = valeurs
                if max(a,b) // min(a,b) == resultat : 
                    return valeur, (l,c)
                
                #Reste à faire le cas ou aucune case est pleine
    return 'aucune valeur'


def indicateur_irregulier(grille_actuelle,dico_cage,dimension=9):

    valeurs =list(range(1,dimension+1))

    for l in range(dimension):
        for c in range(dimension):
            if grille_actuelle[l][c] == 0:
                for val in valeurs : 
                    if irregulier.est_placement_valide(grille_actuelle, dico_cage, l, c, val):
                        return (l,c),val



def indicateur_kakuro():
    return


#test : 

dico_cage = {1: [(7, 8), (8, 8), (8, 7), (8, 6), (7, 7), (7, 6), (6, 7), (6, 6), (5, 6)], 2: [(6, 0), (7, 0), (8, 0), (5, 0), (8, 1), (7, 1), (4, 0), (4, 1), (3, 1)], 3: [(8, 4), (8, 5), (8, 3), (8, 2), (7, 3), (7, 2), (7, 5), (7, 4), (6, 5)], 4: [(0, 4), (1, 4), (1, 3), (1, 2), (2, 4), (3, 4), (2, 3), (2, 2), (3, 2)], 5: [(5, 8), (6, 8), (4, 8), (3, 8), (2, 8), (1, 8), (1, 7), (5, 7), (2, 7)], 6: [(4, 5), (4, 4), (5, 4), (5, 5), (3, 5), (4, 6), (4, 7), (6, 4), (3, 7)], 7: [(0, 3), (0, 2), (0, 1), (0, 0), (1, 1), (1, 0), (2, 0), (3, 0), (2, 1)], 8: [(1, 5), (0, 5), (0, 6), (0, 7), (0, 8), (2, 5), (1, 6), (2, 6), (3, 6)], 9: [(4, 3), (5, 3), (5, 2), (5, 1), (6, 1), (6, 2), (6, 3), (3, 3), (4, 2)]}
grille_à_résoudre = [[7, 0, 9, 0, 0, 5, 8, 0, 6], [5, 0, 0, 0, 2, 3, 0, 0, 0], [3, 8, 0, 1, 0, 0, 0, 0, 0], [0, 0, 8, 0, 3, 6, 9, 0, 0], [9, 0, 4, 0, 6, 0, 0, 0, 0], [0, 0, 0, 6, 0, 2, 0, 0, 4], [0, 4, 2, 0, 0, 0, 0, 0, 7], [0, 7, 0, 0, 0, 0, 5, 1, 0], [0, 2, 5, 0, 0, 4, 3, 0, 0]]

print(indicateur_irregulier(grille_à_résoudre,dico_cage))