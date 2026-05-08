import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.animations import supprimer_elements, retour_menu
from GUI.widgets import creer_boutton_arrondi, survole_non_survole, barre_entree_sauv, COULEUR_CASE, \
afficher_conflits, verification_cases_sudoku
from GUI.sudoku import creer_sudoku_GUI

def aller_grille(
        canvas: tk.Canvas, 
        type_grille: str | None, 
        difficulte: int | None, 
        temps_depart: int, 
        tags_ou_ids_page_suppr: list[int | str] = None, 
        widgets_page_suppr: list[tk.Widget] = None, 
        grille_par_defaut: list[list[int]] = None, 
        indices_cases_verr: list[int] = None
    ) -> None:

    COULEUR_BORDURE_CASES: str = "#000000"
    COULEUR_TEXTE_CASES: str = "#000000"

    supprimer_elements(
        canvas=canvas, 
        tags_ou_ids=tags_ou_ids_page_suppr, 
        widgets=widgets_page_suppr
    )

    type_grille: str = type_grille.lower().strip()
    if type_grille == "sudoku":
        TAG: str = "sudoku"
        NB_CASE_COTE: int = 9
        LONGUEUR_COTE_GRILLE: int = NB_CASE_COTE * 60
        NB_CARRE_COTE: int = 3
        LONGUEUR_COTE_CASE: int = LONGUEUR_COTE_GRILLE // NB_CASE_COTE 
        X_GRILLE: int = (LARGEUR_PIXEL_FENETRE - LONGUEUR_COTE_GRILLE) // 2
        Y_GRILLE: int = (HAUTEUR_PIXEL_FENETRE - LONGUEUR_COTE_GRILLE) // 2
        grille: dict[str, list[dict[str, int]] | list[int]] = creer_sudoku_GUI(
            canvas=canvas, 
            coord=(X_GRILLE, Y_GRILLE), 
            nb_case_cote=NB_CASE_COTE, 
            longueur_cote_case=LONGUEUR_COTE_CASE, 
            nb_carre_cote=NB_CARRE_COTE, 
            tag=TAG, 
            couleur_cases=COULEUR_CASE, 
            couleur_bordure_cases=COULEUR_BORDURE_CASES, 
            couleur_textes=COULEUR_TEXTE_CASES, 
            difficulte=difficulte, 
            grille_par_defaut=grille_par_defaut, 
            indices_cases_verr=indices_cases_verr
        )
        cases: list[dict[str, int]] = grille["cases"]
        list_coord: list[tuple[int, int]] = verification_cases_sudoku(
            canvas=canvas, 
            cases=cases
        )
        afficher_conflits(
            canvas=canvas, 
            list_coord=list_coord, 
            cases=cases
        )
    else:
        return
    
    PARAMS_BOUTON: dict[str, int | str | tuple[str, int]] = {
        "largeur" : 200,
        "hauteur" : 76,
        "police" : ("Cooper Black", 16),
        "epaisseur_bordure" : 2,
        "couleur_texte" : "#ffffff"
    }

    COULEURS_BOUTON: dict[str, str] = {
        "couleur_fond" : "#E0D4C1",
        "couleur_bordure" : "#E9E0CE", 
        "couleur_fond_surv" : "#BEB2A4",
        "couleur_bordure_surv" : "#A89E90"
    }

    ECART_RANGEE: int = PARAMS_BOUTON["hauteur"] + 100
    RANGEE2: int = (HAUTEUR_PIXEL_FENETRE - PARAMS_BOUTON["hauteur"]) // 2 
    RANGEE1: int = RANGEE2 + ECART_RANGEE
    RANGEE3: int = RANGEE2 - ECART_RANGEE
    COLONNE1: int = 75

    TAG_AIDE: str = "bouton_sudoku_aide"
    TAG_SAUV: str = "bouton_sudoku_sauv"
    TAG_RETOUR: str = "bouton_sudoku_retour"
    
    bouton_aide: dict[str, list[int] | int] =  \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(COLONNE1, RANGEE3), 
            tag=TAG_AIDE, 
            texte="Aide", 
            couleur_fond=COULEURS_BOUTON["couleur_fond"], 
            couleur_bordure=COULEURS_BOUTON["couleur_bordure"], 
            **PARAMS_BOUTON
        )

    bouton_sauv: dict[str, list[int] | int] =  \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(COLONNE1, RANGEE2), 
            tag=TAG_SAUV, 
            texte="Sauvegarder", 
            couleur_fond=COULEURS_BOUTON["couleur_fond"], 
            couleur_bordure=COULEURS_BOUTON["couleur_bordure"], 
            **PARAMS_BOUTON
        )

    bouton_retour: dict[str, list[int] | int] =  \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(COLONNE1, RANGEE1), 
            tag=TAG_RETOUR, 
            texte="Retour", 
            couleur_fond=COULEURS_BOUTON["couleur_fond"], 
            couleur_bordure=COULEURS_BOUTON["couleur_bordure"], 
            **PARAMS_BOUTON
        )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_AIDE], 
        fond=bouton_aide["fond"], 
        bordure=bouton_aide["bordure"], 
        couleurs=COULEURS_BOUTON
    )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_SAUV], 
        fond=bouton_sauv["fond"], 
        bordure=bouton_sauv["bordure"], 
        couleurs=COULEURS_BOUTON
    )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_RETOUR], 
        fond=bouton_retour["fond"], 
        bordure=bouton_retour["bordure"], 
        couleurs=COULEURS_BOUTON
    )
    
    page: list[str] = [TAG, TAG_AIDE, TAG_RETOUR, TAG_SAUV, *[case["case_vide"] for case in grille["cases"]], 
                    *[case["texte"] for case in grille["cases"]]]

    LARGEUR_BARRE_ENTREE_SAUV: int = 200
    HAUTEUR_BARRE_ENTREE_SAUV: int = 75
    EPAISSEUR_CADRE_BARRE_ENTREE_SAUV: int = 5
    TAG_BARRE_ENTREE_SAUV: str = "barre_entree_sauv_sudoku"

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
            type_grille=type_grille, 
            temps=126, 
            difficulte=difficulte, 
            couleur_nombres_normale=COULEUR_TEXTE_CASES, 
            couleur_bordure_cases_normale=COULEUR_BORDURE_CASES
        )
    )

    canvas.tag_bind(
        tagOrId=TAG_RETOUR, 
        sequence="<Button-1>", 
        func=lambda event: retour_menu(
            canvas=canvas, 
            tags_ou_ids=[TAG, TAG_SAUV, TAG_RETOUR, TAG_AIDE, "clavier_num"]
        )
    )
