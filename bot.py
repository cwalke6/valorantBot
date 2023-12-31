import discord
import json
import responses
import messageSettings

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        #await message.channel.send(embed=response)
        if(messageSettings.hasEmbed and messageSettings.hasButtons):
            await message.author.send(embed=messageSettings.embed, components = messageSettings.buttons) if is_private else await message.channel.send(messageSettings.embed, components=messageSettings.buttons)
        elif(messageSettings.hasEmbed):
            await message.author.send(embed=messageSettings.embed) if is_private else await message.channel.send(embed=messageSettings.embed)
        elif(messageSettings.hasButtons):
            None
        else:
            await message.author.send(response)
        messageSettings.hasEmbed = False
        messageSettings.hasButtons = False
        # I think to make it work with dms we need to change the if block of this statement. Since now it is just not doing anything if "is_private == true"
    except Exception as e:
        print(e)



def run_discord_bot():
    with open("config.json", "r") as json_file:
        data = json.load(json_file)

    TOKEN = data["discord_token"]
    intents = discord.Intents.default() # Look for this as the first thing we might have to change for integration if we find problems
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')


    @client.event
    async def on_message(message):
        if message.author == client.user: # to stop infinite loop from bot responding to itself
            return
        
        username = str(message.author) # stores username
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?': # private message for a command and just want to get rid of ? which is done in next line.
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)