import logging
import datetime
from google_images_download import google_images_download   #importing the library
from PIL import Image
import os
import random
import dill
from threading import Event
from time import time
from datetime import timedelta
import wikipedia

from telegram.ext import Updater, CommandHandler, DictPersistence, MessageHandler, Filters
from telegram import ChatAction
import telegram
from telegram.ext.dispatcher import run_async

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

@run_async
def start(update, context):
    if "books" in context.user_data.keys():
        if context.user_data['books'] > datetime.datetime.now():
            update.message.reply_text(text="I'm old, i can't find this many books... try in {}".format(context.user_data['books'] - datetime.datetime.now()))
            return
        else:
            context.user_data['books'] = datetime.datetime.now() + datetime.timedelta(seconds=30)
    else:
        context.user_data['books'] = datetime.datetime.now() + datetime.timedelta(seconds=30)
    
    try:
        wikipedia.set_lang("pt")
        random = wikipedia.random()
        random_article = wikipedia.summary(random)
        update.message.reply_text("{}\n\n{}".format(random,random_article))
    except Exception as e:
        print(str(e))


    
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    pp = DictPersistence()
    updater = Updater("1057036633:AAGpEpnOCMiYi9yQR_35NZp4NHg3uhYKTOo", persistence=pp, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("trivia", start))


    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()




if __name__ == '__main__':
    main()