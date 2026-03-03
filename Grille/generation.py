import random
import copy
import math
from verification import compter_solution_V3
from verification import compter_solution_kakuro
from verification import valider_masque

dictionnaire_liste_ligne = {}
dictionnaire_liste_colonne = {}
dictionnaire_liste_carre = {}

def generateur_grille_vide(dimension): 
    grille_vide = [[0] * dimension for i in range(dimension)]
    return(grille_vide)

def initialiser_dictionnaires(dimension):
    racine = int(math.sqrt(dimension))
    carre = int(racine)
    
    global dictionnaire_liste_ligne
    global dictionnaire_liste_colonne
    global dictionnaire_liste_carre

    dictionnaire_liste_ligne = {}
    dictionnaire_liste_colonne = {}
    dictionnaire_liste_carre = {}
    
    for i in range(dimension):
        dictionnaire_liste_ligne[i] = list(range(1, dimension + 1))
        dictionnaire_liste_colonne[i] = list(range(1, dimension + 1))
    
    for i in range(carre):
        dictionnaire_liste_carre[i] = {}
        
        for e in range(carre):
            dictionnaire_liste_carre[i][e] = list(range(1, dimension + 1))

def initialiser_dictionnaires_variantes(dimension):
    
    global dictionnaire_liste_ligne
    global dictionnaire_liste_colonne

    dictionnaire_liste_ligne = {}
    dictionnaire_liste_colonne = {}
    
    for i in range(dimension):
        dictionnaire_liste_ligne[i] = list(range(1, dimension + 1))
        dictionnaire_liste_colonne[i] = list(range(1, dimension + 1))

def remplir_grille_variante(dimension):
    
    racine = int(math.sqrt(dimension))
    grille = generateur_grille_vide(dimension)
    initialiser_dictionnaires(dimension)
    essais = [[[] for _ in range(dimension)] for _ in range(dimension)]  # valeurs déjà essayées par les cases
    ligne = 0
    colonne = 0
    
    while ligne < dimension:
        candidats = list(set(dictionnaire_liste_ligne[ligne]) & set(dictionnaire_liste_colonne[colonne]) - set(essais[ligne][colonne])) # Candidats = intersection des listes disponibles en retirant les valeurs déjà essayées
        
        if not candidats: # Pas de candidat : on remet les essais à zéro pour cette case et on recule
            essais[ligne][colonne] = []
            
            if colonne >= 1: # si on est pas sur la première colonne on recule de une colonne
                colonne -= 1
            
            else: # sinon on remonte à la ligne de dessus et on se met sur la dernière colonne de la ligne
                ligne -= 1
                colonne = dimension - 1
            
            if ligne < 0: 
                return None 
            val_precedente = grille[ligne][colonne] # On rerajoute la valeur de la case précédente dans les listes
            essais[ligne][colonne].append(val_precedente)  # on mémorise qu'elle a échoué
            dictionnaire_liste_ligne[ligne].append(val_precedente) # on rerajoute la valeur testé dans les liste de choix possible car on retourne en arrière
            dictionnaire_liste_colonne[colonne].append(val_precedente)
            grille[ligne][colonne] = 0 
        
        else:
            valeur = (random.choice(candidats)) # On choisit une valeur et on avance
            grille[ligne][colonne] = valeur
            dictionnaire_liste_ligne[ligne].remove(valeur) # on retire la valeur tenté des choix possibles
            dictionnaire_liste_colonne[colonne].remove(valeur)
            
            if colonne == dimension - 1: 
                ligne += 1
                colonne = 0
            
            else:
                colonne += 1
    
    return (grille)


