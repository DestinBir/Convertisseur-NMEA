from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooser
from kivy.core.window import Window

# Modifier les couleurs du fond
Window.clearcolor = (0.05, 0.05, 0.15, 1)  # Bleu-marine

class MainPage(BoxLayout):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Page d'accueil
        self.home_label = Label(text="Bienvenue dans le convertisseur NMEA", font_size='24sp', color=(1, 1, 1, 1))
        self.start_button = Button(text="Commencer", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        self.start_button.bind(on_press=self.show_form)

        # Ajouter les éléments à l'interface
        self.add_widget(self.home_label)
        self.add_widget(self.start_button)

    def show_form(self, instance):
        # Effacer la page d'accueil et montrer le formulaire
        self.clear_widgets()
        self.gpgga_input = TextInput(hint_text="Entrez la trame GPGGA", multiline=False, size_hint=(0.8, 0.2),
                                     pos_hint={'center_x': 0.5}, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        self.save_button = Button(text="Enregistrer", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        self.save_button.bind(on_press=self.ask_permission)

        # Ajout du formulaire
        self.add_widget(self.gpgga_input)
        self.add_widget(self.save_button)

    def ask_permission(self, instance):
        # Demande de permission pour sauvegarder le fichier
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Voulez-vous enregistrer la trame dans un fichier .txt ?"))
        save_button = Button(text="Oui", size_hint=(1, 0.2))
        save_button.bind(on_press=self.save_file)
        content.add_widget(save_button)

        popup = Popup(title="Demande d'autorisation", content=content, size_hint=(0.8, 0.5))
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
        popup.open()

    def convert_gpgga_to_gpgsa(self, gpgga_data):
        # Conversion fictive de GPGGA en GPGSA
        gpgsa = f"$GPGSA,A,3,{gpgga_data}"
        return gpgsa

    def convert_gpgga_to_gprmc(self, gpgga_data):
        # Conversion fictive de GPGGA en GPRMC
        gprmc = f"$GPRMC,{gpgga_data}"
        return gprmc

class NMEAApp(App):
    def build(self):
        return MainPage()

if __name__ == "__main__":
    NMEAApp().run()
