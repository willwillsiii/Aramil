import random 

def rollDice(numDice, maxVal):
    rollRes=[]
    for x in range(numDice):
        rollRes.append(random.randint(1,maxVal))
    return rollRes
