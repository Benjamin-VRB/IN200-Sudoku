import math
from Grille.kenken import verifier_cage
from Grille.affichage_cases_contraintes import afficher_contraintes_kakuro 

####       Fonctions "de base" lignes/colonnes       ####


def verification_lignes_colonnes(grille: list[list[int]], coord: tuple[int, int], liste_cases_invalides):
    """"Vérifie que la valeur qui vient dêtre saisie vérifie les conditions lignes et colonnes du Sudoku.
    
    Entrée:
        La grille de sudoku, les coordonnées de la case venant d'ête remplie, et une liste (qui sera 
        une liste vide)."""
    
    dimension = len(grille)
    ligne = coord[0]
    colonne = coord[1]
    valeur = grille[ligne][colonne]

    liste_indices_lignes = [i for i in range(dimension)]   # Liste des indices des lignes a tester.
    liste_indices_lignes.remove(ligne)                     # à laquelle on enlève l'indice de la case venant d'être remplie.

    for i in liste_indices_lignes:
        if grille[i][colonne] == valeur:
            liste_cases_invalides.append((i, colonne))     # On regarde dans toute la ligne.


    liste_indices_colonnes = [i for i in range(dimension)]  # Liste des indices des colonnes a tester.
    liste_indices_colonnes.remove(colonne)                  # à laquelle on enlève l'indice de la case venant d'être remplie.

    for i in liste_indices_colonnes:
        if grille[ligne][i] == valeur:
            liste_cases_invalides.append((ligne, i))        # On regarde dans toute la colonne



