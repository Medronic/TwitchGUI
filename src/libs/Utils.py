import json
import os
import datetime as dt
import zipfile
from time import sleep

import requests

# DEFINES
LOAD_SETTINGS = "Carregando configurações..."
LOAD_SETTINGS_SUCCESS = "Configurações carregadas com sucesso!"
LOAD_SETTINGS_ERROR = "Erro ao carregar configurações!"

SAVE_SETTINGS = "Salvando configurações..."
SAVE_SETTINGS_SUCCESS = "Configurações salvas com sucesso!"
SAVE_SETTINGS_ERROR = "Erro ao salvar configurações!"

LOGS_FILE = "logs.txt"
CLIPS_FILE = "clips.txt"

date = dt.datetime.now()

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON: {e}")
        return []

LangListName = [
    "",
    "English",
    "Bahasa Indonesia",
    "Català",
    "Dansk",
    "Deutsch",
    "Español",
    "Français",
    "Italiano",
    "Magyar",
    "Nederlands",
    "Norsk",
    "Polski",
    "Português",
    "Română",
    "Slovenčina",
    "Suomi",
    "Svenska",
    "Tagalog",
    "Tiếng Việt",
    "Türkçe",
    "Čeština",
    "Ελληνικά",
    "Български",
    "Русский",
    "Українська",
    "العربية",
    "بهاس ملايو",
    "मानक हिन्दी",
    "ภาษาไทย",
    "中文",
    "日本語",
    "粵語",
    "한국어",
    "American Sign Language",
    "Other"
    ]

LangListIDs = [
    "",
    "en",
    "id",
    "ca",
    "da",
    "de",
    "es",
    "fr",
    "it",
    "hu",
    "nl",
    "no",
    "pl",
    "pt",
    "ro",
    "sk",
    "fi",
    "sv",
    "tl",
    "vi",
    "tr",
    "cs",
    "el",
    "bg",
    "uk",
    "ru",
    "ar",
    "ms",
    "hi",
    "th",
    "zh",
    "ja",
    "zh-hk",
    "ko",
    "asl",
    "other"
]

def SaveFile(fileName, d1=None):
    with open(f"{fileName}", "a", encoding="utf-8") as outfile:
        outfile.write(f"{d1}")

