import tkinter as tk        ### A reverifier avec Benjamin

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.animations import mouvement_exterieur_fond_menu, retour_menu
from GUI.widgets import creer_grille_sudoku,  desactiver_widget

from Grille.windoku import supprimer_valeur


COULEUR_CASE_VERR: str = "#F0F0F0"

def aller_windoku(canvas: tk.Canvas) -> None:
    
    mouvement_exterieur_fond_menu(canvas=canvas)

    TAG: str = "sudoku"

    NB_CASE_COTE: int = 9
    LONGUEUR_COTE_GRILLE: int = NB_CASE_COTE * 60
    NB_CARRE_COTE: int = 3
    LONGUEUR_COTE_CASE: int = LONGUEUR_COTE_GRILLE // NB_CASE_COTE
    
    X_GRILLE: int = (LARGEUR_PIXEL_FENETRE - LONGUEUR_COTE_GRILLE) // 2
    Y_GRILLE: int = (HAUTEUR_PIXEL_FENETRE - LONGUEUR_COTE_GRILLE) // 2

    grille: dict[str, list[dict[str, int]] | list[int]] = \
        creer_grille_sudoku(
            canvas=canvas, 
            tag=TAG, 
            coord=(X_GRILLE, Y_GRILLE), 
            nb_case_cote=NB_CASE_COTE, 
            longueur_cote_case=LONGUEUR_COTE_CASE, 
            nb_carre_cote=NB_CARRE_COTE
        )
    
    grille_valeur = supprimer_valeur(
        nombre_valeur_a_supprimer=50, 
        dimension=NB_CASE_COTE
    )

    def remplir_grille_windoku_GUI(
    canvas: tk.Canvas,
    cases: list[dict[str, int]],
    grille_valeur: list[list[int]],
    regions_windoku: list[list[tuple[int, int]]] = None
) -> None:
        COULEUR_WINDOKU = "#B9B9FA"
    
        for rangee in range(len(grille_valeur)):
            for colonne in range(len(grille_valeur[0])):
                index = rangee * len(grille_valeur[0]) + colonne
                case = cases[index]
                case_vide = case["case_vide"]
                texte = case["texte"]

                # Colorer les cases selon leur région Windoku
                couleur_case = None
                if regions_windoku:
                    for couleur, region in enumerate(regions_windoku, 1):
                        if (rangee, colonne) in region:
                            couleur_case = COULEUR_WINDOKU
                            break

                # Remplir les cases avec les valeurs
                if grille_valeur[rangee][colonne] != 0:
                    desactiver_widget(canvas=canvas, tags_ou_ids=[case_vide, texte])
                    if couleur_case:
                        canvas.itemconfig(case_vide, fill="#9B9BD1") 
                    else:
                        canvas.itemconfig(case_vide, fill=COULEUR_CASE_VERR)
                    canvas.itemconfig(texte, text=grille_valeur[rangee][colonne])
                elif couleur_case:
                    canvas.itemconfig(case_vide, fill=couleur_case)


    regions_windoku = [
    [(i, j) for i in range(1, 4) for j in range(1, 4)], 
    [(i, j) for i in range(1, 4) for j in range(5, 8)],
    [(i, j) for i in range(5, 8) for j in range(1, 4)],
    [(i, j) for i in range(5, 8) for j in range(5, 8)]
    ]


    remplir_grille_windoku_GUI(
        canvas=canvas,
        cases=grille["cases"],
        grille_valeur=grille_valeur,
        regions_windoku=regions_windoku
    )
