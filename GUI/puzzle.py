import tkinter as tk
from PIL import Image, ImageTk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.animations import mouvement_exterieur_fond_menu, retour_menu
from GUI.widgets import creer_boutton_arrondi, survole_non_survole, creer_bouton_rect, creer_cadre



def aller_puzzle(canvas: tk.Canvas) -> None:

    mouvement_exterieur_fond_menu(canvas=canvas)

    TAG: str = "puzzle"

    COULEUR_FOND: str = "#4373A3"

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
        "couleur_fond" : "#555555",
        "couleur_bordure" : "#666666"
    }

    COULEURS_SURVOLE_BOUTONS_FICHES: dict[str, str] = {
        "couleur_fond_surv" : "#474747",
        "couleur_bordure_surv" : "#393939"
    }

import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.animations import mouvement_exterieur_fond_menu, retour_menu
from GUI.widgets import creer_boutton_arrondi, survole_non_survole



def aller_puzzle(canvas: tk.Canvas) -> None:

    mouvement_exterieur_fond_menu(canvas=canvas)

    TAG: str = "puzzle"

    COULEUR_FOND: str = "#4373A3"

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
        "couleur_fond" : "#555555",
        "couleur_bordure" : "#666666"
    }

    COULEURS_SURVOLE_BOUTONS_FICHES: dict[str, str] = {
        "couleur_fond_surv" : "#474747",
        "couleur_bordure_surv" : "#393939"
    }

    canvas_defilement.create_text(
        (X_FICHES, ECART_VERTICAL_FICHES),
        anchor=tk.NW,
        text="Sudoku classiques:",
        fill=COULEUR_TEXT,
        font=(POLICE, 28),
        tags=TAG
    )

 
    def creer_fiche_puzzle(
        canvas: tk.Canvas,
        coord: tuple[int, int],
        largeur: int,
        hauteur: int,
        tag: str,
        image_file: str,
        couleur_fond: str,
        couleur_bordure: str,
        epaisseur_bordure_fiche: int,
        epaisseur_bordure_boutons: int,
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

        # Ajout de l'image
        image = Image.open(image_file)
        image = image.resize((largeur_fond // 3, hauteur_fond // 1))
        image_tk = ImageTk.PhotoImage(image)
        image_id = canvas.create_image(
            (x_fond + largeur_fond // 6, y_fond + hauteur_fond // 2),
            anchor=tk.CENTER,
            image=image_tk
        )
        if not hasattr(canvas, 'images'):
            canvas.images = []
        canvas.images.append(image_tk)  # Garder une référence à l'image

        fiche: dict[str, list[int] | dict[str, int]] = \
            {"fond": fond, "bordure": bordure}

        y_boutons: int = y_fond + hauteur_fond // 5
        hauteur_boutons: int = 3 * hauteur_fond // 5
        ecart_horizontal: int = largeur_fond // 32
        largeur_boutons: int = 120
        police_boutons: tuple[str, int] = (style_police_boutons, hauteur_boutons // 4)
        x_suppr: int = x_fond + largeur_fond - ecart_horizontal - largeur_boutons
        x_charger: int = x_suppr - ecart_horizontal - largeur_boutons + 100

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
                couleur_texte="#949494",
                epaisseur_bordure=epaisseur_bordure_boutons,
                police=police_boutons
            )

        return {"fiche": fiche, "bouton_charger": bouton_charger}

    LARGEUR_BARRE_DEFILEMENT: int = 17
    LARGEUR_CANVAS_DEFILEMENT: int = 700
    X_FICHES: int = 20
    ECART_VERTICAL_FICHES: int = 30
    LARGEUR_FICHES: int = (LARGEUR_CANVAS_DEFILEMENT - LARGEUR_BARRE_DEFILEMENT - 2 * X_FICHES) // 2 - 15 
    HAUTEUR_FICHES: int = 120
    EPAISSEUR_BORDURE_FICHE: int = 7
    EPAISSEUR_BORDURE_BOUTONS: int = 5


    creer_fiche_puzzle(
    canvas=canvas_defilement,
    coord=(20, 100),
    largeur=LARGEUR_FICHES,
    hauteur=HAUTEUR_FICHES,
    tag="",
    image_file="GUI/Images/Grille_Classique1.png",
    couleur_fond="#4373A3",
    couleur_bordure="#AAA8A8",
    epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
    epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
    style_police_boutons="Cooper Black"
    )

    creer_fiche_puzzle(
    canvas=canvas_defilement,
    coord=(350, 100),
    largeur=LARGEUR_FICHES,
    hauteur=HAUTEUR_FICHES,
    tag="",
    image_file="GUI/Images/Grille_Classique2.png",
    couleur_fond="#4373A3",
    couleur_bordure="#AAA8A8",
    epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
    epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
    style_police_boutons="Cooper Black"
    )

    creer_fiche_puzzle(
    canvas=canvas_defilement,
    coord=(20, 240),
    largeur=LARGEUR_FICHES,
    hauteur=HAUTEUR_FICHES,
    tag="",
    image_file="GUI/Images/Grille_Classique3.png",
    couleur_fond="#4373A3",
    couleur_bordure="#AAA8A8",
    epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
    epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
    style_police_boutons="Cooper Black"
    )

    creer_fiche_puzzle(
    canvas=canvas_defilement,
    coord=(350, 240),
    largeur=LARGEUR_FICHES,
    hauteur=HAUTEUR_FICHES,
    tag="",
    image_file="GUI/Images/Grille_Classique4.png",
    couleur_fond="#4373A3",
    couleur_bordure="#AAA8A8",
    epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
    epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
    style_police_boutons="Cooper Black"
    )
    
    creer_fiche_puzzle(
    canvas=canvas_defilement,
    coord=(20, 380),
    largeur=LARGEUR_FICHES,
    hauteur=HAUTEUR_FICHES,
    tag="",
    image_file="GUI/Images/Grille_Classique5.png",
    couleur_fond="#4373A3",
    couleur_bordure="#AAA8A8",
    epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
    epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
    style_police_boutons="Cooper Black"
    )

    creer_fiche_puzzle(
    canvas=canvas_defilement,
    coord=(350, 380),
    largeur=LARGEUR_FICHES,
    hauteur=HAUTEUR_FICHES,
    tag="",
    image_file="GUI/Images/Grille_Classique6.png",
    couleur_fond="#4373A3",
    couleur_bordure="#AAA8A8",
    epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
    epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
    style_police_boutons="Cooper Black"
    )

    creer_fiche_puzzle(
    canvas=canvas_defilement,
    coord=(20, 520),
    largeur=LARGEUR_FICHES,
    hauteur=HAUTEUR_FICHES,
    tag="",
    image_file="GUI/Images/Grille_Classique7.png",
    couleur_fond="#4373A3",
    couleur_bordure="#AAA8A8",
    epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
    epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
    style_police_boutons="Cooper Black"
    )

    creer_fiche_puzzle(
    canvas=canvas_defilement,
    coord=(350, 520),
    largeur=LARGEUR_FICHES,
    hauteur=HAUTEUR_FICHES,
    tag="",
    image_file="GUI/Images/Grille_Classique8.png",
    couleur_fond="#4373A3",
    couleur_bordure="#AAA8A8",
    epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
    epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
    style_police_boutons="Cooper Black"
    )

    creer_fiche_puzzle(
    canvas=canvas_defilement,
    coord=(20, 660),
    largeur=LARGEUR_FICHES,
    hauteur=HAUTEUR_FICHES,
    tag="",
    image_file="GUI/Images/Grille_Classique9.png",
    couleur_fond="#4373A3",
    couleur_bordure="#AAA8A8",
    epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
    epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
    style_police_boutons="Cooper Black"
    )

    creer_fiche_puzzle(
    canvas=canvas_defilement,
    coord=(350, 660),
    largeur=LARGEUR_FICHES,
    hauteur=HAUTEUR_FICHES,
    tag="",
    image_file="GUI/Images/Grille_Classique10.png",
    couleur_fond="#4373A3",
    couleur_bordure="#AAA8A8",
    epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
    epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
    style_police_boutons="Cooper Black"
    )

    canvas_defilement.create_text(
        (X_FICHES, 820),
        anchor=tk.NW,
        text="Grilles de Windoku:",
        fill=COULEUR_TEXT,
        font=(POLICE, 28),
        tags=TAG
    )

    creer_fiche_puzzle(
    canvas=canvas_defilement,
    coord=(20, 885),
    largeur=LARGEUR_FICHES,
    hauteur=HAUTEUR_FICHES,
    tag="",
    image_file="GUI/Images/Windoku1.png",
    couleur_fond="#4373A3",
    couleur_bordure="#AAA8A8",
    epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
    epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
    style_police_boutons="Cooper Black"
    )
    
    creer_fiche_puzzle(
    canvas=canvas_defilement,
    coord=(350, 885),
    largeur=LARGEUR_FICHES,
    hauteur=HAUTEUR_FICHES,
    tag="",
    image_file="GUI/Images/Windoku2.png",
    couleur_fond="#4373A3",
    couleur_bordure="#AAA8A8",
    epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
    epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
    style_police_boutons="Cooper Black"
    )

    creer_fiche_puzzle(
    canvas=canvas_defilement,
    coord=(20, 1025),
    largeur=LARGEUR_FICHES,
    hauteur=HAUTEUR_FICHES,
    tag="",
    image_file="GUI/Images/Windoku3.png",
    couleur_fond="#4373A3",
    couleur_bordure="#AAA8A8",
    epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
    epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
    style_police_boutons="Cooper Black"
    )

    creer_fiche_puzzle(
    canvas=canvas_defilement,
    coord=(350, 1025),
    largeur=LARGEUR_FICHES,
    hauteur=HAUTEUR_FICHES,
    tag="",
    image_file="GUI/Images/Windoku4.png",
    couleur_fond="#4373A3",
    couleur_bordure="#AAA8A8",
    epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE,
    epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS,
    style_police_boutons="Cooper Black"
    )

    


    region_objets: tuple[int, int, int, int] = canvas_defilement.bbox("all")
    canvas_defilement.config(scrollregion=(0, 0, region_objets[2], region_objets[3] + 20))