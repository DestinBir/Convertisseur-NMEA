from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

# Modifier les couleurs du fond
Window.clearcolor = (0.05, 0.05, 0.15, 1)  # Bleu-marine

class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Page d'accueil
        home_label = Label(text="Bienvenue dans le convertisseur NMEA", font_size='24sp', color=(1, 1, 1, 1))
        start_button = Button(text="Commencer", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.3})
        start_button.bind(on_press=self.show_form)

        # Ajouter les éléments à l'interface
        layout.add_widget(home_label)
        layout.add_widget(start_button)
        self.add_widget(layout)

    def show_form(self, instance):
        # Aller à la page de formulaire
        self.manager.current = 'form_page'

class FormPage(Screen):
    def __init__(self, **kwargs):
        super(FormPage, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Formulaire de saisie
        gpgga_input = TextInput(hint_text="Entrez la trame GPGGA", multiline=False, size_hint=(0.3, 0.1),
                                pos_hint={'center_x': 0.3}, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        save_button = Button(text="Enregistrer", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.3})
        save_button.bind(on_press=self.ask_permission)

        # Ajout du formulaire et bouton
        layout.add_widget(gpgga_input)
        layout.add_widget(save_button)

        # Menu en bas
        about_button = Button(text="À propos de nous", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
        about_button.bind(on_press=self.show_about)
        layout.add_widget(about_button)

        self.gpgga_input = gpgga_input
        self.add_widget(layout)

    def ask_permission(self, instance):
        # Demande de permission pour sauvegarder le fichier
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Voulez-vous enregistrer la trame dans un fichier .txt ?"))
        save_button = Button(text="Oui", size_hint=(0.3, 0.1))
        save_button.bind(on_press=self.save_file)
        content.add_widget(save_button)

        popup = Popup(title="Demande d'autorisation", content=content, size_hint=(0.8, 0.5))
        close_button = Button(text="Non", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def save_file(self, instance):
        # Enregistrement dans un fichier .txt
        gpgga_data = self.gpgga_input.text
        gpgsa = self.convert_gpgga_to_gpgsa(gpgga_data)
        gprmc = self.convert_gpgga_to_gprmc(gpgga_data)

        with open("nmea_output.txt", "w") as f:
            f.write(f"GPGGA: {gpgga_data}\n")
            f.write(f"GPGSA: {gpgsa}\n")
            f.write(f"GPRMC: {gprmc}\n")

        # Confirmation de l'enregistrement
        self.show_confirmation()

    def show_confirmation(self):
        # Afficher une popup de confirmation
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Fichier enregistré avec succès !"))
        popup = Popup(title="Confirmation", content=content, size_hint=(0.8, 0.3))
        close_button = Button(text="Fermer", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def convert_gpgga_to_gpgsa(self, gpgga_data):
        # Conversion fictive de GPGGA en GPGSA
        gpgsa = f"$GPGSA,A,3,{gpgga_data}"
        return gpgsa

    def convert_gpgga_to_gprmc(self, gpgga_data):
        # Conversion fictive de GPGGA en GPRMC
        gprmc = f"$GPRMC,{gpgga_data}"
        return gprmc

    def show_about(self, instance):
        # Aller à la page "À propos de nous"
        self.manager.current = 'about_page'

class AboutPage(Screen):
    def __init__(self, **kwargs):
        super(AboutPage, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        about_label = Label(text="Nous sommes une équipe dédiée à créer des solutions technologiques innovantes.", 
                            font_size='18sp', color=(1, 1, 1, 1))
        back_button = Button(text="Retour", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
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
