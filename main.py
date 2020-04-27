##############################################
################ Bibliotecas #################
##############################################

import kivy
import requests
import json

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label 
from kivy.properties import StringProperty


from fb import Firebase




##############################################
################ Classes #####################
##############################################

class HomeScreen(Screen):
    pass
class SettingScreen(Screen):
    pass
class LoginScreen(Screen):
    pass    
class CreateScreen(Screen):
    pass
class ImageButton(ButtonBehavior, Image):
    pass
class LabelButton(ButtonBehavior, Label):
    pass
class ContentNavigationDrawer(BoxLayout):
    pass

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color



        #self.home_screen.ids.screen_manager_nd.current = instance_item

        
class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    target = StringProperty()




class MainApp(MDApp):
    name = ""
    gate = ""

    def build(self):
        self.theme_cls.primary_palette = "DeepOrange"
        GUI = Builder.load_file("main.kv")
        self.my_firebase = Firebase()
        return GUI

    def openScreen(self, itemdrawer):
        self.openScreenName(itemdrawer.target)
        self.root.ids.home_screen.ids.nav_drawer.set_state("close")

    def openScreenName(self, screenName):
        self.root.ids.home_screen.ids.screen_manager_nd.current = screenName

    def loadNdIcons(self, name):
        print("ESTAMOS AQUI")
        self.root.ids.home_screen.ids.content_drawer.ids.drawerlogo.text = name     

        self.root.ids.home_screen.ids.content_drawer.ids.md_list.add_widget(
            ItemDrawer(target="gate_camera", text="Portão",
                   icon="star",
                   on_release=self.openScreen)
        )

        self.root.ids.home_screen.ids.content_drawer.ids.md_list.add_widget(
            ItemDrawer(target="config", text="Configurações",
                    icon="settings-outline",
                    on_release=self.openScreen)
        )

    def on_start(self):
        
        # try to read the permisten signin credentials (refresh token)
        try:
            with open("refresh_token.txt", "r") as f:
                refresh_token = f.read()

            # Use refresh token to get a new idToken
            id_token, local_id = self.my_firebase.exchange_refresh_token(refresh_token)
    
            # Get database data
            results = requests.get("https://gate-app-4d436.firebaseio.com/"+ local_id +".json?auth=" + id_token)
            data = json.loads(results.content.decode())
            gate = data['gate']
            name = data['name']

             # Navigation Drawer
            self.loadNdIcons(name)

           
            self.change_screen("home_screen")


            
        except:
            pass

    def change_screen(self, screen_name):
        # Get the screen manager from the kv file
        # root representa o "pai" no arquivo kv
        screen_manager = self.root.ids['screen_manager']
        # modificando a tela atual para setting
        screen_manager.current = screen_name

    def open_gate(self):
        print("Abrir")

    def close_gate(self):
        print("Fechar")


##############################################
################ Funções #####################
##############################################






##############################################
################ Código ######################
##############################################


if __name__ == '__main__':
    MainApp().run()