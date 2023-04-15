import requests
import os
from telegram.ext import Updater, CommandHandler
from dotenv.main import load_dotenv
from utils import get_charges, get_balance

# Retrieve configuration variables from .env file
load_dotenv()
URL = os.environ['URL']
LINODE_API_KEY = os.environ['LINODE_API_KEY']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

# Set up the Telegram bot
updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

headers = {
    "Authorization": f"Bearer {LINODE_API_KEY}",
    "Content-Type": "application/json"
}

# Define command handlers
def charges_handler(update, context):
    charges = get_charges(headers, requests, URL)
    message = f"Accrued charges: {charges:.2f} USD"
    update.message.reply_text(message)


def balance_handler(update, context):
    balance = get_balance(headers, requests, URL)
    message = f"Current balance: {balance:.2f} USD"
    update.message.reply_text(message)


def ping(update, context):
    message = "Pong!"
    update.message.reply_text(message)


# Register the commands in a handler
dispatcher.add_handler(CommandHandler("balance", balance_handler))
dispatcher.add_handler(CommandHandler("charges", charges_handler))
dispatcher.add_handler(CommandHandler("ping", ping))

# Start the bot
updater.start_polling()
updater.idle()
