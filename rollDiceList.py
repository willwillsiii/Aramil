import random 


def rollDice(numDice, maxVal):
    for x in range(numDice):
        rollRes.append(random.randint(1,maxVal))
        

rollRes=[]
rollDice(6,6)
print(rollRes)
