import random
import copy
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
        nombre_de_doublons_ligne = random.randint(1, n // 3) # Choisis aléatoirement le nombre de doublons dans la liste
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

def compter_solution(grille):
    n = len(grille)
    liste_doublons = []
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                if grille[i][j] == grille[i][k]:
                    liste_doublons.append(((i, j), (i, k)))

    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                if grille[j][i] == grille[k][i]:
                    liste_doublons.append(((j, i), (k, i)))
