import webbrowser as web

import libs.Utils as md
from libs.Twitch import Twitch
import PySimpleGUI as sg

import json

md.LoadSettings()

ttv = Twitch(TwUsername=md.TwitchUsername, TwAccessToken=md.TwitchAccessToken, TwClientID=md.TwitchClientID, TwClientSecret=md.TwitchClientSecret)

sg.theme("DarkPurple4")

ManageStreamTab = [

    [sg.Text(f"{md.mgtStream_lblTitle}"), sg.Input(key="stream_title", size=(40, 1))],

    [sg.Text(f"{md.mgtStream_lblGame}"), sg.Input(size=(30, 1), key='search'), sg.Button('Pesquisar')],
    [sg.Listbox(values=[], size=(30, 3), key='games_list', visible=False,enable_events=True)],

    # [sg.Text(f"{md.mgtStream_lblGame}"), sg.Drop(values=(md.GamesListName), default_value="Dead by Daylight", key="stream_game", readonly=True)],
    [sg.Text(f"{md.mgtStream_lblStreamLng}"), sg.Drop(values=(md.LangListName), default_value="Português", key="stream_language", readonly=True)],

    [sg.Button(f"{md.mgtStream_btnChangeStgs}", key="change_stream_data", font='15px')],

    [sg.Text("============================== CHAT ==============================")],

    [sg.Button(f"Limpar Chat", key="clear_chat", font='15px')],

    [sg.Text("============================== AD ==============================")],
    [sg.Drop(values=("30", "60", "90", "120", "150", "180"), default_value="30", key="ad_time", font=(30), readonly=True), sg.Button('Passar AD', key='start_comercial', size=(12), font='15px')],

    [sg.Text(f"============================ {md.mgtStream_lblViewers} ============================")],
    [sg.Text(f"{md.mgtStream_lblViewers}"), sg.Text("0", key="total_viewers", font='15px'), sg.Button(f"{md.mgtStream_btnViewersRefresh}", key="update_viewers", font='15px')],

    [sg.Text(f"============================ CLIP ============================")],
    [sg.Button(f"{md.mgtStream_btnCreateClip}", key="create_clip")],

    [sg.Text(f"{md.mgtStream_lblClipStatus}"), sg.Input("Your CLIP ID Here", key="clip_id"), sg.Button(f"{md.mgtStream_btnGetClipStatus}", key="get_clip_status")],

    [sg.Text(f"============================ RAID ============================")],

    [sg.Text(f"Streamer:"), sg.Input("username_here", key="streamer_name", font='15px', size=(12, 5)), sg.Button(f"Iniciar Raid", key="start_raid", font='15px'), sg.Button(f"Cancelar Raid", key="cancel_raid", font='15px', disabled=True)]
]

RaidTab = [
    
]

ViewersTab = [
    [sg.Button(f"{md.viewers_btnViewersList}", key="get_viewers_list", size=(20), font='15px'), sg.Button(f"{md.viewers_btnViewersBannedsList}", key="get_banned_list", size=(20), font='15px')],
    [sg.Listbox(values=[], size=(50, 20), key="viewers_list", font='15px'), sg.Listbox(values=[], size=(50, 20), key="banneds_list", font='15px')],
    [sg.Text(f"{md.viewers_lblReason}"), sg.Input("reason here", key="reason", font='15px'), sg.Text(f"{md.viewers_lblTime}"), sg.Input("", key="time", font='15px')],
    [sg.Button(f"{md.viewers_btnBan}", key="ban_user", font='15px'), sg.Button(f"{md.viewers_btnUnBan}", key="unban_user", font='15px'), sg.Button(f"{md.viewers_btnTimeout}", key="timeout_user", font='15px'), sg.Button(f"{md.viewers_btnUnTimeout}", key="untimeout_user", font='15px')]
]

ToolsTab = [
    [sg.Text('User:', key=''), sg.Input(f"whispersclub", key='UserInformation'), sg.Button('Total de Seguidores', key='getFollowers', size=(15), font='15px')],
    [sg.Button('Enviar Mensagem', key='send_msg', size=(15), font='15px')],
    [sg.Multiline('', key='msg_content', text_color='white', size=(480, 20), font='15px')]
]

