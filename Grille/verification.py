import math

def compter_solution_V3(grille, nombre_de_valeur, limite = 2):
    
    # Booléens pour savoir si une valeur est utilisée
    liste_ligne = [[True] * nombre_de_valeur for _ in range(nombre_de_valeur)]
    liste_colonne = [[True] * nombre_de_valeur for _ in range(nombre_de_valeur)]
    liste_carre = [[True] * nombre_de_valeur for _ in range(nombre_de_valeur)]
    
    racine = int(math.sqrt(nombre_de_valeur))
    essaie = []  # liste des cases vides
    compteur_de_solution = 0

    # Initialisation
    for ligne in range(nombre_de_valeur):
        for colonne in range(nombre_de_valeur):
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
        nb_valeurs_min = nombre_de_valeur + 1

        for idx, (ligne, colonne) in enumerate(essaie):
            numero_carre = (ligne // racine) * racine + (colonne // racine)
            
            valeurs_possibles = []

            for indice in range(nombre_de_valeur):
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

def compter_solution_V2(grille, nombre_de_valeur, limite=2):
    ligne = [0] * nombre_de_valeur
    colonne = [0] * nombre_de_valeur
    carre = [0] * nombre_de_valeur
    essaie = []
    racine = int(math.sqrt(nombre_de_valeur))

    for i in range (nombre_de_valeur): # séparation des case remplie des case vide
        for e in range (nombre_de_valeur):
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
        min_nombre_valeur_possible = nombre_de_valeur

        for h, (i, e) in enumerate(essaie): # enumeration de tout les couple h(indice dans la liste essaie) et des tuples (ligne, colonne)
            index_carre = (i // racine) * racine + (e // racine) # determination de l'indice du carre (de 0 a 8) (se représenter les carre et leur donner un numero de gauche à droite et de bas en haut
            bit_utilise = ligne[i] | colonne[e] | carre[index_carre] # determination des bit deja utilisé dans la ligne, colonne et carre de la valeur pour faire l'union des trois
            valeur_possible = (~bit_utilise) &  ((1 << nombre_de_valeur) - 1) # obtention de valeur possible par inversion de valeur interdite à valeur possible + limitation au 9 premier bits 
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

def est_valide(grille, ligne, colonne, valeur, nombre_de_valeur):
    if valeur in grille[ligne]: # Vérifie la ligne
        return False
    if any(grille[i][colonne] == valeur for i in range(nombre_de_valeur)):  # Vérifie la colonne
        return False
    ligne_0, colonne_0 = (ligne // int(math.sqrt(nombre_de_valeur))) * int(math.sqrt(nombre_de_valeur)), (colonne // int(math.sqrt(nombre_de_valeur))) * int(math.sqrt(nombre_de_valeur)) # Vérifie le carré 3x3
    return not any(grille[i][e] == valeur for i in range(ligne_0, ligne_0 + int(math.sqrt(nombre_de_valeur))) for e in range(colonne_0, colonne_0 + int(math.sqrt(nombre_de_valeur))))

def compter_solution_V1(grille, nombre_de_valeur, limite=2):
    compteur = [0] # Compte le nombre de solutions, s'arrête dès qu'on atteint la limite
    def resoudre():  
        if compteur[0] >= limite:
            return
        for i in range(nombre_de_valeur):
            for e in range(nombre_de_valeur):
                if grille[i][e] == 0:
                    for valeur in range(1, nombre_de_valeur + 1):
                        if est_valide(grille, i, e, valeur, nombre_de_valeur):
                            grille[i][e] = valeur
                            resoudre()
                            grille[i][e] = 0
                    return # case vide sans solution valide
        compteur[0] += 1 # grille complète trouvée
    resoudre()
    return compteur[0]
