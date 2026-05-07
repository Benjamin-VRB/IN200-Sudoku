import tkinter as tk
from PIL import Image, ImageTk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.animations import mouvement_exterieur_fond_menu, retour_menu
from GUI.widgets import creer_boutton_arrondi, survole_non_survole, creer_fiche_puzzle

def aller_puzzle(canvas: tk.Canvas) -> None:

    mouvement_exterieur_fond_menu(canvas=canvas)

    TAG: str = "puzzle"

    COULEUR_FOND: str = "#2D4C6B"

    canvas.create_rectangle(
        ((0, 0), (LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE)), 
        fill=COULEUR_FOND, 
        outline=COULEUR_FOND, 
        tags=TAG
    )
    
    COULEUR_TEXT: str = "#ffffff"
    POLICE: str = "Bell MT"

    canvas.create_text(
        (LARGEUR_PIXEL_FENETRE - 165, 200), 
        anchor=tk.E, text="Puzzles", 
        fill=COULEUR_TEXT, 
        font=(POLICE, 60), 
        tags=TAG
    )
    
    COULEUR_CANVAS_DEFILEMENT: str = "#4373A3"
    X_CANVAS_DEFILEMENT: int = 0
    Y_CANVAS_DEFILEMENT: int = 0
    LARGEUR_CANVAS_DEFILEMENT: int = 700
    HAUTEUR_CANVAS_DEFILEMENT: int = HAUTEUR_PIXEL_FENETRE

    canvas_defilement: tk.Canvas = tk.Canvas(
        master=canvas, 
        bg=COULEUR_CANVAS_DEFILEMENT, 
        width=LARGEUR_CANVAS_DEFILEMENT,
        height=HAUTEUR_CANVAS_DEFILEMENT
    )
    
    canvas_defilement.place(
        x=X_CANVAS_DEFILEMENT,
        y=Y_CANVAS_DEFILEMENT,
        anchor=tk.NW
    )
    
    barre_defilement: tk.Scrollbar = tk.Scrollbar(
        master=canvas, 
        bg=COULEUR_CANVAS_DEFILEMENT,
        command=canvas_defilement.yview
    )
    
    canvas_defilement.config(yscrollcommand=barre_defilement.set)

    LARGEUR_BARRE_DEFILEMENT: int = 17
    X_BARRE_DEFILEMENT: int = X_CANVAS_DEFILEMENT + LARGEUR_CANVAS_DEFILEMENT - LARGEUR_BARRE_DEFILEMENT
    Y_BARRE_DEFILEMENT: int = Y_CANVAS_DEFILEMENT

    canvas.create_window(
        (X_BARRE_DEFILEMENT, Y_BARRE_DEFILEMENT), 
        anchor=tk.NW, 
        window=barre_defilement, 
        width=LARGEUR_BARRE_DEFILEMENT, 
        height=HAUTEUR_CANVAS_DEFILEMENT, 
        tags=TAG
    )
    
    LARGEUR_BOUTON: int = 300
    HAUTEUR_BOUTON: int = 124
    X_BOUTON: int = LARGEUR_PIXEL_FENETRE - LARGEUR_BOUTON - 130
    Y_BOUTON: int = HAUTEUR_PIXEL_FENETRE - HAUTEUR_BOUTON - 80

    COULEUR_BOUTON_RETOUR: dict[str, str] = {
        "couleur_fond" : "#939393",
        "couleur_bordure" : "#ADADAD"
    }

    COULEURS_SURVOLE_RETOUR: dict[str, str] = {
        "couleur_fond_surv" : "#636363",
        "couleur_bordure_surv" : "#454545"
    }

    TAG_RETOUR: str = "bouton_menu_sauv_retour"

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
            **COULEUR_BOUTON_RETOUR
        )
    
    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_RETOUR], 
        fond=bouton_retour["fond"], 
        bordure=bouton_retour["bordure"], 
        **(COULEUR_BOUTON_RETOUR | COULEURS_SURVOLE_RETOUR)
    )
    
    canvas.tag_bind(
        tagOrId=TAG_RETOUR, 
        sequence="<Button-1>", 
        func=lambda event: retour_menu(
            canvas=canvas,
            tags_ou_ids=[TAG, TAG_RETOUR], 
            widgets=[canvas_defilement]
        )
    )

    X_FICHES: int = 20
    ECART_VERTICAL_FICHES: int = 30
    LARGEUR_FICHES: int = LARGEUR_CANVAS_DEFILEMENT - LARGEUR_BARRE_DEFILEMENT - 2 * X_FICHES
    HAUTEUR_FICHES: int = 125
    EPAISSEUR_BORDURE_FICHE: int = 7
    EPAISSEUR_BORDURE_BOUTONS: int = 5

    COULEUR_BOUTONS_FICHES: dict[str, str] = {
        "couleur_fond" : "#4373A3",
        "couleur_bordure" : "#AAA8A8"
    }

    COULEURS_SURVOLE_BOUTONS_FICHES: dict[str, str] = {
        "couleur_fond_surv" : "#35597E",
        "couleur_bordure_surv" : "#AAA8A8"
    }

    canvas_defilement.create_text(
        (X_FICHES, ECART_VERTICAL_FICHES),
        anchor=tk.NW,
        text="Sudoku classiques:",
        fill=COULEUR_TEXT,
        font=(POLICE, 28),
        tags=TAG
    )


    LARGEUR_BARRE_DEFILEMENT: int = 17
    LARGEUR_CANVAS_DEFILEMENT: int = 700
    X_FICHES: int = 20
    ECART_VERTICAL_FICHES: int = 30
    LARGEUR_FICHES: int = (LARGEUR_CANVAS_DEFILEMENT - LARGEUR_BARRE_DEFILEMENT - 2 * X_FICHES) // 2 - 15 
    HAUTEUR_FICHES: int = 120
    EPAISSEUR_BORDURE_FICHE: int = 7
    EPAISSEUR_BORDURE_BOUTONS: int = 5

    images = [
        "GUI/Images/Grille_Classique1.png",
        "GUI/Images/Grille_Classique2.png",
        "GUI/Images/Grille_Classique3.png",
        "GUI/Images/Grille_Classique4.png",
        "GUI/Images/Grille_Classique5.png",
        "GUI/Images/Grille_Classique6.png",
        "GUI/Images/Grille_Classique7.png",
        "GUI/Images/Grille_Classique8.png",
        "GUI/Images/Grille_Classique9.png",
        "GUI/Images/Grille_Classique10.png",
    ]
    
    x_coords = [20, 350]
    y_coords = [100, 240, 380, 520, 660]
    
    fiches = []
    for i, image in enumerate(images):
        x = x_coords[i % 2]
        y = y_coords[i // 2]
        fiche = creer_fiche_puzzle(
            canvas=canvas_defilement,
            coord=(x, y),
            largeur=LARGEUR_FICHES,
            hauteur=HAUTEUR_FICHES,
            tag="",
            image_file=image,
            couleur_fond="#4373A3",
            couleur_bordure="#AAA8A8",
            epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
            epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
            style_police_boutons="Cooper Black"
        )
        fiches.append(fiche)
    
    for fiche in fiches:
        bouton_charger_fond: int = fiche["bouton_charger"]["fond"]
        bouton_charger_bordure: list[int] = fiche["bouton_charger"]["bordure"]
        bouton_charger_texte: int = fiche["bouton_charger"]["texte"]
        bouton_charger: list[int] = [bouton_charger_fond, *bouton_charger_bordure, bouton_charger_texte]
        survole_non_survole(
            canvas=canvas_defilement,
            tags_ou_ids=bouton_charger,
            fond=[bouton_charger_fond],
            bordure=bouton_charger_bordure,
            **(COULEUR_BOUTONS_FICHES | COULEURS_SURVOLE_BOUTONS_FICHES)
        )
    


    canvas_defilement.create_text(
        (X_FICHES, 820),
        anchor=tk.NW,
        text="Grilles de Windoku:",
        fill=COULEUR_TEXT,
        font=(POLICE, 28),
        tags=TAG
    )
    images2 = [
        "GUI/Images/Windoku1.png",
        "GUI/Images/Windoku2.png",
        "GUI/Images/Windoku3.png",
        "GUI/Images/Windoku4.png",
    ]

    x_coords = [20, 350]
    y_coords = [885, 1025]

    fiches = []
    for i, image in enumerate(images2):
        x = x_coords[i % 2]
        y = y_coords[i // 2]
        fiche = creer_fiche_puzzle(
            canvas=canvas_defilement,
            coord=(x, y),
            largeur=LARGEUR_FICHES,
            hauteur=HAUTEUR_FICHES,
            tag="",
            image_file=image,
            couleur_fond="#4373A3",
            couleur_bordure="#AAA8A8",
            epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
            epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
            style_police_boutons="Cooper Black"
        )
        fiches.append(fiche)

    for fiche in fiches:
        bouton_charger_fond: int = fiche["bouton_charger"]["fond"]
        bouton_charger_bordure: list[int] = fiche["bouton_charger"]["bordure"]
        bouton_charger_texte: int = fiche["bouton_charger"]["texte"]
        bouton_charger: list[int] = [bouton_charger_fond, *bouton_charger_bordure, bouton_charger_texte]
        survole_non_survole(
            canvas=canvas_defilement,
            tags_ou_ids=bouton_charger,
            fond=[bouton_charger_fond],
            bordure=bouton_charger_bordure,
            **(COULEUR_BOUTONS_FICHES | COULEURS_SURVOLE_BOUTONS_FICHES)
    )
    


    region_objets: tuple[int, int, int, int] = canvas_defilement.bbox("all")
    canvas_defilement.config(scrollregion=(0, 0, region_objets[2], region_objets[3] + 20))