from partie2 import *
from json import dumps, loads
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
    plateau = partie['plateau']
    joueur = partie['joueur']

    # Si s est égal a M, pas besoin de vérifier si c'est une case
    if s == 'M':
        return True

    # Sécurité sur la chaîne
    if len(s) != 2:
        return False

    # Sécurité sur le nombre (pas de conversion erronée)
    # Si ce n'est PAS dans ord(1).. ord(9)
    if ord(s[1]) < ord('1') or ord(s[1]) > ord('9'):
        return False

    # On vérifie la lettre
    i = ord(s[0]) - ord('a')
    j = int(s[1]) - 1

    #if not case_valide(plateau, i, j):
    #    return False

    # Le mouvement est-il valide?
    if not mouvement_valide(plateau, i, j, joueur):
        return False

    return True

def nom_j(joueur):
    if joueur == 1:
        return "Noir"
    else:
        return "Blanc"

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

    def effacer_terminal():
        """ Efface le terminal. """
        os.system('clear')  # pour linux

    effacer_terminal()
    afficher_plateau(partie['plateau'])

    plateau = partie['plateau']
    joueur = partie['joueur']

    # Si personne ne peut jouer, la fonction est fausse
    if not joueur_peut_jouer(plateau, joueur):
        return False

    # Si un des deux joueurs ne peut pas jouer, on saute son tour
    if not joueur_peut_jouer(plateau, joueur):
        print('Le joueur', joueur, 'ne peut pas jouer, on saute son tour')
        partie['joueur'] = pion_adverse(joueur)

    # Boucle de mouvement
    print('C\'est au tour de', nom_j(joueur))
    proposition_coup(partie)
    s = input("Saisir un mouvement ou M pour revenir au menu principal")
    # Si le joueur veut sortir, on retourne au menu
    if s == "M":
        return False

    while not saisie_valide(partie, s):
        print("La saisie est incorrecte")
        s = input("Saisir un mouvement ou M pour revenir au menu principal")
        if s == "M":
            return False

    # La saisie est correcte, on effectue le mouvement et on retourne True
    i = ord(s[0]) - ord('a')
    j = int(s[1]) - 1
    mouvement(plateau, i, j, joueur)
    # Dans l'état du jeu, on change de joueur
    # Cela nous permet dans le graphe des états de changer d'un état à un autre
    # uniquement avec la fonction tour_jeu
    partie['joueur'] = pion_adverse(joueur)
    return True

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

        # Si la partie n'est pas vide, alors une partie est en cours
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
        if not tour_jeu(partie):
            if fin_de_partie(partie['plateau']):
                return True
            else:
                return False

def saisir_taille_plateau():
    """ Fait saisir un nombre parmi 4,6 ou 8 (saisie contrôlée).
    :Exemple:
    n = saisir_taille_plateau()
    n est un entier égal à 4, 6 ou 8.
    """
    n = input("Saisissez la taille du plateau [4, 6, 8]")
            
    if len(n) == 1:
        if ord(n) >= ord('1') or ord(n) <= ord('9'):
            n = int(n)

    saisie_valide_jouer = (4 , 6 , 8)
    while n not in saisie_valide_jouer:
        n = input("Saisissez la taille du plateau [4, 6, 8]")
        
        if len(n) == 1:
            if ord(n) >= ord('1') or ord(n) <= ord('9'):
                n = int(n)


    return n

def sauvegarder_partie(partie):
    """ Sauvegarde la partie passée en paramètre au format json
    dans le fichier sauvegarde_partie.json
    :Exemple:
    p = creer_partie(4)
    sauvegarder_partie(p)
    Le fichier sauvegarde_partie.json doit contenir :
    {"joueur": 1, "plateau": {"n": 4, "cases": [0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 0,
    0, 0, 0, 0]}}
    """
    s = dumps(partie)
    f = open("sauvegarde_partie.json", "w")
    f.write(s)
    f.close()

def charger_partie():
    """ Crée la partie à partir des données du fichier sauvegarde_partie.json
    ou crée une nouvelle partie 4*4.
    Retourne la partie créée.
    :Exemple:
    p = charger_partie()
    Si le fichier sauvegarde_partie.json contient :
    {"joueur": 1, "plateau": {"n": 4, "cases": [0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 0,
    0, 0, 0, 0]}}
    alors p correspond à une nouvelle partie
    """
    f  = open("sauvegarde_partie.json", "r")
    s = f.read()
    f.close()

    partie = loads(s)

    return partie

