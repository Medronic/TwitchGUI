import webbrowser as web
import os
import asyncio

import libs.Utils as md
import libs.Twitch as ttv
import PySimpleGUI as sg

md.LoadSettings()

sg.theme("DarkPurple4")

ManageStreamTab = [
    [sg.Text(f"{md.mgtStream_lblGame}"), sg.Drop(values=("491487", "491487 - Dead by Daylight",
    "21779 - League of Legends",
    "32982 - Grand Theft Auto V",
    "512953 - Elden Ring",
    "516575 - VALORANT",
    "33214 - Fortnite",
    "511224 - Apex Legends",
    "18122 - World of Warcraft",
    "32399 - Counter-Strike: Global Offensive",
    "490100 - Lost Ark",
    "29595 - Dota 2",
    "490130 - Minecraft",
    "138585 - Hearthstone",
    "263490 - Rust"), default_value="491487", key="stream_game", readonly=True)],
    
    [sg.Text(f"{md.mgtStream_lblTitle}"), sg.Input(key="stream_title", size=(40, 1))],
    [sg.Text(f"{md.mgtStream_lblGoLiveNotification}"), sg.Input(key="stream_goLiveNotification", size=(15, 1))],
    [sg.Text(f"{md.mgtStream_lblCategory}"), sg.Input(key="stream_category", size=(15, 1))],
    [sg.Text(f"{md.mgtStream_lblAudience}"), sg.Drop(values=("Everyone", "Subs Only"), default_value="Everyone", key="stream_audience", readonly=True)],
    [sg.Text(f"{md.mgtStream_lblTags}"), sg.Input(key="stream_tags", size=(15, 1))],
    [sg.Text(f"{md.mgtStream_lblStreamLng}"), sg.Drop(values=("pt","en"), default_value="pt", key="stream_language", readonly=True)],

    [sg.Button(f"{md.mgtStream_btnChangeStgs}", key="change_stream_data", font='15px')],

    [sg.Text("============================== AD ==============================")],
    [sg.Drop(values=("30", "60", "90", "120", "150", "180"), default_value="30", key="ad_time", font=(30), readonly=True), sg.Button('Passar AD', key='start_comercial', size=(12), font='15px')],

    [sg.Text(f"============================ {md.mgtStream_lblViewers} ============================")],
    [sg.Text(f"{md.mgtStream_lblViewers}"), sg.Text("0", key="total_viewers", font='15px'), sg.Button(f"{md.mgtStream_btnViewersRefresh}", key="update_viewers", font='15px')],

    [sg.Text(f"============================ Clip ============================")],
    # [sg.Text(f"{md.mgtStream_lblHasDelay}"), sg.Drop(values=("False", "True"), default_value="False", key="has_delay", readonly=True)],
    [sg.Button(f"{md.mgtStream_btnCreateClip}", key="create_clip")],

    [sg.Text(f"{md.mgtStream_lblClipStatus}"), sg.Input("Your CLIP ID Here", key="clip_id"), sg.Button(f"{md.mgtStream_btnGetClipStatus}", key="get_clip_status")]
    
]

ToolsTab = [
    [sg.Text('User:', key=''), sg.Input(f"teste", key='UserInformation'), sg.Button('Total Seguidores', key='getFollowers', size=(15), font='15px')],
    [sg.Button('Enviar Mensagem', key='send_msg', size=(15), font='15px')],
    [sg.Multiline('123', key='msg', text_color='white', size=(480, 20), font='15px')]
]

SettingsTab = [
    [sg.Text(f"{md.Stgs_lblTwitchUsername}"), sg.Input(f"{md.TwitchUsername}", key="username")],
    [sg.Text(f"{md.Stgs_lblTwitchClientID}"), sg.Input(f"{md.TwitchClientID}", key="ClientID")],
    [sg.Text(f"{md.Stgs_lblTwitchClientSecret}"), sg.Input(
        f"{md.TwitchClientSecret}", key="ClientSecret", password_char='*')],
    
    [sg.Text(f"{md.Stgs_lblLanguage}"), sg.Drop(values=("portuguese", "english"), key="language", default_value=f"{md.AppLanguage}", readonly=True)],
    [sg.Button(f"{md.Stgs_btnSave}", key="save_settings",
               size=(18, 1), font='15px')]
]

AboutTab = [
    [sg.Text(f"{md.About_lblAuthor}", font='15px')],
    [sg.Text(f"{md.About_lblDescription}", font='15px')],
    [sg.Text(f"{md.About_lblVersion} {md.AppVersion}", font='15px'), sg.Button(f"{md.About_btnCheckUpdates}", key="check_for_updates", font='15px')],

    [sg.Text("Update Status:"), sg.Text("...", key="txtExtra", visible=True)]
]

