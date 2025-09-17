import requests
import random
import json
import os
import base64
from flask import Flask, jsonify, request, Response
from datetime import datetime, timedelta
import secrets as noncethingy5
import string as noncethingy6
import sqlite3
import random
import time
import hashlib
from threading import Thread
import secrets as noncethingy3
import string as Noncethingy3
Noncethingy1 = str
Noncethingy2 = int

class GameInfo:

    def __init__(self):
        self.TitleId: str = "1E3C4D"
        self.SecretKey: str = "OPN83XUZBHECBZA4BF7URJOA5KYYSG7MEAYSRJZCDUCJ7BEANB"
        self.ApiKey: str = "OC|8743606419096239|938d41d1a1b3fbf441e1c7f2f586bfbb"
        self.photon_webhook_url = "https://discord.com/api/webhooks/1410727704675745893/G_kqiQI4wV0YkhpvSN6Vm0G2k7yyvUzdTUojIE91YxXfAkJVQYpcRcEFGAHWLpTbt7NV"

    def get_auth_headers(self):
        return {"Content-Type": "application/json", "X-SecretKey": self.SecretKey}
        
    
    @staticmethod
    def PrivacyStateIDtoName(name):
        return {"VISIBLE": 0, "PUBLIC_ONLY": 1, "HIDDEN": 2}.get(name, -1)


item_names = [
    "LHABV.", "LBAGW.", "LMAKI.", "LHAGJ.", "LHACX.", "LBAEZ.", "LBAFA.",
    "LBAFC.", "LBAFD.", "LBAFE.", "LBAFF.", "LBAFG.", "LBAFH.", "LBAFO.", 
    "LBAFP.", "LBAFQ.", "LBAFR.", "LMAAO.", "LMAAN.", "LMAIZ.", "LMAIY.", 
    "LMAHI.", "LMALF.", "LBAFB.", "LHABM.", "LHABI.", "LHABN.", "LBAAT.",
    "LHABH.", "LHABK.", "LHABO.", "LFABB.", "LHABJ.", "LHABL.", "LFABK.",
    "LFABJ.", "LMAAM.", "LBABP.", "LFABL.", "LMAAN.", "LFABM.", "LMAAO.",
    "LHACE.", "LBABO.", "LFABN.", "LFABO.", "LFACB.", "LMACP.", "LMACO.",
    "LBACO.", "LFACC.", "LMACN.", "LBACN.", "LHADI.", "LHADJ.", "LBACL.",
    "LFACD.", "LHADK.", "LMACR.uuuu", "LMACM.", "LBACM.", "LMACQ.", "LMACS.",
    "LHADL."
]
settings = GameInfo()
app = Flask(__name__)
players_file = "players.json"
CODES_FILE = "codes.json"
VOTES_FILE = "votes.json"
QUESTS_FILE = 'quests.json'
USERS_FILE = 'users.json'

def return_function_json(data, funcname, funcparam={}):
    user_id = data["FunctionParameter"]["CallerEntityProfile"]["Lineage"][
        "TitlePlayerAccountId"]

    response = requests.post(
        url=
        f"https://{settings.TitleId}.playfabapi.com/Server/ExecuteCloudScript",
        json={
            "PlayFabId": user_id,
            "FunctionName": funcname,
            "FunctionParameter": funcparam
        },
        headers=settings.get_auth_headers())

    if response.status_code == 200:
        return jsonify(response.json().get("data").get(
            "FunctionResult")), response.status_code
    else:
        return jsonify({}), response.status_code


def get_is_nonce_valid(nonce, oculus_id):
    response = requests.post(
        url=
        f'https://graph.oculus.com/user_nonce_validate?nonce={nonce}&user_id={oculus_id}&access_token={settings.ApiKey}',
        url1=
        f'https://graph.oculus.com/user_nonce_validate?nonce={nonce}&user_id={oculus_id}&access_token={settings.ApiKey1}',
        headers={"content-type": "application/json"})
    return response.json().get("is_valid")

@app.route('/nonce', methods=['GET'])
def noncethingy_endpoint():
    try:
        value = Noncethingy3.generate()
        return jsonify({'Nonce': value}), 200
    except Exception as error:
        return jsonify({'Error': str(error)}), 500



