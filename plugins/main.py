from utils.database import get_filter_results, get_file_details, is_subscribed #FROMUTILS DB FILES
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
from Script import script
import random
from pyrogram.errors import UserNotParticipant
BUTTONS = {}
BOT = {}
FORCE_SUB= "wudixh13"

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(bot, message):
    if message.text.startswith("/"):
        return
    if FORCE_SUB:
        try:
            user = await bot.get_chat_member(FORCE_SUB, message.from_user.id)
            if user.status == "kicked out":
                await message.reply_text("You Are Banned")
                return
        except UserNotParticipant :
            await message.reply_text(
                text="🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 🤭.\n\nDᴏ Yᴏᴜ Wᴀɴᴛ Mᴏᴠɪᴇs?\nTʜᴇɴ Jᴏɪɴ Oᴜʀ Mᴀɪɴ Cʜᴀɴɴᴇʟ Aɴᴅ Wᴀᴛᴄʜ ɪᴛ.😂\n Tʜᴇɴ ɢᴏ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴀɴᴅ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ᴍᴏᴠɪᴇ ᴀɢᴀɪɴ ᴀɴᴅ ɢɪᴠᴇ ɪᴛ ᴀ sᴛᴀʀᴛ...!😁",
                reply_markup=InlineKeyboardMarkup( [[
                 InlineKeyboardButton("🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 🤭", url=f"t.me/{FORCE_SUB}")
                ],[
                    InlineKeyboardButton("🔄 Try Again", callback_data=f"checksub#{file_id}")
                ]]
                    )
            )
            return
    
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        kuttubot = f"🔍Hᴇʀᴇ ɪs ᴛʜᴇ ᴍᴏᴠɪᴇ {search} 🎬" #kuttubot is the search result
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"🎭[{get_size(file.file_size)}]🔸{file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"kuttu#{file_id}")]
                    )
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message.id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="🔰Pᴀɢᴇs 1/1🔰",callback_data="pages")]
            )
            await message.reply_text(kuttubot, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="ɴexᴛ ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🔰Pages 1/{data['total']}",callback_data="pages")]
        )
        await message.reply_text(kuttubot, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.group | filters.private & filters.text & filters.incoming & filters.user(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming | filters.private)
async def group(bot, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        kuttubot = f"🔍Hᴇʀᴇ ɪs ᴛʜᴇ ᴍᴏᴠɪᴇ {search} 🎬" #kuttubot is the search result
        nyva=BOT.get("username")
        if not nyva:
            botusername=await bot.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"🎭[{get_size(file.file_size)}]🔸{file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://t.me/{nyva}?start=kuttu-_-{file_id}")] #./.is mes split
                )
        else:
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="🔰Pᴀɢᴇs 1/1🔰",callback_data="pages")]
            )
            await message.reply_text(kuttubot, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="ɴexᴛ ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🔰Pᴀɢᴇs 1/{data['total']}",callback_data="pages")]
        )
        await message.reply_text(kuttubot, reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

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
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except AttributeError:
        typed = query.from_user.id

    if clicked == typed:
        ident, index, keyword = query.data.split("_")
        index = int(index)

        try:
            data = BUTTONS[keyword]
        except KeyError:
            await query.answer("Yᴏᴜ ᴀʀᴇ ᴜsɪɴɢ ᴛʜɪs ғᴏʀ ᴏɴᴇ ᴏf ᴍʏ ᴏʟᴅ ᴍᴇssᴀɢᴇ, ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ ʀᴇᴏ̨ᴜᴇsᴛ ᴀɢᴀɪɴ.", show_alert=True)
            return

        if query.data.startswith("next"):
            if index < data["total"] - 1:
                new_index = index + 1
                buttons = data['buttons'][new_index].copy()
                buttons.append([InlineKeyboardButton("⏪ ʙaᴄᴋ", callback_data=f"back_{new_index}_{keyword}"),
                                InlineKeyboardButton("ɴexᴛ ⏩", callback_data=f"next_{new_index}_{keyword}")])
                buttons.append([InlineKeyboardButton(f"🔰Pᴀɢᴇs {new_index + 1}/{data['total']}", callback_data="pages")])
            else:
                await query.answer("This is the last page.", show_alert=True)
                return

        elif query.data.startswith("back"):
            if index > 0:
                new_index = index - 1
                buttons = data['buttons'][new_index].copy()
                buttons.append([InlineKeyboardButton("⏪ ʙaᴄᴋ", callback_data=f"back_{new_index}_{keyword}"),
                                InlineKeyboardButton("ɴexᴛ ⏩", callback_data=f"next_{new_index}_{keyword}")])
                buttons.append([InlineKeyboardButton(f"🔰Pᴀɢᴇs {new_index + 1}/{data['total']}", callback_data="pages")])
            else:
                await query.answer("This is the first page.", show_alert=True)
                return

        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
        return
        
        elif query.data.startswith("kuttu"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=[{get_size(file.file_size)}]#get_size(files.file_size) fn() calling in size compresor
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [[
                        InlineKeyboardButton('Movie Group🎥', url='telegram.dog/wudixh')
                ],[
                        InlineKeyboardButton('Kᴜᴛᴛᴜ Bᴏᴛ ™ <Uᴘᴅᴀᴛᴇs>', url='telegram.dog/wudixh13')
                    ]]
                
                await query.answer()
                await bot.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,#cap for file setting in environ
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if FORCE_SUB and not await is_subscribed(bot, query):
                await query.answer("I Lɪᴋᴇ Yᴏᴜʀ Sᴍᴀʀᴛɴᴇss, Bᴜᴛ Dᴏɴ'ᴛ Bᴇ Oᴠᴇʀsᴍᴀʀᴛ 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=[{get_size(file.file_size)}]#get_size(files.file_size) fn() calling in size compresor
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [[
                        InlineKeyboardButton('Movie Group🎥', url='telegram.dog/wudixh')
                ],[
                        InlineKeyboardButton('Kᴜᴛᴛᴜ Bᴏᴛ ™ <Uᴘᴅᴀᴛᴇs>', url='telegram.dog/wudixh13')
                    ]]
                
                await query.answer()
                await bot.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,#cap for file setting in environ
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer("I SEE : ",show_alert=True)
    else:
        await query.answer("I SEE : ",show_alert=True)
