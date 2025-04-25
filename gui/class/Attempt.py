class Attempt:

    def __init__(self, canvas, length, colors, width, height):

        self.activated = None
        self.currentAttempt = False
        self.canvas = canvas
        self.width = width
        self.height = height
        self.length = length
        self.colors = colors

    def changeStatus(self):
        self.currentAttempt = not self.currentAttempt

    def create_row(self, y_start):

        radius = 25  # Rayon des cercles
        spacing = 25  # Espacement entre les cercles
        x_start = (self.width - (self.length * 2 * radius + (self.length - 1) * spacing)) // 2  # Position de départ centrée
        y_center = y_start  # Position verticale des cercles

        self.entries = {}  # Liste pour stocker les rectangles créés

        for i in range(self.length):
            x = x_start + i * (2 * radius + spacing)  # Calculer la position x de chaque cercle

            entry = self.canvas.create_rectangle(
                x, y_center, x + 2 * radius, y_center + 2 * radius,
                fill="", outline="gray", width=3, dash=(15, 2)  # Pointillé gris par défaut
            )

            # Créer un "faux" fond transparent pour rendre la zone cliquable
            hover_area = self.canvas.create_rectangle(
                x, y_center, x + 2 * radius, y_center + 2 * radius,
                fill="", outline="", width=0  # Fond transparent invisible
            )

            # Lier l'événement de survol (hover) pour changer le contour en orange lorsque la souris entre dans le rectangle
            self.canvas.tag_bind(hover_area, "<Enter>", lambda event, e=entry: self.on_entry_hover(e, "orange"))
            self.canvas.tag_bind(hover_area, "<Leave>", lambda event, e=entry: self.on_entry_hover(e, "gray"))

            # Lier l'événement de clic pour changer le contour en orange
            self.canvas.tag_bind(hover_area, "<Button-1>", lambda event, e=entry: self.on_entry_click(e))

            self.entries[entry] = None

            if i == 0:
                self.activated = entry


    def update_row(self, entryActivated=None, reset=False):

        for entry in self.entries.keys():  # Pour chaque plot

            if reset is True:
                self.entries[entry] = None
                config = {"fill": ""}
            else:
                config = {}

            self.canvas.itemconfig(entry, outline="gray", **config)  # Remet le contour du plot en gris

        self.activated = entryActivated  # Active le premier plot de la tentative
        self.canvas.itemconfig(self.activated, outline="orange")  # Modifie la couleur du contour du plot activé en orange


    def on_entry_hover(self, entry, color):
        """Change la couleur du contour lors du survol ou du départ de la souris."""
        if not self.currentAttempt: # Si on n'est pas à la bonne ligne
            return

        if self.activated != entry:
            self.canvas.itemconfig(entry, outline=color)


    def on_entry_click(self, entry):
        """Change la couleur du contour lors d'un clic."""
        if not self.currentAttempt:
            return

        for e in self.entries.keys():
            self.canvas.itemconfig(e, outline="gray")  # Remettre tous les contours à gris

        self.canvas.itemconfig(entry, outline="orange")  # Le contour devient orange au clic
        self.activated = entry
