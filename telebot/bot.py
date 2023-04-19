from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler
from telegram.ext.filters import Filters

from telegram import Update
from telegram import ReplyKeyboardMarkup

from telegram.chataction import ChatAction

import requests
from bs4 import BeautifulSoup

base_url = "youre url"
token = "youre token"
messages = {
    "msg_start": "سلام {} {} \n به ربات mohammad خوش آمدید.",
    "msg_sum": "مجموع اعداد به صورت زیر است: \n {}",
    "msg_main_handler": "منو اصلی:",
    "msg_select_language": "زبان موردنظر خو را انتخاب کنید:",
"msg_contact": "ارتباط با ما: \n کانال تلگرامی: \n وبسایت",

    "btn_courses": "دوره های موجود در سایت",
    "btn_articles": "مقالات",
    "btn_help": "راهنمایی",
    "btn_contact_us": "تماس با ما",
    "btn_python": "پایتون",
    "btn_kotlin": "کاتلین",
    "btn_return": "بازگشت"
}


def get_data(lang):
    URL = base_url + lang
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    result = soup.find_all("div", attrs={"class": "col-lg-4 col-md-6 col-sm-6 col-xs-6 term-box"})
    courses = [item.h2.a.text for item in result]
    time = [item.span.text for item in result]
    costs = [item.label.text for item in result]
    return courses, time, costs


def start_handler(update: Update, context: CallbackContext):
    # when a user start the bot.

    # import pdb; pdb.set_trace()
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(text=messages["msg_start"].format(first_name, last_name))
    main_menu_handler(update, context)


def sum_handler(update: Update, context: CallbackContext):
    # return summation of input numbers.

    # import pdb; pdb.set_trace()
    chat_id = update.message.chat_id
    numbers = context.args
    result = sum(int(i) for i in numbers)
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(text=messages["msg_sum"].format(result))


def main_menu_handler(update: Update, context: CallbackContext):
    # import pdb; pdb.set_trace()
    buttons = [
        [messages["btn_articles"], messages["btn_courses"]],
        [messages["btn_contact_us"]],
        [messages["btn_help"]]
    ]
    update.message.reply_text(
        text=messages["msg_main_handler"],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def languages_handler(update: Update, context: CallbackContext):
    buttons = [
        [messages["btn_python"], messages["btn_kotlin"]],
        [messages["btn_return"]]
    ]
    update.message.reply_text(
        text=messages["msg_select_language"],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def python_handler(update: Update, context: CallbackContext):
    text = ""
    courses, time, costs = get_data("python")
    for i in range(len(costs)):
        text += courses[i] + time[i] + costs[i] + "\n \n"
    update.message.reply_text(text=text)


def contact_handler(update: Update, context: CallbackContext):
    update.message.reply_text(text=messages["msg_contact"])


def return_handler(update: Update, context: CallbackContext):

    main_menu_handler(update, context)


def send_music_handler(update: Update, context: CallbackContext):
    # import pdb; pdb.set_trace()
    chat_id = update.message.chat_id
    with open("your music", "rb") as music:
        context.bot.send_chat_action(chat_id, ChatAction.UPLOAD_AUDIO)
        context.bot.sendAudio(chat_id, music, caption="آهنگ مورد علاقه من", duration=600, disable_notification=True, timeout=5000)


def send_photo_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    with open("your photo", "rb") as img:
        context.bot.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)
        context.bot.sendPhoto(chat_id, img, caption="لوگوی تاپلرن")


def send_doc_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    with open("your doc", "rb") as doc:
        context.bot.send_chat_action(chat_id, ChatAction.UPLOAD_DOCUMENT)
        context.bot.sendDocument(chat_id, doc, caption="فایل")


def main():
    updater = Updater(token, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("sum", sum_handler, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler("music", send_music_handler))
    updater.dispatcher.add_handler(CommandHandler("photo", send_photo_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["btn_courses"]), languages_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["btn_return"]), return_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["btn_python"]), python_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["btn_contact_us"]), contact_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["btn_articles"]), send_doc_handler))

    updater.start_polling()

    updater.idle()


main()
