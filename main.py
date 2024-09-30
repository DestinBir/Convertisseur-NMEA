from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.core.window import Window
import sys

import convertisseur

# Modifier les couleurs du fond (Blanc)
Window.clearcolor = (0.9, 0.9, 0.9, 1)  # Blanc en arrière-plan

class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        
        # Layout principal pour la page d'accueil
        layout = BoxLayout(orientation='vertical', padding=[50, 50, 50, 50], spacing=20,
                           size_hint=(0.6, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Titre
        home_label = Label(
            text="Bienvenue dans le convertisseur NMEA", 
            font_size='24sp', 
            color=(0, 0, 0, 1), 
            halign='center'
        )
        
        # Boutons de la page d'accueil
        start_button = Button(
            text="Commencer", 
            size_hint=(0.5, 0.2), 
            pos_hint={'center_x': 0.5}, 
            background_color=(0.1, 0.5, 0.8, 1)
        )
        quit_button = Button(
            text="Quitter", 
            size_hint=(0.5, 0.2), 
            pos_hint={'center_x': 0.5}, 
            background_color=(0.8, 0.1, 0.1, 1)
        )

        # Liens des boutons aux fonctions
        start_button.bind(on_press=self.show_form)
        quit_button.bind(on_press=self.quit_app)

        # Ajouter les éléments au layout
        layout.add_widget(home_label)
        layout.add_widget(start_button)
        layout.add_widget(quit_button)
        self.add_widget(layout)

    def show_form(self, instance):
        self.manager.current = 'form_page'

    def quit_app(self, instance):
        App.get_running_app().stop()
        sys.exit()

class FormPage(Screen):
    def __init__(self, **kwargs):
        super(FormPage, self).__init__(**kwargs)
        
        # Layout principal pour le formulaire
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20,
                           size_hint=(0.6, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Champ de saisie pour la trame GPGGA
        self.gpgga_input = TextInput(
            hint_text="Entrez la trame GPGGA", 
            multiline=False, 
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5}, 
            background_color=(1, 1, 1, 1), 
            foreground_color=(0, 0, 0, 1)
        )
        
        # Bouton pour prévisualiser les résultats
        save_button = Button(
            text="Prévisualiser", 
            size_hint=(0.5, 0.2), 
            pos_hint={'center_x': 0.5}, 
            background_color=(0.2, 0.6, 0.8, 1)
        )
        save_button.bind(on_press=self.preview_results)

        # Bouton retour
        back_button = Button(
            text="Retour", 
            size_hint=(0.5, 0.2), 
            pos_hint={'center_x': 0.5}, 
            background_color=(0.5, 0.5, 0.5, 1)
        )
        back_button.bind(on_press=self.go_back)

        # Ajouter les éléments au layout
        layout.add_widget(self.gpgga_input)
        layout.add_widget(save_button)
        layout.add_widget(back_button)

        # Ajouter le bouton "À propos de nous"
        about_button = Button(
            text="À propos de nous", 
            size_hint=(0.5, 0.2), 
            pos_hint={'center_x': 0.5}, 
            background_color=(0.3, 0.7, 0.9, 1)
        )
        about_button.bind(on_press=self.show_about)
        layout.add_widget(about_button)

        self.add_widget(layout)

    def preview_results(self, instance):
        gpgga_data = self.gpgga_input.text
        gpgsa = convertisseur.generer_gpgsa(gpgga_data)
        gprmc = convertisseur.generer_gprmc(gpgga_data)

        # Prévisualisation des résultats avant enregistrement
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f"GPGGA: {gpgga_data}", color='white'))
        content.add_widget(Label(text=f"GPGSA: {gpgsa}", color='white'))
        content.add_widget(Label(text=f"GPRMC: {gprmc}", color='white'))

        # Boutons pour enregistrer ou annuler
        save_button = Button(text="Enregistrer", size_hint=(1, 0.2), background_color=(0.1, 0.6, 0.2, 1))
        cancel_button = Button(text="Refuser", size_hint=(1, 0.2), background_color=(0.6, 0.1, 0.1, 1))

        # Lier les boutons aux fonctions
        save_button.bind(on_press=lambda x: self.save_file(gpgga_data, gpgsa, gprmc))
        cancel_button.bind(on_press=lambda x: self.close_popup())

        content.add_widget(save_button)
        content.add_widget(cancel_button)

        # Afficher la popup de prévisualisation
        self.popup = Popup(title="Prévisualisation", content=content, size_hint=(0.8, 0.8))
        self.popup.open()

    def save_file(self, gpgga_data, gpgsa, gprmc):
        # Enregistrement dans un fichier .txt
        with open("nmea_output.nmea", "w") as f:
            f.write(f"{gpgga_data}\n")
            f.write(f"{gpgsa}\n")
            f.write(f"{gprmc}\n")

        # Confirmation de l'enregistrement
        self.show_confirmation()
        self.close_popup()

    def close_popup(self):
        self.popup.dismiss()

    def show_confirmation(self):
        # Afficher une popup de confirmation
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Fichier enregistré avec succès !\n Pour permettre de bien l'ouvrir dans nmeagen, on prend .nmea que .txt", color='white'))
        popup = Popup(title="Confirmation", content=content, size_hint=(0.6, 0.3))
        popup.open()

    def show_about(self, instance):
        self.manager.current = 'about_page'

    def go_back(self, instance):
        self.manager.current = 'main_page'

class AboutPage(Screen):
    def __init__(self, **kwargs):
        super(AboutPage, self).__init__(**kwargs)
        
        # Layout principal pour la page "À propos"
        layout = BoxLayout(orientation='vertical', padding=30, spacing=30, size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Informations sur la page "À propos de nous"
        about_label = Label(
            text="[b]Formats NMEA utilisés :[/b]\n\n"
                 "[b]1. GPGGA[/b] : Informations de position (latitude, longitude, altitude).\n\n"
                 "[b]2. GPGSA[/b] : État du récepteur GPS et satellites actifs.\n\n"
                 "[b]3. GPRMC[/b] : Données essentielles pour la navigation.\n\n"
                 "[b]Concepteurs :[/b]\n\n\n\n"
                 "Université Catholique de Bukavu\n"
                 "[b]UCB[/b]\n\n"
                 "Département d'Informatique: Génie Logiciel\n\n"
                 "1- AGISHA KITULI Ghislain\n"
                 "2- AKONKWA USHINDI Isaac\n"
                 "3- Bénédict LUBEMBELA\n"
                 "4- BIRINGANINE BASEME Destin\n"
                 "5- CIRHUZA BUMIZI Isaac\n"
                 "6- JIBU MAROYI Benjamin\n\n\n\n"
                 "Merci d'utiliser notre application !",
            font_size='16sp', 
            markup=True, 
            halign='left',
            color=(0, 0, 0, 1)
        )

        # Bouton retour
        back_button = Button(text="Retour", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5}, background_color=(0.5, 0.5, 0.5, 1))
        back_button.bind(on_press=self.go_back)

        layout.add_widget(about_label)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'form_page'

class NMEAApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainPage(name='main_page'))
        sm.add_widget(FormPage(name='form_page'))
        sm.add_widget(AboutPage(name='about_page'))
        return sm

if __name__ == "__main__":
    NMEAApp().run()
