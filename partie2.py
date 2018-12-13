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
    if not case_valide(i, j):
        return False

    pion_actuel = get_case(p, i, j)

    if get_case(i + vertical, j + horizontal) != pion_adverse(pion_actuel):
        return False

    k = 1
    while not case_valide(i + vertical*k, j + horizontal*k):
        if get_case(i + vertical*k, j + horizontal*k) == case_actuelle:
            return True
        k += 1
    return False

def test_pion_adverse():
    assert pion_adverse(1) == 2
    assert pion_adverse(2) == 1

def test_prise_possible_direction():
    assert prise_possible_direction(p,1,3,0,-1,2)  # retourne True
    assert not prise_possible_direction(p,1,3,0,-1,1)  # retourne False
    assert not prise_possible_direction(p,1,3,-1,-1,2) # retourne False
    assert prise_possible_direction(p,1,0,0,1,1)   # retourne True

if __name__ == '__main__':
    test_pion_adverse()
    test_prise_possible_direction()