import Sudoku_Irregulier as irregulier 

grille_complete = False 

while not grille_complete:
    plan_cage, dico_cages, tentative = irregulier.generer_structure_valide()
    grille_vide = [[0 for _ in range(9)] for _ in range(9)]
    grille_complete = irregulier.generer_grille_complete(grille_vide, dico_cages, plan_cage)


print("\n-----Cage----\n")

for ligne in plan_cage : 
    print(ligne)

print("\n-----Grille----\n")

for ligne in grille_complete : 
    print(ligne)

print("\n-----Grille à résoudre----\n")

grille_à_résoudre  = irregulier.cree_grille_a_resoudre(grille_complete,dico_cages,plan_cage,50)

for ligne in grille_à_résoudre: 
    print(ligne)