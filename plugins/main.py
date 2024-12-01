from utils.database import get_filter_results, get_file_details, is_subscribed #FROMUTILS DB FILES
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
    mv_rqst = search
    reqst_gle = mv_rqst.replace(" ", "+")
    buttonres = [[
        InlineKeyboardButton('🔍 Search 🔎', url=f"https://www.google.com/search?q={reqst_gle}")
    ]]
    kuttubot = f"<u>🎊 Here is what I found for your search: {search} 🎊</u>"
    files = await get_filter_results(query=search)

    if files:
        for file in files:
            file_id = file.file_id
            filename = f"[{get_size(file.file_size)}] 💿 {file.file_name}"
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

    # Handle no results
    if not btn:
        nres = await message.reply_text(
            text=script.NO_RES.format(search),
            reply_markup=InlineKeyboardMarkup(buttonres)
        )  # No result message from script.py
        await asyncio.sleep(12)
        await nres.delete()
        return

    # Handle pagination
    if len(btn) > 10:
        btns = list(split_list(btn, 10))  # Split into pages of 10 buttons
        keyword = f"{message.chat.id}-{message.id}"
        BUTTONS[keyword] = {
            "total": len(btns),
            "buttons": btns
        }
        data = BUTTONS[keyword]
        current_page = 0
        buttons = data['buttons'][current_page].copy()

        # Add pagination buttons
        navigation_buttons = [
            InlineKeyboardButton(f"📃 1/{data['total']}", callback_data="pages"),
            InlineKeyboardButton("Next ⏩", callback_data=f"next_{current_page+1}_{keyword}")
        ]
        buttons.append(navigation_buttons)

        # Send the message with inline keyboard
        autodelete = await message.reply_text(kuttubot, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        # No pagination needed
        buttons = btn.copy()
        buttons.append([InlineKeyboardButton("📃 1", callback_data="pages")])

        # Send the message without pagination
        autodelete = await message.reply_text(kuttubot, reply_markup=InlineKeyboardMarkup(buttons))
    
    # Auto-delete message after 5 minutes
    await asyncio.sleep(300)
    await autodelete.delete()


@Client.on_message(filters.text & (filters.group | filters.private) & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & (filters.group | filters.private) & filters.incoming)
async def filter_message(bot, message):
    if message.text.startswith("/"):
        return
#filter for group from pm to group
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return

    if 2 < len(message.text) < 100:
        await send_search_result(bot, message, message.text, private=message.chat.type == "private")

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

@Client.on_callback_query()
async def cb_handler(bot: Client, query: CallbackQuery):
    clicked_user = query.from_user.id
    try:
        # Check if the callback is linked to the original user
        target_user = query.message.reply_to_message.from_user.id
    except AttributeError:
        target_user = query.from_user.id
    except Exception as e:
        print(f"Error determining target user: {e}")

    if clicked_user == target_user:
        if query.data.startswith("next") or query.data.startswith("back"):
            # Extract pagination details
            action, index, keyword = query.data.split("_", maxsplit=2)
            index = int(index)

            try:
                data = BUTTONS[keyword]  # Retrieve stored pagination data
            except KeyError:
                await query.answer("This message is outdated. Please request the search again.", show_alert=True)
                return
            except Exception as e:
                print(f"Error fetching pagination data: {e}")

            # Handle "Next" action
            if action == "next":
                if index < data["total"] - 1:
                    buttons = data['buttons'][index + 1].copy()
                    buttons.append([
                        InlineKeyboardButton("⏪ Back", callback_data=f"back_{index + 1}_{keyword}"),
                        InlineKeyboardButton("Next ⏩", callback_data=f"next_{index + 1}_{keyword}")
                    ])
                else:
                    buttons = data['buttons'][index].copy()
                    buttons.append([
                        InlineKeyboardButton(f"📃 Page {index + 1}/{data['total']}", callback_data="pages"),
                        InlineKeyboardButton("⏪ Back", callback_data=f"back_{index}_{keyword}")
                    ])
                await query.answer("Next Page")
                await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))

            # Handle "Back" action
            elif action == "back":
                if index > 0:
                    buttons = data['buttons'][index - 1].copy()
                    buttons.append([
                        InlineKeyboardButton("⏪ Back", callback_data=f"back_{index - 1}_{keyword}"),
                        InlineKeyboardButton("Next ⏩", callback_data=f"next_{index - 1}_{keyword}")
                    ])
                else:
                    buttons = data['buttons'][0].copy()
                    buttons.append([
                        InlineKeyboardButton(f"📃 Page {index + 1}/{data['total']}", callback_data="pages"),
                        InlineKeyboardButton("Next ⏩", callback_data=f"next_{index}_{keyword}")
                    ])
                await query.answer("Previous Page")
                await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data.startswith("kuttu"):
            # Handle custom callback for file retrieval
            _, file_id = query.data.split("=")
            filedetails = await get_file_details(file_id)
            for file in filedetails:
                title = file.file_name
                size = get_size(file.file_size)
                caption = file.caption or f"{title}"
                
                if CUSTOM_FILE_CAPTION:
                    try:
                        caption = CUSTOM_FILE_CAPTION.format(
                            file_name=title,
                            file_size=size,
                            file_caption=caption
                        )
                    except Exception as e:
                        print(f"Error formatting caption: {e}")

                buttons = [[
                    InlineKeyboardButton('🎥 Movie Group', url='https://telegram.dog/wudixh')
                ]]
                
                await query.answer()
                await bot.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )

        elif query.data == "pages":
            # Handle "pages" callback
            try:
                await query.answer("Page navigation is displayed.")
            except Exception as e:
                print(f"Error handling 'pages' callback: {e}")

    else:
        await query.answer("This action is not for you.", show_alert=True)
