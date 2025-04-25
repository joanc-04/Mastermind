import common

import codemaker2, codemaker1
import codebreaker2, codebreaker1, codebreaker0


def play(codemaker, codebreaker, quiet=False):
    """
    Fonction principale de ce programme :
    Fait jouer ensemble le codebreaker et le codemaker donnés en arguments
    Renvoie le nombre de coups joués pour trouver la solution

    Attention, il ne *doit* pas être nécessaire de modifier cette fonction
    pour faire fonctionner vos codemaker et codebreaker (dans le cas contraire,
    ceux-ci ne seront pas considérés comme valables)
    """
    n_essais = 0
    codebreaker.init()
    codemaker.init()
    if quiet: print('Solution:', codemaker.getSolution())



    ev = None
    if not quiet:
        print('Combinaisons de taille {}, couleurs disponibles {}'.format(common.LENGTH, common.COLORS))
    while True:
        combinaison = codebreaker.codebreaker(ev)
        ev = codemaker.codemaker(combinaison)
        n_essais += 1
        if not quiet:
            print("Essai {} : {} ({},{})".format(n_essais, combinaison, ev[0], ev[1]))
        if ev[0] >= common.LENGTH:
            if not quiet:
                print("Bravo ! Trouvé {} en {} essais".format(combinaison, n_essais))
            return n_essais



def play_log(codemaker, codebreaker, nom_fichier, quiet=False):
    """
    Lance une partie en enregistrant chaque tentative jouée et son évaluation associée dans un fichier log.

    :param codemaker: Codemaker de la partie.
    :param codebreaker: Codebreaker de la partie.
    :param nom_fichier: Nom du fichier log.
    :return: Le nombre de tentatives nécessaires pour trouver la solution.
    """

    with open(nom_fichier, "w") as file:
        n_essais = 0 # Compte le nombre de tentatives
        codebreaker.init() # Initialise le codebreaker
        codemaker.init() # Initialise le codemaker
        ev = None
        while True: # Tant que la solution n'a pas été trouvée

            combinaison = codebreaker.codebreaker(ev) # Le codebreaker propose une combinaison
            ev = codemaker.codemaker(combinaison) # Le codemaker évalue cette combinaison
            n_essais += 1 # Augmente le nombre de tentatives
            file.write(combinaison + "\n" + str(ev[0]) + "," + str(ev[1]) + "\n") # Ecrit dans le fichier log

            if not quiet:
                if n_essais != 1: print("Solutions possibles :", codebreaker.solutions_possibles)
                print("\nEssai {} : {} ({},{})".format(n_essais, combinaison, ev[0], ev[1]))


            if ev[0] >= common.LENGTH: # Si le codebreaker a trouvé la solution
                file.close()
                if not quiet:
                    print("Bravo ! Trouvé {} en {} essais".format(combinaison, n_essais))

                return n_essais # Renvoie le nombre de tentatives


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    DEBUT TESTS - QUESTION 11
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import codebreaker2, codemaker1

# play_log(codemaker1, codebreaker2, "log0.txt")

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    FIN TESTS - QUESTION 11
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""




# if __name__ == '__main__':
    # Les lignes suivantes sont à modifier / supprimer selon ce qu'on veut faire, quelques exemples :

    # Faire jouer ensemble codemaker0.py et codebreaker0.py pour 5 parties :
    # import codebreaker0
    # import codemaker0
    # for i in range(5):
    #     play(codemaker0, codebreaker0)

    #  Faire jouer un humain contre codemaker0.py :
    #import codemaker0
    #import human_codebreaker
    #play(codemaker0, human_codebreaker)

    # Et plus tard, vous pourrez faire jouer vos nouvelles version du codebreaker et codemaker :
    #import codebreaker2
    #import codemaker2
    #play(codemaker2, codebreaker2)

    # Ou encore :
    #import codebreaker1
    #import human_codemaker
    #play(human_codemaker, codebreaker1)
