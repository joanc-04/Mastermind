import common

def check_codemaker(nom_fichier_log):
    """
    Vérifie si le codemaker a changé de solution au cours de la partie.

    :param nom_fichier_log: Fichier logs de la partie.
    :return: Si le codemaker a triché ou non
    """

    with open(nom_fichier_log, 'r') as file: # Ouvre le fichier logs et récupère les lignes
        lines = file.readlines()

    tentatives = [(lines[i][:-1], lines[i + 1][:-1]) for i in range(0, len(lines), 2)]
    solution = tentatives[-1]

    assert int(solution[1][0]) >= common.LENGTH, "La partie n'est pas encore terminée." # Renvoie une erreur si la partie n'est pas terminée

    for combinaison, evaluation in tentatives:
        if common.evaluation(combinaison, solution[0]) != tuple(map(int, evaluation.split(','))):
            return "Le codemaker a triché !"

    return "Le codemaker n'a pas triché !"


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    DEBUT TESTS - QUESTION 10
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import play
import codemaker2, codebreaker2

# Simuler une partie :
# play.play_log(codemaker2, codebreaker2, "log0.txt") # A DECOMMENTER
#
# Vérifier que le codemaker n'a pas triché de manière visible :
# print(check_codemaker("log0.txt")) # A DECOMMENTER
#
# Re-commenter les deux lignes de code précédentes.
# Modifier l'une des évaluations dans le fichier "log0.txt", puis vérifier que le codemaker a triché de manière visible :
# print(check_codemaker("log0.txt")) # A DECOMMENTER

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    FIN TESTS - QUESTION 10
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



# RORN RORN
# Essai 0 : NRJV (0,2)
# RORN VNNN
# Le codemaker a triché !
# Essai 1 : JBNJ (1,0)
# VNNN BBVR
# Le codemaker a triché !
# Essai 2 : OVNO (0,1)
# BBVR RORJ
# Le codemaker a triché !
# Essai 3 : RBVM (1,0)
# RORJ ROGJ
# Le codemaker a triché !
# Essai 4 : RORJ (3,0)
# ROGJ ROGJ
# Essai 5 : ROGJ (4,0)