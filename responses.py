import bot
import discord
import random
import requests
import re
import json


api_key = "HDEV-390054ce-97c2-4ab1-bc0b-96fac25d03f7"
urlAlt = 'https://api.kyroskoh.xyz'
url = 'https://api.henrikdev.xyz'
headers = {'Accept': 'application/json'}

headers = {
    "Authorization": api_key,
}

def get_response(message: str) -> str:
    # python case sensitive so important to have this
    p_message = message.lower() 

    
    if p_message == 'roll':
        embed = discord.Embed(title=random.randint(1,6))
        return embed
    
    if p_message == '!help':
        embed = discord.Embed(title='Click here for documentation',url='https://github.com/M4nchy/valorantBot')
        # Need to work on actual documentation for the bot
        return embed
    
    if p_message == '!login':

        return 'login command'

    if p_message[:6] == '!stats':
        # !stats na TRENTAKER4000#800mg competitive ascent
        affinity = ''
        if(p_message[7:9] == 'na'):
            affinity = p_message[7:9]
            usernameAndTagAndExtras = p_message[10:].split('#')
        elif(p_message[7:9] == 'eu'):
            affinity = p_message[7:9]
            usernameAndTagAndExtras = p_message[10:].split('#')
        elif(p_message[7:9] == 'kr'):
            affinity = p_message[7:9]
            usernameAndTagAndExtras = p_message[10:].split('#')

        valorantUsername = usernameAndTagAndExtras[0]
        usernameAndTagAndExtras = usernameAndTagAndExtras[1].split()
        valorantTag = usernameAndTagAndExtras[0]

        gamemode = ''
        if(len(usernameAndTagAndExtras) > 1):
            gamemode = usernameAndTagAndExtras[1]
        gameMap = ''
        if(len(usernameAndTagAndExtras) > 2):
            gameMap = usernameAndTagAndExtras[2]

        accountMessage = requests.get(url+'/valorant/v1/account/' + valorantUsername + '/' + valorantTag, headers=headers)

        accountMessage = accountMessage.json()
        puuid = accountMessage['data']['puuid']

        # Need to add if statements here for type of game mode, page number, and size etc
        if(gamemode == ''):
            statsMessage = requests.get(url+ '/valorant/v3/by-puuid/matches/' + affinity + '/' + puuid, headers=headers)
        elif(gamemode != '' and gameMap == ''):
            statsMessage = requests.get(url+'/valorant/v3/by-puuid/matches/' + affinity + '/' + puuid + '?mode=' + gamemode, headers=headers)
        elif(gamemode != '' and gameMap != ''):
            statsMessage = requests.get(url+'/valorant/v3/by-puuid/matches/' + affinity + '/' + puuid, + '?mode=' + gamemode, headers=headers)

        mapsList = []
        
        statsMessage = statsMessage.json()

        for data in statsMessage['data']:
            mapsList.append(data['metadata']['map'])

        userPlayerCard = ''
        # userAgentImage = statsMessage['data'][0]['players']['all_players'][0]['assets']['agent']['small']
        if userPlayerCard == '':
            for player in statsMessage['data'][0]['players']['all_players']:
                if player['puuid'] == puuid:
                    userPlayerCard = player['assets']['card']['small']
        userTotalKills = 0
        userTotalDeaths = 0
        userTotalAssists = 0

        for data in statsMessage['data']:
            for player in data['players']['all_players']:
                if player['puuid'] == puuid:
                    userTotalKills += player['stats']['kills']
                    userTotalDeaths += player['stats']['deaths']
                    userTotalAssists += player['stats']['deaths']

        userTotalKDA = (userTotalKills + userTotalAssists) / userTotalDeaths
        userTotalKDA = round(userTotalKDA, 2)

        embed = discord.Embed(title= 'Recent Stats of: ' + valorantUsername + '#' + valorantTag,
                              description= 'Recent Maps: ' + str(mapsList) + '\n'
                              'Mode: ' + gamemode + '\n'
                              'Total Kills: ' + str(userTotalKills) + '\n'
                              'Total Deaths: ' + str(userTotalDeaths) + '\n'
                              'Total Assists: ' + str(userTotalAssists) + '\n'
                              'KDA: ' + str(userTotalKDA) + '\n', 
                              color=0xFF5733)

        embed.set_thumbnail(url=userPlayerCard)

        return embed
    
    
    if p_message[:11] == '!rankofuser':
        usernameAndTag = p_message[12:].partition('#')
        valorantUsername = usernameAndTag[0]
        valorantTag = usernameAndTag[2]
        accountMessage = json.loads(requests.get(url+'/valorant/v1/account/' + valorantUsername + '/' + valorantTag).text)
        print(url+'/valorant/v1/account/' + valorantUsername + '/' + valorantTag)
        puuid = accountMessage['data']['puuid']

        mmrMessage = json.loads(requests.get(url+'/valorant/v1/by-puuid/mmr/na/' + puuid).text)

        embed = discord.Embed(title=valorantUsername + '#' + valorantTag + ' Rank', description=mmrMessage['data']['currenttierpatched']
                              + ' ' + str(mmrMessage['data']['ranking_in_tier']) + " RR", color=0xFF5733)
        embed.set_thumbnail(url=mmrMessage['data']['images']['large'])

        return embed

    if p_message[:13] == '!matchhistory':
        usernameAndTag = p_message[14:].partition('#')
        valorantUsername = usernameAndTag[0]
        valorantTag = usernameAndTag[2]
        matchHistoryMessage = json.loads(requests.get(url+'/valorant/v3/matches/na/' + valorantUsername + '/' + valorantTag))
        

        return matchHistoryMessage.text
    



def returnRankIcon(puuid):
    mmrMessage = json.loads(requests.get(url+'/valorant/v1/by-puuid/mmr/na/' + puuid).text)
    print(mmrMessage['data']['images']['small'])
    return mmrMessage['data']['images']['small']

# If message not matched to above case will respond to every message
# Maybe look for a better way to implement this not just "return None" since that gives an error in terminal.
    return None 