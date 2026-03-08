import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE


def mouvement_interieur_fond_menu(canvas: tk.Canvas, iteration: int = 1) -> None:
    """
    Déplace le fond du menu, le titre ainsi que les boutons vers l'intérieur de la fenêtre
    """
    hauteur_titre: int = canvas.bbox("sudoku")[3] - canvas.bbox("sudoku")[1]
    distance_finale_titre: int = (HAUTEUR_PIXEL_FENETRE + hauteur_titre) / 2
    DISTANCE_FINALE_FOND: int = LARGEUR_PIXEL_FENETRE / 4 + 100
    DISTANCE_FINALE_BOUTON: int = 350
    NB_ITERATION: int = 80

    # fond
    canvas.move("fond_bleu", DISTANCE_FINALE_FOND / NB_ITERATION, 0)
    canvas.move("fond_orange", -DISTANCE_FINALE_FOND / NB_ITERATION, 0)
    
    # titre
    canvas.move("sudoku", 0, distance_finale_titre / NB_ITERATION)
   
    # boutons
    canvas.move("bouton_perso", DISTANCE_FINALE_BOUTON / NB_ITERATION, 0)
    canvas.move("bouton_puzz", DISTANCE_FINALE_BOUTON / NB_ITERATION, 0)
    canvas.move("bouton_sauv", DISTANCE_FINALE_BOUTON / NB_ITERATION, 0)
    canvas.move("bouton_stats", -DISTANCE_FINALE_BOUTON / NB_ITERATION, 0)
    canvas.move("bouton_credits", -DISTANCE_FINALE_BOUTON / NB_ITERATION, 0)
    canvas.move("bouton_quitter", -DISTANCE_FINALE_BOUTON / NB_ITERATION, 0)

    if iteration < NB_ITERATION:
        temps_attente: int = 630 // NB_ITERATION
        canvas.after(temps_attente, mouvement_interieur_fond_menu, *[canvas, iteration + 1])


def mouvement_exterieur_fond_menu(canvas: tk.Canvas, instantane: bool = True, 
                                  iteration: int = 1) -> None:
    """
    Déplace le fond du menu, le titre ainsi que les boutons vers l'extérieur de la fenêtre
    """
    hauteur_titre: int = canvas.bbox("sudoku")[3] - canvas.bbox("sudoku")[1]
    distance_finale_titre: int = (HAUTEUR_PIXEL_FENETRE + hauteur_titre) / 2
    DISTANCE_FINALE_FOND: int = LARGEUR_PIXEL_FENETRE / 4 + 100
    DISTANCE_FINALE_BOUTON: int = 350
    nb_iteration: int = 80

    if instantane:
        nb_iteration = 1
    
    # fond
    canvas.move("fond_bleu", -DISTANCE_FINALE_FOND / nb_iteration, 0)
    canvas.move("fond_orange", DISTANCE_FINALE_FOND / nb_iteration, 0)

    # titre
    canvas.move("sudoku", 0, -distance_finale_titre / nb_iteration)

    # boutons
    canvas.move("bouton_perso", -DISTANCE_FINALE_BOUTON / nb_iteration, 0)
    canvas.move("bouton_puzz", -DISTANCE_FINALE_BOUTON / nb_iteration, 0)
    canvas.move("bouton_sauv", -DISTANCE_FINALE_BOUTON / nb_iteration, 0)
    canvas.move("bouton_stats", DISTANCE_FINALE_BOUTON / nb_iteration, 0)
    canvas.move("bouton_credits", DISTANCE_FINALE_BOUTON / nb_iteration, 0)
    canvas.move("bouton_quitter", DISTANCE_FINALE_BOUTON / nb_iteration, 0)

    if iteration < nb_iteration:
        temps_attente: int = 630 // nb_iteration
        canvas.after(temps_attente, mouvement_exterieur_fond_menu, *[canvas, False, iteration + 1])
    

def retour_menu(canvas: tk.Canvas, tags_suppr: list[str]) -> None:
    """
    Retourne au menu en supprimant les éléments de l'interface qu'on désire quitter et en 
    actionnant l'animation du menu
    """
    canvas.delete(*tags_suppr)
    mouvement_interieur_fond_menu(canvas)