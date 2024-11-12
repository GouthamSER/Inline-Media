import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from info import ADMINS
import os
from utils.database import save_file

logger = logging.getLogger(__name__)
lock = asyncio.Lock()

# Command to set the skip message ID
@Client.on_message(filters.command(['set1']) & filters.user(ADMINS))
async def set_skip(bot, message):
    """Set the starting message ID"""
    try:
        # Get the skip value from the command argument
        skip_value = int(message.text.split(" ", 1)[1])
        os.environ["SKIP"] = str(skip_value)  # Store it in the environment
        await message.reply(f"Starting message ID set to {skip_value}")
    except (IndexError, ValueError):
        await message.reply("Please provide a valid message ID to skip to. Example: /setskip 7000")

@Client.on_message(filters.command(['ind1') & filters.user(ADMINS))
async def index_files(bot, message):
    """Prompt the user to forward the last message of a channel"""

    if lock.locked():
        await message.reply("Wait until the previous process completes.")
        return
    
    await message.reply(
        "Please forward the last message of the channel you want to index.\n\n"
        "The bot can index messages from public channels or private channels where it is an admin."
    )
   # break
#else:
    #continue

    # Define a listener to capture the forwarded message
    async def capture_forwarded_message(client, forwarded_message):
        nonlocal lock  # Ensure we're accessing the outer lock

        try:
            last_msg_id = forwarded_message.forward_from_message_id
            chat_id = (
                forwarded_message.forward_from_chat.username
                if forwarded_message.forward_from_chat.username
                else forwarded_message.forward_from_chat.id
            )
            await bot.get_messages(chat_id, last_msg_id)
        except Exception as e:
            await forwarded_message.reply(
                f"This is an invalid message. Either the channel is private and the bot is not an admin, or the message was forwarded incorrectly.\n"
                f"Error: <code>{e}</code>"
            )
            return

        msg = await message.reply("Processing...⏳")
        total_files = 0
        async with lock:
            try:
                total = last_msg_id + 1
                current = int(os.environ.get("SKIP", 2))
                nyav = 0
                while current < total:
                    try:
                        fetched_message = await bot.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        continue
                    except Exception as e:
                        logger.exception(e)
                        break

                    media = None
                    for file_type in ("document", "video", "audio"):
                        media = getattr(fetched_message, file_type, None)
                        if media:
                            media.file_type = file_type
                            media.caption = fetched_message.caption
                            try:
                                await save_file(media)
                                total_files += 1
                            except Exception as e:
                                logger.exception(e)
                            break

                    current += 1
                    nyav += 1
                    if nyav == 20:
                        await msg.edit(f"Total messages fetched: {current}\nTotal messages saved: {total_files}")
                        nyav = 0

                await msg.edit(f"Total {total_files} files saved to the database!")
            except Exception as e:
                logger.exception(e)
                await msg.edit(f"Error: {e}")
            finally:
                # Remove the listener after use
                bot.remove_handler(capture_forwarded_message, group=1)

    # Add the listener for the forwarded message
    bot.add_handler(filters.user(message.from_user.id) & filters.forwarded, capture_forwarded_message, group=1)