def othello():
    """ Fonction permettant de jouer à Othello. On peut enchaîner, sauvegarder,
    charger et recommencer des parties d'Othello.
    :Exemple:
    othello()
    """
    def menu(partie):
        action = saisir_action(partie)

        if action == 0:
            # On vide la partie, puis on revient au menu
            # pour laisser l'utilisateur faire ce qu'il veut
            # Si partie == None, la partie est finie et rien n'est en cours
            partie = None
            # Appel récursif
            partie = menu(partie)

        if action == 1 :
            n = saisir_taille_plateau()
            partie = creer_partie(n)

        if action == 2 :
            partie = charger_partie()

        if action == 3:
            sauvegarder_partie(partie)
        # ne sert a rien de faire if action == 4 , car on ne modifie pas l'etat

        return partie


    n = saisir_taille_plateau()
    partie = creer_partie(n)
    while True :
        # on met tour_jeu dans un if , il sera donc appeler a chaque tour de boucle
        if tour_jeu(partie) == False :
            if fin_de_partie(partie["plateau"]):
                winneur = gagnant(partie["plateau"])
                print('Le gagnant est', nom_j(winneur))
                partie = None
            partie = menu(partie)

#######################################
# Défi algorithmique

def proposition_coup(partie):
    """ Calcule sur le plateau quel coup prendrait le plus de pions """
    plateau = partie['plateau']
    n = partie['plateau']['n']

    # Premiere passe: récupérer tous les coups possibles
    liste_coups = []
    i = 0
    while i < n:
        j = 0
        while j < n:
            if mouvement_valide(plateau, i, j, partie['joueur']):
                liste_coups.append( (i,j) )
            j += 1
        i += 1

    meilleur_coup = liste_coups[0]
    meilleur_coup_pions = 0
    # Pour chaque coup, tester...
    i = 0
    while i < len(liste_coups):
        ci, cj = liste_coups[i][0], liste_coups[i][1]
        total_coup = 0

        #... dans chaque direction...
        vecteur_i = -1
        while vecteur_i <= 1:
            vecteur_j = -1
            while vecteur_j <= 1:

                if vecteur_i != 0 or vecteur_j != 0:
                    # ..si la prise est possible:
                    if prise_possible_direction(plateau, ci, cj, \
                                                vecteur_i, vecteur_j, partie['joueur']):
                        k = 1
                        while case_valide(plateau, ci + vecteur_i * k, cj + vecteur_j * k) \
                            and get_case(plateau, ci + vecteur_i * k, cj + vecteur_j * k) != partie['joueur']:
                            k += 1

                        # k représente le nombre de pions possibles à prendre dans
                        # la direction
                        # On ajoute ca pour chaque direction à total_coup
                        total_coup += k
                vecteur_j += 1
            vecteur_i += 1

        # Si ce total de pions prit dans la direction est le meilleur, mettre a jour
        # meilleur coup
        if total_coup > meilleur_coup_pions:
            meilleur_coup = liste_coups[i]
            meilleur_coup_pions = total_coup

        i += 1

    i = chr(97 + meilleur_coup[0])
    j = meilleur_coup[1] + 1
    print('Coup proposé par l\'ordinateur:', str(i)+str(j))

def test_creer_partie():
    attendu = {'joueur': 1, 'plateau': {'n': 4,
                'cases': [0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]}}
    assert creer_partie(4) == attendu

def test_saisie_valide():
    p = creer_partie(4)
    assert saisie_valide(p, "M")  # retourne True
    print('Test', mouvement_valide(p['plateau'], 0, 1, 1))
    print('Prise', prise_possible_direction(p['plateau'], 0, 1,   1, 0,  1))
    afficher_plateau(p['plateau'])
    print("Saisie", saisie_valide(p, "a2")) # retourne True

def test_tour_jeu():
    partie = creer_partie(6)
    tour_jeu(partie)

def test_saisir_action():
    partie = creer_partie(4)
    # Premier cas: il n'y a pas de partie en cours
    # n = saisir_action(None)
    # Deuxieme cas: partie en cours
    n = saisir_action(partie)

def test_jouer():
    partie = creer_partie(6)
    jouer(partie)

if __name__ == '__main__':
    #test_creer_partie()
    #test_saisie_valide()
    #test_tour_jeu()
    #test_saisir_action()
    #test_jouer()
    othello()
