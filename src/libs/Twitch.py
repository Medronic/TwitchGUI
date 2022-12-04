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
global errorMsg
global errorBoolean
global sts_code

msg = ""
errorMsg = None
errorBoolean = False
sts_code = None

def getUserID(username: str):
    url = "{}users?login={}".format(url_base, username)

    global user_id
    
    try:
        errorBoolean = False
        r = requests.get(url, headers=header)
        user_id = r.json()["data"][0]["id"]
        return user_id
    except IndexError as e:
        errorBoolean = True
        errorBoolean = "Error... User not found!"

user_id = getUserID(f"{md.TwitchUsername}")

# Aparentemente funcional
def modifyChannel(game_id, live_title, broadcaster_language):
    global msg

    url = "{}channels?broadcaster_id={}".format(url_base, user_id)

    payload = {
        "game_id": f"{game_id}", "title": f"{live_title}", 
        "broadcaster_language": f"{broadcaster_language}"
    }
    r = requests.patch(url, headers={
        "client-id": f"{md.TwitchClientID}",
        "Authorization": f"Bearer {md.TwitchClientSecret}",
        'Content-Type': 'application/json'
    }, json=payload)

    sts_code = r.status_code

    # print("Código de resposta:", sts_code)

    if sts_code >= 199 and sts_code <= 299:
        msg = "Stream Info updated successfully."
    else:
        msg = f"Error to update Stream Info."

    # return msg

def createClip():
    global msg
    global ClipID

    global errorBoolean
    global errorMsg
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
            md.SaveClips(f"{url_clips_base}{ClipID}\n")
            getClip(ClipID)

        # print("Clip ID:", ClipID)

    except KeyError as e:
        print(f"Ocorreu um Erro. {e}")
        errorBoolean = True
        errorMsg = f"{e}"

    # return msg

    # print(response["data"])

def getClip(clipID):
    global msg

    global errorBoolean
    global errorMsg

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
        errorMsg = f"{e}"

    # print("Código de resposta:", sts_code)

    # if sts_code >= 199 and sts_code <= 299:
    #     msg = "Clip Get success"
    # else:
    #     msg = f"Error to Get Clip!"

    # # return msg

    # print("Clip Data:", ClipData)

def getSpecsCount(username: str):
    global count
    global errorBoolean
    global errorMsg

    url = "{}streams?user_login={}".format(url_base, username)

    r = requests.get(url, headers=header)
    try:
        errorBoolean = False
        count = r.json()["data"][0]["viewer_count"]
        return count
    except IndexError as e:
        errorBoolean = True
        errorMsg = f"Error... Maybe you are Offline (Live)"

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
    url = "{}channels/commercial".format(url_base)
    
    payload = {
        "broadcaster_id": "41245072",
        "length": length
    }

    r = requests.post(url, headers={
        "client-id": f"{md.TwitchClientID}",
        "Authorization": f"Bearer {md.TwitchClientSecret}",
        'Content-Type': 'application/json'
        }, json=payload)

    response = r.json()

    print(response)