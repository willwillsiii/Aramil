import random 

def rollDice(maxVal, numDice):
    rollRes=[]
    for x in range(numDice):
        rollRes.append(random.randint(1, maxVal))
    return rollRes

def chatRoll():
        if message.content.startswith('!roll'):
		    msg=message.content
		    rollType = msg.split()[1]
		    numDice = int(rollType.split('d')[0])
		    maxVal = int(rollType.split('d')[1])
		    rollRes = rollDice(numDice, maxVal)
		    await client.send_message(message.channel, str(rollType) + ' = ' + str(rollRes))
