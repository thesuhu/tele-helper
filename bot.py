import logging
import os
from dotenv import load_dotenv
import requests
from telegram import ParseMode

from scripts.myip import what_my_ip
from scripts.password import password_generator

# create logger
# agar log yang ditulis ke bot.log memiliki nama logger yang sesuai dengan nama module/filename yang sedang dijalankan
logger = logging.getLogger(__name__)
# Dengan begitu, kita bisa membedakan log dari bot.py dengan log dari module lain jika ada.

# Load environment variables from .env file
load_dotenv()

authorized_users_str = os.getenv('INIT_AUTHORIZED_USERS')
authorized_users_list = authorized_users_str.split(',')

def get_authorized_users_list():
    return authorized_users_list

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
/profile \- Get your user profile information
/password \- Generate a secure password
/server \- Get server information \(admin only\)

ℹ️ *How to use:*
/start \- To start the bot and get the available commands
/profile \- To get your user profile information
/password \- To generate a secure password, you can specify the length of the password by typing /password \<length\>
/server \- To get server information \(admin only\)

Note: Some commands may not be available depending on your access level\.
        """
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=help_message, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception as e:
        error_message = "An error occurred while handling /help command"
        logger.exception(error_message)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Sorry, something went wrong. Please try again later. 😞")


def handle_server_command(update, context):
    try:
        # validasi pengguna
        authorized_users_list = get_authorized_users_list()
        if str(update.message.chat_id) not in authorized_users_list:
                context.bot.send_message(chat_id=update.message.chat_id,
                                        text="⚠️ Sorry, only authorized users are allowed to use this command.")
        else:
            # mendapatkan ip server
            ip_info = what_my_ip()
            lat = ip_info['loc'].split(',')[0]
            long = ip_info['loc'].split(',')[1]
            maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{long}"

            message = "🖥️ Here's some information about your server:\n\n"
            message += f"🌐 IP Address: {ip_info['ip']}\n"
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
        logger.exception("Error handling /server command")
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="An error occurred. Please try again later.")


def handle_profile_command(update, context):
    try:
        # Get sender's profile information
        chat_id = update.message.chat_id
        # message_id = update.message.message_id
        bot_token = context.bot.token

        # Create URL to retrieve user's profile information
        url = f"https://api.telegram.org/bot{bot_token}/getChat?chat_id={chat_id}"

        # Send GET request to Telegram Bot API with chat_id parameter
        response = requests.get(url)

        # Convert response to JSON format
        data = response.json()

        # Check if the response is successful
        if data["ok"]:
            # Create an interesting text from user's profile information
            user_profile = f"🧑 Here's some information about your profile:\n\n"
            user_profile += f"🆔 ID: {data['result']['id']}\n"
            user_profile += f"👤 First Name: {data['result']['first_name']}\n"
            user_profile += f"👥 Last Name: {data['result']['last_name']}\n"
            user_profile += f"🆔 Username: @{data['result']['username']}\n"
            user_profile += f"👤 User Type: {data['result']['type']}\n"
            user_profile += f"📝 Bio: {data['result']['bio']}\n"
            user_profile += f"📷 Profile Photo: <a href='tg://user?id={data['result']['id']}' target='_blank'>View</a>\n"

            # Send the created text to the user
            context.bot.send_message(
                chat_id=chat_id, text=user_profile, parse_mode="HTML")
        else:
            # If the response is not successful, send an error message to the user
            context.bot.send_message(
                chat_id=chat_id, text="Sorry, there was an error retrieving user profile. Please try again later.")
    except Exception as e:
        # If there is an error, log the error and send an error message to the user
        logger.exception("Error getting user profile")
        context.bot.send_message(
            chat_id=chat_id, text="Sorry, there was an error retrieving user profile. Please try again later. 😔")


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
        message += "🔒 Please make sure to use a unique and secure password\."
        message = "Here's your new password:\n\n"
        message += f"{password}"
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
