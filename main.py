import os
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Updater
import logging
import datetime
from bot import handle_start_command, handle_profile_command, handle_password_command, \
    handle_help_command, handle_server_command, handle_unshort_command, handle_whois_command, \
    handle_wa_command, handle_lookup_command, handle_email_command

# Load environment variables from .env file
load_dotenv()

# Enable logging
# Read the LOG_FILE_PATH value from the .env file
log_file_path = os.getenv('LOG_FILE_PATH')

# # Configure logging
# logging.basicConfig(
#     level=logging.ERROR,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler(log_file_path),
#         logging.StreamHandler() # stream error message to console
#     ]
# )

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.handlers.RotatingFileHandler(
            filename=log_file_path,
            maxBytes=10*1024*1024,
            backupCount=5
        ),
        logging.StreamHandler()
    ]
)

# # Example usage error
# try:
#     # some code that might raise an exception
#     raise ValueError('Invalid value')
# except ValueError as e:
#     logging.error(str(e))


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
    # ger profile user
    bot.add_handler(CommandHandler("profile", handle_profile_command))
    # passwor generator
    bot.add_handler(CommandHandler('password', handle_password_command))
    # info server
    bot.add_handler(CommandHandler('server', handle_server_command))
    # unshorten URL
    bot.add_handler(CommandHandler('unshort', handle_unshort_command))
    # whois
    bot.add_handler(CommandHandler('whois', handle_whois_command))
    # wa
    bot.add_handler(CommandHandler('wa', handle_wa_command))
    # lookup
    bot.add_handler(CommandHandler('lookup', handle_lookup_command))
    # email
    bot.add_handler(CommandHandler('email', handle_email_command))

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