def load_votes():
    try:
        with open(VOTES_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default polls if file doesn't exist
        return [
            {
                "pollId": 2,
                "question": "IS OPLY TAG ON APPLAB BEST GAME",
                "voteOptions": ["YES", "NO"],
                "voteCount": [100, 150],
                "predictionCount": [100, 150],
                "startTime": "2025-03-17T18:00:00",
                "endTime": "2025-03-24T17:00:00",
                "isActive": False
            },
            {
                "pollId": 3,
                "question": "IS OPLY TAG IS BEST GAME ON APPLAB?",
                "voteOptions": ["YES", "NO"],
                "voteCount": [0, 0],
                "predictionCount": [0, 0],
                "startTime": "2025-03-24T18:00:00",
                "endTime": "2025-04-27T17:00:00",
                "isActive": True
            }
        ]

def save_votes(polls):
    with open(VOTES_FILE, 'w') as f:
        json.dump(polls, f, indent=4)
        
def load_players_data():
    try:
        with open(players_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_players_data(players_data):
    with open(players_file, "w") as file:
        json.dump(players_data, file, indent=4)

def load_codes():
    with open(CODES_FILE, 'r') as f:
        return json.load(f)

def find_code(codes, code_id):
    for code in codes:
        if code["id"].upper() == code_id:
            return code
    return None
def grant_cosmetic_to_player(playfab_id, cosmetic_id):
    url = f"https://{settings.TitleId}.playfabapi.com/Admin/GrantItemsToUsers"
    
    payload = json.dumps({
        "ItemGrants": [
            {
                "PlayFabId": playfab_id,
                "ItemId": cosmetic_id,
                "CatalogVersion": "DLC",
                "Annotation": "Redeeming Code"
            }
        ],
        "CatalogVersion": "DLC"
    })
    
    headers = settings.get_auth_headers()
    
    print("Sending GrantItemsToUsers request")
    print("URL:", url)
    print("Payload:", payload)
    print("Headers:", headers)

    response = requests.request("POST", url, headers=headers, data=payload)
    
    print("Response:", response.status_code, response.text)
    return response




def authenticate_ticket(ticket, expected_id=None):
    try:
        # Send authentication request to PlayFab
        res = requests.post(
            f"https://{settings.TitleId}.playfabapi.com/Server/AuthenticateSessionTicket",
            json={"SessionTicket": ticket},
            headers=settings.get_auth_headers()
        )

        # If the request fails, return None
        if res.status_code != 200:
            print(f"Authentication failed with status code: {res.status_code}")
            return None
        
        # Extract the PlayFabId from the response
        user_id = res.json().get("data", {}).get("UserInfo", {}).get("PlayFabId")
        
        if not user_id:
            print("Failed to extract PlayFabId from response")
            return None

        # Check if the expected user_id matches the authenticated user
        if expected_id and user_id != expected_id:
            print(f"User ID mismatch: expected {expected_id}, got {user_id}")
            return None
        
        return user_id
    
    except requests.exceptions.RequestException as e:
        # Handle exceptions (e.g., connection errors, timeouts)
        print(f"Error during authentication: {str(e)}")
        return None

WEEKLY_CAP = 100
DAILY_RESET_HOUR = 0  # Midnight
WEEKLY_RESET_DAY = 0  # Monday

def load_data():
    with open(QUESTS_FILE, 'r') as f:
        quests = json.load(f)
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    return quests, users

def save_data(quests, users):
    with open(QUESTS_FILE, 'w') as f:
        json.dump(quests, f, indent=2)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def get_current_periods():
    now = datetime.utcnow()
    
    # Daily period key (YYYY-MM-DD)
    daily_key = now.strftime("%Y-%m-%d")
    
    # Weekly period key (Monday of current week)
    weekly_start = now - timedelta(days=now.weekday())
    weekly_key = weekly_start.strftime("%Y-%m-%d")
    
    return daily_key, weekly_key

def get_or_create_user(users, playfab_id):
    if playfab_id not in users:
        users[playfab_id] = {
            'total_points': 0,
            'daily_points': {},
            'weekly_points': {},
            'unclaimed_points': 0
        }
    return users[playfab_id]





@app.route("/api/CheckForBadName", methods=["POST"])
def check_for_bad_name():
    # Log headers and raw body
    print("[Incoming Request] Headers:", dict(request.headers))
    print("[Incoming Request] Body:", request.get_data(as_text=True))

    data = request.get_json(silent=True) or {}
    rjson = data.get("FunctionArgument", {})  # Correct use

    name = (rjson.get("name") or "").upper().strip()
    print(f'Someone just entered {name} into the system.')

    playfab_id = data.get("CallerEntityProfile", {}).get("Lineage", {}).get("MasterPlayerAccountId")

    # Normal bad words
    bad_words = {
        "KKK", "PENIS", "NIGG", "NEG", "NIGA", "MONKEYSLAVE", "SLAVE", "FAG",
        "NAGGI", "TRANNY", "QUEER", "KYS", "DICK", "PUSSY", "VAGINA", "BIGBLACKCOCK",
        "DILDO", "HITLER", "KKX", "XKK", "NIGE", "NIG", "NI6", "PORN",
        "JEW", "JAXX", "SEX", "COCK", "CUM", "FUCK", "NIGGA", "NICKER", "NICKA",
        "NII", "@HERE", "NIGGER", "IHATENIGGERS", "@EVERYONE", "RACIST", "HAILHITLER"
    }

    offensive_patterns = [
        "FUCK CAM", "CAMRACIST", "ICAMTRUMP", "RACISTCAM",
        "CAM", "UACISTCAM", "FUCKCAM", "", 
        "RACNSTCAM", "CAM", "CAM", "CAM", 
        "CAM", "CAM"
    ]

    banned = False  # <-- Flag

    # First check offensive patterns
    for offensive_pattern in offensive_patterns:
        if offensive_pattern in name:
            if playfab_id:
                ban_user(playfab_id, name=name, reason="DEFAMATION DETECTED. CONTINUED USE WILL RESULT IN LEGAL ACTION")
                banned = True
            break

    # Only check bad words if NOT already banned
    if not banned:
        for bad_word in bad_words:
            if bad_word in name:
                if playfab_id:
                    ban_user(playfab_id, name=name, reason=f"BAD NAME. NAME: {name}")
                break
    

    embed = {
        "title": "GorillaComputer Entry",
        "color": 0xFF5733 if banned else 0x4CAF50,
        "fields": [
            {
                "name": "Entry",
                "value": name or "N/A",
                "inline": True
            },
            {
                "name": "PlayFab ID",
                "value": playfab_id or "Unknown",
                "inline": True
            },
            {
                "name": "Action Taken",
                "value": ban_reason if banned else "No ban",
                "inline": False
            }
        ]
    }

    try:
        requests.post(
            "",
            json={"embeds": [embed]},
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        print(f"Failed to send Discord embed: {e}")

    # Always return success
    return jsonify({
        "result": 0,
        "banLength": -1
    })

def get_discord_id_from_playfab(playfab_id):
    db_path = "mongodb://localhost:27017"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT discord_id FROM links WHERE playfab_id = ?", (playfab_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
    except Exception as e:
        print(f"Database error: {e}")
    return None

DISCORD_BOT_TOKEN = "MTQwMTMyMjEzMDI2MzUwNzA1Nw.Gnr12q.m2WAeFAjNTcNzTSAK-tIfcqCZ0Zqk3G5PpUEW8"  # must have 'identify' scope
DISCORD_API_BASE = "https://discord.com/api/v10"

def get_discord_username(discord_id):
    try:
        headers = {
            "Authorization": f"Bot {DISCORD_BOT_TOKEN}"
        }
        response = requests.get(f"{DISCORD_API_BASE}/users/{discord_id}", headers=headers)
        if response.status_code == 200:
            user = response.json()
            return f"{user['username']}#{user['discriminator']}"  # or user['global_name'] for newer accounts
    except Exception as e:
        print(f"Error fetching Discord user: {e}")
    return None

@app.route("/re/api/SetPrivacyState", methods=["POST"])
@app.route("/api/SetPrivacyState", methods=["POST"])
def SetPrivacyState():
    rjson = request.get_json()
    playfab_id = rjson.get("PlayFabId", "")
    privacy_state = rjson.get("PrivacyState", "VISIBLE")
    playfab_ticket = rjson.get("PlayFabTicket", "")

    if not playfab_id or not playfab_ticket or settings.PrivacyStateIDtoName(privacy_state) == -1:
        return "", 400

    auth_session = requests.post(
        f"https://{settings.TitleId}.playfabapi.com/Server/AuthenticateSessionTicket",
        json={"SessionTicket": playfab_ticket},
        headers=settings.get_auth_headers()
    )

    if auth_session.status_code != 200 or auth_session.json()["data"]["UserInfo"]["PlayFabId"] != playfab_id:
        return "", 400

    requests.post(
        f"https://{settings.TitleId}.playfabapi.com/Server/UpdateUserInternalData",
        headers=settings.get_auth_headers(),
        json={"PlayFabId": playfab_id, "Data": {"PrivacyState": privacy_state}}
    )

    return jsonify({"statusCode": 200, "error": None}), 200


@app.route("/", methods=["POST", "GET"])
@app.route("/rea", methods=["POST", "GET"])
def main():
    if request.method != "POST":
        return "", 404

    if "UnityPlayer" not in request.headers.get("User-Agent", ""): 
        return "", 404
    else:
        today = datetime.utcnow().replace(hour=22, minute=0, second=0, microsecond=0)
        start_of_week = today - timedelta(days=today.weekday() + 1)
        end_of_week = start_of_week + timedelta(days=7)
        start_of_week_str = start_of_week.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        end_of_week_str = end_of_week.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    
        day_of_year = today.timetuple().tm_yday
        item_index = day_of_year % len(item_names)
        item_name = item_names[item_index]

        data = {
            "MOTD": "WELCOME TO ULTRA TAGGERS</color>",
            "BundleBoardSign": "disocrd.gg/ultrataggerss",
            "BundleKioskButton": "https://discord.gg/ultrataggerss",
            "BundleKioskSign": "https://discord.gg/ultrataggerss",
            "KIDData": {
                "K-ID Enabled": "false",
                "K-ID Phase": 0
            },
            "BundleLargeSign": "https://discord.gg/ultrataggerss",
            "SeasonalStoreBoardSign": "https://discord.gg/ultrataggerss",
            "GorillanalyticsChance": 1,
            "EmptyFlashbackText": "https://discord.gg/ultrataggerss",
            "PrivateCrittersGrabSettings": 7,
            "PublicCrittersGrabSettings": 0,
            "UseLegacyIAP": False,
            "TOTD": [{
                "PedestalID": "CosmeticStand1",
                "ItemName": item_name, # item_name
                "StartTimeUTC": start_of_week_str, # start_of_week_str
                "EndTimeUTC": end_of_week_str # end_of_week_str
            },
            {
                "PedestalID": "CosmeticStand2",
                "ItemName": item_names[(item_index + 1) % len(item_names)], # item_names[(item_index + 1) % len(item_names)]
                "StartTimeUTC": start_of_week_str, # start_of_week_str
                "EndTimeUTC": end_of_week_str # end_of_week_str
            },
            {
                "PedestalID": "CosmeticStand3",
                "ItemName": item_names[(item_index + 2) % len(item_names)], # item_names[(item_index + 2) % len(item_names)]
                "StartTimeUTC": start_of_week_str, # start_of_week_str
                "EndTimeUTC": end_of_week_str # end_of_week_str
            }],
            "AllowedClientVersions": {"clientVersions": ["live1.1.1.106"]},
            "AutoMuteCheckedHours": {"hours": 169},
            "AutoName_Adverbs": ["Cool", "Fine", "Bald", "Bold", "Half", "Only", "Calm", "Fab", "Ice", "Mad", "Rad", "Big", "New", "Old", "Shy"],
            "AutoName_Nouns": ["Gorilla", "Chicken", "Darling", "Sloth", "King", "Queen", "Royal", "Major", "Actor", "Agent", "Elder", "Honey", "Nurse", "Doctor", "Rebel", "Shape", "Ally", "Driver", "Deputy"],
            "BacktraceSampleRate": 0.001,
            "BundleBoardSafeAccountSign": "EVERY DAY YOU VISIT GORILLA WORLD YOU WILL GET 100 SHINY ROCKS",
            "BundleBoardSign_SafeAccount": "EVERY DAY YOU VISIT GORILLA WORLD YOU WILL GET 100 SHINY ROCKS",
            "BundleData": {"Items": [{"isActive": False, "skuName": "2025_bear_hug_pack", "shinyRocks": 0, "playFabItemName": "LSABX.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 99, "displayName": "Bear Hug Pack"}, {"isActive": False, "skuName": "2025_brass_funke_pack", "shinyRocks": 10000, "playFabItemName": "LSABW.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 97, "displayName": "Brass Funke Pack"}, {"isActive": False, "skuName": "2024_holiday_blast_pack", "shinyRocks": 10000, "playFabItemName": "LSABV.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 95, "displayName": "Holiday Blast Pack"}, {"isActive": False, "skuName": "2024_dragon_armor_pack", "shinyRocks": 10000, "playFabItemName": "LSABU.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 93, "displayName": "Dragon Armor Pack"}, {"isActive": False, "skuName": "2024_headless_nightmare_pack", "shinyRocks": 10000, "playFabItemName": "LSABT.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 91, "displayName": "Headless Nightmare Pack"}, {"isActive": False, "skuName": "2024_pumpkin_patch_pack", "shinyRocks": 10000, "playFabItemName": "LSABS.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 90, "displayName": "Pumpkin Patch Pack"}, {"isActive": False, "skuName": "2024_monkes_wild_pack", "shinyRocks": 10000, "playFabItemName": "LSABR.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 89, "displayName": "Monkes Wild Pack"}, {"isActive": False, "skuName": "CLIMBSTOPPERSBUN", "shinyRocks": 10000, "playFabItemName": "CLIMBSTOPPERSBUN", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 0, "displayName": "CLIMB STOPPERS BUNDLE"}, {"isActive": False, "skuName": "GLAMROCKERBUNDLE", "shinyRocks": 10000, "playFabItemName": "GLAMROCKERBUNDLE", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 0, "displayName": "GLAM ROCKER BUNDLE"}, {"isActive": False, "skuName": "2024_cyber_monke_pack", "shinyRocks": 10000, "playFabItemName": "LSABP.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 87, "displayName": "Cyber Monke Pack"}, {"isActive": False, "skuName": "2024_splash_dash_pack", "shinyRocks": 10000, "playFabItemName": "LSABO.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 85, "displayName": "Splash and Dash Pack"}, {"isActive": False, "skuName": "2024_shiny_rock_special", "shinyRocks": 2200, "playFabItemName": "LSABN.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 83, "displayName": "Shiny Rock Special"}, {"isActive": False, "skuName": "2024_climb_stoppers_pack", "shinyRocks": 10000, "playFabItemName": "LSABM.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 82}, {"isActive": True, "skuName": "2024_glam_rocker_pack", "shinyRocks": 10000, "playFabItemName": "LSABL.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 80}, {"isActive": False, "skuName": "2024_monke_monk_pack", "shinyRocks": 10000, "playFabItemName": "LSABK.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 78}, {"isActive": False, "skuName": "2024_leaf_ninja_pack", "shinyRocks": 10000, "playFabItemName": "LSABJ.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 76}, {"isActive": False, "skuName": "2024_gt_monke_plush", "shinyRocks": 0, "playFabItemName": "LSABI.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 73}, {"isActive": False, "skuName": "2024_beekeeper_pack", "shinyRocks": 10000, "playFabItemName": "LSABH.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 73}, {"isActive": False, "skuName": "2024_i_lava_you_pack", "shinyRocks": 10000, "playFabItemName": "LSABG.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 71}, {"isActive": False, "skuName": "2024_mad_scientist_pack", "shinyRocks": 10000, "playFabItemName": "LSABF.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 69}, {"isActive": False, "skuName": "2023_holiday_fir_pack", "shinyRocks": 10000, "playFabItemName": "LSABE.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 63}, {"isActive": False, "skuName": "2023_spider_monke_bundle", "shinyRocks": 10000, "playFabItemName": "LSABD.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 59}, {"isActive": False, "skuName": "2023_caves_bundle", "shinyRocks": 10000, "playFabItemName": "LSABC.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 54}, {"isActive": False, "skuName": "2023_summer_splash_bundle", "shinyRocks": 10000, "playFabItemName": "LSABA.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 46}, {"isActive": False, "skuName": "2023_march_pot_o_gold", "shinyRocks": 5000, "playFabItemName": "LSAAU.", "majorVersion": 1, "minorVersion": 1, "minorVersion2": 39}, {"skuName": "2023_sweet_heart_bundle", "playFabItemName": "LSAAS.", "shinyRocks": 0, "isActive": False}, {"skuName": "2022_launch_bundle", "playFabItemName": "LSAAP2.", "shinyRocks": 10000, "isActive": False}, {"skuName": "early_access_supporter_pack", "playFabItemName": "Early Access Supporter Pack", "shinyRocks": 0, "isActive": False}]},
            "BundleLargeSafeAccountSign": " ",
            "BundleLargeSign_SafeAccount": " ",
            "CreditsData": [{"Title": "DEV TEAM", "Entries": ["CAM", "ST4R"]}, {"Title": "OWNERS", "Entries": ["Cam", "ST4R", "", "", ""]}],
            "DeployFeatureFlags": {"flags": [{"name": "2024-05-ReturnCurrentVersionV2", "value": 0, "valueType": "percent"}, {"name": "2024-05-ReturnMyOculusHashV2", "value": 0, "valueType": "percent"}, {"name": "2024-05-TryDistributeCurrencyV2", "value": 0, "valueType": "percent"}, {"name": "2024-05-AddOrRemoveDLCOwnershipV2", "value": 0, "valueType": "percent"}, {"name": "2024-05-BroadcastMyRoomV2", "value": 0, "valueType": "percent"}, {"name": "2024-06-CosmeticsAuthenticationV2", "value": 0, "valueType": "percent"}, {"name": "2024-08-KIDIntegrationV1", "value": 0, "valueType": "percent", "alwaysOnForUsers": [""]}]},
            "EnableCustomAuthentication": True,
            "MOTDDeprecation": "",
            "MuteThresholds": {"thresholds": [{"name": "low", "threshold": 20}, {"youname": "high", "threshold": 50}]},
            "VStumpDiscord": "https://discord.gg/Cvv9BJ57fA",
            "VStumpFeaturedMaps": "4641648,4733024,4475071",
            "Bundle1TryOnDesc": "https://discord.gg/Cvv9BJ57fA",
            "Bundle1TryOnPurchaseBtn": "https://discord.gg/Cvv9BJ57fA",
            "TOBAlreadyOwnCompTxt": "YOU OWN THE BUNDLE ALREADY! THANK YOU!",
            "TOBAlreadyOwnPurchaseBtnTxt": "-",
            "TOBDefCompTxt": "PLEASE SELECT A PACK TO TRY ON AND BUY",
            "TOBDefPurchaseBtnDefTxt": "SELECT A PACK",
            "TOBSafeCompTxt": "PURCHASE ITEMS IN YOUR CART AT THE CHECKOUT COUNTER",
            "PromoHutSignText": "https://discord.gg/ultrataggerss",
            "VStumpMOTD": "",
            "GTBlackFridayPromo": "https://discord.gg/ultrataggerss",
            "AllActiveQuests": {"DailyQuests": [{"selectCount": 1, "name": "Gameplay", "quests": [{"disable": False, "questID": 11, "weight": 1, "questName": "Play Infection", "questType": "gameModeRound", "questOccurenceFilter": "INFECTION", "requiredOccurenceCount": 1, "requiredZones": ["forest", "canyon", "beach", "mountain", "skyJungle", "cave", "Metropolis", "bayou", "rotating", "none"]}, {"disable": True, "questID": 19, "weight": 1, "questName": "Play Paintbrawl", "questType": "gameModeRound", "questOccurenceFilter": "PAINTBRAWL", "requiredOccurenceCount": 1, "requiredZones": ["forest", "canyon", "beach", "mountain", "skyJungle", "cave", "Metropolis", "bayou", "rotating", "none"]}, {"disable": False, "questID": 13, "weight": 1, "questName": "Play Freeze Tag", "questType": "gameModeRound", "questOccurenceFilter": "FREEZE TAG", "requiredOccurenceCount": 1, "requiredZones": ["forest", "canyon", "beach", "mountain", "skyJungle", "cave", "Metropolis", "bayou", "rotating", "none"]}, {"disable": False, "questID": 1, "weight": 1, "questName": "Play Guardian", "questType": "gameModeRound", "questOccurenceFilter": "GUARDIAN", "requiredOccurenceCount": 5, "requiredZones": ["forest", "canyon", "beach", "mountain", "cave", "Metropolis", "bayou", "none"]}, {"disable": False, "questID": 4, "weight": 1, "questName": "Tag players", "questType": "misc", "questOccurenceFilter": "GameModeTag", "requiredOccurenceCount": 2, "requiredZones": ["none"]}]}, {"selectCount": 3, "name": "Exploration", "quests": [{"disable": False, "questID": 5, "weight": 1, "questName": "Ride the shark", "questType": "grabObject", "questOccurenceFilter": "ReefSharkRing", "requiredOccurenceCount": 1, "requiredZones": ["none"]}, {"disable": False, "questID": 9, "weight": 1, "questName": "Play the piano", "questType": "tapObject", "questOccurenceFilter": "Piano_Collapsed_Key", "requiredOccurenceCount": 10, "requiredZones": ["none"]}, {"disable": False, "questID": 14, "weight": 1, "questName": "Throw snowballs", "questType": "launchedProjectile", "questOccurenceFilter": "SnowballProjectile", "requiredOccurenceCount": 10, "requiredZones": ["none"]}, {"disable": False, "questID": 15, "weight": 1, "questName": "Go for a swim", "questType": "swimDistance", "questOccurenceFilter": "", "requiredOccurenceCount": 200, "requiredZones": ["none"]}, {"disable": False, "questID": 21, "weight": 1, "questName": "Climb the tallest tree", "questType": "enterLocation", "questOccurenceFilter": "TallestTree", "requiredOccurenceCount": 1, "requiredZones": ["forest"]}, {"disable": False, "questID": 22, "weight": 1, "questName": "Complete the obstacle course", "questType": "enterLocation", "questOccurenceFilter": "ObstacleCourse", "requiredOccurenceCount": 1, "requiredZones": ["none"]}, {"disable": False, "questID": 23, "weight": 1, "questName": "Swim under a waterfall", "questType": "enterLocation", "questOccurenceFilter": "UnderWaterfall", "requiredOccurenceCount": 1, "requiredZones": ["none"]}, {"disable": False, "questID": 24, "weight": 1, "questName": "Sneak upstairs in the store", "questType": "enterLocation", "questOccurenceFilter": "SecretStore", "requiredOccurenceCount": 1, "requiredZones": ["none"]}, {"disable": False, "questID": 25, "weight": 1, "questName": "Climb into the crow's nest", "questType": "enterLocation", "questOccurenceFilter": "CrowsNest", "requiredOccurenceCount": 1, "requiredZones": ["none"]}, {"disable": False, "questID": 26, "weight": 1, "questName": "Go for a walk", "questType": "moveDistance", "questOccurenceFilter": "", "requiredOccurenceCount": 500, "requiredZones": ["none"]}, {"disable": False, "questID": 28, "weight": 1, "questName": "Get small", "questType": "misc", "questOccurenceFilter": "SizeSmall", "requiredOccurenceCount": 1, "requiredZones": ["none"]}, {"disable": False, "questID": 29, "weight": 1, "questName": "Get big", "questType": "misc", "questOccurenceFilter": "SizeLarge", "requiredOccurenceCount": 1, "requiredZones": ["none"]}]}, {"selectCount": 1, "name": "Social", "quests": [{"disable": False, "questID": 2, "weight": 1, "questName": "High Five Players", "questType": "triggerHandEffect", "questOccurenceFilter": "HIGH_FIVE", "requiredOccurenceCount": 10, "requiredZones": ["none"]}, {"disable": False, "questID": 3, "weight": 1, "questName": "Fist Bump Players", "questType": "triggerHandEffect", "questOccurenceFilter": "FIST_BUMP", "requiredOccurenceCount": 10, "requiredZones": ["none"]}, {"disable": False, "questID": 16, "weight": 1, "questName": "Find something to eat", "questType": "eatObject", "questOccurenceFilter": "", "requiredOccurenceCount": 1, "requiredZones": ["none"]}, {"disable": False, "questID": 30, "weight": 1, "questName": "Make a friendship bracelet", "questType": "misc", "questOccurenceFilter": "FriendshipGroupJoined", "requiredOccurenceCount": 1, "requiredZones": ["none"]}]}], "WeeklyQuests": [{"selectCount": 1, "name": "Gameplay", "quests": [{"disable": False, "questID": 17, "weight": 1, "questName": "Play Infection", "questType": "gameModeRound", "questOccurenceFilter": "INFECTION", "requiredOccurenceCount": 5, "requiredZones": ["none"]}, {"disable": True, "questID": 20, "weight": 1, "questName": "Play Paintbrawl", "questType": "gameModeRound", "questOccurenceFilter": "PAINTBRAWL", "requiredOccurenceCount": 5, "requiredZones": ["none"]}, {"disable": False, "questID": 8, "weight": 1, "questName": "Play Freeze Tag", "questType": "gameModeRound", "questOccurenceFilter": "FREEZE TAG", "requiredOccurenceCount": 5, "requiredZones": ["none"]}, {"disable": False, "questID": 10, "weight": 1, "questName": "Play Guardian", "questType": "gameModeRound", "questOccurenceFilter": "GUARDIAN", "requiredOccurenceCount": 25, "requiredZones": ["none"]}, {"disable": False, "questID": 12, "weight": 1, "questName": "Tag players", "questType": "triggerHandEffect", "questOccurenceFilter": "THIRD_PERSON", "requiredOccurenceCount": 10, "requiredZones": ["none"]}]}, {"selectCount": 1, "name": "Exploration and Social", "quests": [{"disable": False, "questID": 6, "weight": 1, "questName": "Throw Snowballs", "questType": "launchedProjectile", "questOccurenceFilter": "SnowballProjectile", "requiredOccurenceCount": 50, "requiredZones": ["none"]}, {"disable": False, "questID": 7, "weight": 1, "questName": "Go for a long swim", "questType": "swimDistance", "questOccurenceFilter": "", "requiredOccurenceCount": 1000, "requiredZones": ["none"]}, {"disable": False, "questID": 18, "weight": 1, "questName": "Eat food", "questType": "eatObject", "questOccurenceFilter": "", "requiredOccurenceCount": 25, "requiredZones": ["none"]}, {"disable": False, "questID": 27, "weight": 1, "questName": "Go for a long walk", "questType": "moveDistance", "questOccurenceFilter": "", "requiredOccurenceCount": 2500, "requiredZones": ["none"]}]}]},
            "ArenaForestSign": "https://discord.gg/ultrataggerss",
            "ArenaRulesSign": "https://discord.gg/ultrataggerss",
            "LBDMakeshipPromo": "https://discord.gg/ultrataggerss",
            "TOS_Real": "test",
            "PrivacyPolicy_Real": "test"
        }
    
        return jsonify(data)


@app.route("/api/GetQuestStatus", methods=["POST"])
@app.route("/re/api/GetQuestStatus", methods=["POST"])
def GetQuestStatus():
    rjson = request.json
    playfab_id = rjson.get("PlayFabId")
    playfab_ticket = rjson.get("PlayFabTicket")
    
    auth_session = requests.post(
        f"https://{settings.TitleId}.playfabapi.com/Server/AuthenticateSessionTicket",
        json={"SessionTicket": playfab_ticket},
        headers=settings.get_auth_headers()
    )

    if auth_session.status_code != 200 or auth_session.json()["data"]["UserInfo"]["PlayFabId"] != playfab_id:
        return "", 400

    if playfab_id in [""]:
        return jsonify({"result": {"dailyPoints": {}, "weeklyPoints": {}, "userPointsTotal": 99999}, "statusCode": 200, "error": None}), 200

    try:
        value_str = requests.post(f"https://{settings.TitleId}.playfabapi.com/Server/GetUserData", headers=settings.get_auth_headers(), json={"PlayFabId": playfab_id, "Keys": ["progression_v1"]}).json()["data"]["Data"]["progression_v1"]["Value"]
        result = loads(value_str)
    except:
        result = {
            "dailyPoints": {},
            "weeklyPoints": {},
            "userPointsTotal": 0
        }

    return jsonify({
        "result": result,
        "statusCode": 200,
        "error": None
    })
    return jsonify({}), 200


@app.route("/api/SetQuestComplete", methods=["POST"])
def SetQuestComplete():
    rjson = request.json
    print(rjson)
    playfab_id = rjson.get("PlayFabId")
    playfab_ticket = rjson.get("PlayFabTicket")
    quest_id = rjson.get("QuestId")

    auth_session = requests.post(
        f"https://{settings.TitleId}.playfabapi.com/Server/AuthenticateSessionTicket",
        json={"SessionTicket": playfab_ticket},
        headers=settings.get_auth_headers()
    )

    if auth_session.status_code != 200 or auth_session.json()["data"]["UserInfo"]["PlayFabId"] != playfab_id:
        print(auth_session.json())
        return "", 400

    try:
        value_str = requests.post(f"https://{settings.TitleId}.playfabapi.com/Admin/GetUserData", headers=settings.get_auth_headers(), json={"PlayFabId": playfab_id, "Keys": ["progression_v1"]}).json()["data"]["Data"]["progression_v1"]["Value"]
        current = loads(value_str)
    except:
        current = {
            "dailyPoints": {},
            "weeklyPoints": {},
            "userPointsTotal": 0
        }

    current["dailyPoints"][datetime.utcnow().strftime("%m/%d/%Y")] = current["dailyPoints"].get(datetime.utcnow().strftime("%m/%d/%Y"), 0) + 1
    current["weeklyPoints"][str(datetime.utcnow().isocalendar()[1])] = current["weeklyPoints"].get(str(datetime.utcnow().isocalendar()[1]), 0)
    current["userPointsTotal"] += 1

    requests.post(f"https://{settings.TitleId}.playfabapi.com/Admin/UpdateUserData", headers=settings.get_auth_headers(), json={"PlayFabId": playfab_id,"Data": {"progression_v1": dumps(current)},"Permission": "Private"})

    return jsonify({
        "result": current,
        "statusCode": 200,
        "error": None
    })

@app.route('/api/CachePlayFabId', methods=['POST'])
def cache_playfab_id():
    data = request.json
    send_to_discord(data)
    required_fields = ['Platform', 'SessionTicket', 'PlayFabId']
    if all([field in data for field in required_fields]):
        return jsonify({"Message": "PlayFabId Cached Successfully"}), 200
    else:
        missing_fields = [
            field for field in required_fields if field not in data
        ]
        return jsonify({
            "Error": "Missing Data",
            "MissingFields": missing_fields
        }), 400


if os.path.exists('data.json'):
    with open('data.json', 'r') as f:
        info = f.read()
        print(info)
        config = json.loads(info)
else:
    config = {}


def log_bad_name(name, id):

    if os.path.exists(f'Users/{id}.json'):
        with open(f'Users/{id}.json', 'r') as f:
            info = f.read()
            print(info)
            logs = json.loads(info)
    else:
        logs = {}

    if id in logs:
        if name in logs[id]:
            logs[id][name] += 1
        else:
            logs[id] = {name: 1}
    else:
        logs[id] = {name: 1}

    with open(f'Users/{id}.json', 'w') as temp_file:
        json.dump(logs, temp_file)
        temp_file.close()


@app.route("/pf/api/PlayFabAuthentication", methods=["POST"])
@app.route("/re/api/PlayFabAuthentication", methods=["POST"])
@app.route("/reals/api/PlayFabAuthentication", methods=["POST"])
@app.route("/rea/api/PlayFabAuthentication", methods=["POST"])
@app.route("/real/api/PlayFabAuthentication", methods=["POST"])
@app.route("/api/PlayFabAuthentication", methods=["POST"])
def playfab_authentication():
    rjson = request.get_json()
    required_fields = ["Nonce", "AppId", "Platform", "OculusId"]
    missing_fields = [field for field in required_fields if not rjson.get(field)]

    if missing_fields:
        return (
            jsonify(
                {
                    "Message": f"Missing parameter(s): {', '.join(missing_fields)}",
                    "Error": f"BadRequest-No{missing_fields[0]}",
                }
            ),
            401,
        )

    if rjson.get("AppId") != settings.TitleId:
        return (
            jsonify(
                {
                    "Message": "Request sent for the wrong App ID",
                    "Error": "BadRequest-AppIdMismatch", # invalid request
                }
            ),
            400,
        )

    url = f"https://{settings.TitleId}.playfabapi.com/Server/LoginWithServerCustomId"
    login_request = requests.post(
        url=url,
        json={
            "ServerCustomId": "OCULUS" + rjson.get("OculusId"),
            "CreateAccount": True,
        },
        headers=settings.get_auth_headers(),
    )

    if login_request.status_code == 200:
        data = login_request.json().get("data")
        sessionpuss = data.get("SessionTicket")
        entity = data.get("EntityToken").get("EntityToken")
        Id = data.get("PlayFabId")
        type = data.get("EntityToken").get("Entity").get("Type")
        entityid = data.get("EntityToken").get("Entity").get("Id")

        link_response = requests.post(
            url=f"https://{settings.TitleId}.playfabapi.com/Server/LinkServerCustomId",
            json={
                "ForceLink": True,
                "PlayFabId": Id,
                "ServerCustomId": rjson.get("CustomId"),
            },
            headers=settings.get_auth_headers(),
        ).json()

        return (
            jsonify(
                {
                    "PlayFabId": Id,
                    "SessionTicket": sessionpuss,
                    "EntityToken": entity,
                    "EntityId": entityid,
                    "EntityType": type,
                }
            ),
            200,
        )
    else:
        if login_request.status_code == 403:
            ban_info = login_request.json()
            if ban_info.get("errorCode") == 1002:
                ban_message = ban_info.get("errorMessage", "No ban message provided.")
                ban_details = ban_info.get("errorDetails", {})
                ban_expiration_key = next(iter(ban_details.keys()), None)
                ban_expiration_list = ban_details.get(ban_expiration_key, [])
                ban_expiration = (
                    ban_expiration_list[0]
                    if len(ban_expiration_list) > 0
                    else "nuh"
                )
                print(ban_info)
                return (
                    jsonify(
                        {
                            "BanMessage": ban_expiration_key,
                            "BanExpirationTime": ban_expiration,
                        }
                    ),
                    403,
                )
            else:
                error_message = ban_info.get(
                    "errorMessage", "Forbidden without ban information."
                )
                return (
                    jsonify({"Error": "PlayFab Error", "Message": error_message}),
                    403,
                )
        else:
            error_info = login_request.json()
            error_message = error_info.get("errorMessage", "An error occurred.")
            return (
                jsonify({"Error": "PlayFab Error", "Message": error_message}),
                login_request.status_code,
            )



def ban_user(current_player_id, duration_hours=0, reason="CHEATING. PERMANENT BAN, THIS IS NOT APPEALABLE"):
    return requests.post(f"https://{settings.TitleId}.playfabapi.com/Server/BanUsers", headers=settings.get_auth_headers(), json={
        "Bans": [{
            "PlayFabId": current_player_id,
            "DurationInHours": duration_hours,
            "Reason": reason
        }]
    })
@app.route("/api/TitleData", methods=["POST", "GET"])
def titledata():
    response = requests.post(
        url=f"https://{settings.TitleId}.playfabapi.com/Server/GetTitleData",
        headers=settings.get_auth_headers())

    if response.status_code == 200:
        return jsonify(response.json().get("data").get("Data"))
    else:
        return jsonify({}), response.status_code

@app.route("/api/Vote", methods=["POST"])
def vote():
    if request.method != "POST":
        return "", 404

    data = request.json
    ticket = data.get("PlayFabTicket")
    poll_id = int(data.get("PollId", -1))
    playfab_id = data.get("PlayFabId")
    option_index = data.get("OptionIndex")
    is_prediction = data.get("IsPrediction")

    polls = load_votes()
    poll = next((p for p in polls if p["pollId"] == poll_id), None)
    
    if not poll or not poll["isActive"]:
        return "", 404

    if not isinstance(option_index, int) or not (0 <= option_index < len(poll["voteOptions"])):
        return "", 400

    if "voteCount" not in poll or len(poll["voteCount"]) != len(poll["voteOptions"]):
        poll["voteCount"] = [0] * len(poll["voteOptions"])
    if "predictionCount" not in poll or len(poll["predictionCount"]) != len(poll["voteOptions"]):
        poll["predictionCount"] = [0] * len(poll["voteOptions"])

    if is_prediction:
        poll["predictionCount"][option_index] += 1
    else:
        poll["voteCount"][option_index] += 1

    save_votes(polls)

    embed = {
        "embeds": [
            {
                "title": "Ã¢Å“â€¦ - Vote success",
                "description": (
                    f"**PlayFab ID**: {playfab_id}\n"
                    f"**Prediction**: {is_prediction}\n"
                    f"**Question**: {poll['question']}\n"
                    f"**Voting for**: {poll['voteOptions'][option_index]}\n"
                    f"**Search Thing**: {is_prediction}-{poll['voteOptions'][option_index]}"
                ),
                "color": 3447003
            }
        ]
    }

    requests.post(
        "",
        json=embed
    )

    return jsonify(poll), 200

friends_file = "friends_data.json"
privacy_file = "privacy_data.json"
roomcodes_file = "roomcodes.json"

def load_friends_data():
    try:
        with open(friends_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_friends_data(data):
    with open(friends_file, "w") as f:
        json.dump(data, f, indent=4)

def load_code_data():
    try:
        with open(roomcodes_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_code_data():
    with open(roomcodes_file, "w") as f:
        json.dump(data, f, indent=4)

def load_privacy_data():
    try:
        with open(privacy_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
        
def save_privacy_data(data):
    with open(privacy_file, "w") as f:
        json.dump(data, f, indent=4)

friends_data = load_friends_data()
privacy_data = load_privacy_data()
code_data = load_code_data()


@app.route("/api/GetFriendsV2", methods=["POST"])
def GetFriendsV2():
    rjson = request.get_json()
    playfab_id = rjson.get("PlayFabId", "")
    playfab_ticket = rjson.get("PlayFabTicket", "")

    if not playfab_id or not playfab_ticket:
        return "Missing fields", 400

    auth_session = requests.post(
        f"https://{settings.TitleId}.playfabapi.com/Server/AuthenticateSessionTicket",
        json={"SessionTicket": playfab_ticket},
        headers=settings.get_auth_headers()
    )

    if auth_session.status_code != 200 or auth_session.json()["data"]["UserInfo"]["PlayFabId"] != playfab_id:
        return "", 400

    internal_data = requests.post(
        f"https://{settings.TitleId}.playfabapi.com/Server/GetUserInternalData",
        headers=settings.get_auth_headers(),
        json={"PlayFabId": playfab_id}
    ).json().get("data", {}).get("Data", {})

    friend_string = internal_data.get("Friends", {}).get("Value", "")
    privacy_state_str = internal_data.get("PrivacyState", {}).get("Value", "VISIBLE")
    friends = []

    # âœ… This stays outside try-except
    try:
        with open("roomcodes.json", "r") as f:
            room_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        room_data = {}

    # âœ… Moved outside the `except`
    for friend_id in friend_string.split(','):
        if not friend_id.strip():
            continue

        friend_data_resp = requests.post(
            f"https://{settings.TitleId}.playfabapi.com/Server/GetUserInternalData",
            headers=settings.get_auth_headers(),
            json={"PlayFabId": friend_id}
        )

        if friend_data_resp.status_code != 200:
            continue

        d = friend_data_resp.json().get("data", {}).get("Data", {})

        def clean(x): return None if x == "null" or x == "" else x

        nickname = clean(d.get("Nickname", {}).get("Value", ""))
        room_id = room_data.get(friend_id)  # âœ… Use roomcodes.json only
        zone = clean(d.get("Zone", {}).get("Value", ""))
        region = clean(d.get("Region", {}).get("Value", ""))
        is_public = "false"
        friend_privacy = d.get("PrivacyState", {}).get("Value", "VISIBLE")

        presence = {
            "friendLinkId": friend_id,
            "userName": nickname,
            "roomId": None,
            "zone": None,
            "region": None,
            "isPublic": is_public
        }

        if friend_privacy == "HIDDEN":
            pass
        elif friend_privacy == "PUBLIC_ONLY":
            if is_public:
                presence.update({
                    "roomId": room_id,
                    "zone": zone,
                    "region": region,
                    "isPublic": is_public
                })
        else:
            presence.update({
                "roomId": room_id,
                "zone": zone,
                "region": region,
                "isPublic": is_public
            })

        friends.append({
            "presence": presence,
            "created": datetime.now().isoformat()
        })

    return jsonify({
        "result": {
            "friends": friends,
            "myPrivacyState": settings.PrivacyStateIDtoName(privacy_state_str)
        },
        "statusCode": 200,
        "error": None
    })

@app.route("/api/RemoveFriend", methods=["POST"])
@app.route("/re/api/RemoveFriend", methods=["POST"])
def RemoveFriend():
    rjson = request.get_json()
    playfab_id = rjson.get("PlayFabId", "")
    friend_link_id = rjson.get("FriendFriendLinkId", "")
    my_link_id = rjson.get("MyFriendLinkId", "")
    ticket = rjson.get("PlayFabTicket", "")

    if not playfab_id: return "Must supply a valid PlayFab ID", 400
    if not friend_link_id: return "Must supply a valid FriendFriendLinkId", 400

    auth_session = requests.post(
        f"https://{settings.TitleId}.playfabapi.com/Server/AuthenticateSessionTicket",
        json={"SessionTicket": ticket},
        headers=settings.get_auth_headers()
    )

    if auth_session.status_code != 200 or auth_session.json()["data"]["UserInfo"]["PlayFabId"] != playfab_id:
        return "Unauthorized", 403

    for a, b in [(playfab_id, friend_link_id), (friend_link_id, my_link_id)]:
        data = requests.post(
            f"https://{settings.TitleId}.playfabapi.com/Server/GetUserInternalData",
            headers=settings.get_auth_headers(),
            json={"PlayFabId": a}
        ).json()
        friends_str = data.get("data", {}).get("Data", {}).get("Friends", {}).get("Value", "")
        friends = set(friends_str.split(',')) if friends_str else set()
        friends.discard(b)
        requests.post(
            f"https://{settings.TitleId}.playfabapi.com/Server/UpdateUserInternalData",
            headers=settings.get_auth_headers(),
            json={"PlayFabId": a, "Data": {"Friends": ','.join(friends)}}
        )

    return jsonify({"statusCode": 200, "error": None}), 200

@app.route("/api/RequestFriend", methods=["POST"])
@app.route("/re/api/RequestFriend", methods=["POST"])
def RequestFriend():
    rjson = request.get_json()
    playfab_id = rjson.get("PlayFabId", "")
    friend_link_id = rjson.get("FriendFriendLinkId", "")
    ticket = rjson.get("PlayFabTicket", "")
    print(rjson)
    if not playfab_id: return "Must supply a valid PlayFab ID", 400
    if not friend_link_id: return "Must supply a valid FriendFriendLinkId", 400

    auth_session = requests.post(
        f"https://{settings.TitleId}.playfabapi.com/Server/AuthenticateSessionTicket",
        json={"SessionTicket": ticket},
        headers=settings.get_auth_headers()
    )

    if auth_session.status_code != 200 or auth_session.json()["data"]["UserInfo"]["PlayFabId"] != playfab_id:
        return "", 500

    data = requests.post(f"https://{settings.TitleId}.playfabapi.com/Server/GetUserInternalData", headers=settings.get_auth_headers(), json={"PlayFabId": playfab_id}).json()
    friends_str = data.get("data", {}).get("Data", {}).get("Friends", {}).get("Value", "")
    friends = set(friends_str.split(',')) if friends_str else set()
    friends.add(friend_link_id)

    requests.post(
        f"https://{settings.TitleId}.playfabapi.com/Server/UpdateUserInternalData",
        headers=settings.get_auth_headers(),
        json={"PlayFabId": playfab_id, "Data": {"Friends": ','.join(friends)}}
    )

    return jsonify({"statusCode": 200, "error": None}), 200


@app.route("/api/ConsumeOculusIAP", methods=["POST"])
def consume_oculus_iap():
    rjson = request.get_json()

    access_token = rjson.get("userToken")
    user_id = rjson.get("userID")
    nonce = rjson.get("nonce")
    sku = rjson.get("sku")

    response = requests.post(
        url=
        f"https://graph.oculus.com/consume_entitlement?nonce={nonce}&user_id={user_id}&sku={sku}&access_token={settings.ApiKey}",
        headers={"content-type": "application/json"})

    if response.json().get("success"):
        return jsonify({"result": True})
    else:
        return jsonify({"error": True})
        
@app.route("/pf/api/ConsumeCodeItem", methods=["POST"])
@app.route("/re/api/ConsumeCodeItem", methods=["POST"])
@app.route("/reals/api/ConsumeCodeItem", methods=["POST"])
@app.route("/rea/api/ConsumeCodeItem", methods=["POST"])
@app.route("/real/api/ConsumeCodeItem", methods=["POST"])
@app.route("/api/ConsumeCodeItem", methods=["POST"])
def consume_code_item():
    try:
        data = request.get_json()
        code_id = data.get("itemGUID", "").upper()
        playfab_id = data.get("playFabID")
        session_ticket = data.get("playFabSessionTicket")

        codes = load_codes()
        code_entry = find_code(codes, code_id)

        if not code_entry:
            return jsonify({"result": "CodeNotFound"}), 404

        if code_entry["redeemed"]:
            return jsonify({
                "result": "AlreadyRedeemed",
                "playFabItemName": code_entry["cosmetic"]
            }), 200

        grant_response = grant_cosmetic_to_player(playfab_id, code_entry["cosmetic"])

        if grant_response.status_code != 200:
            return jsonify({
                "result": "GrantFailed",
                "error": grant_response.text
            }), 500

        embed = {
            "embeds": [
                {
                    "title": "Ã°Å¸Å½Â - Code Redeemed",
                    "description": (
                        f"**PlayFab ID**: {playfab_id}\n"
                        f"**Redeemed Code**: `{code_id}`\n"
                        f"**Cosmetic Granted**: `{code_entry['cosmetic']}`"
                    ),
                    "color": 0x00ff00
                }
            ]
        }

        requests.post(
            "",
            json=embed
        )

        code_entry["redeemed"] = True
        save_codes(codes)

        return jsonify({
            "result": "Success",
            "itemID": code_id,
            "playFabItemName": code_entry["cosmetic"]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route("/api/GetAcceptedAgreements", methods=["POST", "GET"])
def get_accepted_agreements():
    rjson = request.get_json()["FunctionResult"]
    return jsonify(rjson)

@app.route("/api/SubmitAcceptedAgreements", methods=["POST"])
def SubmitAcceptedAgreements():
    rjson = request.json
    playfab_ticket = rjson.get("PlayFabTicket")
    agreements = rjson.get("Agreements", {})  # Expected format: {key: value}

    # Optional: Validate session ticket with PlayFab API
    auth_session = requests.post(
        f"https://{settings.TitleId}.playfabapi.com/Server/AuthenticateSessionTicket",
        json={"SessionTicket": playfab_ticket},
        headers=settings.get_auth_headers()
    )
    if auth_session.status_code != 200:
        return "", 400  # Invalid ticket

    # Update accepted agreements in PlayFab User Data
    updates = {
        f"accepted_agreement:{key}": val
        for key, val in agreements.items()
    }

    for key, val in updates.items():
        data = {"PlayFabId": playfab_ticket, "Data": {key: val}}
        response = requests.post(
            f"https://{settings.TitleId}.playfabapi.com/Server/UpdateUserData",
            headers=settings.get_auth_headers(),
            json=data
        )
        if response.status_code != 200:
            return jsonify({"error": "Failed to update agreement status"}), 500

    return jsonify({"status": "ok"}), 200



@app.route("/api/ReturnMyOculusHashV2")
def return_my_oculus_hash_v2():
    return return_function_json(request.get_json(), "ReturnMyOculusHash")

@app.route("/api/ReturnCurrentVersionV2", methods=["POST"])
def ReturnCurrentVersionV2():
    rjson = request.json
    print(rjson)
    currentPlayerId = rjson["CallerEntityProfile"]["Lineage"]["MasterPlayerAccountId"]
    if rjson.get("FunctionArgument").get("UpdatedSynchTest") != 12379015:
        ban_user(currentPlayerId)
        
        return jsonify({"Fail": True, "ResultCode": None})

    return jsonify({
        "ResultCode": 0,
        "BannedUsers": "35",
        "MOTD": "SERVER MAINTENANCE HAS COMPLETED! I WOULD SAY PLEASE RETURN TO YOUR MONKEY BUSINESS, BUT I ASSUME NOBODY REALLY STOPPED.",
         "VStumpFeaturedMaps": "4475071",
        "QueueStats": {"TopTroops": []}
    })

def send_discord_embed(playfab_id, name, reason, duration_in_hours):
    embed = {
        "title": "Ã°Å¸Å¡Â« User Banned for Bad Name",
        "color": 0xFF0000,
        "fields": [
            {"name": "PlayFab ID", "value": playfab_id, "inline": True},
            {"name": "Reason", "value": reason, "inline": False},
            {"name": "Duration", "value": f"{duration_in_hours} hour(s)", "inline": True},
            {"name": "Name Used", "value": name or "*Unknown*", "inline": False}
        ],
        "footer": {
            "text": "This ban was issued automatically based on username detection."
        },
        "timestamp": datetime.utcnow().isoformat()
    }

    payload = {"embeds": [embed]}
    headers = {"Content-Type": "application/json"}

    # Log the payload before sending to Discord
    print(f"[Discord Log] Sending embed to Discord: {payload}")

    try:
        res = requests.post("", json=payload, headers=headers)
        if res.status_code != 204:
            print(f"[Discord] Failed to send embed: {res.text}")
    except Exception as e:
        print(f"[Discord] Error sending embed: {str(e)}")

def ban_user(playfab_id, name=None, reason="Bad name detected.", duration_in_hours=1):
    url = f"https://{settings.TitleId}.playfabapi.com/Admin/BanUsers"
    headers = settings.get_auth_headers()
    payload = {
        "Bans": [
            {
                "PlayFabId": playfab_id,
                "Reason": reason,
                "DurationInHours": duration_in_hours
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"[Ban Error] Failed to ban {playfab_id}: {response.text}")
    else:
        print(f"[Ban Success] Banned {playfab_id} for {reason}.")
        send_discord_embed(playfab_id, name, reason, duration_in_hours)


@app.route("/api/TryDistributeCurrencyV2", methods=["POST", "GET"])
def try_distribute_currency_v2():
    return return_function_json(request.get_json(), "TryDistributeCurrency")

@app.route("/api/BroadCastMyRoomV2", methods=["POST", "GET"])
def broadcast_my_room_v2():
    return return_function_json(request.get_json(), "BroadCastMyRoom",
                                request.get_json()["FunctionParameter"])

@app.route("/pf/api/FetchPoll", methods=["POST"])
@app.route("/re/api/FetchPoll", methods=["POST"])
@app.route("/reals/api/FetchPoll", methods=["POST"])
@app.route("/rea/api/FetchPoll", methods=["POST"])
@app.route("/real/api/FetchPoll", methods=["POST"])
@app.route("/pf/api/FetchPoll", methods=["POST"])
@app.route("/api/FetchPoll", methods=["GET", "POST"])
def fetch_poll():
    if request.method != "POST":
        return "", 404

    polls = load_votes()
    return jsonify(polls), 200



@app.route("/api/ShouldUserAutomutePlayer", methods=["POST", "GET"])
def should_user_automute_player():
    return jsonify(mute_cache)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1416)


@app.route("/aa-Mothership.com", methods=["PUT", "POST", "GET", "DELETE"])
def FuckassAuthbro():
    EnvID = Mothership.get("EnvironmentId")
    Token = Mothership.get("Token")
    return jsonify({
        "EnvironmentId": EnvID,
        "Token": Token
    }), 200

@app.route("/pf/api/photon", methods=["POST", "GET"])
@app.route("/api/photon", methods=["POST", "GET"])
def photon():
    rjson = request.get_json()
    print(rjson)
    if not rjson or "Ticket" not in rjson:
        return jsonify({"ResultCode": 0, "UserId": None}), 400

    if rjson["Platform"] != "Quest":
        return jsonify({"ResultCode": 0, "UserId": None}), 400

    if rjson["AppId"] != settings.TitleId:
        return jsonify({"ResultCode": 0, "UserId": None}), 400

    ticket = rjson["Ticket"]
    user_id = ticket.split('-')[0]

    response = requests.post(
        f"https://{settings.TitleId}.playfabapi.com/Server/AuthenticateSessionTicket",
        json={"SessionTicket": ticket},
        headers=settings.get_auth_headers()
    )

    if response.status_code != 200:
        return jsonify({"ResultCode": 0, "UserId": None}), 400

    return jsonify({"ResultCode": 1, "UserId": user_id})


@app.route("/api/RoomJoined", methods=["POST"])
def RoomJoined():
    rjson_raw = request.get_json()
    rjson = rjson_raw if isinstance(rjson_raw, dict) else vars(rjson_raw)

    if not rjson:
        print("RoomJoined 400 - Empty body")
        return jsonify({"ResultCode": 0, "UserId": None}), 400

    if rjson.get("Platform") != "Quest" or rjson.get("AppId") != "9F111":
        print("RoomJoined 400 - Invalid Platform/AppId:")
        print(json.dumps(rjson, indent=2))
        return jsonify({"ResultCode": 0, "UserId": None}), 400

    user_id = rjson.get("UserId", "unknown")
    room_id = rjson.get("RoomId", "unknown")

    try:
        with open("roomcodes.json", "r") as f:
            room_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        room_data = {}

    room_data[user_id] = room_id

    with open("roomcodes.json", "w") as f:
        json.dump(room_data, f, indent=2)


    return jsonify({"ResultCode": 1, "UserId": user_id}), 200


@app.route("/api/RoomLeft", methods=["POST"])
def RoomLeft():
    rjson_raw = request.get_json()
    rjson = rjson_raw if isinstance(rjson_raw, dict) else vars(rjson_raw)

    if not rjson:
        print("RoomLeft 400 - Empty body")
        return jsonify({"ResultCode": 0, "UserId": None}), 400

    if rjson.get("Platform") != "Quest" or rjson.get("AppId") != "9F111":
        print("RoomLeft 400 - Invalid Platform/AppId:")
        print(json.dumps(rjson, indent=2))
        return jsonify({"ResultCode": 0, "UserId": None}), 400

    user_id = rjson.get("UserId", "unknown")

    try:
        with open("roomcodes.json", "r") as f:
            room_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        room_data = {}

    if user_id in room_data:
        del room_data[user_id]

    with open("roomcodes.json", "w") as f:
        json.dump(room_data, f, indent=2)

    return jsonify({"ResultCode": 1, "UserId": user_id}), 200
