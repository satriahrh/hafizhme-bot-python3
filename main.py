from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
from time import time

import logging
import os


load_dotenv()

# OR, the same with increased verbosity:
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only
env_path = '.env'
load_dotenv(dotenv_path=env_path)

TOKEN=os.getenv('TOKEN')
WAKTU_KERJA=int(os.getenv('WAKTU_KERJA'))
INTERVAL_PULANG=int(os.getenv('INTERVAL_PULANG'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    message = "Hafizhme Bot Python3"
    message += "\n"
    message += "\n/kerja Untuk mulai kerja selama 9 jam"
    update.message.reply_text(message)


def pulang_kerja(bot, job):
    """Pengingat pulang kerja"""
    message = "Waktunya pulaaang!!!"
    message += "\n"
    message += "\n/beres_kerja untuk mengakhiri hari ini :D"
    bot.send_message(job.context, text=message)


def kerja(bot, update, job_queue, chat_data):
    """Mulai kerja"""
    chat_id = update.message.chat_id
    try:
        # Add job to queue
        job = job_queue.run_repeating(pulang_kerja, interval=INTERVAL_PULANG, first=WAKTU_KERJA, context=chat_id)
        chat_data['kerja'] = {
            'job': job,
            'mulai kerja': time()
        }

        message = "Bismillahirrahmanirrahim, selamat kerja!!"
        message += "\n"
        message += "\n/gajadi_kerja Untuk menunda kerja"
        message += "\n/beres_kerja Untuk untuk mengakhiri kerja"
        update.message.reply_text(message)

    except (IndexError, ValueError):
        update.message.reply_text('/kerja untuk mulai kerja')


def gajadi_kerja(bot, update, chat_data):
    """Cancel kerja"""
    if 'kerja' not in chat_data:
        update.message.reply_text('Kamu belum mulai kerja')
        return

    job = chat_data['kerja']['job']
    job.schedule_removal()
    del chat_data['kerja']

    message = "Kamu belum mau kerja"
    message += "\n"
    message += "\nKalau udah siap, jangan lupa /kerja"
    update.message.reply_text(message)


def beres_kerja(bot, update, chat_data):
    if 'kerja' not in chat_data:
        update.message.reply_text('Kamu belum mulai kerja')
        return

    if time() - chat_data['kerja']['mulai kerja'] < WAKTU_KERJA:
        update.message.reply_text('Kamu masih harus kerja')
        return

    job = chat_data['kerja']['job']
    job.schedule_removal()
    del chat_data['kerja']

    message = "Hati-hati di jalan yaaah :*"
    message += "\n"
    message += "\nJangan lupa chat @Astifvani"
    update.message.reply_text(message)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Run bot."""
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("kerja", kerja,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("gajadi_kerja", gajadi_kerja, pass_chat_data=True))
    dp.add_handler(CommandHandler("beres_kerja", beres_kerja, pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
