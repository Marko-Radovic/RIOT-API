import requests
import math
from sheet_api import request_of_data
import time as t
from dotenv import load_dotenv
import os

load_dotenv()
# ---------------------------------------------------- API KEY ---------------------------------------------------------
API_KEY = os.environ.get("RIOT_API_KEY")

# ---------------------------------------------------- SUMMONER NAME ---------------------------------------------------

summoner = input("Please enter summoner name on EUW: ")

# ---------------------------------------------------- PULLING SUMMONER DATA -------------------------------------------

response = requests.get(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={API_KEY}")
response.raise_for_status()
# ---------------------------------------------------- SAVING SUMMONER DATA --------------------------------------------

response_json = response.json()

id = response_json['id']

acc_id = response_json['accountId']

puuid = response_json['puuid']

# ---------------------------------------------------- # OF MATCHES ----------------------------------------------------

# number_of_matches = input("How many matches would you like to pull? (0-100): ")
# starting_match = input("At what match would you like to start")
start_of_data = 500
count_of_matches = 10

# ---------------------------------------------------- PULLING MATCHES DATA --------------------------------------------
while start_of_data > 0:
    matches_response = requests.get(f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}"
                                    f"/ids?queue=420&type=ranked&start={start_of_data}&count={count_of_matches}&api_key={API_KEY}")

    # ---------------------------------------------------- SAVING MATCHES DATA --------------------------------------------

    matches_json = matches_response.json()
    test_list = []
    whole_list =[]
    count = 2

    for match in matches_json:
        individual_response = requests.get(f"https://europe.api.riotgames.com/lol/match/v5/matches/{match}?api_key={API_KEY}")
        individual_match = individual_response.json()
        participants = individual_match['info']['participants']
        for player in participants:
            match_duration = individual_match['info']['gameDuration']/1000
            match_minutes = math.floor(match_duration/60)
            match_seconds = math.floor(match_duration%60)
            cs_per_min = round((player['totalMinionsKilled']+player['neutralMinionsKilled'])/match_duration*60, 1)
            total_cs = player['totalMinionsKilled']+player['neutralMinionsKilled']
            if player['summonerId'] == id:
                game_duration = f"{match_minutes}:{match_seconds}"
                test_list.extend([str(match), str(game_duration),str(player['championName']),str(player['totalMinionsKilled']),str(player['neutralMinionsKilled'])
                                  ,str(total_cs),str(cs_per_min),str(player['visionWardsBoughtInGame']) ,str(player['wardsPlaced'])
                                  ,str(player['totalDamageDealtToChampions']),str(player['damageDealtToTurrets']),str(player['damageDealtToObjectives'])])
                whole_list.append(test_list)
                test_list=[]
                # print(f"{puuid}")
                # print(f"\nGame duration: {match_minutes}:{match_seconds}")
                # print(f"Champion played: {player['championName']}")
                # print(f"KDA:{player['kills']}/{player['deaths']}/{player['assists']}")
                # print(f"Creeps killed:{player['totalMinionsKilled']}")
                # print(f"Monsters killed: {player['neutralMinionsKilled']}")
                # print(f"Creep Score: {player['totalMinionsKilled']+player['neutralMinionsKilled']}")
                # print(f"Total CS/MIN: {cs_per_min}")
                # print(f"Control wards purchased: {player['visionWardsBoughtInGame']}")
                # print(f"Wards placed: {player['wardsPlaced']}")
                # print(f"Vision score: {player['visionScore']}")
                # print(f"Damage dealt to champions: {player['totalDamageDealtToChampions']}")
                # print(f"Damage dealt to turrets: {player['damageDealtToTurrets']}")
                # print(f"Damage dealt to objectives: {player['damageDealtToObjectives']}")
                whole_list.extend(test_list)
                whole_list.reverse()
                start_of_data -= 1
                count+=1
    t.sleep(20)
    print(whole_list)
    request_of_data(whole_list, count)
