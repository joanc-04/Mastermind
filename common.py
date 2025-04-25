import itertools
import sys

LENGTH = 4 # Nombre de plots dans une combinaison
COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G'] # Couleurs possibles dans une combinaison
memo_evaluations = dict() # Enregistre les évaluations faites (principe de mémoisation)



def evaluation(combinaison, reference):
    """
    Évalue une combinaison testée par rapport à une combinaison de référence.
    Elle compte le nombre de plots bien placés, ainsi que le nombre de plots présents, mais mal placés.

    :param combinaison: Combinaison testée par le codebreaker.
    :param reference: Combinaison de référence.
    :return: ("nombre de plots bien placés", "nombre de plots présents, mais mal placés")
    """

    global memo_evaluations

    if len(reference) != len(combinaison): # Si la solution et de la combinaison testée n'ont pas la même taille, alors on renvoie une erreur.
        return "Erreur : les deux combinaisons n'ont pas la même longueur"

    if (eval := memo_evaluations.get((combinaison, reference)) or memo_evaluations.get((reference, combinaison))) is not None: # Si l'évaluation a déjà été calculée, on la renvoie directement. Il y a symétrie de la fonction évaluation.
        return eval

    nombre_plots_bien_places = nombre_plots_mal_places = 0 # Compte le nombre de plots bien placés, et ceux présents, mais mal placé

    plots_reference_non_trouves = [] # Plots présents dans la combinaison de référence, mais non trouvés.
    plots_combinaison_non_trouves = [] # Plots présents dans la combinaison testée tels que le i-ème plot de la combinaison testée soit différent du i-ème plot de la référence.

    for i, plot in enumerate(combinaison): # Pour chaque plot de la combinaison testée.
        if reference[i] == plot: # Si le i-ème plot de la combinaison est bien placé
            nombre_plots_bien_places += 1
        else:
            plots_combinaison_non_trouves.append(plot) # Enregistre i-ème plot de la combinaison qui est une erreur
            plots_reference_non_trouves.append(reference[i]) # Enregistre le i-ème plot de la référence qui n'a pas été trouvé

    for i, plot in enumerate(plots_combinaison_non_trouves): # Pour chaque erreur de la combinaison
        if plot in plots_reference_non_trouves: # Si ce plot est présent dans la référence, mais mal placé
            nombre_plots_mal_places += 1
            plots_reference_non_trouves.remove(plot) # Enlève le plot des solutions non trouvées pour ne pas le prendre en compte deux fois

    eval = memo_evaluations[(combinaison, reference)] = memo_evaluations[(reference, combinaison)] = nombre_plots_bien_places, nombre_plots_mal_places # Enregistre l'évaluation trouvée pour la mémoisation

    return eval # Renvoie l'évaluation


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    DEBUT TESTS - QUESTION 1
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def test_evaluation():

    tests = [
        # (combinaison, solution, résultat attendu)
        ("RGBY", "RGB", "Erreur : les deux combinaisons n'ont pas la même longueur"),  # "Erreur
        ("RGBY", "RGBY", (4, 0)),  # Tout est bien placé
        ("RGBY", "YBGR", (0, 4)),  # Tout est mal placé
        ("RGBY", "RBGY", (2, 2)),  # Deux bien placés, deux mal placés
        ("RRBB", "BBRR", (0, 4)),  # Deux couleurs inversées
        ("RRGG", "RRBB", (2, 0)),  # Deux bien placés, pas de mal placés
        ("RRGG", "GGRR", (0, 4)),  # Tout mal placé
        ("AAAA", "BBBB", (0, 0)),  # Aucune correspondance
    ]

    for combinaison, solution, resultat_attendu in tests:
        resultat = evaluation(combinaison, solution)
        assert resultat == resultat_attendu, f"Échec : {combinaison} - {solution}, attendu {resultat_attendu}, obtenu {resultat}"

    print("Tous les tests ont réussi !")

# Si on n'obtient pas le résultat attendu, alors il y a une erreur.
# test_evaluation() # A DE-COMMENTER

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    FIN TESTS - QUESTION 1
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def evaluation_partielle(combinaison, reference):
    """
    Évalue partiellement la combinaison testée par rapport à une combinaison de référence.
    Cette évaluation ne prend en compte uniquement les plots bien placés, mais pas les plots présents, mais mal placés.

    :param combinaison: Combinaison testée par le codebreaker.
    :param reference: Combinaison de référence.
    :return: ("nombre de mots bien placés", "nombre de plots présents, mais mal placés = 0")
    """

    if len(reference) != len(combinaison): # Si la taille de la solution est différente de celle de la solution, alors on renvoie une erreur.
        return "Erreur : les deux combinaisons n'ont pas la même longueur"

    nombre_plots_bien_placés = 0  # Nombre de plots bien placés

    for i, plot in enumerate(combinaison): # Pour chaque plot de la combinaison testée
        if plot == reference[i]: # Si le i-ème plot de la combinaison est bien placé
            nombre_plots_bien_placés += 1

    return nombre_plots_bien_placés, 0 # Renvoie l'évaluation


