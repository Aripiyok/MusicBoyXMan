from pyrogram.errors import ChatAdminRequired, ChatWriteForbidden, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Music import app
from Music.config import MUST_JOIN


def subcribe(func):
    async def wrapper(_, message: Message):
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        if not MUST_JOIN:  # Not compulsory
            return
        try:
            try:
                await app.get_chat_member(MUST_JOIN, message.from_user.id)
            except UserNotParticipant:
                if MUST_JOIN.isalpha():
                    link = "https://t.me/" + MUST_JOIN
                else:
                    chat_info = await app.get_chat(MUST_JOIN)
                    link = chat_info.invite_link
                try:
                    await message.reply(
                        f"**Hy kak** {rpk} **__Untuk menghindari penggunaan yang berlebihan bot ini di khususkan untuk yang sudah join di channel kami!__**",
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                               [[InlineKeyboardButton("•• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •• ", url=link)]]
                    ),
                )
                    await message.stop_propagation()
                except ChatWriteForbidden:
                    pass
        except ChatAdminRequired:
            print(f"Saya bukan admin di chat MUST_JOIN chat : {MUST_JOIN} !")

    return wrapper
