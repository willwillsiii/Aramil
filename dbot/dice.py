from functools import singledispatch
import random
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

@rollDice.register(str)
def _(rollStr):
    numDice = rollStr.split('d')[0]
    maxVal = rollStr.split('d')[1]
    # set defaults for numDice and maxVal
    if numDice == '': numDice = '1'
    if maxVal == '': maxVal = '6'
    # check for decimals
    if '.' in numDice:
        raise ValueError("invalid literal numDice=" + numDice +
                         " for int() with base 10: '" + numDice + "'")
    if '.' in maxVal:
        raise ValueError("invalid literal maxVal=" + maxVal +
                         " for int() with base 10: '" + maxVal + "'")
    return rollDice(int(maxVal),int(numDice))

def rollMath(rollStr):
    rollList = parseRoll(rollStr)
    # check each element for roll
    for i in range(len(rollList)):
        if 'd' in rollList[i]:
            rollList[i] = str(sum(rollDice(rollList[i])))
    return eval(''.join(rollList))

def chatRoll(msg, verbose=False, formatted=False):
    msg = msg.split(' ', 1)[1]
    returnMsg = msg
    if verbose:
        returnMsg += " = "
        rollList = parseRoll(msg)
        returnExp = rollList.copy()
        for i in range(len(rollList)):
            if 'd' in rollList[i]:
                rollRes = rollDice(rollList[i])
                rollSum = sum(rollRes)
                if formatted:
                    rollList[i] = ("**" + str(rollRes) + 
                                   "***(" + str(rollSum) + ")*")
                else:
                    rollList[i] = str(rollRes) + "(" + str(rollSum) + ")"
                returnExp[i] = str(rollSum)
            else:
                returnExp[i] = rollList[i]
            returnMsg += rollList[i]
        rollRes = eval(''.join(returnExp))
    else:
        rollRes = rollMath(msg)
    returnMsg += " = " + str(rollRes)
    return returnMsg

