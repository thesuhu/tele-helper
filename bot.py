import logging
import os
import re
from dotenv import load_dotenv
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from scripts.myip import what_my_ip
from scripts.password import password_generator
from scripts.unshorten import unshorten_url
from scripts.whois_lookup import ip_lookup, print_whois
from scripts.email import verify_email

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
📋 *Commands*

Below is a list of available commands that are grouped by category\. Please use the appropriate command for your needs\.

🌟 *General*

/start \- Start the bot
/profile \- Get your user profile information
/password \- Generate a secure password
/wa \- Send a WhatsApp message without saving the phone number

🔍 *OSINT*

/unshort \- Unshorten a shortened URL
/whois \- Get WHOIS information about a domain \(admin only\)
/lookup \- Look up information about a domain or IP address \(admin only\)
/email \- Verify the existence of an email address \(admin only\)

👑 *Admin*

/server \- Get server information \(admin only\)

📝 *How to use*

To view the full usage instructions, please click on this link to access the [README](https://github\.com/thesuhu/tele-helper/blob/master/README\.md)\.

Note: Some commands may not be available depending on your access level\.
        """

        context.bot.send_message(chat_id=update.message.chat_id, text=help_message,
                                 parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)

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
            message += f"🏙️ Region: {ip_info['region']}\n"
            message += f"🌍 Country: {ip_info['country']}\n"
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
            if length < 12 or length > 50:
                raise ValueError(
                    "Invalid password length. Password length should be an integer between 12 and 50.")
        else:
            length = 12

        # membuat password acak
        password = password_generator(length)

        # send the generated password to the user
        message = "🔒 Please make sure to use a unique and secure password. "
        message += "Here's your new password:\n\n"
        message += f"<code>{password}</code>"
        message += "\n\nTo copy your new password to your clipboard, please press and hold on the password above."
        context.bot.send_message(
            chat_id=update.message.chat_id, text=message, disable_web_page_preview=True, parse_mode=ParseMode.HTML)

    except ValueError as e:
        logger.error(str(e))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str(e))
    except Exception as e:
        logger.error(str(e))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Sorry, an error occurred while processing your request.")


def handle_unshort_command(update, context):
    try:
        # get first parameter
        if len(context.args) == 0:
            raise ValueError(
                "Please provide a URL to unshorten. Send me the URL you want to unshorten in the format: /unshorten <URL>")

         # Get the original URL
        url = unshorten_url(context.args[0])

        # Send the original URL back to the user
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f"🌐 Here is the original URL:\n\n {url}")
    except ValueError as e:
        logger.error(str(e))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str(e))
    except Exception as e:
        logger.error(str(e))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Sorry, an error occurred while processing your request.")


def get_country_flag(country_code):
    OFFSET = 127397
    codepoints = tuple(ord(char) + OFFSET for char in country_code.upper())
    return chr(codepoints[0]) + chr(codepoints[1])

# check if the field is a list of datetime objects


def list_or_str(dt):
    if isinstance(dt, list):
        return ', '.join(str(d) for d in dt)
    else:
        return str(dt)


def handle_whois_command(update, context):
    try:
        # validasi pengguna
        authorized_users_list = get_authorized_users_list()
        if str(update.message.chat_id) not in authorized_users_list:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="⚠️ Sorry, only authorized users are allowed to use this command.")
        else:
            # get first parameter
            if len(context.args) == 0:
                raise ValueError(
                    "Please provide a domain name or IP address. Send me the domain name or IP address you want to look up in the format: /whois <domain or IP>")

            # get domain name from args
            domain_name = context.args[0]

            # get whois information
            whois_info = print_whois(domain_name)

            print(whois_info)

            # # check if the field is a list of datetime objects
            # def list_or_str(dt):
            #     if isinstance(dt, list):
            #         return ', '.join(str(d) for d in dt)
            #     else:
            #         return str(dt)

            # check if whois info is empty
            if 'registrar' in whois_info and (whois_info['registrar']) is None:
                response_message = f"❌ Sorry, the domain name '{domain_name}' does not seem to be valid. Please enter a valid domain name."
            else:
                # format response message with whois info
                response_message = "🔍 Here's some information about the domain you requested:\n\n"

            # format response message
            if 'domain_id' in whois_info and whois_info['domain_id']:
                response_message += f"🌐 Domain ID: {whois_info['domain_id']}\n"
            if 'domain_name' in whois_info and whois_info['domain_name']:
                response_message += f"🌐 Domain Name: {list_or_str(whois_info['domain_name'])}\n"
            if 'registrar' in whois_info and whois_info['registrar']:
                response_message += f"🔍 Registrar: {whois_info['registrar']}\n"
            if 'org' in whois_info and whois_info['org']:
                response_message += f"🏢 Organization: {whois_info['org']}\n"
            if 'state' in whois_info and whois_info['state']:
                response_message += f"🏙️ State: {whois_info['state']}\n"
            if 'country' in whois_info and whois_info['country']:
                response_message += f"🌍 Country: {whois_info['country']} {get_country_flag(whois_info['country'])}\n"
            if 'emails' in whois_info and whois_info['emails']:
                response_message += f"📧 Emails: {list_or_str(whois_info['emails'])}\n"
            if 'registrar_city' in whois_info and whois_info['registrar_city']:
                response_message += f"🏙️ Registrar city: {whois_info['registrar_city']}\n"
            if 'registrar_postal_code' in whois_info and whois_info['registrar_postal_code']:
                response_message += f"📮 Registrar postal code: {whois_info['registrar_postal_code']}\n"
            if 'registrar_country' in whois_info and whois_info['registrar_country']:
                response_message += f"🌍 Registrar country: {whois_info['registrar_country']} {get_country_flag(whois_info['registrar_country'])}\n"
            if 'registrar_phone' in whois_info and whois_info['registrar_phone']:
                response_message += f"📞 Registrar phone: {whois_info['registrar_phone']}\n"
            if 'registrar_email' in whois_info and whois_info['registrar_email']:
                response_message += f"📧 Registrar email: {whois_info['registrar_email']}\n"
            if 'status' in whois_info and whois_info['status']:
                response_message += f"📈 Status: {list_or_str(whois_info['status'])}\n"
            if 'creation_date' in whois_info and whois_info['creation_date']:
                response_message += f"🕒 Creation date: {list_or_str(whois_info['creation_date'])}\n"
            if 'updated_date' in whois_info and whois_info['updated_date']:
                response_message += f"🕒 Updated date: {list_or_str(whois_info['updated_date'])}\n"
            if 'expiration_date' in whois_info and whois_info['expiration_date']:
                response_message += f"🕒 Expiration date: {list_or_str(whois_info['expiration_date'])}\n"
            if 'name_servers' in whois_info and whois_info['name_servers']:
                response_message += f"🔧 Name servers: {list_or_str(whois_info['name_servers'])}\n"
            if 'dnssec' in whois_info and whois_info['dnssec']:
                response_message += f"🔒 DNSSEC: {whois_info['dnssec']}\n"

            # send message
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=response_message, parse_mode=ParseMode.HTML)

    except ValueError as e:
        logger.error(str(e))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str(e))
    except Exception as e:
        logger.error(str(e))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Sorry, an error occurred while processing your request.")


def handle_wa_command(update, context):
    try:
        # Check if phone number parameter is provided
        if len(context.args) == 0:
            raise ValueError("Please provide a phone number.")

        # Get phone number from the arguments
        phone_number = context.args[0]

        # Check if the phone number is valid or not
        if not re.match(r"^(?:\+62|0)[2-9][0-9]{6,10}$", phone_number):
            raise ValueError("Invalid phone number format.")

        # Add Indonesian country code if the phone number is not in international format
        if phone_number.startswith("0"):
            phone_number = "+62" + phone_number[1:]

        # Create the WhatsApp message URL
        wa_url = f"https://wa.me/{phone_number}"

        # Create the WhatsApp message URL
        wa_url = f"https://wa.me/{phone_number}"
        button_text = "Send WhatsApp Message"
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(button_text, url=wa_url)]])
        message = f"📱 Please click the following button to send a message to {phone_number} on WhatsApp:"
        context.bot.send_message(chat_id=update.message.chat_id, text=message, reply_markup=reply_markup)

    except ValueError as e:
        logger.error(str(e))
        context.bot.send_message(chat_id=update.message.chat_id, text=str(e))

    except Exception as e:
        logger.error(str(e))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Sorry, an error occurred while processing your request.")


def handle_lookup_command(update, context):
    try:
        # validasi pengguna
        authorized_users_list = get_authorized_users_list()
        if str(update.message.chat_id) not in authorized_users_list:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="⚠️ Sorry, only authorized users are allowed to use this command.")
        else:
            # get first parameter
            if len(context.args) == 0:
                raise ValueError(
                    "Please provide an IP address. Send me the IP address you want to look up in the format: /ip <IP address>")

            # get IP address from args
            ip_address = context.args[0]

            # get IP location information
            ip_info = ip_lookup(ip_address)

            # # check if the field is a list of values
            # def list_or_str(lst):
            #     if isinstance(lst, list):
            #         return ', '.join(str(d) for d in lst)
            #     else:
            #         return str(lst)

            # check if IP info is empty
            if not ip_info:
                response_message = f"❌ Sorry, I could not find information about the IP address '{ip_address}'. Please enter a valid IP address."
            else:
                # format response message with IP info
                response_message = "🔍 Here's some information about the IP address you requested:\n\n"

            # format response message
            if 'ip_address' in ip_info and ip_info['ip_address']:
                response_message += f"🌐 IP Address: {ip_info['ip_address']}\n"
            if 'hostname' in ip_info and ip_info['hostname']:
                response_message += f"🔍 Hostname: {ip_info['hostname']}\n"
            if 'city' in ip_info and ip_info['city']:
                response_message += f"🏙️ City: {ip_info['city']}\n"
            if 'region' in ip_info and ip_info['region']:
                response_message += f"🏞️ Region: {ip_info['region']}\n"
            if 'country' in ip_info and ip_info['country']:
                response_message += f"🌍 Country: {ip_info['country']} {get_country_flag(ip_info['country'])}\n"
            if 'latitude' in ip_info and ip_info['latitude'] and 'longitude' in ip_info and ip_info['longitude']:
                response_message += f"🌍 Coordinates: ({ip_info['latitude']}, {ip_info['longitude']})\n"
            if 'postal_code' in ip_info and ip_info['postal_code']:
                response_message += f"📮 Postal Code: {ip_info['postal_code']}\n"
            if 'timezone' in ip_info and ip_info['timezone']:
                response_message += f"🕒 Timezone: {ip_info['timezone']}\n"
            if 'asn' in ip_info and ip_info['asn']:
                response_message += f"🛡️ ASN: {ip_info['asn']}\n"
            if 'asn_org' in ip_info and ip_info['asn_org']:
                response_message += f"🏢 ASN Organization: {ip_info['asn_org']}\n"
            if 'isp' in ip_info and ip_info['isp']:
                response_message += f"📶 ISP: {ip_info['isp']}\n"

            # send message
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=response_message, parse_mode=ParseMode.HTML)

    except ValueError as e:
        logger.error(str(e))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str(e))
    except Exception as e:
        logger.error(str(e))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Sorry, an error occurred while processing your request.")


def is_valid_email(email):
    """
    Returns True if email format is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def handle_email_command(update, context):
    try:
        # validasi pengguna
        authorized_users_list = get_authorized_users_list()
        if str(update.message.chat_id) not in authorized_users_list:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="⚠️ Sorry, only authorized users are allowed to use this command.")
        else:
            # get first parameter
            if len(context.args) == 0:
                raise ValueError(
                    "Please provide an email address. Send me the email address you want to verify in the format: /email <email address>")

            email = context.args[0]
            # validate email format
            if not is_valid_email(email):
                raise ValueError(
                    "Invalid email format"
                )
            hunter_api_key = os.getenv('HUNTER_API_KEY')
            result = verify_email(email, hunter_api_key)
            # print(result)
            if 'data' in result:
                data = result['data']
                message = f"📩 Email verification result:\n\n"
                message += f"📧 Email Address: {data['email']}\n"
                message += f"🔍 Verification Status: {data['status']}\n"
                message += f"🚪 Mailbox Status: {data['result']}\n"
                message += f"📈 Confidence Score: {data['score']}\n"
                message += f"🔒 Is the Email a Catchall: {'Yes' if data['accept_all'] else 'No'}\n"
                message += f"❌ Is the Email Blocked: {'Yes' if data['block'] else 'No'}\n"
                message += f"🌐 Sources: {', '.join(data['sources'])}\n"
                message += f"🤖 Is the Email a Gibberish: {'Yes' if data['gibberish'] else 'No'}\n"
                message += f"🗑️ Is the Email Disposable: {'Yes' if data['disposable'] else 'No'}\n"
                message += f"🌐 Is the Email from a Webmail Provider: {'Yes' if data['webmail'] else 'No'}\n"
                message += f"📧 Does the Email have MX Records: {'Yes' if data['mx_records'] else 'No'}\n"
                message += f"📧 Is the SMTP Server Available: {'Yes' if data['smtp_server'] else 'No'}\n"
                message += f"📧 Can the SMTP Server Connect to the Email Address: {'Yes' if data['smtp_check'] else 'No'}\n"
                message += f"📧 Does the Email Address Follow the RFC Standard: {'Yes' if data['regexp'] else 'No'}\n"
                context.bot.send_message(chat_id=update.message.chat_id,
                                            text=message, parse_mode=ParseMode.HTML)
            elif 'errors' in result:
                error_message = f"❌ Failed to verify email: {result['errors'][0]['details']}"
                context.bot.send_message(chat_id=update.message.chat_id,
                                            text=error_message, parse_mode=ParseMode.HTML)

    except ValueError as e:
        logger.error(str(e))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str(e))
    except Exception as e:
        logger.error(str(e))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Sorry, an error occurred while processing your request.")
