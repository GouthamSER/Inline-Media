class script(object):
  START_TXT="""**Hey {}, I'm Media Search bot & Auto Filter Bot**
  
Here you can search files in inline mode & Auto FIlter. Just press following buttons and start searching.
"""
  HELP_TXT="""Hᴇʏ {}
Tʜɪs ɪs ᴛʜᴇ Hᴇʟᴘ Txᴛ..
/start - start the bot
/index - to index the files (admin)
/stats - to see how many files are in db
/log - to see the errors
/channel - to see how many channels connected
/usage - to see how the bot use cpu & mem
"""
  ABOUT_TXT=""" Hey {} ,
✯ Mʏ Nᴀᴍᴇ: Kᴜᴛᴛᴜ Bᴏᴛ 2 ™
✯ Cʀᴇᴀᴛᴏʀ: Gᴏᴜᴛʜᴀᴍ Sᴇʀ
✯ Lɪʙʀᴀʀʏ: Pʏʀᴏɢʀᴀᴍ
✯ Lᴀɴɢᴜᴀɢᴇ: Pʏᴛʜᴏɴ 3
✯ DᴀᴛᴀBᴀsᴇ: MᴏɴɢᴏDB
✯ Bᴏᴛ Sᴇʀᴠᴇʀ: Koyeb"""

  STATUS_TXT="""📁 Tᴏᴛᴀʟ Fɪʟᴇs: {}
🤵Usᴇʀs: <code>{}</code>
📜 Usɪɴɢ Sᴛᴏʀᴀɢᴇ:<code>{}/512 MB</code>
♻ Fʀᴇᴇ Sᴛᴏʀᴀɢᴇ:<code>{}/512 MB</code>
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
❤️‍🔥 <i>Movie Requests</i> - <a href="t.me/wudixh">Click Me 👈</a> """
