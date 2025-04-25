#!/usr/bin/env python3

import common


def init():
    return

def codebreaker(__):  # Inutile d'affiche la correction reçue, la boucle principale de jeu s'en charge
    while True:
        combinaison = input("Saisir combinaison: ")  # On lit une combinaison au clavier au lieu d'appeler le codebreaker (qui sera donc joué par un humain)
        if len(combinaison) != common.LENGTH:
            print("Combinaison invalide (longueur {} au lieu de {})".format(len(combinaison), common.LENGTH))
            continue
        for c in combinaison:
            if c not in common.COLORS:
                print("Combinaison invalide (couleur {} n'existe pas)".format(c))
                continue
        return combinaison 

