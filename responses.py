import random

def get_response(message: str) -> str:
    # python case sensitive so important to have this
    p_message = message.lower() 

    if p_message == 'hello':
        return 'Hey there!'
    
    if p_message == 'roll':
        return str(random.randint(1,6))
    
    if p_message == '!help':
        return '`This is a help message that you can modify.`'
    

# If message not matched to above case will respond to every message
# Maybe look for a better way to implement this not just "return None" since that gives an error in terminal.
    return None 