#!/usr/bin/env python3

import common

def init():
    return

def codemaker(combinaison):
    print('Combinaison proposée: {}'.format(combinaison))
    while True:
        try:
            bp = int(input('Saisir nombre de plots bien placés: '))
        except ValueError:
            continue
        if bp < 0 or bp > common.LENGTH:
            print("valeur invalide (< 0 ou > {})".format(common.LENGTH))
            continue
        break
    while True:
        try:
            mp = int(input('Saisir nombre de plots mal placés: '))
        except ValueError:
            continue
        if mp < 0 or mp > common.LENGTH:
            print("valeur invalide (< 0 ou > {})".format(common.LENGTH))
            continue
        break
    return bp, mp
 
