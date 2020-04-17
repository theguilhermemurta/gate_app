##############################################
################ Bibliotecas #################
##############################################

import kivy
import requests
import json

from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label 


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
class ImageButton(ButtonBehavior, Image):
	pass
class LabelButton(ButtonBehavior, Label):
	pass




GUI = Builder.load_file("main.kv")
class MainApp(App):
	id = 1   #trocar pelo login 
	def build(self):
		self.my_firebase = Firebase()
		return GUI

	def on_start(self):
		# Get database data
		results = requests.get("https://gate-app-4d436.firebaseio.com/"+ str(self.id)+".json")
		data = json.loads(results.content.decode())
		gate = data['gate']
		print("data has been found", data)
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