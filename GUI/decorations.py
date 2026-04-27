import tkinter as tk


def creer_cadre(canvas: tk.Canvas, coord: tuple[int, int], largeur: int, hauteur: int, 
                couleur: str, rayon_coins: int, tag: str) -> list[int]:
    
    cadre: list[int] = []

    cadre.append(
        canvas.create_oval((coord[0], coord[1]), (coord[0] + 2 * rayon_coins, coord[1] + 2 * rayon_coins), 
                           fill=couleur, outline=couleur, tags=tag)
    )
    
    cadre.append(
        canvas.create_oval((coord[0] + largeur - 2 * rayon_coins, coord[1]), 
                           (coord[0] + largeur, coord[1] + 2 * rayon_coins), 
                           fill=couleur, outline=couleur, tags=tag)
    )
    
    cadre.append(
        canvas.create_oval((coord[0] + largeur - 2 * rayon_coins, coord[1] + hauteur - 2 * rayon_coins), 
                           (coord[0] + largeur, coord[1] + hauteur), 
                           fill=couleur, outline=couleur, tags=tag)
    )
    
    cadre.append(
        canvas.create_oval((coord[0], coord[1] + hauteur - 2 * rayon_coins), 
                           (coord[0] + 2 * rayon_coins, coord[1] + hauteur), 
                           fill=couleur, outline=couleur, tags=tag)
    )
    
    cadre.append(
        canvas.create_polygon((coord[0] + rayon_coins, coord[1]), 
                              (coord[0] - rayon_coins + largeur, coord[1]), 
                              (coord[0] - rayon_coins + largeur, coord[1] + rayon_coins), 
                              (coord[0] + largeur, coord[1] + rayon_coins), 
                              (coord[0] + largeur, coord[1] - rayon_coins + hauteur), 
                              (coord[0] - rayon_coins + largeur, coord[1] - rayon_coins + hauteur), 
                              (coord[0] - rayon_coins + largeur, coord[1] + hauteur), 
                              (coord[0] + rayon_coins, coord[1] + hauteur), 
                              (coord[0] + rayon_coins, coord[1] - rayon_coins + hauteur), 
                              (coord[0], coord[1] - rayon_coins + hauteur), 
                              (coord[0], coord[1] + rayon_coins), 
                              (coord[0] + rayon_coins, coord[1] + rayon_coins), 
                              fill=couleur, outline=couleur, tags=tag)
    )
    
    return cadre