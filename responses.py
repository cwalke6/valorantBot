import random
import sqlite3
import bot

def get_response(message: str, userID) -> str:
    # python case sensitive so important to have this
    p_message = message.lower() 

    if p_message == 'hello':
        return 'Hey there!'
    
    if p_message == 'roll':
        return str(random.randint(1,6))
    
    if p_message == '!help':
        return '`Here is a link to the github page with a readme on how to use this bot: https://github.com/M4nchy/valorantBot`'
    
    if p_message[:9] == '!register':
        valorantUsernameAndTag = p_message[10:].partition('#')
        valorantUsername = valorantUsernameAndTag[0]
        valorantTag = valorantUsernameAndTag[2]
        sqliteConnection = sqlite3.connect('usernames.db')
        cursor = sqliteConnection.cursor()
        sqlite_insert_query = "INSERT INTO usernames VALUES (\'"+valorantUsername+"\',\'"+valorantTag+"\')"
        count = cursor.execute(sqlite_insert_query)
        
        sqliteConnection.commit()
        print("Row inserted successfully ", cursor.rowcount)
        cursor.close()
        
        return 'Username:' + valorantUsername + 'tag:' + valorantTag

# If message not matched to above case will respond to every message
    return None