import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


class MesTachesApp(App):

    def build(self):

        self.fichier = os.path.join(self.user_data_dir, "tasks.json")

        # Charger les tâches sauvegardées
        self.taches = self.charger_taches()

        # Interface principale
        self.layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        # Titre
        self.titre = Label(
            text="MES TÂCHES",
            font_size=32,
            size_hint_y=None,
            height=60
        )

        self.layout.add_widget(self.titre)

        # Compteur
        self.compteur = Label(
            text="",
            font_size=20,
            size_hint_y=None,
            height=50
        )

        self.layout.add_widget(self.compteur)

        # Liste
        self.liste_taches = BoxLayout(
            orientation="vertical",
            spacing=10
        )

        self.layout.add_widget(self.liste_taches)

        # Bouton ajouter
        bouton_ajouter = Button(
            text="+ Ajouter une tâche",
            font_size=20,
            size_hint_y=None,
            height=70
        )

        bouton_ajouter.bind(
            on_press=self.ouvrir_fenetre_ajout
        )

        self.layout.add_widget(bouton_ajouter)

        # Afficher les tâches
        self.actualiser_liste()

        return self.layout

    # -----------------------------
    # CHARGER LES TÂCHES
    # -----------------------------

    def charger_taches(self):

        if not os.path.exists(self.fichier):
            return []

        try:
            with open(self.fichier, "r", encoding="utf-8") as fichier:
                return json.load(fichier)

        except:
            return []

    # -----------------------------
    # SAUVEGARDER LES TÂCHES
    # -----------------------------

    def sauvegarder_taches(self):

        with open(self.fichier, "w", encoding="utf-8") as fichier:

            json.dump(
                self.taches,
                fichier,
                ensure_ascii=False,
                indent=4
            )

    # -----------------------------
    # AJOUTER
    # -----------------------------

    def ouvrir_fenetre_ajout(self, instance):

        contenu = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=15
        )

        champ = TextInput(
            hint_text="Écris ta tâche ici...",
            font_size=20,
            multiline=False
        )

        contenu.add_widget(champ)

        bouton = Button(
            text="Ajouter",
            font_size=20,
            size_hint_y=None,
            height=60
        )

        contenu.add_widget(bouton)

        popup = Popup(
            title="Nouvelle tâche",
            content=contenu,
            size_hint=(0.85, 0.4)
        )

        bouton.bind(
            on_press=lambda instance:
            self.ajouter_tache(champ.text, popup)
        )

        popup.open()

    def ajouter_tache(self, texte, popup):

        texte = texte.strip()

        if texte == "":
            return

        self.taches.append({
            "texte": texte,
            "terminee": False
        })

        self.sauvegarder_taches()

        popup.dismiss()

        self.actualiser_liste()

    # -----------------------------
    # TERMINER
    # -----------------------------

    def terminer_tache(self, index):

        self.taches[index]["terminee"] = not self.taches[index]["terminee"]

        self.sauvegarder_taches()

        self.actualiser_liste()

    # -----------------------------
    # SUPPRIMER
    # -----------------------------

    def supprimer_tache(self, index):

        del self.taches[index]

        self.sauvegarder_taches()

        self.actualiser_liste()

    # -----------------------------
    # ACTUALISER
    # -----------------------------

    def actualiser_liste(self):

        self.liste_taches.clear_widgets()

        for index, tache in enumerate(self.taches):

            ligne = BoxLayout(
                orientation="horizontal",
                spacing=5,
                size_hint_y=None,
                height=60
            )

            if tache["terminee"]:
                texte = "☑ " + tache["texte"]
            else:
                texte = "☐ " + tache["texte"]

            bouton_tache = Button(
                text=texte,
                font_size=18
            )

            bouton_tache.bind(
                on_press=lambda instance, i=index:
                self.terminer_tache(i)
            )

            ligne.add_widget(bouton_tache)

            bouton_supprimer = Button(
                text="🗑️",
                font_size=20,
                size_hint_x=None,
                width=60
            )

            bouton_supprimer.bind(
                on_press=lambda instance, i=index:
                self.supprimer_tache(i)
            )

            ligne.add_widget(bouton_supprimer)

            self.liste_taches.add_widget(ligne)

        restantes = sum(
            1
            for tache in self.taches
            if not tache["terminee"]
        )

        if restantes == 0:
            self.compteur.text = "Toutes les tâches sont terminées 🎉"

        elif restantes == 1:
            self.compteur.text = "1 tâche restante"

        else:
            self.compteur.text = f"{restantes} tâches restantes"


if __name__ == "__main__":
    MesTachesApp().run()