from functools import singledispatch
import random
import re

@singledispatch
def rollDice(maxVal, numDice = 1):
    rollRes = []
    for x in range(numDice):
        rollRes.append(random.randint(1, maxVal))
    return rollRes

@rollDice.register(str)
def _(rollStr):
    rollList = re.split(r'([\s\+\-\*\/])', rollStr) #parse
    rollList = list(filter(None, rollList)) #remove empty strings
    for i in range(len(rollList)): #check each element for roll
        if 'd' in rollList[i]:
            numDice = rollList[i].split('d')[0]
            maxVal = rollList[i].split('d')[1]
            if numDice == '': numDice = '1'
            if maxVal == '': maxVal = '6'
            rollList[i] = str(sum(rollDice(int(maxVal),int(numDice))))
        return eval(''.join(rollList))

def chatRoll(msg):
    msg = msg.split()[1]
    rollRes = rollDice(msg)
    return msg + ' = ' + str(rollRes)
