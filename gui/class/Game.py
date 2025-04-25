import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import common
import codemaker0, codemaker1, codemaker2
from Attempt import Attempt
import Mastermind



class Game:
    """
    Une instance de cette classe est générée lorsqu'on lance la partie (une fois qu'on a configuré les paramètres).
    Cette instance génère alors l'interface graphique qui permet de jouer, mais fait également appel aux codemaker qui évaluent les combinaisons testées.
    """

    def __init__(self, root, canvas, codemaker, colors, attemptsNumber, length, width, height, create_background, create_button): # Exécute ce code lorsqu'on crée une instance du jeu

        # Variables de la fenêtre de l'application
        self.root = root
        self.canvas = canvas                        # Canva
        self.width = width                          # Largeur
        self.height = height                        # Hauteur
        self.create_background = create_background  # Fonction qui génère l'arrière-plan
        self.create_button = create_button          # Fonction qui génère un bouton

        # Variables de jeu
        self.colors = colors                                        # Couleurs avec lesquelles on joue
        self.length = length                                        # Taille de la solution à deviner
        self.codemaker = codemaker                                  # Numéro du codemaker sélectionné
        self.codemaker = globals()["codemaker" + str(codemaker)]    # Appel du fichier codemaker correspondant
        # self.length = common.LENGTH                               # Taille d'une combinaison
        # self.colors = common.COLORS                               # Couleurs possibles
        self.attemptsNumber = attemptsNumber                        # Nombres de tentatives
        self.attempts = []                                          # Liste contenant les tentatives faites
        self.currentAttemptNumber = 0                               # Numéro de la tentative actuelle

        # Initialise le codemaker
        self.startBack()

        # Interface graphique
        self.create_widgets()

        # Détection des touches de clavier
        self.root.bind("<Tab>", lambda event: self.on_tab_pressed(False))
        self.root.bind("<Shift-Tab>", lambda event: self.on_tab_pressed(True))
        self.root.bind("<Return>", lambda event: self.on_enter_pressed())
        self.root.bind("<KeyPress>", lambda event: self.on_key_pressed(event))


    # Initialise le codemaker
    def startBack(self):
        """
        Initialise le codemaker
        :return:
        """

        common.COLORS = list(self.colors.values())[:len(self.colors)]
        common.LENGTH = self.length
        self.codemaker.init()

        inverse_correspondances = {v: k for k, v in self.colors.items()} # Inverse les correspondances clé-valeur

        print(f"La solution à deviner est : {" - ".join([inverse_correspondances[i] for i in list(self.codemaker.getSolution())])}")

    # Interface graphique
    def create_widgets(self):
        """
        Génère toute l'interface graphique.
        :return:
        """

        # Arrière-plan
        self.create_background()

        # Titre de l'application
        self.canvas.create_text(self.width//2, 40, text="Mastermind", fill="white", anchor="center", font=("Helvetica", 20))

        # Barre de couleurs
        self.create_color_circles()

        # Grille de tentatives
        self.create_attempts()

        # Bouton envoyer
        self.create_button(75, self.height - 100, 75 + 150, self.height - 50, "Submit", self.on_submit)

        # Bouton réinitialiser
        self.create_button(275, self.height - 100, 275 + 150, self.height - 50, "Reset", self.on_reset)


    # Grille de tentatives
    def create_attempts(self):

        for i in range(self.attemptsNumber): # Pour chaque tentative
            attempt = Attempt(self.canvas, self.length, self.colors, self.width, self.height) # Crée un objet tentative
            attempt.create_row(75 + i * 60) # Génère la ligne sur l'interface graphique
            self.attempts.append(attempt) # Enregistre cette tentative dans la liste des tentatives

        # Lorsqu'on crée la grille, c'est la première tentative qui est activée
        firstAttempt = self.attempts[self.currentAttemptNumber] # Récupère la première tentative
        firstAttempt.changeStatus() # Change le status de la première tentative
        firstAttempt.update_row(list(firstAttempt.entries.keys())[0])


    # Détecte si un chiffre est cliqué
    def on_key_pressed(self, event):
        """
        Si un chiffre est cliqué, on modifie la couleur du plot actif de la tentative active.
        :param event:
        :return:
        """

        if event.char in [str(i) for i in list(range(1, len(self.colors) + 1))]: # Si le plot est compris entre 1 et le nombre de couleur
            listColors = list(self.colors.keys()) # TODO
            self.on_circle_click(listColors[int(event.char) - 1]) # Modifie la couleur du plot actif

        if event.keysym == "r":
            self.on_reset()

    # Détecte si la touche "entré" est cliqué
    def on_enter_pressed(self):
        """
        Si la touche entrée est cliqué, c'est comme si on avait cliqué sur le bouton envoyé.
        :return:
        """

        self.on_submit()

    # Détecte si la touche "tab" ou "shift-tab" est cliqué
    def on_tab_pressed(self, shift):
        """
        Si la touche "tab" est cliqué, on décale le plot actif d'un plot sur la droite.
        Si la touche "shift-tab" est cliqué, on décale le plot actif d'un plot sur la gauche.
        :return:
        """

        attempt = self.getCurrentAttempt() # Récupère la tentative active

        index = list(attempt.entries.keys()).index(attempt.activated)  # Récupère l'index actuel du plot actif.
        newIndex = (index + 1 if index != self.length - 1 else 0) if shift is False else (index - 1 if index != 0 else -1)  # Détermine le nouvel index décalé d'un sur la droite ou la gauche.
        attempt.update_row(list(attempt.entries.keys())[newIndex]) # Met à jour la couleur du contour des plots


    # Récupère la tentative active
    def getCurrentAttempt(self):
        """
        Récupère la tentative active
        :return:
        """

        return self.attempts[self.currentAttemptNumber]


    # Cercles de couleurs en bas
    def create_color_circles(self):
        """Crée une barre de ronds de couleur."""

        # colors = [color for color in list(self.colors.keys())[:self.colorsAmount - 1]]

        radius = 20  # Rayon des cercles
        spacing = self.width / (len(self.colors) + 1)  # Espacement entre les cercles
        x_start = spacing  # Position de départ
        y_center = self.height - 150  # Position verticale des cercles

        self.color_circles = {}  # Dictionnaire pour stocker les cercles et leurs couleurs

        for i, color in enumerate(self.colors):
            x = x_start + i * spacing  # Position horizontale du cercle
            circle = self.canvas.create_rectangle(x - radius, y_center - radius, x + radius, y_center + radius, fill=color, outline="black") # Dessiner un cercle sur le canvas
            self.canvas.tag_bind(circle, "<Button-1>", lambda event, c=color: self.on_circle_click(c)) # Associer un événement de clic
            self.color_circles[circle] = color # Stocker le cercle et sa couleur

    # Modifie la couleur du plot actif lorsqu'on clique sur une couleur
    def on_circle_click(self, color):
        """Modifie la couleur du plot actif de la tentative active lorsqu'une couleur est cliqué."""

        attempt = self.getCurrentAttempt() # Récupère la tentative active
        entryActivated = attempt.activated # Récupère le plot actif

        self.canvas.itemconfig(entryActivated, fill=color) # Modifie la couleur du plot actif.
        attempt.entries[entryActivated] = color # Enregistre la nouvelle couleur du plot (qui servira pour l'évaluation)

        print(f"Cercle cliqué: {color}")


    # Détecte quand on valide une combinaison
    def on_submit(self):
        """
        Détecte quand on valide une combinaison.
        :return:
        """

        attempt = self.getCurrentAttempt() # Récupère la tentative actuelle

        if None in attempt.entries.values(): # Si la combinaison est incomplète
            return messagebox.showinfo("Erreur", f"Veuillez entrer {self.length} couleurs !")

        attempt.update_row() # Met à jour la couleur du contour des plots

        self.attempts[self.currentAttemptNumber].changeStatus() # Désactive la tentative actuelle pour qu'elle ne réponde plus aux divers évènements
        self.currentAttemptNumber += 1 # Met à jour le numéro de la tentative actuelle

        evaluation = self.evaluate(attempt.entries) # Evalue la combinaison testée

        if evaluation[0] >= self.length: # Si la combinaison testée est correcte
            messagebox.showinfo("Fin de partie", f"Félicitation du as gagné !")
            self.new_game()

        else:

            coords = self.canvas.coords(list(attempt.entries.keys())[-1]) # Récupère les coordonnées de la ligne de carrés gris (pour aligner l'affichage de l'évaluation)
            x_start = coords[2] + 20

            # Affiche les plots bien placés
            self.canvas.create_text(x_start, coords[1] + 10, text=str(evaluation[0]), fill="white", anchor="center", font=("Helvetica", 17))
            self.canvas.create_rectangle(x_start + 20, coords[1], x_start + 40, coords[3] - 30, fill="green", outline="white")

            # Affiche les plots présents, mais mal placés
            self.canvas.create_text(x_start, coords[1] + 40, text=str(evaluation[1]), fill="white", anchor="center", font=("Helvetica", 17))
            self.canvas.create_rectangle(x_start + 20, coords[1] + 30, x_start + 40, coords[3], fill="red", outline="white")


            if self.currentAttemptNumber < self.attemptsNumber: # Si on a encore des tentatives
                newAttempt = self.getCurrentAttempt() # Récupère la nouvelle tentative
                self.attempts[self.currentAttemptNumber].changeStatus() # Active la nouvelle tentative pour qu'elle réponde aux divers évènements
                newAttempt.update_row(newAttempt.activated)

            else: # Si on n'a plus de tentatives
                messagebox.showinfo("Fin de partie", f"Dommage tu as perdu...")
                self.new_game()


    # Evalue la combinaison testée
    def evaluate(self, entries):
        """
        Evalue la combinaison testée
        :param entries: Combinaison testée
        :return:
        """

        return self.codemaker.codemaker("".join([self.colors[e] for e in entries.values()]))


    # Réinitialise la tentative en cours
    def on_reset(self):
        """
        Réinitialise la tentative en cours
        :return:
        """

        attempt = self.getCurrentAttempt() # Récupère la tentative actuelle

        attempt.update_row(list(attempt.entries.keys())[0], reset=True) # Met à jour la couleur des contours

    # Relance une nouvelle partie
    def new_game(self):
        """

        :return:
        """
        self.root.destroy()
        root = tk.Tk()  # Crée la fenêtre de l'application
        app = Mastermind.Mastermind(root)  # Lance l'application
        root.mainloop()  # Gère l'interface graphique en écoutant et répondant aux évènements