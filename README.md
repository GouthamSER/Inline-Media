# [AutoFilter WITH InlineMedia](https://github.com/GouthamSER/Inline-Media)
<p align = "center">
<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Aerial+Code&size=20&pause=1000&width=435&lines=Welcome+To+AutoFilter+with+Inline+Media+Bot;Created+by+GouthamSER;Thiz+bot+Use+Indexes+Files+above+2GB;Simple+features!" alt="Typing SVG" /></a>
</p>

* Index channel or group files for inline search and Auth Groups.
* When you post file on telegram channel or group this bot will save that file in database, so you can search easily in inline mode.
* Supports document, video and audio file formats with caption support.
* Db Space Showing feature some cb added

### Required Variables
* `BOT_TOKEN`: Create a bot using [@BotFather](https://telegram.dog/BotFather), and get the Telegram API token.
* `CUSTOM_FILE_CAPTION`: Environ set [etc-(Filename,Filesize)]
* `AUTH_CHANNEL`: Force SUB to channel
* `AUTH_GROUP`:**Supourt Group AutoFIlter**
* `API_ID`: Get this value from [telegram.org](https://my.telegram.org/apps)
* `API_HASH`: Get this value from [telegram.org](https://my.telegram.org/apps)
* `CHANNELS`: Username or ID of channel or group. Separate multiple IDs by space
* `ADMINS`: Username or ID of Admin. Separate multiple Admins by space
* `DATABASE_URI`: [mongoDB](https://www.mongodb.com) URI. Get this value from [mongoDB](https://www.mongodb.com). For more help watch this [video](https://youtu.be/@im_goutham_josh)
* `DATABASE_NAME`: Name of the database in [mongoDB](https://www.mongodb.com). For more help watch this [video](https://youtu.be/@im_goutham_josh)

### Optional Variables
* `COLLECTION_NAME`: Name of the collections. Defaults to Telegram_files. If you going to use same database, then use different collection name for each bot
* `CACHE_TIME`: The maximum amount of time in seconds that the result of the inline query may be cached on the server
* `USE_CAPTION_FILTER`: Whether bot should use captions to improve search results. (True/False)
* `AUTH_USERS`: Username or ID of users to give access of inline search. Separate multiple users by space. Leave it empty if you don't want to restrict bot usage.
* `AUTH_CHANNEL`: Username or ID of channel. Without subscribing this channel users cannot use bot.
* `START_MSG`: Welcome message for start command.
* `INVITE_MSG`: Auth channel invitation message.

## Admin commands
```
channel - Get basic infomation about channels
stats - Show total of saved files
delete - Delete file from database
index - Index all files from channel or group
log - Get log file
```


## Thanks to [Pyrogram](https://github.com/pyrogram/pyrogram)
## Thanks to [Mahesh](https://github.com/Mahesh0253)
## Thanks to [Me](github.com/GouthamSER)

## Support [Channel](t.me/wudixh13)

## License
Code released under [The GNU v3 General Public License](LICENSE).

