import random
import common

def init():
    """
    Initialise les variables utilisées par le codebreaker à chaque début de partie.

    :return:
    """

    global solutions_possibles, derniere_combinaison_testee

    solutions_possibles = None # Enregistre l'ensemble des solutions possibles encore possible
    derniere_combinaison_testee = None # Enregistre la dernière combinaison testée

    return


def codebreaker(evaluation_p):
    """
    Génère une aléatoirement la combinaison à tester parmi celles qui sont susceptibles d'être solution.

    :param evaluation_p: Evaluation de la dernière combinaison testée. Il vaut "None" si c'est la première combinaison testée de la partie.
    :return: Combinaison à tester.
    """

    global solutions_possibles, derniere_combinaison_testee

    if evaluation_p is None: # Si le codebreaker n'a pas encore joué
        derniere_combinaison_testee = ''.join(random.choices(common.COLORS, k=common.LENGTH)) # Génère aléatoirement la première combinaison à tester

    else:
        
        if solutions_possibles is None: # Si une seule tentative a déjà été faite
            solutions_possibles = common.donner_possibles(derniere_combinaison_testee, evaluation_p) # Génère l'ensemble des solutions possibles en tenant compte de cette première tentative
        else:
            common.maj_possibles(solutions_possibles, derniere_combinaison_testee, evaluation_p) # Met à jour l'ensemble des solutions possibles en tenant compte de la tentative précédente

        if solutions_possibles:
            derniere_combinaison_testee = random.choice(list(solutions_possibles)) # Sélectionne aléatoirement la combinaison à tester parmi celles qui sont susceptibles d'être solution

    return derniere_combinaison_testee # Renvoie la combinaison à tester