import json

import requests
import PySimpleGUI

import libs.Utils as md

APIS_URL = {
    "BASE": "https://api.twitch.tv/helix/",
    "TMI": "https://tmi.twitch.tv/group/user/{}/chatters",
    "CLIP": "https://www.twitch.tv/{}/clip"
}

class Twitch:

    def __init__(self, TwUsername, TwAccessToken, TwClientID, TwClientSecret):
        self.Account = TwUsername
        self.AccessToken = TwAccessToken
        self.ClientID = TwClientID
        self.ClientSecret = TwClientSecret

        self.Headers = {
            "client-id": self.ClientID,
            "Authorization": f"Bearer {self.AccessToken}",
            'Content-Type': 'application/json'
        }

        self.ViewersList = None
        self.ViewersBannedList = None

        self.msg = ""
        self.errorBool = False
        self.sts_code = None

    # Working
    def getUserID(self, username: str):

        url = "{}users?login={}".format(APIS_URL["BASE"], username)
        
        try:
            self.errorBool = False
            r = requests.get(url, headers=self.Headers)
            user_id = r.json()["data"][0]["id"]
            return user_id

        # Possivelmente um erro de Autorização!
        except KeyError as e:
            self.errorBool = True
            self.msg = """Ocorreu um erro! Possível causa:\n
            
            - Errro de Autorização."""
            return self.msg
        
        # Quando o username fornecido não existir!
        except IndexError as e:
            self.errorBool = True
            self.msg = """Ocorre um erro! Possível causa:\n
            
            - Usuário fornecido não existe."""
            return self.msg
        
    def getChannelFollows(self):
        url = "{}channels/followers?broadcaster_id={}".format(APIS_URL["BASE"], self.getUserID(md.TwitchUsername))
        
        try:
            self.errorBool = False
            r = requests.get(url, headers=self.Headers)
            self.msg = r.json()["total"]
            return f"Total of Follows: {self.msg}"
        except KeyError as e:
            print("Ocorreu um erro.")
    
    # Not Working
    def getViewersList(self):
        try:
            self.errorBool = False
            r = requests.get(APIS_URL["TMI"].format("medronic"), headers=self.Headers)
            self.sts_code = r.status_code
            response = r.json()
            
            self.ViewersList = response["chatters"]["viewers"]
            
            # print(viewers)

        except IndexError as e:
            self.errorBool = True
            self.msg = f"""Erro ao pegar a lista de Espectadores!\n\nPossível causa: Sua transmissão está Offline\n\nSolution: Inicie sua Transmissão!"""
            return self.msg
                
    def banUser(self, viewer: str = "", reason: str = "", duration: int = ""):

        viewer_id = self.getUserID(viewer)
        broadcaster_id = self.getUserID(md.TwitchUsername)
        url = "{}moderation/bans?broadcaster_id={}&moderator_id={}".format(APIS_URL["BASE"], broadcaster_id, broadcaster_id)
        try:
            self.errorBool = False
            payload = {
            "data": {
                "user_id": f"{viewer_id}", "reason": f"{reason}"
                }
            }

            r = requests.post(url, headers=self.Headers,
                              json=payload)

            response = r.json()

            print(response)
        except IndexError as e:
            self.errorBool = True
            self.msg = f"""Ocorreu um erro! \n\nMotivo:\n
            
            Você não selecionou alguém a ser banido!"""

    def unBanUser(self, viewer: str = ""):
        viewer_id = self.getUserID(viewer)
        broadcaster_id = self.getUserID(md.TwitchUsername)
        url = "{}moderation/bans?broadcaster_id={}&moderator_id={}&user_id={}".format(APIS_URL["BASE"], broadcaster_id, broadcaster_id, viewer_id)

        r = requests.delete(url, headers={
            "client-id": f"{md.TwitchClientID}",
            "Authorization": f"Bearer {md.TwitchAccessToken}"
        })

        self.sts_code = r.status_code

        if self.sts_code == 204:
            self.errorBool = False
            self.msg = """Usuário desbanido com sucesso!"""
            return self.msg

    def getBannedList(self):

        broadcaster_id = self.getUserID(md.TwitchUsername)

        url = "{}moderation/banned?broadcaster_id={}".format(APIS_URL["BASE"], broadcaster_id)

        response = requests.get(url, headers=self.Headers)

        self.ViewersBannedList = response
        if response.status_code == 200:
            return self.ViewersBannedList.json()["data"]
        else:
            self.msg = """Ocorreu um erro ao listar os usuários banidos."""
            return self.msg

    def modifyChannel(self, game_id, live_title, broadcaster_language):

        user_id = self.getUserID(f"{md.TwitchUsername}")

        url = "{}channels?broadcaster_id={}".format(APIS_URL["BASE"], user_id)

        payload = {
            "game_id": f"{game_id}", "title": f"{live_title}", 
            "broadcaster_language": f"{broadcaster_language}"
        }

        self.errorBool = False
        r = requests.patch(url, headers=self.Headers, json=payload)
        
        self.sts_code = r.status_code

        if self.sts_code >= 199 and self.sts_code <= 299:
            self.errorBool = False
            self.msg = """Alterações feitas com sucesso!"""
        else:
            self.errorBool = True
            self.msg = f"""Erro ao atualizar informações da transmissão.\n Possível causa: Os primeiro campo está vázio\n\n Solução: Preencha o campo mencionado (3)"""

        return self.msg

    def createClip(self):
    
        user_id = self.getUserID(f"{md.TwitchUsername}")

        url = "{}clips?broadcaster_id={}".format(APIS_URL["BASE"], user_id)

        try:
            self.errorBool = False
            r = requests.post(url, headers=self.Headers)

            self.sts_code = r.status_code
            response = r.json()

            ClipID = response["data"][0]["id"]

            if self.sts_code >= 199 and self.sts_code <= 299:
                self.msg = "Clip Criado!"
                # md.SaveClips(fl=md.LOGS_FILE, d1="{}{}").format(APIS_URL["CLIP"], ClipID)
                self.getClip(ClipID)

            print("Clip ID:", ClipID)

        except KeyError as e:
            print(f"Ocorreu um Erro. {e}")
            self.errorBool = True
            self.msg = f"{e}"

    def getClip(self, clipID):

        url = "{}clips?id={}".format(APIS_URL["BASE"], clipID)

        try:
            self.errorBool = False
            r = requests.get(url, headers=self.Headers)

            self.sts_code = r.status_code

            response = r.json()

            ClipData = response["data"]
            # ClipID = response["data"][0]["id"]

            print("Get Clip Data:", ClipData)

        except KeyError as e:
            print(f"Ocorreu um Erro. {e}")
            self.errorBool = True
            self.msg = f"{e}"

    def getSpecsCount(self, username: str):

        url = "{}streams?user_login={}".format(APIS_URL["BASE"], username)

        r = requests.get(url, headers=self.Headers)
        try:
            self.errorBool = False
            count = r.json()["data"][0]["viewer_count"]
            return count
        except IndexError as e:
            self.errorBool = True
            self.msg = f"""Erro ao listar os espectadores!\n\nPossível causa: Sua transmissão está Offline\n\nSolução: Inicie a Transmissão"""
            return self.msg

    def getAllRewards(self):
        global result

        broadcaster_id = self.getUserID(md.TwitchUsername)
        url = "{}channel_points/custom_rewards?broadcaster_id={}".format(APIS_URL["BASE"], broadcaster_id)

        r = requests.get(url, headers=self.Headers)
        result = r.json()["data"]
        print("Rewards:", result)

        print("Response Code: ", r.status_code)

    def startCommercial(self, length: int):
        global retry_timer

        RETRY_AFTER = 10

        url = "{}channels/commercial".format(APIS_URL["BASE"])
        
        payload = {
            "broadcaster_id": f"{self.getUserID(md.TwitchUsername)}",
            "length": length
        }

        self.errorBool = False

        r = requests.post(url, headers=self.Headers, json=payload)

        self.sts_code = r.status_code
        response = r.json()

        if self.sts_code == 200:
            self.errorBool = False
            retry_timer = response["data"][0]["retry_after"]
            self.msg = f"Iniciando o comercial. Você pode executar outro anúncio em {retry_timer} segundos"
            
        elif self.sts_code == 400:
            self.errorBool = True
            self.msg = f"Bad Request."
        elif self.sts_code == 401:
            self.errorBool = True
            self.msg = f"Unauthorized."
        elif self.sts_code == 404:
            self.errorBool = True
            self.msg = f"Not Found."
        elif self.sts_code == 429:
            self.errorBool = True
            self.msg = f"Muitas tentativas. Tente novamente em {RETRY_AFTER} Segundos"
        else: 
            self.msg = f"Response Code: {self.sts_code}"
        return self.msg

    def sendWhispers(self, de: str, para: str, mensagem: str):

        deID = self.getUserID(de)
        paraID = self.getUserID(para)

        url = "{}whispers?from_user_id={}&to_user_id={}".format(APIS_URL["BASE"], deID, paraID)

        payload = {
            "message": f"{mensagem}"
        }

        try:
            self.errorBool = False
            r = requests.post(url, headers=self.Headers, json=payload)

            self.sts_code = r.status_code

            print("Código de resposta:", self.sts_code)
            if self.sts_code == 204:
                self.msg = f"""Mensagem foi enviada com sucesso! Usuário: {para} | ID: {paraID}"""
            else:
                self.msg = f"""Ocorreu um erro ao enviar a mensagem\n"""
            return self.msg

        except KeyError as e:
            print(f"Ocorreu um Erro. {e}")
            self.errorBool = True
            self.msg = f"{e}"

    def ClearChat(self):
        broadcaster_id = self.getUserID(md.TwitchUsername)
        url = "{}moderation/chat?broadcaster_id={}&moderator_id={}".format(APIS_URL["BASE"], broadcaster_id, broadcaster_id)

        r = requests.delete(url, headers={
            "client-id": f"{md.TwitchClientID}",
            "Authorization": f"Bearer {md.TwitchAccessToken}"
        })

        self.sts_code = r.status_code

        if self.sts_code == 204:
            self.errorBool = False
            self.msg = """Todas as mensagens do chat foram deletadas com sucesso!"""
            return self.msg
        else:
            self.errorBool = True
            self.msg = """Ocorreu algum erro ao tentar limpar o chat"""
            return self.msg
        
    def StartRaid(self, to_broadcaster: str):
        from_broadcaster_id = self.getUserID(md.TwitchUsername)
        to_broadcaster_id = self.getUserID(to_broadcaster)
        url = "{}raids?from_broadcaster_id={}&to_broadcaster_id={}".format(APIS_URL["BASE"], from_broadcaster_id, to_broadcaster_id)

        payload = {

        }

        try:
            self.errorBool = False
            r = requests.post(url, headers=self.Headers) #, json=payload

            self.sts_code = r.status_code

            if self.sts_code == 200:
                self.msg = f"""A raid foi iniciada com sucesso! Streamer: {to_broadcaster}"""
            return self.msg
        except KeyError as e:
            print(f"Ocorreu um Erro. {e}")
            self.errorBool = True
            self.msg = f"{e}"

    def CancelRaid(self):
        broadcaster_id = self.getUserID(md.TwitchUsername)
        url = "{}raids?broadcaster_id={}".format(APIS_URL["BASE"], broadcaster_id)

        r = requests.delete(url, headers={
            "client-id": f"{md.TwitchClientID}",
            "Authorization": f"Bearer {md.TwitchAccessToken}"
        })

        self.sts_code = r.status_code

        if self.sts_code == 204:
            self.errorBool = False
            self.msg = """Raid cancelada com sucesso!"""
            return self.msg
        elif self.sts_code == 404:
            self.errorBool = False
            self.msg = """"Ocorreu um erro ao tentar cancelar a Raid!\n\n Motivo: A invasão já foi enviada ou não existe."""
            return self.msg