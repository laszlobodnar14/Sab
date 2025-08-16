import os

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

gifs = {
    "bak": "https://cdn.discordapp.com/attachments/1059887015505702933/1406314003600248903/sab_bak.gif?ex=68a2037a&is=68a0b1fa&hm=2aaf9ee14c6d3e0e1d192d64c43d8daad197a063b66e088f43249bea5c2bde95&",
    "sab": "https://media.discordapp.net/attachments/1059887015505702933/1405592851102044220/Sab.gif",
    "matepie": "https://media.discordapp.net/attachments/1059887015505702933/1405592851102044220/Sab.gif"
}

@bot.event
async def on_ready():
    print(f"Beléptem mint {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    szoveg = message.content.lower()
    for kulcsszo, gif in gifs.items():
        if kulcsszo in szoveg:
            await message.channel.send(gif)

    await bot.process_commands(message)


token = os.getenv("DISCORD_TOKEN")
bot.run(token)
