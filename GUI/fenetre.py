import tkinter as tk


TITRE: str = "Sudoku"
REDIMENSIONNABLE: bool = False

racine: tk.Tk = tk.Tk()

LARGEUR_PIXEL_FENETRE: int = 1280
HAUTEUR_PIXEL_FENETRE: int = 720

racine.title(TITRE)
racine.resizable(width=REDIMENSIONNABLE, height=REDIMENSIONNABLE)
racine.geometry(f"{LARGEUR_PIXEL_FENETRE}x{HAUTEUR_PIXEL_FENETRE}")