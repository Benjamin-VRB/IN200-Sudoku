import json 

JSON_SAUVEGARDES = "Sauvegardes/grilles_sauvegardees.json"


def charger_sauvegardes() -> list:

    try:
        lecture=open(
            file=JSON_SAUVEGARDES, 
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
            file=JSON_SAUVEGARDES, 
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


def charger_sauvegarde():

    lecture=open(JSON_SAUVEGARDES, "r")
    donnee = json.load(lecture)
    lecture.close()

    if donnee["etat"] == "vide" : 
        return None 
    return donnee


def sauvegarde_partie(nom_fichier, variante, grille_init, grille_actu, temps, aides, erreurs):
    # Blocage du nom réservé aux statistiques
    if nom_fichier.lower() == "stats":
        print("Nom interdit : 'stats' est réservé au système.")
        nouveau = input("Choisis un autre nom : ")
        return sauvegarde_partie(nouveau, variante, grille_init, grille_actu, temps, aides, erreurs)

    # On ajoute le dossier 'saves/' devant le nom et verifie la presence du .json
    if not nom_fichier.endswith(".json"):
        nom_final = "saves/" + nom_fichier + ".json"
    else:
        nom_final = "saves/" + nom_fichier

    # Vérification d'existence
    try:
        # On essaie d'ouvrir pour voir s'il est là
        with open(nom_final, "r"):
            existe = True
    except FileNotFoundError:
        # S'il n'est pas là, c'est parfait, on continue
        existe = False

    # Si le fichier existe, on lance la procédure de confirmation
    if existe:
        while True:
            reponse = input(f"Le fichier {nom_final} existe déjà. Écraser ? (oui/non) : ").lower().strip()
            if reponse == "oui":
                break # On sort de la boucle pour aller écrire le fichier  
            
            if reponse == "non":
                nouveau_nom = input("Entrez un nouveau nom de sauvegarde : ")
                # On relance tout le processus avec le nouveau nom
                return sauvegarde_partie(nouveau_nom, variante, grille_init, grille_actu, temps, aides, erreurs)
            
            print("Veuillez répondre par 'oui' ou 'non'.")

    # Préparation des données dans l'ordre voulu
    donnees = {
        "variante": variante,
        "grille_initiale": grille_init,
        "grille_actuelle": grille_actu,
        "temps": temps,
        "nombre_aides": aides,
        "nombre_erreurs": erreurs
    }

    # Écriture effective
    try:
        with open(nom_final, "w", encoding="utf-8") as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)
        print("Sauvegarde réussie !")
        return True
    except Exception as e:
        print(f"Erreur imprévue : {e}")
        return False
    

def mettre_a_jour_stats(evenement, difficulte=None):
    # evenement peut être : "erreur", "aide", "lance", "termine"
    nom_fichier = "stats.json"
    
    # On essaie de lire les stats actuelles
    try:
        with open(nom_fichier, "r", encoding="utf-8") as f:
            stats = json.load(f)
    except FileNotFoundError:
        # Si c'est la toute première fois, on initialise tout à zéro
        stats = {
            "puzzles_lances": 0, "puzzles_termines": 0,
            "total_erreurs": 0, "total_aides": 0,
            "facile": 0, "moyen": 0, "difficile": 0
        }

    # On traite l'action qui vient de se passer
    if evenement == "erreur":
        stats["total_erreurs"] = stats["total_erreurs"] + 1
    
    elif evenement == "aide":
        stats["total_aides"] = stats["total_aides"] + 1
    
    elif evenement == "lance":
        stats["puzzles_lances"] = stats["puzzles_lances"] + 1
    
    elif evenement == "termine":
        stats["puzzles_termines"] = stats["puzzles_termines"] + 1
        # Si on donne la difficulté, on ajoute +1 au compteur du niveau
        if difficulte:
            niveau = difficulte.lower()
            if niveau in stats:
                stats[niveau] = stats[niveau] + 1
            else:
                stats[niveau] = 1

    # On réenregistre le fichier après chaque modif 
    try:
        with open(nom_fichier, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Souci avec les stats : {e}")


def charger_partie(nom_fichier):
    # On s'assure d'avoir l'extension pour trouver le bon fichier et on rajoute le saves/
    if not nom_fichier.endswith(".json"):
        nom_final = "saves/" + nom_fichier + ".json"
    else:
        nom_final = "saves/" + nom_fichier

    try:
        # On tente d'ouvrir le fichier en mode lecture 
        with open(nom_final, "r", encoding="utf-8") as f:
            # On transforme le texte JSON en dictionnaire Python
            donnees = json.load(f)
        
        print(f"C'est parti ! Chargement de {nom_final} réussi.")
        return donnees

    except FileNotFoundError:
        # Si le fichier a été supprimé entre-temps ou est introuvable
        print(f"Oups, le fichier {nom_final} est introuvable.")
        return None
        
    except json.JSONDecodeError:
        # Si quelqu'un a modifié le fichier à la main et a fait une erreur
        print("Erreur : Le fichier de sauvegarde est corrompu et illisible.")
        return None
        
    except Exception as e:
        # Pour n'importe quel autre souci technique
        print(f"Une erreur bizarre est survenue : {e}")
        return None
