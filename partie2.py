from partie1 import *

def pion_adverse(joueur):
    """ Retourne l'entier correspondant à l'adversaire :
    - retourne 2 si joueur vaut 1,
    - retourne 1 si joueur vaut 2.
    Lève une erreur si joueur est différent de 1 et 2.
    """
    if joueur not in (1, 2):
        return False

    if joueur == 1:
        return 2
    elif joueur == 2:
        return 1

def prise_possible_direction(p, i, j, vertical, horizontal, joueur):
    """ Retourne True si le joueur peut retourner un pion adverse
    dans la direction (vertical,horizontal) en posant un pion dans la case (i,j),
    False sinon.

    :Exemple:

    p = creer_plateau(4)
    prise_possible_direction(p,1,3,0,-1,2)  # retourne True
    prise_possible_direction(p,1,3,0,-1,1)  # retourne False
    prise_possible_direction(p,1,3,-1,-1,2) # retourne False
    prise_possible_direction(p,1,0,0,1,1)   # retourne True
    """
    if joueur not in (1, 2):
        return False

    if not case_valide(p, i, j):
        return False

    if vertical == 0 and horizontal == 0:
        return False

    # On regarde dans la direction décalé de 1 si le pion à coté est de la
    # valeur opposé
    # Si c'est faux, la ligne ne peut pas être retournée
    contenu_case = get_case(p, i + vertical, j + horizontal)
    if contenu_case != pion_adverse(joueur):
        return False

    # On sait donc que le premier pion après le pion actuel
    # est de la couleur opposé, donc on regarde dans la ligne à partir du
    # deuxième pion

    # On regarde dans la ligne tous les pions suivants, en incrémentant le vecteur
    # direction de 1 à chaque fois
    k = 2
    # Si on sort du tableau, alors la prise est impossible
    # car on n'a jamais rencontré de pion de notre couleur
    while case_valide(p, i + vertical*k, j + horizontal*k):
        # contenu_case contient le contenu de la case regardée
        contenu_case = get_case(p, i + vertical*k, j + horizontal*k)
        
        # Si on recontre une vide, alors la prise est impossible
        if contenu_case == 0:
            return False
        # Si on rencontre au moins un pion de notre couleur, alors la prise est possible
        if get_case(p, i + vertical*k, j + horizontal*k) == joueur:
            return True
        k += 1
    return False

def mouvement_valide(plateau, i, j, joueur):
    """Retourne True si le joueur peut poser un pion à la case (i,j), False sinon.

    :Exemple:

    p = creer_plateau(4)
    mouvement_valide(p,1,3,2) # retourne True
    mouvement_valide(p,0,0,1) # retourne False
    """

    if not case_valide(plateau, i, j):
        return False

    # On teste pour les neuf directions possibles, c'est a dire toutes les combinaisons
    # des vecteurs entre (-1, -1) et (1, 1)
    vecteur_i = -1
    while vecteur_i <= 1:

        vecteur_j = -1
        while vecteur_j <= 1:
            # On ne teste pas pour la direction (0, 0)
            if i != 0 and j != 0:
                if prise_possible_direction(plateau, i, j, vecteur_i, vecteur_j, joueur):
                    return True

            vecteur_j += 1
        vecteur_i += 1

    # Si toute la boucle s'est faite sans que la prise soit possible, alors la prise est impossible
    return False

def mouvement_direction(plateau, i, j, vertical, horizontal, joueur):
    """ Joue le pion du joueur à la case (i,j) si c'est possible.

    :Exemple:

    p = creer_plateau(4)
    mouvement_direction(p,0,3,-1,1,2) # ne modifie rien
    mouvement_direction(p,1,3,0,-1,2) # met la valeur 2 dans la case (1,2)
    """
    # Tests de type
    if joueur not in (1, 2):
        return

    if not case_valide(plateau, i, j):
        return

    if vertical == 0 and horizontal == 0:
        return

    # Est-ce que la prise est possible?
    if not prise_possible_direction(plateau, i, j, vertical, horizontal, joueur):
        return

    set_case(plateau, i, j, joueur)

    # On sait déja, grâce a prise_possible_direction, qu'il y a au moins un pion
    # de la couleur opposé.
    # De plus, on sait qu'un pion de la même couleur nous attend à la fin
    # Il suffit alors de faire une boucle et de s'arréter quand on rencontre le
    # pion de cette même couleur
    k = 1
    while get_case(plateau, i + vertical*k, j + horizontal*k) != joueur:
        set_case(plateau, i + vertical*k, j + horizontal*k , joueur)
        k += 1

