from termcolor import colored

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
    return indice >= 0 and indice <= taille

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

    n, cases = plateau['n'], plateau['cases']

    # On interpréte le tableau linéaire comme un tableau à deux dimensions.
    # Ainsi, pour traduire la représentation (ligne, colonne) en la représentation
    # linéaire, il faudra, pour les lignes, multiplier par la longeur de la
    # ligne, ici n.
    # Pour la colonne, il faudra simplement ajouter l'indice de la colonne, car
    # colonne et avancement dans le tableau linéaire sont la même chose.
    # Autrement dit, cette formule traduit l'indice de la forme matricielle
    # a la forme linéaire, utilisée dans notre programme.
    indice = n*i + j
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

    n, cases = plateau['n'], plateau['cases']
    # Passage matriciel --> linéaire.
    indice = n*i + j
    cases[indice] = val

    # case: nom assigné à l'élement courant qui est ensuite manipulé dans la boucle.
    i = 0
    cases_libres = 0
    while i < len(cases):
        if cases[i] == 0:
            cases_libres += 1
        i += 1
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
    plateau = {}
    plateau['n'] = n

    cases = []
    i = 0
    while i < n*n:
        cases.append(0)
        i += 1

    plateau['cases'] = cases

    # On trouve les cases du milieu
    # Nous avons une longueur paire, donc la taille du milieu est de 2*2
    # L'index de la ligne et de la colonne sont les mêmes
    initial = int((n / 2) - 1)

    # Boucle imbriquée pour avoir les quatre cas possibles
    i = 0
    while i <= 1:
        j = 0
        while j <= 1:
            # Si i+j pair:
            # i et j sont les décalements des pions par rapport à
            # la case du centre en haut a gauche. Si le décalement est
            # impair, le pion change de couleur car il est directement
            # a coté.
            # Paranthèses nécéssaires, sinon j%2 direct
            if (i+j) % 2 == 1:
                pion = 1
            else:
                pion = 2
            # Boucle imbriquée
            # On va avoir les 4 cas possibles en parcourant de gauche
            # a droite et de haut en bas.
            set_case(plateau, initial + i, initial + j, pion)
            j += 1
        i += 1

    return plateau

def afficher_plateau(plateau):
    """
    Affiche le plateau.
    """
    cases, n = plateau['cases'], plateau['n']

    def ligne_nombres():
        ligne = '   '
        i = 0
        while i < n:
            ligne += '   '
            ligne += str(i+1)
            ligne += '   '
            i += 1

        return ligne

    def ligne_couleur(i):
        ligne = '   '
        j = 0
        while j < n:
            # Si i est impair, alors i+j devient impair avec j pair
            # et i+j devient pair avec j impair
            # Ainsi, cette expression inverse les resultats quand
            # i est impair
            # En effet, toutes les lignes impaires doivent commencer
            # avec du cyan et les autres avec du magenta
            # On garantit ainsi que pour i impair, la ligne commence
            # avec un cyan
            if (i+j) % 2 == 0:
                ligne += colored('       ', on_color='on_magenta')
            else:
                ligne += colored('       ', on_color='on_cyan')
            j += 1

        return ligne

    def ligne_pion(i):
        ligne = ' '
        # 97 est le code ascii pour la lettre a
        offset = 97
        # Pour la ligne 0, print a
        # Pour la ligne 1, print b, car le code de b est 98..
        ligne += chr(offset + i)
        ligne += ' '

        j = 0
        while j < n:
            pair_impair = (i+j) % 2 == 0
            if pair_impair:
                on_color = 'on_magenta'
            else:
                on_color = 'on_cyan'

            ligne += colored('  ', on_color=on_color)

            pion = get_case(plateau, i, j)
            if pion == 1:
                ligne += colored('###', color='grey', on_color=on_color)
            elif pion == 2:
                ligne += colored('###', color='white', on_color=on_color)
            else:
                ligne += colored('   ', on_color=on_color)

            ligne += colored('  ', on_color=on_color)

            j += 1

        return ligne

    # Boucle principale
    print(ligne_nombres())
    i = 0
    while i < n:
        print(ligne_couleur(i))
        print(ligne_pion(i))
        print(ligne_couleur(i))
        i += 1

## Tests
# assert: teste sur condition
def test_indice_valide():
    p = creer_plateau(4)
    assert indice_valide(p, 0)
    assert not indice_valide(p, 18)
    p = creer_plateau(8)
    assert indice_valide(p, 0)
    assert not indice_valide(p, 18)

def test_case_valide():
    p = creer_plateau(4)
    assert case_valide(p, 0, 0)
    assert not case_valide(p, 18, 1)
    p = creer_plateau(8)
    assert case_valide(p, 0, 0)
    assert case_valide(p, 7, 1)
    assert not case_valide(p, 18, 1)

def test_get_case():
    p = creer_plateau(4)
    assert get_case(p, 0, 0) == 0
    assert get_case(p, 1, 1) == 2
    assert get_case(p, 1, 2) == 1

    # Traduction linéaire -> matriciel
    p['cases'][14] = 1
    assert get_case(p, 3, 2) == 1

    p = creer_plateau(8)
    assert get_case(p, 0, 0) == 0
    assert get_case(p, 3, 3) == 2
    assert get_case(p, 3, 4) == 1

def test_set_case():
    p = creer_plateau(4)
    set_case(p, 0, 0, 1)
    assert get_case(p, 0, 0) == 1
    set_case(p, 0, 0, 0)
    assert get_case(p, 0, 0) == 0
    set_case(p, 1, 1, 2)
    assert get_case(p, 1, 1) == 2
    set_case(p, 1, 2, 1)
    assert get_case(p, 1, 2) == 1

    p = creer_plateau(8)
    set_case(p, 0, 0, 1)
    assert get_case(p, 0, 0) == 1
    set_case(p, 0, 0, 0)
    assert get_case(p, 0, 0) == 0
    set_case(p, 3, 3, 2)
    assert get_case(p, 3, 3) == 2
    set_case(p, 3, 4, 1)
    assert get_case(p, 3, 4) == 1

def test_creer_plateau():

    p = creer_plateau(4)
    # On test ce qu'il y a dans le plateau
    assert p['n'] == 4
    assert len(p['cases']) == 16
    assert get_case(p, 0, 0) == 0
    assert get_case(p, 1, 1) == 2
    assert get_case(p, 1, 2) == 1
    assert get_case(p, 2, 1) == 1
    assert get_case(p, 2, 2) == 2

    p = creer_plateau(8)
    assert p['n'] == 8
    assert len(p['cases']) == 64
    assert get_case(p, 0, 0) == 0
    assert get_case(p, 3, 3) == 2
    assert get_case(p, 3, 4) == 1
    assert get_case(p, 4, 3) == 1
    assert get_case(p, 4, 4) == 2

def test_afficher_plateau():
    p = creer_plateau(4)
    afficher_plateau(p)

    p = creer_plateau(8)
    afficher_plateau(p)

if __name__ == '__main__':
    test_indice_valide()
    test_case_valide()
    test_get_case()
    test_set_case()
    test_creer_plateau()
    test_afficher_plateau()