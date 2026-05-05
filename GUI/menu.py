import tkinter as tk

from GUI.fenetre import racine, LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.stats import aller_stats
from GUI.credits import aller_credits
from GUI.menu_sauvegardes import aller_menu_sauvegardes
from GUI.widgets import creer_boutton_arrondi, survole_non_survole
from GUI.animations import mouvement_interieur_fond_menu
from GUI.menu_partie_perso import aller_menu_partie_perso
from GUI.interface_jeu import aller_grille
from GUI.puzzle import aller_puzzle


def aller_menu() -> tk.Canvas:
    """
    Crée le canvas et affiche le menu
    """
    # canvas
    COULEUR_FOND_CNV: str = "#fffbf4"

    canvas: tk.Canvas = tk.Canvas(
        master=racine, 
        width=LARGEUR_PIXEL_FENETRE,
        height=HAUTEUR_PIXEL_FENETRE,
        bg=COULEUR_FOND_CNV
    )

    canvas.pack()

    # menu

    # côté gauche du fond
    COULEUR_FOND_GAUCHE: str = "#4373A3"
    TAG_FOND_GAUCHE: str = "fond_bleu"
    x_lim_gauche_haut: int = LARGEUR_PIXEL_FENETRE // 4 + 100
    x_lim_gauche_bas: int = LARGEUR_PIXEL_FENETRE // 5 + 100

    canvas.create_polygon(
        ((-x_lim_gauche_haut, 0), (0, 0), (x_lim_gauche_bas - x_lim_gauche_haut, HAUTEUR_PIXEL_FENETRE), 
         (-x_lim_gauche_haut, HAUTEUR_PIXEL_FENETRE)), 
        fill=COULEUR_FOND_GAUCHE, 
        outline=COULEUR_FOND_GAUCHE, 
        tags=TAG_FOND_GAUCHE
    )

    canvas.create_polygon(
        ((-50, 0), (-25, 0), 
         (x_lim_gauche_bas - x_lim_gauche_haut - 25, HAUTEUR_PIXEL_FENETRE), 
         (x_lim_gauche_bas - x_lim_gauche_haut - 50, HAUTEUR_PIXEL_FENETRE)), 
        fill=COULEUR_FOND_CNV, 
        outline=COULEUR_FOND_CNV, 
        tags=TAG_FOND_GAUCHE
    )
    
    # côté droite du fond
    COULEUR_FOND_DROITE: str = "#CE8450"
    TAG_FOND_DROITE: str = "fond_orange"
    x_lim_droite_haut: int = 4 * LARGEUR_PIXEL_FENETRE // 5 - 100
    x_lim_droite_bas: int = 3 * LARGEUR_PIXEL_FENETRE // 4 - 100

    canvas.create_polygon(
        ((2 * LARGEUR_PIXEL_FENETRE - x_lim_droite_bas, 0), 
         (x_lim_droite_haut + LARGEUR_PIXEL_FENETRE - x_lim_droite_bas, 0), 
         (LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE), 
         (2 * LARGEUR_PIXEL_FENETRE - x_lim_droite_bas, HAUTEUR_PIXEL_FENETRE)), 
        fill=COULEUR_FOND_DROITE, 
        outline=COULEUR_FOND_DROITE, 
        tags=TAG_FOND_DROITE
    )

    canvas.create_polygon(
        ((x_lim_droite_haut + 25 + LARGEUR_PIXEL_FENETRE - x_lim_droite_bas, 0),
         (x_lim_droite_haut + 50 + LARGEUR_PIXEL_FENETRE - x_lim_droite_bas, 0), 
         (LARGEUR_PIXEL_FENETRE + 50, HAUTEUR_PIXEL_FENETRE), 
         (LARGEUR_PIXEL_FENETRE + 25, HAUTEUR_PIXEL_FENETRE)), 
        fill=COULEUR_FOND_CNV, 
        outline=COULEUR_FOND_CNV, 
        tags=TAG_FOND_DROITE
    )
    
    # boutons
    PARAMS_BOUTON: dict[str, int | tuple[str, int]] = {
        "largeur" : 300,
        "hauteur" : 124,
        "police" : ("Cooper Black", 16),
        "epaisseur_bordure" : 2
    }

    COULEURS_BOUTON: dict[str, str] = {
        "couleur_fond" : "#E9E5DE",
        "couleur_bordure" : "#F4EFE4"
    }
    
    COULEURS_SURVOLE: dict[str, str] = {
        "couleur_fond_surv" : "#C7C3BE",
        "couleur_bordure_surv" : "#AFAAA3"
    }

    ECART_RANGEE: int = 200
    RANGEE1: int = (HAUTEUR_PIXEL_FENETRE - PARAMS_BOUTON["hauteur"]) // 2 - ECART_RANGEE
    RANGEE2: int = RANGEE1 + ECART_RANGEE
    RANGEE3: int = RANGEE2 + ECART_RANGEE
    COLONNE1: int = -PARAMS_BOUTON["largeur"]
    COLONNE2: int = LARGEUR_PIXEL_FENETRE

    TAG_PERSO: str = "bouton_perso"
    TAG_PUZZ: str = "bouton_puzz"
    TAG_SAUV: str = "bouton_sauv"
    TAG_STATS: str = "bouton_stats"
    TAG_CREDITS: str = "bouton_credits"
    TAG_QUITTER: str = "bouton_quitter"

    bouton_perso: dict[str, list[int] | int] = \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(COLONNE1, RANGEE1), 
            tag=TAG_PERSO, 
            texte="Partie personnalisée", 
            couleur_texte=COULEUR_FOND_GAUCHE, 
            **(PARAMS_BOUTON | COULEURS_BOUTON)
        )
    
    bouton_puzz: dict[str, list[int] | int] = \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(COLONNE1, RANGEE2), 
            tag=TAG_PUZZ, 
            texte="Puzzles", 
            couleur_texte=COULEUR_FOND_GAUCHE, 
            **(PARAMS_BOUTON | COULEURS_BOUTON)
        )
    
    bouton_sauv: dict[str, list[int] | int] = \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(COLONNE1, RANGEE3), 
            tag=TAG_SAUV, 
            texte="Sauvegardes", 
            couleur_texte=COULEUR_FOND_GAUCHE, 
            **(PARAMS_BOUTON | COULEURS_BOUTON)
        )
    
    bouton_stats: dict[str, list[int] | int] = \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(COLONNE2, RANGEE1), 
            tag=TAG_STATS, 
            texte="Statistiques", 
            couleur_texte=COULEUR_FOND_DROITE, 
            **(PARAMS_BOUTON | COULEURS_BOUTON)
        )
    
    bouton_credits: dict[str, list[int] | int] = \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(COLONNE2, RANGEE2), 
            tag=TAG_CREDITS, 
            texte="Crédits", 
            couleur_texte=COULEUR_FOND_DROITE, 
            **(PARAMS_BOUTON | COULEURS_BOUTON)
        )
    
    bouton_quitter: dict[str, list[int] | int] = \
        creer_boutton_arrondi(
            canvas=canvas, 
            coord=(COLONNE2, RANGEE3), 
            tag=TAG_QUITTER, 
            texte="Quitter", 
            couleur_texte=COULEUR_FOND_DROITE, 
            **(PARAMS_BOUTON | COULEURS_BOUTON)
        )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_PERSO], 
        fond=bouton_perso["fond"], 
        bordure=bouton_perso["bordure"], 
        **(COULEURS_BOUTON | COULEURS_SURVOLE)
    )
    
    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_PUZZ], 
        fond=bouton_puzz["fond"], 
        bordure=bouton_puzz["bordure"], 
        **(COULEURS_BOUTON | COULEURS_SURVOLE)
    )
    
    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_SAUV], 
        fond=bouton_sauv["fond"], 
        bordure=bouton_sauv["bordure"], 
        **(COULEURS_BOUTON | COULEURS_SURVOLE)
    )

    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_STATS], 
        fond=bouton_stats["fond"], 
        bordure=bouton_stats["bordure"], 
        **(COULEURS_BOUTON | COULEURS_SURVOLE)
    )
    
    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_CREDITS], 
        fond=bouton_credits["fond"], 
        bordure=bouton_credits["bordure"], 
        **(COULEURS_BOUTON | COULEURS_SURVOLE)
    )
    
    survole_non_survole(
        canvas=canvas, 
        tags_ou_ids=[TAG_QUITTER], 
        fond=bouton_quitter["fond"], 
        bordure=bouton_quitter["bordure"], 
        **(COULEURS_BOUTON | COULEURS_SURVOLE)
    )

    canvas.tag_bind(
        tagOrId=TAG_PERSO, 
        sequence="<Button-1>", 
        func=lambda event: aller_grille(canvas=canvas, type="sudoku", difficulte="", temps_depart=0)
    )
    
    canvas.tag_bind(
        tagOrId=TAG_SAUV, 
        sequence="<Button-1>", 
        func=lambda event: aller_menu_sauvegardes(canvas=canvas)
    )
    
    canvas.tag_bind(
        tagOrId=TAG_STATS, 
        sequence="<Button-1>", 
        func=lambda event: aller_stats(canvas=canvas)
    )
    
    canvas.tag_bind(
        tagOrId=TAG_CREDITS, 
        sequence="<Button-1>", 
        func=lambda event: aller_credits(canvas=canvas)
    )
    
    canvas.tag_bind(
        tagOrId=TAG_PUZZ, 
        sequence="<Button-1>", 
        func=lambda event: aller_puzzle(canvas=canvas)
    )

    canvas.tag_bind(
        tagOrId=TAG_QUITTER, 
        sequence="<Button-1>", 
        func=lambda event: exit()
    )

    # titre
    canvas.create_text(
        (LARGEUR_PIXEL_FENETRE // 2, 0), 
        text="Sudoku", 
        font=("Californian fb", 100), 
        anchor=tk.S, 
        fill="#A38D54", 
        tags="titre_menu"
    )
    
    mouvement_interieur_fond_menu(canvas=canvas)
    return canvas