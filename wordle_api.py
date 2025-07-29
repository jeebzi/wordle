from random import randint
from util import init_matrice
from wordle import est_possible, init_liste_illegal, most_common


def load_name(path):
    """
    charge les noms dans le fichier puis renvoie la liste de ces noms
    """
    tab = []
    f = open(path, 'r')
    for ligne in f:
        tab += [ligne[:-1]]
    f.close()
    return tab

def make_guess(choix, couleurs):
    """
    remplace init_guess prend en entrée
    choix : mot de 5 lettres
    couleurs: chaien de chiffres
    renvoie [choix, [0,0,2,0,1]] ou une erreure
    """
    if len(choix) != 5:
        raise ValueError("le mot doit contenir 5 lettres")
    if len(couleurs) != 5 or any(c not in '012' for c in couleurs):
        raise ValueError("couleurs invalide; utilisez 0, 1 ou 2")
    return [choix, [int(c) for c in couleurs]]

def filter_words(mots_possible, guess):
    """
    retourne une nouvelle liste de mot filtrer selon guess
    """
    lettres_illegal, lettre_possible = init_liste_illegal(guess)
    return [m for m in mots_possible
            if est_possible(m, guess, lettres_illegal, lettre_possible)]

def recommend(mots: list, round: int) -> str:
    """
    Renvoie la recommandation :
    - si round==0: 'arose'
    - sinon: le mot le plus commun selon most_common
    """
    return "arose" if round == 0 else mots[most_common(mots)]

def full_round(path: str, historique: list) -> dict:
    """
    Pour un round complet :
    - path : chemin vers le fichier de mots
    - historique : liste de dict { 'choix': str, 'couleurs': str }
    Renvoie { 'mots_restants': [...], 'reco': ..., 'round': n }
    """
    mots = load_name(path)
    for i, h in enumerate(historique):
        guess = make_guess(h['choix'], h['couleurs'])
        mots = filter_words(mots, guess)
    reco = recommend(mots, len(historique))
    return {
        'mots_restants': mots,
        'reco': reco,
        'round': len(historique)
    }
