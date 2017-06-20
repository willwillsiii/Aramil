import discord
import asyncio
import logging
import random

# homebrew package imports
from dbot.dice import chatRoll

# log setup
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Initialization
#----------------
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
        
# Chat Commands
#---------------
@client.event
async def on_message(message):
    if message.content.startswith('!roll'):
        try:
            rollMsg = chatRoll(message.content)
        except ValueError as ValErr:
            errMsg = str(ValErr)
            
            if 'positive integer number of faces' in errMsg or 'invalid literal maxVal' in errMsg: #maxVal is not a positive int
                sides = errMsg.split('-', 1)[0] #split string to get sides, etc. 0.5-sided returns 0.5
                if 'invalid literal' in errMsg: sides = errMsg.split("'")[1] # '0.5' returns 0.5
                rollMsg = "Show me a " + sides + "-sided die and I will roll it for you."
            
            elif 'positive integer number of dice' in errMsg or 'invalid literal numDice' in errMsg: #numDice is not a positive int
                numDice = errMsg.split(' ', 1)[0]
                if 'invalid literal' in errMsg: numDice = errMsg.split("'")[1] # '0.5' returns 0.5
                if '-' in numDice:
                    rollMsg = "Can you roll a negative number of dice? Really, you must teach me."
                else:
                    rollMsg = "Sorry, I am no wizard; therefore, I cannot roll " + numDice + " dice."
            
            elif 'Maximum sides is 200' in errMsg:
                sides = errMsg.split('-', 1)[0]
                rollMsg = ("I don't have a " + sides + "-sided die. "
                           "My collection only has a maximum of 200-sided dice.")
            
            elif '100 dice at once' in errMsg:
                numDice = errMsg.split(' ', 1)[0]
                rollMsg = ("Using " + numDice + " dice is illogical. "
                           "If you think you can roll more than 100 at once, do it yourself.")
            else:
                rollMsg = "Sorry, I didn't understand you."
                raise ValErr
                
        except:
            rollMsg = "Sorry, I didn't understand you."
            raise
        finally:
            await client.send_message(message.channel, rollMsg)

# Begin Execution
#-----------------
# read token from text file
with open('token.txt', 'r') as tokenFile:
    token = tokenFile.read().replace('\n', '') # remove new-line chars
client.run(token)
