import telegram
import requests
import os
from telegram.ext import Updater, CommandHandler
from linode_api4 import LinodeClient
from dotenv.main import load_dotenv

# Set up the Linode API client from .env file
load_dotenv()
URL = os.environ['URL']
LINODE_API_KEY = os.environ['LINODE_API_KEY']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
client = LinodeClient(LINODE_API_KEY)
bot = telegram.Bot(TELEGRAM_BOT_TOKEN)

headers = {
    "Authorization": f"Bearer {LINODE_API_KEY}",
    "Content-Type": "application/json"
}

# Define a function to retrieve the accrued charges and balance from Linode


def get_charges():
    response = requests.get(URL, headers=headers)
    accrued_charges = response.json()["balance_uninvoiced"]
    return accrued_charges


def get_balance():
    response = requests.get(URL, headers=headers)
    balance = response.json()["balance"]
    return balance

# Define a function for handlers


def charges_handler(update, context):
    charges = get_charges()
    message = "Accrued charges:\n"
    update.message.reply_text(message + str(charges))


def balance_handler(update, context):
    balance = get_balance()
    message = "Balance:\n"
    update.message.reply_text(message + str(balance))


def ping(update, context):
    message = "Pong!"
    update.message.reply_text(message)


# Set up the Telegram bot
updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Register the commands in a handler
dispatcher.add_handler(CommandHandler("balance", balance_handler))
dispatcher.add_handler(CommandHandler("charges", charges_handler))
dispatcher.add_handler(CommandHandler("ping", ping))

# Start the bot
updater.start_polling()
updater.idle()
