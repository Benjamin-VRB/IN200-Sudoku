import Sudoku_Irregulier as irregulier 

grille_cage,cages,tentative = irregulier.generation_cage_utile()


print("\n-----Cage----\n")

for ligne in grille_cage : 
    print(ligne)

grille_vide = [ [0 for _ in range(9)]for _ in range(9)]
grille_complete = irregulier.generer_grille_complete(grille_vide,cages)

print("\n-----Grille----\n")

for ligne in grille_complete : 
    print(ligne)


print("\n-----Grille à résoudre----\n")

grille_à_résoudre  = irregulier.supprime_valeurs_irregulier(grille_complete,grille_cage,73)

for ligne in grille_à_résoudre: 
    print(ligne)