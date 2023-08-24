import agentIconsDict
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
        # Need to add latam and br catches
        command = p_message.split('#')
        list1 = command[0].split()
        list2 = command[1].split()
        usernameAndTagAndExtras = list1 + list2
        affinity = usernameAndTagAndExtras[1]
        valorantUsername = usernameAndTagAndExtras[2]
        valorantTag = usernameAndTagAndExtras[3]
        gamesPulled = 5
        gamemode = ''

        if(len(usernameAndTagAndExtras) > 4):
            if(len(usernameAndTagAndExtras[4]) != 2 and len(usernameAndTagAndExtras[4]) != 1):
                gamemode = usernameAndTagAndExtras[4]
            elif(len(usernameAndTagAndExtras[4]) == 2 or len(usernameAndTagAndExtras[4]) == 1):
                gamesPulled = usernameAndTagAndExtras[4]
        gameMap = ''
        if(len(usernameAndTagAndExtras) > 5):
            if(len(usernameAndTagAndExtras[5]) != 2 and len(usernameAndTagAndExtras[5]) != 1):
                gameMap = usernameAndTagAndExtras[5]
            elif(len(usernameAndTagAndExtras[5]) == 2 or len(usernameAndTagAndExtras[5]) == 1):
                gamesPulled = usernameAndTagAndExtras[5]
        if(len(usernameAndTagAndExtras) > 6):
            gamesPulled = usernameAndTagAndExtras[6]

        accountMessage = requests.get(url+'/valorant/v1/account/' + valorantUsername + '/' + valorantTag, headers=headers)

        accountMessage = accountMessage.json()
        puuid = accountMessage['data']['puuid']

        # Need to add if statements here for type of game mode, page number, and size etc
        # For additional Queries add &<QUERY NAME>=<VALUE> to url

        if(gamemode == '' and gameMap == '' and gamesPulled == 5):
            statsMessage = requests.get(url+ '/valorant/v3/by-puuid/matches/' + affinity + '/' + puuid, headers=headers)
        elif(gamemode == '' and gameMap == '' and gamesPulled != 5):
            statsMessage = requests.get(url+'/valorant/v3/by-puuid/matches/' + affinity + '/' + puuid + '?size=' + gamesPulled, headers=headers)
        elif(gamemode == '' and gameMap != '' and gamesPulled == 5):
            statsMessage = requests.get(url+'/valorant/v3/by-puuid/matches/' + affinity + '/' + puuid + '?map=' + gameMap, headers=headers)
        elif(gamemode == '' and gameMap != '' and gamesPulled != 5):
            statsMessage = requests.get(url+'/valorant/v3/by-puuid/matches/' + affinity + '/' + puuid + '?map=' + gameMap + '&size=' + gamesPulled, headers=headers)
        elif(gamemode != '' and gameMap == '' and gamesPulled == 5):
            statsMessage = requests.get(url+'/valorant/v3/by-puuid/matches/' + affinity + '/' + puuid + '?mode=' + gamemode, headers=headers)
        elif(gamemode != '' and gameMap == '' and gamesPulled != 5):
            statsMessage = requests.get(url+'/valorant/v3/by-puuid/matches/' + affinity + '/' + puuid + '?mode=' + gamemode + '&size=' + gamesPulled, headers=headers)
        elif(gamemode != '' and gameMap != '' and gamesPulled == 5):
            statsMessage = requests.get(url+'/valorant/v3/by-puuid/matches/' + affinity + '/' + puuid + '?mode=' + gamemode + '&map=' + gameMap, headers=headers)            
        elif(gamemode != '' and gameMap != '' and gamesPulled != 5):
            statsMessage = requests.get(url+'/valorant/v3/by-puuid/matches/' + affinity + '/' + puuid + '?mode=' + gamemode + '&map=' + gameMap + '&size=' + gamesPulled, headers=headers)

        mapsList, roundsPlayedList = [], []
        statsMessage = statsMessage.json()

        for data in statsMessage['data']:
            mapsList.append(data['metadata']['map'])
            roundsPlayedList.append(data['metadata']['rounds_played'])

        userPlayerCard = ''
        # userAgentImage = statsMessage['data'][0]['players']['all_players'][0]['assets']['agent']['small']
        if userPlayerCard == '':
            for player in statsMessage['data'][0]['players']['all_players']:
                if player['puuid'] == puuid:
                    userPlayerCard = player['assets']['card']['small']

        userKillsList, userDeathsList, userAssistsList, userAgentList, userScoreList = [], [], [], [], []
        userTotalKills, userTotalDeaths, userTotalAssists, userAvgKills, userAvgDeaths, userAvgAssists, userAvgScore, matchesPulled = 0, 0, 0, 0, 0, 0, 0, 5
        matchesPulled = 5

        for data in statsMessage['data']:
            for player in data['players']['all_players']:
                if player['puuid'] == puuid:
                    userKillsList.append(player['stats']['kills'])
                    userTotalKills += player['stats']['kills']
                    userDeathsList.append(player['stats']['deaths'])
                    userTotalDeaths += player['stats']['deaths']
                    userAssistsList.append(player['stats']['kills'])
                    userTotalAssists += player['stats']['deaths']
                    userAgentList.append(player['character'])
                    userScoreList.append(player['stats']['score'])
        for i in range(len(userScoreList)):
            userAvgScore += (userScoreList[i] / roundsPlayedList[i])
        userAvgScore /= matchesPulled
        userAvgScore = round(userAvgScore, 0)
        userTotalKDA = (userTotalKills + userTotalAssists) / userTotalDeaths
        userTotalKDA = round(userTotalKDA, 2)
        userTotalKD = (userTotalKills / userTotalDeaths)
        userTotalKD = round(userTotalKD, 2)
        userAvgKills = userTotalKills / matchesPulled
        userAvgDeaths = userTotalDeaths / matchesPulled
        userAvgAssists = userTotalAssists / matchesPulled

        # set all agent names to their discord emoji equivalent
        for i in range(len(userAgentList)):
            userAgentList[i] = agentIconsDict.agentIcons[userAgentList[i].lower()]
        userAgentList = str(userAgentList)[1:-1]
        userAgentList = userAgentList.replace('\'', '')

        if(gamemode != ''):
            embed = discord.Embed(title= 'Recent Stats of: ' + valorantUsername + '#' + valorantTag,
                                    description= 'Mode: ' + gamemode + '\n'
                                    'Recent Maps:      ' + str(mapsList) + '\n'
                                    'Agent per game:   ' + str(userAgentList) + '\n'
                                    'Kills per game:   ' + str(userKillsList) + '\n'
                                    'Deaths per game:  ' + str(userDeathsList) + '\n'
                                    'Assists per game: ' +str(userAssistsList) + '\n'
                                    '### __**Match Average**__ \n'
                                    'Average ACS: ' + str(userAvgScore) + '\n'
                                    'Average Kills: ' + str(userAvgKills) +
                                    ' Average Deaths: ' + str(userAvgDeaths) +
                                    ' Average Assists: ' + str(userAvgAssists) + '\n'
                                    'KD:  ' + str(userTotalKD) + '\n'
                                    'KDA: ' + str(userTotalKDA) + '\n', 
                                    color=0xFF5733)
        else:
            embed = discord.Embed(title= 'Recent Stats of: ' + valorantUsername + '#' + valorantTag,
                                    description= 'Mode: All' + '\n'
                                    'Recent Maps:      ' + str(mapsList) + '\n'
                                    'Agent per game:   ' + str(userAgentList) + '\n'
                                    'Kills per game:   ' + str(userKillsList) + '\n'
                                    'Deaths per game:  ' + str(userDeathsList) + '\n'
                                    'Assists per game: ' +str(userAssistsList) + '\n'
                                    '### __**Match Average**__ \n'
                                    'Average ACS: ' + str(userAvgScore) + '\n'
                                    'Average Kills: ' + str(userAvgKills) +
                                    ' Average Deaths: ' + str(userAvgDeaths) +
                                    ' Average Assists: ' + str(userAvgAssists) + '\n'
                                    'KD:  ' + str(userTotalKD) + '\n'
                                    'KDA: ' + str(userTotalKDA) + '\n', 
                                    color=0xFF5733)

        embed.set_thumbnail(url=userPlayerCard)

        return embed
    
    
    if p_message[:11] == '!rankofuser':
        usernameAndTag = p_message[12:].partition('#')
        valorantUsername = usernameAndTag[0]
        valorantTag = usernameAndTag[2]
        accountMessage = json.loads(requests.get(url+'/valorant/v1/account/' + valorantUsername + '/' + valorantTag).text)
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
    
    if p_message[:12] == '!careerstats':
        # /valorant/v1/lifetime/matches/{affinity}/{name}/{tag}
        command = p_message.split('#')
        list1 = command[0].split()
        list2 = command[1].split()
        usernameAndTagAndExtras = list1 + list2
        affinity = usernameAndTagAndExtras[1]
        valorantUsername = usernameAndTagAndExtras[2]
        valorantTag = usernameAndTagAndExtras[3]

        gamemode = ''
        if(len(usernameAndTagAndExtras) > 4):
            gamemode = usernameAndTagAndExtras[4]

        # TO DO: Add if statements to change the url depending on queueries in the command line
        # Only two options are gamemode and map

        if gamemode == '':
            careerMessage = requests.get(url+'/valorant/v1/lifetime/matches/' + affinity + '/' + valorantUsername + '/' + valorantTag)
        else:
            careerMessage = requests.get(url+'/valorant/v1/lifetime/matches/' + affinity + '/' + valorantUsername + '/' + valorantTag + '?=mode' + gamemode)
        careerMessage = careerMessage.json()

        for data in careerMessage['data']:
            


        embed = discord.Embed()

        return embed



    if p_message[:5] == '!test':
        embed = discord.Embed(title='__**Match Averages:**__',
                              description= agentIconsDict.agentIcons['deadlock'] + '\n'
                              '# __**Header 1**__' + '\n'
                              '## Header 2' + '\n')

        return embed
    



def returnRankIcon(puuid):
    mmrMessage = json.loads(requests.get(url+'/valorant/v1/by-puuid/mmr/na/' + puuid).text)
    print(mmrMessage['data']['images']['small'])
    return mmrMessage['data']['images']['small']

# If message not matched to above case will respond to every message
# Maybe look for a better way to implement this not just "return None" since that gives an error in terminal.
    return None 