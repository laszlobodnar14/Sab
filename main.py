import os

import discord
from discord.ext import commands
from discord.ext import tasks
import aiohttp
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

gifs = {
    "bak": "https://cdn.discordapp.com/attachments/1059887015505702933/1406314003600248903/sab_bak.gif?ex=68a2037a&is=68a0b1fa&hm=2aaf9ee14c6d3e0e1d192d64c43d8daad197a063b66e088f43249bea5c2bde95&",
    "sab": "https://media.discordapp.net/attachments/1059887015505702933/1405592851102044220/Sab.gif",
    "matepie": "https://media.discordapp.net/attachments/1059887015505702933/1405987014582468669/mpiethinking.gif?ex=68a2cd32&is=68a17bb2&hm=23dca040c3507a02001113190a27a9447a8a81469326c81d369ce1d75f4e0758&="

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

    @tasks.loop(minutes=5)
    async def check_tiktok_live():
        username = "felhasznalonev"
        url = f"https://www.tiktok.com/@egoversal"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
                html = await resp.text()
                if "LIVE" in html:
                    channel = bot.get_channel(1256302102058107010)
                    await channel.send(f"@tesztastream Sab újra élőben, vajon hány bak fogy el ma? Lesz itt minden, sirás vagy éppen nevetés. {url} ")



token = os.getenv("DISCORD_TOKEN")
bot.run(token)
