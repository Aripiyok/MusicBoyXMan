from pyrogram import filters, Client
from pyrogram.types import Message
from Music import app, SUDOERS, Music_START_TIME
import os
import psutil
import time
from datetime import datetime
from Music.MusicUtilities.helpers.time import get_readable_time
from Music.helpers.subcribe import subcribe

async def bot_sys_stats():
    bot_uptime = int(time.time() - Music_START_TIME)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f'''
Uptime: {get_readable_time((bot_uptime))}
CPU: {cpu}%
RAM: {mem}%
Disk: {disk}%'''
    return stats


@app.on_message(filters.command(["ping", "ping@Tg_Vc_00_Bot"]))
@subcribe
async def ping(_, message):
    uptime = await bot_sys_stats()
    start = datetime.now()
    response = await message.reply_photo(
        photo="https://telegra.ph/file/85bb7a9fbbd405521109a.jpg",
        caption=">> Pong!"
    )
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    await response.edit_text(f"✅**__Pong!__**\n`⚡{resp} ms`\n\n<b><u>✨**__Music System Stats__**</u></b>{uptime}")
