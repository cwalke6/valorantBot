import valorantImages
import bot
import discord
import random
import requests
import re
import json
import messageSettings

from discord.ui import View, Button

api_key = "HDEV-390054ce-97c2-4ab1-bc0b-96fac25d03f7"
urlAlt = 'https://api.kyroskoh.xyz'
url = 'https://api.henrikdev.xyz'
trackerggUrl = 'https://tracker.gg/valorant/match/'
headers = {'Accept': 'application/json'}

headers = {
    "Authorization": api_key,
}

def get_response(message: str) -> str:
    # python case sensitive so important to have this
    p_message = message.lower() 

    
    if p_message == 'roll':
        messageSettings.embed = discord.Embed(title=random.randint(1,6))
        return None
    
    if p_message == '!help':
        messageSettings.embed = discord.Embed(title='Click here for documentation',url='https://github.com/M4nchy/valorantBot')
        # Need to work on actual documentation for the bot
        return None
    
    if p_message == '!login':
        return 'login command'

    if p_message[:6] == '!stats':
        # Need to add latam and br catches
        valorantUsername = ''
        gameMap = ''
        gamemode = ''

        allList = p_message[7:].partition('#')

        # Do it this way in order to incorporate spaces in usernames
        usernameList = allList[0].split()
        for i in range(1, len(usernameList)):
            valorantUsername += usernameList[i] + ' '
        valorantUsername = valorantUsername[:-1]

        affinity = usernameList[0]

        valorantTagAndExtras = allList[2].split()
        valorantTag = valorantTagAndExtras[0]
        if len(valorantTagAndExtras) > 1:
            if len(valorantTagAndExtras[1]) == 1 or len(valorantTagAndExtras[1]) == 2:
                gamesPulled = valorantTagAndExtras[1]
            else:
                gamemode = valorantTagAndExtras[1]
        if len(valorantTagAndExtras) > 2:
            if len(valorantTagAndExtras[2]) == 1 or len(valorantTagAndExtras[2]) == 2:
                gamesPulled = valorantTagAndExtras[2]
            else:
                gameMap = valorantTagAndExtras[2]
        if len(valorantTagAndExtras) > 3:
            gamesPulled = valorantTagAndExtras[3]
        gamesPulled = 5

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
            userAgentList[i] = valorantImages.agentIcons[userAgentList[i].lower()]
        userAgentList = str(userAgentList)[1:-1]
        userAgentList = userAgentList.replace('\'', '')

        if(gamemode != ''):
            messageSettings.embed = discord.Embed(title= 'Recent Stats of: ' + valorantUsername + '#' + valorantTag,
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
            messageSettings.embed = discord.Embed(title= 'Recent Stats of: ' + valorantUsername + '#' + valorantTag,
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

        messageSettings.embed.set_thumbnail(url=userPlayerCard)
        messageSettings.hasEmbed = True

        return None
    
    
    if p_message[:11] == '!rankofuser':
        valorantUsername = ''
        allList = p_message[13:].partition('#')

        # Do it this way in order to incorporate spaces in usernames
        usernameList = allList[0].split()
        for i in range(1, len(usernameList)):
            valorantUsername += usernameList[i] + ' '
        valorantUsername = valorantUsername[:-1]

        affinity = usernameList[0]

        valorantTagAndExtras = allList[2].split()
        valorantTag = valorantTagAndExtras[0]
        if len(valorantTagAndExtras) > 1:
            if len(valorantTagAndExtras[1]) == 1 or len(valorantTagAndExtras[1]) == 2:
                size = valorantTagAndExtras[1]
            else:
                gamemode = valorantTagAndExtras[1]
        if len(valorantTagAndExtras) > 2:
            if len(valorantTagAndExtras[2]) == 1 or len(valorantTagAndExtras[2]) == 2:
                size = valorantTagAndExtras[2]
            else:
                gamemode = valorantTagAndExtras[2]

        accountMessage = json.loads(requests.get(url+'/valorant/v1/account/' + valorantUsername + '/' + valorantTag).text, headers=headers)
        puuid = accountMessage['data']['puuid']

        mmrMessage = json.loads(requests.get(url+'/valorant/v1/by-puuid/mmr/na/' + puuid).text, headers=headers)
        messageSettings.embed = discord.Embed(title=valorantUsername + '#' + valorantTag + ' Rank', description=mmrMessage['data']['currenttierpatched']
                              + ' ' + str(mmrMessage['data']['ranking_in_tier']) + " RR", color=0xFF5733)
        messageSettings.embed.set_thumbnail(url=mmrMessage['data']['images']['large'])
        messageSettings.hasEmbed = True

        return None

    if p_message[:13] == '!matchhistory':
        # make all one line
        matchIDList = []
        trackerggUrlList = []
        agentList = []
        mapList = []
        playerTeamList = []
        playerMatchRecord = []
        redTeamWins = []
        blueTeamWins = []
        killsList = []
        deathsList = []
        assistsList = []

        valorantUsername = ''
        gamemode = ''
        embedTitle = '**Match History**'
        embedDescription = ''
        roundTeamWinsIndex = -1

        allList = p_message[14:].partition('#')

        # Do it this way in order to incorporate spaces in usernames
        usernameList = allList[0].split()
        for i in range(1, len(usernameList)):
            valorantUsername += usernameList[i] + ' '
        valorantUsername = valorantUsername[:-1]

        affinity = usernameList[0]

        valorantTagAndExtras = allList[2].split()
        valorantTag = valorantTagAndExtras[0]
        if len(valorantTagAndExtras) > 1:
            if len(valorantTagAndExtras[1]) == 1 or len(valorantTagAndExtras[1]) == 2:
                size = valorantTagAndExtras[1]
            else:
                gamemode = valorantTagAndExtras[1]
        if len(valorantTagAndExtras) > 2:
            if len(valorantTagAndExtras[2]) == 1 or len(valorantTagAndExtras[2]) == 2:
                size = valorantTagAndExtras[2]
            else:
                gamemode = valorantTagAndExtras[2]

        accountMessage = json.loads(requests.get(url+'/valorant/v1/account/' + valorantUsername + '/' + valorantTag).text, headers=headers)
        puuid = accountMessage['data']['puuid']

        if gamemode == '':
            matchHistoryMessage = requests.get(url+'/valorant/v3/matches/' + affinity + '/' + valorantUsername + '/' + valorantTag + '?size=10', headers=headers)
        else:
            matchHistoryMessage = requests.get(url+'/valorant/v3/matches/' + affinity + '/' + valorantUsername + '/' + valorantTag + '?mode=' + gamemode + '&size=10', headers=headers)
        matchHistoryMessage = matchHistoryMessage.json()

        for match in matchHistoryMessage['data']:
            matchIDList.append(match['metadata']['matchid'])
            mapList.append(match['metadata']['map'])
            for player in match['players']['all_players']:
                if player['puuid'] == puuid:
                    agentList.append(player['character'])
                    playerTeamList.append(player['team'])
                    killsList.append(player['stats']['kills'])
                    deathsList.append(player['stats']['deaths'])
                    assistsList.append(player['stats']['assists'])
            roundTeamWinsIndex += 1
            blueTeamWins.append(0)
            redTeamWins.append(0)
            for rounds in match['rounds']:
                if rounds['winning_team'] == 'Blue':
                    blueTeamWins[roundTeamWinsIndex] += 1
                else:
                    redTeamWins[roundTeamWinsIndex] += 1

        for i in range(len(playerTeamList)):
            if redTeamWins[i] > blueTeamWins[i]:
                if(playerTeamList[i] == 'Red'):
                    playerMatchRecord.append(':green_circle:')
                else:
                    playerMatchRecord.append(':red_circle:')
            if redTeamWins[i] < blueTeamWins[i]:
                if(playerTeamList[i] == 'Blue'):
                    playerMatchRecord.append(':green_circle:')
                else:
                    playerMatchRecord.append(':red_circle:')

        for i in range(len(agentList)):
            agentList[i] = valorantImages.agentIcons[agentList[i].lower()]

        for id in matchIDList:
            matchUrl = trackerggUrl + id
            trackerggUrlList.append(matchUrl)
        for i in range(len(matchIDList)):
            if i>8:
                embedDescription += '**[Match ' + str(i+1) + '](' + trackerggUrlList[i] + ')** ' + ' | ' + playerMatchRecord[i] + ' | ' + mapList[i] + ' | ' + agentList[i] + ' | ' + str(redTeamWins[i]) + '-' + str(blueTeamWins[i]) + ' | ' + str(killsList[i]) + '/' + str(deathsList[i]) + '/' + str(assistsList[i]) + '\n'
            else:
                embedDescription += '**[Match ' + str(i+1) + '](' + trackerggUrlList[i] + ')** ' + ' | ' + playerMatchRecord[i] + ' | ' + mapList[i] + ' | ' + agentList[i] + ' | ' + str(redTeamWins[i]) + '-' + str(blueTeamWins[i]) + ' | ' + str(killsList[i]) + '/' + str(deathsList[i]) + '/' + str(assistsList[i]) + '\n'

        embedDescription += '\n' + 'For detailed stats about a specific match use command: \n \"!match <region> username#tag <gamemode> <match number>\"'

        messageSettings.embed = discord.Embed(title=embedTitle, description=embedDescription)
        messageSettings.hasEmbed = True

        return None
    
    if p_message[:6] == '!match':
        # !match <affinity> <username>#<tag> {gamemode} {match to pull}
        # Pulls whatever match and gamemode requested
        # Should probably make this use the lifetime matches to be able to pull more than 10 matches.

        gamemode = ''
        embedTitle = '**Match Stats**'
        embedDescription = ''
        matchIndex, redTeamWins, blueTeamWins = 1, 0, 0
        playerStatsDict = {}
        tempPlayerpuuid = ''
        playerpuuidList = []
        valorantUsername = ''

        allList = p_message[7:].partition('#')

        # Do it this way in order to incorporate spaces in usernames
        usernameList = allList[0].split()
        for i in range(1, len(usernameList)):
            valorantUsername += usernameList[i] + ' '
        valorantUsername = valorantUsername[:-1]

        affinity = usernameList[0]

        valorantTagAndExtras = allList[2].split()
        valorantTag = valorantTagAndExtras[0]
        if len(valorantTagAndExtras) > 1:
            if len(valorantTagAndExtras[1]) == 1 or len(valorantTagAndExtras[1]) == 2:
                matchIndex = valorantTagAndExtras[1]
            else:
                gamemode = valorantTagAndExtras[1]
        if len(valorantTagAndExtras) > 2:
            if len(valorantTagAndExtras[2]) == 1 or len(valorantTagAndExtras[2]) == 2:
                matchIndex = valorantTagAndExtras[2]
            else:
                gamemode = valorantTagAndExtras[2]

        matchIndex = int(matchIndex)-1

        if gamemode == '':
            matchMessage = requests.get(url+'/valorant/v3/matches/' + affinity + '/' + valorantUsername + '/' + valorantTag + '?size=10', headers=headers)
        else:
            matchMessage = requests.get(url+'/valorant/v3/matches/' + affinity + '/' + valorantUsername + '/' + valorantTag + '?mode=' + gamemode + '&size=10', headers=headers)
        matchMessage = matchMessage.json()

        mapImage = valorantImages.mapIcons[matchMessage['data'][matchIndex]['metadata']['map']]
        matchURL = trackerggUrl + matchMessage['data'][matchIndex]['metadata']['matchid']
        embedDescription = '### **[Tracker.gg Match Link]('+matchURL+')**\n'

        for player in matchMessage['data'][matchIndex]['players']['all_players']:
            playerStatsList = []
            tempPlayerpuuid = player['puuid']
            playerpuuidList.append(tempPlayerpuuid) # MAy not need this
            playerStatsList.append(player['name']) #0
            playerStatsList.append(player['team']) #1
            playerStatsList.append(player['character']) #2
            playerStatsList.append(player['currenttier_patched']) #3
            playerStatsList.append(player['stats']['kills']) #4
            playerStatsList.append(player['stats']['deaths']) #5
            playerStatsList.append(player['stats']['assists']) #6
            playerStatsList.append(player['stats']['score']) #7
            playerStatsDict[tempPlayerpuuid] = playerStatsList

        for rounds in matchMessage['data'][matchIndex]['rounds']:
            if rounds['winning_team'] == 'Red':
                redTeamWins += 1
            else:
                blueTeamWins += 1
        totalRounds = redTeamWins + blueTeamWins

        if redTeamWins < blueTeamWins:
            embedDescription += '**Rounds Won: ' + str(blueTeamWins) + '** :trophy:\n'
        else:
            embedDescription += '**Rounds Won: ' + str(blueTeamWins) + '** \n'

        # Sort the dictionary by Score
        playerStatsDict = dict(sorted(playerStatsDict.items(), key=lambda item: item[1][7], reverse=True))
        first_key = next(iter(playerStatsDict))  # Get the first key

        for key in playerStatsDict:
            if playerStatsDict[key][1] == 'Blue':
                tempName = playerStatsDict[key][0]
                tempCharacter = valorantImages.agentIcons[playerStatsDict[key][2].lower()]
                tempRank = playerStatsDict[key][3]
                tempKills = playerStatsDict[key][4]
                tempDeaths = playerStatsDict[key][5]
                tempAssists = playerStatsDict[key][6]
                tempScore = round(playerStatsDict[key][7] / totalRounds, 0)
                if key == first_key:
                    embedDescription += tempCharacter + ' | ' + tempName + ' | ' + tempRank + ' | ' +str(tempScore)[:-2] + ' | ' + str(tempKills) + '/'  + str(tempDeaths) + '/' + str(tempAssists) + ' :star:' +'\n'
                else:
                    embedDescription += tempCharacter + ' | ' + tempName + ' | ' + tempRank + ' | ' +str(tempScore)[:-2] + ' | ' + str(tempKills) + '/'  + str(tempDeaths) + '/' + str(tempAssists) +'\n'
        embedDescription += '\n'
        if redTeamWins < blueTeamWins:
            embedDescription += '**Rounds Won: ' + str(redTeamWins) + '** : \n'
        else:
            embedDescription += '**Rounds Won: ' + str(redTeamWins) + '** :trophy:\n'
        for key in playerStatsDict:
            if playerStatsDict[key][1] == 'Red':
                tempName = playerStatsDict[key][0]
                tempCharacter = valorantImages.agentIcons[playerStatsDict[key][2].lower()]
                tempRank = playerStatsDict[key][3]
                tempKills = playerStatsDict[key][4]
                tempDeaths = playerStatsDict[key][5]
                tempAssists = playerStatsDict[key][6]
                tempScore = round(playerStatsDict[key][7] / totalRounds, 0)
                if key == first_key:
                    embedDescription += tempCharacter + ' | ' + tempName + ' | ' + tempRank + ' | ' +str(tempScore)[:-2] + ' | ' + str(tempKills) + '/'  + str(tempDeaths) + '/' + str(tempAssists) + ' :star:' +'\n'
                else:
                    embedDescription += tempCharacter + ' | ' + tempName + ' | ' + tempRank + ' | ' +str(tempScore)[:-2] + ' | ' + str(tempKills) + '/'  + str(tempDeaths) + '/' + str(tempAssists) +'\n'
        messageSettings.embed = discord.Embed(title=embedTitle, description=embedDescription)
        messageSettings.hasEmbed = True
        messageSettings.embed.set_thumbnail(url=mapImage)

        return None
    
    if p_message[:12] == '!careerstats':
        # /valorant/v1/lifetime/matches/{affinity}/{name}/{tag}
        gamemode = ''
        valorantUsername = ''

        allList = p_message[13:].partition('#')

        # Do it this way in order to incorporate spaces in usernames
        usernameList = allList[0].split()
        for i in range(1, len(usernameList)):
            valorantUsername += usernameList[i] + ' '
        valorantUsername = valorantUsername[:-1]

        affinity = usernameList[0]

        valorantTagAndExtras = allList[2].split()
        valorantTag = valorantTagAndExtras[0]
        if len(valorantTagAndExtras) > 1:
            if len(valorantTagAndExtras[1]) == 1 or len(valorantTagAndExtras[1]) == 2:
                size = valorantTagAndExtras[1]
            else:
                gamemode = valorantTagAndExtras[1]
        if len(valorantTagAndExtras) > 2:
            if len(valorantTagAndExtras[2]) == 1 or len(valorantTagAndExtras[2]) == 2:
                size = valorantTagAndExtras[2]
            else:
                gamemode = valorantTagAndExtras[2]

        # TO DO: Add if statements to change the url depending on queueries in the command line
        # Only two options are gamemode and size

        if gamemode == '':
            careerMessage = requests.get(url+'/valorant/v1/lifetime/matches/' + affinity + '/' + valorantUsername + '/' + valorantTag, headers=headers)
        else:
            careerMessage = requests.get(url+'/valorant/v1/lifetime/matches/' + affinity + '/' + valorantUsername + '/' + valorantTag + '?mode=' + gamemode, headers=headers)
        careerMessage = careerMessage.json()

        matchIDList = []
        totalShots = 0
        headShots = 0
        headshotPercentage = 0

        for data in careerMessage['data']:
            matchIDList.append(data['meta']['id'])
            totalShots += data['stats']['shots']['head']
            headShots += data['stats']['shots']['head']
            totalShots += data['stats']['shots']['body']
            totalShots += data['stats']['shots']['leg']

        headshotPercentage = (headShots / totalShots)
        headshotPercentage *= 100
        headshotPercentage = str(round(headshotPercentage, 0))
        headshotPercentage = headshotPercentage.rstrip('0')
        headshotPercentage = headshotPercentage[:-1]
        

        messageSettings.embed = discord.Embed(title='**Career Stats**',
                              description='Matches: ' + '\n'
                              'HS%: ' + str(headshotPercentage) + '\n')
        messageSettings.hasEmbed = True

        return None



    if p_message[:5] == '!test':
        embedDescription = valorantImages.agentIcons['deadlock'] + '\n' + '#__**Header 1**__' + '\n' + '## Header 2' + '\n'
        messageSettings.embed = discord.Embed(title='__**Match Averages:**__',
                              description=embedDescription)
        messageSettings.hasEmbed = True
        messageSettings.hasButton = True
        return None

    return None


def returnRankIcon(puuid):
    mmrMessage = json.loads(requests.get(url+'/valorant/v1/by-puuid/mmr/na/' + puuid).text, headers=headers)
    print(mmrMessage['data']['images']['small'])
    return mmrMessage['data']['images']['small']

