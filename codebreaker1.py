import random
import common
import matplotlib.pyplot as plt
import numpy as np

def init():
    """
    Initialise les variables utilisées par le codebreaker à chaque début de partie.

    :return:
    """

    global combinaisons_testees

    combinaisons_testees = set() # Enregistre les combinaisons testées depuis le début de la partie

    return


def codebreaker(evaluation_p):
    """
    Génère une aléatoirement la combinaison à tester parmi celles pas encore testées.

    :param evaluation_p: Evaluation de la dernière combinaison testée. Il vaut "None" si c'est la première combinaison testée de la partie.
    :return: Combinaison à tester.
    """

    global combinaisons_testees

    combinaison = ''.join(random.choices(common.COLORS, k=common.LENGTH)) # Génère aléatoirement une combinaison

    while combinaison in combinaisons_testees: # Tant que la combinaison a déjà été testée
        combinaison = ''.join(random.choices(common.COLORS, k=common.LENGTH)) # Re-génère aléatoirement une combinaison
    combinaisons_testees.add(combinaison) # Enregistre cette combinaison comme testée

    return combinaison # Renvoie la combinaison à tester.