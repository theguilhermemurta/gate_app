##############################################
################ Bibliotecas #################
##############################################

import kivy

from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image





##############################################
################ Classes #####################
##############################################

class HomeScreen(Screen):
	pass
class SettingScreen(Screen):
	pass
class ImageButton(ButtonBehavior, Image):
	pass



GUI = Builder.load_file("main.kv")
class MainApp(App):
	def build(self):
		return GUI

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