import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from info import ADMINS
import os
from utils.database import save_file
import pyromod.listen

logger = logging.getLogger(__name__)
lock = asyncio.Lock()


@Client.on_message(filters.command(['index', 'indexfiles']) & filters.user(ADMINS))
async def ask_index_confirmation(bot, message):
    """Ask for confirmation before starting indexing"""
    confirmation_buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("Yes", callback_data="confirm_index_yes"),
            InlineKeyboardButton("No", callback_data="confirm_index_no")
        ]]
    )
    await message.reply(
        "Would you like to start indexing files?",
        reply_markup=confirmation_buttons
    )


@Client.on_callback_query(filters.regex("confirm_index"))
async def on_confirm_index_callback(bot: Client, callback_query: CallbackQuery):
    """Handle callback for indexing confirmation"""
    if callback_query.data == "confirm_index_yes":
        await callback_query.message.delete()
        await index_files(bot, callback_query.message)
    elif callback_query.data == "confirm_index_no":
        await callback_query.message.edit("Indexing canceled.")


async def index_files(bot, message):
    """Save channel or group files"""
    if lock.locked():
        await message.reply('Wait until previous process completes.')
        return

    while True:
        last_msg = await bot.ask(
            text="Forward the last message from a channel to save it to the database.\n\n"
                 "Forward posts from any public channel, but if it's private, ensure the bot is an admin in the channel.\n\n"
                 "Make sure to forward with quotes (not as a copy).",
            chat_id=message.from_user.id
        )
        try:
            last_msg_id = last_msg.forward_from_message_id
            chat_id = last_msg.forward_from_chat.username or last_msg.forward_from_chat.id
            await bot.get_messages(chat_id, last_msg_id)
            break
        except Exception as e:
            await last_msg.reply_text(
                f"Invalid message: Either the channel is private and the bot is not an admin, "
                f"or the message was forwarded as a copy.\nError: <code>{e}</code>"
            )
            continue

    msg = await message.reply('Processing...⏳')
    total_files = 0

    async with lock:
        try:
            total = last_msg_id + 1
            current = int(os.environ.get("SKIP", 2))
            nyav = 0
            while True:
                try:
                    message = await bot.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    message = await bot.get_messages(chat_id, current, replies=0)
                except Exception as e:
                    logger.exception(e)
                    continue

                try:
                    for file_type in ("document", "video", "audio"):
                        media = getattr(message, file_type, None)
                        if media is not None:
                            break
                    if media:
                        media.file_type = file_type
                        media.caption = message.caption
                        await save_file(media)
                        total_files += 1
                except Exception as e:
                    logger.exception(e)
                    continue

                current += 1
                nyav += 1
                if nyav == 20:
                    await msg.edit(f"Total messages fetched: {current}\nTotal messages saved: {total_files}")
                    nyav = 0
                if current == total:
                    break

        except Exception as e:
            logger.exception(e)
            await msg.edit(f'Error: {e}')
        else:
            await msg.edit(f'Total {total_files} files saved to database!')
