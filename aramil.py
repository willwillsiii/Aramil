import discord
import asyncio
import logging
import random

# homebrew package imports
from dbot.dice import chat_roll

# Logging Setup
#---------------
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Client Initialization
#-----------------------
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
            # check for verbose rolling
            if message.content[5:].startswith('v'):
                roll_msg = chat_roll(message.content[6:], True, True)
            else:
                roll_msg = chat_roll(message.content[5:])
        except ValueError as val_err:
            err_msg = str(val_err)

            # max_val is not a positive int
            if 'positive integer number of faces' in err_msg or (
                    'invalid literal max_val') in err_msg:
                sides = err_msg.split('-', 1)[0]
                # split string to get sides, etc. 0.5-sided returns 0.5
                if 'invalid literal' in err_msg:
                    sides = err_msg.split("'")[1]
                # '0.5' returns 0.5
                roll_msg = ("Show me a " + sides +
                           "-sided die and I will roll it for you.")
            # num_dice is not a positive int
            elif 'positive integer number of dice' in err_msg or (
                    'invalid literal num_dice') in err_msg:
                num_dice = err_msg.split(' ', 1)[0]
                # '0.5' returns 0.5
                if 'invalid literal' in err_msg:
                           num_dice = err_msg.split("'")[1]
                if '-' in num_dice:
                    roll_msg = ("Can you roll a negative number of dice?" +
                               " Really, you must teach me.")
                else:
                    roll_msg = ("Sorry, I am no wizard; " + 
                               "therefore, I cannot roll " + num_dice +
                               " dice.")
            elif 'Maximum sides is 200' in err_msg:
                sides = err_msg.split('-', 1)[0]
                roll_msg = ("I don't have a " + sides + "-sided die. "
                           "My collection only has a maximum of " +
                           "200-sided dice.")
            elif '100 dice at once' in err_msg:
                num_dice = err_msg.split(' ', 1)[0]
                roll_msg = ("Using " + num_dice + " dice is illogical. "
                           "If you think you can roll more than 100 at " +
                           "once, do it yourself.")
            else:
                roll_msg = "Sorry, I didn't understand you."
                raise val_err

        except:
            roll_msg = "Sorry, I didn't understand you."
            raise
        finally:
            # prepend mention
            if '\n' in roll_msg:
                roll_msg = ''.join([message.author.mention, ": \n", roll_msg])
            else:
                roll_msg = ''.join([message.author.mention, ": ", roll_msg])
            await client.send_message(message.channel, roll_msg)

# Begin Execution
#-----------------
# read token from text file
with open('token.txt', 'r') as token_file:
    token = token_file.read().replace('\n', '')
client.run(token)
