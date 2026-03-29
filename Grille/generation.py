import random
import copy
import math
from Grille.verification import compter_solution_V3
from Grille.verification import compter_solution_kakuro
from Grille.verification import valider_masque_kakuro
from Grille.verification import trouver_groupes_horizontaux_kakuro
from Grille.verification import trouver_groupes_verticaux_kakuro

dictionnaire_liste_ligne = {}
dictionnaire_liste_colonne = {}
dictionnaire_liste_carre = {}

def generateur_grille_vide(dimension : int): 
    """
    Génère une matrice vide à la dimension démandée  
    """
    grille_vide = [[0] * dimension for i in range(dimension)]
    return(grille_vide)

def initialiser_dictionnaires(dimension : int):
    """
    Initialise les dictionnaires globaux contenant les valeurs possibles 
    pour chaque ligne, colonne et carré.
    
    Chaque dictionnaire contient une liste de chiffres de 1 à 'dimension'.
    Utilisé pour accélérer la recherche de candidats lors du remplissage
    """
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

def initialiser_dictionnaires_variantes(dimension : int):
    
    
    global dictionnaire_liste_ligne
    global dictionnaire_liste_colonne

    dictionnaire_liste_ligne = {}
    dictionnaire_liste_colonne = {}
    
    for i in range(dimension):
        dictionnaire_liste_ligne[i] = list(range(1, dimension + 1))
        dictionnaire_liste_colonne[i] = list(range(1, dimension + 1))

def remplir_grille_variante(dimension : int):
    """
    Génère une grille complète en utilisant un backtracking itératif.
    """
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

def generer_masque_kakuro(dimension, max_groupe=9): 
    """Génère un masque de Kakuro valide (0 = case blanche, 1 = case noire)."""
    grille = [[1 for _ in range(dimension)] for _ in range(dimension)]
    
    for ligne in range(dimension):
        colonne = 0
        while colonne < dimension:
            restant = dimension - colonne
            if restant < 2:
                break
            taille = random.randint(2, min(max_groupe, restant))
            for i in range(taille):
                grille[ligne][colonne + i] = 0
            colonne += taille
            if colonne < dimension:
                grille[ligne][colonne] = 1
                colonne += 1
    return grille

def remplir_grille_V2(dimension : int):
    """
    Génère une grille de Sudoku complète en utilisant une stratégie de 
    Backtracking optimisée.

    L'optimisation réside dans le choix des cases à traiter : en prenant celle qui à le moins de chiffres possibles.
    """
    racine = int(math.sqrt(dimension))

    grille = generateur_grille_vide(dimension)

    liste_ligne = [[True]*dimension for _ in range(dimension)]
    liste_colonne = [[True]*dimension for _ in range(dimension)]
    liste_carre = [[True]*dimension for _ in range(dimension)]

    essaie = [(i,e) for i in range(dimension) for e in range(dimension)]

    def solveur():
        if not essaie:
            return True

        indice_min = -1
        valeurs_possibles_min = []
        nb_valeurs_min = dimension + 1

        for idx, (ligne, colonne) in enumerate(essaie):
            numero_carre = (ligne//racine)*racine + (colonne//racine)
            candidats = [v for v in range(dimension)
                         if liste_ligne[ligne][v] and
                            liste_colonne[colonne][v] and
                            liste_carre[numero_carre][v]]

            nb_valeurs = len(candidats)
            if nb_valeurs < nb_valeurs_min:
                nb_valeurs_min = nb_valeurs
                valeurs_possibles_min = candidats
                indice_min = idx
            if nb_valeurs == 1:
                break

        if nb_valeurs_min == 0 or indice_min == -1:
            return False

        ligne, colonne = essaie.pop(indice_min)
        numero_carre = (ligne//racine)*racine + (colonne//racine)
        random.shuffle(valeurs_possibles_min)

        for i in valeurs_possibles_min:
            grille[ligne][colonne] = i + 1
            liste_ligne[ligne][i] = False
            liste_colonne[colonne][i] = False
            liste_carre[numero_carre][i] = False

            if solveur():
                return True

            # backtrack
            grille[ligne][colonne] = 0
            liste_ligne[ligne][i] = True
            liste_colonne[colonne][i] = True
            liste_carre[numero_carre][i] = True

        essaie.insert(indice_min, (ligne, colonne))
        return False

    if solveur():  
        return grille
    else:
        return None
        
def supprimer_valeur(grille_complete : list[list:int], nombre_valeur_a_supprimer : int, dimension : int):
    """
    Transforme notre grille pleine en un sudoku à remplir.
    Tout en s'assurant que le joueur n'aura toujours qu'une seule solution possible.

    Entrée : 
        grille_a_vider: Une grille de Sudoku complète.
        nombre_valeurs_a_supprimer: Le nombre de cases que l'on veut vider.
        dimension : taille de notre grille
    Sortie : 
        grille_vidée : Une grille de Sudoku prête à être resolue par l'utilisateur
    """
    
    grille_vidée = copy.deepcopy(grille_complete)
    positions = [(ligne, colonne) for ligne in range(dimension) for colonne in range(dimension)]
    random.shuffle(positions)

    nombre_case_supprime = 0

    while nombre_case_supprime < nombre_valeur_a_supprimer:
        if not positions:
            # plus de positions → recommence avec nouvelle grille
            if (nombre_valeur_a_supprimer - nombre_case_supprime) > 5:   
                return supprimer_valeur(remplir_grille(dimension), nombre_valeur_a_supprimer, dimension)
            else:
                return grille_vidée

        ligne, colonne = positions.pop()
        valeur_originale = grille_vidée[ligne][colonne]
        grille_vidée[ligne][colonne] = 0

        if compter_solution_V3(grille_vidée, dimension) == 1:
            nombre_case_supprime += 1
        else:
            grille_vidée[ligne][colonne] = valeur_originale

    return grille_vidée
