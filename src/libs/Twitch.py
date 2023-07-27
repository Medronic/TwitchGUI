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

        self.ClipID = None

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
            self.msg = f"{md.Msgs_E_getUserID_KeyError}"
            return self.msg
        
        # Quando o username fornecido não existir!
        except IndexError as e:
            self.errorBool = True
            self.msg = f"{md.Msgs_E_getUserID_IndexError}"
            return self.msg
        
    def getChannelFollows(self):
        url = "{}channels/followers?broadcaster_id={}".format(APIS_URL["BASE"], self.getUserID(md.TwitchUsername))
        
        try:
            self.errorBool = False
            r = requests.get(url, headers=self.Headers)
            self.msg = r.json()["total"]
            return f"{md.Msgs_S_getChannelFollows}".format(self.msg)
        except KeyError as e:
            print(f"{md.Msgs_E_getChannelFollows_KeyError}")
    
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
            self.msg = f"{md.Msgs_E_getViewersList_KeyError}"
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
            self.msg = f"{md.Msgs_E_banUser_IndexError}"

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
            self.msg = f"{md.Msgs_S_unBanUser}".format(viewer)
            return self.msg

    def getBannedList(self):

        broadcaster_id = self.getUserID(md.TwitchUsername)

        url = "{}moderation/banned?broadcaster_id={}".format(APIS_URL["BASE"], broadcaster_id)

        response = requests.get(url, headers=self.Headers)

        self.ViewersBannedList = response
        if response.status_code == 200:
            return self.ViewersBannedList.json()["data"]
        else:
            self.msg = f"{md.Msgs_E_getBannedList_ec}"
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
            self.msg = f"{md.Msgs_S_modifyChannel}"
        else:
            self.errorBool = True
            self.msg = f"{md.Msgs_E_modifyChannel_ec}"

        return self.msg

    def createClip(self):
    
        user_id = self.getUserID(f"{md.TwitchUsername}")

        url = "{}clips?broadcaster_id={}".format(APIS_URL["BASE"], user_id)

        payload = {
            "has_delay": False
        }

        try:
            self.errorBool = False
            r = requests.post(url, headers=self.Headers, json=payload)

            self.sts_code = r.status_code
            response = r.json()

            self.ClipID = response["data"][0]["id"]

            if self.sts_code >= 199 and self.sts_code <= 299:
                self.msg = f"{md.Msgs_S_createClip}"
                # md.SaveFile(fileName=md.CLIPS_FILE, d1=f"")
                self.getClip(self.ClipID)

            print("Clip ID:", self.ClipID)

        except KeyError as e:
            # print(f"{md.Msgs_E_createClip_KeyError}")
            self.errorBool = True
            self.msg = f"{md.Msgs_E_createClip_KeyError}"

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
            # print(f"{md.Msgs_E_getClip_KeyError}")
            self.errorBool = True
            self.msg = f"{md.Msgs_E_getClip_KeyError}"

    def getSpecsCount(self, username: str):

        url = "{}streams?user_login={}".format(APIS_URL["BASE"], username)

        r = requests.get(url, headers=self.Headers)
        try:
            self.errorBool = False
            count = r.json()["data"][0]["viewer_count"]
            return count
        except IndexError as e:
            self.errorBool = True
            self.msg = f"{md.Msgs_E_getSpecsCount_IndexError}"
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
            self.msg = f"{md.Msgs_S_startCommercial}".format(retry_timer)
            
        elif self.sts_code == 400:
            self.errorBool = True
            self.msg = f"{md.Msgs_E_startCommercial_c400}"
        elif self.sts_code == 401:
            self.errorBool = True
            self.msg = f"{md.Msgs_E_startCommercial_c401}"
        elif self.sts_code == 404:
            self.errorBool = True
            self.msg = f"{md.Msgs_E_startCommercial_c404}"
        elif self.sts_code == 429:
            self.errorBool = True
            self.msg = f"{md.Msgs_E_startCommercial_c429}"
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
                self.msg = f"{md.Msgs_S_sendWhispers}".format(para, paraID)
            else:
                self.msg = f"{md.Msgs_E_sendWhispers_ec}"
            return self.msg

        except KeyError as e:
            # print(f"{md.Msgs_E_sendWhispers_KeyError}")
            self.errorBool = True
            self.msg = f"{md.Msgs_E_sendWhispers_KeyError}"

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
            self.msg = f"{md.Msgs_S_ClearChat}"
            return self.msg
        else:
            self.errorBool = True
            self.msg = f"{md.Msgs_E_ClearChat_ec}"
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
                self.msg = f"{md.Msgs_S_StartRaid}"
            return self.msg
        except KeyError as e:
            # print(f"{md.Msgs_E_StartRaid_KeyError}")
            self.errorBool = True
            self.msg = f"{md.Msgs_E_StartRaid_KeyError}"

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
            self.msg = f"{md.Msgs_S_CancelRaid}"
            return self.msg
        elif self.sts_code == 404:
            self.errorBool = False
            self.msg = f"{md.Msgs_E_CancelRaid_c404}"
            return self.msg