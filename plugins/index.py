import logging
import asyncio
import re
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from info import ADMINS
import os
import pyromod.listen
from utils import save_file
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
logger = logging.getLogger(__name__)
lock = asyncio.Lock()

# Set default skip value, can be updated by /setskip command
skip_messages = int(os.environ.get("SKIP", 2))

@Client.on_message(filters.command(['setskip']) & filters.user(ADMINS))
async def set_skip_command(bot, message):
    """Set the number of messages to skip"""
    global skip_messages
    try:
        skip_value = int(message.text.split()[1])
        skip_messages = skip_value
        await message.reply(f"Skip value set to {skip_value}.")
    except (IndexError, ValueError):
        await message.reply("Please provide a valid skip value. Usage: /setskip <number>")

@Client.on_message(filters.command(['add']) & filters.user(ADMINS))
async def index_files(bot, message):
    """Save channel or group files""" 
    
    if lock.locked():
        await message.reply('Wait until previous process completes.')
    else:
        confirmation_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Yes", callback_data="confirm_yes"), InlineKeyboardButton("No", callback_data="confirm_no")]
        ])
        
        await message.reply("Would you like to start indexing files?", reply_markup=confirmation_buttons)

@Client.on_callback_query(filters.regex("confirm_"))
async def confirm_index_files(bot, query):
    if query.data == "confirm_no":
        await query.message.edit_text("Indexing process cancelled.")
        return

    await query.message.edit_text("Forward the last message of a channel which I should save to my database.\n\nYou can forward posts from any public channel, but for private channels, the bot should be an admin.")
    
    last_msg = await bot.ask(chat_id=query.from_user.id, text="Please forward with quotes (Not as a copy)")
    
    while True:
        try:
            last_msg_id = last_msg.forward_from_message_id
            chat_id = last_msg.forward_from_chat.username if last_msg.forward_from_chat.username else last_msg.forward_from_chat.id
            await bot.get_messages(chat_id, last_msg_id)
            break
        except Exception as e:
            await last_msg.reply_text(f"This is an invalid message or there was an error.\nError: <code>{e}</code>")
            return
    
    msg = await query.message.reply('Processing...⏳')
    total_files = 0
    current = skip_messages
    nyav = 0
    
    async with lock:
        try:
            total = last_msg_id + 1
            while current < total:
                try:
                    message = await bot.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    continue
                except Exception as e:
                    logger.exception(e)
                    break

                media = None
                for file_type in ("document", "video", "audio"):
                    media = getattr(message, file_type, None)
                    if media:
                        media.file_type = file_type
                        media.caption = message.caption
                        try:
                            await save_file(media)
                            total_files += 1
                        except Exception as e:
                            logger.exception(e)
                        break

                current += 1
                nyav += 1
                if nyav >= 20:
                    await msg.edit(f"Total messages fetched: {current}\nTotal messages saved: {total_files}")
                    nyav = 0

            await msg.edit(f'Total {total_files} files saved to database!')
        except Exception as e:
            logger.exception(e)
            await msg.edit(f'Error: {e}')
