import os
import discord
from discord.ext import commands, tasks
import re
import aiohttp
import asyncio

last_video_id = None
was_live = False

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

gifs = {
    "bak": "https://cdn.discordapp.com/attachments/1059887015505702933/1406314003600248903/sab_bak.gif",
    "sab": "https://media.discordapp.net/attachments/1059887015505702933/1405592851102044220/Sab.gif",
    "matepie": "https://media.discordapp.net/attachments/1059887015505702933/1405987014582468669/mpiethinking.gif",
    "kuss": "https://media.giphy.com/media/8HvWy0vV3xb6l4FBaR/giphy.gif"
}

links = {
    "supremegoat": "https://op.gg/lol/summoners/euw/TTV%20SupremeG0at-Akali",
    "hanyas": "https://trashcity.net/video/13749/a-kozmopolita-sabkelemen-öklendezős-bevásárlása-a-spar-ban"
}


@bot.event
async def on_ready():
    print(f"Beléptem mint {bot.user}")
    check_tiktok_live.start()
    check_tiktok_new_video.start()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    szoveg = message.content.lower()

    # GIF-ek
    for kulcsszo, gif in gifs.items():
        if kulcsszo in szoveg:
            await message.channel.send(gif)

    # Linkek
    for kulcsszo, link in links.items():
        if kulcsszo in szoveg:
            await message.channel.send(link)

    # TikTok legújabb videó kulcsszó
    if "video" in szoveg:
        username = "egoversal"
        url = f"https://www.tiktok.com/@{username}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
                html = await resp.text()

                video_ids = re.findall(r'video/(\d+)', html)
                if video_ids:
                    latest_id = video_ids[0]
                    await message.channel.send(
                        f"Legújabb TikTok videó apucitol 🎥 \nhttps://www.tiktok.com/@{username}/video/{latest_id}"
                    )

    # parancsok feldolgozása (mindig a végén)
    await bot.process_commands(message)


@tasks.loop(minutes=5)
async def check_tiktok_live():
    global was_live
    username = "egoversal"
    url = f"https://www.tiktok.com/@{username}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
            html = await resp.text()

            is_live = '"liveRoomId"' in html or '"live_room_id"' in html

            if is_live and not was_live:
                was_live = True
                channel = bot.get_channel(1256302102058107010)
                await channel.send(f"@tesztastream Apuci éppen élőben van TikTokon! \n{url}")

            elif not is_live and was_live:
                was_live = False


@tasks.loop(minutes=5)
async def check_tiktok_new_video():
    global last_video_id
    username = "egoversal"
    url = f"https://www.tiktok.com/@{username}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
            html = await resp.text()

            video_ids = re.findall(r'video/(\d+)', html)
            if not video_ids:
                return

            latest_id = video_ids[0]

            if last_video_id is None:
                last_video_id = latest_id
            elif latest_id != last_video_id:
                last_video_id = latest_id
                channel = bot.get_channel(1256302102058107010)
                await channel.send(
                    f"Új TikTok videó @{username}-tól! \nhttps://www.tiktok.com/@{username}/video/{latest_id}"
                )


token = os.getenv("DISCORD_TOKEN")
bot.run(token)
