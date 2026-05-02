import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.animations import mouvement_exterieur_fond_menu, retour_menu, supprimer_sauv_menu_sauvegardes
from GUI.widgets import creer_boutton_arrondi, survole_non_survole, creer_fiche_sauv

from Grille.sauvegarde import charger_sauvegardes


def aller_menu_sauvegardes(canvas: tk.Canvas) -> None:

    mouvement_exterieur_fond_menu(canvas=canvas)

    TAG: str = "menu_sauvegardes"

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
        (LARGEUR_PIXEL_FENETRE - 70, 200), 
        anchor=tk.E, text="Sauvegardes", 
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

    sauvegardes: list = charger_sauvegardes()

    if len(sauvegardes) <= 0:
        canvas_defilement.create_text(
            (X_CANVAS_DEFILEMENT + LARGEUR_CANVAS_DEFILEMENT // 2, 
             Y_CANVAS_DEFILEMENT + HAUTEUR_CANVAS_DEFILEMENT // 2), 
            fill="#ffffff", 
            anchor=tk.CENTER, 
            font=("Century", 25), 
            text="Aucune sauvegarde", 
            tags=TAG
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
    
    for i, sauv in enumerate(iterable=sauvegardes):

        fiche: dict[str, dict[str, list[int] | dict[str, int]] | dict[str, list[int] | int]] = \
            creer_fiche_sauv(
                canvas=canvas_defilement, 
                coord=(X_FICHES, ECART_VERTICAL_FICHES + i * (HAUTEUR_FICHES + ECART_VERTICAL_FICHES)), 
                largeur=LARGEUR_FICHES, 
                hauteur=HAUTEUR_FICHES,  
                tag="", 
                nom_sauv=sauv["nom"], 
                date=sauv["date"], 
                type_grille=sauv["type"], 
                temps="5min 32s", 
                difficulte="Facile", 
                statut="en_cours", 
                style_police_texte="Century", 
                style_police_boutons="Cooper Black", 
                couleur_texte="#ffffff", 
                epaisseur_bordure_fiche=EPAISSEUR_BORDURE_FICHE, 
                epaisseur_bordure_boutons=EPAISSEUR_BORDURE_BOUTONS, 
                **COULEUR_BOUTONS_FICHES
            )

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

        bouton_suppr_fond: int = fiche["bouton_suppr"]["fond"]
        bouton_suppr_bordure: list[int] = fiche["bouton_suppr"]["bordure"]
        bouton_suppr_texte: int = fiche["bouton_suppr"]["texte"]
        bouton_suppr: list[int] = [bouton_suppr_fond, *bouton_suppr_bordure, bouton_suppr_texte]

        survole_non_survole(
            canvas=canvas_defilement, 
            tags_ou_ids=bouton_suppr, 
            fond=[bouton_suppr_fond], 
            bordure=bouton_suppr_bordure, 
            **(COULEUR_BOUTONS_FICHES | COULEURS_SURVOLE_BOUTONS_FICHES)
        )

        for id in bouton_charger:
            canvas_defilement.tag_bind(
                tagOrId=id, 
                sequence="<Button-1>"
            )

        for id in bouton_suppr:
            canvas_defilement.tag_bind(
                tagOrId=id, 
                sequence="<Button-1>", 
                func=lambda event, indice=i: supprimer_sauv_menu_sauvegardes(
                    canvas=canvas, 
                    fonction_page=aller_menu_sauvegardes, 
                    indices=[indice], 
                    tags_ou_ids=[TAG, TAG_RETOUR], 
                    widgets=[canvas_defilement]
                )
            )

    region_objets: tuple[int, int, int, int] = canvas_defilement.bbox("all")
    canvas_defilement.config(scrollregion=(0, 0, region_objets[2], region_objets[3] + 20))