from utils.database import get_filter_results, get_file_details, is_subscribed #FROMUTILS DB FILES
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re, asyncio, random
from Script import script
from pyrogram.errors import *
BUTTONS = {}
BOT = {}

@Client.on_message(filters.text & filters.private & filters.incoming)
async def bot_pm_filter(client, message):
    """Handles filtering in bot's private messages like group logic."""
    if message.text.startswith("/"):
        return

    if AUTH_CHANNEL:
        # Check if the user is subscribed to the channel
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📢 Join Updates Channel 📢", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went wrong. Please try again later.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return

    if 2 < len(message.text) < 100:
        search = message.text
        mo_tech_yt = f"**🗂️ Title:** {search}\n\n**📤 Uploaded by: Kuttu Bot**"
        btn = []

        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva

        # Fetch results
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}]🔪{file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://t.me/{nyva}?start=file_{file_id}")]
                )
        else:
            return

        if not btn:
            return

        if len(btn) > 10:
            # Pagination logic
            btns = list(split_list(btn, 10))
            keyword = f"{message.chat.id}-{message.id}"
            BUTTONS[keyword] = {
                "total": len(btns),
                "buttons": btns
            }
            data = BUTTONS[keyword]
            buttons = data['buttons'][0].copy()

            buttons.append(
                [InlineKeyboardButton("NEXT ⏩", callback_data=f"next_0_{keyword}")]
            )
            buttons.append(
                [InlineKeyboardButton(f"📃 Pages 1/{data['total']}", callback_data="pages")]
            )
            await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(f"📃 Pages 1/1", callback_data="pages")]
            )
            autd=await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(150)
            await autd.delete()


@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group_filter(client, message):
    """Handles filtering logic in groups."""
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return

    if 2 < len(message.text) < 50:
        search = message.text
        mo_tech_yt = f"**🗂️ Title:** {search}\n\n**📤 Uploaded by: {message.chat.title}**"
        btn = []
        
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva

        # Fetch results
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}]🔪{file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://t.me/{nyva}?start=file_{file_id}")]
                )
        else:
            return

        if not btn:
            return

        if len(btn) > 10:
            # Pagination logic
            btns = list(split_list(btn, 10))
            keyword = f"{message.chat.id}-{message.id}"
            BUTTONS[keyword] = {
                "total": len(btns),
                "buttons": btns
            }
            data = BUTTONS[keyword]
            buttons = data['buttons'][0].copy()

            buttons.append(
                [InlineKeyboardButton("NEXT ⏩", callback_data=f"next_0_{keyword}")]
            )
            buttons.append(
                [InlineKeyboardButton(f"📃 Pages 1/{data['total']}", callback_data="pages")]
            )
            await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(f"📃 Pages 1/1", callback_data="pages")]
            )
            aut=await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(150)
            await aut.delete()



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
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return

        elif query.data.startswith("file"):
            ident, file_id = query.data.split("_")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('Owner', url=f'https://t.me/im_goutham_josh')]
                    ]
                
                await query.answer()
                au=await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
                k = await message.reply_text("**⚠️ 𝖳𝗁𝗂𝗌 𝗆𝖾𝖽𝗂𝖺 𝗐𝗂𝗅𝗅 𝖻𝖾 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝗐𝗂𝗍𝗁𝗂𝗇 5 𝗆𝗂𝗇𝗎𝗍𝖾.**\n__𝖪𝗂𝗇𝖽𝗅𝗒 𝖿𝗈𝗋𝗐𝖺𝗋𝖽 𝗂𝗍 𝗍𝗈 𝗌𝖺𝗏𝖾𝖽 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌.__")
                await asyncio.sleep(300)
                await au.delete()
                await k.edit("<b>Your File/Video is successfully deleted!!!</b>")
                
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("_")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('Owner', url=f'https://t.me/im_goutham_josh')]
                    ]
                
                await query.answer()
                au=await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
                k = await message.reply_text("**⚠️ 𝖳𝗁𝗂𝗌 𝗆𝖾𝖽𝗂𝖺 𝗐𝗂𝗅𝗅 𝖻𝖾 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝗐𝗂𝗍𝗁𝗂𝗇 5 𝗆𝗂𝗇𝗎𝗍𝖾.**\n__𝖪𝗂𝗇𝖽𝗅𝗒 𝖿𝗈𝗋𝗐𝖺𝗋𝖽 𝗂𝗍 𝗍𝗈 𝗌𝖺𝗏𝖾𝖽 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌.__")
                await asyncio.sleep(300)
                await au.delete()
                await k.edit("<b>Your File/Video is successfully deleted!!!</b>")


        elif query.data == "pages":
            await query.answer("page cb")
    else:
        await query.answer("കൌതുകും ലേശം കൂടുതൽ ആണല്ലേ👀",show_alert=True)
