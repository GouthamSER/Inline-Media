import re, os, logging, asyncio, random
import time, shutil, psutil, sys #for cb usage alert in startcmnd cb
from utils import Media
from utils.database import get_file_details #forsutofilter
from pyrogram import Client, filters, StopPropagation, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import *
from info import CHANNELS, ADMINS, INVITE_MSG, LOG_CHANNEL, PICS, CUSTOM_FILE_CAPTION, AUTH_CHANNEL, BOT_START_TIME
from utils import Media #class 2 are there dbstatus.py and database.py class Database and class Media
from utils.dbstatus import db #db import from dbstatus.py
from Script import script
from plugins.inline import size_formatter

logger = logging.getLogger(__name__)

FORCE_SUB1 = "wudixh14"
FORCE_SUB2 = "wudixh"

@Client.on_message(filters.command("start"))
async def start(bot, message):
    # USER SAVING IN DB
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOGP_TXT.format(message.from_user.id, message.from_user.mention))
        
    user_cmnd = message.text
    if user_cmnd.startswith("/start kuttu"):
        if FORCE_SUB1 or FORCE_SUB2:
            try:
                # Check subscription status for the first channel
                user1 = await bot.get_chat_member(FORCE_SUB1, message.from_user.id)
                if user1.status == "kicked":
                    await message.reply_text("You are banned from the first required channel.")
                    return

                # Check subscription status for the second channel
                user2 = await bot.get_chat_member(FORCE_SUB2, message.from_user.id)
                if user2.status == "kicked":
                    await message.reply_text("You are banned from the second required channel.")
                    return

            except UserNotParticipant:
                # Prompt user to join both channels
                await message.reply_text(
                    text="🔊 Please join our required channels to use this bot.\n\nJoin both channels and then try again.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Update Channel ⚙️", url=f"https://t.me/{FORCE_SUB1}")],
                        [InlineKeyboardButton("Movie Group 💿", url=f"https://t.me/{FORCE_SUB2}")],
                        [InlineKeyboardButton("✅ Check Again", callback_data="checksub")]
                    ])
                )
                return
            except Exception as e:
                # Handle generic exceptions
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f"⚠️ Something went wrong.\n\n**Error:** `{e}`",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        try:
            ident, file_id = message.text.split("=")
            filedetails = await get_file_details(file_id)
            
            for files in filedetails:
                title = files.file_name
                size = size_formatter(files.file_size)  # fn() call size_formatter is mb gb converter
                f_caption = files.caption
                
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption = CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption = f_caption
                buttons = [[
                        InlineKeyboardButton('Movie Group🎥', url='telegram.dog/wudixh')
                ]]#, [
                       # InlineKeyboardButton('Kᴜᴛᴛᴜ Bᴏᴛ ™ <Uᴘᴅᴀᴛᴇs>', url='telegram.dog/wudixh13')
                #]]
                
                await bot.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    parse_mode=enums.ParseMode.HTML
                )
        
        except Exception as err:
            await message.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")
    else:
        emo=await message.reply_text("👀")
        await asyncio.sleep(1.1)
        await emo.delete()
        await message.reply_text(
            text=script.START_TXT.format(message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton('🎉 Aᴅᴅ Mᴇ ᴛᴏ ᴜʀ Gʀᴏᴜᴘ 🎉', url=f'http://t.me/im_kuttu2_bot?startgroup=true')
                ], [
                    InlineKeyboardButton('Sᴇᴀʀᴄʜ Hᴇʀᴇ 🔎', switch_inline_query_current_chat=''),
                    InlineKeyboardButton('Gᴏ Group ↗', switch_inline_query='')
                ], [
                    InlineKeyboardButton('🛠️ Hᴇʟᴘ 🛠️', callback_data='help'),
                    InlineKeyboardButton('🛡️ Aʙᴏᴜᴛ 🛡️', callback_data='about')     
                ], [
                    InlineKeyboardButton('📈 Usage', callback_data='usg')
                ]]
            )
        )
    StopPropagation

