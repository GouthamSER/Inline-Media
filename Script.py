class script(object):
  START_TXT=""" <b><i>Hey {}, I'm Media Search bot & Auto Filter Bot</i></b>
  
<blockquote>Here you can search files in inline mode & Auto Filter. Just press following buttons and start searching.</blockquote>
"""
  HELP_TXT="""Hᴇʏ {}
__Tʜɪs ɪs ᴛʜᴇ Hᴇʟᴘ Txᴛ..__

/alive - check alive bot
/help - help
/start - start the bot
/movie - movie req format
/series - series req format

<blockquote>📯𝗗𝗜𝗦𝗖𝗟𝗔𝗜𝗠𝗘𝗥 :
A𝗅𝗅 𝗍𝗁𝖾 𝖿𝗂𝗅𝖾𝗌 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍 𝖺𝗋𝖾 𝖿𝗋𝖾𝖾𝗅𝗒 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝗈𝗇 𝗍𝗁𝖾 𝗂𝗇𝗍𝖾𝗋𝗇𝖾𝗍 𝗈𝗋 𝗉𝗈𝗌𝗍𝖾𝖽 𝖻𝗒 𝗌𝗈𝗆𝖾𝖻𝗈𝖽𝗒 𝖾𝗅𝗌𝖾.
𝖳𝗁𝗂𝗌 𝖻𝗈𝗍 𝗂𝗌 𝗂𝗇𝖽𝖾𝗑𝗂𝗇𝗀 𝖿𝗂𝗅𝖾𝗌 𝗐𝗁𝗂𝖼𝗁 𝖺𝗋𝖾 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝗎𝗉𝗅𝗈𝖺𝖽𝖾𝖽 𝗈𝗇 𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖿𝗈𝗋 𝖾𝖺𝗌𝖾 𝗈𝖿 𝗌𝖾𝖺𝗋𝖼𝗁𝗂𝗇𝗀,
𝖶𝖾 𝗋𝖾𝗌𝗉𝖾𝖼𝗍 𝖺𝗅𝗅 𝗍𝗁𝖾 𝖼𝗈𝗉𝗒𝗋𝗂𝗀𝗁𝗍 𝗅𝖺𝗐𝗌 𝖺𝗇𝖽 𝗐𝗈𝗋𝗄𝗌 𝗂𝗇 𝖼𝗈𝗆𝗉𝗅𝗂𝖺𝗇𝖼𝖾 𝗐𝗂𝗍𝗁 𝖣𝖬𝖢𝖠 𝖺𝗇𝖽 𝖤𝖴𝖢𝖣.
𝖨𝖿 𝖺𝗇𝗒𝗍𝗁𝗂𝗇𝗀 𝗂𝗌 𝖺𝗀𝖺𝗂𝗇𝗌𝗍 𝗅𝖺𝗐 𝗉𝗅𝖾𝖺𝗌𝖾 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 𝗎𝗌 𝗌𝗈 𝗍𝗁𝖺𝗍 𝗂𝗍 𝖼𝖺𝗇 𝖻𝖾 𝗋𝖾𝗆𝗈𝗏𝖾𝖽 𝖺𝗌𝖺𝗉.</blockquote>

"""
  ABOUT_TXT=""" Hey {} ,
✯ Mʏ Nᴀᴍᴇ: Kᴜᴛᴛᴜ Bᴏᴛ 2 ™
✯ Cʀᴇᴀᴛᴏʀ: Gᴏᴜᴛʜᴀᴍ Sᴇʀ
✯ Lɪʙʀᴀʀʏ: Pʏʀᴏɢʀᴀᴍ 2
✯ Lᴀɴɢᴜᴀɢᴇ: Pʏᴛʜᴏɴ 3
✯ DᴀᴛᴀBᴀsᴇ: MᴏɴɢᴏDB
✯ Bᴏᴛ Sᴇʀᴠᴇʀ: Koyeb"""

  INDEX_TXT=""" **__Hi__**
  /index - index the file
  /stopindex - stopindex via cmnd
  /setskip - skip the msg
  """

  STATUS_TXT="""📁 Tᴏᴛᴀʟ Fɪʟᴇs: {}
🤵Usᴇʀs : <code>{}</code>
📜Usɪɴɢ Sᴛᴏʀᴀɢᴇ : <code>{}/512 MB</code>
♻ Fʀᴇᴇ Sᴛᴏʀᴀɢᴇ : <code>{}/512 MB</code>
""" # [ "{}" - size_formater fn() import from inline ]
  
  DEV_TXT="""Iɴғᴏʀᴍᴀᴛɪᴏɴ Aʙᴏᴜᴛ Oᴡɴᴇʀ!!!
Cʟɪᴄᴋ ᴛʜᴇ Bᴜᴛᴛᴏɴ Tᴏ Sᴇᴇ✔"""

  LOGP_TXT="""Kᴜᴛᴛᴜ Bᴏᴛ 2
#NewUser
ID - <code>{}</code>
Name - {}
"""
  RESTART_TXT = """
<b>𝖡𝗈𝗍 𝖱𝖾𝗌𝗍𝖺𝗋𝗍𝖾𝖽 !</b>
Kuttu Bot 2 :)
📅 𝖣𝖺𝗍𝖾 : <code>{}</code>
⏰ 𝖳𝗂𝗆𝖾 : <code>{}</code>
🌐 𝖳𝗂𝗆𝖾𝗓𝗈𝗇𝖾 : <code>Asia/Kolkata</code>
🛠️ 𝖡𝗎𝗂𝗅𝖽 𝖲𝗍𝖺𝗍𝗎𝗌 : <code>𝗏2 [ 𝖲𝗍able 😁 ]</code></b>"""

  RESTART24_TXT = """
<b><u>𝖡𝗈𝗍 𝖱𝖾𝗌𝗍𝖺𝗋𝗍𝖾𝖽 24 hrs Completed✅</u></b>"""
    
  CUSTOM_FILE_CAPTION = """📂 <em>File Name</em>: <code>Kᴜᴛᴛᴜ 2|{file_name}</code>
🖇 <em>File Size</em>: <code>{file_size}</code>
------------------------     ----------
❤️‍🔥 <i>Movie Requests</i> - <a href="t.me/wudixh">Click Me 👈</a> 
------------------------     ----------"""  

  USG_TXT="""⚙️ 𝖡𝗈𝗍 𝖲𝗍𝖺𝗍𝗎𝗌
  
🕔 𝖴𝗉𝗍𝗂𝗆𝖾: {}
🛠 𝖢𝖯𝖴 𝖴𝗌𝖺𝗀𝖾: {}%
🗜 𝖱𝖠𝖬 𝖴𝗌𝖺𝗀𝖾: {}%"""

  NO_RES="""sᴏʀʀʏ ɴᴏ ꜰɪʟᴇs ᴡᴇʀᴇ ꜰᴏᴜɴᴅ ꜰᴏʀ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛ {} 😕

ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴘᴇʟʟɪɴɢ ɪɴ ɢᴏᴏɢʟᴇ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ 😃

ᴍᴏᴠɪᴇ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ 👇

ᴇxᴀᴍᴘʟᴇ : Uncharted or Uncharted 2022 or Uncharted En

ꜱᴇʀɪᴇꜱ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ 👇

ᴇxᴀᴍᴘʟᴇ : Loki S01 or Loki S01E04 or Lucifer S03E24

🚯 ᴅᴏɴᴛ ᴜꜱᴇ ➠ ':(!,./) """
