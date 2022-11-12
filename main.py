from telegram.ext import Updater, CommandHandler

with open('token.txt', 'r') as f:
    TOKEN = f.read()

def start(update, context):
    update.message.reply_text("Hello! Welcome to Tindero, your restaurant guide!")

def help(update, context):
    update.message.reply_text("""
    The following commands are available:

    /start -> Start Tindero
    /help -> This message
    """)

updater = Updater(TOKEN, use_context=True)
disp = updater.dispatcher

disp.add_handler(CommandHandler("start", start))
disp.add_handler(CommandHandler("help", help))

updater.start_polling()
updater.idle()
