# Tele Helper

Telegram bot built with Python that provides a set of useful tools to help you.

## Usage

Clone this repository and install these dependencies by running the following command:

```sh
pip install -r requirements.txt
```

Rename file `.env-example` to `.env` and edit the file. Paste your [Telegram Bot](https://web.telegram.com) api key:

```
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
| /start | Start the bot | To start the bot and get the available commands |
| /profile | Get your user profile information | To get your user profile information |
| /password | Generate a secure password | To generate a secure password, you can specify the length of the password by typing /password <length> |

### OSINT

| Command | Description | How to |
| --- | --- | --- |
| /unshort | Unshorten a shortened URL | To unshorten a shortened URL, type /unshort <URL> |

### Admin

| Command | Description | How to |
| --- | --- | --- |
| /server | Get server information (admin only) | To get server information (admin only) |

