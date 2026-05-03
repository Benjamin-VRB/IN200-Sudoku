import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.widgets import creer_boutton_arrondi, survole_non_survole
from GUI.animations import retour_menu, mouvement_exterieur_fond_menu
from GUI.decorations import creer_cadre

def aller_menu_partie_perso(canvas: tk.Canvas) -> None:

    mouvement_exterieur_fond_menu(canvas=canvas)

    TAG: str = "menu_parties_perso"

    COULEUR_FOND: str = "#373737"

    canvas.create_rectangle(
        ((0, 0), (LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE)), 
        fill=COULEUR_FOND, 
        outline=COULEUR_FOND, 
        tags=TAG
    )

    POLICE: str = "Bell MT"

    PARAMS_TEXT: dict[str, str] = {
        "anchor" : tk.CENTER, 
        "fill" : "#ffffff",  
        "tags" : TAG
    }

    canvas.create_text(
        (LARGEUR_PIXEL_FENETRE // 2, 50), 
        text="Partie personnalisée", 
        font=(POLICE, 50), 
        **PARAMS_TEXT
    )

    X_CADRE: int = 400
    Y_CADRE: int = 130
    LARGEUR: int = LARGEUR_PIXEL_FENETRE - X_CADRE - 50
    HAUTEUR: int = HAUTEUR_PIXEL_FENETRE - Y_CADRE - 50
    RAYON_COINS: int = 30
    COULEUR_CADRE = "#444444"

    creer_cadre(
        canvas=canvas, 
        coord=(X_CADRE, Y_CADRE), 
        largeur=LARGEUR, 
        hauteur=HAUTEUR, 
        rayon_coins=RAYON_COINS, 
        couleur=COULEUR_CADRE, 
        tag=TAG
    )

    LARGEUR_BOUTON: int = 300
    HAUTEUR_BOUTON: int = 124

    COULEUR_BOUTON: dict[str, str] = {
        "couleur_fond" : "#939393",
        "couleur_bordure" : "#ADADAD"
    }

    COULEURS_SURVOLE: dict[str, str] = {
        "couleur_fond_surv" : "#636363",
        "couleur_bordure_surv" : "#454545"
    }

    PARAMS_BOUTONS: dict[str, str | int | tuple[str | int, ...]] = {
        "largeur" : 300, 
        "hauteur" : 124,
        "police" : ("Cooper Black", 16), 
        "epaisseur_bordure" : 2, 
        "couleur_texte" : "#ffffff"
    }.update(COULEUR_BOUTON)

    X_BOUTON_RETOUR: int = 50
    Y_BOUTON_RETOUR: int = HAUTEUR_PIXEL_FENETRE - HAUTEUR_BOUTON - 150
    TAG_RETOUR: str = "bouton_menu_partie_perso_retour"

    bouton_retour: dict[str, list[int] | int] =  \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(X_BOUTON_RETOUR, Y_BOUTON_RETOUR), 
            tag=TAG_RETOUR, 
            texte="Retour", 
            largeur=LARGEUR_BOUTON, 
            hauteur=HAUTEUR_BOUTON,  
            **PARAMS_BOUTONS
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

    TAG_JOUER: str = "bouton_credits_retour"

    bouton_retour: dict[str, list[int] | int] =  \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(X_BOUTON_RETOUR, Y_BOUTON_RETOUR), 
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