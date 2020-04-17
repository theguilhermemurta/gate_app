import requests 
import json

from kivy.app import App

class Firebase():

	wak = "AIzaSyA1bZHAQQ5p2ME459ILNpg1I6E0llGau78" # Web API Key

	def sign_up(self, email, password):
		app = App.get_running_app()
		# Send email and password to Firebase
		# Firebase will return localID, authToken (your autorization, expire in 1 hour), refreshToken (use to get a new authToken)	
		signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.wak
		signup_payload = {"email": email, "password": password, "returnSecureToken": True}
		signup_request = requests.post(signup_url, data = signup_payload)
		sign_up_data = json.loads(signup_request.content.decode())

		if signup_request.ok == True:
			refresh_token = sign_up_data['refreshToken']
			localId = sign_up_data['localId']
			idToken = sign_up_data['idToken']
			# Save refreshToken to a file
			with open("refresh_token.txt", "w") as f:
				f.write(refresh_token)
			# Save localId to a variable in main app class
			app.local_id = localId
			# Save idToken to a variable in main app class
			app.id_token = idToken
			# Create new key in database from localID
			# Get gate IP
			my_data = '{"gate": "192.168.0.1"}' #it has to be a string
			requests.patch("https://gate-app-4d436.firebaseio.com/" + localId + ".json?auth=" + idToken, data = my_data)

			app.change_screen("home_screen")

		if signup_request.ok == False:
			error_data = json.loads(signup_request.content.decode())
			error_message = error_data["error"]["message"]
			app.root.ids['login_screen'].ids['login_message'].text = error_message

		
 
	def sign_in(self):
		pass