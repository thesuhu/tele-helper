# Tele Helper

Telegram bot built with Python that provides a set of useful tools to help you.

## Usage

Clone this repository and install these dependencies by running the following command:

```sh
pip install -r requirements.txt
```

Rename file `.env-example` to `.env` and edit the file. Paste your [Telegram Bot](https://web.telegram.com) api key. To use all feature, please provide optional environment into `.env` file

```text
TELEGRAM_BOT_API_KEY=
```

Start the bot by running this command:

```sh
python3 main.py
```

After running the bot, get help on the available commands using the /help command.

## Commands

Below is a list of available commands that are grouped by category. Please use the appropriate command for your needs.

### General

| Command | Description | How to |
| --- | --- | --- |
| /start | Start the bot | To start the bot |
| /help | Show list of available commands and their usage instructions | To show the list of available commands and their usage instructions |
| /profile | Get your user profile information | To get your user profile information |
| /password | Generate a secure password | To generate a secure password, you can specify the length of the password by typing /password `<length>` |
| /wa | Send a WhatsApp message without saving the number | To send a WhatsApp message without saving the number, type /wa `<phone_number>` |

### OSINT

| Command | Description | How to |
| --- | --- | --- |
| /unshort | Unshorten a shortened URL | To unshorten a shortened URL, type /unshort `<URL>` |
| /whois | Look up domain registration details (admin only) | To look up domain registration details, type /whois `<domain name>` |
| /lookup | Look up information about a domain or IP address (admin only) | To look up information about a domain or IP address, type /lookup `<domain or IP>` |
| /email | Verify an email address (admin only) | To verify an email address, type /email `<email address>` |

### Admin

| Command | Description | How to |
| --- | --- | --- |
| /server | Get server information (admin only) | To get server information |

## Ways to Support

If you find this useful, please ⭐ the repository. Any feedback is welcome.

You can contribute or you want to, feel free to [**Buy me a coffee! :coffee:**](https://www.buymeacoffee.com/thesuhu), I will be really thankfull for anything even if it is a coffee or just a kind comment towards my work, because that helps me a lot.

Alternatively, you can also [**Sawer**](https://saweria.co/thesuhu) if you prefer that platform.