def remplir_grille(dimension):
    
    racine = int(math.sqrt(dimension))
    grille = generateur_grille_vide(dimension)
    initialiser_dictionnaires(dimension)
    essais = [[[] for _ in range(dimension)] for _ in range(dimension)]  # valeurs déjà essayées par les cases
    ligne = 0
    colonne = 0
    
    while ligne < dimension:
        candidats = list(set(dictionnaire_liste_ligne[ligne]) & set(dictionnaire_liste_colonne[colonne]) & set(dictionnaire_liste_carre[ligne//racine][colonne//racine]) - set(essais[ligne][colonne])) # Candidats = intersection des listes disponibles en retirant les valeurs déjà essayées
        
        if not candidats: # Pas de candidat : on remet les essais à zéro pour cette case et on recule
            essais[ligne][colonne] = []
            
            if colonne >= 1: # si on est pas sur la première colonne on recule de une colonne
                colonne -= 1
            
            else: # sinon on remonte à la ligne de dessus et on se met sur la dernière colonne de la ligne
                ligne -= 1
                colonne = dimension - 1
            
            if ligne < 0: 
                return None 
            val_precedente = grille[ligne][colonne] # On rerajoute la valeur de la case précédente dans les listes
            essais[ligne][colonne].append(val_precedente)  # on mémorise qu'elle a échoué
            dictionnaire_liste_ligne[ligne].append(val_precedente) # on rerajoute la valeur testé dans les liste de choix possible car on retourne en arrière
            dictionnaire_liste_carre[ligne//racine][colonne//racine].append(val_precedente)
            dictionnaire_liste_colonne[colonne].append(val_precedente)
            grille[ligne][colonne] = 0 
        
        else:
            valeur = random.choice(candidats) # On choisit une valeur et on avance
            grille[ligne][colonne] = valeur
            dictionnaire_liste_ligne[ligne].remove(valeur) # on retire la valeur tenté des choix possibles
            dictionnaire_liste_colonne[colonne].remove(valeur)
            dictionnaire_liste_carre[ligne//racine][colonne//racine].remove(valeur)
            
            if colonne == dimension - 1: 
                ligne += 1
                colonne = 0
            
            else:
                colonne += 1
    
    return (grille)

def supprimer_valeur(grille_complete, nombre_valeur_a_supprimer, dimension):
    grille_vider = copy.deepcopy(grille_complete)
    positions = [(ligne, colonne) for ligne in range(dimension) for colonne in range(dimension)]
    random.shuffle(positions)

    nombre_case_supprime = 0

    while nombre_case_supprime < nombre_valeur_a_supprimer:
        if not positions:
            # plus de positions → recommence avec nouvelle grille
            if (nombre_valeur_a_supprimer - nombre_case_supprime) > 5:   
                return supprimer_valeur(remplir_grille(dimension), nombre_valeur_a_supprimer, dimension)
            else:
                return grille_vider

        ligne, colonne = positions.pop()
        valeur_originale = grille_vider[ligne][colonne]
        grille_vider[ligne][colonne] = 0

        if compter_solution_V3(grille_vider, dimension) == 1:
            nombre_case_supprime += 1
        else:
            grille_vider[ligne][colonne] = valeur_originale

    return grille_vider

def generer_masque(dimension, taux_noir=0.3, max_groupe=9):

    while True:

        grille = [[0 for _ in range(dimension)] for _ in range(dimension)]

        for ligne in range(dimension):
            for colonne in range(dimension):
                if random.random() < taux_noir:
                    grille[ligne][colonne] = 1

        if valider_masque(grille, dimension, max_groupe):
            return grille

def trouver_groupes_horizontaux(grille, dimension):
    groupes = []

    for ligne in range(dimension):
        colonne = 0
        while colonne < dimension:

            if grille[ligne][colonne] == 1:
                colonne += 1
                continue

            debut = colonne

            while colonne < dimension and grille[ligne][colonne] == 0:
                colonne += 1

            if colonne - debut >= 2:
                groupes.append([(ligne, c) for c in range(debut, colonne)])

    return groupes
    
    
def trouver_groupes_verticaux(grille, dimension):
    groupes = []

    for colonne in range(dimension):
        ligne = 0

        while ligne < dimension:

            # Si case noire → on avance
            if grille[ligne][colonne] == 1:
                ligne += 1
                continue

            debut = ligne

            # Avancer tant que case blanche
            while ligne < dimension and grille[ligne][colonne] == 0:
                ligne += 1

            # Vérifier taille ≥ 2
            if ligne - debut >= 2:
                groupes.append([(l, colonne) for l in range(debut, ligne)])

    return groupes

def generer_kakuro(grille, dimension):

    while True:

        # Génération masque valide
        grille_masque = generer_masque(dimension)

        if not valider_masque(grille_masque, dimension):
            continue

        # Trouver groupes
        groupes_horizontaux = trouver_groupes_horizontaux(grille_masque, dimension)
        groupes_verticaux = trouver_groupes_verticaux(grille_masque, dimension)

        # Sécurité minimale
        if not groupes_horizontaux or not groupes_verticaux:
            continue

        # Calcul des sommes à partir de la solution complète
        somme_horizontale = [sum(grille[l][c] for (l, c) in groupe) for groupe in groupes_horizontaux]   

        somme_verticale = [sum(grille[l][c] for (l, c) in groupe) for groupe in groupes_verticaux]  

        # Construction du puzzle vide
        puzzle = [[None for _ in range(dimension)] for _ in range(dimension)]

        # Placer cases noires
        for l in range(dimension):
            for c in range(dimension):
                if grille_masque[l][c] == 1:
                    puzzle[l][c] = {"type": "noire", "H": None, "V": None}
                else:
                    puzzle[l][c] = {"type": "blanche", "valeur": 0}

        # Placer les sommes horizontales
        for i, groupe in enumerate(groupes_horizontaux):
            l, c = groupe[0]
            if c > 0 and puzzle[l][c-1]["type"] == "noire":
                puzzle[l][c-1]["H"] = somme_horizontale[i]

        # Placer les sommes verticales
        for i, groupe in enumerate(groupes_verticaux):
            l, c = groupe[0]
            if l > 0 and puzzle[l-1][c]["type"] == "noire":
                puzzle[l-1][c]["V"] = somme_verticale[i]

        # Vérifier unicité
        nb_solutions = compter_solution_kakuro(puzzle, dimension, groupes_verticaux, groupes_horizontaux, limite=2)
            
        if nb_solutions == 1:
            return puzzle

print(remplir_grille_variante(9),)
    
    


