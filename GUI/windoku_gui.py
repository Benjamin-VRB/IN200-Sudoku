import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.animations import supprimer_elements, retour_menu
from GUI.widgets import creer_grille_sudoku, creer_boutton_arrondi, survole_non_survole,barre_entree_sauv, desactiver_widget, COULEUR_CASE, afficher_conflits, COULEUR_CASE_VERR, COULEUR_CASE_VERR, COULEUR_CASE_PROBLEME, COULEUR_CASE_PROBLEME_VERR, trouver_cases_verrouillee, entree_focus_case, renvoyer_grille
from Grille.verification import verification_windoku_complet
from Grille.windoku import supprimer_valeur

COULEUR_WINDOKU: str = "#B9B9FA"
COULEUR_WINDOKU_VERR: str = "#9B9BD1"

REGIONS_WINDOKU: list[list[tuple[int, int]]] = [
    [(i, j) for i in range(1, 4) for j in range(1, 4)],
    [(i, j) for i in range(1, 4) for j in range(5, 8)],
    [(i, j) for i in range(5, 8) for j in range(1, 4)],
    [(i, j) for i in range(5, 8) for j in range(5, 8)],
]

def _couleur_case_windoku(rangee: int, colonne: int, verrouille: bool) -> str | None:
    """Retourne la couleur windoku d'une case si elle appartient à une région, sinon None."""
    for region in REGIONS_WINDOKU:
        if (rangee, colonne) in region:
            return COULEUR_WINDOKU_VERR if verrouille else COULEUR_WINDOKU
    return None

def reset_couleur_cases_rouges_windoku(
        canvas: tk.Canvas,
        cases: list[dict[str, int]],
) -> None:
    nb_colonnes: int = 9
    cases_verr: list[dict[str, int]] = trouver_cases_verrouillee(canvas=canvas, cases=cases)

    for index, case in enumerate(cases):
        case_vide: int = case["case_vide"]
        couleur_actuelle: str = canvas.itemcget(tagOrId=case_vide, option="fill")

        if couleur_actuelle not in (COULEUR_CASE_PROBLEME, COULEUR_CASE_PROBLEME_VERR):
            continue

        rangee: int = index // nb_colonnes
        colonne: int = index % nb_colonnes
        verrouille: bool = case in cases_verr
        couleur_windoku: str | None = _couleur_case_windoku(rangee, colonne, verrouille)

        if couleur_windoku:
            canvas.itemconfig(tagOrId=case_vide, fill=couleur_windoku)
        elif verrouille:
            canvas.itemconfig(tagOrId=case_vide, fill=COULEUR_CASE_VERR)
        else:
            canvas.itemconfig(tagOrId=case_vide, fill=COULEUR_CASE)

def afficher_conflits_windoku(
        canvas: tk.Canvas,
        list_coord: list[tuple[int, int]],
        cases: list[dict[str, int]],
) -> None:
    reset_couleur_cases_rouges_windoku(canvas=canvas, cases=cases)

    cases_verr: list[dict[str, int]] = trouver_cases_verrouillee(
        canvas=canvas, cases=cases
    )

    for coord in list_coord:
        indice: int = coord[0] * 9 + coord[1]
        case: dict[str, int] = cases[indice]
        case_vide: int = case["case_vide"]
        if case in cases_verr:
            canvas.itemconfig(tagOrId=case_vide, fill=COULEUR_CASE_PROBLEME_VERR)
        else:
            canvas.itemconfig(tagOrId=case_vide, fill=COULEUR_CASE_PROBLEME)

