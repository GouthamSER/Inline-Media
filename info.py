import re
from os import environ
from Script import script
from time import time

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
USER_SESSION = environ.get('USER_SESSION', 'User_Bot')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']
USERBOT_STRING_SESSION = environ.get('USERBOT_STRING_SESSION')
BOT_USERNAME = environ.get('BOT_USERNAME', '')

# Bot settings
BOT_START_TIME = time()
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
PORT = environ.get("PORT", "8000")
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', '📂 <em>File Name</em>: <code>Kᴜᴛᴛᴜ|{file_name}</code> <br><br>🖇 <em>File Size</em>: <code>{file_size}</code> <br><br>❤️‍🔥 <i>Movie Requests</i> - ||@wudixh|| '))

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ['ADMINS'].split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ['CHANNELS'].split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_GROUPS = [int(admin) for admin in environ.get("AUTH_GROUPS", "").split()]
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel
PICS=environ.get('PICS', 'PhoTO Link here')
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "")
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CUSTOM_FILE_CAPTION}")

# MongoDB information
DATABASE_URI = environ['DATABASE_URI']
DATABASE_NAME = environ['DATABASE_NAME']
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# INLINE USAGES
SHARE_BUTTON_TEXT = 'Checkout {username} for searching files'
INVITE_MSG = environ.get('INVITE_MSG', 'Please join @.... to use this bot')
