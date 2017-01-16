import random 

def rollDice(maxVal, numDice):
    rollRes=[]
    for x in range(numDice):
        rollRes.append(random.randint(1, maxVal))
    return rollRes
