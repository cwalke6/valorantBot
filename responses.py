
import random
import requests

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
        rank = requests.get('https://api.kyroskoh.xyz/valorant/v1/mmr/na/TRENTAKER4000/800mg')
        return rank
    

# If message not matched to above case will respond to every message
# Maybe look for a better way to implement this not just "return None" since that gives an error in terminal.
    return None 