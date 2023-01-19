import configparser
from pymongo import MongoClient
from api_requests import Requests as api_request
from db_requests import DB_requests as db_request
from telegram import \
    KeyboardButton, \
    ReplyKeyboardMarkup,\
    ReplyKeyboardRemove
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler

# Setting up Config
config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config.get('default', "bot_api")

# Setting up DB
USERNAME = config.get('default', 'username')
PASSWORD = config.get('default', 'password')
DATABASE_NAME = config.get('default', "db_name")
RESTAURANTS = config.get('default', "restaurants")
USERS = config.get('default', "users")

# Start the Client (MongoDB)
url = f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.hhwhphl.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)

# Variables
yes_choice = "Yes"
no_choice = "No"
user_location = ""
db = []
restaurant = []
users = []

def start(update, context):
    buttons = [[KeyboardButton(yes_choice)], [KeyboardButton(no_choice)]]
    update.message.reply_text("""
    Hello! Welcome to Tindero, your restaurant guide!
    Should I start suggesting restaurants?
    """, reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))
    data = {'_id': update.message.chat.id, 'username': update.message.chat.username}
    db_request.insert_data_to_collection(users, data)

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
        suggest(update, context)
    if no_choice in update.message.text:
        update.message.reply_text("Let us know what we can do to help. Thanks!", reply_markup=ReplyKeyboardRemove(True))
    else:
        update.message.reply_text("Hello!", reply_markup=ReplyKeyboardRemove(True))

def suggest(update, context):
    update.message.reply_text("TEST SUGGEST")

def location_handler(update, context):
    buttons = [[KeyboardButton(yes_choice, request_location=True)], [KeyboardButton(no_choice)]]
    update.message.reply_text(
        """Tindero would like to get access to your location for more accurate recommendation.
        Do you want to share your location?""",
        reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))

def location(update, context):
    user_location = update.message.location
    longitude = user_location.longitude
    latitude = user_location.latitude
    array = api_request.search_business(latitude=latitude, longitude=longitude, radius="5000")
    update.message.reply_text(
        f"""
        You are currently in LATITUDE: {latitude} and LONGITUDE: {longitude}
        We are currently collecting restaurants near you!
        """,
        reply_markup=ReplyKeyboardRemove(True))

    for data in array:
        db_request.insert_data_to_collection(restaurant, data)

def error(update, context):
    print(f'Update {update} caused error: {context.error}')

if __name__ == '__main__':
    # Connect to DB
    try:
        db = client[DATABASE_NAME]
        restaurant = db[RESTAURANTS]
        users = db[USERS]

        # client.run_until_disconnected()

    except Exception as e:
        print('Cause: {}'.format(e))

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("suggest", suggest))
    dp.add_handler(CommandHandler("location", location_handler))

    # Messages
    dp.add_handler(MessageHandler(Filters.location, location))
    dp.add_handler(MessageHandler(Filters.text, message_handler))

    # Errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
