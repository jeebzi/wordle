from random import randint
from util import init_matrice

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

def faire_choix():
    """
    prompte l'utilisateur à choisir un mot de 5 lettres
    """
    choix = input("choisissez un mot de 5 lettres: ")
    while len(choix) != 5:
        choix = input("arrête de faire le retard: ")
    return choix

def init_guess(choix):
    """
    a partir d'un choix retourne un guess
    """
    guess = [choix, [0] * len(choix)]
    couleurs = input("rentrez les couleur obtenue 0 pour gris 1 pour jaune 2 pour vert ex:00201: ")
    while len(couleurs) != len(choix):
        couleurs = input("pas de bonne taille: ")
    i = 0
    while i < len(couleurs):
        guess[1][i] = int(couleurs[i])
        i += 1
    return guess

def filtre(mots_possible, guess):
    """
    prend un guess et la liste des mots possible
    puis filtre pour ne garder que ceux qui remplissent les conditions
    un guess et un tableau de 2 élément, le premier et la chaine de charactère
    le second un tableau d'entier 0:gris 1:jaune 2:vert
    """
    lettres_illegal, lettre_possible = init_liste_illegal(guess)
    cpt = 0
    i = 0
    n = len(mots_possible)
    while cpt < n:
        if est_possible(mots_possible[i], guess, lettres_illegal, lettre_possible) == True:
            i += 1
        else:
            mots_possible.pop(i)
        cpt += 1

def est_possible(mot, guess, lettres_illegal, lettre_possible):
    """
    prend un mote et un guess et renvoie True si le mots est compatible False sinon
    """
    possible = []
    for lettre in lettre_possible:
        possible += [lettre]
    i = 0 #itère sur les lettres
    while i < len(mot):
        if (lettres_illegal[ord(mot[i]) - ord('a')] and guess[1][i] != 2 and mot[i] not in possible) == 1 or (guess[1][i] == 2 and guess[0][i] != mot[i]) or (guess[1][i] == 1 and guess[0][i] == mot[i]):
            return False
        if mot[i] in possible:
            possible.remove(mot[i])
        i += 1
    if len(possible) > 0:
        return False
    return True

def init_liste_illegal(guess):
    """retourne la liste binaire de 26 élément avec 1 si la lettre ne doit pas être
    dans le mot
    """
    illegal = [0] * 26
    possible = []
    i = 0
    while i < len(guess[0]):
        if guess[1][i] == 0:
            illegal[ord(guess[0][i]) - ord('a')] = 1
        if guess[1][i] == 1:
            possible += [guess[0][i]]
        i += 1
    return illegal, possible

def affiche_mot_random(mots):
    """
    print un mot random de la liste
    """
    print(mots[randint(0, len(mots) - 1)])

def affiche_mot(mots):
    """
    print tous les mots
    """
    i = 0
    while i < len(mots):
        print(mots[i])
        i += 1

def affiche_combo(mots):
    affiche_mot(mots)
    print("=======")
    affiche_mot_random(mots)


def similarite(a, b):
    """
    renvoie le nombre de lettre en commun entre le mot a et b
    """
    commun = 0
    indice_ban = [0] * 5
    i = 0
    while i < len(a):
        j = 0
        while j < len(b) and (a[i] != b[j] or (indice_ban[j] == 1)):
            j += 1
        if j < len(b):
            commun += 1
            indice_ban[j] = 1
        i += 1
    return commun

def most_common(mots):
    """
    retroune l'indice du mot dans la liste de mot qui a le plus de lettre en commun avec
    tous les autres
    """
    i_max = 0
    maxi = 0
    matrice = init_matrice(len(mots), len(mots) + 1)
    i = 0
    while i < len(mots) - 1:
        j = i + 1
        somme = matrice[i][-1]
        while j < len(mots):
            sim = similarite(mots[i], mots[j])
            matrice[i][j] = sim
            matrice[j][i] = sim
            matrice[j][-1] += sim
            somme += sim
            j += 1
        matrice[i][-1] = somme
        #check max
        if somme > maxi:
            i_max = i
            maxi = somme
        i += 1
    j = 0
    return i_max

def main():
    mots = load_name("five_letter_words.txt")
    cpt = 0
    while len(mots) > 1:
        if cpt != 0:
            reco = mots[most_common(mots)]
        else:
            reco = "arose"
        affiche_combo(mots)
        print("reco:", reco)
        choix = faire_choix()
        guess = init_guess(choix)
        filtre(mots, guess)
        cpt += 1
    affiche_mot(mots)




if __name__ == "__main__":
    main()
