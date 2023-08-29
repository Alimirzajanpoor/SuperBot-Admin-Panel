import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sqlite3
import json
import base64

chat_data = []


def start(update, context):
    super_user_id = 5218498019
    chat_id = update.message.chat_id

    if update.message.chat_id != super_user_id:
        authdb = sqlite3.connect("pythonsqlite.db")
        c = authdb.cursor()
        sql = "SELECT chat_id FROM user_ids"
        chat_id = update.message.chat_id

        is_verified = False
        try:
            c.execute(sql)
            rows = c.fetchall()
        except:
            bot.send_message(chat_id=chat_id, text="error in database")

        for chat_ids in rows:
            if chat_ids[0] == chat_id:
                bot.send_message(chat_id=chat_id, text="you are verified!.")
                bot.send_message(
                    chat_id=chat_id,
                    text="now u have full accesses so all messages as a user",
                )
                is_verified = True

        if not is_verified:
            bot.send_message(chat_id=chat_id, text="your are not verified")
            bot.send_message(chat_id=chat_id, text="for getting verified use /req")
    else:
        bot.send_message(chat_id=chat_id, text="admin pannel")


def add_ppl(update, context):
    super_user_id = 5218498019
    message = update.message
    print(message)

    if update.message.chat_id == super_user_id:
        authdb = sqlite3.connect("pythonsqlite.db")
        c = authdb.cursor()
        sql = """INSERT INTO user_ids (chat_id,username,firstname) VALUES (?,?,?)"""
        chat_id = update.message.chat_id
        boz = message.text.replace(" ", "")
        boz1 = boz.replace("/add", "")
        user = bot.get_chat(chat_id=boz1)
        first_name = user.first_name
        username = user.username

        try:
            c.execute(sql, (boz1, username, first_name))
            authdb.commit()
            bot.send_message(
                chat_id=chat_id,
                text="user {1} with id of {0} is added ".format(boz1, first_name),
            )
            bot.send_message(
                chat_id=boz1, text="your are verfied ! use /start for contiue"
            )
        except:
            bot.send_message(chat_id=chat_id, text="error in database")


def show_ppl(update, context):
    super_user_id = 5218498019
    message = update.message
    print(message)

    if update.message.chat_id == super_user_id:
        authdb = sqlite3.connect("pythonsqlite.db")
        c = authdb.cursor()
        sql = "SELECT * FROM user_ids"

        try:
            c.execute(sql)
            rows = c.fetchall()
        except:
            bot.send_message(chat_id=super_user_id, text="error in database")

        for chat_ids in rows:
            bot.send_message(
                chat_id=super_user_id,
                text="user_id: {0},\nusername: {1},\nfirstname: {2}".format(
                    chat_ids[0], chat_ids[1], chat_ids[2]
                ),
            )


def kick_ppl(update, context):
    super_user_id = 5218498019
    message = update.message
    print(message)

    if update.message.chat_id == super_user_id:
        authdb = sqlite3.connect("pythonsqlite.db")
        c = authdb.cursor()
        sql = """DELETE from user_ids  where chat_id=?"""
        chat_id = update.message.chat_id
        boz = message.text.replace(" ", "")
        boz1 = boz.replace("/kick", "")

        try:
            c.execute(sql, (boz1,))
            authdb.commit()
            bot.send_message(
                chat_id=chat_id, text="user with id of {0} is deleted ".format(boz1)
            )
            bot.send_message(chat_id=boz1, text="your are kicked from the session")
        except:
            bot.send_message(chat_id=chat_id, text="error in database")


def update_ppl(update, context):
    super_user_id = 5218498019
    message = update.message
    print(message)

    if update.message.chat_id == super_user_id:
        authdb = sqlite3.connect("pythonsqlite.db")
        c = authdb.cursor()
        sql = """UPDATE user_ids SET chat_id=?  where chat_id=?"""
        chat_id = update.message.chat_id
        boz = message.text.replace(" ", "")
        boz1 = boz.replace("/update", "")
        boz2 = boz1.split(",")

        try:
            c.execute(sql, (boz2[1], boz2[0]))
            authdb.commit()
            bot.send_message(chat_id=chat_id, text="user is updated ".format(boz1))
        except:
            bot.send_message(chat_id=chat_id, text="error in database")