def get_permutations(element=None, taille=None):

    global COLORS, LENGTH

    if not element: element = COLORS
    if not taille: taille = LENGTH

    # Méthode 1 : On utilise la bibliothèque itertools.
    # return set([''.join(permutation) for permutation in itertools.product(COLORS, repeat=LENGTH)])

    # Méthode 2 : Méthode itérative sans bibliothèque.
    permutations = set(element) # Initialise l'ensemble des permutations comme l'ensemble des éléments possibles (aucun produit cartésien n'a encore été fait)
    for _ in range(taille - 1): # Pour chaque produit cartésien (on en fait taille - 1).
        maj_permutations = set()
        for permutation in permutations: # Pour chaque permutation en cours de construction
            for e in element: # Pour chaque élément possible
                maj_permutations.add(permutation + e) # Continue de construire la permutation en ajoutant un élément
        permutations = maj_permutations # Met à jour l'ensemble des permutations en cours de construction

    return permutations # Renvoie l'ensemble des permutations

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                        DEBUT TESTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# On teste le fonctionnement de get_permutations()

# permutations = get_permutations()
# print(permutations)
# print(len(permutations))
# On obtient bien 4096 combinaisons possibles pour : len(éléments) = 8 ; taille = 4.

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                        FIN TESTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def donner_possibles(combinaison, evaluation_combinaison):
    """
    Détermine l'ensemble des solutions possibles après la première tentative et en tenant compte de son évaluation.

    :param combinaison: Première tentative
    :param evaluation_combinaison: Evaluation de la première tentative
    :return: Ensemble des solutions possibles
    """

    solutions_possibles = set() # Enregistre l'ensemble des solutions possibles
    permutations = get_permutations() # Récupère toutes les permutations (chacune des combinaisons qu'on peut tester)

    for permutation in permutations: # Pour chaque permutation
        if evaluation(permutation, combinaison) == evaluation_combinaison: # Si la permutation est potentiellement la solution
            solutions_possibles.add(permutation) # Enregistre cette permutation dans les solutions possibles

    return solutions_possibles # Renvoie l'ensemble des solutions possibles


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    DEBUT TESTS - QUESTION 5
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# IL FAUT BIEN RE-COMMENTER TOUTES LES LIGNES DE LA PARTIE TESTS UNE FOIS LES TESTS FINIS !!!

# LENGTH = 4 # Nombre de plots dans une combinaison
# COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G'] # Couleurs possibles dans une combinaison

# permutations = get_permutations()
# print(len(permutations), permutations) # On obtient bien 4096 combinaisons possibles.


# LENGTH = 3
# COLORS = ["R", "G", "B"]

# print(donner_possibles("RBG", (1, 2))) # On doit obtenir {'BRG', 'GBR', 'RGB'} (1 est bien placé, il faut inverser les deux autres lettres)
# print(donner_possibles("RBG", (2, 0))) # On doit obtenir {'RGG', 'BBG', 'RBR', 'RBB', 'GBG', 'RRG'}
# print(donner_possibles("RBG", (2, 1))) # On doit obtenir set()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    FIN TESTS - QUESTION 5
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def maj_possibles(solutions_possibles, combinaison, evaluation_combinaison):
    """
    Met à jour l'ensemble des solutions possibles après une tentative et en tentant compte de son évaluation.

    :param solutions_possibles: Ensemble des solutions possibles
    :param combinaison: Tentative
    :param evaluation_combinaison: Evaluation de la tentative
    :return:
    """

    for solution_possible in solutions_possibles.copy(): # Pour chacune des solutions possibles
        if evaluation(combinaison, solution_possible) != evaluation_combinaison: # Si cette solution possible ne l'est plus
            solutions_possibles.remove(solution_possible) # Enlève cette solution des solutions possibles


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    DEBUT TESTS - QUESTION 6
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# IL FAUT BIEN RE-COMMENTER TOUTES LES LIGNES DE LA PARTIE TESTS UNE FOIS LES TESTS FINIS !!!

# LENGTH = 3
# COLORS = ["R", "G", "B"]

# solutions_possibles = get_permutations()
# maj_possibles(solutions_possibles, "RBG", (1, 2))
# print(solutions_possibles) # On doit obtenir {'BRG', 'GBR', 'RGB'}

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    FIN TESTS - QUESTION 6
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""