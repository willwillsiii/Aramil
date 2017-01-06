import discord
import random

client = discord.Client()

def roll():
    if message.content.startswith("!roll"):
        if message.content.endswith("d4"):
            d4
        if message.content.endswith("d6"):
            d6
        if message.content.endswith("d8"):
            d8
        if message.content.endswith("d10"):
            d10
        if message.content.endswith("d100"):
            d100
        if message.content.endswith("d12"):
            d12
        if message.content.endswith("d20"):
            d20


            
def d4():
    if message.content.endswith("d4"):
        num1 = randint(1,5)
        client.send_message(message.channel,"you rolled a "+ num1)
        

def d6():
    if message.content.endswith("d6"):
        num1 = randint(1,7)
        client.send_message(message.channel,"you rolled a "+ num1)
def d8():
    if message.content.endswith("d8"):
        num1 = randint(1,9)
        client.send_message(message.channel,"you rolled a "+ num1)

def d10():
    if message.content.endswith("d10"):
        num1 = randint(1,11)
        client.send_message(message.channel,"you rolled a "+ num1)

def d12():
    if message.content.endswith("d12"):
        num1 = randint(1,13)
        client.send_message(message.channel,"you rolled a "+ num1)

def d100():
    if message.content.endswith("d10"):
        num1 = randint(1,101,10)
        client.send_message(message.channel,"you rolled a "+ num1)

def d20():
    if message.content.endswith("d20"):
        num1 = randint(1,21)
        client.send_message(message.channel,"you rolled a "+ num1)













        

client.login('Billsbestestfriend@gmail.com')
client.run
