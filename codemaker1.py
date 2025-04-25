import random
import common


def init():
    """
    Initialise les variables utilisées par le codemaker à chaque début de partie.

    :return:
    """

    global solution

    solution = ''.join(random.choices(common.COLORS, k=common.LENGTH)) # Génère aléatoirement la solution à deviner

    return



def codemaker(combinaison):
    """
    Evalue la combinaison testée.

    :param combinaison: Combinaison testée par le codebreaker.
    :return: ("nombre de mots bien placés", "nombre de plots présents, mais mal placés")
    """

    global solution

    return common.evaluation(solution, combinaison) # On renvoie l'évaluation de la combinaison testée.


def getSolution():
    """
    Renvoie la solution à deviner. Utilisé dans l'interface graphique.

    :return: Solution à deviner.
    """

    global solution

    return solution