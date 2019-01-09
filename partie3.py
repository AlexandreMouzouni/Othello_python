from partie2 import *
import os

def creer_partie(n):
    """ Crée une partie. Une partie est un dictionnaire contenant :
    - le joueur dont c'est le tour (clé joueur) initialisé à 1,
    - le plateau (clé plateau).

    :Exemple:

    creer_partie(4) retourne un dictionnaire contenant les entrées (couples clés/valeurs) :
    - joueur : 1
    - plateau : {
        - n : 4,
        - cases : [0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]
    }
    """
    return {'joueur': 1, 'plateau': creer_plateau(n)}

def saisie_valide(partie, s):
    """ Retourne True si la chaîne s correspond à un mouvement valide pour le joueur courant,
    et False sinon.
    La chaîne s est valide si :
    - s est égal à la lettre M ou
    - s correspond à une case (de la forme a1 pour la case (0,0), ..., h8 pour la case (7,7))
      où le joueur courant peut poser son pion.

    :Exemple:

    p = creer_partie(4)
    saisie_valide(p, "M")  # retourne True
    saisie_valide(p, "b1") # retourne True
    saisie_valide(p, "b4") # return False
    """
    n = partie['plateau']['n']

    # Si s est égal a M, pas besoin de vérifier si c'est une case
    if s != 'M':
        # On vérifie la lettre
        lettre = s[0]
        valeur_lettre = ord(lettre)
        valeur_derniere_lettre = ord('a') + n - 1

        lettre = s[0]
        valeur_lettre = ord(lettre)
        valeur_derniere_lettre = ord('a') + n - 1

        if valeur_lettre >= valeur_derniere_lettre \
            or valeur_lettre < ord('a'):
            return False

        # On vérifie le chiffre
        nombre = int(s[1])
        if nombre < 1 or nombre > 8:
            return False

    return True

def tour_jeu(partie):
    """ Effectue un tour de jeu :
    - efface le terminal,
    - affiche le plateau,
    - si le joueur courant peut jouer, effectue la saisie d'un mouvement valide (saisie contrôlée),
    - Effectue le mouvement sur le plateau de jeu,
    - Retourne True si le joueur courant a joué ou False s'il souhaite accéder au menu principal.

    :Exemple:

    p = creer_partie(4)
    tour_jeu(p)
    #Si l'utilisateur a saisi b1, alors p vaut :
    { "joueur" : 1,
      "plateau" : {
        "n" : 4,
        "cases" : [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]
      }
    }
    """

    # A réparer

    def effacer_terminal():
        """ Efface le terminal. """
        os.system('clear')  # pour linux

    effacer_terminal()
    afficher_plateau(partie['plateau'])

    plateau = partie['plateau']
    joueur = partie['joueur']

    if not joueur_peut_jouer(plateau, joueur):
        return False

    s = input("saisir un mouvement ou M pour revenir au menu principale ")
    if s != "M":
        saisie = False
        while not saisie:
            if saisie_valide(partie, s):
                lettre = s[0]
                # on convertit la lette en nombre avec ord , on sait que ord(a) vaut 97
                #donc on soustrait 96  a ce nombre
                i = ord(lettre) - 96
                j = int(s[1])

                if mouvement_valide(plateau, i, j, joueur ) :
                    mouvement(plateau, i, j, joueur)
                    saisie = True

            print("La saisie est incorrecte")
            s = input("saisir un mouvement ou M pour revenir au menu principale ")
        return True
    else:
        return False

def saisir_action(partie):
    """ Retourne le choix du joueur pour menu (saisie contrôlée):
    - 0 pour terminer le jeu,
    - 1 pour commencer une nouvelle partie,
    - 2 pour charger une partie,
    - 3 pour sauvegarder une partie (si une partie est en cours),
    - 4 pour reprendre la partie (si une partie est en cours).

    :Exemple:

    n = saisir_action(None)

    n est un entier compris entre 0 et 2 inclus.
    """
    # La boucle se répête tant que l'on n'est pas sorti
    while True:
        s = input('Entrez une action:')
        entree = int(s)

        # Si la partie n'est pas vide, alors une partie est en coursw
        partie_en_cours = partie is not None

        if entree == 0:
            # Si la partie est en cours:
            # Dans le cas, l'action 0 est valide
            # Sinon, elle est invalide
            if partie_en_cours:
                return 0

        if entree == 1:
            # On ne peut commencer une partie que si il n'y a pas de
            # parties déja en cours
            if not partie_en_cours:
                return 1

        if entree == 2:
            # On peut charger une partie quand on veut
            return 2

        if entree == 3:
            # On ne peut sauvegarder une partie que si
            # elle est pas en cours
            if partie_en_cours:
                return 3

        if entree == 4:
            # on ne peut reprendre une partie que si
            # elle est en cours
            if partie_en_cours:
                return 4

def jouer(partie) :
    """ Permet de jouer à la partie en cours (passée en paramètre).
    Retourne True si la partie est terminée, False sinon.

    :Exemple:

    p = creer_partie(4)
    res = jouer(p)

    Si res vaut True, alors les deux joueurs ont fait une partie entière d'Othello
    sur une grille 4 * 4.
    """
    while True:
        # Joueur 1
        # Si tour_jeu est faux, le joueur actuel a souhaité
        # sortir du jeu pour aller dans le menu principal
        # On retourne donc false
        if not tour_jeu(partie):
            return False
        if fin_de_partie(partie['plateau']):
            return True


def test_creer_partie():
    attendu = {'joueur': 1, 'plateau': {'n': 4,
                'cases': [0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]}}
    assert creer_partie(4) == attendu

def test_saisie_valide():
    p = creer_partie(4)
    assert saisie_valide(p, "M")  # retourne True
    assert saisie_valide(p, "a1") # retourne True
    assert saisie_valide(p, "b1") # retourne True
    assert saisie_valide(p, "b4") # return False

def test_tour_jeu():
    partie = creer_partie(6)
    tour_jeu(partie)

def test_saisir_action():
    partie = creer_partie(4)
    # Premier cas: il n'y a pas de partie en cours
    #n = saisir_action(None)
    # Deuxieme cas: partie en cours
    n = saisir_action(partie)

def test_jouer():
    partie = creer_partie(6)
    jouer(partie)

if __name__ == '__main__':
    test_creer_partie()
    test_saisie_valide()
    #test_tour_jeu()
    #test_saisir_action()
    test_jouer()