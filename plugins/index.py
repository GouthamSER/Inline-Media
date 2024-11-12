import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from info import ADMINS
import os
from utils.database import save_file
import pyromod.listen

logger = logging.getLogger(__name__)
lock = asyncio.Lock()

# Command to set the skip message ID
@Client.on_message(filters.command(['setskip']) & filters.user(ADMINS))
async def set_skip(bot, message):
    """Set the starting message ID"""
    try:
        # Get the skip value from the command argument
        skip_value = int(message.text.split(" ", 1)[1])
        os.environ["SKIP"] = str(skip_value)  # Store it in the environment
        await message.reply(f"Starting message ID set to {skip_value}")
    except (IndexError, ValueError):
        await message.reply("Please provide a valid message ID to skip to. Example: /setskip 7000")

@Client.on_message(filters.command(['index', 'indexfiles']) & filters.user(ADMINS))
async def index_files(bot, message):
    """Save channel or group files"""
    if lock.locked():
        await message.reply("Wait until the previous process completes.")
    else:
        while True:
            last_msg = await bot.ask(
                text="Forward me the last message of a channel which I should save to my database.\n\n"
                     "You can forward posts from any public channel, but for private channels, the bot should be an admin in the channel.\n\n"
                     "Make sure to forward with quotes (Not as a copy)",
                chat_id=message.from_user.id
            )
            try:
                last_msg_id = last_msg.forward_from_message_id
                if last_msg.forward_from_chat.username:
                    chat_id = last_msg.forward_from_chat.username
                else:
                    chat_id = last_msg.forward_from_chat.id
                await bot.get_messages(chat_id, last_msg_id)
                break
            except Exception as e:
                await last_msg.reply_text(
                    f"This is an invalid message. Either the channel is private and the bot is not an admin, or you forwarded the message as copy.\n"
                    f"Error: <code>{e}</code>"
                )
                break  #forward file is txt stop index
            else: 
                continue #continue is file 

        msg = await message.reply("Processing...⏳")
        total_files = 0
        async with lock:
            try:
                total = last_msg_id + 1
                # Use the skip value from environment or default to 2 if not set
                current = int(os.environ.get("SKIP", 2))
                nyav = 0
                while True:
                    try:
                        message = await bot.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                        message = await bot.get_messages(chat_id, current, replies=0)
                    except Exception as e:
                        print(e)
                        pass
                    try:
                        for file_type in ("document", "video", "audio"):
                            media = getattr(message, file_type, None)
                            if media is not None:
                                break
                            else:
                                continue
                        media.file_type = file_type
                        media.caption = message.caption
                        await save_file(media)
                        total_files += 1
                    except Exception as e:
                        print(e)
                        pass
                    current += 1
                    nyav += 1
                    if nyav == 20:
                        await msg.edit(f"Total messages fetched: {current}\nTotal messages saved: {total_files}")
                        nyav -= 20
                    if current == total:
                        break
                    else:
                        continue
            except Exception as e:
                logger.exception(e)
                await msg.edit(f"Error: {e}")
            else:
                await msg.edit(f"Total {total_files} files saved to the database!")
