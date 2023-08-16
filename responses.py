
import random
import requests
import json

api_key = "HDEV-390054ce-97c2-4ab1-bc0b-96fac25d03f7"
urlAlt = 'https://api.kyroskoh.xyz'
url = 'https://api.henrikdev.xyz'

headers = {
    "Authorization": api_key,
}

def get_response(message: str) -> str:
    # python case sensitive so important to have this
    p_message = message.lower() 

    if p_message == 'hello':
        return 'Hey there!'
    
    if p_message == 'roll':
        return str(random.randint(1,6))
    
    if p_message == '!help':
        return '`Here is a link to the github page with a readme on how to use this bot: https://github.com/M4nchy/valorantBot`'
    
    if p_message == '!login':
        return 'login command'

    if p_message == '!stats':
        return 'stats command'
    
    if p_message == '!rank':
        #rank = requests.get(urlAlt+'/valorant/v1/mmr/na/TRENTAKER4000/800mg')
        rank = requests.get(urlAlt+'/valorant/v1/mmr/na/camden/333')
        print("rank: ", rank)
        print("rank text: ", rank.text)
        return rank.text
    
    if p_message[:11] == '!rankofuser':
        usernameAndTag = p_message[12:].partition('#')
        valorantUsername = usernameAndTag[0]
        valorantTag = usernameAndTag[2]

        rank = requests.get(urlAlt+'/valorant/v1/mmr/na/' + valorantUsername + '/' + valorantTag).text
        print(rank)

        return rank

    if p_message == '!matchhistory':
        matchHistory = requests.get(url+'/valorant/v3/matches/na/TRENTAKER4000/800mg')
        print(matchHistory)
        print(matchHistory.text)
        return matchHistory.text
    
    if p_message == '!mmr':
        mmrMessage = requests.get(url+'/valorant/v1/by-puuid/mmr/na/33f2484f-990d-5536-84d3-b32309a6d5b2').text
        print('mmrMessage: ', mmrMessage)
        return mmrMessage

    if p_message[:10] == '!mmrofuser':
        usernameAndTag = p_message[11:].partition('#')
        valorantUsername = usernameAndTag[0]
        valorantTag = usernameAndTag[2]
        accountMessage = json.loads(requests.get(url+'/valorant/v1/account/' + valorantUsername + '/' + valorantTag).text)
        # print(accountMessage['data']['puuid'])
        # print(accountMessage['data']['card']['large'])
        puuid = accountMessage['data']['puuid']

        mmrMessage = json.loads(requests.get(url+'/valorant/v1/by-puuid/mmr/na/' + puuid).text)

        # /valorant/v2/mmr/{affinity}/{name}/{tag}

        return mmrMessage['data']['images']['large']

        return mmrMessage['data']['currenttierpatched'] + ' - ' +  str(mmrMessage['data']['ranking_in_tier']) +  'RR'

# If message not matched to above case will respond to every message
# Maybe look for a better way to implement this not just "return None" since that gives an error in terminal.
    return None 