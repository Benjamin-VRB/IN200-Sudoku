import tkinter as tk
import datetime
import math

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.decorations import creer_cadre

from Grille.sauvegarde import sauvegarder
from Grille.verification import verification_sudoku_classique_complet


COULEUR_CASE: str = "#ffffff"
COULEUR_CASE_VERR: str = "#F0F0F0"
COULEUR_CASE_PROBLEME: str = "#ffc5bc"
COULEUR_CASE_PROBLEME_VERR: str = "#d3a49c"


def creer_boutton_arrondi(
    canvas: tk.Canvas, 
    coord: tuple[int, int], 
    tag: str, 
    largeur: int, 
    hauteur: int, 
    texte: str, 
    couleur_texte: str,
    couleur_fond: str, 
    epaisseur_bordure: int, 
    couleur_bordure: str, 
    police: tuple[str | int, ...]
) -> dict[str, list[int] | int]:
    """
    Crée un bouton sur le canvas 
    """
    bordure: list[int] = []

    bordure.append(
        canvas.create_arc(
            (coord, 
             (coord[0] + hauteur, coord[1] + hauteur)), 
            fill=couleur_bordure, 
            outline=couleur_bordure, 
            start=90, 
            extent=180, 
            tags=tag
        )
    )

    bordure.append(
        canvas.create_rectangle(
            ((coord[0] + hauteur // 2, coord[1]), 
             (coord[0] + largeur - hauteur // 2, coord[1] + hauteur)), 
            fill=couleur_bordure, 
            outline=couleur_bordure, 
            tags=tag
        )
    )

    bordure.append(
        canvas.create_arc(
            ((coord[0] + largeur - hauteur, coord[1]), 
             (coord[0] + largeur, coord[1] + hauteur)), 
            fill=couleur_bordure, 
            outline=couleur_bordure, 
            start=90, 
            extent=-180, 
            tags=tag
        )
    )
    
    fond: list[int] = []

    fond.append(
        canvas.create_arc(
            ((coord[0] + epaisseur_bordure, coord[1] + epaisseur_bordure), 
             (coord[0] + hauteur - epaisseur_bordure, coord[1] + hauteur - epaisseur_bordure)), 
            fill=couleur_fond, 
            outline=couleur_fond, 
            start=90, 
            extent=180, 
            tags=tag
        )
    )

    fond.append(
        canvas.create_rectangle(
            ((coord[0] + (hauteur - 2 * epaisseur_bordure) // 2, coord[1] + epaisseur_bordure), 
             (coord[0] + largeur - (hauteur - 2 * epaisseur_bordure) // 2, 
              coord[1] + hauteur - epaisseur_bordure)), 
            fill=couleur_fond, 
            outline=couleur_fond, 
            tags=tag
        )
    )

    fond.append(
        canvas.create_arc(
            ((coord[0] + largeur - hauteur + epaisseur_bordure, coord[1] + epaisseur_bordure), 
             (coord[0] + largeur - epaisseur_bordure, coord[1] + hauteur - epaisseur_bordure)), 
            fill=couleur_fond, 
            outline=couleur_fond, 
            start=90, 
            extent=-180, 
            tags=tag
        )
    )
    
    if texte != "":
        texte_bouton: int = canvas.create_text(
            (coord[0] + largeur // 2, coord[1] + hauteur // 2), 
            text=texte, 
            font=police, 
            anchor=tk.CENTER, 
            fill=couleur_texte, 
            tags=tag
        )
        
    return {"fond" : fond, "bordure" : bordure, "texte" : texte_bouton}


def changer_couleurs(
    canvas: tk.Canvas, 
    fond: list[int], 
    bordure: list[int], 
    couleur_fond: str, 
    couleur_bordure: str
) -> None:
    """
    Change les couleurs des éléments
    """
    for id in fond:
        canvas.itemconfig(
            tagOrId=id, 
            fill=couleur_fond, 
            outline=couleur_fond
        )
    for id in bordure:
        canvas.itemconfig(
            tagOrId=id, 
            fill=couleur_bordure, 
            outline=couleur_bordure
        )


def survole_non_survole(
    canvas: tk.Canvas, 
    tags_ou_ids: list[str | int], 
    fond: list[int], 
    bordure: list[int], 
    couleur_fond: str, 
    couleur_bordure: str, 
    couleur_fond_surv: str, 
    couleur_bordure_surv: str
) -> None:
    """
    Change les couleurs du widgets lorqu'il est survolé et lorsqu'il n'est plus survolé par la souris
    """
    for tag_or_id in tags_ou_ids:

        canvas.tag_bind(
            tagOrId=tag_or_id, 
            sequence="<Enter>", 
            func=lambda event: changer_couleurs(
                canvas=canvas, 
                fond=fond, 
                bordure=bordure, 
                couleur_fond=couleur_fond_surv, 
                couleur_bordure=couleur_bordure_surv
            )
        )

        canvas.tag_bind(
            tagOrId=tag_or_id, 
            sequence="<Leave>", 
            func=lambda event: changer_couleurs(
                canvas=canvas, 
                fond=fond, 
                bordure=bordure, 
                couleur_fond=couleur_fond, 
                couleur_bordure=couleur_bordure
            )
        )


def desactiver_widget(
    canvas: tk.Canvas, 
    tags_ou_ids: list[str | int]
) -> None:
    """
    Desactive les interactions avec les widgets indiqués
    """
    for tag_or_id in tags_ou_ids:
        canvas.itemconfig(
            tagOrId=tag_or_id, 
            state=tk.DISABLED
        )


def activer_widget(
    canvas: tk.Canvas, 
    tags_ou_ids: list[str | int]
) -> None:
    """
    Active les interactions avec les widgets indiqués
    """
    for tag_or_id in tags_ou_ids:
        canvas.itemconfig(
            tagOrId=tag_or_id, 
            state=tk.NORMAL
        )


def trouver_cases_verrouillee(
    canvas: tk.Canvas, 
    cases: list[dict[str, int]]
) -> list[dict[str, int]]:

    cases_verr: list[dict[str, int]] = []
    for case in cases:
        case_vide: int = case["case_vide"]
        if canvas.itemcget(
            tagOrId=case_vide, 
            option="fill"
        ) in [COULEUR_CASE_VERR, COULEUR_CASE_PROBLEME_VERR]:
            cases_verr.append(case)
    return cases_verr


def reset_couleur_cases_rouges(
    canvas: tk.Canvas, 
    cases: list[dict[str, int]]
) -> None:
    
    for case in cases:
        case_vide: int = case["case_vide"]
        if canvas.itemcget(
            tagOrId=case_vide, 
            option="fill"
        ) == COULEUR_CASE_PROBLEME_VERR:
            canvas.itemconfig(
                tagOrId=case_vide, 
                fill=COULEUR_CASE_VERR
            )
        if canvas.itemcget(
            tagOrId=case_vide, 
            option="fill"
        ) == COULEUR_CASE_PROBLEME:
            canvas.itemconfig(
                tagOrId=case_vide, 
                fill=COULEUR_CASE
            )


def reset_focus_cases(
    canvas: tk.Canvas, 
    cases: list[dict[str, int]]
) -> None:

    canvas.unbind_all(sequence="<KeyPress>")
    canvas.delete("clavier_num")
    for case in cases:
        case_vide: int = case["case_vide"]
        canvas.itemconfig(
            tagOrId=case_vide, 
            width=1, 
            outline="#000000"
        )
        canvas.tag_lower(case_vide)


def verification_cases_sudoku(
    canvas: tk.Canvas, 
    case: dict[str, int], 
    cases: list[dict[str, int]]
) -> list[tuple[int, int]]:
    
    grille: list[list[int]] = []
    nombre_cases_cote_grille: int = int(math.sqrt(len(cases)))
    for _ in range(nombre_cases_cote_grille):
        rangee: list[int] = []
        for _ in range(nombre_cases_cote_grille):
            texte: int = case["texte"]
            nombre: int = canvas.itemcget(
                tagOrId=texte, 
                option="text"
            )
            rangee.append(nombre)
        grille.append(rangee)
    list_coord_nombres_identiques: list[tuple[int, int]] = \
        verification_sudoku_classique_complet(grille=grille)
    return list_coord_nombres_identiques


def afficher_cases_identiques(
    canvas: tk.Canvas, 
    list_coord: list[tuple[int, int]], 
    cases: list[dict[str, int]], 
):
    
    reset_couleur_cases_rouges(
        canvas=canvas, 
        cases=cases
    )

    cases_verr: list[dict[str, int]] = trouver_cases_verrouillee(
        canvas=canvas, 
        cases=cases
    )
    for coord in list_coord:
        indice: int = coord[1] * 9 + coord[0]
        case: dict[str, int] = cases[indice]
        case_vide: int = case["case_vide"]
        if case in cases_verr:
            canvas.itemconfig(
                tagOrId=case_vide,
                fill=COULEUR_CASE_PROBLEME_VERR
            )
        else:
            canvas.itemconfig(
                tagOrId=case_vide,
                fill=COULEUR_CASE_PROBLEME
            )


def modifier_valeur_case_grille(
    event, 
    canvas: tk.Canvas, 
    case: dict[str, int], 
    valeur_max: int, 
    cases: list[dict[str, int]]
) -> None:
    
    texte: int = case["texte"]
    nombre_actuel: str = canvas.itemcget(
        tagOrId=texte, 
        option="text"
    )
    if len(event.char) > 0 and event.char in "123456789" and \
        int(nombre_actuel + event.char) <= valeur_max:
        canvas.itemconfig(
            tagOrId=texte, 
            text=nombre_actuel + event.char
        )
    elif event.keysym in ["Return", "Escape"]:
        reset_focus_cases(
            canvas=canvas, 
            cases=[case]
        )
        list_coord: list[tuple[int, int]] = verification_cases_sudoku(
            canvas=canvas, 
            case=case, 
            cases=cases
        )
        afficher_cases_identiques(
            canvas=canvas, 
            list_coord=list_coord, 
            cases=cases
        )
    elif len(nombre_actuel) > 0:
        if event.char == "0" and int(nombre_actuel + event.char) <= valeur_max:
            canvas.itemconfig(
                tagOrId=texte, 
                text=nombre_actuel + event.char
            )
        elif event.keysym in ["BackSpace", "Delete"]:
            canvas.itemconfig(
                tagOrId=texte, 
                text=nombre_actuel[:-1]
            )


def modifier_valeur_case_clavier_num(
    canvas: tk.Canvas, 
    case: dict[str, int], 
    valeur_max: int, 
    valeur: str
) -> None:
    
    texte: int = case["texte"]
    nombre_actuel: str = canvas.itemcget(
        tagOrId=texte, 
        option="text"
    )
    if valeur in "123456789" and int(nombre_actuel + valeur) <= valeur_max:
        canvas.itemconfig(
            tagOrId=texte, 
            text=nombre_actuel + valeur
        )
    elif valeur == "0" and int(nombre_actuel + valeur) <= valeur_max \
        and nombre_actuel != "":
        canvas.itemconfig(
            tagOrId=texte, 
            text=nombre_actuel + valeur
        )
    elif valeur == "suppr":
        canvas.itemconfig(
            tagOrId=texte, 
            text=nombre_actuel[:-1]
        )


def creer_clavier_numerique(
    canvas: tk.Canvas, 
    coord: tuple[int, int], 
    largeur: int, 
    hauteur: int, 
    case: dict[str, int], 
    valeur_max: int
) -> dict[str, dict[str, dict[str, tk.Button | int]] | int]:

    largeur_bouton: int = largeur // 3
    hauteur_bouton: int = hauteur // 4

    PARAMAS_BOUTON: dict[str, str | tuple[str, int]] = {
        "bg" : "#ffffff", 
        "fg" : "#000000", 
        "font" : ("Century", 12), 
    }

    TAG: str = "clavier_num"
    ANCHOR = tk.NW
    FUNC = modifier_valeur_case_clavier_num

    boutons: dict[str, tuple[tk.Button, int]] = {}

    bouton7: tk.Button = tk.Button(
        master=canvas, 
        command=lambda case=case: FUNC(
            canvas=canvas, 
            case=case, 
            valeur_max=valeur_max, 
            valeur="7"
        ), 
        text="7", 
        **PARAMAS_BOUTON
    )

    window7: int = canvas.create_window(
        coord, 
        tags=TAG, 
        anchor=ANCHOR, 
        width=largeur_bouton, 
        height=hauteur_bouton, window=bouton7
    )
    
    boutons["bouton7"] = {"bouton" : bouton7, "fenetre" : window7}

    bouton8: tk.Button = tk.Button(
        master=canvas, 
        command=lambda case=case: FUNC(
            canvas=canvas, 
            case=case, 
            valeur_max=valeur_max, 
            valeur="8"
        ),
        text="8", 
        **PARAMAS_BOUTON
    )

    window8: int = canvas.create_window(
        (coord[0] + largeur_bouton, coord[1]), 
        tags=TAG, 
        anchor=ANCHOR, 
        width=largeur_bouton, 
        height=hauteur_bouton, 
        window=bouton8
    )

    boutons["bouton8"] = {"bouton" : bouton8, "fenetre" : window8}
    
    bouton9: tk.Button = tk.Button(
        master=canvas, 
        command=lambda case=case: FUNC(
            canvas=canvas, 
            case=case, 
            valeur_max=valeur_max, 
            valeur="9"
        ),
        text="9", 
        **PARAMAS_BOUTON
    )

    window9: int = canvas.create_window(
        (coord[0] + 2 *largeur_bouton, coord[1]), 
        tags=TAG, 
        anchor=ANCHOR, 
        width=largeur_bouton, 
        height=hauteur_bouton, 
        window=bouton9
    )

    boutons["bouton9"] = {"bouton" : bouton9, "fenetre" : window9}
    
    bouton4: tk.Button = tk.Button(
        master=canvas, 
        command=lambda case=case: FUNC(
            canvas=canvas, 
            case=case, 
            valeur_max=valeur_max, 
            valeur="4"
        ),
        text="4", 
        **PARAMAS_BOUTON
    )
    
    window4: int = canvas.create_window(
        (coord[0], coord[1] + hauteur_bouton), 
        tags=TAG, 
        anchor=ANCHOR, 
        width=largeur_bouton, 
        height=hauteur_bouton, 
        window=bouton4
    )

    boutons["bouton4"] = {"bouton" : bouton4, "fenetre" : window4}
    
    bouton5: tk.Button = tk.Button(
        master=canvas, 
        command=lambda case=case: FUNC(
            canvas=canvas, 
            case=case, 
            valeur_max=valeur_max, 
            valeur="5"
        ),
        text="5", 
        **PARAMAS_BOUTON
    )

    window5: int = canvas.create_window(
        (coord[0] + largeur_bouton, coord[1] + hauteur_bouton), 
        tags=TAG, 
        anchor=ANCHOR, 
        width=largeur_bouton, 
        height=hauteur_bouton, 
        window=bouton5
    )

    boutons["bouton5"] = {"bouton" : bouton5, "fenetre" : window5}

    bouton6: tk.Button = tk.Button(
        master=canvas, 
        command=lambda case=case: FUNC(
            canvas=canvas, 
            case=case, 
            valeur_max=valeur_max, 
            valeur="6"
        ),
        text="6", 
        **PARAMAS_BOUTON
    )

    window6: int = canvas.create_window(
        (coord[0] + 2 * largeur_bouton, coord[1] + hauteur_bouton), 
        tags=TAG, 
        anchor=ANCHOR, 
        width=largeur_bouton, 
        height=hauteur_bouton, 
        window=bouton6
    )

    boutons["bouton6"] = {"bouton" : bouton6, "fenetre" : window6}

    bouton1: tk.Button = tk.Button(
        master=canvas, 
        command=lambda case=case: FUNC(
            canvas=canvas, 
            case=case, 
            valeur_max=valeur_max, 
            valeur="1"
        ),
        text="1", 
        **PARAMAS_BOUTON
    )

    window1: int = canvas.create_window(
        (coord[0], coord[1] + 2 * hauteur_bouton), 
        tags=TAG, 
        anchor=ANCHOR, 
        width=largeur_bouton, 
        height=hauteur_bouton, 
        window=bouton1
    )

    boutons["bouton1"] = {"bouton" : bouton1, "fenetre" : window1}

    bouton2: tk.Button = tk.Button(
        master=canvas, 
        command=lambda case=case: FUNC(
            canvas=canvas, 
            case=case, 
            valeur_max=valeur_max, 
            valeur="2"
        ),
        text="2", 
        **PARAMAS_BOUTON
    )

    window2: int = canvas.create_window(
        (coord[0] + largeur_bouton, coord[1] + 2 * hauteur_bouton), 
        tags=TAG, 
        anchor=ANCHOR, 
        width=largeur_bouton, 
        height=hauteur_bouton, 
        window=bouton2
    )

    boutons["bouton2"] = {"bouton" : bouton2, "fenetre" : window2}

    bouton3: tk.Button = tk.Button(
        master=canvas, 
        command=lambda case=case: FUNC(
            canvas=canvas, 
            case=case, 
            valeur_max=valeur_max, 
            valeur="3"
        ),
        text="3", 
        **PARAMAS_BOUTON
    )

    window3: int = canvas.create_window(
        (coord[0] + 2 * largeur_bouton, coord[1] + 2 * hauteur_bouton),  
        tags=TAG, 
        anchor=ANCHOR, 
        width=largeur_bouton, 
        height=hauteur_bouton, 
        window=bouton3
    )

    boutons["bouton3"] = {"bouton" : bouton3, "fenetre" : window3}

    bouton0: tk.Button = tk.Button(
        master=canvas, 
        command=lambda case=case: FUNC(
            canvas=canvas, 
            case=case, 
            valeur_max=valeur_max, 
            valeur="0"
        ),
        text="0", 
        **PARAMAS_BOUTON
    )

    window0: int = canvas.create_window(
        (coord[0], coord[1] + 3 * hauteur_bouton), 
        tags=TAG, 
        anchor=ANCHOR, 
        width=largeur_bouton, 
        height=hauteur_bouton, 
        window=bouton0
    )

    boutons["bouton0"] = {"bouton" : bouton0, "fenetre" : window0}

    bouton_suppr: tk.Button = tk.Button(
        master=canvas, 
        command=lambda case=case: FUNC(
            canvas=canvas, 
            case=case, 
            valeur_max=valeur_max, 
            valeur="suppr"
        ),
        text="Suppr", 
        **PARAMAS_BOUTON
    )

    window_suppr: int = canvas.create_window(
        (coord[0] + largeur_bouton, coord[1] + 3 * hauteur_bouton), 
        tags=TAG, 
        anchor=ANCHOR, 
        width=2 * largeur_bouton, 
        height=hauteur_bouton, 
        window=bouton_suppr
    )

    boutons["bouton_suppr"] = {"bouton" : bouton_suppr, "fenetre" : window_suppr}

    COULEUR_CADRE: str = "#000000"
    EPAISSEUR_CADRE: int = 3

    cadre: int = canvas.create_rectangle(
        ((coord[0] - EPAISSEUR_CADRE, coord[1] - EPAISSEUR_CADRE), 
         (coord[0] + 3 * largeur_bouton + EPAISSEUR_CADRE - 1, 
          coord[1] + 4 * hauteur_bouton + EPAISSEUR_CADRE - 1)), 
        fill=COULEUR_CADRE, 
        outline="", 
        tags=TAG
    )
    
    return {"boutons" : boutons, "cadre" : cadre}
    

def entree_focus_case(
    canvas: tk.Canvas, 
    case: dict[str, int], 
    valeur_max: int, 
    cases: list[dict[str, int]]
) -> None:
    
    case_vide: int = case["case_vide"]
    texte: int = case["texte"]

    reset_focus_cases(
        canvas=canvas, 
        cases=cases
    )
    canvas.tag_raise(case_vide)
    canvas.tag_raise(texte)
    canvas.itemconfig(
        tagOrId=case_vide, 
        width=4, 
        outline="#3185ED"
    )

    LARGEUR_CLAVIER_NUM: int = 250
    HAUTEUR_CLAVIER_NUM: int = 400
    creer_clavier_numerique(
        canvas=canvas, 
        coord=(LARGEUR_PIXEL_FENETRE - 300, 150), 
        largeur=LARGEUR_CLAVIER_NUM, 
        hauteur=HAUTEUR_CLAVIER_NUM, 
        case=case, 
        valeur_max=valeur_max
    )
    
    canvas.bind_all(
        sequence="<KeyPress>", 
        func=lambda event: modifier_valeur_case_grille(
            event, 
            canvas=canvas, 
            case=case,
            valeur_max=valeur_max, 
            cases=cases
        )
    )


def creer_case(
    canvas: tk.Canvas, 
    tag: str, 
    coord: tuple[int, int], 
    longueur_cote: int
) -> dict[str, int]:

    case_vide: int = canvas.create_rectangle(
        (coord, (coord[0] + longueur_cote, coord[1] + longueur_cote)),
        fill=COULEUR_CASE, 
        outline="#000000", 
        width=1, 
        tags=tag
    )

    texte: int = canvas.create_text(
        (coord[0] + longueur_cote // 2, coord[1] + longueur_cote // 2),
        anchor=tk.CENTER, 
        font=("Century", int(1 / 3  * longueur_cote)), 
        fill="#000000", 
        tags=tag, 
        text=""
    )

    return {"case_vide" : case_vide, "texte" : texte}


def creer_grille_sudoku(
    canvas: tk.Canvas, 
    tag: str, 
    coord: tuple[int, int], 
    nb_case_cote: int, 
    longueur_cote_case: int, 
    nb_carre_cote: int
) -> dict[str, list[dict[str, int]] | list[int]]:
    
    cases: list[dict[str, int]] = []
    for rangee in range(nb_case_cote):
        for colonne in range(nb_case_cote):
            x_case: int = coord[0] + colonne * longueur_cote_case
            y_case: int = coord[1] + rangee * longueur_cote_case
            cases.append(
                creer_case(
                    canvas=canvas, 
                    tag=tag, 
                    coord=(x_case, y_case), 
                    longueur_cote=longueur_cote_case
                )
            )  
    
    carres: list[int] = []
    if nb_case_cote % nb_carre_cote == 0:
        longueur_cote_carre = longueur_cote_case * nb_case_cote // nb_carre_cote
        for i in range(nb_carre_cote):
            for j in range(nb_carre_cote):
                x_carre_1: int = coord[0] + longueur_cote_carre * i
                y_carre_2: int = coord[1] + longueur_cote_carre * j
                carres.append(
                    canvas.create_rectangle(
                        ((x_carre_1, y_carre_2), 
                         (x_carre_1 + longueur_cote_carre, y_carre_2 + longueur_cote_carre)),
                        fill="", 
                        width=3, 
                        tags=tag
                    )
                )
                
    sequence: str = "<Button-1>"
    FUNC = entree_focus_case
    for case in cases:
        case_vide: int = case["case_vide"]
        texte: int = case["texte"]
        canvas.tag_bind(
            tagOrId=case_vide, 
            sequence=sequence, 
            func=lambda event, case=case: FUNC(
                canvas=canvas, 
                case=case, 
                valeur_max=nb_case_cote, 
                cases=cases
            )
        )
        canvas.tag_bind(
            tagOrId=texte, 
            sequence=sequence, 
            func=lambda event, case=case: FUNC(
                canvas=canvas, 
                case=case, 
                valeur_max=nb_case_cote, 
                cases=cases
            )
        )
        
    return {"cases" : cases, "carres" : carres}


def remplir_grille_sudoku_GUI(
    canvas: tk.Canvas, 
    cases: list[dict[str, int]], 
    grille_valeur: list[list[int]]
) -> None:
    
    for rangee in range(len(grille_valeur)):
        for colonne in range(len(grille_valeur[0])):
            if grille_valeur[rangee][colonne] != 0:
                case: tuple[int] = cases[rangee * len(grille_valeur[0]) + colonne]
                case_vide: int = case["case_vide"]
                texte: int = case["texte"]
                desactiver_widget(
                    canvas=canvas, 
                    tags_ou_ids=[case_vide, texte]
                )
                canvas.itemconfig(
                    tagOrId=case_vide, 
                    fill=COULEUR_CASE_VERR
                )
                canvas.itemconfig(
                    tagOrId=texte, 
                    text=grille_valeur[rangee][colonne]
                )


def interagir_barre_sauv(
    event, 
    canvas: tk.Canvas, 
    tag_barre_sauv: str, 
    nom_sauv: str, 
    cases: list[dict[str, int]], 
    cases_verr: list[dict[str, int]],
    temps: int, 
    page: list[str | int], 
    type_grille: str, 
    difficulte: str
) -> None:
    
    if event.keysym in ["Return", "Escape"]:
        cases_vides_verr: list[int] = [case["case_vide"] for case in cases_verr]
        textes_verr: list[int] = [case["texte"] for case in cases_verr]
        if event.keysym == "Return":
            if nom_sauv == "":
                nom_sauv = "Aucun nom"
            grille: list[list[int]] = []
            nombre_cases_cote_grille: int = math.sqrt(len(cases))
            for i in range(nombre_cases_cote_grille):
                rangee: list[int] = []
                for j in range(nombre_cases_cote_grille):
                    indice: int = i * nombre_cases_cote_grille + j
                    texte: str = canvas.itemcget(
                        tagOrId=cases[indice]["texte"], 
                        option="text"
                    )
                    rangee.append(texte)
                grille.append(rangee)
            cases_verr_indices: list[int] = [cases.index(case) for case in cases if case in cases_verr]
            date: datetime.datetime = datetime.datetime.now()
            date_str: str = "%02d/%02d/%04d - %02dh %02dmin %02ds" % \
                (date.day, date.month, date.year, date.hour, date.minute, date.second)
            temps_str: str = f"{temps // 60}min {temps % 60}s"
            sauvegarder(
                nom=nom_sauv, 
                grille_actuelle=grille,  
                cases_verr=cases_verr_indices, 
                temps=temps_str, 
                date=date_str, 
                type_grille=type_grille, 
                statut="en_cours", 
                difficulte=difficulte
            )
        canvas.delete(tag_barre_sauv)
        activer_widget(
            canvas=canvas, 
            tags_ou_ids=page
        )
        desactiver_widget(
            canvas=canvas, 
            tags_ou_ids=cases_vides_verr + textes_verr
        )


def barre_entree_sauv(
    canvas: tk.Canvas, 
    largeur: int, 
    hauteur: int, 
    epaisseur_cadre: int, 
    page: list[str | int], 
    cases: list[dict[str, int]], 
    temps: int, 
    difficulte: str, 
    tag: str, 
    type_grille: str
) -> dict[str, int | tk.Entry]:
    
    desactiver_widget(
        canvas=canvas, 
        tags_ou_ids=page
    )
    reset_focus_cases(
        canvas=canvas, 
        cases=cases
    )

    x_cadre: int = (LARGEUR_PIXEL_FENETRE - largeur) // 2
    y_cadre: int = (HAUTEUR_PIXEL_FENETRE - hauteur) // 2
    x_fenetre: int = x_cadre + epaisseur_cadre
    y_fenetre: int = y_cadre + epaisseur_cadre
    largeur_fenetre: int = largeur - 2 * epaisseur_cadre
    hauteur_fenetre: int = hauteur - 2 * epaisseur_cadre

    
    cadre: int = creer_cadre(
        canvas=canvas, 
        coord=(x_cadre, y_cadre), 
        largeur=largeur, 
        hauteur=hauteur, 
        couleur="#3C3936", 
        rayon_coins=epaisseur_cadre, 
        tag=tag
    )
    
    entree: tk.Entry = tk.Entry(
        master=canvas, 
        justify="center", 
        font=("Century", int(1 / 4  * hauteur))
    )

    fenetre: int = canvas.create_window(
        (x_fenetre, y_fenetre), 
        width=largeur_fenetre, 
        height=hauteur_fenetre, 
        window=entree, 
        tags=tag, 
        anchor=tk.NW
    )
    
    cases_verr: list[dict[str, int]] = trouver_cases_verrouillee(
        canvas=canvas, 
        cases=cases
    )

    canvas.bind_all(
        sequence="<KeyPress>", 
        func=lambda event: interagir_barre_sauv(
            event, 
            canvas=canvas, 
            tag_barre_sauv=tag, 
            nom_sauv=entree.get(), 
            cases=cases, 
            cases_verr=cases_verr, 
            temps=temps, 
            difficulte=difficulte, 
            page=page, 
            type_grille=type_grille
        )
    )

    return {"fenetre" : fenetre, "entree" : entree, "cadre" : cadre}


def creer_bouton_rect(
    canvas: tk.Canvas, 
    coord: tuple[int, int], 
    largeur: int, 
    hauteur: int, 
    tag: str, 
    texte: str, 
    couleur_fond: str, 
    couleur_texte: str, 
    epaisseur_bordure: int, 
    couleur_bordure: str, 
    police: tuple[str | int, ...]
) -> dict[str, list[int] | int]:
    
    bordure: list[int] = creer_cadre(
        canvas=canvas, 
        coord=coord, 
        largeur=largeur, 
        hauteur=hauteur, 
        couleur=couleur_bordure, 
        rayon_coins=epaisseur_bordure, 
        tag=tag
    )
    
    x_fond: int = coord[0] + epaisseur_bordure
    y_fond: int = coord[1] + epaisseur_bordure  
    largeur_fond: int = largeur - 2 * epaisseur_bordure
    hauteur_fond: int = hauteur - 2 * epaisseur_bordure
    fond: int = canvas.create_rectangle(
        (x_fond, y_fond), 
        (x_fond + largeur_fond, y_fond + hauteur_fond), 
        fill=couleur_fond, 
        outline=couleur_fond, 
        tags=tag
    )
    
    if texte != "":
        texte_bouton: int = canvas.create_text(
            (coord[0] + largeur // 2, coord[1] + hauteur // 2), 
            text=texte, 
            font=police, 
            anchor=tk.CENTER, 
            fill=couleur_texte, 
            tags=tag
        )
        
    return {"fond" : fond, "bordure" : bordure, "texte" : texte_bouton}


def creer_fiche_sauv(
    canvas: tk.Canvas, 
    coord: tuple[int, int], 
    largeur: int, 
    hauteur: int, 
    tag: str, 
    nom_sauv: str, 
    date: str, 
    temps: str,
    difficulte: str,
    type_grille: str, 
    statut: str,
    couleur_fond: str, 
    couleur_texte: str, 
    epaisseur_bordure_fiche: int, 
    epaisseur_bordure_boutons: int, 
    couleur_bordure: str, 
    style_police_texte: str, 
    style_police_boutons: str
) -> dict[str, dict[str, list[int] | dict[str, int]] | dict[str, list[int] | int]]:
    
    bordure: list[int] = creer_cadre(
        canvas=canvas, 
        coord=coord, 
        largeur=largeur, 
        hauteur=hauteur, 
        couleur=couleur_bordure, 
        rayon_coins=epaisseur_bordure_fiche, 
        tag=tag
    )
    
    RAYON_COINS_FOND: int = 0
    x_fond: int = coord[0] + epaisseur_bordure_fiche
    y_fond: int = coord[1] + epaisseur_bordure_fiche  
    largeur_fond: int = largeur - 2 * epaisseur_bordure_fiche
    hauteur_fond: int = hauteur - 2 * epaisseur_bordure_fiche
    fond: list[int] = creer_cadre(
        canvas=canvas, 
        coord=(x_fond, y_fond), 
        largeur=largeur_fond, 
        hauteur=hauteur_fond, 
        couleur=couleur_fond, 
        rayon_coins=RAYON_COINS_FOND, 
        tag=tag
    )
    
    textes: dict[str, int] = {}

    x_textes: int = coord[0] + epaisseur_bordure_fiche + 10
    ecart_vertical: int =  hauteur_fond // 8 
    taille_police_nom: int = hauteur_fond // 6 

    if len(nom_sauv) > 20:
        nom_sauv = nom_sauv[:20] + "..."

    textes["nom_sauvegarde"] = \
        canvas.create_text(
            (x_textes, 
             coord[1] + epaisseur_bordure_fiche + ecart_vertical), 
            anchor=tk.NW, 
            fill=couleur_texte, 
            font=(style_police_texte, taille_police_nom), 
            text=nom_sauv
        )

    taille_police_type: int = hauteur_fond // 10

    textes["type_grille"] = \
        canvas.create_text(
            (x_textes, 
             coord[1] + epaisseur_bordure_fiche + 2 * ecart_vertical + taille_police_nom), 
            anchor=tk.NW, 
            fill=couleur_texte, 
            font=(style_police_texte, taille_police_type), 
            text=f"{type_grille.lower().capitalize()} {difficulte.lower()}"
        )
    
    taille_police_statut: int = hauteur_fond // 10

    if statut == "termine":

        textes["statut"] = \
            canvas.create_text(
                (x_textes, 
                 coord[1] + epaisseur_bordure_fiche + 3 * ecart_vertical + \
                    taille_police_nom + taille_police_type), 
                anchor=tk.NW, 
                fill=couleur_texte, 
                font=(style_police_texte, taille_police_statut), 
                text=f"Partie terminée - meilleur temps : {temps}"
            )
    
    elif statut == "en_cours":

        textes["statut"] = \
            canvas.create_text(
                (x_textes, 
                 coord[1] + epaisseur_bordure_fiche + 3 * ecart_vertical + \
                    taille_police_nom + taille_police_type), 
                anchor=tk.NW, 
                fill=couleur_texte, 
                font=(style_police_texte, taille_police_statut), 
                text=f"Partie en cours - temps : {temps}"
            )
        
    taille_police_date: int = hauteur_fond // 13

    textes["date"] = \
        canvas.create_text(
            (x_textes, 
             coord[1] + epaisseur_bordure_fiche + 4 * ecart_vertical + \
                taille_police_nom + taille_police_type + taille_police_statut), 
            anchor=tk.NW, 
            fill=couleur_texte, 
            font=(style_police_texte, taille_police_date), 
            text=date
        )

    fiche: dict[str, list[int] | dict[str, int]] = \
        {"fond" : fond, "bordure" : bordure, "textes" : textes}

    y_boutons: int = y_fond + hauteur_fond // 5
    hauteur_boutons: int = 3 * hauteur_fond // 5
    ecart_horizontal: int = largeur_fond // 32
    largeur_boutons: int = 15 * largeur_fond // 64
    police_boutons: tuple[str, int] = (style_police_boutons, hauteur_boutons // 4)

    x_suppr: int = x_fond + largeur_fond - ecart_horizontal - largeur_boutons
    bouton_suppr: dict[str, list[int] | int] = \
        creer_bouton_rect(
            canvas=canvas, 
            coord=(x_suppr, y_boutons), 
            largeur=largeur_boutons, 
            hauteur=hauteur_boutons, 
            tag=tag, 
            texte="Suppr", 
            couleur_bordure=couleur_bordure, 
            couleur_fond=couleur_fond, 
            couleur_texte=couleur_texte, 
            epaisseur_bordure=epaisseur_bordure_boutons, 
            police=police_boutons
        )
    
    x_charger: int = x_suppr - ecart_horizontal - largeur_boutons
    bouton_charger: dict[str, list[int] | int] = \
        creer_bouton_rect(
            canvas=canvas, 
            coord=(x_charger, y_boutons), 
            largeur=largeur_boutons, 
            hauteur=hauteur_boutons, 
            tag=tag, 
            texte="Charger", 
            couleur_bordure=couleur_bordure, 
            couleur_fond=couleur_fond, 
            couleur_texte=couleur_texte, 
            epaisseur_bordure=epaisseur_bordure_boutons, 
            police=police_boutons
        )
    
    return  {"fiche" : fiche, "bouton_charger" : bouton_charger, "bouton_suppr" : bouton_suppr}


def creer_grille_sudoku_irregulier(
    canvas: tk.Canvas, 
    tag: str, 
    coord: tuple[int, int], 
    nb_case_cote: int, 
    longueur_cote_case: int, 
    plan_cage: list[list[int]]
) -> dict[str, list[dict[str, int]] | list[int]]:
    """
    Permet de dessiner une grille de sudoku irregulier.
    """
    # Son format : [ {"case_vide": 1, "texte": 2} ...] où 1 et 2 sont les identifiants de la case vide et le texte
    cases: list[dict[str, int]] = []
    
    # Quadrilage de base à l'aide de deux boucles
    for rangee in range(nb_case_cote):
        for colonne in range(nb_case_cote):
            # On calcule la position exacte pour chaque case
            x_case: int = coord[0] + colonne * longueur_cote_case
            y_case: int = coord[1] + rangee * longueur_cote_case
            
            # On crée cette case
            nouvelle_case = creer_case(
                canvas=canvas, 
                tag=tag, 
                coord=(x_case, y_case), 
                longueur_cote=longueur_cote_case
            )
            cases.append(nouvelle_case) 
    
    # Création du pourtour
    bordures: list[int] = [] 
    longueur_totale: int = nb_case_cote * longueur_cote_case
    
    cadre_exterieur = creer_cadre(
        canvas=canvas, 
        coord=coord, 
        largeur=longueur_totale, 
        hauteur=longueur_totale, 
        couleur="#000000", 
        rayon_coins=0,
        tag=tag
    )
    bordures.extend(cadre_exterieur) 

    # Delimitation des bordures des cages
    EPAISSEUR_BORDURE: int = 3 
    
    for i in range(nb_case_cote):
        for j in range(nb_case_cote):
            # On détermine les coordonnées des 4 coins de notre case traitée
            x1: int = coord[0] + j * longueur_cote_case
            y1: int = coord[1] + i * longueur_cote_case
            x2: int = x1 + longueur_cote_case
            y2: int = y1 + longueur_cote_case
            

            num_cage: int = plan_cage[i][j]
            
            # On détermine si notre case actuelle est limitrophe à droite d'une autre cage
            # Ce qui revient à voir si la case à droite de celle qu'on traite est differente et evidemment qj'on ne soit pas dans la derniere colonne
            if j < nb_case_cote - 1 and plan_cage[i][j+1] != num_cage:
                bordures.append(
                    canvas.create_line(x2, y1, x2, y2, fill="#000000", width=EPAISSEUR_BORDURE, tags=tag)
                )
                
            # De meme on regarde si notre case est limitrophe en bas
            # Ce qui revient à voir si la case en bas de celle qu'on traite est differente et qu'evidemment qu'on ne soit pas dans la derniere ligne
            if i < nb_case_cote - 1 and plan_cage[i+1][j] != num_cage:
                bordures.append(
                    canvas.create_line(x1, y2, x2, y2, fill="#000000", width=EPAISSEUR_BORDURE, tags=tag)
                )

    # Maintenant faisons que les cases soient interactives
    sequence: str = "<Button-1>"
    FUNC = entree_focus_case
    for case in cases:
        case_vide: int = case["case_vide"]
        texte: int = case["texte"]
        canvas.tag_bind(
            tagOrId=case_vide, 
            sequence=sequence, 
            func=lambda event, case=case: FUNC(
                canvas=canvas, 
                case=case, 
                valeur_max=nb_case_cote, 
                cases=cases
            )
        )
        canvas.tag_bind(
            tagOrId=texte, 
            sequence=sequence, 
            func=lambda event, case=case: FUNC(
                canvas=canvas, 
                case=case, 
                valeur_max=nb_case_cote, 
                cases=cases
            )
        )
        
    return {"cases": cases, "bordures": bordures}

def ajouter_indications_kenken(canvas: tk.Canvas, dico_cage: dict, x_grille: int, y_grille: int, longueur_cote_case: int, tag: str):
    """ Ajoute les indications des cibles et des opérations pour le Kenken"""
    
    for nom_cage in dico_cage:
        # On accède directement aux données avec les clés
        infos_cage = dico_cage[nom_cage]
        cible = infos_cage["cible"]
        operation = infos_cage["operation"]

        texte_indication = str(cible) + str(operation)

        liste_cases = infos_cage["cases"]

        # On doit trouver la case la plus haute et la plus à gauche parmi ces cases
        case_haut_gauche = liste_cases[0] 

        for case in liste_cases:
        # Si la ligne est plus haute, ou si ligne est à la meme hauteur mais plus à gauche
            if case[0] < case_haut_gauche[0] or (case[0] == case_haut_gauche[0] and case[1] < case_haut_gauche[1]):
                case_haut_gauche = case

        lig, col = case_haut_gauche

        # Calcul des coordonnées 
        x_texte = x_grille + (col * longueur_cote_case) + 4
        y_texte = y_grille + (lig * longueur_cote_case) + 4

        canvas.create_text(
            x_texte, 
            y_texte,
            text=texte_indication,
            anchor="nw",
            font=("Arial", 10, "bold"),
            fill="black",
            tags=(tag, "indication_kenken")
        )