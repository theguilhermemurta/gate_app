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
class CreateScreen(Screen):
	pass
class ImageButton(ButtonBehavior, Image):
	pass
class LabelButton(ButtonBehavior, Label):
	pass




GUI = Builder.load_file("main.kv")
class MainApp(App):
	def build(self):
		self.my_firebase = Firebase()
		return GUI

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