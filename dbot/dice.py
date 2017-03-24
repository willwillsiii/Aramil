from functools import singledispatch
import random
import re

@singledispatch
def rollDice(maxVal, numDice = 1):
    
    if maxVal <= 0 or not isinstance(maxVal, int):
        raise ValueError(str(maxVal) + '-sided die does not have a positive integer number of faces.')
    if numDice <= 0 or not isinstance(numDice, int):
        raise ValueError(str(numDice) + ' dice is not a positive integer number of dice.')
    
    if maxVal > 200:
        raise ValueError(str(maxVal) + '-sided die is too large. Maximum sides is 200.')
    if numDice > 100:
        raise ValueError(str(numDice) + ' dice is too many. Only roll up to 100 dice at once.')
        
    rollRes = []
    for x in range(numDice):
        rollRes.append(random.randint(1, maxVal))
    return rollRes

@rollDice.register(str)
def _(rollStr):
    rollList = re.split(r'([\s\+\-\*\/\(\)])', rollStr) #parse
    rollList = list(filter(None, rollList)) #remove empty strings
    for i in range(len(rollList)): #check each element for roll
        if 'd' in rollList[i]:
            numDice = rollList[i].split('d')[0]
            maxVal = rollList[i].split('d')[1]
            if numDice == '': numDice = '1'
            if maxVal == '': maxVal = '6'
            if '.' in numDice:
                raise ValueError("invalid literal numDice=" + numDice + " for int() with base 10: '" + numDice + "'")
            if '.' in maxVal:
                raise ValueError("invalid literal maxVal=" + maxVal + " for int() with base 10: '" + maxVal + "'")
            rollList[i] = str(sum(rollDice(int(maxVal),int(numDice))))
    return eval(''.join(rollList))

def chatRoll(msg):
    msg = msg.split(' ', 1)[1]
    rollRes = rollDice(msg)
    return msg + ' = ' + str(rollRes)