def verification_carre_Sudoku(grille: list[list[int]], coord: tuple[int, int], liste_cases_invalides):
    """Vérifie que la valeur qui vient dêtre saisie vérifie la condition carré du Sudoku.
    
    Entrée:
        La grille de sudoku, les coordonnées de la case venant d'ête remplie, et une liste (qui sera 
        une liste vide)."""

    dimension = len(grille)
    liste_cases_invalides = []     

    ligne = coord[0]
    colonne = coord[1]
    valeur = grille[ligne][colonne]

    taille_bloc = int(math.sqrt(dimension))                 # calcul de la taille d'un carré

    debut_ligne = (ligne // taille_bloc) * taille_bloc          # On regarde dans quel bloc se trouve la case qu'on vient de remplir
    debut_colonne = (colonne // taille_bloc) * taille_bloc

    for i in range(debut_ligne, debut_ligne + taille_bloc):           # On teste toutes les cases de ce bloc.
        for j in range(debut_colonne, debut_colonne + taille_bloc):
            if (i, j) != coord and grille[i][j] == valeur:
                liste_cases_invalides.append((i, j))




####       Sudoku classique       ####

def verification_sudoku_classique_complet(grille: list[list[int]], coord: tuple[int, int]):
    """"Vérifie que la valeur qui vient dêtre saisie vérifie toutes les conditions du Sudoku.
    
    Entrée:
        La grille de sudoku et les coordonnées de la case venant d'ête remplie.
    Sortie:
        Renvoie la liste de toutes les cases pour lesquelles cette valeur ne fonctionne pas."""

    liste_cases_invalides = []
    verification_lignes_colonnes(grille, coord, liste_cases_invalides)  # Vérification des lignes et ds colonnes.
    verification_carre_Sudoku(grille, coord, liste_cases_invalides)    # Vérification des carrés.
    return liste_cases_invalides




####       Variante Kenken       ####


def verification_cages_kenken(grille, dictionnaire_cages):
    """Vérifie que les cages vérifient toujours les informations requises sur les opérations.
    
    Entrée:
        La grille de sudoku ainsi que le dictionnaire contenant les informations sur les cages."""

    for cage in dictionnaire_cages.values():
        if not verifier_cage(grille, cage):   #Vérifie si toutes les cages correspondent bien aux informations du dictionnaire.
            return cage
    return True


def verification_kenken(grille, coord, dictionnaire_cages):
    """"Vérifie que la valeur qui vient dêtre saisie vérifie toutes les conditions du Kenken.
    
    Entrée:
        La grille de sudoku, les coordonnées de la case venant d'ête remplie et un dictionnaire contenenant
        les informations du kenken.
    Sortie:
        Renvoie la liste de toutes les cases et cages pour lesquelles cette valeur ne fonctionne pas."""

    liste_cases_invalides = []
    verification_lignes_colonnes(grille, coord, liste_cases_invalides)      # vérification des lignes et des colonnes.
    verif = verification_cages_kenken(grille, dictionnaire_cages)         # Vérifications des cages du kenken

    if  liste_cases_invalides != [] and verif:         # traitement des différents cas.
        return liste_cases_invalides
    
    elif liste_cases_invalides != []:
        return liste_cases_invalides, verif
    
    elif liste_cases_invalides == [] and verif:
        return
    
    elif liste_cases_invalides == []:
        return verif



####       Variante Sudoku consécutif       ####

def verification_consecutif(grille, coord, liste_doublons_consecutifs, liste_cases_invalides):
    """Vérifie que tous les doublons de cases censés être consecutives le sont bien.
    
    Entrée:
        Les coordonnées de la cases venant d'être remplie,
        la liste des doublons consecutifs et une liste (initialement vide) qui contiendra les cases
        pour lesquelles cela ne marche pas.
    Sortie:
        Renvoie la liste des cases pour lesquelles la case qui vient d'être saisie ne fonctionne pas."""
    
    for doublons in liste_doublons_consecutifs:     # On regarde dans chaques doublons.
        for j in doublons:                         # Si la case venant d'être saisie fait partie de la liste des doublons.
            if coord == j:                     
                if j == doublons[0]:                   # On "repère la deuxième case du doublon s'il il existe"
                    deuxieme_case = doublons[1]
                elif j == doublons[1]:
                    deuxieme_case = doublons[0]

                if abs(grille[j[0]][j[1]] - grille[deuxieme_case[0]][deuxieme_case[1]]) != 1:          # On regarde si les valeurs sont bien adjacentes
                    liste_cases_invalides.append(deuxieme_case)
                    return liste_cases_invalides        # Si elles ne le sont pas on rajoute l'autre case dans la liste des cases invalides.
    return liste_cases_invalides
    

def verification_sudoku_consecutif(grille, coord, liste_doublons_consecutifs):
    """Vérifie que toutes les conditions du sudoku consecutif sont bien respectées..
    
    Entrée:
        La grille en cours de remplissage, les coordonnées de la cases venant d'être remplie,
        la liste des doublons consecutifs.
    Sortie:
        Renvoie la liste des cases pour lesquelles la case qui vient d'être saisie ne fonctionne pas."""
    
    liste_cases_invalides = []
    verification_lignes_colonnes(grille, coord, liste_cases_invalides)        # Verifie les lignes et les colonnes
    verification_carre_Sudoku(grille, coord, liste_cases_invalides)              # Verifie les carrés
    verification_consecutif(coord, liste_doublons_consecutifs, liste_cases_invalides)     # Vérifie les cases consécutive
    return liste_cases_invalides        # Renvoie la liste des cases invalides.

#### Variante Kakuro ####

def analyser_erreurs(grille_joueur, grille_indices, r, c):
    """Retourne un set de coordonnées (r, c) qui violent une règle."""
    segments = afficher_contraintes_kakuro(grille_indices, r, c)
    cases_rouges = set()

    for cle in ['h', 'v']:
        info = segments[cle]
        cases_du_groupe = info['cases']
        cible = info['cible']
        
        somme_actuelle = 0
        remplies = 0
        doublons = {} # Valeur -> Coordonnée

        for (curr_r, curr_c) in cases_du_groupe:
            val = grille_joueur[curr_r][curr_c]
            
            if val != 0 and val != ".":
                somme_actuelle += int(val)
                remplies += 1
                
                # Règle 1 : Pas de doublons
                if val in doublons:
                    cases_rouges.add((curr_r, curr_c))
                    cases_rouges.add(doublons[val])
                else:
                    doublons[val] = (curr_r, curr_c)

        # Règle 2 : La somme ne doit jamais dépasser l'indice
        if somme_actuelle > cible:
            cases_rouges.update(cases_du_groupe)
        
        # Règle 3 : Si groupe plein, la somme doit être exacte
        elif remplies == len(cases_du_groupe) and somme_actuelle != cible:
            cases_rouges.update(cases_du_groupe)

    return cases_rouges