import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.widgets import creer_boutton, survole_non_survole
from GUI.animations import mouvement_exterieur_fond_menu, retour_menu


def aller_stats(canvas: tk.Canvas) -> None:
    """
    Affiche la page des statistiques
    """
    mouvement_exterieur_fond_menu(canvas)

    TAG: str = "stats"

    # fond
    COULEUR_FOND: str = "#373737"

    canvas.create_rectangle((0, 0), (LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE), 
                            fill=COULEUR_FOND, outline=COULEUR_FOND, tags=TAG)
    
    # texte / titre
    COULEUR_TEXT: str = "#ffffff"
    POLICE: str = "Bell MT"

    canvas.create_text((LARGEUR_PIXEL_FENETRE // 2, 50), anchor=tk.CENTER, text="Statistiques", 
                       fill=COULEUR_TEXT, font=(POLICE, 60), tags=TAG)
    
    # cadre
    COULEUR_CADRE: str = "#444444"
    ECART_CENTRE: int = 250
    XY1: tuple[int, int] = (LARGEUR_PIXEL_FENETRE // 2 - ECART_CENTRE, 110)
    XY2: tuple[int, int] = (LARGEUR_PIXEL_FENETRE // 2 + ECART_CENTRE, 500)

    canvas.create_rectangle(XY1, XY2, fill=COULEUR_CADRE, outline=COULEUR_CADRE, tags=TAG)

    # texte / stats
    PARAMS_TEXT: dict[str, str | tuple[str, int]] = {
        "anchor" : tk.W, 
        "fill" : COULEUR_TEXT, 
        "font" : (POLICE, 15), 
        "tags" : TAG
        }

    X_TEXT: int = XY1[0] + 20

    canvas.create_text((X_TEXT, 140), text="Parties terminées : ", **PARAMS_TEXT)
    canvas.create_text((X_TEXT, 170), text="Parties niveau facile terminées : ", **PARAMS_TEXT)
    canvas.create_text((X_TEXT, 200), text="Parties niveau moyen terminées : ", **PARAMS_TEXT)
    canvas.create_text((X_TEXT, 230), text="Parties niveau difficile terminées : ", **PARAMS_TEXT)
    canvas.create_text((X_TEXT, 260), text="Erreurs commises : ", **PARAMS_TEXT)
    canvas.create_text((X_TEXT, 290), text="Moyenne erreurs commises par partie : ", **PARAMS_TEXT)
    canvas.create_text((X_TEXT, 320), text="Aides utilisées : ", **PARAMS_TEXT)
    canvas.create_text((X_TEXT, 350), text="Moyenne aides utilisées par partie : ", **PARAMS_TEXT)
    canvas.create_text((X_TEXT, 380), text="Puzzles terminés : ", **PARAMS_TEXT)

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

    fond_retour, bordure_retour =  \
        creer_boutton(canvas, coord=(X_BOUTON, Y_BOUTON), tag=TAG_RETOUR, 
                    texte="Retour", largeur=LARGEUR_BOUTON, hauteur=HAUTEUR_BOUTON,  
                    police=("Cooper Black", 16), epaisseur_bordure=2, 
                    **COULEUR_BOUTON)[:-1]
    
    survole_non_survole(canvas, tag=TAG_RETOUR, fond=fond_retour, 
                        bordure=bordure_retour, **(COULEUR_BOUTON | COULEURS_SURVOLE))
    
    canvas.tag_bind(TAG_RETOUR, "<Button-1>", 
                lambda event: retour_menu(canvas, tags_or_ids=[TAG, TAG_RETOUR]))