def request_verify(update, context):
    super_user_id = 5218498019
    is_verified = False
    authdb = sqlite3.connect("pythonsqlite.db")
    c = authdb.cursor()
    sql = "SELECT chat_id FROM user_ids"
    chat_id = update.message.chat_id
    try:
        c.execute(sql)
        rows = c.fetchall()
    except:
        bot.send_message(chat_id=chat_id, text="error in database")

    chat_id = update.message.chat_id
    username = update.message.from_user
    if update.message.chat_id != super_user_id:
        print(username)
        for chat_ids in rows:
            if chat_ids[0] == chat_id:
                bot.send_message(
                    chat_id=chat_id, text="you are already verfied use /start"
                )
                is_verified = True
                break

        if not is_verified:
            bot.send_message(
                chat_id=super_user_id,
                text="user with user id : {0}\nusername: @{1}\nfirstname: {2}\nhas requested a verify".format(
                    chat_id, username["username"], username["first_name"]
                ),
            )
            bot.send_message(
                chat_id=chat_id, text="your request has been sent to admin"
            )


def message_handler(update, context):
    super_user_id = 5218498019  # replace with the ID of your super user
    authdb = sqlite3.connect("pythonsqlite.db")
    c = authdb.cursor()
    sql = "SELECT chat_id FROM user_ids"
    c.execute(sql)
    rows = c.fetchall()

    # is_verified = False
    if update.message.chat_id == super_user_id:
        message = update.message

        all_chat_ids = rows

        print(all_chat_ids)
        for chat_id in all_chat_ids:
            if message.text:
                try:
                    bot.send_message(chat_id=chat_id[0], text=message.text)
                except:
                    bot.send_message(
                        chat_id=super_user_id,
                        text=f"couldnt send a message for user with id of {chat_id[0]}",
                    )

            elif message.photo:
                photo_file = update.message.photo[-1].get_file()
                # photo_data=photo_file.get("file_path")
                # photo_data = base64.b64encode(photo_file.download_as_bytearray()).decode('utf-8')
                print(photo_file)
                # photo_data = photo_file.download_as_bytearray()
                try:
                    bot.send_photo(chat_id=chat_id[0], photo=photo_file.file_id)
                except:
                    bot.send_message(
                        chat_id=super_user_id,
                        text=f"couldnt send a message for user with id of {chat_id[0]}",
                    )

            elif message.video:
                video_file = message.video.get_file()
                try:
                    bot.sendVideo(chat_id=chat_id[0], video=video_file.file_id)
                except:
                    bot.send_message(
                        chat_id=super_user_id,
                        text=f"couldnt send a message for user with id of {chat_id[0]}",
                    )
            elif message.document:
                document_file = message.document.get_file()
                try:
                    bot.sendDocument(chat_id=chat_id[0], document=document_file.file_id)
                except:
                    bot.send_message(
                        chat_id=super_user_id,
                        text=f"couldnt send a message for user with id of {chat_id[0]}",
                    )

            elif message.sticker:
                sticker_file = message.sticker.get_file()
                try:
                    bot.send_sticker(chat_id=chat_id[0], sticker=sticker_file.file_id)
                except:
                    bot.send_message(
                        chat_id=super_user_id,
                        text=f"couldnt send a message for user with id of {chat_id[0]}",
                    )

            elif message.animation:
                animation_file = message.animation.get_file()
                bot.send_animation(chat_id=chat_id[0], animation=animation_file.file_id)
            elif message.audio:
                audio_file = message.audio.get_file()
                try:
                    bot.send_audio(chat_id=chat_id[0], audio=audio_file.file_id)
                except:
                    bot.send_message(
                        chat_id=super_user_id,
                        text=f"couldnt send a message for user with id of {chat_id[0]}",
                    )
            elif message.voice:
                voice_file = message.voice.get_file()
                try:
                    bot.send_voice(chat_id=chat_id[0], voice=voice_file.file_id)
                except:
                    bot.send_message(
                        chat_id=super_user_id,
                        text=f"couldnt send a message for user with id of {chat_id[0]}",
                    )

            else:
                context.bot.send_message(
                    chat_id=chat_id[0],
                    text="Sorry, I can't handle that type of message.",
                )
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="You are not authorized to use this command.",
        )


if __name__ == "__main__":
    bot = telegram.Bot(token="6046265799:AAHfRKRTntXDvjy4dvrx5jsr6AD_z-ieswI")

    updater = telegram.ext.Updater(bot.token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(telegram.ext.CommandHandler("start", start))
    dispatcher.add_handler(telegram.ext.CommandHandler("add", add_ppl))
    dispatcher.add_handler(telegram.ext.CommandHandler("kick", kick_ppl))
    dispatcher.add_handler(telegram.ext.CommandHandler("update", update_ppl))
    dispatcher.add_handler(telegram.ext.CommandHandler("req", request_verify))
    dispatcher.add_handler(telegram.ext.CommandHandler("show", show_ppl))
    dispatcher.add_handler(telegram.ext.MessageHandler(Filters.all, message_handler))

    updater.start_polling()
    updater.idle()
