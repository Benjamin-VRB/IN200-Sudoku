import tkinter as tk

from GUI.widgets import creer_grille_sudoku, remplir_grille_sudoku_GUI

from Grille.sudoku import supprimer_valeur


def creer_sudoku_GUI(
        canvas: tk.Canvas, 
        coord: tuple[int, int], 
        nb_case_cote: int, 
        longueur_cote_case: int, 
        nb_carre_cote: int, 
        tags_page_jeu: dict[str, str], 
        couleur_cases: str, 
        couleur_bordure_cases: str, 
        couleur_textes: str, 
        difficulte: int = None, 
        grille_par_defaut: list[list[int]] = None, 
        indices_cases_verr: list[int] = None
    ) -> dict[str, list[dict[str, int]] | list[int]]:

    if difficulte is None and grille_par_defaut is None:
        return

    grille: dict[str, list[dict[str, int]] | list[int]] = \
        creer_grille_sudoku(
            canvas=canvas, 
            tags_page_jeu=tags_page_jeu, 
            coord=coord, 
            nb_case_cote=nb_case_cote, 
            longueur_cote_case=longueur_cote_case, 
            nb_carre_cote=nb_carre_cote, 
            couleur_cases=couleur_cases, 
            couleur_bordure_cases=couleur_bordure_cases, 
            couleur_textes=couleur_textes, 
            difficulte=difficulte
        )
    
    cases: list[dict[str, int]] = grille["cases"]

    if grille_par_defaut is None:
        if difficulte == 4:
            nombre_valeur_a_supprimer: int = 63
        elif difficulte == 3:
            nombre_valeur_a_supprimer: int = 54
        elif difficulte == 2:
            nombre_valeur_a_supprimer: int = 45
        elif difficulte == 1:
            nombre_valeur_a_supprimer: int = 36

        grille_valeur: list[list[int]] = supprimer_valeur(
            nombre_valeur_a_supprimer=nombre_valeur_a_supprimer, 
            dimension=nb_case_cote
        )[1]
        remplir_grille_sudoku_GUI(
            canvas=canvas, 
            cases=cases, 
            grille_valeur=grille_valeur
        )
    else:
        remplir_grille_sudoku_GUI(
            canvas=canvas, 
            cases=cases, 
            grille_valeur=grille_par_defaut, 
            indices_cases_verr=indices_cases_verr
        )

    
    
    return grille