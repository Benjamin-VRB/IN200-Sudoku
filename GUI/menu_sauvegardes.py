import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.animations import mouvement_exterieur_fond_menu, retour_menu
from GUI.widgets import creer_boutton_arrondi, survole_non_survole, creer_fiche_sauv
from GUI.decorations import creer_cadre

def aller_menu_sauvegardes(canvas: tk.Canvas) -> None:

    mouvement_exterieur_fond_menu(canvas=canvas)

    TAG: str = "menu_sauvegardes"

    COULEUR_FOND: str = "#373737"

    canvas.create_rectangle((0, 0), (LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE), 
                            fill=COULEUR_FOND, outline=COULEUR_FOND, tags=TAG)
    
    COULEUR_TEXT: str = "#ffffff"
    POLICE: str = "Bell MT"

    canvas.create_text((LARGEUR_PIXEL_FENETRE - 70, 150), anchor=tk.E, text="Sauvegardes", 
                       fill=COULEUR_TEXT, font=(POLICE, 60), tags=TAG)
    
    COULEUR_CADRE: str = "#4E4E4E"
    XY_CADRE: tuple[int, int] = (20, 0)
    LARGEUR_CADRE: int = 700
    HAUTEUR_CADRE: int = HAUTEUR_PIXEL_FENETRE
    RAYON_COINS: int = 0

    creer_cadre(canvas=canvas, coord=XY_CADRE, largeur=LARGEUR_CADRE, hauteur=HAUTEUR_CADRE, 
                couleur=COULEUR_CADRE, rayon_coins=RAYON_COINS, tag=TAG)
    
    barre_defilement: tk.Scrollbar = tk.Scrollbar(canvas, bg=COULEUR_CADRE, width=HAUTEUR_CADRE)
    
    LARGEUR_BARRE_DEFILEMENT: int = 17
    X_BARRE_DEFILEMENT: int = XY_CADRE[0] + LARGEUR_CADRE - LARGEUR_BARRE_DEFILEMENT - 5
    Y_BARRE_DEFILEMENT: int = XY_CADRE[1] + 10
    HAUTEUR_FENETRE_BARRE_DEFILEMENT: int = HAUTEUR_CADRE - 20
    fenetre: int = canvas.create_window((X_BARRE_DEFILEMENT, Y_BARRE_DEFILEMENT), anchor=tk.NW, 
                                        window=barre_defilement, width=LARGEUR_BARRE_DEFILEMENT, 
                                        height=HAUTEUR_FENETRE_BARRE_DEFILEMENT, tags=TAG)
    
    LARGEUR_BOUTON: int = 300
    HAUTEUR_BOUTON: int = 124
    X_BOUTON: int = LARGEUR_PIXEL_FENETRE - LARGEUR_BOUTON - 75
    Y_BOUTON: int = HAUTEUR_PIXEL_FENETRE - HAUTEUR_BOUTON - 50

    COULEUR_BOUTON: dict[str, str] = {
        "couleur_fond" : "#939393",
        "couleur_bordure" : "#ADADAD"
    }

    COULEURS_SURVOLE: dict[str, str] = {
        "couleur_fond_surv" : "#636363",
        "couleur_bordure_surv" : "#454545"
    }

    TAG_RETOUR: str = "bouton_menu_sauv_retour"

    bouton_retour: dict[str, list[int] | int] = \
        creer_boutton_arrondi(canvas=canvas, coord=(X_BOUTON, Y_BOUTON), tag=TAG_RETOUR, 
                              texte="Retour", largeur=LARGEUR_BOUTON, hauteur=HAUTEUR_BOUTON, 
                              police=("Cooper Black", 16), epaisseur_bordure=2, couleur_texte="#ffffff", 
                              **COULEUR_BOUTON)
    
    survole_non_survole(canvas=canvas, tag=TAG_RETOUR, fond=bouton_retour["fond"], 
                        bordure=bouton_retour["bordure"], **(COULEUR_BOUTON | COULEURS_SURVOLE))
    
    canvas.tag_bind(TAG_RETOUR, "<Button-1>", lambda event: 
                    retour_menu(canvas=canvas, tags_or_ids=[TAG, TAG_RETOUR]))
    
    creer_fiche_sauv(canvas=canvas, coord=(100, 100), largeur=400, hauteur=100, rayon_coins=15, tag="", 
                     nom_sauv="Test", date="22/04/2026 - 16h 39min 52s", type_grille="Sudoku", 
                     couleur_fond="#555555", couleur_bordure="#666666", style_police_texte="Century", 
                     style_police_boutons="Cooper Black", couleur_texte="#ffffff", 
                     epaisseur_bordure_fiche=5, epaisseur_bordure_boutons=3)