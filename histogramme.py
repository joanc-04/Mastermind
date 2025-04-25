import sys
import common
import matplotlib.pyplot as plt
import numpy as np
import codebreaker0, codemaker0, codebreaker1, codemaker1, codebreaker2, codemaker2, codebreaker3, play

def generer_histogramme(codemakerX_numero, codebreakerX_numero, codemakerY_numero=None, codebreakerY_numero=None, question=None, nombre_tentatives=1000, quiet=True, nombre_graphique=3, nombre_bar=50):
    """
    Génère un histogramme permettant de comparer les performances sur le nombre de tentatives jusqu'à arriver à la solution pour différents codemaker et codebreaker.

    :param codemakerX_numero:
    :param codebreakerX_numero:
    :param codemakerY_numero:
    :param codebreakerY_numero:
    :param question:
    :param nombre_tentatives:
    :param quiet:
    :return:
    """

    if question is None: # Si on n'a pas indiqué le numéro de la question, alors on renvoie une erreur.
        sys.exit("Absence du numéro de la question.")

    if not (1 <= nombre_graphique <= 3):
        sys.exit("Vous ne pouvez afficher qu'entre 1 et 3 graphiques par ligne.")

    # Graphique bleu
    codemakerX = globals()["codemaker" + str(codemakerX_numero)] # On importe le fichier associé à codemakerX
    codebreakerX = globals()["codebreaker" + str(codebreakerX_numero)] # On importe le fichier associé à codebreakerX
    liste_nombres_tentatives_codemakerX_codebreakerX = [play.play(codemakerX, codebreakerX, quiet=quiet) for _ in range(nombre_tentatives)] # On simule "nombre_tentatives" parties en faisant jouer codemakerX et codebreakerX.
    print("Le graphique bleu a été généré !")

    # Graphique orange
    liste_nombres_tentatives_codemakerY_codebreakerY = []
    if codemakerY_numero:
        codemakerY = globals()["codemaker" + str(codemakerY_numero)] # On importe le fichier associé à codemakerY
        codebreakerY = globals()["codebreaker" + str(codebreakerY_numero)] # On importe le fichier associé à codebreakerY
        liste_nombres_tentatives_codemakerY_codebreakerY = [play.play(codemakerY, codebreakerY, quiet=quiet) for _ in range(nombre_tentatives)] # On simule "nombre_tentatives" parties en faisant jouer codemakerY et codebreakerY.
        print("Le graphique orange a été généré !")


    # Largeur des intervalles des histogrammes
    liste_nombres_tentatives = liste_nombres_tentatives_codemakerX_codebreakerX + liste_nombres_tentatives_codemakerY_codebreakerY
    x_lim = 1.2 * min([max(liste_nombres_tentatives_codemakerX_codebreakerX), max(liste_nombres_tentatives_codemakerY_codebreakerY)]) if codemakerY_numero else max(liste_nombres_tentatives_codemakerX_codebreakerX)
    bins = (
        np.linspace(0, max(liste_nombres_tentatives),  nombre_bar),
        np.linspace(0, x_lim,  nombre_bar),
        np.histogram_bin_edges(liste_nombres_tentatives, bins="auto"),
    )

    fig, ax = plt.subplots(nrows=2, ncols=nombre_graphique, figsize=(26, 18)) # Création du graphique
    fig.subplots_adjust(hspace=0.4)

    # Calcul des moyennes du nombre de tentatives
    moyenne_nombres_tentatives_codemakerX_codebreakerX = np.mean(liste_nombres_tentatives_codemakerX_codebreakerX)
    if codemakerY_numero: moyenne_nombres_tentatives_codemakerY_codebreakerY = np.mean(liste_nombres_tentatives_codemakerY_codebreakerY)

    for i in range(nombre_graphique): # Pour chacun des graphiques

        # Cette partie est relatif à la première ligne de graphiques.
        axis = ax[0] if nombre_graphique == 1 else ax[0][i] # Si on veut afficher un seul graphique par ligne, on a ax=[graphique, graphique]. Alors que si veut afficher plusieurs graphiques par ligne, on a ax=[[graphique_0, graphique_1, graphique_2], [graphique_0, graphique_1, graphique_2]]

        if i in [1, 2]:
            axis.set_xlim(0, x_lim)

        # Affichage des éléments relatifs aux parties simulées de codemakerX vs codebreakerX
        axis.hist(liste_nombres_tentatives_codemakerX_codebreakerX, bins=bins[i], color='skyblue', edgecolor="black", alpha=0.5, label=f"Codebreaker {codebreakerX_numero} VS Codemaker {codemakerX_numero}") # Affichage du graphique.
        axis.axvline(moyenne_nombres_tentatives_codemakerX_codebreakerX, color='darkblue', linestyle='dashed', linewidth=2, label=f"Moyenne : {moyenne_nombres_tentatives_codemakerX_codebreakerX:.1f}") # Affichage de la ligne de l'espérance.

        # Affichage des éléments relatifs aux parties simulées de codemakerY vs codebreakerY
        if codemakerY_numero:
            axis.hist(liste_nombres_tentatives_codemakerY_codebreakerY, bins=bins[i], color='orange', edgecolor="black", alpha=0.4, label=f"Codebreaker {codebreakerY_numero} VS Codemaker {codemakerY_numero}")  # Affichage de la ligne de l'espérance.
            axis.axvline(moyenne_nombres_tentatives_codemakerY_codebreakerY, color='red', linestyle='dashed', linewidth=2, label=f"Moyenne : {moyenne_nombres_tentatives_codemakerY_codebreakerY:.1f}") # Affiche du graphique.

        # Cette partie est relatif à la deuxième ligne de graphiques.
        axis = ax[1] if nombre_graphique == 1 else ax[1][i] # Si on veut afficher un seul graphique par ligne, on a ax=[graphique, graphique]. Alors que si veut afficher plusieurs graphiques par ligne, on a ax=[[graphique_0, graphique_1, graphique_2], [graphique_0, graphique_1, graphique_2]]

        if i in [1, 2]:
            axis.set_xlim(0, x_lim)

        # Densité pour codemakerX vs codebreakerX
        hist_x, bin_edges_x = np.histogram(liste_nombres_tentatives_codemakerX_codebreakerX, bins=bins[i])
        bin_centers_x = (bin_edges_x[:-1] + bin_edges_x[1:]) / 2
        x_smooth = np.linspace(bin_centers_x.min(), bin_centers_x.max(), 300)
        y_smooth = np.interp(x_smooth, bin_centers_x, hist_x)  # Interpolation linéaire

        axis.plot(x_smooth, y_smooth, color="blue", linestyle="-", linewidth=3, alpha=0.6, label=f"Courbe")
        axis.axvline(moyenne_nombres_tentatives_codemakerX_codebreakerX, color='darkblue', linestyle='dashed', linewidth=2)

        # Densité pour codemakerY vs codebreakerY
        if codemakerY_numero:
            hist_y, bin_edges_y = np.histogram(liste_nombres_tentatives_codemakerY_codebreakerY, bins=bins[i])
            bin_centers_y = (bin_edges_y[:-1] + bin_edges_y[1:]) / 2
            x_smooth_y = np.linspace(bin_centers_y.min(), bin_centers_y.max(), 300)
            y_smooth_y = np.interp(x_smooth_y, bin_centers_y, hist_y)
            axis.plot(x_smooth_y, y_smooth_y, color="orange", linestyle="-", linewidth=3, alpha=0.7, label=f"Courbe")
            axis.axvline(moyenne_nombres_tentatives_codemakerY_codebreakerY, color='red', linestyle='dashed', linewidth=2)

        axis.grid(True, linestyle="--", alpha=0.6)  # Ajoute une grille légère pour améliorer la lisibilité

    # Titre des axes.
    fig.text(0.5, 0.04, "Nombre de tentatives", ha='center', fontsize=25, fontweight='bold')  # Axe des abscisses
    fig.text(0.04, 0.5, "Fréquence", va='center', rotation='vertical', fontsize=25, fontweight='bold')  # Axe des ordonnées

    # Légende des histogrammes.
    handles, labels = (ax[0] if nombre_graphique == 1 else ax[0][0]).get_legend_handles_labels()  # Récupère les légendes seulement du premier graphique de la première ligne (car les légendes de chacun des graphiques de la ligne sont communes).
    handles_, labels_ = (ax[1] if nombre_graphique == 1 else ax[1][0]).get_legend_handles_labels()  # Récupère les légendes seulement du premier graphique de la deuxième ligne (car les légendes de chacun des graphiques de la ligne sont communes).
    handles = handles[:2] + [handles_[0]] + handles[2:] + ([handles_[1]] if len(handles_) > 1 else [])
    labels = labels[:2] + [labels_[0]] + labels[2:] + ([labels_[1]] if len(labels_) > 1 else [])
    fig.legend(handles, labels, fontsize=18, ncol=2 if codemakerY_numero else 1, loc="upper center", bbox_to_anchor=(0.5, 0.53))

    # Titre du graphique
    title = (
            "Comparaison du nombre de tentatives jusqu'à trouver la solution\n" +
            f"(Codebreaker {str(codebreakerX_numero)} VS Codemaker {str(codemakerX_numero)}" +
            (f" & Codebreaker {str(codebreakerY_numero)} VS Codemaker {str(codemakerY_numero)}" if codemakerY_numero else "") +
            ")"
    )
    fig.suptitle(title, fontsize=25, fontweight='bold')


    fig.savefig(f"question_{question}.pdf") # On enregistre le graphique
    # plt.show() # On affiche le graphique



# LES TESTS CI-DESSOUS SONT A DE-COMMENTER UN-A-UN

# Question 3
# generer_histogramme(0, 0,question=3, nombre_graphique=1, nombre_bar=100)

# Question 4
# generer_histogramme(1,0,1, 1, question=4, nombre_graphique=3)

# Question 7
# generer_histogramme(1, 1, 1, 2, question=7)

# Question 8
# generer_histogramme(1, 2, 2, 2, question=8, nombre_tentatives=100)

# Question 12
# generer_histogramme(1, 2, 1, 3, 12, nombre_tentatives=200)
# generer_histogramme(2, 2, 2, 3, "12_bis", nombre_tentatives=200)