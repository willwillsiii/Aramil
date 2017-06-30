from functools import singledispatch
import random
import collections
import re

@singledispatch
def rollDice(maxVal, numDice=1):
    
    if maxVal <= 0 or not isinstance(maxVal, int):
        raise ValueError(str(maxVal) +
                         '-sided die does not have a positive integer ' + 
                         'number of faces.')
    if numDice <= 0 or not isinstance(numDice, int):
        raise ValueError(str(numDice) + ' dice is not a positive integer ' +
                         'number of dice.')
    
    if maxVal > 200:
        raise ValueError(str(maxVal) + '-sided die is too large. ' + 
                         'Maximum sides is 200.')
    if numDice > 100:
        raise ValueError(str(numDice) + ' dice is too many. Only roll ' +
                         'up to 100 dice at once.')
    
    rollRes = []
    for x in range(numDice):
        rollRes.append(random.randint(1, maxVal))
    return rollRes

def parseRoll(rollStr):
    # parse
    rollList = re.split(r'([\s\+\-\*\/\(\)])', rollStr)
    # remove empty strings
    rollList = list(filter(None, rollList))
    return rollList

def modRoll(rollStr):
    if rollStr == '': rollStr = 'd'
    numDice, maxVal = tuple(rollStr.split('d'))
    # set defaults for numDice and maxVal
    if numDice == '': numDice = '1'
    if maxVal == '': maxVal = '20'
    roll = numDice + 'd' + maxVal
    Dice = collections.namedtuple('Dice', ['roll', 'numDice', 'maxVal'])
    return Dice(roll, numDice, maxVal)

@rollDice.register(str)
def _(rollStr):
    d = modRoll(rollStr)
    # check for decimals
    if '.' in d.numDice:
        raise ValueError("invalid literal for int() with base 10: 'numDice="
                         + d.numDice + "'")
    if '.' in d.maxVal:
        raise ValueError("invalid literal for int() with base 10: 'maxVal="
                         + d.maxVal + "'")
    return rollDice(int(d.maxVal),int(d.numDice))

def rollMath(rollStr):
    rollList = parseRoll(rollStr)
    # check each element for roll
    for i in range(len(rollList)):
        if 'd' in rollList[i]:
            rollList[i] = str(sum(rollDice(rollList[i])))
    return eval(''.join(rollList))

def chatRoll(msg, verbose=False, formatted=False):
    try:
        msg = msg.strip().split(' ', 1)[1]
    except:
        msg = 'd'
    returnMsg = ''
    modMsg = ''
    rollList = parseRoll(msg)
    if rollList == []: rollList = ['d']
    for i in range(len(rollList)):
        if 'd' in rollList[i]:
            d = modRoll(rollList[i])
            modMsg += d.roll
            rollRes = rollDice(rollList[i])
            rollSum = sum(rollRes)
            if verbose:
                if formatted:
                    if d.numDice == '1':
                        returnMsg += "**" + str(rollRes) + "**"
                    else:
                        returnMsg += ("**" + str(rollRes) + 
                                  "**{" + str(rollSum) + "}")
                else:
                    returnMsg += str(rollRes) + "{" + str(rollSum) + "}"
            rollList[i] = str(rollSum)
        else:
            modMsg += rollList[i]
            if verbose:
                returnMsg += rollList[i]
    returnMsg = modMsg + ' = ' + returnMsg
    if verbose:
        returnMsg += ' = '
    if formatted:
        returnMsg += "**" + str(eval(''.join(rollList))) + "**"
    else:
        returnMsg += str(eval(''.join(rollList)))
    return returnMsg

