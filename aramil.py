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
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# Chat Commands
#---------------
channel_id_dict = {
        'goodbarrelinn': 258048760930762755,
        'alchemyroom': 285097089535311872
    }
channel = client.get_channel(channel_id_dict['alchemyroom'])
@client.event
async def on_message(message):
    global channel

    if message.content.startswith('!roll'):
        async with message.channel.typing():
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
                    # get sides, i.e. 0.5-sided returns 0.5
                    if 'invalid literal' in err_msg:
                        sides = err_msg.split("'")[1]
                    roll_msg = ("Show me a {}-sided die"
                                " and I will roll it for you.".format(sides))
                # num_dice is not a positive int
                elif 'positive integer number of dice' in err_msg or (
                        'invalid literal num_dice') in err_msg:
                    num_dice = err_msg.split(' ', 1)[0]
                    # '0.5' returns 0.5
                    if 'invalid literal' in err_msg:
                               num_dice = err_msg.split("'")[1]
                    if '-' in num_dice:
                        roll_msg = ("Can you roll a negative number of dice?"
                                   " Really, you must teach me.")
                    else:
                        roll_msg = ("Sorry, I am no wizard;"
                                   " therefore, I cannot roll"
                                   " {} dice.".format(num_dice))
                elif 'Maximum sides is 200' in err_msg:
                    sides = err_msg.split('-', 1)[0]
                    roll_msg = ("I don't have a {}-sided die."
                               " My collection only has a maximum of"
                               " 200-sided dice.".format(sides))
                elif '100 dice at once' in err_msg:
                    num_dice = err_msg.split(' ', 1)[0]
                    roll_msg = ("Using {} dice is illogical."
                        " If you think you can roll more than 100 at once,"
                        " do it yourself.".format(num_dice))
                else:
                    roll_msg = "Sorry, I didn't understand you."
                    raise val_err

            except:
                roll_msg = "Sorry, I didn't understand you."
                raise
            finally:
                # prepend mention
                roll_msg = ''.join([message.author.mention, "\n", roll_msg])
        await message.channel.send(roll_msg)

    if message.author.id == 191661210452754432:
        if message.content.startswith('!say'):
            async with message.channel.typing():
                say_msg = message.content[5:]
            await channel.send(say_msg)
        if message.content.startswith('!channel'):
            async with message.channel.typing():
                channel_name = message.content.split(maxsplit=1)[1]
                try:
                    channel = client.get_channel(channel_id_dict[channel_name])
                    await message.channel.send(
                            "Channel changed to {}.".format(channel_name))
                except KeyError:
                    await message.channel.send(
                        "I don't recognize that channel.")

# Begin Execution
#-----------------
# read token from text file
with open('token.txt', 'r') as token_file:
    token = token_file.read().replace('\n', '')
client.run(token)
