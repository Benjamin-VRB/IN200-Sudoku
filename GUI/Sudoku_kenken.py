
import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.animations import mouvement_exterieur_fond_menu, retour_menu
from GUI.widgets import creer_boutton_arrondi, survole_non_survole, remplir_grille_sudoku_GUI, barre_entree_sauv
from GUI.widgets import creer_grille_sudoku_irregulier 

from Grille.aide import indicateur_kenken
import Grille.kenken as Kenken



def aller_kenken(canvas: tk.Canvas):

    mouvement_exterieur_fond_menu(canvas=canvas)

    TAG: str = "kenken"
    NB_CASE_COTE: int = 9

    LONGUEUR_COTE_GRILLE: int = NB_CASE_COTE * 60
    LONGUEUR_COTE_CASE: int = LONGUEUR_COTE_GRILLE // NB_CASE_COTE
    X_GRILLE: int = (LARGEUR_PIXEL_FENETRE - LONGUEUR_COTE_GRILLE) // 2
    Y_GRILLE: int = (HAUTEUR_PIXEL_FENETRE - LONGUEUR_COTE_GRILLE) // 2

    # Génération
    grille_complete, dico_cage = Kenken.retourner_infos_kenken(dimensions=NB_CASE_COTE)
    plan_cage = [[0 for _ in range(NB_CASE_COTE)] for _ in range(NB_CASE_COTE)]

    num_cage = 0

    for nom_cage in dico_cage:
        # On récupére les coordonnées des cases de cette cage
        liste_cases = dico_cage[nom_cage]["cases"]
        
        # Pour chaque case de cette cage on indique le numéro
        for coordonnees in liste_cases:
            lig = coordonnees[0]
            col = coordonnees[1]
            plan_cage[lig][col] = num_cage
            
        # On poursuit pour les autres cages 
        num_cage += 1
    
    grille_a_jouer = [[0 for _ in range(NB_CASE_COTE)] for _ in range(NB_CASE_COTE)]

    # On dessine la grille vide de ce qu'on a généré
    grille = creer_grille_sudoku_irregulier(
        canvas=canvas, 
        tag=TAG, 
        coord=(X_GRILLE, Y_GRILLE), 
        nb_case_cote=NB_CASE_COTE, 
        longueur_cote_case=LONGUEUR_COTE_CASE, 
        carte_regions=plan_cage 
    )

    # On remplit notre grille avec les nombre que nous avons
    remplir_grille_sudoku_GUI(
        canvas=canvas, 
        cases=grille["cases"], 
        grille_valeur=grille_a_jouer
    )

    # Boutons

    PARAMS_BOUTON: dict[str, int | str | tuple[str, int]] = {
        "largeur" : 200,
        "hauteur" : 76,
        "police" : ("Cooper Black", 16),
        "epaisseur_bordure" : 2,
        "couleur_texte" : "#ffffff"
    }

    COULEURS_BOUTON: dict[str, str] = {
        "couleur_fond" : "#E0D4C1",
        "couleur_bordure" : "#E9E0CE"
    }   
    
    COULEURS_SURVOLE: dict[str, str] = {
        "couleur_fond_surv" : "#BEB2A4",
        "couleur_bordure_surv" : "#A89E90"
    }

    # La distance entre le centre de deux boutons
    ECART_RANGEE: int = PARAMS_BOUTON["hauteur"] + 100

    # On détermine le centre vertical exact de la fenêtre 
    RANGEE2: int = (HAUTEUR_PIXEL_FENETRE - PARAMS_BOUTON["hauteur"]) // 2 

    # La position du bouton du bas
    RANGEE1: int = RANGEE2 + ECART_RANGEE

    # La position du bouton du haut
    RANGEE3: int = RANGEE2 - ECART_RANGEE

    # On met les boutons à 75 pixels du bord gauche de la fenetre 
    COLONNE1: int = 75

    # Identification des boutons
    TAG_AIDE: str = "bouton_sudoku_aide"
    TAG_SAUV: str = "bouton_sudoku_sauv"
    TAG_RETOUR: str = "bouton_sudoku_retour"
    
    bouton_aide: dict[str, list[int] | int] = \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(COLONNE1, RANGEE3), 
            tag=TAG_AIDE, 
            texte="Aide", 
            **(PARAMS_BOUTON | COULEURS_BOUTON)
        )

    bouton_sauv: dict[str, list[int] | int] = \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(COLONNE1, RANGEE2), 
            tag=TAG_SAUV, 
            texte="Sauvegarder", 
            **(PARAMS_BOUTON | COULEURS_BOUTON)
        )

    bouton_retour: dict[str, list[int] | int] = \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(COLONNE1, RANGEE1), 
            tag=TAG_RETOUR, 
            texte="Retour", 
            **(PARAMS_BOUTON | COULEURS_BOUTON)
        )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_AIDE], 
        fond=bouton_aide["fond"], 
        bordure=bouton_aide["bordure"], 
        **(COULEURS_BOUTON | COULEURS_SURVOLE)
    )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_SAUV], 
        fond=bouton_sauv["fond"], 
        bordure=bouton_sauv["bordure"], 
        **(COULEURS_BOUTON | COULEURS_SURVOLE)
    )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_RETOUR], 
        fond=bouton_retour["fond"], 
        bordure=bouton_retour["bordure"], 
        **(COULEURS_BOUTON | COULEURS_SURVOLE)
    )

    # Création de la sauvegarde 
    page: list[str] = [TAG, TAG_AIDE, TAG_RETOUR, TAG_SAUV, *[case["case_vide"] for case in grille["cases"]], 
                       *[case["texte"] for case in grille["cases"]]]

    LARGEUR_BARRE_ENTREE_SAUV: int = 200
    HAUTEUR_BARRE_ENTREE_SAUV: int = 75
    EPAISSEUR_CADRE_BARRE_ENTREE_SAUV: int = 5
    TAG_BARRE_ENTREE_SAUV: str = "barre_entree_sauv_sudoku"

    # Action des boutons
    
    def action_aide(event):
    # On récupère les valeurs de notre grille actuelle
        grille_joueur = []
    
        for lig in range(NB_CASE_COTE):
            ligne = []
            for col in range(NB_CASE_COTE):
                id_texte = grille["cases"][lig * NB_CASE_COTE + col]["texte"]
                # On lit le texte affiché
                valeur = canvas.itemcget(id_texte, "text")
                if valeur != "" :
                    ligne.append(int(valeur))
                else :
                    ligne.append(0)
            grille_joueur.append(ligne)

        resultat = indicateur_kenken(grille_joueur, grille_complete, NB_CASE_COTE)
        if resultat == (None, None) : 
            return 
        
        statut, donnees = resultat
        valeur_solution, (lig, col) = donnees
        index = lig * NB_CASE_COTE + col
        id_case = grille["cases"][index]["case_vide"]
        id_texte = grille["cases"][index]["texte"]
        if statut == "Erreur":
            # On change en conséquence la case problématique
            canvas.itemconfig(id_texte, text=str(valeur_solution))
            canvas.itemconfig(id_case, fill="#FF6666")
        
        elif statut == "Correct":
            # On ajoute une case pour aider le joueur
            canvas.itemconfig(id_texte, text=str(valeur_solution))
            canvas.itemconfig(id_case, fill="#99FF99")

    
    # Bouton Sauvegarder
    canvas.tag_bind(
        tagOrId=TAG_SAUV, 
        sequence="<Button-1>", 
        func=lambda event: barre_entree_sauv(
            canvas=canvas, 
            largeur=LARGEUR_BARRE_ENTREE_SAUV, 
            hauteur=HAUTEUR_BARRE_ENTREE_SAUV, 
            epaisseur_cadre=EPAISSEUR_CADRE_BARRE_ENTREE_SAUV, 
            page=page, 
            cases=grille["cases"],  
            tag=TAG_BARRE_ENTREE_SAUV, 
            type_grille="Sudoku Irregulier", 
            temps=0, 
            difficulte="facile"
        )
    )

    # Bouton retour
    canvas.tag_bind(
        tagOrId=TAG_RETOUR, 
        sequence="<Button-1>", 
        func=lambda event: retour_menu(
            canvas=canvas, 
            tags_ou_ids=[TAG, TAG_SAUV, TAG_RETOUR, TAG_AIDE, "clavier_num"]
        )
    )
    # Bouton aide
    canvas.tag_bind(TAG_AIDE, "<Button-1>", action_aide)