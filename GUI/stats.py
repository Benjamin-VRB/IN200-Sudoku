import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.widgets import creer_boutton_arrondi, survole_non_survole
from GUI.animations import mouvement_exterieur_fond_menu, retour_menu
from GUI.decorations import creer_cadre


def aller_stats(canvas: tk.Canvas) -> None:
    """
    Affiche la page des statistiques
    """
    mouvement_exterieur_fond_menu(canvas=canvas)

    TAG: str = "stats"

    # fond
    COULEUR_FOND: str = "#373737"

    canvas.create_rectangle(
        ((0, 0), (LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE)), 
        fill=COULEUR_FOND, 
        outline=COULEUR_FOND, 
        tags=TAG
    )
    
    # texte / titre
    COULEUR_TEXT: str = "#ffffff"
    POLICE: str = "Bell MT"

    canvas.create_text(
        (LARGEUR_PIXEL_FENETRE // 2, 50), 
        anchor=tk.CENTER, 
        text="Statistiques", 
        fill=COULEUR_TEXT, 
        font=(POLICE, 60), 
        tags=TAG
    )
    
    # cadre
    COULEUR_CADRE: str = "#444444"
    ECART_CENTRE: int = 250
    XY: tuple[int, int] = (LARGEUR_PIXEL_FENETRE // 2 - ECART_CENTRE, 110)
    LARGEUR_CADRE: int = 2 * ECART_CENTRE
    HAUTEUR_CADRE: int = 390
    RAYON_COINS: int = 20

    creer_cadre(
        canvas=canvas, 
        coord=XY, 
        largeur=LARGEUR_CADRE, 
        hauteur=HAUTEUR_CADRE, 
        couleur=COULEUR_CADRE, 
        rayon_coins=RAYON_COINS, 
        tag=TAG
    )

    # texte / stats
    PARAMS_TEXT: dict[str, str | tuple[str, int]] = {
        "anchor" : tk.W, 
        "fill" : COULEUR_TEXT, 
        "font" : (POLICE, 15), 
        "tags" : TAG
    }

    X_TEXT: int = XY[0] + 20

    canvas.create_text(
        (X_TEXT, 140), 
        text="Parties terminées : ", 
        **PARAMS_TEXT
    )

    canvas.create_text(
        (X_TEXT, 170), 
        text="Parties niveau facile terminées : ", 
        **PARAMS_TEXT
    )

    canvas.create_text(
        (X_TEXT, 200), 
        text="Parties niveau moyen terminées : ", 
        **PARAMS_TEXT
    )

    canvas.create_text(
        (X_TEXT, 230), 
        text="Parties niveau difficile terminées : ", 
        **PARAMS_TEXT
    )

    canvas.create_text(
        (X_TEXT, 260), 
        text="Erreurs commises : ", 
        **PARAMS_TEXT
    )

    canvas.create_text(
        (X_TEXT, 290), 
        text="Moyenne erreurs commises par partie : ", 
        **PARAMS_TEXT
    )

    canvas.create_text(
        (X_TEXT, 320), 
        text="Aides utilisées : ", 
        **PARAMS_TEXT
    )

    canvas.create_text(
        (X_TEXT, 350), 
        text="Moyenne aides utilisées par partie : ", 
        **PARAMS_TEXT
    )

    canvas.create_text(
        (X_TEXT, 380), 
        text="Puzzles terminés : ", 
        **PARAMS_TEXT
    )

    # bouton de retour au menu
    LARGEUR_BOUTON: int = 300
    HAUTEUR_BOUTON: int = 124
    X_BOUTON: int = (LARGEUR_PIXEL_FENETRE - LARGEUR_BOUTON) // 2
    Y_BOUTON: int = HAUTEUR_PIXEL_FENETRE - HAUTEUR_BOUTON - 50

    COULEUR_BOUTON: dict[str, str] = {
        "couleur_fond" : "#939393",
        "couleur_bordure" : "#ADADAD"
    }

    COULEURS_SURVOLE: dict[str, str] = {
        "couleur_fond_surv" : "#636363",
        "couleur_bordure_surv" : "#454545"
    }

    TAG_RETOUR: str = "bouton_stats_retour"

    bouton_retour: dict[str, list[int] | int] = \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(X_BOUTON, Y_BOUTON), 
            tag=TAG_RETOUR, 
            texte="Retour", 
            largeur=LARGEUR_BOUTON, 
            hauteur=HAUTEUR_BOUTON, 
            police=("Cooper Black", 16), 
            epaisseur_bordure=2, 
            couleur_texte="#ffffff", 
            **COULEUR_BOUTON
        )
    
    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_RETOUR], 
        fond=bouton_retour["fond"], 
        bordure=bouton_retour["bordure"], 
        **(COULEUR_BOUTON | COULEURS_SURVOLE)
    )
    
    canvas.tag_bind(
        tagOrId=TAG_RETOUR, 
        sequence="<Button-1>", 
        func=lambda event: retour_menu(
            canvas=canvas, 
            tags_ou_ids=[TAG, TAG_RETOUR]
        )
    )