def mouvement(plateau, i, j, joueur):
    """ Ajoute le pion du joueur à la case (i,j) et met à jour le plateau.

    :Exemple:

    p = creer_plateau(4)
    mouvement(p,0,3,2) # ne modifie rien
    mouvement(p,1,3,2) # met la valeur 2 dans les cases (1,2) et (1,3)
    """

    # Teste de types
    if not case_valide(plateau, i, j):
        return False

    if joueur not in (1, 2):
        return False

    # On teste pour les neuf directions possibles, c'est a dire toutes les combinaisons
    # des vecteurs entre (-1, -1) et (1, 1)
    vecteur_i = -1
    while vecteur_i <= 1:

        vecteur_j = -1
        while vecteur_j <= 1:
            # On ne teste pas pour la direction (0, 0)
            if i != 0 and j != 0:
                mouvement_direction(plateau, i, j, vecteur_i, vecteur_j, joueur)

            vecteur_j += 1
        vecteur_i += 1

def joueur_peut_jouer(plateau, joueur):
    """ Retourne True s'il existe une case sur laquelle le joueur peut jouer, False sinon.

    :Exemple:

    p = creer_plateau(4)
    joueur_peut_jouer(p,1) # retourne True
    # On remplace les pions du joueur 2 par des pions du joueur 1
    set_case(p,1,1,1)
    set_case(p,2,2,1)
    joueur_peut_jouer(p,1) # retourne False
    """
    i = 0
    while i < plateau['n']:
        j = 0
        while j < plateau['n']:
            #test si la case est vide
            if plateau['cases'][i] == 0:
                #test si c'est possible de placer le pion
                if mouvement_valide(plateau, i, j, joueur):
                    return True
            j += 1
        i += 1
    return False

def fin_de_partie(plateau):
    """ Retourne True si la partie est finie, 0 sinon.

       :Exemple:

       p = creer_plateau(4)
       fin_de_partie(p) # retourne False
       # On remplace les pions du joueur 2 par des pions du joueur 1
       set_case(p,1,1,1)
       set_case(p,2,2,1)
       fin_de_partie(p) # retourne True
    """
    i = 0
    while i < plateau['n']:
        j = 0
        while j < plateau['n']:
            if plateau['cases'][i] == 0 :
                #test si le mouvement est possible pour chacun des joueur
                if mouvement_valide(plateau, i , j , 1) \
                or mouvement_valide(plateau, i , j , 2):
                    return 0
            j += 1
        i += 1

    return True

def gagnant(plateau):
    """ Retourne :
    - 2 si le joueur 2 a plus de pions que le joueur 1,
    - 1 si le joueur 1 a plus de pions que le joueur 2,
    - 0 si égalité.

    :Exemple:

    p = creer_plateau(4)
    # On remplace les pions du joueur 2 par des pions du joueur 1
    set_case(p,1,1,1)
    set_case(p,2,2,1)
    gagnant(p) # retourne 1
    """
    i=0
    pions_joueur_1 = 0
    pions_joueur_2 = 0
    # on itere sur le tableau puis on compte les pions de chaque joueur
    while i < len(plateau['cases']):
        if plateau['cases'][i] == 1 :
            pions_joueur_1 += 1
        elif plateau['cases'][i] == 2 :
            pions_joueur_2 += 1
        i += 1

    if pions_joueur_1 > pions_joueur_2 :
        return 1
    elif pions_joueur_1 < pions_joueur_2 :
        return 2
    else :
        return 0

def test_pion_adverse():
    assert pion_adverse(1) == 2
    assert pion_adverse(2) == 1

def test_prise_possible_direction():
    p = creer_plateau(4)
    # Blanc placé en bas, capture de 1 pion noir avec blanc à la fin
    assert prise_possible_direction(p,3,1,-1,0,2)
    # noir place  en bas en cas ou le au cas ou le pion est de la couleur oppose
    assert prise_possible_direction(p, 3 , 2 , -1,0,1)
    # test pour une diagonale pour capture de 1 pion
    set_case(p , 2, 2, 1)
    assert prise_possible_direction(p , 3, 3 ,-1 , -1, 2)
    # test pour une diagonale si la direction sort du plateau
    assert not prise_possible_direction(p , 3,3 , 1 , 1 , 2)
    assert not prise_possible_direction(p , 0, 1 , 1 , 0 , 2)
    set_case(p , 0 , 2, 2)
    #test pour un blanc place en bas capture pour une multitude de pions
    assert prise_possible_direction(p , 3 , 2 , -1 , 0, 2)
    #test pour traverser sans trouver de pion de la meme couleur
    # Traverse uniquement sur des noirs
    set_case(p , 0 , 2 , 1)
    assert not prise_possible_direction(p , 3 , 2 , -1 , 0 , 2)
    # Test pour traverser sans pions de la même couleur, en rencontrant un vide
    set_case(p , 1 , 2 , 0)
    assert not prise_possible_direction(p , 3 , 2 , -1 , 0 , 2)

    # Test si la direction est (0, 0)
    assert not prise_possible_direction(p , 1, 1, 0, 0 , 2)
    # Test pour case invalide
    assert not prise_possible_direction(p, 14, 14, 0, 0, 2)
    # Test pour joueur invalide
    assert not prise_possible_direction(p, 0, 0, 0, 0, 14)

