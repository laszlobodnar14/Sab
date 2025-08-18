import os
import discord
from discord.ext import commands, tasks
from TikTokApi import TikTokApi
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


    for kulcsszo, gif in gifs.items():
        if kulcsszo in szoveg:
            await message.channel.send(gif)


    for kulcsszo, link in links.items():
        if kulcsszo in szoveg:
            await message.channel.send(link)


    if "video" in szoveg:
        username = "egoversal"
        try:
            with TikTokApi() as api:
                user = api.user(username=username)
                videos = user.videos(count=1)
                latest_video = next(videos)
                video_id = latest_video.id
                await message.channel.send(
                    f"Legújabb TikTok videó apucitol \nhttps://www.tiktok.com/@{username}/video/{video_id}"
                )
        except Exception as e:
            await message.channel.send(f"Matepie egy cigany")

    await bot.process_commands(message)


@tasks.loop(minutes=5)
async def check_tiktok_live():
    global was_live
    username = "egoversal"

    url = f"https://www.tiktok.com/@{username}"

    try:
        with TikTokApi() as api:
            user = api.user(username=username)
            is_live = user.is_live
            channel = bot.get_channel(1256302102058107010)

            if is_live and not was_live:
                was_live = True
                await channel.send(f"@tesztastream Apuci éppen élőben van TikTokon! \n{url}")

            elif not is_live and was_live:
                was_live = False
    except:
        pass


@tasks.loop(minutes=5)
async def check_tiktok_new_video():
    global last_video_id
    username = "egoversal"

    try:
        with TikTokApi() as api:
            user = api.user(username=username)
            videos = user.videos(count=1)
            latest_video = next(videos)
            latest_id = latest_video.id

            if last_video_id is None:
                last_video_id = latest_id
            elif latest_id != last_video_id:
                last_video_id = latest_id
                channel = bot.get_channel(1256302102058107010)
                await channel.send(
                    f"Új TikTok videó @{username}-tól! \nhttps://www.tiktok.com/@{username}/video/{latest_id}"
                )
    except:
        pass


token = os.getenv("DISCORD_TOKEN")
bot.run(token)
