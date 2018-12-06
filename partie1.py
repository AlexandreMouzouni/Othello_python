def indice_valide(plateau, indice):
    """ 
    Retourne True si indice est un indice valide de case pour le plateau
    (entre 0 et n-1)

    :Exemple:

    p = creer_plateau(8)
    indice_valide(p,0)   # retourne True
    indice_valide(p,18) # retourne False

    """

    taille = plateau['n'] - 1
    return indice >= 0 and indice < taille

def case_valide(plateau, i, j):
    """ Retourne True si (i,j) est une case du plateau (i et j sont des indices
    valides)

    :Exemple:

    p = creer_plateau(8)
    case_valide(p,3,3)  # retourne True
    case_valide(p,18,3) # retourne False
    """

    # Sachant qu'on teste sur un carré, la longeur et la largeur sont identiques.
    # On peut donc faire les mêmes comparaisons pour les deux indices.
    return indice_valide(plateau, i) and indice_valide(plateau, j)

def get_case(plateau, i, j):
    """ Retourne la valeur de la case (i,j). Erreur si (i,j) n'est pas valide.

    :Exemple:

    p = creer_plateau(4)
    get_case(p,0,0)  # retourne 0 (la case est vide)
    get_case(p,1,1)  # retourne 2 (la case contient un pion blanc)
    get_case(p,1,2)  # retourne 1 (la case contient un pion noir)
    get_case(p,18,3) # lève une erreur
    """

    # Erreur si la case n'est pas valide
    if not case_valide(plateau, i, j):
        print('erreur')
        return

    n, cases = plateau['n'], plateau['cases']

    # On interpréte le tableau linéaire comme un tableau à deux dimensions.
    # Ainsi, pour traduire la représentation (ligne, colonne) en la représentation
    # linéaire, il faudra, pour les lignes, multiplier par la longeur de la
    # ligne, ici n.
    # Pour la colonne, il faudra simplement ajouter l'indice de la colonne, car
    # colonne et avancement dans le tableau linéaire sont la même chose.
    # Autrement dit, cette formule traduit l'indice de la forme matricielle
    # a la forme linéaire, utilisée dans notre programme.
    indice = n*j + i
    return cases[indice]

def set_case(plateau, i, j, val):
    """ Affecte la valeur val dans la case (i,j). Erreur si (i,j) n'est pas une case
    ou si val n'est pas entre 0 et 2.
    Met aussi à jour le nombre de cases libres (sans pion).

    :Exemple:

    p = creer_plateau(4)
    set_case(p,0,0,1)  # met un pion noir (i.e., met la valeur 1) dans la case (0,0)
    set_case(p,1,2,0)  # enlève le pion (i.e., met la valeur 0) dans la case (1,2)
    set_case(p,18,3,1) # lève une erreur
    set_case(p,2,3,6)  # lève une erreur
    """
    # Erreur si la case n'est pas valide
    if not case_valide(plateau, i, j):
        print('erreur')
        return

    # Erreur si la valeur n'est pas valide (n'est pas entre les valeurs possible
    # prises pour les cases).
    if val < 0 or val > 2:
        print('erreur')
        return

    n, cases = plateau['n'], plateau['cases']
    # Passage matriciel --> linéaire.
    indice = n*j + i
    cases[indice] = val

    # i = 0
    # cases_libres = 0
    # while i < len(cases):
    #     if cases[i] == 0:
    #         cases_libres += 1
    #     i += 1
    # return cases_libres

    # Retourne le nombre de cases libres.
    cases_libres = 0

    # case: nom assigné à l'élement courant qui est ensuite manipulé dans la boucle.
    for case in cases:
        if case == 0:
            cases_libres += 1
    return cases_libres

def creer_plateau(n):
    """Retourne une nouvelle partie. Lève une erreur si n est différent de 4, 6 ou 8.
    Une partie est un dictionnaire contenant :
    - n : valeur passée en paramètre
    - cases : tableau de n*n cases initialisées

    :Exemple:
    creer_plateau(4) retourne un dictionnaire contenant les entrées (couples clés/valeurs) :
    - n : 4
    - cases : [0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0]
    """

    # On regarde si la taille du tableau est correcte.
    # Tuple: l'ensemble 4, 6, 8 des valeurs correctes ne sera jamais modifié et
    #        débarassé immédiatement.
    #        Ainsi, on peut utiliser un tuple pour utiliser moins de mémoire.
    # in: appartenance à un ensemble. Ici, l'ensemble des valeurs 4,6,8.
    if n not in (4, 6, 8):
        print('erreur')

    plateau = {}
    plateau['n'] = n

    cases = []
    i = 0
    while i < n:
        cases.append(0)
        i += 1

    plateau['cases'] = cases

    # On trouve les cases du milieu
    # Nous avons une longueur paire, donc la taille du milieu est de 2*2
    # L'index de la ligne et de la colonne sont les mêmes
    initial = n / 2) - 1

    # Booléen, ensuite converti en 0 ou 1 avec int
    # Il nous dira quel pion placer
    # En effet, on alterne en pion blanc et noir en commencant de
    # haut a droite pour placer les 4 du centre
    pion = True

    # Boucle imbriquée pour avoir les quatre cas possibles
    i = 0
    while i <= 1:
        j = 0
        while j <= 1:
            set_case(plateau, initial + i, initial + j, int(pion))
            # Inversion du pion
            pion = not pion
            j += 1
        i += 1

def afficher_plateau(plateau):
    """Affiche le plateau à l'écran. """

# cases = [0, 0, 0, 0,
#      0, 2, 1, 0,
#      0, 1, 2, 0,
#      0, 0, 0, 0]
#
# plateau = {'n': 4, 'cases':  [0, 0, 0, 0,
#                               0, 2, 1, 0,
#                               0, 1, 2, 0,
#                               0, 0, 0, 0] }

if __name__ == '__main__':
    p = creer_plateau(8)

    indice_valide(p, 0)  # retourne True
    indice_valide(p, 18)  # retourne False