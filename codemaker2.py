import itertools
import random
import numpy as np
import common



def init():
    """
    Initialise les variables utilisées par le codemaker à chaque début de partie.

    :return:
    """

    global solution, solutions_possibles

    solution = ''.join(random.choices(common.COLORS, k=common.LENGTH)) # Génère aléatoirement la solution à deviner
    solutions_possibles = common.get_permutations() # Génère l'ensemble des solutions possibles

    return



def codemaker(combinaison):
    """
    Evalue la combinaison testée en pouvant changer de solution si cela permet de rallonger la partie.

    :param combinaison: Combinaison testée par le codebreaker.
    :return: ("nombre de mots bien placés", "nombre de plots présents, mais mal placés)
    """

    global solution, solutions_possibles


    # Si le nombre de solutions possibles restant est trop grand (> sqrt(1e6)), changer la solution serait trop lourd en termes de complexité. Il y a deux boucles imbriquées sur solutions_possibles, puis une boucle pour calculer l'évaluation.
    if len(solutions_possibles) > np.sqrt(1e6):
        common.maj_possibles(solutions_possibles, combinaison, common.evaluation(combinaison, solution))

    else:

        # Version plus lisible
        nombres_solutions_possibles_apres_triches = dict() # Pour chaque solution possible avec laquelle on peut tricher, on stocke le nombre de solutions qui seront encore possibles après la triche et en tenant compte de la "combinaison" donnée en paramètre.
        for nouvelle_solution in solutions_possibles: # Pour chaque solution possible avec laquelle on peut tricher

            nombre_solutions_possibles_apres_triche = 0 # Nombre de solutions encore possibles après avoir triché
            for solution_potentielle in solutions_possibles: # Pour chaque solution qui est encore possible

                if common.evaluation(solution_potentielle, nouvelle_solution) == common.evaluation(combinaison, nouvelle_solution): # On regarde si elle est sera encore possible après la triche
                    nombre_solutions_possibles_apres_triche += 1

            nombres_solutions_possibles_apres_triches[nouvelle_solution] = nombre_solutions_possibles_apres_triche # On enregistre le nombre de solutions qui seront possibles après la triche

        solution = max(nombres_solutions_possibles_apres_triches, key=nombres_solutions_possibles_apres_triches.get) # On sélectionne la solution telle que le nombre de solutions générées est maximale

        common.maj_possibles(solutions_possibles, combinaison, common.evaluation(combinaison, solution)) # On met à jour l'ensemble des solutions possibles en tenant compte de la combinaison qui vient d'être testée par rapport à la nouvelle solution sélectionnée


        # Version condensée
        # solution = max(solutions_possibles, key=lambda nouvelle_solution: sum(1 for solution_possible in solutions_possibles if common.evaluation(solution_possible, nouvelle_solution) == common.evaluation(combinaison, nouvelle_solution)))
        # common.maj_possibles(solutions_possibles, combinaison, common.evaluation(combinaison, solution))

    return common.evaluation(combinaison, solution) # On renvoie l'évaluation de combinaison testée


def getSolution():
    """
    Renvoie la solution à deviner. Utilisé dans l'interface graphique.

    :return: Solution à deviner.
    """

    global solution

    return solution