# -*- coding: utf-8 -*-

# import time
# import datetime

import json
import asyncio

import libs.Utils as md
import requests

md.LoadSettings()

url_base = "https://api.twitch.tv/helix/"
url_clips_base = f"https://www.twitch.tv/{md.TwitchUsername}/clip/"

header = {
    "client-id": f"{md.TwitchClientID}",
    "Authorization": f"Bearer {md.TwitchClientSecret}"
}

global msg
global errorBoolean
global sts_code

msg = ""
errorBoolean = False
sts_code = None

def getUserID(username: str):
    url = "{}users?login={}".format(url_base, username)

    global errorBoolean
    global msg
    global user_id

    
    try:
        errorBoolean = False
        r = requests.get(url, headers=header)
        user_id = r.json()["data"][0]["id"]
        return user_id
    except IndexError as e:
        errorBoolean = True
        msg = "Error... User not found!"

user_id = getUserID(f"{md.TwitchUsername}")

def modifyChannel(game_id, live_title, broadcaster_language):
    global errorBoolean
    global msg

    url = "{}channels?broadcaster_id={}".format(url_base, user_id)

    payload = {
        "game_id": f"{game_id}", "title": f"{live_title}", 
        "broadcaster_language": f"{broadcaster_language}"
    }
    errorBoolean = False
    r = requests.patch(url, headers={
        "client-id": f"{md.TwitchClientID}",
        "Authorization": f"Bearer {md.TwitchClientSecret}",
        'Content-Type': 'application/json'
    }, json=payload)
    
    sts_code = r.status_code

    # print("Código de resposta:", sts_code)

    if sts_code >= 199 and sts_code <= 299:
        errorBoolean = False
        msg = "Stream Info updated successfully."
    else:
        errorBoolean = True
        msg = f"Error to update Stream Info.\nPossible error: The first three fields are empty\n\nSolution: Fill the empty fields mentioned (3)"

    # return msg

def createClip():
    global errorBoolean
    global msg
    global ClipID

    url = "{}clips?broadcaster_id={}".format(url_base, user_id)

    try:
        errorBoolean = False
        r = requests.post(url, headers={
            "client-id": f"{md.TwitchClientID}",
            "Authorization": f"Bearer {md.TwitchClientSecret}"
        })

        sts_code = r.status_code
        response = r.json()

        ClipID = response["data"][0]["id"]

        # print("Código de resposta:", sts_code)
        if sts_code >= 199 and sts_code <= 299:
            msg = "Clip Created!"
            md.SaveClips(fl=md.LOGS_FILE, d1=f"{url_clips_base}{ClipID}")
            getClip(ClipID)

        # print("Clip ID:", ClipID)

    except KeyError as e:
        print(f"Ocorreu um Erro. {e}")
        errorBoolean = True
        msg = f"{e}"

    # return msg

    # print(response["data"])

def getClip(clipID):
    global errorBoolean
    global msg

    url = "{}clips?id={}".format(url_base, clipID)

    try:
        errorBoolean = False
        r = requests.get(url, headers={
            "client-id": f"{md.TwitchClientID}",
            "Authorization": f"Bearer {md.TwitchClientSecret}"
        })

        sts_code = r.status_code

        response = r.json()

        ClipData = response["data"]
        # ClipID = response["data"][0]["id"]

        print("Get Clip Data:", ClipData)

    except KeyError as e:
        print(f"Ocorreu um Erro. {e}")
        errorBoolean = True
        msg = f"{e}"

    # print("Código de resposta:", sts_code)

    # if sts_code >= 199 and sts_code <= 299:
    #     msg = "Clip Get success"
    # else:
    #     msg = f"Error to Get Clip!"

    # return msg

    # print("Clip Data:", ClipData)

def getSpecsCount(username: str):
    global count
    global errorBoolean
    global msg

    url = "{}streams?user_login={}".format(url_base, username)

    r = requests.get(url, headers=header)
    try:
        errorBoolean = False
        count = r.json()["data"][0]["viewer_count"]
        return count
    except IndexError as e:
        errorBoolean = True
        msg = f"Error to get viewers!\nPossible error: Your live stream is offline\n\nSolution: Start your Live Stream!"