RewardTab = [

    [sg.Text("================ CREATE REWARD ================")],

    [sg.Text(f"{md.reward_lblName}", font='15px'), sg.Input(key="reward_name", size=(15, 1), font='15px')],
    [sg.Text(f"{md.reward_lblPrice}", font='15px'), sg.Input("5000", key="reward_cost", size=(15, 1), font='15px')],
    [sg.Text(f"{md.reward_lblMsg}", font='15px'), sg.Input(key="reward_msg", size=(15, 1), font='15px', tooltip="Mensagem que será exibida ao usuário antes de resgatar a recompensa")],
    [sg.Text(f"{md.reward_lblEnabled}"), sg.Drop(values=("True", "False"), default_value="True", key="reward_status", font=(30), readonly=True, tooltip="True = Sim, False = Não")],
    [sg.Text(f"{md.reward_lblNeedComment}"), sg.Drop(values=("True", "False"), default_value="False", key="reward_comment_check", font=(30), readonly=True, tooltip="True = Sim, False = Não")],
    
    [sg.Text(f"{md.reward_lblMaxPerStream}"), sg.Drop(values=("True", "False"), default_value="False", key="reward_max_check", font=(30), readonly=True, tooltip="True = Sim, False = Não")],
    [sg.Text(f"{md.reward_lblMaxPerStreamNumber}"), sg.Input("5", key="reward_max_stream", size=(15, 1), font='15px')],
    [sg.Text(f"{md.reward_lblMaxPerUser}"), sg.Drop(values=("True", "False"), default_value="False", key="reward_max_user_check", font=(30), readonly=True, tooltip="True = Sim, False = Não")],
    [sg.Text(f"{md.reward_lblMaxPerUserNumber}"), sg.Input("5", key="reward_max_user", size=(15, 1), font='15px')],

    [sg.Text(f"{md.reward_lblCooldown}"), sg.Drop(values=("True", "False"), default_value="False", key="reward_cooldown_check", font=(30), readonly=True, tooltip="True = Sim, False = Não")],
    [sg.Text(f"{md.reward_lblCooldownNumber}"), sg.Input("5", key="reward_cooldown", size=(15, 1), font='15px')],
    [sg.Button(f"{md.reward_btnCreate}", key="create_reward", size=(15, 1), font='15px')],

    [sg.Text("================ DELETE REWARD ================")],

    [sg.Button("Get all Rewards", key="get_rewards")],

    [sg.Text("", key="rewards_list")]
]

layout = [
    [sg.TabGroup([[sg.Tab(f"{md.lngManageStreamTab}", ManageStreamTab), sg.Tab(f"{md.lngRewardsTab}", RewardTab), sg.Tab(f"{md.lngFunctionsTab}", ToolsTab), sg.Tab(
        f"{md.lngSettingsTab}", SettingsTab), sg.Tab(f"{md.lngAboutTab}", AboutTab)]])],
]

window = sg.Window(f"Twitch GUI", layout, size=(650, 500), icon="./static/img/icons/favicon.ico", resizable=False)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == "change_stream_data":
        GameID = values["stream_game"]
        Title = values["stream_title"]
        Lng = values["stream_language"]

        if not GameID and Title:
             sg.popup(f"Fill the fields {md.mgtStream_lblGame} and {md.mgtStream_lblTitle}!", title="Fields in Blank")
        else:
            ttv.modifyChannel(game_id=GameID, live_title=Title, broadcaster_language=Lng)
            md.SaveLogs(ttv.msg)
            sg.popup(f"{ttv.msg}", title="Response Code")

    if event == "start_comercial":
        ad_time = values["ad_time"]
        ttv.startCommercial(ad_time)

    if event == "create_clip":
        # HasDelay = values["has_delay"]
        # ttv.createClip(HasDelay)
        ttv.createClip()
        if ttv.msg == "Clip Created!":
            web.open(f"https://www.twitch.tv/{md.TwitchUsername}/clip/{ttv.ClipID}")
        else:
            sg.popup("Error to create clip! try again!", "Error")

    if event == "get_clip_status":
        clip_id = values["clip_id"]
        # Futuramente criar uma janela para exibir os dados
        ttv.getClip(clip_id)

    if event == "save_settings":
        Lng = values["language"]
        TwUsername = values["username"]
        TwClient = values["ClientID"]
        TwSecret = values["ClientSecret"]

        md.SaveSettings(lang=Lng, theme="Default", TwUsername=TwUsername, TwClient=TwClient, TwSecret=TwSecret)

        sg.popup("Settings Saved!\nPlease restart Twitch GUI!", title="Success")

    if event == "update_viewers":
            viewers = ttv.getSpecsCount(f"{md.TwitchUsername}")
            window['total_viewers'].update(viewers)
            if ttv.errorBoolean == True:
                sg.popup(f"{ttv.errorMsg}", title="Response Code")

    if event == "create_reward":
        title = values["reward_name"]
        cost = values["reward_cost"]
        msg = values["reward_msg"]
        status = values["reward_status"]
        CommentBoolean = values["reward_comment_check"]

        MaxPerStreamBoolean = values["reward_max_check"]
        MaxPerStreamNumber = values["reward_max_stream"]

        MaxPerUserBoolean = values["reward_max_user_check"]
        MaxPerUserNumber = values["reward_max_user"]

        CooldownBoolean = values["reward_cooldown_check"]
        CooldownNumber = values["reward_cooldown"]

        if not title and cost:
             sg.popup(f"Fill the fields {md.reward_lblName} and {md.reward_lblPrice}!", title="Fields in Blank")
        else:
            ttv.createRewards(title=title, cost=cost, prompt=msg, is_enabled=status, is_user_input_required=CommentBoolean, is_max_per_stream_enabled=MaxPerStreamBoolean, max_per_stream=MaxPerStreamNumber, is_max_per_user_per_stream_enabled=MaxPerUserBoolean, max_per_user_per_stream=MaxPerUserNumber, is_global_cooldown_enabled=CooldownBoolean, global_cooldown_seconds=CooldownNumber)
            sg.popup(f"{ttv.sts_code}", title="Response Code")

    if event == "get_rewards":
        ttv.getAllRewards()

    if event == "check_for_updates":
        md.checkUpdate()
        if md.needUpdate == True:
            msg = str(f'{md.About_lblUpdateAvailable}')
            window['txtExtra'].Update(value=f'{msg}')

            window['txtExtra'].Update(value=f'{md.updateMsg}')
        elif md.needUpdate == False:
            msg = str(f'{md.About_lblNoUpdate}')
            window['txtExtra'].Update(value=f'{msg}')