import tkinter as tk

from GUI.widgets import creer_grille_sudoku, remplir_grille_sudoku_GUI

from Grille.sudoku import supprimer_valeur


def creer_sudoku_GUI(
        canvas: tk.Canvas, 
        coord: tuple[int, int], 
        nb_case_cote: int, 
        longueur_cote_case: int, 
        nb_carre_cote: int, 
        tag: str
    ) -> dict[str, list[dict[str, int]] | list[int]]:

    grille: dict[str, list[dict[str, int]] | list[int]] = \
        creer_grille_sudoku(
            canvas=canvas, 
            tag=tag, 
            coord=coord, 
            nb_case_cote=nb_case_cote, 
            longueur_cote_case=longueur_cote_case, 
            nb_carre_cote=nb_carre_cote
        )
    
    grille_valeur = supprimer_valeur(
        nombre_valeur_a_supprimer=60, 
        dimension=nb_case_cote
    )

    remplir_grille_sudoku_GUI(
        canvas=canvas, 
        cases=grille["cases"], 
        grille_valeur=grille_valeur
    )
    
    return grille