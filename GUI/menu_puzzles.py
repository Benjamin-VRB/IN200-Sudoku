import tkinter as tk
import json

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.animations import mouvement_exterieur_fond_menu, retour_menu
from GUI.widgets import creer_boutton_arrondi, survole_non_survole, creer_fiche_puzzle
from GUI.interface_jeu_puzzle import aller_grille_puzzle

def aller_puzzle(canvas: tk.Canvas) -> None:

    mouvement_exterieur_fond_menu(canvas=canvas)

    TAG: str = "puzzle"

    COULEUR_FOND: str = "#373737"

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
    
    COULEUR_CANVAS_DEFILEMENT: str = "#4E4E4E"
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

    COULEURS_BOUTON_RETOUR: dict[str, str] = {
        "couleur_fond" : "#939393",
        "couleur_bordure" : "#ADADAD", 
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
            couleur_fond=COULEURS_BOUTON_RETOUR["couleur_fond"], 
            couleur_bordure=COULEURS_BOUTON_RETOUR["couleur_bordure"]
        )
    
    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_RETOUR], 
        fond=bouton_retour["fond"], 
        bordure=bouton_retour["bordure"], 
        couleurs=COULEURS_BOUTON_RETOUR
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

    X_COORDS: list[int] = [20, 350]
    ECART_VERTICAL_FICHES: int = 30
    LARGEUR_FICHES: int = LARGEUR_CANVAS_DEFILEMENT - LARGEUR_BARRE_DEFILEMENT - 2 * X_COORDS[0]
    HAUTEUR_FICHES: int = 125
    EPAISSEUR_BORDURE_FICHE: int = 7
    EPAISSEUR_BORDURE_BOUTONS: int = 5

    COULEURS_FICHES: dict[str, str] = {
        "couleur_fond" : "#555555",
        "couleur_bordure" : "#666666", 
        "couleur_fond_surv" : "#474747",
        "couleur_bordure_surv" : "#393939"
    }

    canvas_defilement.create_text(
        (X_COORDS[0], ECART_VERTICAL_FICHES),
        anchor=tk.NW,
        text="Sudoku:",
        fill=COULEUR_TEXT,
        font=(POLICE, 28),
        tags=TAG
    )

    ECART_VERTICAL_FICHES: int = 30
    LARGEUR_FICHES: int = (LARGEUR_CANVAS_DEFILEMENT - LARGEUR_BARRE_DEFILEMENT - 2 * X_COORDS[0]) // 2 - 15 
    HAUTEUR_FICHES: int = 120
    EPAISSEUR_BORDURE_FICHE: int = 7
    EPAISSEUR_BORDURE_BOUTONS: int = 5

    IMAGES: list[str] = [
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
    
    Y_COORDS_SUDOKU: list[int] = [100, 240, 380, 520, 660]
    
    fiches_sudoku: list[dict[str, dict[str, list[int] | dict[str, int]] | dict[str, list[int] | int]]] = []
    for i, image in enumerate(IMAGES):
        x: int  = X_COORDS[i % 2]
        y: int  = Y_COORDS_SUDOKU[i // 2]
        fiche: dict[str, dict[str, list[int] | dict[str, int]] | dict[str, list[int] | int]] = \
            creer_fiche_puzzle(
                canvas=canvas_defilement,
                coord=(x, y),
                largeur=LARGEUR_FICHES,
                hauteur=HAUTEUR_FICHES,
                tag=TAG,
                image=image,
                couleur_fond=COULEURS_FICHES["couleur_fond"],
                couleur_bordure=COULEURS_FICHES["couleur_bordure"], 
                couleur_texte="#FFFFFF", 
                epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
                epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
                style_police_boutons="Cooper Black"
            )
        fiches_sudoku.append(fiche)
    
    def recuperer_grille_json(type_grille, nom_grille):
        with open('Puzzles/Groupe_de_puzzles.json', 'r') as f:
            grilles = json.load(f)
        grille_originale = grilles[type_grille][nom_grille]
        progression = grilles[type_grille].get(nom_grille + "_progression")
        return grille_originale, progression  



    for i, fiche in enumerate(fiches_sudoku):
        bouton_charger_fond: int = fiche["bouton_charger"]["fond"]
        bouton_charger_bordure: list[int] = fiche["bouton_charger"]["bordure"]
        bouton_charger_texte: int = fiche["bouton_charger"]["texte"]
        bouton_charger: list[int] = [bouton_charger_fond, *bouton_charger_bordure, bouton_charger_texte]
        survole_non_survole(
            canvas=canvas_defilement,
            tags_ou_ids=bouton_charger,
            fond=[bouton_charger_fond],
            bordure=bouton_charger_bordure,
            couleurs=COULEURS_FICHES
        )
        canvas_defilement.tag_bind(
            tagOrId=bouton_charger_texte,
            sequence="<Button-1>",
            func=lambda event, i=i: (
                lambda orig, prog: aller_grille_puzzle(
                    canvas=canvas,
                    type_grille="sudoku",
                    difficulte=None,
                    temps_depart=0,
                    nom_puzzle="Puzzle_Classique" + str(i+1),
                    tags_ou_ids_page_suppr=[TAG, TAG_RETOUR],
                    widgets_page_suppr=[canvas_defilement],
                    grille_par_defaut=orig,         
                    grille_progression=prog,        
                    indices_cases_verr=None
                )
            )(*recuperer_grille_json("Classique", "Puzzle_Classique"+str(i+1)))
        )
        canvas_defilement.tag_bind(
            tagOrId=bouton_charger_fond,
            sequence="<Button-1>",
            func=lambda event, i=i: (
                lambda orig, prog: aller_grille_puzzle(
                    canvas=canvas,
                    type_grille="sudoku",
                    difficulte=None,
                    temps_depart=0,
                    nom_puzzle="Puzzle_Classique" + str(i+1),
                    tags_ou_ids_page_suppr=[TAG, TAG_RETOUR],
                    widgets_page_suppr=[canvas_defilement],
                    grille_par_defaut=orig,         
                    grille_progression=prog,        
                    indices_cases_verr=None
                )
            )(*recuperer_grille_json("Classique", "Puzzle_Classique"+str(i+1)))
        )
        canvas_defilement.tag_bind(
            tagOrId=bouton_charger_bordure,
            sequence="<Button-1>",
            func=lambda event, i=i: (
                lambda orig, prog: aller_grille_puzzle(
                    canvas=canvas,
                    type_grille="sudoku",
                    difficulte=None,
                    temps_depart=0,
                    nom_puzzle="Puzzle_Classique" + str(i+1),
                    tags_ou_ids_page_suppr=[TAG, TAG_RETOUR],
                    widgets_page_suppr=[canvas_defilement],
                    grille_par_defaut=orig,         
                    grille_progression=prog,        
                    indices_cases_verr=None
                )
            )(*recuperer_grille_json("Classique", "Puzzle_Classique"+str(i+1)))
        )

    canvas_defilement.create_text(
        (X_COORDS[0], 820),
        anchor=tk.NW,
        text="Windoku:",
        fill=COULEUR_TEXT,
        font=(POLICE, 28),
        tags=TAG
    )

    IMAGES2: list[str] = [
        "GUI/Images/Windoku1.png",
        "GUI/Images/Windoku2.png",
        "GUI/Images/Windoku3.png",
        "GUI/Images/Windoku4.png",
    ]

    Y_COORDS_WINDOKU: list[int] = [885, 1025]

    fiches_windoku: list[dict[str, dict[str, list[int] | dict[str, int]] | dict[str, list[int] | int]]] = []
    for i, image in enumerate(IMAGES2):
        x: int = X_COORDS[i % 2]
        y: int = Y_COORDS_WINDOKU[i // 2]
        fiche: dict[str, dict[str, list[int] | dict[str, int]] | dict[str, list[int] | int]] = \
            creer_fiche_puzzle(
                canvas=canvas_defilement,
                coord=(x, y),
                largeur=LARGEUR_FICHES,
                hauteur=HAUTEUR_FICHES,
                tag=TAG,
                image=image,
                couleur_fond=COULEURS_FICHES["couleur_fond"],
                couleur_bordure=COULEURS_FICHES["couleur_bordure"],
                couleur_texte="#ffffff", 
                epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
                epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
                style_police_boutons="Cooper Black"
            )
        fiches_windoku.append(fiche)

    for fiche in fiches_windoku:
        bouton_charger_fond: int = fiche["bouton_charger"]["fond"]
        bouton_charger_bordure: list[int] = fiche["bouton_charger"]["bordure"]
        bouton_charger_texte: int = fiche["bouton_charger"]["texte"]
        bouton_charger: list[int] = [bouton_charger_fond, *bouton_charger_bordure, bouton_charger_texte]
        survole_non_survole(
            canvas=canvas_defilement,
            tags_ou_ids=bouton_charger,
            fond=[bouton_charger_fond],
            bordure=bouton_charger_bordure,
            couleurs=COULEURS_FICHES
        )
        

    region_objets: tuple[int, int, int, int] = canvas_defilement.bbox("all")
    canvas_defilement.config(scrollregion=(0, 0, region_objets[2], region_objets[3] + 20))