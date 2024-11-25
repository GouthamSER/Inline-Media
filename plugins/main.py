from utils.database import get_filter_results, get_file_details, is_subscribed
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re, asyncio
from Script import script
import random
from pyrogram.errors import *
BUTTONS = {}
BOT = {}


async def send_search_result(bot, message, search, private=True):
    btn = []
    kuttubot = f"<u>🎊 𝖧𝖾𝗋𝖾 𝖨𝗌 𝖶𝗁𝖺𝗍 𝖨 𝖥𝗈𝗎𝗇𝖽 𝖥𝗈𝗋 𝖸𝗈𝗎𝗋 {search} 🎊 </u>"
    files = await get_filter_results(query=search)
    
    if files:
        for file in files:
            file_id = file.file_id
            filename = f"[{get_size(file.file_size)}]💿{file.file_name}"
            if private:
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", callback_data=f"kuttu={file_id}")]
                )
            else:
                nyva = BOT.get("username")
                if not nyva:
                    botusername = await bot.get_me()
                    nyva = botusername.username
                    BOT["username"] = nyva
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://t.me/{nyva}?start=kuttu={file_id}")]
                )

    if not btn:
        nres = await message.reply_text(script.NO_RES.format(search))
        await asyncio.sleep(30)
        await nres.delete()
        return

    if len(btn) > 10:
        btns = list(split_list(btn, 10))
        keyword = f"{message.chat.id}-{message.id}"
        BUTTONS[keyword] = {
            "total": len(btns),
            "buttons": btns
        }
        current_page = 0
        buttons = btns[current_page].copy()

        navigation_buttons = [
            InlineKeyboardButton(f"📃 Pages {current_page + 1}/{len(btns)}", callback_data="pages"),
            InlineKeyboardButton("Next ⏩", callback_data=f"next_{current_page+1}_{keyword}")
        ]
        buttons.append(navigation_buttons)

        autodelete = await message.reply_text(kuttubot, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        buttons = btn.copy()
        buttons.append([InlineKeyboardButton("📃 Pages", callback_data="pages")])
        autodelete = await message.reply_text(kuttubot, reply_markup=InlineKeyboardMarkup(buttons))

    await asyncio.sleep(300)
    await autodelete.delete()


@Client.on_callback_query(filters.regex(r"^next_\d+_.+"))
async def handle_next_callback(bot: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except AttributeError:
        typed = query.from_user.id

    if clicked == typed:
        _, index, keyword = query.data.split("_", maxsplit=2)
        index = int(index)

        try:
            data = BUTTONS[keyword]
        except KeyError:
            await query.answer("This message is outdated. Please send the request again.")
            return

        if index < data["total"]:
            buttons = data['buttons'][index].copy()
            buttons.append([
                InlineKeyboardButton("⏪ Back", callback_data=f"back_{index - 1}_{keyword}"),
                InlineKeyboardButton("Next ⏩", callback_data=f"next_{index + 1}_{keyword}")
            ])
        await query.answer("Next Page")
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await query.answer("You are not allowed to interact with this message.")


@Client.on_callback_query(filters.regex(r"^back_\d+_.+"))
async def handle_back_callback(bot: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except AttributeError:
        typed = query.from_user.id

    if clicked == typed:
        _, index, keyword = query.data.split("_", maxsplit=2)
        index = int(index)

        try:
            data = BUTTONS[keyword]
        except KeyError:
            await query.answer("This message is outdated. Please send the request again.")
            return

        if index >= 0:
            buttons = data['buttons'][index].copy()
            buttons.append([
                InlineKeyboardButton("⏪ Back", callback_data=f"back_{index - 1}_{keyword}"),
                InlineKeyboardButton("Next ⏩", callback_data=f"next_{index + 1}_{keyword}")
            ])
        await query.answer("Previous Page")
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await query.answer("You are not allowed to interact with this message.")


@Client.on_callback_query(filters.regex(r"^kuttu=.*"))
async def handle_kuttu_callback(bot: Client, query: CallbackQuery):
    ident, file_id = query.data.split("=")
    filedetails = await get_file_details(file_id)
    for files in filedetails:
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption or f"{title}"

        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
            except Exception as e:
                print(e)

        buttons = [[
            InlineKeyboardButton('Movie Group 🎥', url='https://telegram.dog/wudixh')
        ]]

        await query.answer()
        await bot.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            reply_markup=InlineKeyboardMarkup(buttons)
        )


def get_size(size):
    units = ["By", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])


def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