SettingsTab = [
    [sg.Text(f"{md.Stgs_lblTwitchUsername}"), sg.Input(f"{md.TwitchUsername}", key="username")],
    [sg.Text(f"{md.Stgs_lblTwitchAccessToken}"), sg.Input(
        f"{md.TwitchAccessToken}", key="AccessToken", password_char='*')],
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
    [sg.TabGroup([
    [sg.Tab(f"{md.lngManageStreamTab}", ManageStreamTab),
    # sg.Tab(f"Raid", RaidTab),
    sg.Tab(f"{md.lngViewersTab}", ViewersTab),
    sg.Tab(f"{md.lngRewardsTab}", RewardTab),
    sg.Tab(f"{md.lngFunctionsTab}", ToolsTab),
    sg.Tab(f"{md.lngSettingsTab}", SettingsTab),
    sg.Tab(f"{md.lngAboutTab}", AboutTab)]])],
]

window = sg.Window(f"Twitch GUI", layout, size=(650, 600), icon="./static/img/icons/favicon.ico", resizable=False)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Pesquisar':
        search_term = values['search'].strip().lower()
        window['games_list'].update(visible=True)
        filtered_data = [item for item in md.read_json_file("games.json") if search_term in item['name'].lower()]
        window['games_list'].update(values=[item['name'] for item in filtered_data])

    elif event == 'games_list':
        selected_item = values['games_list'][0]
        item_details = next((item for item in md.read_json_file("games.json") if item['name'] == selected_item), None)
        if item_details:
            global id_game
            id_game = item_details['Id']

    if event == "change_stream_data":
        Title = values["stream_title"]
        GameName = values["games_list"]
        LngName = values["stream_language"]

        id_game = 0

        try:
            # GameNameIndex = md.GamesListName.index(GameName)
            # GameID = md.GamesListIDs[GameNameIndex]

            LangNameIndex = md.LangListName.index(LngName)
            LangID = md.LangListIDs[LangNameIndex]

            if not Title:
                sg.popup(f"Fill the fields {md.mgtStream_lblTitle}!", 
                title="Fields in Blank")
            else:
                ttv.modifyChannel(game_id=id_game, live_title=Title, broadcaster_language=LangID)
                md.SaveFile(fileName=md.LOGS_FILE, d1=f"{md.date} [Modify Channel] {ttv.msg}\n")
                sg.popup(f"{ttv.msg}", title="Response Code")
        except IndexError as e:
            sg.popup(f"Error... Maybe The List of Games or Language is index out of range.", title="Error")
            md.SaveFile(fileName=md.LOGS_FILE, d1=f"{md.date} [Modify Channel] {e}\n")

    if event == "start_raid":
        to_streamer = values["streamer_name"]
        ttv.StartRaid(to_streamer)
        if ttv.errorBool != True:
            sg.popup(f"{ttv.msg}", title="Success")
            window['cancel_raid'].update(disabled=False)
        else:
            sg.popup(f"{ttv.msg}", title="Error")

    if event == "cancel_raid":
        ttv.CancelRaid()
        if ttv.errorBool != True:
            window['cancel_raid'].update(disabled=True)
            sg.popup(f"{ttv.msg}", title="Success")
        else:
            sg.popup(f"{ttv.msg}", title="Error")

    if event == "clear_chat":
        ttv.ClearChat()
        if ttv.errorBool != True:
            sg.popup(f"{ttv.msg}", title="Success")
        else:
            sg.popup(f"{ttv.msg}", title="Error")
            md.SaveFile(fileName=md.LOGS_FILE, d1=f"{md.date} [Start Comercial] {ttv.msg}\n")

    if event == "start_comercial":
        ad_time = values["ad_time"]
        ttv.startCommercial(ad_time)
        if ttv.errorBool != True:
            sg.popup(f"{ttv.msg}", title="Success")
            md.SaveFile(fileName=md.LOGS_FILE, d1=f"{md.date} [Start Comercial] {ttv.msg}\n")
        else:
            sg.popup(f"{ttv.msg}", title="Error to run AD")
            md.SaveFile(fileName=md.LOGS_FILE, d1=f"{md.date} [Start Comercial] {ttv.msg}\n")

    if event == "create_clip":
        ttv.createClip()
        if ttv.msg == "Clip Created!":
            web.open(f"https://www.twitch.tv/{md.TwitchUsername}/clip/{ttv.ClipID}")
        else:
            sg.popup("Error to create clip!\nPossible error: your live stream is offline\n\nSolution: start your live stream!", title="Create Clip - Error")

    if event == "get_clip_status":
        clip_id = values["clip_id"]
        ttv.getClip(clip_id)

    if event == "get_viewers_list":
        lista = [usuario["user_name"] for usuario in ttv.getViewersList()]
        window["viewers_list"].update(lista)

    if event == "get_banned_list":
        lista = [usuario["user_name"] for usuario in ttv.getBannedList()]

        window["banneds_list"].update(lista)

    if event == "ban_user":
        selected = window["viewers_list"].get()
        reason = values["reason"]
        time = values["time"]

        try:
            if time.isnumeric():
                if time != 0:
                    sg.popup("O tempo precisa ser mais de 0 segundos", title="Error")
            else:
                try:
                    selectedConverted = selected[0]
                    user_id = ttv.getUserID(selectedConverted)
                    ttv.banUser(user_id, reason, time)
                except IndexError as e:
                    sg.popup("Sua lista está vazia ou nenhum usuário foi selecionado!\n\n Solução: Primeiro obtenha a lista de visualizadores e selecione um usuário para banir!", title="Error")
        except AttributeError as e:
            sg.popup("Sua lista está vazia ou nenhum usuário foi selecionado!\n\n Solução: Primeiro obtenha a lista de visualizadores e selecione um usuário para banir!", title="Error")

    if event == "unban_user":
        selected = window["banneds_list"].get()
        try:
            selectedConverted = selected[0]
            ttv.unBanUser(selectedConverted)
            if ttv.errorBool == True:
                sg.popup(f"{ttv.msg}", title="Error")
            else:
                sg.popup(f"{ttv.msg}", title="Success")
        except IndexError as e:
            sg.popup("Sua lista está vazia ou nenhum usuário foi selecionado!\n\n Solução: Primeiro obtenha a lista de visualizadores e selecione um usuário para banir!", title="Error")

    if event == "save_settings":
        Lng = values["language"]
        TwUsername = values["username"]
        TwAccessToken = values["AccessToken"]
        TwClient = values["ClientID"]
        TwSecret = values["ClientSecret"]

        md.SaveSettings(lang=Lng, theme="Default", TwUsername=TwUsername, TwAccessToken=TwAccessToken, TwClient=TwClient, TwSecret=TwSecret)

        sg.popup("Settings Saved!\nPlease restart Twitch GUI!", title="Success")
        md.SaveFile(fileName=md.LOGS_FILE, d1=f"{md.date} [Save Settings] {ttv.msg}\n")

    if event == "update_viewers":
            viewers = ttv.getSpecsCount(f"{md.TwitchUsername}")
            if ttv.errorBool == True:
                sg.popup(f"{ttv.msg}\n", title="Error")
                md.SaveFile(fileName=md.LOGS_FILE, d1=f"{md.date} [Count Viewers] Error to get viewers! Possible error: Your live stream is offline\n")
            else:
                window['total_viewers'].update(viewers)

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

    if event == "getFollowers":
        sg.popup(f"{ttv.getChannelFollows()}", title="Total Follows")

    if event == "send_msg":
        fromUser = md.TwitchUsername
        toUser = values["UserInformation"]
        msg_content = values["msg_content"]
        ttv.sendWhispers(de=fromUser, para=toUser, mensagem=msg_content)
        if ttv.errorBool == False:
            sg.popup(f"{ttv.msg}")
        else:
            sg.popup(f"{ttv.msg}")

    if event == "check_for_updates":
        md.checkUpdate()
        if md.needUpdate == True:
            msg = str(f'{md.About_lblUpdateAvailable}')
            window['txtExtra'].Update(value=f'{msg}')

            window['txtExtra'].Update(value=f'{md.updateMsg}')
        elif md.needUpdate == False:
            msg = str(f'{md.About_lblNoUpdate}')
            window['txtExtra'].Update(value=f'{msg}')