def test_mouvement_valide():
    p = creer_plateau(4)
    assert mouvement_valide(p,1,3,2) # retourne True
    assert not mouvement_valide(p,0,0,2) # retourne False

    # Test de type
    assert not mouvement_valide(p, 13, 13, 1)

def test_mouvement_direction():
    p = creer_plateau(4)
    # Remplace un pion déja placé
    mouvement_direction(p,1, 2, -1, 0, 2)
    assert p['cases'] == [0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]
    # Place un pion blanc en 3, 1 avec une fausse direction
    mouvement_direction(p,3, 1, -1, -1, 2)
    assert p['cases'] == [0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]
    # Place un pion blanc en 3, 1 avec une direction correcte
    mouvement_direction(p,3, 1, -1, 0, 2)
    assert p['cases'] == [0, 0, 0, 0, 0, 2, 1, 0, 0, 2, 2, 0, 0, 2, 0, 0]

    # Tests de types
    mouvement_direction(p,-1, -1, 0, 0, 1)
    assert p['cases'] == [0, 0, 0, 0, 0, 2, 1, 0, 0, 2, 2, 0, 0, 2, 0, 0]
    mouvement_direction(p,0, 0, 0, 0, 17)
    assert p['cases'] == [0, 0, 0, 0, 0, 2, 1, 0, 0, 2, 2, 0, 0, 2, 0, 0]
    mouvement_direction(p,0, 0, 17, 17, 0)
    assert p['cases'] == [0, 0, 0, 0, 0, 2, 1, 0, 0, 2, 2, 0, 0, 2, 0, 0]

def test_mouvement():
    p = creer_plateau(4)
    # Tests de type
    assert not mouvement(p, 17, 17, 0)
    assert not mouvement(p, 0, 0, 17)

    mouvement(p, 0, 3, 2)  # ne modifie rien
    assert p['cases'] == [0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]
    mouvement(p, 1, 3, 2)  # met la valeur 2 dans les cases (1, 2) et (1, 3)
    assert p['cases'] == [0, 0, 0, 0, 0, 2, 2, 2, 0, 1, 2, 0, 0, 0, 0, 0]

def test_joueur_peut_jouer():
    p = creer_plateau(4)
    assert joueur_peut_jouer(p, 1)  # retourne True
    # On remplace les pions du joueur 2 par des pions du joueur 1
    set_case(p, 1, 1, 1)
    set_case(p, 2, 2, 1)
    assert not joueur_peut_jouer(p, 1)  # retourne False

def test_fin_de_partie():
    p = creer_plateau(4)
    assert fin_de_partie(p) == 0  # retourne  0
    # On remplace les pions du joueur 2 par des pions du joueur 1
    set_case(p, 1, 1, 1)
    set_case(p, 2, 2, 1)
    assert fin_de_partie(p)  # retourne True

    # Test si le plateau est plein
    i = 0
    while i < p['n']:
        j = 0
        while j < p['n']:
            set_case(p, i, j, 1)
            j += 1
        i += 1

    assert fin_de_partie(p)

def test_gagnant():
    p = creer_plateau(4)
    # On remplace les pions du joueur 2 par des pions du joueur 1
    set_case(p, 1, 1, 1)
    set_case(p, 2, 2, 1)
    assert gagnant(p) == 1  # retourne 1
    set_case(p, 1, 1, 2)
    set_case(p, 2, 2, 2)
    assert gagnant(p) == 0
    set_case(p, 2, 1, 2)
    set_case(p, 2, 2, 2)
    assert gagnant(p) == 2
    set_case(p, 1, 1, 0)
    set_case(p, 2, 2, 0)
    assert gagnant(p) == 0

if __name__ == '__main__':
    test_pion_adverse()
    test_prise_possible_direction()
    test_mouvement_valide()
    test_mouvement_direction()
    test_mouvement()
    test_joueur_peut_jouer()
    test_fin_de_partie()
    test_gagnant()