# Função Ler as Configurações e Linguagens
def LoadSettings():
    print("Carregando configurações...")
    SaveFile(fileName=LOGS_FILE, d1=f"{date} Loading settings...\n")

    if os.path.isfile('settings.json'):
        arquivo_json = open('settings.json', 'r', encoding='utf-8')
        data = json.loads(arquivo_json.read())
        
        global AppLanguage
        global AppVersion
        global AppTheme

        global TwitchUsername
        global TwitchAccessToken
        global TwitchClientID
        global TwitchClientSecret

        AppLanguage = data["Settings"]['Application']['Language']
        AppVersion = data["Settings"]['Application']['Version']
        AppTheme = data["Settings"]['Application']['Theme']

        TwitchUsername = data['Settings']['Twitch']['Username']
        TwitchAccessToken = data['Settings']['Twitch']['AccessToken']
        TwitchClientID = data['Settings']['Twitch']['ClientID']
        TwitchClientSecret = data['Settings']['Twitch']['ClientSecret']

        print("Settings loaded successfully!")
        SaveFile(fileName=LOGS_FILE, d1=f"{date} Settings loaded successfully!\n")
    else:
        print("Settings file not found! Creating default settings file...")
        SaveFile(fileName=LOGS_FILE, d1=f"{date} Settings file not found! Creating default settings file...\n")

    print("Loading Languages...")
    SaveFile(fileName=LOGS_FILE, d1=f"{date} Loading Languages...\n")

    if os.path.isfile('languages.json'):
        arquivo_json = open('languages.json', 'r', encoding='utf-8')
        data = json.loads(arquivo_json.read())

        global lngManageStreamTab
        global lngViewersTab
        global lngRewardsTab
        global lngFunctionsTab
        global lngSettingsTab
        global lngAboutTab

        lngManageStreamTab = data[f'{AppLanguage}'][0]['TabGroup']['StreamManager']
        lngViewersTab = data[f'{AppLanguage}'][0]['TabGroup']['Viewers']
        lngRewardsTab = data[f'{AppLanguage}'][0]['TabGroup']['Rewards']
        lngFunctionsTab = data[f'{AppLanguage}'][0]['TabGroup']['Functions']
        lngSettingsTab = data[f'{AppLanguage}'][0]['TabGroup']['Settings']
        lngAboutTab = data[f'{AppLanguage}'][0]['TabGroup']['About']

        global mgtStream_lblGame
        global mgtStream_lblTitle
        global mgtStream_lblGoLiveNotification
        global mgtStream_lblCategory
        global mgtStream_lblAudience
        global mgtStream_lblTags
        global mgtStream_lblStreamLng
        global mgtStream_lblRerun
        global mgtStream_btnChangeStgs

        global mgtStream_lblViewers
        global mgtStream_btnViewersRefresh

        global mgtStream_lblHasDelay
        global mgtStream_lblClipStatus
        global mgtStream_btnCreateClip
        global mgtStream_btnGetClipStatus

        mgtStream_lblGame = data[f'{AppLanguage}'][0]['StreamManager']['Texts']['Game']
        mgtStream_lblTitle = data[f'{AppLanguage}'][0]['StreamManager']['Texts']['Title']
        mgtStream_lblGoLiveNotification = data[f'{AppLanguage}'][0]['StreamManager']['Texts']['GoLiveNotification']
        mgtStream_lblCategory = data[f'{AppLanguage}'][0]['StreamManager']['Texts']['Category']
        mgtStream_lblAudience = data[f'{AppLanguage}'][0]['StreamManager']['Texts']['Audience']
        mgtStream_lblTags = data[f'{AppLanguage}'][0]['StreamManager']['Texts']['Tags']
        mgtStream_lblStreamLng = data[f'{AppLanguage}'][0]['StreamManager']['Texts']['StreamLanguage']
        mgtStream_lblRerun = data[f'{AppLanguage}'][0]['StreamManager']['Texts']['Rerun']
        mgtStream_btnChangeStgs = data[f'{AppLanguage}'][0]['StreamManager']['Buttons']['ChangeSettings']

        mgtStream_lblViewers = data[f'{AppLanguage}'][0]['StreamManager']['Texts']['Viewers']
        mgtStream_btnViewersRefresh = data[f'{AppLanguage}'][0]['StreamManager']['Buttons']['ViewersRefresh']

        mgtStream_lblHasDelay = data[f'{AppLanguage}'][0]['StreamManager']['Texts']['HasDelay']
        mgtStream_lblClipStatus = data[f'{AppLanguage}'][0]['StreamManager']['Texts']['ClipStatus']

        mgtStream_btnCreateClip = data[f'{AppLanguage}'][0]['StreamManager']['Buttons']['CreateClip']
        mgtStream_btnGetClipStatus = data[f'{AppLanguage}'][0]['StreamManager']['Buttons']['GetClipStatus']

        global viewers_lblReason
        global viewers_lblTime
        
        viewers_lblReason = data[f'{AppLanguage}'][0]['Viewers']['Texts']['Reason']
        viewers_lblTime = data[f'{AppLanguage}'][0]['Viewers']['Texts']['Time']

        global viewers_btnViewersList
        global viewers_btnViewersBannedsList
        global viewers_btnBan
        global viewers_btnUnBan
        global viewers_btnTimeout
        global viewers_btnUnTimeout

        viewers_btnViewersList = data[f'{AppLanguage}'][0]['Viewers']['Buttons']['ViewersList']
        viewers_btnViewersBannedsList = data[f'{AppLanguage}'][0]['Viewers']['Buttons']['ViewersBannedsList']
        viewers_btnBan = data[f'{AppLanguage}'][0]['Viewers']['Buttons']['BanUser']
        viewers_btnUnBan = data[f'{AppLanguage}'][0]['Viewers']['Buttons']['UnBanUser']
        viewers_btnTimeout = data[f'{AppLanguage}'][0]['Viewers']['Buttons']['Timeout']
        viewers_btnUnTimeout = data[f'{AppLanguage}'][0]['Viewers']['Buttons']['UnTimeout']
        
        global reward_lblName
        global reward_lblPrice
        global reward_lblMsg
        global reward_lblEnabled
        global reward_lblNeedComment
        global reward_lblMaxPerStream
        global reward_lblMaxPerStreamNumber
        global reward_lblMaxPerUser
        global reward_lblMaxPerUserNumber
        global reward_lblCooldown
        global reward_lblCooldownNumber
        global reward_btnCreate

        reward_lblName = data[f'{AppLanguage}'][0]['Rewards']['Texts']['Name']
        reward_lblPrice = data[f'{AppLanguage}'][0]['Rewards']['Texts']['Price']
        reward_lblMsg = data[f'{AppLanguage}'][0]['Rewards']['Texts']['Message']
        reward_lblEnabled = data[f'{AppLanguage}'][0]['Rewards']['Texts']['Enabled']
        reward_lblNeedComment = data[f'{AppLanguage}'][0]['Rewards']['Texts']['NeedComment']
        reward_lblMaxPerStream = data[f'{AppLanguage}'][0]['Rewards']['Texts']['MaxPerStream']
        reward_lblMaxPerStreamNumber = data[f'{AppLanguage}'][0]['Rewards']['Texts']['MaxPerStreamNumber']
        reward_lblMaxPerUser = data[f'{AppLanguage}'][0]['Rewards']['Texts']['MaxPerUser']
        reward_lblMaxPerUserNumber = data[f'{AppLanguage}'][0]['Rewards']['Texts']['MaxPerUserNumber']
        reward_lblCooldown = data[f'{AppLanguage}'][0]['Rewards']['Texts']['Cooldown']
        reward_lblCooldownNumber = data[f'{AppLanguage}'][0]['Rewards']['Texts']['CooldownNumber']
        reward_btnCreate = data[f'{AppLanguage}'][0]['Rewards']['Buttons']['CreateReward']

        global Stgs_lblTwitchUsername
        global Stgs_lblTwitchAccessToken
        global Stgs_lblTwitchClientID
        global Stgs_lblTwitchClientSecret
        global Stgs_lblLanguage
        global Stgs_btnSave

        Stgs_lblTwitchUsername = data[f'{AppLanguage}'][0]['Settings']['Texts']['Username']
        Stgs_lblTwitchAccessToken = data[f'{AppLanguage}'][0]['Settings']['Texts']['AccessToken']
        Stgs_lblTwitchClientID = data[f'{AppLanguage}'][0]['Settings']['Texts']['ClientID']
        Stgs_lblTwitchClientSecret = data[f'{AppLanguage}'][0]['Settings']['Texts']['ClientSecret']
        Stgs_lblLanguage = data[f'{AppLanguage}'][0]['Settings']['Texts']['Language']
        Stgs_btnSave = data[f'{AppLanguage}'][0]['Settings']['Buttons']['Save']

        global About_lblDescription
        global About_lblAuthor
        global About_lblVersion
        global About_btnCheckUpdates

        global About_lblCheckingUpdate
        global About_lblNoUpdate
        global About_lblUpdateAvailable
        global About_lblErrorToCheck
        global About_lblErrorToDownload
        global About_lblDownloaded
        global About_lblFileUnziped
        global About_lblErrorToUnzip

        About_lblAuthor = data[f'{AppLanguage}'][0]['About']['Texts']['Author']
        About_lblDescription = data[f'{AppLanguage}'][0]['About']['Texts']['Description']
        About_lblVersion = data[f'{AppLanguage}'][0]['About']['Texts']['Version']['Number']
        About_btnCheckUpdates = data[f'{AppLanguage}'][0]['About']['Buttons']['CheckUpdates']

        About_lblCheckingUpdate = data[f'{AppLanguage}'][0]['About']['Texts']['Version']['UpdateMsgs']['Checking']
        About_lblNoUpdate = data[f'{AppLanguage}'][0]['About']['Texts']['Version']['UpdateMsgs']['NoUpdates']
        About_lblUpdateAvailable = data[f'{AppLanguage}'][0]['About']['Texts']['Version']['UpdateMsgs']['UpdateAvailable']
        About_lblErrorToCheck = data[f'{AppLanguage}'][0]['About']['Texts']['Version']['UpdateMsgs']['ErrorToCheck']
        About_lblErrorToDownload = data[f'{AppLanguage}'][0]['About']['Texts']['Version']['UpdateMsgs']['ErrorToDownload']
        About_lblDownloaded = data[f'{AppLanguage}'][0]['About']['Texts']['Version']['UpdateMsgs']['Downloaded']
        About_lblFileUnziped = data[f'{AppLanguage}'][0]['About']['Texts']['Version']['UpdateMsgs']['FileUnziped']
        About_lblErrorToUnzip = data[f'{AppLanguage}'][0]['About']['Texts']['Version']['UpdateMsgs']['ErrorToUnzip']

        # Mensagens de Sucesso

        global Msgs_S_getUserID
        global Msgs_S_getChannelFollows
        global Msgs_S_getViewersList
        global Msgs_S_banUser
        global Msgs_S_unBanUser
        global Msgs_S_getBannedList
        global Msgs_S_modifyChannel
        global Msgs_S_createClip
        global Msgs_S_getClip
        global Msgs_S_getSpecsCount
        global Msgs_S_getAllRewards
        global Msgs_S_startCommercial
        global Msgs_S_sendWhispers
        global Msgs_S_ClearChat
        global Msgs_S_StartRaid
        global Msgs_S_CancelRaid

        Msgs_S_getUserID = data[f'{AppLanguage}'][0]['Msgs']['Success']['getUserID']
        Msgs_S_getChannelFollows = data[f'{AppLanguage}'][0]['Msgs']['Success']['getChannelFollows']
        Msgs_S_getViewersList = data[f'{AppLanguage}'][0]['Msgs']['Success']['getViewersList']
        Msgs_S_banUser = data[f'{AppLanguage}'][0]['Msgs']['Success']['banUser']
        Msgs_S_unBanUser = data[f'{AppLanguage}'][0]['Msgs']['Success']['unBanUser']
        Msgs_S_getBannedList = data[f'{AppLanguage}'][0]['Msgs']['Success']['getBannedList']
        Msgs_S_modifyChannel = data[f'{AppLanguage}'][0]['Msgs']['Success']['modifyChannel']
        Msgs_S_createClip = data[f'{AppLanguage}'][0]['Msgs']['Success']['createClip']
        Msgs_S_getClip = data[f'{AppLanguage}'][0]['Msgs']['Success']['getClip']
        Msgs_S_getSpecsCount = data[f'{AppLanguage}'][0]['Msgs']['Success']['getSpecsCount']
        Msgs_S_getAllRewards = data[f'{AppLanguage}'][0]['Msgs']['Success']['getAllRewards']
        Msgs_S_startCommercial = data[f'{AppLanguage}'][0]['Msgs']['Success']['startCommercial']
        Msgs_S_sendWhispers = data[f'{AppLanguage}'][0]['Msgs']['Success']['sendWhispers']
        Msgs_S_ClearChat = data[f'{AppLanguage}'][0]['Msgs']['Success']['ClearChat']
        Msgs_S_StartRaid = data[f'{AppLanguage}'][0]['Msgs']['Success']['StartRaid']
        Msgs_S_CancelRaid = data[f'{AppLanguage}'][0]['Msgs']['Success']['CancelRaid']

        # Mensagens de Erro

        global Msgs_E_getUserID_KeyError
        global Msgs_E_getUserID_IndexError
        global Msgs_E_getChannelFollows_KeyError
        global Msgs_E_getViewersList_KeyError
        global Msgs_E_banUser_IndexError
        global Msgs_E_getBannedList_ec
        global Msgs_E_modifyChannel_ec
        global Msgs_E_createClip_KeyError
        global Msgs_E_getClip_KeyError
        global Msgs_E_getSpecsCount_IndexError
        global Msgs_E_getAllRewards_ec
        global Msgs_E_startCommercial_c400
        global Msgs_E_startCommercial_c401
        global Msgs_E_startCommercial_c404
        global Msgs_E_startCommercial_c429
        global Msgs_E_sendWhispers_ec
        global Msgs_E_sendWhispers_KeyError
        global Msgs_E_ClearChat_ec
        global Msgs_E_StartRaid_KeyError
        global Msgs_E_CancelRaid_c404
        
        Msgs_E_getUserID_KeyError = data[f'{AppLanguage}'][0]['Msgs']['Error']['getUserID']["KeyError"]
        Msgs_E_getUserID_IndexError = data[f'{AppLanguage}'][0]['Msgs']['Error']['getUserID']["IndexError"]

        Msgs_E_getChannelFollows_KeyError = data[f'{AppLanguage}'][0]['Msgs']['Error']['getChannelFollows']["KeyError"]

        Msgs_E_getViewersList_KeyError = data[f'{AppLanguage}'][0]['Msgs']['Error']['getViewersList']["KeyError"]

        Msgs_E_banUser_IndexError = data[f'{AppLanguage}'][0]['Msgs']['Error']['banUser']["IndexError"]

        Msgs_E_getBannedList_ec = data[f'{AppLanguage}'][0]['Msgs']['Error']['getBannedList']["ec"]

        Msgs_E_modifyChannel_ec = data[f'{AppLanguage}'][0]['Msgs']['Error']['modifyChannel']["ec"]

        Msgs_E_createClip_KeyError = data[f'{AppLanguage}'][0]['Msgs']['Error']['createClip']["KeyError"]

        Msgs_E_getClip_KeyError = data[f'{AppLanguage}'][0]['Msgs']['Error']['getClip']["KeyError"]

        Msgs_E_getSpecsCount_IndexError = data[f'{AppLanguage}'][0]['Msgs']['Error']['getSpecsCount']["IndexError"]

        Msgs_E_getAllRewards_ec = data[f'{AppLanguage}'][0]['Msgs']['Error']['getAllRewards']["ec"]

        Msgs_E_startCommercial_c400 = data[f'{AppLanguage}'][0]['Msgs']['Error']['startCommercial']["c400"]
        Msgs_E_startCommercial_c401 = data[f'{AppLanguage}'][0]['Msgs']['Error']['startCommercial']["c401"]
        Msgs_E_startCommercial_c404 = data[f'{AppLanguage}'][0]['Msgs']['Error']['startCommercial']["c404"]
        Msgs_E_startCommercial_c429 = data[f'{AppLanguage}'][0]['Msgs']['Error']['startCommercial']["c429"]

        Msgs_E_sendWhispers_ec = data[f'{AppLanguage}'][0]['Msgs']['Error']['sendWhispers']["ec"]
        Msgs_E_sendWhispers_KeyError = data[f'{AppLanguage}'][0]['Msgs']['Error']['sendWhispers']["KeyError"]

        Msgs_E_ClearChat_ec = data[f'{AppLanguage}'][0]['Msgs']['Error']['ClearChat']["ec"]

        Msgs_E_StartRaid_KeyError = data[f'{AppLanguage}'][0]['Msgs']['Error']['StartRaid']["KeyError"]

        Msgs_E_CancelRaid_c404 = data[f'{AppLanguage}'][0]['Msgs']['Error']['CancelRaid']["c404"]

        SaveFile(fileName=LOGS_FILE, d1=f"{date} Language Settings successfully loaded!\n")
    else:
        SaveFile(LOGS_FILE, d1=data, d2=f"")
        SaveFile(fileName=LOGS_FILE, d1=f"{date} Language file settings not found! Creating default language file...\n")

