import tkinter as tk
from tkinter import ttk
from Game import Game
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from config import correspondances

class Mastermind:
    """
    Une instance de cette classe est générée lorsqu'on exécute le programme : une application se crée.
    Cette instance génère alors l'interface graphique pour la configuration de la partie.
    """

    def __init__(self, root):

        # Variables de la fenêtre de l'application
        self.root = root
        self.root.title("Mastermind") # Titre
        self.width, self.height = 500, 800 # Dimensions
        self.root.geometry(f"{self.width}x{self.height}")  # Ajuste la taille par défaut de la fenêtre

        # Variables de l'interface graphique (on génère un Canva)
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, highlightthickness=0) # Crée le Canva
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1) # Positionne le Canva dans la fenêtre

        # Menu de configuration du Mastermind
        self.__create_settings_screen()


    # Menu de configuration du Mastermind
    def __create_settings_screen(self):
        """
        Affiche le menu de configuration du Mastermind
        :return:
        """

        # Arrière-plan
        self.create_background()

        # Titre
        self.canvas.create_text(self.width // 2, 100, text="Configuration de la partie", fill="white", anchor="center", font=("Helvetica", 20))

        # Menu déroulant pour le choix du codemaker
        self.create_drop_down_menu()

        # Sélecteur du nombre de couleurs possibles
        self.create_slider("sliderColors", 1, len(correspondances), len(correspondances), "Choisissez le nombre de couleurs possibles.", y=350)

        # Sélecteur de la taille d'une combinaison
        self.create_slider("sliderLength", 1, 5, 4, "Choisissez la taille de la solution", y=450)

        # Sélecteur de la taille d'une combinaison
        self.create_slider("sliderAttempts", 1, 9, 8, "Choisissez le nombre de tentatives", y=550)

        # Bouton de lancement de la partie
        self.create_button(175, 700, 325, 750, "Start", self.__launchGame)


    # Arrière-plan
    def create_background(self):
        """Pour l'arrière-plan, on crée un dégradé noir-blanc."""

        # Dessiner le dégradé
        for i in range(self.height):
            gray = int(((self.height - i) / self.height) * 75)  # Inverse le calcul pour un dégradé de blanc à noir
            color = f"#{gray:02x}{gray:02x}{gray:02x}"  # Convertit la couleur obtenue en hexadécimale.
            self.canvas.create_line(0, i, self.width, i, fill=color)  # Crée une ligne horizontale de la couleur obtenue.


    # Menu déroulant pour le choix du codemaker
    def create_drop_down_menu(self):
        """
        Affiche le menu déroulant pour le choix du codemaker.
        :return:
        """

        self.canvas.create_text(self.width // 2, 200, text="Choisissez un codemaker", fill="white", anchor="center", font=("Helvetica", 16))

        options = ["Codemaker 0", "Codemaker 1", "Codemaker 2"]  # Choix possibles

        self.selected_option = tk.StringVar(self.root)
        self.selected_option.set(options[1])  # Valeur par défaut

        self.frame = tk.Frame(self.root, bg="darkblue", bd=5)  # Cadre pour rendre le menu déroulant plus joli
        self.frame.place(x=self.width // 2, y=250, anchor="center", width=200, height=50)  # Positionne le cadre

        # Créer le menu déroulant avec un joli design
        self.option_menu = tk.OptionMenu(self.frame, self.selected_option, *options)  # Crée le menu déroulant
        self.option_menu.config(
            font=("Arial", 14),  # Police et taille
            width=20,  # Largeur
            bg="lightblue",  # Couleur de fond
            fg="black",  # Couleur du texte
            activebackground="lightblue",  # Couleur du fond actif
            activeforeground="black",  # Couleur du texte actif
            relief="flat"  # Supprimer la bordure
        )
        self.option_menu.pack(fill="both", expand=True)  # Positionne le menu déroulant dans son cadre


    # Bouton
    def create_button(self, x1, y1, x2, y2, label, onClick_func):
        """
        Affiche un bouton à la position indiquée en paramètre
        :param x1: Abscisse de départ
        :param y1: Ordonnée de départ
        :param x2: Abscisse de fin
        :param y2: Ordonnée de fin
        :param label: Label du bouton
        :param onClick_func: Fonction à appeler quand le bouton est cliqué
        :return:
        """

        button = self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue", outline="black", width=2)  # Crée le bouton
        self.canvas.tag_bind(button, "<Button-1>", lambda event: onClick_func()) # Quand le bouton est cliqué, on lance la partie

        button_label = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=label, font=("Arial", 14)) # Crée le label du bouton
        self.canvas.tag_bind(button_label, "<Button-1>", lambda event: onClick_func()) # Quand le label est cliqué, on lance la partie

    # Curseur pour choisir un entier entre 1 et 9
    def create_slider(self, sliderName, minValue, maxValue, defaultValue, label, y):

        self.canvas.create_text(self.width // 2, y, text=label, fill="white", anchor="center", font=("Helvetica", 16))

        # Créer un cadre pour le slider
        frame = tk.Frame(self.root, bg="darkblue", bd=5)
        frame.place(x=self.width // 2, y=y + 50, anchor="center", width=200, height=50)

        # Variable qui stocke la valeur sélectionnée
        slider_var = tk.IntVar(value=defaultValue)

        # Créer le curseur (slider)
        slider = tk.Scale(frame, from_=minValue, to=maxValue, orient="horizontal", variable=slider_var, length=200, resolution=1, tickinterval=1, bg="lightblue", fg="black", font=("Arial", 12), highlightthickness=0)

        slider.pack()

        # Stocker le slider et sa variable dans l'instance
        setattr(self, sliderName, slider)
        setattr(self, sliderName + "Fram", frame)

    # Lance la partie
    def __launchGame(self):
        """
        Lance la partie de Mastermind
        :return:
        """

        codemaker = int(self.selected_option.get()[-1]) # Récupère le numéro du codemaker sélectionné
        colors = dict(list(correspondances.items())[:int(self.sliderColors.get())])
        length = int(self.sliderLength.get())
        attemptsNumber = int(self.sliderAttempts.get())

        self.canvas.delete("all")  # On efface toute la page de configuration (ce qui a été fait avec Canva)
        self.sliderColors.destroy() # On efface le sélecteur du nombre de couleurs (fait avec Tkinter)
        self.sliderColorsFram.destroy()
        self.sliderLength.destroy() # On efface le sélecteur de la taille de la solution (fait avec Tkinter)
        self.sliderLengthFram.destroy()
        self.sliderAttempts.destroy() # On efface le sélecteur de la taille de la solution (fait avec Tkinter)
        self.sliderAttemptsFram.destroy()
        self.option_menu.destroy() # On efface le menu déroulant (fait avec Tkinter)
        self.frame.destroy() # On efface le cadre (fait avec Tkinter)

        Game(self.root, self.canvas, codemaker, colors, attemptsNumber, length, self.width, self.height, self.create_background, self.create_button) # Lance la partie
        print("Partie lancée !")