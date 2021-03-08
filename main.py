import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person / bot!"
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('ice inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    if msg.startswith("ice new"):
        encouraging_message = msg.split("ice new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("Message added pal")

    if msg.startswith("ice del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("ice del", 1)[1])
            delete_encouragment(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("ice list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("ice responding"):
        value = msg.split("ice responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send(
                "Responding is on. (When you say sad message it will respond.)")
        else:
            db["responding"] = False
            await message.channel.send(
                "Responding is off. (When you say sad message it will not respond.)")

    if msg.startswith("ice lifehacks"):
        await message.channel.send(
            "Life sucks a lot, and there are a lot of things to get past. But life is so hard, there are no hacks to get past it... nub"
        )

    if msg.startswith("ice help"):
        await message.channel.send("This is made to impersonate me not much else This is made to impersonate me not much else. Also join the support server here: https://discord.gg/n7SyHn32rr ```Other cmds: ice help, ice responding true, ice responding false, more commands coming soon/never.     the responding setup: responding false = don't respond to sad messages, and respoding true = respond with positive messages when a user is sad/down.```.")

@client.event
async def displayembed(ctx, title, description, field, name, footer):
    embed = discord.Embed(title=title, description=description)
    embed.add_field(name=name, value=field)
    embed.set_footer(name=footer)
    await ctx.send(embed=embed)

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.idle, activity=discord.Game('Hello. I am impersonating!'))
  print('We have logged in as the bot.')

keep_alive()
client.run(os.getenv('TOKEN'))
