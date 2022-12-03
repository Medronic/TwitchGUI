# -*- coding: utf-8 -*-

# import time
# import datetime

import json

import libs.Utils as md
import requests

md.LoadSettings()

url_base = "https://api.twitch.tv/helix/"

header = {
    "client-id": f"{md.TwitchClientID}",
    "Authorization": f"Bearer {md.TwitchClientSecret}"
}

global errorMsg
global errorBoolean
global sts_code

errorBoolean = False
errorMsg = None
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

# Necessita ser corrigido!
def modifyChannel(game_id, live_title, broadcaster_language):
    global errorBoolean
    global errorMsg

    url = "{}channels?broadcaster_id={}".format(url_base, user_id)

    payload = {
        "game_id": f"{game_id}", "title": f"{live_title}", 
        "broadcaster_language": f"{broadcaster_language}"
    }

    try:
        errorBoolean = False
        r = requests.patch(url, headers={
            "client-id": f"{md.TwitchClientID}",
            "Authorization": f"Bearer {md.TwitchClientSecret}",
            'Content-Type': 'application/json'
            }, json=payload)

    except IndexError as e:
        errorBoolean = True
        errorMsg = f"Ocorreu um erro. O erro é desconhecido."

# Working!
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
    username = getUserID(md.TwitchUsername)
    url = "{}channel_points/custom_rewards?broadcaster_id={}".format(url_base, username)

    r = requests.get(url, headers=header)
    global result
    result = r.json()["data"]
    print(result)

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