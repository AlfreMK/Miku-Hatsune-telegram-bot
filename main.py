import logging
from os import environ
from dotenv import load_dotenv
import datetime
from functions import get_random_video

from telegram import __version__ as TG_VER
from telegram import __version_info__
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext, JobQueue, Updater

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# code extracted and adapted from https://docs.python-telegram-bot.org/en/stable/examples.timerbot.html

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi! Use /set to receive every day the daily song of the day.")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.jobs()
    if not current_jobs:
        return False
    for job in current_jobs:
        if name == str(job.chat_id):
            job.schedule_removal()
    return True


async def callback_minute(context: CallbackContext):
    job = context.job
    random_video = get_random_video()
    await context.bot.send_message(chat_id=job.chat_id,
                             text=f'Song of the day: {random_video}')


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    # context.job_queue.run_repeating(callback_minute, chat_id=chat_id, interval=5, first=1)
    # context.job_queue.run_once(callback_minute, due, chat_id=chat_id, name=str(chat_id), data=due)
    context.job_queue.run_daily(callback_auto_message, time=datetime.time(hour=0, minute=0), days=(0, 1, 2, 3, 4, 5, 6), context=chat_id)
    text = "Daily song successfully set!"
    if job_removed:
        text += " Old one was removed."
    await update.effective_message.reply_text(text)


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Daily song successfully unset!" if job_removed else "You have no active daily song."
    await update.message.reply_text(text)


def main() -> None:
    """Start the bot."""
    load_dotenv(".env")
    API_KEY = environ['API_KEY']
    application = Application.builder().token(API_KEY).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))


    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()