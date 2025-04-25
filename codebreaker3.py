import itertools
import random
import common
from semestre2.Projet.common import donner_possibles


def init():
    """
    Initialise les variables utilisées par le codebreaker à chaque début de partie.

    :return:
    """

    global solutions_possibles, dernière_combinaison_testée

    solutions_possibles = None  # Enregistre l'ensemble des solutions possibles encore possible
    dernière_combinaison_testée = None  # Enregistre la dernière combinaison testée

    return



def codebreaker(evaluation_p):
    """
    Génère une aléatoirement la combinaison à tester en tenant compte du moins pire des cas si jamais le codemaker change de solution.

    Par exemple :
        - Permutations : {a, b, c, d}
        - Solutions possibles : {a, b, c}
        - Solution actuelle : a

        On admet que les solutions possibles évoluent de telle manière :

        - Si le codebreaker teste a :
            - Si le codemaker change de solution et choisi b, les solutions possibles deviendront : {b} [1]
            - Si le codemaker change de solution et choisi c, les solutions possibles deviendront : {c} [1]
            Le pire des cas est alors un ensemble de solutions possibles de taille 1.

        - Si le codebreaker teste b :
            - Si le codemaker ne change pas de solution a, les solutions possibles deviendront : {a, c} [2]
            - Si le codemaker change de solution et choisi c, les solutions possibles deviendront : {c} [1]
            Le pire des cas est alors un ensemble de solutions possibles de taille 2.

        - Si le codebreaker teste c :
            - Si le codemaker ne change pas de solution a, les solutions possibles deviendront : {a} [1]
            - Si le codemaker change de solution et choisi b, les solutions possibles deviendront : {b, a} [2]
            Le pire des cas est alors un ensemble de solutions possibles de taille 2.

        - Si le codebreaker teste d :
            - Si le codemaker ne change pas de solution a, les solutions possibles deviendront : {a} [1]
            - Si le codemaker change de solution et choisi b, les solutions possibles deviendront : {b} [1]
            - Si le codemaker change de solution et choisi c, les solutions possibles deviendront : {a, b, c} [3]
            Le pire des cas est alors un ensemble de solutions possibles de taille 3.

        Le codebreaker va donc tester "a" puisque c'est la tentative qui va minimiser le pire des cas : quelque-soit le changement de solution du codemaker, on aura au maximum 1 solution possible.

        Remarque : Si c'était la tentative "d" qui minimiserait l'ensemble des solutions possibles, alors on aurait essayé "d".


    :param evaluation_p: Evaluation de la dernière combinaison testée. Il vaut "None" si c'est la première combinaison testée de la partie.
    :return: Combinaison à tester.
    """

    global solutions_possibles, dernière_combinaison_testée

    if evaluation_p is None:  # Si le codebreaker n'a pas encore joué
        dernière_combinaison_testée = ''.join(random.choices(common.COLORS, k=common.LENGTH))  # Génère aléatoirement la première combinaison à tester

    else:

        if solutions_possibles is None:  # Si une seule tentative a déjà été faite
            solutions_possibles = common.donner_possibles(dernière_combinaison_testée, evaluation_p)  # Génère l'ensemble des solutions possibles en tenant compte de cette première tentative
        else:
            common.maj_possibles(solutions_possibles, dernière_combinaison_testée, evaluation_p)  # Met à jour l'ensemble des solutions possibles en tenant compte de la tentative précédente

        if len(solutions_possibles) == 1: # S'il n'y a plus que la solution dans l'ensemble des solutions possible
            dernière_combinaison_testée = next(iter(solutions_possibles)) # On sélectionne cet solution

        else:

            # Version plus lisible
            permutation__pire_nombre_solutions_possibles = dict() # Pour chaque permutation, on enregistre le pire nombre de solutions possibles en tenant compte des triches possibles
            for permutation in common.get_permutations(): # Pour chaque permutation

                nombres_solutions_possibles_apres_triches = [] # Liste telle que son i-ème élément est le nombre de solutions encore possible après que le i-ème élément des solutions possibles soit choisi comme nouvelle solution
                for nouvelle_solution in solutions_possibles: # Pour chaque solution que le codemaker pourrait définir comme nouvelle solution

                    nombre_solutions_possibles_apres_triche = 0 # Nombre de solutions possibles après la i-ème triche
                    for solution_potentielle in solutions_possibles: # Pour chaque solution potentiellement encore possible après triche

                        if common.evaluation(solution_potentielle, permutation) == common.evaluation(permutation, nouvelle_solution): # Si la solution potentielle est bien encore possible
                            nombre_solutions_possibles_apres_triche += 1 # Augmente le nombre de solutions possible après la i-ème triche

                    nombres_solutions_possibles_apres_triches.append(nombre_solutions_possibles_apres_triche) # Enregistre le nombre de solutions possibles après la i-ème triche

                permutation__pire_nombre_solutions_possibles[permutation] = max(nombres_solutions_possibles_apres_triches) # Récupère le pire nombre de solutions possibles après la i-ème triche

            # Version condensée
            # permutation__pire_nombre_solutions_possibles = {permutation: max([sum([1 for solution_potentielle in solutions_possibles if common.evaluation(solution_potentielle, permutation) == common.evaluation(permutation, nouvelle_solution)]) for nouvelle_solution in solutions_possibles]) for permutation in permutation__pire_nombre_solutions_possibles}

            dernière_combinaison_testée = min(permutation__pire_nombre_solutions_possibles, key=permutation__pire_nombre_solutions_possibles.get) # Récupère la permutation telle que, si on triche, on minimise le pire nombre de solutions possibles qu'il restera en prenant en compte que le codemaker peut changer de solution

    return dernière_combinaison_testée # Renvoie la combinaison à tester