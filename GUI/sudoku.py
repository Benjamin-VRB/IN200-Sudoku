import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.animations import mouvement_exterieur_fond_menu, retour_menu
from GUI.widgets import creer_grille_sudoku, creer_boutton_arrondi, survole_non_survole, remplir_grille_sudoku_GUI, \
barre_entree_sauv

from Grille.sudoku import supprimer_valeur


def aller_sudoku(canvas: tk.Canvas) -> None:
    
    mouvement_exterieur_fond_menu(canvas=canvas)

    TAG: str = "sudoku"

    NB_CASE_COTE: int = 9
    LONGUEUR_COTE_GRILLE: int = NB_CASE_COTE * 60
    NB_CARRE_COTE: int = 3
    LONGUEUR_COTE_CASE: int = LONGUEUR_COTE_GRILLE // NB_CASE_COTE
    
    X_GRILLE: int = (LARGEUR_PIXEL_FENETRE - LONGUEUR_COTE_GRILLE) // 2
    Y_GRILLE: int = (HAUTEUR_PIXEL_FENETRE - LONGUEUR_COTE_GRILLE) // 2

    grille: dict[str, list[dict[str, int]] | list[int]] = \
        creer_grille_sudoku(canvas=canvas, tag=TAG, coord=(X_GRILLE, Y_GRILLE), nb_case_cote=NB_CASE_COTE, 
                            longueur_cote_case=LONGUEUR_COTE_CASE, nb_carre_cote=NB_CARRE_COTE)
    grille_valeur, grille_solution = supprimer_valeur(nombre_valeur_a_supprimer=60, 
                                                      dimension=NB_CASE_COTE)
    remplir_grille_sudoku_GUI(canvas=canvas, cases=grille["cases"], grille_valeur=grille_valeur)
    
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

    ECART_RANGEE: int = PARAMS_BOUTON["hauteur"] + 100
    RANGEE2: int = (HAUTEUR_PIXEL_FENETRE - PARAMS_BOUTON["hauteur"]) // 2 
    RANGEE1: int = RANGEE2 + ECART_RANGEE
    RANGEE3: int = RANGEE2 - ECART_RANGEE
    COLONNE1: int = 75

    TAG_AIDE: str = "bouton_sudoku_aide"
    TAG_SAUV: str = "bouton_sudoku_sauv"
    TAG_RETOUR: str = "bouton_sudoku_retour"
    
    bouton_aide: dict[str, list[int] | int] =  \
        creer_boutton_arrondi(canvas=canvas, coord=(COLONNE1, RANGEE3), tag=TAG_AIDE, 
                              texte="Aide", **(PARAMS_BOUTON | COULEURS_BOUTON))

    bouton_sauv: dict[str, list[int] | int] =  \
        creer_boutton_arrondi(canvas=canvas, coord=(COLONNE1, RANGEE2), tag=TAG_SAUV, 
                              texte="Sauvegarder", **(PARAMS_BOUTON | COULEURS_BOUTON))

    bouton_retour: dict[str, list[int] | int] =  \
        creer_boutton_arrondi(canvas=canvas, coord=(COLONNE1, RANGEE1), tag=TAG_RETOUR, 
                              texte="Retour", **(PARAMS_BOUTON | COULEURS_BOUTON))

    survole_non_survole(canvas=canvas, tag=TAG_AIDE, fond=bouton_aide["fond"], 
                        bordure=bouton_aide["bordure"], **(COULEURS_BOUTON | COULEURS_SURVOLE))

    survole_non_survole(canvas=canvas, tag=TAG_SAUV, fond=bouton_sauv["fond"], 
                        bordure=bouton_sauv["bordure"], **(COULEURS_BOUTON | COULEURS_SURVOLE))

    survole_non_survole(canvas=canvas, tag=TAG_RETOUR, fond=bouton_retour["fond"], 
                        bordure=bouton_retour["bordure"], **(COULEURS_BOUTON | COULEURS_SURVOLE))
    
    page: list[str] = [TAG, TAG_AIDE, TAG_RETOUR, TAG_SAUV, *[case["case_vide"] for case in grille["cases"]], 
                       *[case["texte"] for case in grille["cases"]]]

    LARGEUR_BARRE_ENTREE_SAUV: int = 200
    HAUTEUR_BARRE_ENTREE_SAUV: int = 75
    EPAISSEUR_CADRE_BARRE_ENTREE_SAUV: int = 5

    canvas.tag_bind(tagOrId=TAG_SAUV, sequence="<Button-1>", func=lambda event: 
                    barre_entree_sauv(canvas=canvas, largeur=LARGEUR_BARRE_ENTREE_SAUV, 
                                      hauteur=HAUTEUR_BARRE_ENTREE_SAUV, 
                                      epaisseur_cadre=EPAISSEUR_CADRE_BARRE_ENTREE_SAUV, 
                                      page=page, cases=grille["cases"], 
                                      grille_solution=grille_solution, temps=0, 
                                      tag="barre_entree_sauv_sudoku", type_grille="Sudoku"))

    canvas.tag_bind(tagOrId=TAG_RETOUR, sequence="<Button-1>", func=lambda event: 
                    retour_menu(canvas=canvas, tags_or_ids=[TAG, TAG_SAUV, TAG_RETOUR, 
                                                            TAG_AIDE, "clavier_num"]))
