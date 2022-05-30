import numpy as np
import face_recognition
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton, ChatAction
ADMIN_ID = 00000000
TOKEN = 'Token'


def start_command(update, context):
    # update.message.from_user.id
    update.message.reply_text(text="Rasm kiriting!")


def message_handler(update, context):
    message = update.message.text
    update.message.reply_text(text=f"Sizning xabaringiz '{message}'")


def photo_handler(update, context):
    file = update.message.photo[-1].file_id
    odj = context.bot.get_file(file)
    odj.download('Rasm/suratlar.jpg')
    with open('sample.json') as json_file:
        data = json.load(json_file)

    known_face_encodings = [np.asarray(i['encode']) for i in data]
    known_face_names = [f"{i['dir']} -> {i['name']}" for i in data]

    unknown = face_recognition.load_image_file('/Users/student/PycharmProjects/pythonvenv/Rasm/suratlar.jpg')
    unknown_enc = face_recognition.face_encodings(unknown)[0]

    res = face_recognition.api.compare_faces(known_face_encodings,unknown_enc, tolerance=0.5)
    if True not in res: update.message.reply_text(f"Bu o'quvchi bizda yo'q")
    for idx, r in enumerate(res):
        if r:
            update.message.reply_text(known_face_names[idx])


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))

    updater.start_polling()
    updater.idle()

main()