# Função verificar por atualizações
def checkUpdate():
    global serverVersion
    global needUpdate
    url = 'https://pastebin.com/raw/CXBiknQT'
    r = requests.get(url)
    serverVersion = float(r.text)

    SaveFile(fileName=LOGS_FILE, d1=f"{date} Checking for updates...\n")
    
    # print("Versão do Servidor:", serverVersion)
    # print("Versão do Programa (Local)", AppVersion)
    
    if AppVersion != serverVersion:
        SaveFile(fileName=LOGS_FILE, d1=f"{date} New version found!\n")
        needUpdate = True
        update()
    else:
        SaveFile(fileName=LOGS_FILE, d1=f"{date} No new version found!\n")
        needUpdate = False

# Função atualizar
def update():
    global folder
    global file_name
    global updateMsg

    updateMsg = ''
    folder = f'Twitch_GUIv{serverVersion}'
    file_name = f'Twitch_GUIv{serverVersion}.zip'

    url = f'https://leavepriv8.com/Softwares/Twitch_GUI/{file_name}'
    r = requests.get(url, allow_redirects=True)
    
    open(f'{file_name}', 'wb').write(r.content)

    updateMsg = f'{About_lblDownloaded}'
    SaveFile(fileName=LOGS_FILE, d1=f"{date} {updateMsg}\n")
    try:
        with zipfile.ZipFile(f'{file_name}','r') as zip_ref:
            zip_ref.extractall(f'{folder}')
            
            sleep(2)
            updateMsg = f'{About_lblFileUnziped}' + folder
            SaveFile(fileName=LOGS_FILE, d1=f"{date} {updateMsg}\n")
    except zipfile.BadZipfile as e:
        print("Bad File")
        updateMsg = "Error (Bad File). Maybe Update URL is invalid!"
        SaveFile(fileName=LOGS_FILE, d1=f"{date} {updateMsg}\n")
        os.remove(f"{file_name}")

# Função Salvar as Configurações
def SaveSettings(lang, theme, TwUsername, TwAccessToken, TwClient, TwSecret):
    data = {}
    data['Settings'] = {'Application': {'Language': lang, 'Version': AppVersion, 'Theme': theme}, 'Twitch': {'Username': TwUsername, 'AccessToken': TwAccessToken, 'ClientID': TwClient, 'ClientSecret': TwSecret}}
    with open('settings.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)