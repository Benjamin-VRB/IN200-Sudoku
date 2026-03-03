import random
import math

dictionnaire_liste_ligne = {}
dictionnaire_liste_colonne = {}

def generateur_grille_vide(nombre_de_valeur): 
    grille_vide = [[0] * nombre_de_valeur for i in range(nombre_de_valeur)]
    return(grille_vide)
def initialiser_dictionnaires(nombre_de_valeur):
    
    global dictionnaire_liste_ligne
    global dictionnaire_liste_colonne

    dictionnaire_liste_ligne = {}
    dictionnaire_liste_colonne = {}
    
    for i in range(nombre_de_valeur):
        dictionnaire_liste_ligne[i] = list(range(1, nombre_de_valeur + 1))
        dictionnaire_liste_colonne[i] = list(range(1, nombre_de_valeur + 1))

def remplir_grille(nombre_de_valeur):
    
    racine = int(math.sqrt(nombre_de_valeur))
    grille = generateur_grille_vide(nombre_de_valeur)
    initialiser_dictionnaires(nombre_de_valeur)
    essais = [[[] for _ in range(nombre_de_valeur)] for _ in range(nombre_de_valeur)]  # valeurs déjà essayées par les cases
    ligne = 0
    colonne = 0
    
    while ligne < nombre_de_valeur:
        candidats = list(set(dictionnaire_liste_ligne[ligne]) & set(dictionnaire_liste_colonne[colonne]) - set(essais[ligne][colonne])) # Candidats = intersection des listes disponibles en retirant les valeurs déjà essayées
        
        if not candidats: # Pas de candidat : on remet les essais à zéro pour cette case et on recule
            essais[ligne][colonne] = []
            
            if colonne >= 1: # si on est pas sur la première colonne on recule de une colonne
                colonne -= 1
            
            else: # sinon on remonte à la ligne de dessus et on se met sur la dernière colonne de la ligne
                ligne -= 1
                colonne = nombre_de_valeur - 1
            
            if ligne < 0: 
                return None 
            val_precedente = grille[ligne][colonne] # On rerajoute la valeur de la case précédente dans les listes
            essais[ligne][colonne].append(val_precedente)  # on mémorise qu'elle a échoué
            dictionnaire_liste_ligne[ligne].append(val_precedente) # on rerajoute la valeur testé dans les liste de choix possible car on retourne en arrière
            dictionnaire_liste_colonne[colonne].append(val_precedente)
            grille[ligne][colonne] = 0 
        
        else:
            valeur = random.choice(candidats) # On choisit une valeur et on avance
            grille[ligne][colonne] = valeur
            dictionnaire_liste_ligne[ligne].remove(valeur) # on retire la valeur tenté des choix possibles
            dictionnaire_liste_colonne[colonne].remove(valeur)
            
            if colonne == nombre_de_valeur - 1: 
                ligne += 1
                colonne = 0
            
            else:
                colonne += 1
    
    return (grille)

