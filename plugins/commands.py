import re, os, logging, asyncio, random
import time, shutil, psutil, sys #for cb usage alert in startcmnd cb
from utils import Media
from utils.database import get_file_details, is_subscribed #forsutofilter
from pyrogram import Client, filters, StopPropagation, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import *
from info import CHANNELS, ADMINS, INVITE_MSG, LOG_CHANNEL, PICS, CUSTOM_FILE_CAPTION, AUTH_CHANNEL, BOT_START_TIME, BOT_USERNAME
from utils import Media #class 2 are there dbstatus.py and database.py class Database and class Media
from utils.dbstatus import db #db import from dbstatus.py
from Script import script
from plugins.inline import size_formatter
BOT={}
logger = logging.getLogger(__name__)


@Client.on_message(filters.command("start"))
async def start(bot, message):
    """Handles the /start command and prompts for channel subscription if necessary."""

    # Save user to DB
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOGP_TXT.format(message.from_user.id, message.from_user.mention))

    user_cmd = message.text

    # Handle deep-linking for file access
    if user_cmd.startswith("/start file"):
        if AUTH_CHANNEL:
            invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
            try:
                user = await bot.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
                if user.status == "kicked":
                    await bot.send_message(
                        chat_id=message.from_user.id,
                        text="Sorry, you are banned from using this bot.",
                        parse_mode="markdown"
                    )
                    return
            except UserNotParticipant:
                try:
                    _, file_id = message.text.split("_")
                except ValueError:
                    await message.reply("Invalid start command format.")
                    return
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text="**Please join the updates channel to use this bot.**",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("Join Updates Channel", url=invite_link.invite_link)],
                            [InlineKeyboardButton("Try Again", callback_data=f"checksub_{file_id}")]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text="Something went wrong. Please try again later.",
                    parse_mode="markdown"
                )
                return

        try:
            _, file_id = message.text.split("_")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size = files.file_size
                f_caption = files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption = CUSTOM_FILE_CAPTION.format(
                            file_name=title,
                            file_size=size,
                            file_caption=f_caption
                        )
                    except Exception as e:
                        print(e)
                if not f_caption:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [InlineKeyboardButton('Owner', url=f'https://t.me/im_goutham_josh')]
                ]
                au=await bot.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                k = await message.reply_text("**⚠️ 𝖳𝗁𝗂𝗌 𝗆𝖾𝖽𝗂𝖺 𝗐𝗂𝗅𝗅 𝖻𝖾 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝗐𝗂𝗍𝗁𝗂𝗇 5 𝗆𝗂𝗇𝗎𝗍𝖾.**\n__𝖪𝗂𝗇𝖽𝗅𝗒 𝖿𝗈𝗋𝗐𝖺𝗋𝖽 𝗂𝗍 𝗍𝗈 𝗌𝖺𝗏𝖾𝖽 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌.__")
                await asyncio.sleep(300)
                await au.delete()
                await k.edit("<b>Your File/Video is successfully deleted!!!</b>")
        except Exception as err:
            await message.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")

    # Subscription command
    elif len(message.command) > 1 and message.command[1] == 'subscribe':
        invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
        await bot.send_message(
            chat_id=message.from_user.id,
            text="**Please join the updates channel to use this bot.**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Join Updates Channel", url=invite_link.invite_link)]]
            )
        )

    # Default /start response
    else:
        emo = await message.reply_text("👀")
        await asyncio.sleep(1.1)
        await emo.delete()

        await message.reply_text(
            text=script.START_TXT.format(message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('➕ Add Me to Your Group', url=f'https://t.me/{BOT_USERNAME}?startgroup=true')],
                    [
                        InlineKeyboardButton('🔍 Search Here', switch_inline_query_current_chat=''),
                        InlineKeyboardButton('↗ Search Globally', switch_inline_query='')
                    ],
                    [
                        InlineKeyboardButton('🛠 Help', callback_data='help'),
                        InlineKeyboardButton('🛡 About', callback_data='about')
                    ],
                    [InlineKeyboardButton('📈 Usage', callback_data='usg')]
                ]
            )
        )

    # Prevent further handler execution
    raise StopPropagation
#callback
@Client.on_callback_query()
async def startquery(client: Client, query: CallbackQuery):
    if query.data=="start":
        await message.reply_text(
            text=script.START_TXT.format(message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('➕ Add Me to Your Group', url=f'https://t.me/{BOT_USERNAME}?startgroup=true')],
                    [
                        InlineKeyboardButton('🔍 Search Here', switch_inline_query_current_chat=''),
                        InlineKeyboardButton('↗ Search Globally', switch_inline_query='')
                    ],
                    [
                        InlineKeyboardButton('🛠 Help', callback_data='help'),
                        InlineKeyboardButton('🛡 About', callback_data='about')
                    ],
                    [InlineKeyboardButton('📈 Usage', callback_data='usg')]
                ]
            )
        )
    elif query.data == "help":
        await query.answer("Helping... ⚙️")
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('📂 Index', callback_data="index")],
                    [InlineKeyboardButton('⬅ Back', callback_data="start")]
                ]
            )
        )
    elif query.data == "index":
        # Check if the user is an admin
        if query.from_user.id in ADMINS:
            await query.answer("Admin Access ✅")
            await query.message.edit_text(
                text=script.INDEX_TXT,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('⬅ Back', callback_data="help"),
                            InlineKeyboardButton('🏠 Home', callback_data="start")
                        ]
                    ]
                )
            )
        else:
            await query.answer("Access denied. Admins only.", show_alert=True)

    elif query.data == "about":
        await query.answer("About... ℹ️")
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('👤 Owner', callback_data="dev"),
                        InlineKeyboardButton("📊 Stats", callback_data="stats")
                    ],
                    [
                        InlineKeyboardButton('⬅ Back', callback_data="start")
                    ]
                ]
            )
        )

    elif query.data == "stats":
        total = await Media.count_documents()
        users = await db.total_users_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = size_formatter(monsize)
        free = size_formatter(free)

        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, monsize, free),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton('⬅ Back', callback_data="about")]]
            )
        )

    elif query.data == "dev":
        await query.answer("Developer Info 👨‍💻")
        await query.message.edit_text(
            text=script.DEV_TXT,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('📣 Channel', url="https://t.me/wudixh13/4")],
                    [
                        InlineKeyboardButton('⬅ Back', callback_data="about"),
                        InlineKeyboardButton('🏠 Home', callback_data="start")
                    ]
                ]
            )
        )
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
