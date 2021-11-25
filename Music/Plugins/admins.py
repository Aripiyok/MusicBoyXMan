from asyncio import QueueEmpty
from pyrogram import Client, filters
from pyrogram.types import Message, Audio, Voice
from Music import app
from Music.MusicUtilities.helpers.decorators import authorized_users_only, errors
from Music.MusicUtilities.helpers.filters import command, other_filters
from Music.MusicUtilities.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
import os
import yt_dlp
from youtubesearchpython import VideosSearch
from os import path
import random
import asyncio
import shutil
from time import time
import time as sedtime
from Music import dbb, app, BOT_USERNAME, BOT_ID, ASSID, ASSNAME, ASSUSERNAME, ASSMENTION
from cache.admins import admins
from Music.MusicUtilities.tgcallsrun import (music, convert, download, clear, get, is_empty, put, task_done, smexy)
from Music.MusicUtilities.helpers.gets import (get_url, themes, random_assistant)
from pyrogram.types import Message
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
from Music.MusicUtilities.helpers.thumbnails import gen_thumb
from Music.MusicUtilities.helpers.chattitle import CHAT_TITLE
from Music.MusicUtilities.helpers.ytdl import ytdl_opts 
from Music.MusicUtilities.helpers.inline import (play_keyboard, search_markup, play_markup, playlist_markup, audio_markup)
from Music.MusicUtilities.tgcallsrun import (convert, download)
from pyrogram import filters
from typing import Dict, List, Union
from youtubesearchpython import VideosSearch
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant


@app.on_message(filters.command("cleandb"))
async def stop_cmd(_, message): 
    chat_id = message.chat.id
    try:
        clear(chat_id)
    except QueueEmpty:
        pass                        
    await remove_active_chat(chat_id)
    try:
        await music.pytgcalls.leave_group_call(chat_id)
    except:
        pass   
    await message.reply_text("Erased Databae, Queues, Logs, Raw Files, Downloads.")
    
@app.on_message(filters.command("pause"))
async def pause_cmd(_, message): 
    if message.sender_chat:
        return await message.reply_text("You're an __Anonymous Admin__!\nRevert back to User Account.") 
    permission = "can_manage_voice_chats"
    checking = message.from_user.mention
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text("I dont think if something's playing on voice chat")
    elif not await is_music_playing(message.chat.id):
        return await message.reply_text("I dont think if something's playing on voice chat")   
    await music_off(chat_id)
    await music.pytgcalls.pause_stream(chat_id)
    await message.reply_text(f"🎧 Voicechat Paused by {checking}!")
    
@app.on_message(filters.command("resume"))
async def stop_cmd(_, message): 
    if message.sender_chat:
        return await message.reply_text("You're an __Anonymous Admin__!\nRevert back to User Account.") 
    permission = "can_manage_voice_chats"
    checking = message.from_user.mention
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text("I dont think if something's playing on voice chat")
    elif await is_music_playing(chat_id):
        return await message.reply_text("I dont think if something's playing on voice chat") 
    else:
        await music_on(chat_id)
        await music.pytgcalls.resume_stream(chat_id)
        await message.reply_text(f"🎧 Voicechat Resumed by {checking}!")

@app.on_message(filters.command(["stop", "end"]))
async def stop_cmd(_, message): 
    if message.sender_chat:
        return await message.reply_text("You're an __Anonymous Admin__!\nRevert back to User Account.") 
    permission = "can_manage_voice_chats"
    checking = message.from_user.mention
    chat_id = message.chat.id
    if await is_active_chat(chat_id):
        try:
            clear(chat_id)
        except QueueEmpty:
            pass                        
        await remove_active_chat(chat_id)
        await music.pytgcalls.leave_group_call(chat_id)
        await message.reply_text(f"🎧 Voicechat End/Stopped by {checking}!") 
    else:
        return await message.reply_text("I dont think if something's playing on voice chat")
    
@app.on_message(filters.command("skip"))
async def stop_cmd(_, message): 
    if message.sender_chat:
        return await message.reply_text("You're an __Anonymous Admin__!\nRevert back to User Account.") 
    permission = "can_manage_voice_chats"
    checking = message.from_user.mention
    chat_id = message.chat.id
    chat_title = message.chat.title
    if not await is_active_chat(chat_id):
           await message.reply_text("Nothing's playing on Music")