def createRewards(title: str, cost: int, prompt = None, is_enabled = True, 
    background_color = "#453C67", is_user_input_required = True, 
    is_max_per_stream_enabled = False, max_per_stream = False, 
    is_max_per_user_per_stream_enabled = False, max_per_user_per_stream = False, 
    is_global_cooldown_enabled = False, global_cooldown_seconds = 0, 
    should_redemptions_skip_request_queue = False):

    payload = {"title": f"{title}", "cost": f"{cost}", "prompt": f"{prompt}", "is_enabled": f"{is_enabled}", 
    "background_color": f"#453C67", "is_user_input_required": f"{is_user_input_required}", 
    "is_max_per_stream_enabled": f"{is_max_per_stream_enabled}", "max_per_stream": f"{max_per_stream}", 
    "is_max_per_user_per_stream_enabled": f"{is_max_per_user_per_stream_enabled}", "max_per_user_per_stream": f"{max_per_user_per_stream}", 
    "is_global_cooldown_enabled": f"{is_global_cooldown_enabled}", "global_cooldown_seconds": f"{global_cooldown_seconds}", 
    "should_redemptions_skip_request_queue": f"{should_redemptions_skip_request_queue}"}
    url = "{}channel_points/custom_rewards?broadcaster_id={}".format(url_base, user_id)
    r = requests.post(url, headers={
        "client-id": f"{md.TwitchClientID}",
        "Authorization": f"Bearer {md.TwitchClientSecret}",
        'Content-Type': 'application/json'
        }, json=payload)

    global response
    global sts_code
    response = r.json()

    sts_code = None

    if r.status_code == 200:
        sts_code = f"Reward Created"
    elif r.status_code == 400:
        sts_code = f"Error 400. {response}"
    elif r.status_code == 401:
        sts_code = f"Error 401. {response}"
    elif r.status_code == 403:
        sts_code = f"Error 403. {response}"
    elif r.status_code == 500:
        sts_code = f"Error 500. {response}"
    
    print(response)

def getAllRewards():
    global result

    username = getUserID(md.TwitchUsername)
    url = "{}channel_points/custom_rewards?broadcaster_id={}".format(url_base, username)

    r = requests.get(url, headers=header)
    result = r.json()["data"]
    print("Rewards:", result)

    print("Response Code: ", r.status_code)

def startCommercial(length: int):
    global errorBoolean
    global msg
    global retry_timer

    RETRY_AFTER = 10

    url = "{}channels/commercial".format(url_base)
    
    payload = {
        "broadcaster_id": f"{getUserID(md.TwitchUsername)}",
        "length": length
    }

    errorBoolean = False

    r = requests.post(url, headers={
        "client-id": f"{md.TwitchClientID}",
        "Authorization": f"Bearer {md.TwitchClientSecret}",
        'Content-Type': 'application/json'
    }, json=payload)


    sts_code = r.status_code
    response = r.json()

    # Verificar pela ciscustancia caso o tempo do AD for mais de 180 
    # se irá retornar um tempo maior para o proximo AD

    if sts_code == 200:
        errorBoolean = False
        retry_timer = response["data"][0]["retry_after"]
        msg = f"Starting commercial break. Keep in mind you are still live and not all viewers will receive a commercial. You can run another AD in {retry_timer} seconds"
    elif sts_code == 400:
        errorBoolean = True
        msg = f"Bad Request."
    elif sts_code == 401:
        errorBoolean = True
        msg = f"Unauthorized."
    elif sts_code == 404:
        errorBoolean = True
        msg = f"Not Found."
    elif sts_code == 429:
        errorBoolean = True
        msg = f"Too Many Requests. Try again in {RETRY_AFTER} Minutes"

    else: 
        msg = f"Response Code: {sts_code}"
    # print(f"Response Code: {sts_code}")