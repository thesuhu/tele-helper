import os
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Updater
import logging
import datetime
from bot import handle_start_command, handle_ip_command, handle_password_command, handle_help_command

# Load environment variables from .env file
load_dotenv()

# Enable logging
# Read the LOG_FILE_PATH value from the .env file
log_file_path = os.getenv('LOG_FILE_PATH')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        # logging.StreamHandler()
    ]
)


def main():
    # baca telegram token from env
    telegram_bot_token = os.getenv("TELEGRAM_BOT_API_KEY")

    # inisialisasi bot
    updater = Updater(token=telegram_bot_token, use_context=True)
    bot = updater.dispatcher

    # Add handlers for Telegram Bot commands
    bot.add_handler(CommandHandler("start", handle_start_command))
    # help handler
    bot.add_handler(CommandHandler("help", handle_help_command))
    # menambahkan handler untuk perintah /ip
    bot.add_handler(CommandHandler("ip", handle_ip_command))
    # passwor generator
    bot.add_handler(CommandHandler('password', handle_password_command))

    # start bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    print(f'Starting Helper Bot... {datetime.datetime.now()}')
    try:
        main()
    except Exception as e:
        # Log the error
        logging.error(
            "An error occurred while starting Helper Bot: %s", str(e))
        print("Oops! An error occurred while starting Helper Bot. Please check the logs for more information.")
