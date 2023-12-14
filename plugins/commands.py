import os
import logging
import asyncio
import random
from utils import Media
from utils.database import get_file_details #forsutofilter
from pyrogram import Client, filters, StopPropagation, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import UserNotParticipant
from info import CHANNELS, ADMINS, INVITE_MSG, LOG_CHANNEL, PICS, CUSTOM_FILE_CAPTION
from utils import Media #class 2 are there dbstatus.py and database.py class Database and class Media
from utils.dbstatus import db #db import from dbstatus.py
from Script import script
from plugins.inline import size_formatter

logger = logging.getLogger(__name__)

FORCE_SUB = "@wudixh"

@Client.on_message(filters.command("start"))
async def start(bot, message):
    #USER SAVING IN DB
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOGP_TXT.format(message.from_user.id, message.from_user.mention))
    user_cmnd = message.text
    if user_cmnd.startswith("/start kuttu"):
        
        if AUTH_CHANNEL:
            try:
                user = await bot.get_chat_member(int(AUTH_CHANNEL)), message.from_user.id)
                if user.status == "kicked":
                    await bot.send_message(
                        chat_id=message.from_user.id,
                        text="Sorry Sir, You are Banned to use me😢.",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant :
                ident, file_id = message.text.split("./.")
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text="**Please Join My Updates Channel to use this Bot!**",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("📢 Join Updates Channel 📢", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton("🔄 Try Again", callback_data=f"checksub#{file_id}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text="Something went Wrong.❌",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        try:
            ident, file_id = message.text.split("./.")
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
                buttons = [[
                        InlineKeyboardButton('>Movie Group<', url='telegram.dog/wudixh')
                    ]]
                
                await bot.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    parse_mode=enums.ParseMode.HTML
                    )
        
        except Exception as err:
            await message.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")
    
    elif len(message.command) > 1 and message.command[1] == 'subscribe':
        invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
        await bot.send_message(
            chat_id=message.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📢 Join Updates Channel 📢", url=invite_link.invite_link)
                ]]
                ))
    else:
        await message.reply_text(
            text=script.START_TXT.format(message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton('Sᴇᴀʀᴄʜ Hᴇʀᴇ 🔎', switch_inline_query_current_chat=''),
                InlineKeyboardButton('Gᴏ Group ↗', switch_inline_query='')
            ],[
                InlineKeyboardButton("Hᴇʟᴘ📒", callback_data="help"),
                InlineKeyboardButton("Aʙᴏᴜᴛ😶", callback_data="about")       
                ]]
            ))
        StopPropagation
#callback
@Client.on_callback_query()
async def startmes(bot:Client, mes:CallbackQuery):
    if mes.data=="start":
        await mes.message.edit(
            text=script.START_TXT.format(mes.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton('Sᴇᴀʀᴄʜ Hᴇʀᴇ 🔎', switch_inline_query_current_chat=''),
                InlineKeyboardButton('Gᴏ Iɴʟɪɴᴇ ↗', switch_inline_query='')
            ],[
                InlineKeyboardButton("Hᴇʟᴘ📒", callback_data="help"),
                InlineKeyboardButton("Aʙᴏᴜᴛ😶", callback_data="about")       
                ]]
            ))
    elif mes.data=="help":
        await mes.answer("Pʀᴏᴄᴇssɪɴɢ...⏳")
        await mes.message.edit(
            text=script.HELP_TXT.format(mes.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton('🔙Bᴀᴄᴋ', callback_data="start")
                ]]
            ))
    elif mes.data=="about":
        await mes.answer("Pʀᴏᴄᴇssɪɴɢ...⏳")
        await mes.message.edit(
            text=script.ABOUT_TXT.format(mes.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton('🔙Bᴀᴄᴋ', callback_data="start"),
                    InlineKeyboardButton("Sᴛᴀᴛᴜs💹", callback_data="stats")
                ],[
                    InlineKeyboardButton('🤵Oᴡɴᴇʀ', callback_data="dev")
                ]]
            ))
    elif mes.data=="stats":
        total = await Media.count_documents()
        users = await db.total_users_count()
        monsize = await db.get_db_size() #db import from util
        free = 536870912 - monsize
        monsize = size_formatter(monsize) #fn()calling size_formatter
        free = size_formatter(free) #fn()calling size_formatter
        msg = await mes.message.reply("**𝐴𝑐𝑐𝑒𝑠𝑠𝑖𝑛𝑔 𝑆𝑡𝑎𝑡𝑢𝑠 𝐷𝑎𝑡𝑎**")
        await msg.edit_text(
            text=script.STATUS_TXT.format(total, users, monsize, free),
            reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton('🔙Bᴀᴄᴋ', callback_data="about")
                    ]]
                ))
    
    elif mes.data=="dev":
        await mes.answer("Pʀᴏᴄᴇssɪɴɢ...⏳")
        await mes.message.edit(
            text=script.DEV_TXT,
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton('🔙Bᴀᴄᴋ', callback_data="about")
                ],[
                    InlineKeyboardButton('Cᴏɴᴛᴀᴄᴛ↗', url=f"https://telegram.dog/wudixh13/4")
                ]]
            ))
 #CB ENDED               

@Client.on_message(filters.command('help'))
async def help(bot, message):  
    await message.reply_text(
        text=script.HELP_TXT.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton('🔙Bᴀᴄᴋ', callback_data="start")
                ]]
            ))

@Client.on_message(filters.command('about'))
async def about(bot, message):
    await message.reply_text(
        text=script.ABOUT_TXT.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton('🔙Bᴀᴄᴋ', callback_data="start")
                ]]
            ))

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
    msg = await message.reply("**𝐴𝑐𝑐𝑒𝑠𝑠𝑖𝑛𝑔 𝑆𝑡𝑎𝑡𝑢𝑠 𝐷𝑎𝑡𝑎**")
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
        await msg.edit('File is successfully deleted from database')
    else:
        await msg.edit('File not found in database')
