import os

import aiohttp
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
    "kuss": "https://media.giphy.com/media/8HvWy0vV3xb6l4FBaR/giphy.gif",
    "fika": "https://media.discordapp.net/attachments/1059887015505702933/1409267765000536226/sabfika.gif?ex=68acc262&is=68ab70e2&hm=4572d010c785f17415940e81e5108b09e9eb7c83d4b4283fefd0f8a705fbe8f0&=&width=541&height=960"
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
            async with TikTokApi() as api:
                user = await api.user(username=username)
                videos = await user.videos(count=1)
                if videos:
                    latest_video = videos[0]
                    video_id = latest_video.id
                    await message.channel.send(
                        f"Legújabb TikTok videó apucitol \nhttps://www.tiktok.com/@{username}/video/{video_id}"
                    )
                else:
                    await message.channel.send("Matepie egy cigany")
        except Exception as e:
            await message.channel.send(f"Matepie egy cigany")

    await bot.process_commands(message)


@tasks.loop(minutes=5)
async def check_tiktok_live():
    global was_live
    username = "egoversal"
    url = f"https://www.tiktok.com/@{username}"

    async  with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
            html = await resp.text()
            is_live = '"liveRoomId"' in html or '"live_room_id"' in html

            if is_live and not was_live:
                was_live = True
                channel = bot.get_channel(1256302102058107010)
                await channel.send(f"Apuci eppen eloben kozvetit \n{url}/live")
            elif not is_live and was_live:
                was_live = False



@tasks.loop(minutes=5)
async def check_tiktok_new_video():
    global last_video_id
    username = "egoversal"

    try:
        async with TikTokApi() as api:
            user = await api.user(username=username)
            videos = await user.videos(count=1)
            if videos:
                latest_video = videos[0]
                latest_id = latest_video.id

                if last_video_id is None:
                    last_video_id = latest_id
                elif latest_id != last_video_id:
                    last_video_id = latest_id
                    channel = bot.get_channel(1256302102058107010)
                    await channel.send(
                        f"Új TikTok videó @{username}-tól! \nhttps://www.tiktok.com/@{username}/video/{latest_id}"
                    )
    except Exception as e:
        print(f"Matepie egy cigany")



token = os.getenv("DISCORD_TOKEN")
bot.run(token)

