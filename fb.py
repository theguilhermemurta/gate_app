import requests 
import json
import os
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from kivy.app import App

class Firebase():

    wak = "AIzaSyA1bZHAQQ5p2ME459ILNpg1I6E0llGau78" # Web API Key

    dialog = None

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

            my_data = '{"name": "%s", "gate": "0"}' % name  #it has to be a string
            requests.patch("https://gate-app-4d436.firebaseio.com/" + localId + ".json?auth=" + idToken, data = my_data)

            self.send_verification_email(idToken)

            # Create new key in

            app.change_screen("login_screen")

        elif signup_request.ok == False:
            # Print in a label the error massage
            error_data = json.loads(signup_request.content.decode())
            error_message = error_data["error"]["message"]
            #app.root.ids['login_screen'].ids['login_message'].text = error_message
            self.error_massage(error_message)

        
 
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

            check = self.check_verification(idToken)

            if check == True:
                # Save refreshToken to a file
                with open("refresh_token.txt", "w") as f:
                    f.write(refresh_token)

                # Save localId to a variable in main app class
                # Save idToken to a variable in main app class
                app.local_id = localId
                app.id_token = idToken

                results = requests.get("https://gate-app-4d436.firebaseio.com/"+ localId +".json?auth=" + idToken)
                data = json.loads(results.content.decode())
                gate = data['gate']
                name = data['name']
                app.loadNdIcons(name)
                app.change_screen("home_screen")

            else:

                app.root.ids['login_screen'].ids['login_message'].text = "Email não verificado"
                self.new_verification_popup(idToken)

        else:
            # print in a label the error message
            error_data = json.loads(signin_request.content.decode())
            error_message = error_data["error"]["message"]
            #app.root.ids['login_screen'].ids['login_message'].text = error_message
            self.error_message(error_message)

        
            

    def gate_config(self):
        app = App.get_running_app()

        try:
            with open("refresh_token.txt", "r") as f:
                refresh_token = f.read()
            # Use refresh token to get a new idToken
            id_token, local_id = self.exchange_refresh_token(refresh_token)

            # Get database data
            results = requests.get("https://gate-app-4d436.firebaseio.com/"+ local_id +".json?auth=" + id_token)
            data = json.loads(results.content.decode())
            name = data['name']
            my_data = '{"name": "%s", "gate": "%s"}' %(name, gate)
            sent_req = requests.patch("https://gate-app-4d436.firebaseio.com/" + local_id + ".json?auth=" + id_token, data = my_data)
            print(json.loads(sent_req.content.decode()))
            
        except:
            print("FAILED")
            pass

    def log_out(self):
        app = App.get_running_app()

        try:
            with open("refresh_token.txt", "w") as f:
                f.write("")
            print("ESTOU AQUI")
            app.change_screen("login_screen")
        except: 
            print("FAILED IN LOGOUT")


    # Função que envia o códico de verificação para o email
    def send_verification_email(self, idToken):

        url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key=" + self.wak
        vemail_payload = '{"requestType":"VERIFY_EMAIL","idToken":"%s"}' % idToken
        vemail_request = requests.post(url, data = vemail_payload)


    # Confere se o email foi verificado. Para isso recolhe infomação sobre o usuário no firabase
    # esses dados estão em json 
    def check_verification(self, idToken):

        url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=" + self.wak
        check_payload = '{"idToken":"%s"}' % idToken
        check_request = requests.post(url, data = check_payload)
        print(check_request)
        check_data = json.loads(check_request.content.decode())
    
        return check_data['users'][0]['emailVerified']


    # Popup que indica que o email não foi verificado, permite que seja enviado novamente o código
    def new_verification_popup(self, idToken):
        app = App.get_running_app()

        v_popup = MDDialog(title = "Email não verificado!", text= "Deseja que seja enviado outro email?",
                            size_hint = [.25, .25], 
                            buttons=[
                                MDFlatButton(
                                    text="CANCEL", text_color=app.theme_cls.primary_color),
                                MDRaisedButton(
                                    text="ACCEPT", text_color=app.theme_cls.primary_color, on_release = lambda x: self.send_verification_email(idToken))
                                    ]
                            )
        v_popup.open()

    # Função que cria um popup mostrando o erro no login e na criação de contas
    def error_message(self, message):

        error_popup = MDDialog(title = "Error", text= message,
                            size_hint = [.25, .25])
        error_popup.open()

    def config_gate(self, idToken):
        pass


               





# GATE_CONFIG tirei gate.text
