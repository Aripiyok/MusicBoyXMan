from functools import wraps

from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.types import Message
from Music import app, SUDOERS
from typing import List

from pyrogram.types import Chat

from cache.admins import get as gett
from cache.admins import set


async def get_administrators(chat: Chat) -> List[int]:
    get = gett(chat.id)

    if get:
        return get
    else:
        administrators = await chat.get_members(filter="administrators")
        to_set = []

        for administrator in administrators:
            if administrator.can_manage_voice_chats:
                to_set.append(administrator.user.id)

        set(chat.id, to_set)
        return await get_administrators(chat)


async def authorised(message):
    chatID = message.chat.id
    return 0


async def unauthorised(message: Message):
    chatID = message.chat.id
    text = (
        "You don't have the required permission to perform this action."
        + f"\n__REQUIRES ADMIN WITH MANAGE VC RIGHTS__"
    )
    try:
        await message.reply_text(text)
    except ChatWriteForbidden:
        await app.leave_chat(chatID)
    return 1

async def adminsOnly(permission, message):
    chatID = message.chat.id
    if not message.from_user:
        if message.sender_chat:
            return await authorised(message)
        return await unauthorised(message)
    userID = message.from_user.id
    permissions = await member_permissions(chatID, userID)
    if userID not in SUDOERS and permission not in permissions:
        return await unauthorised(message)
    return await authorised( message)
