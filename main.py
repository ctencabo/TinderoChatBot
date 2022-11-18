from constants import Api as api
from telegram import \
    KeyboardButton, \
    ReplyKeyboardMarkup,\
    ReplyKeyboardRemove,\
    InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler

TOKEN = api.TELEGRAM_BOT_API
ZOMATO = api.ZOMATO_API

yes_choice = "Yes"
no_choice = "No"

def start(update, context):
    buttons = [[KeyboardButton(yes_choice)], [KeyboardButton(no_choice)]]
    update.message.reply_text("""
    Hello! Welcome to Tindero, your restaurant guide!
    
    Should I start suggesting restaurants?
    """, reply_markup=ReplyKeyboardMarkup(buttons))

def help(update, context):
    update.message.reply_text("""
    The following commands are available:

    /start -> Start Tindero
    /help -> This message
    /suggest -> Tindero will ask a series of questions to help in suggesting a restaurant
    /location -> Tindero will provide your current location for more accurate suggesting of restaurants
    """)

def message_handler(update, context):
    if yes_choice in update.message.text:
        suggest(update, context)
    if no_choice in update.message.text:
        update.message.reply_text("Let us know what we can do to help. Thanks!", reply_markup=ReplyKeyboardRemove(True))

def suggest(update, context):
    buttons = [[InlineKeyboardButton("Test1", callback_data=''), InlineKeyboardButton("Test2", callback_data='')]]
    update.message.reply_text(
        "HELLOOOOO I CAN'T SUGGEST ANYTHING AT THE MOMENT",
        reply_markup=InlineKeyboardMarkup(buttons))

def location_handler(update, context):
    buttons = [[KeyboardButton(yes_choice, request_location=True)], [KeyboardButton(no_choice)]]
    update.message.reply_text("Do you want to share your location?", reply_markup=ReplyKeyboardMarkup(buttons))

def location(update, context):
    user_location = update.message.location
    update.message.reply_text(f'You are currently in LATITUDE: {user_location.latitude} and LONGITUDE: {user_location.longitude}', reply_markup=ReplyKeyboardRemove(True))

updater = Updater(TOKEN, use_context=True)
disp = updater.dispatcher

disp.add_handler(CommandHandler("start", start))
disp.add_handler(CommandHandler("help", help))
disp.add_handler(CommandHandler("suggest", suggest))
disp.add_handler(CommandHandler("location", location_handler))
disp.add_handler(MessageHandler(Filters.location, location))
disp.add_handler(MessageHandler(Filters.text, message_handler))

updater.start_polling()
updater.idle()
