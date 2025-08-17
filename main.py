import os

import discord
from discord.ext import commands
from discord.ext import tasks
import re
import aiohttp
import asyncio

last_video_id = None

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

gifs = {
    "bak": "https://cdn.discordapp.com/attachments/1059887015505702933/1406314003600248903/sab_bak.gif?ex=68a2037a&is=68a0b1fa&hm=2aaf9ee14c6d3e0e1d192d64c43d8daad197a063b66e088f43249bea5c2bde95&",
    "sab": "https://media.discordapp.net/attachments/1059887015505702933/1405592851102044220/Sab.gif",
    "matepie": "https://media.discordapp.net/attachments/1059887015505702933/1405987014582468669/mpiethinking.gif?ex=68a2cd32&is=68a17bb2&hm=23dca040c3507a02001113190a27a9447a8a81469326c81d369ce1d75f4e0758&=",
    "kuss" : "https://media.giphy.com/media/8HvWy0vV3xb6l4FBaR/giphy.gif",
    "niba" : "https://tenor.com/view/letter-n-gif-9063758, https://tenor.com/view/letter-i-gif-9063753, https://tenor.com/view/double-g-letter-g-g-is-here-g-police-letter-g-dancing-gif-27064909, https://tenor.com/view/letter-e-gif-9063749, https://tenor.com/view/letter-r-dancing-dance-moves-letter-gif-17607007 "



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


    @tasks.loop(minutes=5)
    async def check_tiktok_new_video():
        global last_video_id
        username = "egoversal"
        url = f"https://www.tiktok.com/@{username}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
                html = await resp.text()

                video_ids = re.findall(r'video/(\d+)',html)
                if not video_ids:
                    return

                latest_id = video_ids[0]

                if last_video_id is None:
                    last_video_id = latest_id
                elif latest_id != last_video_id:
                    last_video_id = latest_id
                    channel = bot.get_channel(1256302102058107010)
                    await channel.send(
                        f"Sab kiralyunk uj videot toltott fel, irány megnezni! \nhttps://tiktok.com/@{username}/videos/{latest_id}"
                    )





token = os.getenv("DISCORD_TOKEN")
bot.run(token)

