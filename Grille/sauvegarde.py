import json 

FICHIER_SAUVEGARDE = "Sauvegardes/grilles_sauvegardees.json"


def charger_sauvegardes() -> list:

    try:
        lecture=open(
            file=FICHIER_SAUVEGARDE, 
            mode="r"
        )
        sauv: list = json.load(fp=lecture)
        lecture.close()
    except:
        sauv: list = []
    return sauv


def modifier_sauvegardes(fonction):
    def fonction_modifiee(**arguments):
        sauv: list = charger_sauvegardes()
        sauv: list = fonction(
            sauv=sauv, 
            **arguments
        )
        fich = open(
            file=FICHIER_SAUVEGARDE, 
            mode="w"
        )
        json.dump(
            obj=sauv, 
            fp=fich, 
            indent=2, 
            sort_keys=True
        )
    return fonction_modifiee


@modifier_sauvegardes
def sauvegarder(
    sauv: list,
    nom: str, 
    grille_actuelle: list[list[int]], 
    grille_solution: list[list[int]], 
    cases_verr: tuple[list[int], list[int]], 
    temps: int, 
    date: str, 
    type_grille: str, 
    statut: str, 
    difficulte: str
) -> list:
    
    donnee: dict[str, str | list[list[int]] | tuple[list[int], list[int]] | int] = {
        "nom" : nom,
        "date" : date,
        "type" : type_grille,
        "grille_actuelle" : grille_actuelle,
        "grille_solution" : grille_solution,
        "cases_verrouillees" : cases_verr,
        "temps" : temps, 
        "statut" : statut, 
        "difficulte" : difficulte
    }
    
    sauv.insert(0, donnee)
    return sauv


@modifier_sauvegardes
def supprimer_sauvegardes(
    sauv: list, 
    indices: list[int]
) -> list:
    
    for indice in indices:
        if indice < 0:
            indice += len(sauv)
    list(set(indices)).sort(reverse=True) 
    for indice in indices:
        if indice < len(sauv):
            sauv.pop(indice)
    return sauv
    


