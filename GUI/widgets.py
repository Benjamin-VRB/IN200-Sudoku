import tkinter as tk


def creer_boutton(canvas: tk.Canvas, coord: tuple[int, int], tag: str, largeur: int = 200, 
        hauteur: int = 100, texte: str = "", couleur_fond: str = "#ffffff", 
        couleur_texte: str = "#ffffff", epaisseur_bordure: int= 5, 
        couleur_bordure: str = "#000000", police: tuple = ("Arial", 11)
        ) -> tuple[list[int] | int]:
    """
    Crée un bouton sur le canvas 
    """
    bordure: list[int] = []

    bordure.append(
        canvas.create_arc(coord, (coord[0] + hauteur, coord[1] + hauteur), fill=couleur_bordure, 
                          outline=couleur_bordure, start=90, extent=180, tags=tag)
        )
    bordure.append(
        canvas.create_rectangle((coord[0] + hauteur // 2, coord[1]), 
                                (coord[0] + largeur - hauteur // 2, coord[1] + hauteur), 
                                fill=couleur_bordure, outline=couleur_bordure, tags=tag)
        )
    bordure.append(
        canvas.create_arc((coord[0] + largeur - hauteur, coord[1]), (coord[0] + largeur, coord[1] + hauteur), 
                          fill=couleur_bordure, outline=couleur_bordure, start=90, extent=-180, tags=tag)
        )
    
    fond: list[int] = []

    fond.append(
        canvas.create_arc((coord[0] + epaisseur_bordure, coord[1] + epaisseur_bordure), 
                          (coord[0] + hauteur - epaisseur_bordure, coord[1] + hauteur - epaisseur_bordure), 
                          fill=couleur_fond, outline=couleur_fond, start=90, extent=180, tags=tag)
        )
    fond.append(
        canvas.create_rectangle((coord[0] + (hauteur - 2 * epaisseur_bordure) // 2, coord[1] + epaisseur_bordure), 
                                (coord[0] + largeur - (hauteur - 2 * epaisseur_bordure) // 2, 
                                 coord[1] + hauteur - epaisseur_bordure), 
                                 fill=couleur_fond, outline=couleur_fond, tags=tag)
        )
    fond.append(
        canvas.create_arc((coord[0] + largeur - hauteur + epaisseur_bordure, coord[1] + epaisseur_bordure), 
                          (coord[0] + largeur - epaisseur_bordure, coord[1] + hauteur - epaisseur_bordure), 
                          fill=couleur_fond, outline=couleur_fond, start=90, extent=-180, tags=tag)
        )
    
    if texte != "":
        texte_bouton: int = canvas.create_text((coord[0] + largeur // 2, coord[1] + hauteur // 2), 
                                               text=texte, font=police, anchor=tk.CENTER, 
                                               fill=couleur_texte, tags=tag)
        
    return fond, bordure, texte_bouton


def desactiver_widget(canvas: tk.Canvas, tags_or_ids: list[str]) -> None:
    """
    Desactive les interactions avec les widgets indiqués
    """
    for tag_or_id in tags_or_ids:
        canvas.itemconfig(tag_or_id, state=tk.DISABLED)


def activer_widget(canvas: tk.Canvas, tags_or_ids: list[str]) -> None:
    """
    Active les interactions avec les widgets indiqués
    """
    for tag_or_id in tags_or_ids:
        canvas.itemconfig(tag_or_id, state=tk.NORMAL)

"""
def creer_case_vide(canvas: tk.Canvas, tag: str, coord: tuple[int], longueur_cote: int) -> int:

    case_vide: int = canvas.create_rectangle(coord, (coord[0] + longueur_cote, coord[1] + longueur_cote),
                                             fill="#ffffff", outline="#000000", width=2, tags=tag)
    texte: int = canvas.create_text((coord[0] + longueur_cote // 2, coord[1] + longueur_cote // 2),
                                   anchor=tk.CENTER, font=("Century", 1200 // longueur_cote), 
                                   fill="#000000", tags=tag)

    return (case_vide, texte)


def creer_grille_sudoku(canvas: tk.Canvas, tag: str, coord: tuple[int], nb_case_cote: int, 
                        longueur_cote_case: int, nb_carre_cote: int):
    
    grille: list[list[int]] = [[], []]
    for rangee in range(nb_case_cote):
        for colonne in range(nb_case_cote):
            x_case: int = coord[0] + colonne * longueur_cote_case
            y_case: int = coord[1] + rangee * longueur_cote_case
            grille[0].append(
                creer_case_vide(canvas, tag=tag, coord=(x_case, y_case), longueur_cote=longueur_cote_case)
                )
            
    if nb_case_cote % nb_carre_cote == 0:
        longueur_cote_carre = longueur_cote_case * nb_case_cote // nb_carre_cote
        for i in range(nb_carre_cote):
            for j in range(nb_carre_cote):
                x_carre_1: int = coord[0] + longueur_cote_carre * i
                y_carre_2: int = coord[1] + longueur_cote_carre * j
                canvas.create_rectangle((x_carre_1, y_carre_2), 
                                        (x_carre_1 + longueur_cote_carre, y_carre_2 + longueur_cote_carre),
                                        fill="", width=4, tags=tag)
    return grille
"""