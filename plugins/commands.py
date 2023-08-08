import os
import logging
import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import UserNotParticipant
from info import START_MSG, CHANNELS, ADMINS, INVITE_MSG, HELP_TXT, ABOUT_TXT
from utils import Media

logger = logging.getLogger(__name__)

FORCE_SUB = "wudixh13"

@Client.on_message(filters.command('start'))
async def start(bot, message):
    """Start command handler"""
    if FORCE_SUB:
        try:
            user = await bot.get_chat_member(FORCE_SUB, message.from_user.id)
            if user.status == "kicked out":
                await message.reply_text("You Are Banned")
                return
        except UserNotParticipant :
            await message.reply_text(
                text="🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 🤭.\n\nDᴏ Yᴏᴜ Wᴀɴᴛ Mᴏᴠɪᴇs? Tʜᴇɴ Jᴏɪɴ Oᴜʀ Mᴀɪɴ Cʜᴀɴɴᴇʟ Aɴᴅ Wᴀᴛᴄʜ ɪᴛ.😂\n Tʜᴇɴ ɢᴏ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴀɴᴅ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ᴍᴏᴠɪᴇ ᴀɢᴀɪɴ ᴀɴᴅ ɢɪᴠᴇ ɪᴛ ᴀ sᴛᴀʀᴛ...!😁",
                reply_markup=InlineKeyboardMarkup( [[
                 InlineKeyboardButton("🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 🤭", url=f"t.me/{FORCE_SUB}")
                 ]]
                 )
            )
            return
        buttonsstart = [[
            InlineKeyboardButton('Sᴇᴀʀᴄʜ Hᴇʀᴇ 🔎', switch_inline_query_current_chat=''),
            InlineKeyboardButton('Gᴏ Iɴʟɪɴᴇ ↗', switch_inline_query=''),
        ]]
        s=await message.reply_sticker("CAACAgUAAxkBAAIuc2OxMvp4oKa3eqg6zBTCZZdtxFV3AAIvAAPhAAEBGxa4Kik7WjyMHgQ")
        await asyncio.sleep(1)
        await s.delete()
        
        await message.reply_photo(
            photo="https://telegra.ph/file/a3da9285babbf059a665d.jpg",
            caption=START_MSG.format(message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton('Sᴇᴀʀᴄʜ Hᴇʀᴇ 🔎', switch_inline_query_current_chat=''),
                InlineKeyboardButton('Gᴏ Iɴʟɪɴᴇ ↗', switch_inline_query='')
            ],[
                InlineKeyboardButton("Hᴇʟᴘ📒", callback_data="help"),
                InlineKeyboardButton("Aʙᴏᴜᴛ😶", callback_data="about")       
                ]]
            ))
#CALLBACK ADDED
@Client.on_callback_query()
async def start(bot, msg):
    
    if msg.data == "start":
        await msg.message.edit_text(
            text=START_MSG.format(message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton('Sᴇᴀʀᴄʜ Hᴇʀᴇ 🔎', switch_inline_query_current_chat=''),
                InlineKeyboardButton('Gᴏ Iɴʟɪɴᴇ ↗', switch_inline_query='')
            ],[
                InlineKeyboardButton("Hᴇʟᴘ📒", callback_data="help"),
                InlineKeyboardButton("Aʙᴏᴜᴛ😶", callback_data="about")       
                ]]
            )

    elif msg.data == "help":
        await msg.message.edit_text(
            text=HELP_TXT.format(message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("Bᴀᴄᴋ👈", callback_data="start")
            ]]
            )
        )
    elif msg.data == "about":
        await msg.message.edit_text(
            text=ABOUT_TXT.format(message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton('Bᴀᴄᴋ👈', callback_data="start")
            ]]
            )
        )
        

@Client.on_message(filters.command('help'))
async def help(bot, message):  
    await message.reply_text(
        text=HELP_TXT.format(message.from_user.mention))

@Client.on_message(filters.command('about'))
async def about(bot, message):
    await message.reply_text(
        text=ABOUT_TXT.format(message.from_user.mention))

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
    msg = await message.reply("Pʀᴏᴄᴇssɪɴɢ...⏳", quote=True)
    try:
        total = await Media.count_documents()
        await msg.edit(f'📁 Sᴀᴠᴇᴅ ғɪʟᴇs: {total}')
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

    msg = await message.reply("Processing...⏳", quote=True)

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
