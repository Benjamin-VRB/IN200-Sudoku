import tkinter as tk

def preparer_cases_GUI(grille_kakuro):
    """
    Agit comme un traducteur entre le "cerveau" du jeu et l'interface graphique.
    
    L'idée est de prendre notre grille brute (les entiers et les listes) et de 
    créer une petite "fiche" (dictionnaire) pour chaque case. Sur cette fiche, 
    on prépare des cases vides (les 'None') pour stocker plus tard les numéros 
    d'identification des objets que Tkinter va dessiner.
    """
    liste_cases = []
    taille = len(grille_kakuro)

    for r in range(taille):
        for c in range(taille):
            donnee = grille_kakuro[r][c]
            
            # On prépare la fiche d'identité de la case
            case_info = {
                "coord": (r, c),
                "case_vide_id": None,   # Pour le fond (rectangle)
                "texte_id": None,       # Pour le gros chiffre tapé par le joueur
                "ligne_diag_id": None,  # Pour la diagonale des cases noires
                "id_h": None,           # Pour l'indice horizontal
                "id_v": None,           # Pour l'indice vertical
                "valeur_joueur": 0      # L'état de départ : le joueur n'a rien tapé
            }

            # On détermine la nature de la case
            if isinstance(donnee, int):
                # C'est une case de jeu classique
                case_info["type"] = "blanche"
                case_info["valeur_solution"] = donnee
            else:
                # C'est un mur avec des indices [Somme H, Somme V]
                case_info["type"] = "indice"
                case_info["indices"] = donnee 
            
            liste_cases.append(case_info)
            
    return liste_cases