#callback
@Client.on_callback_query()
async def startquery(client: Client, query: CallbackQuery):
    if query.data=="start":
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton('🎉 Aᴅᴅ Mᴇ ᴛᴏ ᴜʀ Gʀᴏᴜᴘ 🎉', url=f'http://t.me/im_kuttu2_bot?startgroup=true')
            ],[
                InlineKeyboardButton('Sᴇᴀʀᴄʜ Hᴇʀᴇ 🔎', switch_inline_query_current_chat=''),
                InlineKeyboardButton('Gᴏ Iɴʟɪɴᴇ ↗', switch_inline_query='')
            ],[
                InlineKeyboardButton('🛠️ Hᴇʟᴘ 🛠️', callback_data='help'),
                InlineKeyboardButton('🛡️ Aʙᴏᴜᴛ 🛡️', callback_data='about')     
            ],[
                InlineKeyboardButton('📈 Usage', callback_data='usg')
                ]]
            ))
    elif query.data=="help":
        await query.answer("Helping..⚙️..")
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton('Index 📂', callback_data="index")
                ],[
                    InlineKeyboardButton('< Bᴀᴄᴋ', callback_data="start")
                ]]
            ))
    elif query.data == "index":
        # Check if the user is an admin
        if query.from_user.id in ADMINS:
            await query.answer("Admin Use Only <!>")
            await query.message.edit_text(
                text=script.INDEX_TXT,
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton('< Bᴀᴄᴋ', callback_data="help"),
                        InlineKeyboardButton('Home 🏠', callback_data="start")
                    ]]
                ))
        else:
            # Notify the user that they are not authorized
            await query.answer("You are not authorized to access this section.", show_alert=True)
    
    elif query.data=="about":
        await query.answer("About..💀..")
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton('🤵Oᴡɴᴇʀ', callback_data="dev"),
                    InlineKeyboardButton("Sᴛᴀᴛᴜs 💹", callback_data="stats")
                ],[
                    InlineKeyboardButton('< Bᴀᴄᴋ', callback_data="start")
                ]]
            ))
    elif query.data=="stats":
        total = await Media.count_documents()
        users = await db.total_users_count()
        monsize = await db.get_db_size() #db import from util
        free = 536870912 - monsize
        monsize = size_formatter(monsize) #fn()calling size_formatter
        free = size_formatter(free) #fn()calling size_formatter
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, monsize, free),
            reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton('< Bᴀᴄᴋ', callback_data="about")
                    ]]
                ))
    
    elif query.data=="dev":
        await query.answer("Developer..👻..")
        await query.message.edit_text(
            text=script.DEV_TXT,
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton('Cᴏɴᴛᴀᴄᴛ↗', url=f"https://t.me/wudixh13/4")
                ],[
                    InlineKeyboardButton('< Back', callback_data="about"),
                    InlineKeyboardButton('Home 🏠', callback_data="start")
                ]]
            ))
    elif query.data=="usg":
        currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - BOT_START_TIME))
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        await query.answer(#query answer no edit msg
            text=script.USG_TXT.format(currentTime, cpu_usage, ram_usage),
            show_alert="true"
        )
 #CB ENDED               

#@Client.on_message(filters.command('help'))
#async def help(bot, message):
 #   await message.reply_text(
 #       text=script.HELP_TXT.format(message.from_user.mention))

@Client.on_message(filters.command('about'))
async def about(bot, message):
    await message.reply_text(
        text=script.ABOUT_TXT.format(message.from_user.mention))

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('stats')) #use all members
async def total(bot, message):
    """Show total files in database"""
    total = await Media.count_documents()
    users = await db.total_users_count()
    monsize = await db.get_db_size() #db import from util
    free = 536870912 - monsize
    monsize = size_formatter(monsize)
    free = size_formatter(free)
    msg = await message.reply("Aᴄᴄᴇssɪɴɢ Dᴀᴛᴀ Cᴇɴᴛᴇʀ ⏳⏳⏳")
    await asyncio.sleep(1)
    try:
        total = await Media.count_documents()
        await msg.edit_text(
            text=script.STATUS_TXT.format(total, users, monsize, free)
        )
    except Exception as e:
        logger.exception('Failed to check total files')
        await msg.edit(f'Error: {e}')


@Client.on_message(filters.command('log') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if not (reply and reply.media):
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    msg = await message.reply("Pʀᴏᴄᴇssɪɴɢ...⏳", quote=True)

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media:
            media.file_type = file_type
            break
    else:
        await msg.edit('This is not supported file format')
        return

    result = await Media.collection.delete_one({
        'file_name': media.file_name,
        'file_size': media.file_size,
        'file_type': media.file_type,
        'mime_type': media.mime_type
    })

    if result.deleted_count:
        await msg.edit('Fɪʟᴇ ɪs Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ ғʀᴏᴍ DᴀᴛᴀBᴀsᴇ')
    else:
        await msg.edit('Fɪʟᴇ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ DᴀᴛᴀBᴀsᴇ')

#checksun callback 2 channel fsub
@Client.on_callback_query(filters.regex("checksub"))
async def recheck_subscription(bot, query: CallbackQuery):
    try:
        # Check subscription status for both channels
        user1 = await bot.get_chat_member(FORCE_SUB1, query.from_user.id)
        user2 = await bot.get_chat_member(FORCE_SUB2, query.from_user.id)

        if user1.status not in ["member", "administrator", "creator"]:
            await query.answer("❌ You are not joined to the first required channel.", show_alert=True)
            return

        if user2.status not in ["member", "administrator", "creator"]:
            await query.answer("❌ You are not joined to the second required channel.", show_alert=True)
            return

        # If subscribed to both channels
        await query.answer("✅ You have joined both channels!", show_alert=True)
        await query.message.delete()  # Delete the "Check Again" message
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="✅ Thank you for joining the required channels! You can now use the bot."
        )

    except UserNotParticipant:
        await query.answer("❌ You are not joined to both channels. Please join to continue.", show_alert=True)

    except Exception as e:
        await query.answer(f"⚠️ An error occurred: {str(e)}", show_alert=True)