def remplir_grille_windoku_GUI(
        canvas: tk.Canvas,
        cases: list[dict[str, int]],
        grille_valeur: list[list[int]],
) -> None:
    """
    Remplit la grille windoku au démarrage d'une nouvelle partie.
    Les cases non nulles sont verrouillées. Les régions windoku sont colorées.
    """
    nb_colonnes: int = len(grille_valeur[0])

    for rangee, ligne in enumerate(grille_valeur):
        for colonne, valeur in enumerate(ligne):
            index: int = rangee * nb_colonnes + colonne
            case: dict[str, int] = cases[index]
            case_vide: int = case["case_vide"]
            texte: int = case["texte"]

            couleur_windoku: str | None = _couleur_case_windoku(rangee, colonne, verrouille=(valeur != 0))

            if valeur != 0:
                desactiver_widget(canvas=canvas, tags_ou_ids=[case_vide, texte])
                canvas.itemconfig(
                    case_vide,
                    fill=couleur_windoku if couleur_windoku else COULEUR_CASE_VERR,  # gris si hors région
                )
                canvas.itemconfig(texte, text=str(valeur))
            else:
                if couleur_windoku:
                    canvas.itemconfig(case_vide, fill=couleur_windoku)


def remplir_grille_windoku_GUI_en_cours(
        canvas: tk.Canvas,
        cases: list[dict[str, int]],
        grille_valeur: list[list[int]],
        indices_cases_verr: list[int],
) -> None:
    """
    Remplit la grille windoku lors d'une reprise de partie sauvegardée.
    Les cases dont l'index est dans indices_cases_verr sont verrouillées.
    """
    nb_colonnes: int = len(grille_valeur[0])

    for rangee, ligne in enumerate(grille_valeur):
        for colonne, valeur in enumerate(ligne):
            index: int = rangee * nb_colonnes + colonne
            case: dict[str, int] = cases[index]
            case_vide: int = case["case_vide"]
            texte: int = case["texte"]

            verrouille: bool = index in indices_cases_verr
            couleur_windoku: str | None = _couleur_case_windoku(rangee, colonne, verrouille=verrouille)

            if valeur != 0:
                if verrouille:
                    desactiver_widget(canvas=canvas, tags_ou_ids=[case_vide, texte])
                canvas.itemconfig(
                    case_vide,
                    fill=couleur_windoku if couleur_windoku else COULEUR_CASE,
                )
                canvas.itemconfig(texte, text=str(valeur))
            else:
                if couleur_windoku:
                    canvas.itemconfig(case_vide, fill=couleur_windoku)


def creer_windoku_GUI(
        canvas: tk.Canvas,
        coord: tuple[int, int],
        nb_case_cote: int,
        longueur_cote_case: int,
        nb_carre_cote: int,
        tag: str,
        couleur_cases: str,
        couleur_bordure_cases: str,
        couleur_textes: str,
        difficulte: int = None,
        grille_par_defaut: list[list[int]] = None,
        indices_cases_verr: list[int] = None,
) -> dict[str, list[dict[str, int]] | list[int]]:
    """
    Crée et remplit la grille windoku dans le canvas.
    Même signature que creer_sudoku_GUI, avec coloration des régions windoku.
    """
    if difficulte is None and grille_par_defaut is None:
        return

    grille: dict[str, list[dict[str, int]] | list[int]] = \
        creer_grille_sudoku(
            canvas=canvas,
            tag=tag,
            coord=coord,
            nb_case_cote=nb_case_cote,
            longueur_cote_case=longueur_cote_case,
            nb_carre_cote=nb_carre_cote,
            couleur_cases=couleur_cases,
            couleur_bordure_cases=couleur_bordure_cases,
            couleur_textes=couleur_textes,
        )

    cases: list[dict[str, int]] = grille["cases"]

    def func_conflits_windoku():
        grille_valeur = renvoyer_grille(canvas=canvas, cases=cases)
        list_coord = verification_windoku_complet(grille_valeur)
        afficher_conflits_windoku(canvas=canvas, list_coord=list_coord, cases=cases)
        
    for case in cases:
        for id in [case["case_vide"], case["texte"]]:
            canvas.tag_bind(
                tagOrId=id,
                sequence="<Button-1>",
                func=lambda event, c=case: entree_focus_case(
                    canvas=canvas,
                    case=c,
                    valeur_max=nb_case_cote,
                    cases=cases,
                    couleur_nombres_normale=couleur_textes,
                    couleur_bordure_cases_normale=couleur_bordure_cases,
                    func_afficher_conflits=func_conflits_windoku,
                )
            )


    if grille_par_defaut is None:
        if difficulte == 4:
            nombre_valeur_a_supprimer: int = 63
        elif difficulte == 3:
            nombre_valeur_a_supprimer: int = 56
        elif difficulte == 2:
            nombre_valeur_a_supprimer: int = 48
        elif difficulte == 1:
            nombre_valeur_a_supprimer: int = 40
        else:
            nombre_valeur_a_supprimer: int = 50


        grille_valeur: list[list[int]] = supprimer_valeur(
            nombre_valeur_a_supprimer=nombre_valeur_a_supprimer,
            dimension=nb_case_cote,
        )

        remplir_grille_windoku_GUI(
            canvas=canvas,
            cases=cases,
            grille_valeur=grille_valeur,
        )
    else:
        if indices_cases_verr is None:
            remplir_grille_windoku_GUI(
                canvas=canvas,
                cases=cases,
                grille_valeur=grille_par_defaut,
            )
        else:
            remplir_grille_windoku_GUI_en_cours(
                canvas=canvas,
                cases=cases,
                grille_valeur=grille_par_defaut,
                indices_cases_verr=indices_cases_verr,
            )

    return grille

