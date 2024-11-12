import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.WARNING)

# for prevent stoping the bot after 1 week
logging.getLogger("asyncio").setLevel(logging.CRITICAL -1)

# peer id invaild fixxx
from pyrogram import utils as pyroutils
pyroutils.MIN_CHAT_ID = -999999999999
pyroutils.MIN_CHANNEL_ID = -100999999999999

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from utils import Media
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL
from aiohttp import web as webserver
from os import environ
from utils.dbstatus import db
from plugins.webcode import bot_run
from Script import script #for restarttxt
from datetime import date, datetime, timedelta
import asyncio
import pytz
import pyromod.listen

PORT_CODE = environ.get("PORT", "8080")

class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        self.username = '@' + me.username
        print(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        print("Recoded By Goutham SER </>")

        tz = pytz.timezone('Asia/Kolkata')
        today = date.today()
        now = datetime.now(tz)
        time = now.strftime("%H:%M:%S %p")
        await self.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
        
        client = webserver.AppRunner(await bot_run())
        await client.setup()
        bind_address = "0.0.0.0"
        await webserver.TCPSite(client, bind_address,
        PORT_CODE).start()
       
        # Start the auto-restart task
        asyncio.create_task(self.auto_restart())

    async def auto_restart(self):
        while True:
            await asyncio.sleep(86400)  # Sleep for 24 hours (86400 seconds)
            logging.info("Restarting bot...")
            await self.send_message(chat_id=LOG_CHANNEL, text=script.RESTART24_TXT.format(today, time))
            await self.stop()
            await self.start() 
     
    #Bot stopped 
    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")


app = Bot()
app.run()