def permuter_valeurs(grille):
    n = len(grille)
    for i in range(n):
        nombre_de_doublons_ligne = random.randint(1, n // 4) # Choisis aléatoirement le nombre de doublons dans la liste
        colonnes_disponibles = list(range(n)) # Liste permettant qu'une permutation ne se répète pas deux fois

        for i in range(nombre_de_doublons_ligne):
            if len(colonnes_disponibles) < 2:
                break  

            colonne_source = random.choice(colonnes_disponibles) # Choisir deux colonnes différentes
            colonnes_disponibles.remove(colonne_source)
            colonne_cible = random.choice(colonnes_disponibles)
            colonnes_disponibles.remove(colonne_cible)
            grille[i][colonne_cible] = grille[i][colonne_source] # Permuter les valeurs

        nombre_de_doublons_colonne = random.randint(1, n // 3) # Choisis aléatoirement le nombre de doublons dans la liste
        lignes_disponibles = list(range(n)) # Liste permettant qu'une permutation ne se répète pas deux fois

        for i in range(nombre_de_doublons_colonne):
            if len(lignes_disponibles) < 2:
                break  

            ligne_source = random.choice(lignes_disponibles) # Choisir deux colonnes différentes
            lignes_disponibles.remove(ligne_source)
            ligne_cible = random.choice(lignes_disponibles)
            lignes_disponibles.remove(ligne_cible)
            grille[i][ligne_cible] = grille[i][ligne_source] # Permuter les valeurs

    return grille

def verifier_case_adjacentes(case, grille_couleur_de_case):
    i, j = case
    if grille_couleur_de_case[i][j] == 1:
        return False

    n = len(grille_couleur_de_case)
    if i > 0 and grille_couleur_de_case[i-1][j] == 1: # Vérification du voisin du haut
        return False
    
    if i < n-1 and grille_couleur_de_case[i+1][j] == 1: # Vérification voisin du bas
        return False
    
    if j > 0 and grille_couleur_de_case[i][j-1] == 1: # Vérification du voisin de gauche
        return False
    
    if j < n-1 and grille_couleur_de_case[i][j+1] == 1: # vérification du voisin de droite
        return False
    return True


def verifier_case_reliée(grille_couleur_de_case): # fonction qui vérifie si toutes les cases blanches sont reliées entre elles.
    n = len(grille_couleur_de_case)
    case_blanche_trouvée = False
    for i in range(n):           # Recherche d'une case blanche
        for j in range(n):
            if grille_couleur_de_case[i][j] == 0:  # Si on trouve une case blanche, on initialise notre recherche à cette case.
                début_ligne = i
                début_colonne = j                  
                case_blanche_trouvée = True
                break
        if case_blanche_trouvée:
            break

    if case_blanche_trouvée == False:   # Si il n'y a pas de case blanche, on s'arrête car c'est impossible.
        return False    

    case_visitée = [[False for i in range(n)] for i in range(n)] # Liste des cases visitées
    case_a_verifier = [(début_ligne , début_colonne)] # Liste des cases reconnus à vérifier
    while len(case_a_verifier) > 0:
        i, j = case_a_verifier[0]
        case_a_verifier.remove((i, j))
        
        if case_visitée[i][j] :
            continue

        case_visitée[i][j] = True
        if i > 0 and grille_couleur_de_case[i-1][j] == 0 and not case_visitée[i-1][j]: # vérification du voisin du haut 
            case_a_verifier.append((i-1, j))

        if i < n-1 and grille_couleur_de_case[i+1][j] == 0 and not case_visitée[i+1][j]: # vérification du voisin du bas
            case_a_verifier.append((i+1, j))

        if j > 0 and grille_couleur_de_case[i][j-1] == 0 and not case_visitée[i][j-1]: # vérification du voisin de gauche
            case_a_verifier.append((i, j-1))

        if j < n-1 and grille_couleur_de_case[i][j+1] == 0 and not case_visitée[i][j+1]: # vérification du voisin de droite
            case_a_verifier.append((i, j+1))

    for i in range(n):  # On vérifie si toutes les cases ont été visitées
        for j in range(n):
            if grille_couleur_de_case[i][j] == 0 and not case_visitée[i][j]:
                return False

    return True # Toutes les cases blanches sont connectées


def vérifier_validité_d_une_grille(grille_couleurs_de_case):
    if verifier_case_adjacentes(grille_couleurs_de_case) and verifier_case_reliée(grille_couleurs_de_case):
        return True


def compter_solution(grille):
    n = len(grille)
    compteur_de_solution = 0
    Grille_case_noire = [[0 for i in range(n)] for j in range(n)]

    cases_doublon = [] # On cherche les cases qui représentent des doublons.

    for i in range(n):    # Dans les lignes
        valeurs_vues = {}
        for j in range(n):
            valeur = grille[i][j]
            if valeur not in valeurs_vues:
                valeurs_vues[valeur] = []
            valeurs_vues[valeur].append(j)
        for positions in valeurs_vues.values():
            if len(positions) > 1:
                for col in positions:
                    if (i, col) not in cases_doublon:
                        cases_doublon.append((i, col))

    for j in range(n):  # Dans les colonnes.
        valeurs_vues = {}
        for i in range(n):
            valeur = grille[i][j]
            if valeur not in valeurs_vues:
                valeurs_vues[valeur] = []
            valeurs_vues[valeur].append(i)
        for positions in valeurs_vues.values():
            if len(positions) > 1:
                for ligne in positions:
                    if (ligne, j) not in cases_doublon:
                        cases_doublon.append((ligne, j))


    def verifier_absence_de_doublon_case(ligne, colonne): # Fonction qui recherche si il reste des doublons. Utile pour le comptage de solutions.
        valeur = grille[ligne][colonne]     # Dans les lignes
        for j in range(n):
            if j != colonne and Grille_case_noire[ligne][j] == 0:
                if grille[ligne][j] == valeur:
                    return False
        for i in range(n):                  # Dans les colonnes.
            if i != ligne and Grille_case_noire[i][colonne] == 0:
                if grille[i][colonne] == valeur:
                    return False
        return True

    
    def chercher_solution(index):   # Fonction qui recherche les solutions et qui les compte
        nonlocal compteur_de_solution
        if compteur_de_solution > 1:
            return
        if index == len(cases_doublon):
            if verifier_case_reliée(Grille_case_noire):
                compteur_de_solution += 1
            return
        ligne, colonne = cases_doublon[index]

        if verifier_absence_de_doublon_case(ligne, colonne):  # Test en laissant la case blanche
            chercher_solution(index + 1)

        if verifier_case_adjacentes((ligne, colonne), Grille_case_noire): # Test en noircissant la case
            Grille_case_noire[ligne][colonne] = 1
            chercher_solution(index + 1)
            Grille_case_noire[ligne][colonne] = 0

    
    chercher_solution(0)    # On lance la recherche de soultions.
    return compteur_de_solution == 1

taille = 10
solution_unique_trouvee = False

while not solution_unique_trouvee:

    grille = remplir_grille(taille)

    if grille is not None:
        grille = permuter_valeurs(grille)

        if compter_solution(grille):
            solution_unique_trouvee = True

for ligne in grille:
    print(ligne)