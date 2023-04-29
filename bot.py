import logging
from telegram import ParseMode

from scripts.myip import what_my_ip
from scripts.password import password_generator

# create logger
# agar log yang ditulis ke bot.log memiliki nama logger yang sesuai dengan nama module/filename yang sedang dijalankan
logger = logging.getLogger(__name__)
# Dengan begitu, kita bisa membedakan log dari bot.py dengan log dari module lain jika ada.


def handle_start_command(update, context):
    try:
        welcome_message = """
🤖👋 Hi there\! Welcome to *Helper Bot*, your personal assistant at your fingertips\.

To get started, simply type /help to see what *Helper Bot* can do for you\.
        """
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=welcome_message, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception as e:
        logging.exception("Exception occurred in handle_start_command")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Sorry, I couldn't process your request at the moment. Please try again later.")


def handle_help_command(update, context):
    try:
        help_message = """
ℹ️ *Available commands:*
/start \- Start the bot
/ip \- Get your public IP address
/password \- Generate a secure password

ℹ️ *How to use:*
/start \- To start the bot and get the available commands
/ip \- To get your public IP address and location on Google Maps
/password \- To generate a secure password, you can specify the length of the password by typing /password \<length\>
        """
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=help_message, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception as e:
        error_message = "An error occurred while handling /help command"
        logger.exception(error_message)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Sorry, something went wrong. Please try again later.")


def handle_ip_command(update, context):
    try:
        # mendapatkan informasi lengkap tentang alamat IP publik pengguna
        ip_info = what_my_ip()
        lat = ip_info['loc'].split(',')[0]
        long = ip_info['loc'].split(',')[1]
        maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{long}"

        message = f"🌐 IP Address: {ip_info['ip']}\n"
        message += f"🔍 ISP: {ip_info['org']}\n"
        message += f"🏙️ City: {ip_info['city']}\n"
        message += f"🌍 Region: {ip_info['region']}\n"
        message += f"🗺️ Country: {ip_info['country']}\n"
        message += f"🌞 Latitude: {lat}\n"
        message += f"🌜 Longitude: {long}"
        message += f"\n\n🌐 View on <a href='{maps_url}'>Google Maps</a>"

        # update.message.reply_html(message)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=message, parse_mode=ParseMode.HTML)

    except Exception as e:
        logger.exception("Error handling /ip command")
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="An error occurred. Please try again later.")


def handle_password_command(update, context):
    try:
        # mengambil panjang password dari argumen
        if len(context.args) > 0:
            length = int(context.args[0])
            # memvalidasi panjang password
            if length < 12 or length > 256:
                raise ValueError(
                    "Password length should be an integer between 12 and 256.")
        else:
            length = 12

        # membuat password acak
        password = password_generator(length)

        # send the generated password to the user
        message = "🔒 Here's your new password:\n\n"
        message += f"{password}\n\n"
        message += "Please make sure to use a unique and secure password."
        context.bot.send_message(
            chat_id=update.message.chat_id, text=message, disable_web_page_preview=True)

    except ValueError as e:
        logger.error(str(e))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Invalid password length. Password length should be an integer between 12 and 256.")

    except Exception as e:
        logger.error(str(e))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Sorry, an error occurred while processing your request.")
