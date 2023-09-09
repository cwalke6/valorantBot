# Used to hold global variables to let the message know what to send
import discord

global hasEmbed
global hasButtons
hasEmbed = False
hasButtons = False
embed = discord.Embed()
buttons = ''
action_row = ''

def getHasEmbed():
    return hasEmbed

def getHasBut():
    return hasButtons