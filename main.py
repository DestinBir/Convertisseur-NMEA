from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import sys

# Modifier les couleurs du fond
Window.clearcolor = (0.05, 0.05, 0.2, 1)  # Bleu foncé

class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20, size_hint=(0.6, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Page d'accueil
        home_label = Label(text="Bienvenue dans le convertisseur NMEA", font_size='24sp', color=(1, 1, 1, 1), halign='center')
        start_button = Button(text="Commencer", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5}, background_color=(0.1, 0.5, 0.8, 1))
        quit_button = Button(text="Quitter", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5}, background_color=(0.8, 0.1, 0.1, 1))

        start_button.bind(on_press=self.show_form)
        quit_button.bind(on_press=self.quit_app)

        # Ajouter les éléments à l'interface
        layout.add_widget(home_label)
        layout.add_widget(start_button)
        layout.add_widget(quit_button)
        self.add_widget(layout)

    def show_form(self, instance):
        self.manager.current = 'form_page'

    def quit_app(self, instance):
        # Quitter l'application
        App.get_running_app().stop()
        sys.exit()

class FormPage(Screen):
    def __init__(self, **kwargs):
        super(FormPage, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint=(0.6, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Formulaire de saisie
        self.gpgga_input = TextInput(hint_text="Entrez la trame GPGGA", multiline=False, size_hint=(0.8, 0.2),
                                pos_hint={'center_x': 0.5}, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        save_button = Button(text="Prévisualiser", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5}, background_color=(0.2, 0.6, 0.8, 1))
        save_button.bind(on_press=self.preview_results)

        # Ajout du formulaire et bouton
        layout.add_widget(self.gpgga_input)
        layout.add_widget(save_button)

        # Menu en bas
        about_button = Button(text="À propos de nous", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5}, background_color=(0.3, 0.7, 0.9, 1))
        about_button.bind(on_press=self.show_about)
        layout.add_widget(about_button)

        self.add_widget(layout)

    def preview_results(self, instance):
        gpgga_data = self.gpgga_input.text
        gpgsa = self.convert_gpgga_to_gpgsa(gpgga_data)
        gprmc = self.convert_gpgga_to_gprmc(gpgga_data)

        # Prévisualisation des résultats avant enregistrement
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f"GPGGA: {gpgga_data}"))
        content.add_widget(Label(text=f"GPGSA: {gpgsa}"))
        content.add_widget(Label(text=f"GPRMC: {gprmc}"))

        save_button = Button(text="Enregistrer", size_hint=(1, 0.2), background_color=(0.1, 0.6, 0.2, 1))
        cancel_button = Button(text="Refuser", size_hint=(1, 0.2), background_color=(0.6, 0.1, 0.1, 1))

        save_button.bind(on_press=lambda x: self.save_file(gpgga_data, gpgsa, gprmc))
        cancel_button.bind(on_press=lambda x: self.close_popup())

        content.add_widget(save_button)
        content.add_widget(cancel_button)

        self.popup = Popup(title="Prévisualisation", content=content, size_hint=(0.8, 0.8))
        self.popup.open()

    def save_file(self, gpgga_data, gpgsa, gprmc):
        # Enregistrement dans un fichier .txt
        with open("nmea_output.txt", "w") as f:
            f.write(f"GPGGA: {gpgga_data}\n")
            f.write(f"GPGSA: {gpgsa}\n")
            f.write(f"GPRMC: {gprmc}\n")

        # Confirmation de l'enregistrement
        self.show_confirmation()
        self.close_popup()

    def close_popup(self):
        self.popup.dismiss()

    def show_confirmation(self):
        # Afficher une popup de confirmation
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Fichier enregistré avec succès !"))
        popup = Popup(title="Confirmation", content=content, size_hint=(0.6, 0.3))
        popup.open()

    def convert_gpgga_to_gpgsa(self, gpgga_data):
        # Conversion fictive de GPGGA en GPGSA
        return f"$GPGSA,A,3,{gpgga_data}"

    def convert_gpgga_to_gprmc(self, gpgga_data):
        # Conversion fictive de GPGGA en GPRMC
        return f"$GPRMC,{gpgga_data}"

    def show_about(self, instance):
        # Aller à la page "À propos de nous"
        self.manager.current = 'about_page'

class AboutPage(Screen):
    def __init__(self, **kwargs):
        super(AboutPage, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=30, size_hint=(0.7, 0.7), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Texte descriptif des formats GPGGA, GPGSA et GPRMC et ajout des noms des concepteurs
        about_label = Label(text="Formats NMEA :\n\n"
                                 "1. GPGGA : Données de position GPS comme latitude, longitude et altitude.\n"
                                 "2. GPGSA : Données sur l'état du récepteur GPS et les satellites utilisés.\n"
                                 "3. GPRMC : Données de navigation (position, vitesse, heure).\n\n"
                                 "Concepteurs :\n"
                                 "1. AGISHA KITULI Ghislain\n"
                                 "2. AKONKWA USHINDI Isaac\n"
                                 "3. Bénédict LUBEMBELA\n"
                                 "4. BIRINGANINE BASEME Destin\n"
                                 "5. CIRHUZA BUMIZI Isaac\n"
                                 "6. JIBU MAROYI Benjamin\n\n"
                                 "Université Catholique de Bukavu, Département de l'informatique en Génie Logiciel.",
                            font_size='16sp', color=(1, 1, 1, 1), halign='center')
        back_button = Button(text="Retour", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5}, background_color=(0.3, 0.6, 0.9, 1))
        back_button.bind(on_press=self.go_back)

        layout.add_widget(about_label)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        # Retourner à la page de formulaire
        self.manager.current = 'form_page'

class NMEAApp(App):
    def build(self):
        # Création du gestionnaire d'écran (ScreenManager)
        sm = ScreenManager()
        sm.add_widget(MainPage(name='main_page'))
        sm.add_widget(FormPage(name='form_page'))
        sm.add_widget(AboutPage(name='about_page'))
        return sm

if __name__ == "__main__":
    NMEAApp().run()
