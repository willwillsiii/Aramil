import discord
import asyncio
import logging
import random

# homebrew package imports
from dbot import rollDice

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
	if message.content.startswith('!test'):
		counter = 0
		tmp = await client.send_message(message.channel, 'Calculating messages...')
		async for log in client.logs_from(message.channel, limit=100):
			if log.author == message.author:
				counter += 1
		await client.edit_message(tmp, 'You have {} messages.'.format(counter))

	elif message.content.startswith('!sleep'):
		await asyncio.sleep(5)
		await client.send_message(message.channel, 'Done sleeping')
		
	elif message.content.startswith('!roll d6'):
		rollRes = str(random.randint(1,6))
		await client.send_message(message.channel, 'You rolled a ' + rollRes + '.')
		
# Begin Execution
#-----------------
# read token from text file
with open('token.txt', 'r') as tokenFile:
	token = tokenFile.read().replace('\n', '') # remove new-line chars
client.run(token)