def aller_windoku(
        canvas: tk.Canvas,
        difficulte: int | None,
        temps_depart: int,
        tags_ou_ids_page_suppr: list[int | str] = None,
        widgets_page_suppr: list[tk.Widget] = None,
        grille_par_defaut: list[list[int]] = None,
        indices_cases_verr: list[int] = None,
) -> None:

    COULEUR_BORDURE_CASES: str = "#000000"
    COULEUR_TEXTE_CASES: str = "#000000"

    supprimer_elements(
        canvas=canvas,
        tags_ou_ids=tags_ou_ids_page_suppr,
        widgets=widgets_page_suppr,
    )

    TAG: str = "windoku"
    NB_CASE_COTE: int = 9
    LONGUEUR_COTE_GRILLE: int = NB_CASE_COTE * 60
    NB_CARRE_COTE: int = 3
    LONGUEUR_COTE_CASE: int = LONGUEUR_COTE_GRILLE // NB_CASE_COTE
    X_GRILLE: int = (LARGEUR_PIXEL_FENETRE - LONGUEUR_COTE_GRILLE) // 2
    Y_GRILLE: int = (HAUTEUR_PIXEL_FENETRE - LONGUEUR_COTE_GRILLE) // 2

    grille: dict[str, list[dict[str, int]] | list[int]] = creer_windoku_GUI(
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
        indices_cases_verr=indices_cases_verr,
    )

    cases: list[dict[str, int]] = grille["cases"]

    nb_colonnes: int = 9
    grille_valeur: list[list[int]] = [
        [int(canvas.itemcget(cases[i * nb_colonnes + j]["texte"], "text") or 0)
         for j in range(nb_colonnes)]
        for i in range(nb_colonnes)
    ]
    list_coord: list[tuple[int, int]] = verification_windoku_complet(grille_valeur)

    afficher_conflits_windoku(
        canvas=canvas,
        list_coord=list_coord,
        cases=cases,
    )

    PARAMS_BOUTON: dict[str, int | str | tuple[str, int]] = {
        "largeur": 200,
        "hauteur": 76,
        "police": ("Cooper Black", 16),
        "epaisseur_bordure": 2,
        "couleur_texte": "#ffffff",
    }

    COULEURS_BOUTON: dict[str, str] = {
        "couleur_fond": "#E0D4C1",
        "couleur_bordure": "#E9E0CE",
        "couleur_fond_surv": "#BEB2A4",
        "couleur_bordure_surv": "#A89E90",
    }

    ECART_RANGEE: int = PARAMS_BOUTON["hauteur"] + 100
    RANGEE2: int = (HAUTEUR_PIXEL_FENETRE - PARAMS_BOUTON["hauteur"]) // 2
    RANGEE1: int = RANGEE2 + ECART_RANGEE
    RANGEE3: int = RANGEE2 - ECART_RANGEE
    COLONNE1: int = 75

    TAG_AIDE: str = "bouton_windoku_aide"
    TAG_SAUV: str = "bouton_windoku_sauv"
    TAG_RETOUR: str = "bouton_windoku_retour"

    bouton_aide: dict[str, list[int] | int] = \
        creer_boutton_arrondi(
            canvas=canvas,
            coord=(COLONNE1, RANGEE3),
            tag=TAG_AIDE,
            texte="Aide",
            couleur_fond=COULEURS_BOUTON["couleur_fond"],
            couleur_bordure=COULEURS_BOUTON["couleur_bordure"],
            **PARAMS_BOUTON,
        )

    bouton_sauv: dict[str, list[int] | int] = \
        creer_boutton_arrondi(
            canvas=canvas,
            coord=(COLONNE1, RANGEE2),
            tag=TAG_SAUV,
            texte="Sauvegarder",
            couleur_fond=COULEURS_BOUTON["couleur_fond"],
            couleur_bordure=COULEURS_BOUTON["couleur_bordure"],
            **PARAMS_BOUTON,
        )

    bouton_retour: dict[str, list[int] | int] = \
        creer_boutton_arrondi(
            canvas=canvas,
            coord=(COLONNE1, RANGEE1),
            tag=TAG_RETOUR,
            texte="Retour",
            couleur_fond=COULEURS_BOUTON["couleur_fond"],
            couleur_bordure=COULEURS_BOUTON["couleur_bordure"],
            **PARAMS_BOUTON,
        )

    survole_non_survole(
        canvas=canvas,
        tags_ou_ids=[TAG_AIDE],
        fond=bouton_aide["fond"],
        bordure=bouton_aide["bordure"],
        couleurs=COULEURS_BOUTON,
    )

    survole_non_survole(
        canvas=canvas,
        tags_ou_ids=[TAG_SAUV],
        fond=bouton_sauv["fond"],
        bordure=bouton_sauv["bordure"],
        couleurs=COULEURS_BOUTON,
    )

    survole_non_survole(
        canvas=canvas,
        tags_ou_ids=[TAG_RETOUR],
        fond=bouton_retour["fond"],
        bordure=bouton_retour["bordure"],
        couleurs=COULEURS_BOUTON,
    )

    page: list[str] = [
        TAG, TAG_AIDE, TAG_RETOUR, TAG_SAUV,
        *[case["case_vide"] for case in grille["cases"]],
        *[case["texte"] for case in grille["cases"]],
    ]
    LARGEUR_BARRE_ENTREE_SAUV: int = 200
    HAUTEUR_BARRE_ENTREE_SAUV: int = 75
    EPAISSEUR_CADRE_BARRE_ENTREE_SAUV: int = 5
    TAG_BARRE_ENTREE_SAUV: str = "barre_entree_sauv_windoku"

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
            type_grille="windoku",
            temps=temps_depart,
            difficulte=difficulte,
            couleur_nombres_normale=COULEUR_TEXTE_CASES,
            couleur_bordure_cases_normale=COULEUR_BORDURE_CASES,
        ),
    )

    canvas.tag_bind(
        tagOrId=TAG_RETOUR,
        sequence="<Button-1>",
        func=lambda event: retour_menu(
            canvas=canvas,
            tags_ou_ids=[TAG, TAG_SAUV, TAG_RETOUR, TAG_AIDE, "clavier_num"],
        ),
    )

    