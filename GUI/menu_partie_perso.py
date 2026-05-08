import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.widgets import creer_boutton_arrondi, survole_non_survole, creer_bouton_rect, bouton_active, \
renvoyer_mode_et_dif
from GUI.animations import retour_menu, mouvement_exterieur_fond_menu
from GUI.decorations import creer_cadre
from GUI.interface_jeu import aller_grille


def jouer_debut(
        canvas: tk.Canvas, 
        boutons_mode: list[dict[str, int | list[int]]],
        boutons_dif: list[dict[str, int | list[int]]],
        couleurs_bouton_act: dict[str, str], 
        tags_ou_ids_page_suppr: list[int | str] = None, 
        widgets_page_suppr: list[tk.Widget] = None
    ) -> None:

    info_partie: dict[str, str | int] = renvoyer_mode_et_dif(
        canvas=canvas, 
        boutons_dif=boutons_dif, 
        boutons_mode=boutons_mode,
        couleurs_bouton_act=couleurs_bouton_act
    )

    if (info_partie["mode"] in ["sudoku", "16x16", "windoku", "consecutif"] and \
    info_partie["difficulte"] is None) or info_partie["mode"] is None:
        return

    aller_grille(
        canvas=canvas, 
        type_grille=info_partie["mode"], 
        difficulte=info_partie["difficulte"], 
        temps_depart=0, 
        tags_ou_ids_page_suppr=tags_ou_ids_page_suppr, 
        widgets_page_suppr=widgets_page_suppr
    )


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
        "fill" : "#ffffff",  
        "tags" : TAG
    }

    canvas.create_text(
        (LARGEUR_PIXEL_FENETRE // 2, 50), 
        text="Partie personnalisée", 
        anchor=tk.CENTER, 
        font=(POLICE, 50), 
        **PARAMS_TEXT
    )

    X_CADRE: int = 400
    Y_CADRE: int = 130
    LARGEUR_CADRE: int = LARGEUR_PIXEL_FENETRE - X_CADRE - 50
    HAUTEUR_CADRE: int = HAUTEUR_PIXEL_FENETRE - Y_CADRE - 50
    RAYON_COINS_CADRE: int = 30
    COULEUR_CADRE = "#444444"

    creer_cadre(
        canvas=canvas, 
        coord=(X_CADRE, Y_CADRE), 
        largeur=LARGEUR_CADRE, 
        hauteur=HAUTEUR_CADRE, 
        rayon_coins=RAYON_COINS_CADRE, 
        couleur=COULEUR_CADRE, 
        tag=TAG
    )

    COULEURS_BOUTONS_MODE_DIF_DESACT: dict[str, str] = {
        "couleur_fond" : "#555555",
        "couleur_bordure" : "#666666", 
        "couleur_fond_surv" : "#474747",
        "couleur_bordure_surv" : "#393939"
    }

    COULEURS_BOUTONS_MODE_DIF_ACT: dict[str, str] = {
        "couleur_fond" : "#2a86bc", 
        "couleur_bordure" : "#3b9fd9", 
        "couleur_fond_surv" : "#2177a8", 
        "couleur_bordure_surv" : "#1d6995"
    }

    couleurs_bouton_sudoku: dict[str, str] = COULEURS_BOUTONS_MODE_DIF_DESACT.copy()
    couleurs_bouton_kenken: dict[str, str] = COULEURS_BOUTONS_MODE_DIF_DESACT.copy()
    couleurs_bouton_kakuro: dict[str, str] = COULEURS_BOUTONS_MODE_DIF_DESACT.copy()
    couleurs_bouton_chaos: dict[str, str] = COULEURS_BOUTONS_MODE_DIF_DESACT.copy()
    couleurs_bouton_consecutif: dict[str, str] = COULEURS_BOUTONS_MODE_DIF_DESACT.copy()
    couleurs_bouton_16x16: dict[str, str] = COULEURS_BOUTONS_MODE_DIF_DESACT.copy()
    couleurs_bouton_windoku: dict[str, str] = COULEURS_BOUTONS_MODE_DIF_DESACT.copy()

    list_couleurs_boutons_mode: list[dict[str, str]] = [
        couleurs_bouton_sudoku, 
        couleurs_bouton_kenken, 
        couleurs_bouton_kakuro, 
        couleurs_bouton_chaos, 
        couleurs_bouton_consecutif, 
        couleurs_bouton_16x16, 
        couleurs_bouton_windoku
    ]
    
    PARAMS_BOUTONS_MODES: dict[str, str | int] = {
        "largeur" : 230, 
        "hauteur" : 74, 
        "police" : ("Cooper Black", 14), 
        "couleur_texte" : "#ffffff", 
        "epaisseur_bordure" : 10
    }

    X_COLONNE1_MODES: int = X_CADRE + RAYON_COINS_CADRE
    Y_RANGEE1_MODES: int = Y_CADRE + RAYON_COINS_CADRE + 100
    ECART_VERTICAL_MODES: int = 25
    ECART_HORIZONTAL_MODES: int = 20
    X_COLONNE2_MODES: int = X_COLONNE1_MODES + PARAMS_BOUTONS_MODES["largeur"] + ECART_HORIZONTAL_MODES
    Y_RANGEE2_MODES: int = Y_RANGEE1_MODES + PARAMS_BOUTONS_MODES["hauteur"] + ECART_VERTICAL_MODES
    Y_RANGEE3_MODES: int = Y_RANGEE2_MODES + PARAMS_BOUTONS_MODES["hauteur"] + ECART_VERTICAL_MODES
    Y_RANGEE4_MODES: int = Y_RANGEE3_MODES + PARAMS_BOUTONS_MODES["hauteur"] + ECART_VERTICAL_MODES

    canvas.create_text(
        (X_COLONNE1_MODES + PARAMS_BOUTONS_MODES["largeur"] + ECART_HORIZONTAL_MODES // 2, 
         Y_CADRE + RAYON_COINS_CADRE + 25), 
        anchor=tk.CENTER, 
        text="Modes de jeu", 
        font=(POLICE, 30), 
        **PARAMS_TEXT
    )

    TAG_SUDOKU: str = "bouton_sudoku"
    bouton_sudoku: dict[str, list[int] | int] = \
        creer_bouton_rect(
            canvas=canvas, 
            coord=(X_COLONNE1_MODES, Y_RANGEE1_MODES), 
            tag=TAG_SUDOKU, 
            texte="Sudoku", 
            couleur_fond=couleurs_bouton_sudoku["couleur_fond"], 
            couleur_bordure=couleurs_bouton_sudoku["couleur_bordure"], 
            **PARAMS_BOUTONS_MODES
        )
    
    TAG_KENKEN: str = "bouton_kenken"
    bouton_kenken: dict[str, list[int] | int] = \
        creer_bouton_rect(
            canvas=canvas, 
            coord=(X_COLONNE2_MODES, Y_RANGEE1_MODES), 
            tag=TAG_KENKEN, 
            texte="Kenken", 
            couleur_fond=couleurs_bouton_kenken["couleur_fond"], 
            couleur_bordure=couleurs_bouton_kenken["couleur_bordure"], 
            **PARAMS_BOUTONS_MODES
        )
    
    TAG_WINDOKU: str = "bouton_windoku"
    bouton_windoku: dict[str, list[int] | int] = \
        creer_bouton_rect(
            canvas=canvas, 
            coord=(X_COLONNE1_MODES, Y_RANGEE2_MODES), 
            tag=TAG_WINDOKU, 
            texte="Windoku", 
            couleur_fond=couleurs_bouton_windoku["couleur_fond"], 
            couleur_bordure=couleurs_bouton_windoku["couleur_bordure"], 
            **PARAMS_BOUTONS_MODES
        )
    
    
    TAG_CONSECUTIF: str = "bouton_consecutif"
    bouton_consecutif: dict[str, list[int] | int] = \
        creer_bouton_rect(
            canvas=canvas, 
            coord=(X_COLONNE1_MODES, Y_RANGEE3_MODES), 
            tag=TAG_CONSECUTIF, 
            texte="Sudoku consécutif", 
            couleur_fond=couleurs_bouton_consecutif["couleur_fond"], 
            couleur_bordure=couleurs_bouton_consecutif["couleur_bordure"], 
            **PARAMS_BOUTONS_MODES
        )
    
    TAG_CHAOS: str = "bouton_chaos"
    bouton_chaos: dict[str, list[int] | int] = \
        creer_bouton_rect(
            canvas=canvas, 
            coord=(X_COLONNE2_MODES, Y_RANGEE3_MODES), 
            tag=TAG_CHAOS, 
            texte="Sudoku chaos", 
            couleur_fond=couleurs_bouton_chaos["couleur_fond"], 
            couleur_bordure=couleurs_bouton_chaos["couleur_bordure"], 
            **PARAMS_BOUTONS_MODES
        )
    
    TAG_KAKURO: str = "bouton_kakuro"
    bouton_kakuro: dict[str, list[int] | int] = \
        creer_bouton_rect(
            canvas=canvas, 
            coord=(X_COLONNE2_MODES, Y_RANGEE2_MODES), 
            tag=TAG_KAKURO, 
            texte="Kakuro", 
            couleur_fond=couleurs_bouton_kakuro["couleur_fond"], 
            couleur_bordure=couleurs_bouton_kakuro["couleur_bordure"], 
            **PARAMS_BOUTONS_MODES
        )
    
    TAG_16X16: str = "bouton_16x16"
    bouton_16x16: dict[str, list[int] | int] = \
        creer_bouton_rect(
            canvas=canvas, 
            coord=((X_COLONNE1_MODES + X_COLONNE2_MODES) // 2, Y_RANGEE4_MODES), 
            tag=TAG_16X16, 
            texte="Sudoku 16x16", 
            couleur_fond=couleurs_bouton_16x16["couleur_fond"], 
            couleur_bordure=couleurs_bouton_16x16["couleur_bordure"], 
            **PARAMS_BOUTONS_MODES
        )

    list_boutons_mode: list[dict[str, list[int] | int]] = [
        bouton_sudoku, 
        bouton_16x16, 
        bouton_chaos, 
        bouton_consecutif, 
        bouton_kakuro, 
        bouton_kenken, 
        bouton_windoku
    ]
    
    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_SUDOKU], 
        fond=[bouton_sudoku["fond"]], 
        bordure=bouton_sudoku["bordure"], 
        couleurs=couleurs_bouton_sudoku
    )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_KENKEN], 
        fond=[bouton_kenken["fond"]], 
        bordure=bouton_kenken["bordure"], 
        couleurs=couleurs_bouton_kenken
    )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_KAKURO], 
        fond=[bouton_kakuro["fond"]], 
        bordure=bouton_kakuro["bordure"], 
        couleurs=couleurs_bouton_kakuro
    )
    
    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_16X16], 
        fond=[bouton_16x16["fond"]], 
        bordure=bouton_16x16["bordure"], 
        couleurs=couleurs_bouton_16x16
    )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_CHAOS], 
        fond=[bouton_chaos["fond"]], 
        bordure=bouton_chaos["bordure"], 
        couleurs=couleurs_bouton_chaos
    )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_WINDOKU], 
        fond=[bouton_windoku["fond"]], 
        bordure=bouton_windoku["bordure"], 
        couleurs=couleurs_bouton_windoku
    )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_CONSECUTIF], 
        fond=[bouton_consecutif["fond"]], 
        bordure=bouton_consecutif["bordure"], 
        couleurs=couleurs_bouton_consecutif
    )

    PARAMS_BOUTONS_DIF: dict[str, str | int] = {
        "largeur" : 230, 
        "hauteur" : 74, 
        "police" : ("Cooper Black", 14), 
        "couleur_texte" : "#ffffff", 
        "epaisseur_bordure" : 10
    }

    X_BOUTONS_DIF: int = X_CADRE + LARGEUR_CADRE - RAYON_COINS_CADRE - PARAMS_BOUTONS_DIF["largeur"]
    Y_RANGEE1_DIF: int = Y_CADRE + RAYON_COINS_CADRE + 100
    ECART_VERTICAL_DIF: int = 25
    Y_RANGEE2_DIF: int = Y_RANGEE1_DIF + PARAMS_BOUTONS_DIF["hauteur"] + ECART_VERTICAL_DIF
    Y_RANGEE3_DIF: int = Y_RANGEE2_DIF + PARAMS_BOUTONS_DIF["hauteur"] + ECART_VERTICAL_DIF
    Y_RANGEE4_DIF: int = Y_RANGEE3_DIF + PARAMS_BOUTONS_DIF["hauteur"] + ECART_VERTICAL_DIF

    couleurs_bouton_tres_difficile: dict[str, str] = COULEURS_BOUTONS_MODE_DIF_DESACT.copy()
    couleurs_bouton_difficile: dict[str, str] = COULEURS_BOUTONS_MODE_DIF_DESACT.copy()
    couleurs_bouton_moyen: dict[str, str] = COULEURS_BOUTONS_MODE_DIF_DESACT.copy()
    couleurs_bouton_facile: dict[str, str] = COULEURS_BOUTONS_MODE_DIF_DESACT.copy()

    list_couleurs_boutons_dif: list[dict[str, str]] = [
        couleurs_bouton_tres_difficile, 
        couleurs_bouton_difficile, 
        couleurs_bouton_moyen, 
        couleurs_bouton_facile
    ]

    canvas.create_text(
        (X_BOUTONS_DIF + PARAMS_BOUTONS_DIF["largeur"] // 2, 
         Y_CADRE + RAYON_COINS_CADRE + 25), 
        anchor=tk.CENTER, 
        text="Difficulté", 
        font=(POLICE, 30), 
        **PARAMS_TEXT
    )

    TAG_TRES_DIFFICILE: str = "tres_difficile"
    bouton_tres_difficile: dict[str, list[int] | int] = creer_bouton_rect(
        canvas=canvas, 
        coord=(X_BOUTONS_DIF, Y_RANGEE1_DIF), 
        tag=TAG_TRES_DIFFICILE, 
        texte="Très difficile", 
        couleur_fond=COULEURS_BOUTONS_MODE_DIF_DESACT["couleur_fond"], 
        couleur_bordure=COULEURS_BOUTONS_MODE_DIF_DESACT["couleur_bordure"], 
        **PARAMS_BOUTONS_DIF
    )

    TAG_DIFFICILE: str = "difficile"
    bouton_difficile: dict[str, list[int] | int] = creer_bouton_rect(
        canvas=canvas, 
        coord=(X_BOUTONS_DIF, Y_RANGEE2_DIF), 
        tag=TAG_DIFFICILE, 
        texte="Difficile", 
        couleur_fond=COULEURS_BOUTONS_MODE_DIF_DESACT["couleur_fond"], 
        couleur_bordure=COULEURS_BOUTONS_MODE_DIF_DESACT["couleur_bordure"], 
        **PARAMS_BOUTONS_DIF
    )

    TAG_MOYEN: str = "moyen"
    bouton_moyen: dict[str, list[int] | int] = creer_bouton_rect(
        canvas=canvas, 
        coord=(X_BOUTONS_DIF, Y_RANGEE3_DIF), 
        tag=TAG_MOYEN, 
        texte="Moyen", 
        couleur_fond=COULEURS_BOUTONS_MODE_DIF_DESACT["couleur_fond"], 
        couleur_bordure=COULEURS_BOUTONS_MODE_DIF_DESACT["couleur_bordure"], 
        **PARAMS_BOUTONS_DIF
    )

    TAG_FACILE: str = "facile"
    bouton_facile: dict[str, list[int] | int] = creer_bouton_rect(
        canvas=canvas, 
        coord=(X_BOUTONS_DIF, Y_RANGEE4_DIF), 
        tag=TAG_FACILE, 
        texte="Facile", 
        couleur_fond=COULEURS_BOUTONS_MODE_DIF_DESACT["couleur_fond"], 
        couleur_bordure=COULEURS_BOUTONS_MODE_DIF_DESACT["couleur_bordure"], 
        **PARAMS_BOUTONS_DIF
    )

    list_boutons_dif: list[dict[str, list[int] | int]] = [
        bouton_tres_difficile, 
        bouton_difficile, 
        bouton_moyen, 
        bouton_facile
    ]

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_TRES_DIFFICILE], 
        fond=[bouton_tres_difficile["fond"]], 
        bordure=bouton_tres_difficile["bordure"], 
        couleurs=couleurs_bouton_tres_difficile
    )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_DIFFICILE], 
        fond=[bouton_difficile["fond"]], 
        bordure=bouton_difficile["bordure"], 
        couleurs=couleurs_bouton_difficile
    )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_MOYEN], 
        fond=[bouton_moyen["fond"]], 
        bordure=bouton_moyen["bordure"], 
        couleurs=couleurs_bouton_moyen
    )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_FACILE], 
        fond=[bouton_facile["fond"]], 
        bordure=bouton_facile["bordure"], 
        couleurs=couleurs_bouton_facile
    )

    canvas.tag_bind(
        tagOrId=TAG_SUDOKU, 
        sequence="<Button-1>", 
        func=lambda event : bouton_active(
            canvas=canvas, 
            bouton_act=bouton_sudoku, 
            boutons_desact= \
                [bouton for bouton in list_boutons_mode if bouton != bouton_sudoku], 
            couleurs_act=COULEURS_BOUTONS_MODE_DIF_ACT, 
            couleurs_desact=COULEURS_BOUTONS_MODE_DIF_DESACT, 
            couleurs_bouton_act=couleurs_bouton_sudoku, 
            list_couleurs_boutons_desact=[couleurs for couleurs in list_couleurs_boutons_mode \
                                     if couleurs != couleurs_bouton_sudoku]
        )
    )

    canvas.tag_bind(
        tagOrId=TAG_KENKEN, 
        sequence="<Button-1>", 
        func=lambda event : bouton_active(
            canvas=canvas, 
            bouton_act=bouton_kenken, 
            boutons_desact= \
                [bouton for bouton in list_boutons_mode if bouton != bouton_kenken] + \
                    list_boutons_dif, 
            couleurs_act=COULEURS_BOUTONS_MODE_DIF_ACT, 
            couleurs_desact=COULEURS_BOUTONS_MODE_DIF_DESACT, 
            couleurs_bouton_act=couleurs_bouton_kenken, 
            list_couleurs_boutons_desact=[couleurs for couleurs in list_couleurs_boutons_mode \
                                     if couleurs != couleurs_bouton_kenken] + \
                                     list_couleurs_boutons_dif
        )
    )

    canvas.tag_bind(
        tagOrId=TAG_KAKURO, 
        sequence="<Button-1>", 
        func=lambda event : bouton_active(
            canvas=canvas, 
            bouton_act=bouton_kakuro, 
            boutons_desact= \
                [bouton for bouton in list_boutons_mode if bouton != bouton_kakuro] + \
                    list_boutons_dif, 
            couleurs_act=COULEURS_BOUTONS_MODE_DIF_ACT, 
            couleurs_desact=COULEURS_BOUTONS_MODE_DIF_DESACT, 
            couleurs_bouton_act=couleurs_bouton_kakuro, 
            list_couleurs_boutons_desact=[couleurs for couleurs in list_couleurs_boutons_mode \
                                     if couleurs != couleurs_bouton_kakuro] + \
                                     list_couleurs_boutons_dif
        )
    )
    
    canvas.tag_bind(
        tagOrId=TAG_CONSECUTIF, 
        sequence="<Button-1>", 
        func=lambda event : bouton_active(
            canvas=canvas, 
            bouton_act=bouton_consecutif, 
            boutons_desact= \
                [bouton for bouton in list_boutons_mode if bouton != bouton_consecutif], 
            couleurs_act=COULEURS_BOUTONS_MODE_DIF_ACT, 
            couleurs_desact=COULEURS_BOUTONS_MODE_DIF_DESACT, 
            couleurs_bouton_act=couleurs_bouton_consecutif, 
            list_couleurs_boutons_desact=[couleurs for couleurs in list_couleurs_boutons_mode \
                                     if couleurs != couleurs_bouton_consecutif]
        )
    )

    canvas.tag_bind(
        tagOrId=TAG_CHAOS, 
        sequence="<Button-1>", 
        func=lambda event : bouton_active(
            canvas=canvas, 
            bouton_act=bouton_chaos, 
            boutons_desact= \
                [bouton for bouton in list_boutons_mode if bouton != bouton_chaos] + \
                    list_boutons_dif, 
            couleurs_act=COULEURS_BOUTONS_MODE_DIF_ACT, 
            couleurs_desact=COULEURS_BOUTONS_MODE_DIF_DESACT, 
            couleurs_bouton_act=couleurs_bouton_chaos, 
            list_couleurs_boutons_desact=[couleurs for couleurs in list_couleurs_boutons_mode \
                                     if couleurs != couleurs_bouton_chaos] + \
                                     list_couleurs_boutons_dif
        )
    )

    canvas.tag_bind(
        tagOrId=TAG_16X16, 
        sequence="<Button-1>", 
        func=lambda event : bouton_active(
            canvas=canvas, 
            bouton_act=bouton_16x16, 
            boutons_desact= \
                [bouton for bouton in list_boutons_mode if bouton != bouton_16x16], 
            couleurs_act=COULEURS_BOUTONS_MODE_DIF_ACT, 
            couleurs_desact=COULEURS_BOUTONS_MODE_DIF_DESACT, 
            couleurs_bouton_act=couleurs_bouton_16x16, 
            list_couleurs_boutons_desact=[couleurs for couleurs in list_couleurs_boutons_mode \
                                     if couleurs != couleurs_bouton_16x16]
        )
    )

    canvas.tag_bind(
        tagOrId=TAG_WINDOKU, 
        sequence="<Button-1>", 
        func=lambda event : bouton_active(
            canvas=canvas, 
            bouton_act=bouton_windoku, 
            boutons_desact= \
                [bouton for bouton in list_boutons_mode if bouton != bouton_windoku], 
            couleurs_act=COULEURS_BOUTONS_MODE_DIF_ACT, 
            couleurs_desact=COULEURS_BOUTONS_MODE_DIF_DESACT, 
            couleurs_bouton_act=couleurs_bouton_windoku, 
            list_couleurs_boutons_desact=[couleurs for couleurs in list_couleurs_boutons_mode \
                                     if couleurs != couleurs_bouton_windoku]
        )
    )
    canvas.tag_bind(
        tagOrId=TAG_TRES_DIFFICILE, 
        sequence="<Button-1>", 
        func=lambda event : bouton_active(
            canvas=canvas, 
            bouton_act=bouton_tres_difficile, 
            boutons_desact= \
                [bouton for bouton in list_boutons_dif if bouton != bouton_tres_difficile] + \
                    [bouton_kakuro, bouton_kenken, bouton_chaos], 
            couleurs_act=COULEURS_BOUTONS_MODE_DIF_ACT, 
            couleurs_desact=COULEURS_BOUTONS_MODE_DIF_DESACT, 
            couleurs_bouton_act=couleurs_bouton_tres_difficile, 
            list_couleurs_boutons_desact=[couleurs for couleurs in list_couleurs_boutons_dif \
                                     if couleurs != couleurs_bouton_tres_difficile] + \
                                     [couleurs_bouton_kakuro, couleurs_bouton_kenken, 
                                      couleurs_bouton_chaos]
        )
    )

    canvas.tag_bind(
        tagOrId=TAG_DIFFICILE, 
        sequence="<Button-1>", 
        func=lambda event : bouton_active(
            canvas=canvas, 
            bouton_act=bouton_difficile, 
            boutons_desact= \
                [bouton for bouton in list_boutons_dif if bouton != bouton_difficile] + \
                    [bouton_kakuro, bouton_kenken, bouton_chaos], 
            couleurs_act=COULEURS_BOUTONS_MODE_DIF_ACT, 
            couleurs_desact=COULEURS_BOUTONS_MODE_DIF_DESACT, 
            couleurs_bouton_act=couleurs_bouton_difficile, 
            list_couleurs_boutons_desact=[couleurs for couleurs in list_couleurs_boutons_dif \
                                     if couleurs != couleurs_bouton_difficile] + \
                                     [couleurs_bouton_kakuro, couleurs_bouton_kenken, 
                                      couleurs_bouton_chaos]
        )
    )

    canvas.tag_bind(
        tagOrId=TAG_MOYEN, 
        sequence="<Button-1>", 
        func=lambda event : bouton_active(
            canvas=canvas, 
            bouton_act=bouton_moyen, 
            boutons_desact= \
                [bouton for bouton in list_boutons_dif if bouton != bouton_moyen] + \
                    [bouton_kakuro, bouton_kenken, bouton_chaos], 
            couleurs_act=COULEURS_BOUTONS_MODE_DIF_ACT, 
            couleurs_desact=COULEURS_BOUTONS_MODE_DIF_DESACT, 
            couleurs_bouton_act=couleurs_bouton_moyen, 
            list_couleurs_boutons_desact=[couleurs for couleurs in list_couleurs_boutons_dif \
                                     if couleurs != couleurs_bouton_moyen] + \
                                     [couleurs_bouton_kakuro, couleurs_bouton_kenken, 
                                      couleurs_bouton_chaos]
        )
    )

    canvas.tag_bind(
        tagOrId=TAG_FACILE, 
        sequence="<Button-1>", 
        func=lambda event : bouton_active(
            canvas=canvas, 
            bouton_act=bouton_facile, 
            boutons_desact= \
                [bouton for bouton in list_boutons_dif if bouton != bouton_facile] + \
                    [bouton_kakuro, bouton_kenken, bouton_chaos], 
            couleurs_act=COULEURS_BOUTONS_MODE_DIF_ACT, 
            couleurs_desact=COULEURS_BOUTONS_MODE_DIF_DESACT, 
            couleurs_bouton_act=couleurs_bouton_facile, 
            list_couleurs_boutons_desact=[couleurs for couleurs in list_couleurs_boutons_dif \
                                     if couleurs != couleurs_bouton_facile] + \
                                     [couleurs_bouton_kakuro, couleurs_bouton_kenken, 
                                      couleurs_bouton_chaos]
        )
    )

    COULEURS_BOUTONS_MENU: dict[str, str] = {
        "couleur_fond" : "#939393",
        "couleur_bordure" : "#ADADAD", 
        "couleur_fond_surv" : "#636363",
        "couleur_bordure_surv" : "#454545"
    }

    PARAMS_BOUTONS_MENU: dict[str, str | int | tuple[str | int, ...]] = {
        "largeur" : 300, 
        "hauteur" : 124,
        "police" : ("Cooper Black", 16), 
        "epaisseur_bordure" : 2, 
        "couleur_texte" : "#ffffff"
    }
    
    X_BOUTONS: int = 50

    Y_BOUTON_RETOUR: int = HAUTEUR_PIXEL_FENETRE - PARAMS_BOUTONS_MENU["hauteur"] - 150
    TAG_RETOUR: str = "bouton_menu_partie_perso_retour"

    bouton_retour: dict[str, list[int] | int] =  \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(X_BOUTONS, Y_BOUTON_RETOUR), 
            tag=TAG_RETOUR, 
            texte="Retour", 
            couleur_fond=COULEURS_BOUTONS_MENU["couleur_fond"], 
            couleur_bordure=COULEURS_BOUTONS_MENU["couleur_bordure"], 
            **PARAMS_BOUTONS_MENU
        )
    
    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_RETOUR], 
        fond=bouton_retour["fond"], 
        bordure=bouton_retour["bordure"], 
        couleurs=COULEURS_BOUTONS_MENU
    )
    
    Y_BOUTON_JOUER: int = Y_BOUTON_RETOUR - PARAMS_BOUTONS_MENU["hauteur"] - 100
    TAG_JOUER: str = "bouton_credits_jouer"

    bouton_jouer: dict[str, list[int] | int] =  \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(X_BOUTONS, Y_BOUTON_JOUER), 
            tag=TAG_JOUER, 
            texte="Jouer", 
            couleur_fond=COULEURS_BOUTONS_MENU["couleur_fond"], 
            couleur_bordure=COULEURS_BOUTONS_MENU["couleur_bordure"], 
            **PARAMS_BOUTONS_MENU
        )
    
    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_JOUER], 
        fond=bouton_jouer["fond"], 
        bordure=bouton_jouer["bordure"], 
        couleurs=COULEURS_BOUTONS_MENU
    )

    canvas.tag_bind(
        tagOrId=TAG_RETOUR, 
        sequence="<Button-1>", 
        func=lambda event: retour_menu(
            canvas=canvas, 
            tags_ou_ids=[TAG, TAG_RETOUR, TAG_JOUER, TAG_16X16, TAG_CHAOS, TAG_CONSECUTIF, 
                         TAG_DIFFICILE, TAG_FACILE, TAG_KAKURO, TAG_KENKEN, 
                         TAG_MOYEN, TAG_TRES_DIFFICILE, TAG_WINDOKU, TAG_SUDOKU]
        )
    )

    canvas.tag_bind(
        tagOrId=TAG_JOUER, 
        sequence="<Button-1>", 
        func=lambda event: jouer_debut(
            canvas=canvas, 
            boutons_mode=list_boutons_mode, 
            boutons_dif=list_boutons_dif, 
            couleurs_bouton_act=COULEURS_BOUTONS_MODE_DIF_ACT, 
            tags_ou_ids_page_suppr=[TAG, TAG_16X16, TAG_CHAOS, TAG_CONSECUTIF, TAG_DIFFICILE, 
                                    TAG_FACILE, TAG_JOUER, TAG_KAKURO, TAG_KENKEN, TAG_MOYEN, 
                                    TAG_RETOUR, TAG_SUDOKU, TAG_TRES_DIFFICILE, TAG_WINDOKU]
        )
    )