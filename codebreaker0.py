import random
import common
import matplotlib.pyplot as plt
import numpy as np



def init():
    """
    Initialise les variables utilisées par le codebreaker à chaque début de partie.

    :return:
    """

    return



def codebreaker(evaluation_p):
    """
    Génère une aléatoirement la combinaison à tester.

    :param evaluation_p: Evaluation de la dernière combinaison testée. Il vaut "None" si c'est la première combinaison testée de la partie.
    :return: Combinaison à tester.
    """

    return ''.join(random.choices(common.COLORS, k=common.LENGTH)) # Renvoie la combinaison à tester.