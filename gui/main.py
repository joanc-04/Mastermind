import tkinter as tk
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './class/')))

from Mastermind import Mastermind

if __name__ == "__main__":
    root = tk.Tk() # Crée la fenêtre de l'application
    app = Mastermind(root) # Lance l'application
    root.mainloop() # Gère l'interface graphique en écoutant et répondant aux évènements