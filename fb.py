import requests 
import json

from kivy.app import App

class Firebase():

	wak = "AIzaSyA1bZHAQQ5p2ME459ILNpg1I6E0llGau78" # Web API Key

	def sign_up(self, name, email, password):
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
			my_data = '{"name": "%s", "gate": "0"}' % name  #it has to be a string
			print(my_data)
			requests.patch("https://gate-app-4d436.firebaseio.com/" + localId + ".json?auth=" + idToken, data = my_data)

			app.change_screen("home_screen")

		elif signup_request.ok == False:
			error_data = json.loads(signup_request.content.decode())
			error_message = error_data["error"]["message"]
			app.root.ids['login_screen'].ids['login_message'].text = error_message

		
 
	def exchange_refresh_token(self, refresh_token):
		refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.wak
		refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
		refresh_req = requests.post(refresh_url, data = refresh_payload)
		#print("Request ok????", refresh_req.ok)
		#print(refresh_req.json())

		id_token = refresh_req.json()['id_token']
		local_id = refresh_req.json()['user_id']


		return id_token, local_id
	



	def sign_in(self, email, password):
		app = App.get_running_app()
		signin_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.wak
		signin_payload = {"email": email, "password": password, "returnSecureToken": True}
		signin_request = requests.post(signin_url, data = signin_payload)
		sign_in_data = json.loads(signin_request.content.decode())

		if signin_request.ok == True:
			refresh_token = sign_in_data['refreshToken']
			localId = sign_in_data['localId']
			idToken = sign_in_data['idToken']
			# Save refreshToken to a file
			with open("refresh_token.txt", "w") as f:
				f.write(refresh_token)
			# Save localId to a variable in main app class
			app.local_id = localId
			# Save idToken to a variable in main app class
			app.id_token = idToken

			app.change_screen("home_screen")

		elif signin_request.ok == False:
			error_data = json.loads(signin_request.content.decode())
			error_message = error_data["error"]["message"]
			app.root.ids['login_screen'].ids['login_message'].text = error_message