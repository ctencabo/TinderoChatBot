from constants import Api as api
from api_requests import Requests as api_request
from telegram import \
    KeyboardButton, \
    ReplyKeyboardMarkup,\
    ReplyKeyboardRemove
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler

TOKEN = api.TELEGRAM_BOT_API

yes_choice = "Yes"
no_choice = "No"
user_location = ""

def start(update, context):
    buttons = [[KeyboardButton(yes_choice)], [KeyboardButton(no_choice)]]
    update.message.reply_text("""
    Hello! Welcome to Tindero, your restaurant guide!

    Should I start suggesting restaurants?
    """, reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))

def help(update, context):
    update.message.reply_text("""
    The following commands are available:

    /start -> Start Tindero
    /help -> This message
    /suggest -> Tindero will ask a series of questions to help in suggesting a restaurant
    /location -> Tindero will provide your current location and get the list of restaurants around you
    """)

def message_handler(update, context):
    if yes_choice in update.message.text:
        location(update, context)
    if no_choice in update.message.text:
        update.message.reply_text("Let us know what we can do to help. Thanks!", reply_markup=ReplyKeyboardRemove(True))
    else:
        update.message.reply_text("IMO NAWNG", reply_markup=ReplyKeyboardRemove(True))

def suggest(update, context):
    update.message.reply_text("TEST SUGGEST")

def location_handler(update, context):
    buttons = [[KeyboardButton(yes_choice, request_location=True)], [KeyboardButton(no_choice)]]
    update.message.reply_text(
        "Do you want to share your location?",
        reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))

def location(update, context):
    user_location = update.message.location
    longitude = user_location.longitude
    latitude = user_location.latitude
    array = api_request.search_business(latitude=latitude, longitude=longitude, radius="5000")
    update.message.reply_text(
        f"""
        You are currently in LATITUDE: {latitude} and LONGITUDE: {longitude} Here are the restaurants near you:
        """,
        reply_markup=ReplyKeyboardRemove(True))

    for data in array:
        update.message.reply_text(text=f"[{data['name']}]({data['url']})", parse_mode="markdown")
        # update.message.reply_photo(photo=data['image_url'], caption=data['name'])


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
